from datetime import datetime, date, timedelta
from bson import ObjectId
from fastapi import FastAPI, Depends, HTTPException, Request, UploadFile, WebSocket, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from typing import List, Optional
from pydantic import parse_obj_as
from . import crud, models, schemas, database, auth, csrf, utils
from .auth import get_current_user
from .utils import registrar_atividade
import logging
from fastapi import status
import io
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import xlsxwriter
import secrets
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.datastructures import MutableHeaders
import os

# Importar e incluir o router de usuários
from .user_routes import router as user_router

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(user_router)

# Configuração de CORS
origins = [
    "http://localhost:8080",
    "http://localhost",
    "http://localhost:8000",
    "http://192.168.10.27",
    "http://192.168.10.27:8080",
    "http://192.168.1.5",
    "http://192.168.1.5:8000",
    "http://192.168.1.5:8080",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
    "*"  # Permitir todas as origens em desenvolvimento
]

# Definir modo de ambiente (desenvolvimento/produção)
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
# Defina para True para aplicar proteção CSRF mesmo em modo de desenvolvimento
ENFORCE_CSRF = os.environ.get("ENFORCE_CSRF", "False").lower() in ["true", "1", "yes"]

# Middleware para adicionar cabeçalhos de segurança
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Executar a requisição
            response = await call_next(request)

            # Adicionar ou atualizar cabeçalhos de segurança
            headers = dict(response.headers)
            
            # 1. Prevenir clickjacking
            headers["X-Frame-Options"] = "DENY"
            
            # 2. Prevenir MIME sniffing
            headers["X-Content-Type-Options"] = "nosniff"
            
            # 3. Habilitar proteção XSS no navegador
            headers["X-XSS-Protection"] = "1; mode=block"
            
            # 4. Referrer Policy - controlar informações enviadas na header Referer
            headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
            
            # 5. Configurações CSP (Content Security Policy)
            if ENVIRONMENT == "development":
                # Política mais permissiva para desenvolvimento
                headers["Content-Security-Policy"] = (
                    "default-src 'self'; "
                    "script-src 'self' 'unsafe-inline'; "
                    "style-src 'self' 'unsafe-inline'; "
                    "img-src 'self' data:; "
                    "connect-src 'self'; "
                    "font-src 'self'; "
                    "object-src 'none'; "
                    "media-src 'self'; "
                    "frame-src 'none'; "
                    "form-action 'self';"
                )
            else:
                # Política mais restritiva para produção
                headers["Content-Security-Policy"] = (
                    "default-src 'self'; "
                    "script-src 'self'; "
                    "style-src 'self'; "
                    "img-src 'self'; "
                    "connect-src 'self'; "
                    "font-src 'self'; "
                    "object-src 'none'; "
                    "media-src 'self'; "
                    "frame-ancestors 'none'; "
                    "form-action 'self';"
                )
                
                # 6. HSTS (Strict-Transport-Security) - apenas em produção
                headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
            
            # 7. Permissões - limitar recursos do navegador
            headers["Permissions-Policy"] = (
                "camera=(), "
                "microphone=(), "
                "geolocation=(), "
                "payment=()"
            )
            
            # Atualizar os cabeçalhos da resposta
            for key, value in headers.items():
                response.headers[key] = value
                
            # Log para verificar cabeçalhos aplicados
            logger.debug(f"Cabeçalhos de segurança aplicados: {dict(response.headers)}")
                
            return response
        except Exception as e:
            logger.error(f"Erro ao aplicar cabeçalhos de segurança: {e}")
            # Re-levantar a exceção para não ocultar erros
            raise

# Middleware para validar CSRF em métodos sensíveis
class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Caminhos que estão isentos de verificação CSRF
        exempt_paths = ["/token", "/security/csrf-token"]
        
        # Ignorar verificação CSRF para o endpoint de login, token CSRF e OPTIONS
        if request.url.path in exempt_paths or request.method == "OPTIONS":
            logger.info(f"CSRF ignorado para caminho isento: {request.url.path}")
            return await call_next(request)
            
        # Verificar CSRF apenas em métodos sensíveis
        if request.method in ("POST", "PUT", "DELETE", "PATCH"):
            # Tenta obter o token do header e cookie
            header_token = request.headers.get(csrf.CSRF_HEADER_NAME)
            cookie_token = request.cookies.get(csrf.CSRF_COOKIE_NAME)
            
            # Log detalhado para diagnóstico
            logger.info(f"[CSRF] Método: {request.method}, URL: {request.url.path}")
            logger.info(f"[CSRF] Token no header: {bool(header_token)}, Token no cookie: {bool(cookie_token)}")
            
            if header_token:
                logger.info(f"[CSRF] Primeiros 10 caracteres do token header: {header_token[:10] if len(header_token) >= 10 else header_token}...")
            if cookie_token:
                logger.info(f"[CSRF] Primeiros 10 caracteres do token cookie: {cookie_token[:10] if len(cookie_token) >= 10 else cookie_token}...")
            
            if not ENFORCE_CSRF and ENVIRONMENT == "development":
                # Modo permissivo para desenvolvimento (apenas logging)
                if not header_token or not cookie_token:
                    logger.warning(f"CSRF Warning: Token ausente - Header: {bool(header_token)}, Cookie: {bool(cookie_token)}")
                elif header_token != cookie_token:
                    logger.warning(f"CSRF Warning: Tokens não correspondem - Header: {header_token[:10] if len(header_token) >= 10 else header_token}..., Cookie: {cookie_token[:10] if len(cookie_token) >= 10 else cookie_token}...")
                else:
                    logger.info(f"[CSRF] Validação bem-sucedida para {request.url.path}")
            else:
                # Validação RIGOROSA (seja em produção ou desenvolvimento com ENFORCE_CSRF=True)
                if not header_token or not cookie_token:
                    logger.warning(f"CSRF Error: Token ausente - Header: {bool(header_token)}, Cookie: {bool(cookie_token)}")
                    return JSONResponse(
                        status_code=403, 
                        content={"detail": "CSRF token ausente. Recarregue a página e tente novamente."}
                    )
                elif header_token != cookie_token:
                    logger.warning(f"CSRF Error: Tokens não correspondem - Header: {header_token[:10] if len(header_token) >= 10 else header_token}..., Cookie: {cookie_token[:10] if len(cookie_token) >= 10 else cookie_token}...")
                    return JSONResponse(
                        status_code=403, 
                        content={"detail": "CSRF token inválido. Recarregue a página e tente novamente."}
                    )
                
                # Verificar a validade do token (expiração, formato)
                if not csrf.verify_csrf_token(header_token):
                    logger.warning(f"CSRF Error: Token inválido ou expirado")
                    return JSONResponse(
                        status_code=403, 
                        content={"detail": "CSRF token expirado ou inválido. Recarregue a página e tente novamente."}
                    )
                
                logger.info(f"[CSRF] Validação bem-sucedida para {request.url.path}")
        
        # Executar o próximo middleware ou rota
        response = await call_next(request)
        return response

# Usar a chave secreta do módulo CSRF
CSRF_SECRET = csrf.CSRF_SECRET_KEY
CSRF_COOKIE_NAME = csrf.CSRF_COOKIE_NAME
CSRF_HEADER_NAME = csrf.CSRF_HEADER_NAME

# Adicionar os middlewares na ordem correta
# 1. Primeiro o middleware de segurança para garantir que ele seja aplicado em todas as respostas
app.add_middleware(SecurityHeadersMiddleware)

# 2. Em seguida, o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost",
        "http://localhost:8000",
        "http://192.168.10.27",
        "http://192.168.10.27:8080",
        "http://192.168.1.5",
        "http://192.168.1.5:8000",
        "http://192.168.1.5:8080",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8080",
        "*"  # Permitir todas as origens em desenvolvimento
    ],  # Utilizando a lista de origens definida acima
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],  # Métodos específicos
    allow_headers=["*"],  # Permitir todos os cabeçalhos
    expose_headers=["Content-Type", "X-CSRF-Token"],
    max_age=86400,  # Cache preflight por 24 horas
)

# 3. Por último, o middleware CSRF
app.add_middleware(CSRFMiddleware)

# Endpoint para gerar e retornar o token CSRF
@app.get("/security/csrf-token")
async def get_csrf_token():
    token = csrf.generate_csrf_token()
    response = JSONResponse(content={"csrf_token": token})
    
    # Logs para depuração
    logger.info(f"Gerando novo token CSRF: {token[:10] if len(token) >= 10 else token}...")
    
    # Configurações de cookie baseadas no ambiente
    cookie_config = {
        "key": CSRF_COOKIE_NAME,
        "value": token,
        "max_age": 3600  # Expira em 1 hora
    }
    
    if ENVIRONMENT == "development":
        # Configurações mais permissivas para desenvolvimento
        cookie_config.update({
            "httponly": False,  # Permite acesso via JavaScript para testes
            "samesite": "lax",  # Menos restritivo
            "secure": False     # Não requer HTTPS
        })
    else:
        # Configurações seguras para produção
        cookie_config.update({
            "httponly": True,   # Previne acesso via JavaScript
            "samesite": "strict",  # Mais restritivo
            "secure": True      # Requer HTTPS
        })
    
    response.set_cookie(**cookie_config)
    
    # Adicionar o token também como um cabeçalho para facilitar testes
    response.headers["X-CSRF-Token"] = token
    
    return response

@app.middleware("http")
async def log_auth_middleware(request: Request, call_next):
    token = request.headers.get("Authorization")
    if token:
        logger.info(f"Token recebido: {token[:15]}...")
    else:
        logger.warning("Nenhum token fornecido")
    response = await call_next(request)
    return response

# Validação de formato de data
def validate_and_convert_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=f"Formato de data inválido: {date_str}. Esperado: yyyy-MM-dd."
        )

# Função para converter objetos datetime.date em datetime.datetime
def convert_dates_to_datetime(data_dict):
    """
    Converte todos os objetos datetime.date em datetime.datetime em um dicionário recursivamente.
    Isso é necessário porque o MongoDB não consegue serializar objetos datetime.date diretamente.
    
    Args:
        data_dict (dict): O dicionário com possíveis objetos date
        
    Returns:
        dict: O dicionário com todas as datas convertidas para datetime
    """
    if not isinstance(data_dict, dict):
        return data_dict
        
    result = {}
    for key, value in data_dict.items():
        if isinstance(value, date) and not isinstance(value, datetime):
            # Converter date para datetime
            result[key] = datetime.combine(value, datetime.min.time())
        elif isinstance(value, dict):
            # Processar dicionários aninhados
            result[key] = convert_dates_to_datetime(value)
        elif isinstance(value, list):
            # Processar listas
            result[key] = [convert_dates_to_datetime(item) if isinstance(item, dict) else item for item in value]
        else:
            # Manter outros valores inalterados
            result[key] = value
    
    return result

# Rota para login e geração de token
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: schemas.LoginRequest, request: Request, db=Depends(database.get_db)):
    logger.info(f"Tentativa de login para usuário: {form_data.username}")
    
    # Capturar IP e User-Agent
    ip_address = utils.get_client_ip(request)
    user_agent = request.headers.get("User-Agent", "Desconhecido")
    
    logger.info(f"Tentativa de login a partir do IP: {ip_address} | User-Agent: {user_agent[:50]}...")
    
    user = await auth.authenticate_user(db, form_data.username, form_data.senha)
    if not user:
        # Registrar atividade de login com falha
        await registrar_atividade(
            db=db,
            tipo="login",
            descricao=f"Tentativa de login falhou para o usuário: {form_data.username}",
            usuario_nome=form_data.username,
            ip_address=ip_address,
            user_agent=user_agent,
            dados_adicionais={
                "status": "falha",
                "motivo": "Credenciais inválidas"
            }
        )
        logger.warning(f"Credenciais inválidas fornecidas para usuário: {form_data.username} - IP: {ip_address}")
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Registrar atividade de login bem-sucedido
    await registrar_atividade(
        db=db,
        tipo="login",
        descricao=f"Login bem-sucedido para o usuário: {user['nome']}",
        usuario_nome=user["nome"],
        ip_address=ip_address,
        user_agent=user_agent,
        dados_adicionais={
            "status": "sucesso"
        }
    )
    
    # Gerar dados para o token
    data = {
        "sub": user["username"],
        "nome": user["nome"],
        "tipo_usuario": user.get("tipo_usuario", "comum"),
        "setor": user.get("setor", "")
    }
    
    # Criar token de acesso
    access_token = auth.create_access_token(data=data)
    
    logger.info(f"Token gerado com sucesso para {user['nome']} com tipo {user.get('tipo_usuario')} - IP: {ip_address}")
    
    # Retornar o token e os dados do usuário
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "nome": user["nome"],
        "tipo_usuario": user.get("tipo_usuario", "comum"),
        "setor": user.get("setor", "")
    }

# Rota para validação de token
@app.get("/auth/validate-token")
async def validate_token(token: str = Depends(auth.oauth2_scheme), db=Depends(database.get_db)):
    try:
        user = await auth.get_current_user(token=token, db=db)
        
        # Log detalhado
        logger.info(f"Token validado para {user.get('username')}")
        
        # Converte o _id para string para evitar problemas de serialização
        if "_id" in user:
            user["_id"] = str(user["_id"])
        
        # Remover campo senha da resposta por segurança
        if "senha" in user:
            del user["senha"]
        
        return {
            "status": "valid", 
            "user": user
        }
    except Exception as e:
        logger.error(f"Erro na validação do token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )

# Função para obter o próximo ID de pedido
async def get_last_id(db):
    last_pedido = await db["pedidos"].find().sort("id", -1).limit(1).to_list(1)
    return last_pedido[0]["id"] + 1 if last_pedido else 1

# Rota para criação de pedidos
@app.post("/pedidos/", response_model=models.Pedido)
async def criar_pedido(pedido: schemas.PedidoCreate, request: Request, db=Depends(database.get_db), current_user=Depends(get_current_user)):
    try:
        next_id = await get_last_id(db)

        pedido_dict = pedido.dict()
        pedido_dict["id"] = next_id

        # Capturar IP e User-Agent
        ip_address = utils.get_client_ip(request)
        user_agent = request.headers.get("User-Agent", "Desconhecido")

        # Obter o nome do usuário autenticado do token
        usuario_nome = current_user.get("nome")
        if not usuario_nome:
            usuario_nome = current_user.get("username", "Sistema")
            
        # Obter o setor do usuário do token
        setor_usuario = current_user.get("setor", "Escritório")
        
        # Verificar se o usuário é admin ou gestor
        is_admin = current_user.get("tipo_usuario") == "admin"
        is_gestor = current_user.get("tipo_usuario") == "gestor"
            
        logger.info(f"Usuário autenticado: {usuario_nome}, Setor: {setor_usuario}")
        
        # Sobrescreve o campo usuario_nome, ignorando o enviado pelo cliente
        pedido_dict["usuario_nome"] = usuario_nome
        
        # Sobrescreve o campo setor apenas se não for admin ou gestor
        if not (is_admin or is_gestor):
            pedido_dict["setor"] = setor_usuario

        # Assegura que a data do pedido seja a data e hora atual
        pedido_dict["deliveryDate"] = datetime.now()

        # Insere o pedido no banco
        if pedido_dict.get('file'):
            logger.info(f"Arquivo Base64 recebido: {pedido_dict['file'][:30]}...")  # Exibe parte do conteúdo
        pedido_dict['anexo'] = pedido_dict.pop('file')  # Renomeia o campo - IMPORTANTE - NÃO ALTERAR

        await db["pedidos"].insert_one(pedido_dict)
        
        # Registra a atividade de criação
        await registrar_atividade(
            db,
            tipo="criacao",
            descricao=f"Pedido #{next_id} '{pedido.descricao[:50]}...' criado",
            usuario_nome=usuario_nome,
            pedido_id=next_id,
            ip_address=ip_address,
            user_agent=user_agent,
            dados_adicionais={
                "setor": pedido_dict.get("setor", setor_usuario),
                "titulo": pedido.descricao
            }
        )

        logger.info(f"Pedido criado com sucesso: {pedido_dict}")
        return pedido_dict
    except Exception as e:
        logger.error(f"Erro ao criar pedido: {e}")
        
        # Se temos as informações do usuário e IP, registramos o erro
        if 'usuario_nome' in locals() and 'ip_address' in locals():
            await registrar_atividade(
                db=db,
                tipo="erro",
                descricao=f"Erro ao criar pedido: {str(e)}",
                usuario_nome=locals()['usuario_nome'],
                ip_address=locals()['ip_address'],
                user_agent=locals()['user_agent'] if 'user_agent' in locals() else "Desconhecido",
                dados_adicionais={
                    "status": "falha", 
                    "detalhes": str(e),
                    "descricao_pedido": pedido.descricao if hasattr(pedido, 'descricao') else "Desconhecido"
                }
            )
            
        raise HTTPException(status_code=500, detail="Erro ao criar pedido.")

# Rota para listar pedidos
@app.get("/pedidos/", response_model=List[models.Pedido])
async def listar_pedidos(request: Request, db=Depends(database.get_db), current_user=Depends(get_current_user)):
    try:
        # Capturar IP e User-Agent
        ip_address = utils.get_client_ip(request)
        user_agent = request.headers.get("User-Agent", "Desconhecido")
        
        # Obter o nome do usuário
        usuario_nome = current_user.get("nome")
        if not usuario_nome:
            usuario_nome = current_user.get("username", "Sistema")
        
        # Verificar se o usuário é admin
        is_admin = current_user.get("tipo_usuario") == "admin"
        
        # Obter o setor do usuário
        setor_usuario = current_user.get("setor", "Escritório")
        
        # Se for admin, retorna todos os pedidos, caso contrário filtra por setor
        if is_admin:
            logger.info(f"Listando todos os pedidos para o administrador: {usuario_nome}")
            pedidos = await db["pedidos"].find().to_list(None)
            
            # Registrar consulta de todos os pedidos (admin)
            await registrar_atividade(
                db=db,
                tipo="consulta",
                descricao=f"Listagem de todos os pedidos ({len(pedidos)} pedidos)",
                usuario_nome=usuario_nome,
                ip_address=ip_address,
                user_agent=user_agent,
                dados_adicionais={
                    "tipo_listagem": "todos", 
                    "quantidade": len(pedidos),
                    "admin": True
                }
            )
        else:
            logger.info(f"Listando pedidos do setor {setor_usuario} para o usuário: {usuario_nome}")
            pedidos = await db["pedidos"].find({"setor": setor_usuario}).to_list(None)
            
            # Registrar consulta filtrada por setor
            await registrar_atividade(
                db=db,
                tipo="consulta",
                descricao=f"Listagem de pedidos do setor {setor_usuario} ({len(pedidos)} pedidos)",
                usuario_nome=usuario_nome,
                ip_address=ip_address,
                user_agent=user_agent,
                dados_adicionais={
                    "tipo_listagem": "por_setor", 
                    "setor": setor_usuario,
                    "quantidade": len(pedidos)
                }
            )
        
        for pedido in pedidos:
            pedido["_id"] = str(pedido["_id"])
        
        logger.info(f"Pedidos encontrados: {len(pedidos)}")
        return pedidos
    except Exception as e:
        logger.error(f"Erro ao listar pedidos: {e}")
        
        # Registrar erro se tivermos o contexto
        if 'usuario_nome' in locals() and 'ip_address' in locals():
            await registrar_atividade(
                db=db,
                tipo="erro",
                descricao=f"Erro ao listar pedidos: {str(e)}",
                usuario_nome=locals()['usuario_nome'],
                ip_address=locals()['ip_address'],
                user_agent=locals()['user_agent'] if 'user_agent' in locals() else "Desconhecido",
                dados_adicionais={"status": "falha", "detalhes": str(e)}
            )
            
        raise HTTPException(status_code=500, detail="Erro ao listar pedidos.")

@app.get("/pedidos/{pedido_id}")
async def obter_pedido(pedido_id: int, request: Request, db=Depends(database.get_db), current_user=Depends(get_current_user)):
    try:
        # Capturar IP e User-Agent
        ip_address = utils.get_client_ip(request)
        user_agent = request.headers.get("User-Agent", "Desconhecido")
        
        # Obter o nome do usuário
        usuario_nome = current_user.get("nome")
        if not usuario_nome:
            usuario_nome = current_user.get("username", "Sistema")
            
        # Buscar o pedido
        pedido = await db["pedidos"].find_one({"id": pedido_id})
        if not pedido:
            # Registrar consulta para pedido não encontrado
            await registrar_atividade(
                db=db,
                tipo="consulta",
                descricao=f"Tentativa de consulta ao pedido #{pedido_id} - não encontrado",
                usuario_nome=usuario_nome,
                ip_address=ip_address,
                user_agent=user_agent,
                dados_adicionais={
                    "status": "falha",
                    "motivo": "Pedido não encontrado"
                }
            )
            raise HTTPException(status_code=404, detail="Pedido não encontrado.")
        
        # Verificar se o usuário é admin
        is_admin = current_user.get("tipo_usuario") == "admin"
        
        # Obter o setor do usuário
        setor_usuario = current_user.get("setor", "Escritório")
        
        # Verificar se o usuário tem permissão para ver este pedido
        if not is_admin and pedido.get("setor") != setor_usuario:
            # Registrar tentativa de acesso não autorizado
            await registrar_atividade(
                db=db,
                tipo="seguranca",
                descricao=f"Tentativa de acesso não autorizado ao pedido #{pedido_id} do setor {pedido.get('setor')}",
                usuario_nome=usuario_nome,
                pedido_id=pedido_id,
                ip_address=ip_address,
                user_agent=user_agent,
                dados_adicionais={
                    "status": "falha",
                    "motivo": "Acesso entre setores",
                    "setor_usuario": setor_usuario,
                    "setor_pedido": pedido.get("setor")
                }
            )
            
            logger.warning(f"Usuário {usuario_nome} (setor: {setor_usuario}) tentou visualizar um pedido do setor {pedido.get('setor')}")
            raise HTTPException(
                status_code=403, 
                detail="Você não tem permissão para visualizar pedidos de outros setores."
            )
        
        # Registrar atividade de consulta bem-sucedida
        await registrar_atividade(
            db=db,
            tipo="consulta",
            descricao=f"Consulta ao pedido #{pedido_id} - {pedido.get('descricao', '')[:30]}...",
            usuario_nome=usuario_nome,
            pedido_id=pedido_id,
            ip_address=ip_address,
            user_agent=user_agent,
            dados_adicionais={
                "status": "sucesso",
                "setor": pedido.get("setor")
            }
        )
        
        return pedido
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Erro ao consultar pedido #{pedido_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro ao consultar pedido.")

# Rota para atualização de pedidos
@app.put("/pedidos/{pedido_id}")
async def atualizar_pedido(pedido_id: int, pedido: schemas.PedidoCreate, request: Request, db=Depends(database.get_db), current_user=Depends(get_current_user)):
    try:
        logger.info(f"Requisição PUT recebida para o pedido ID: {pedido_id}")
        logger.info(f"Dados recebidos para atualização: {pedido}")
        
        # Capturar IP e User-Agent
        ip_address = utils.get_client_ip(request)
        user_agent = request.headers.get("User-Agent", "Desconhecido")

        # Buscar o pedido atual para comparações
        pedido_atual = await db["pedidos"].find_one({"id": pedido_id})
        if not pedido_atual:
            # Registrar erro de pedido não encontrado
            await registrar_atividade(
                db=db,
                tipo="erro",
                descricao=f"Tentativa de atualização de pedido inexistente #{pedido_id}",
                usuario_nome=current_user.get("nome", "Sistema"),
                ip_address=ip_address,
                user_agent=user_agent,
                dados_adicionais={
                    "status": "falha",
                    "motivo": "Pedido não encontrado"
                }
            )
            raise HTTPException(status_code=404, detail="Pedido não encontrado.")
            
        # Verificar se o usuário é admin ou gestor
        is_admin = current_user.get("tipo_usuario") == "admin"
        is_gestor = current_user.get("tipo_usuario") == "gestor"
        
        # Obter o setor e nome do usuário
        setor_usuario = current_user.get("setor", "Escritório")
        usuario_nome = current_user.get("nome")
        
        # Verificar se o usuário tem permissão para editar este pedido
        pode_editar = False
        
        # Admin e gestor podem editar qualquer pedido
        if is_admin or is_gestor:
            pode_editar = True
        # Usuário comum só pode editar pedidos que ele mesmo criou
        elif pedido_atual.get("usuario_nome") == usuario_nome:
            pode_editar = True
            
        if not pode_editar:
            msg_erro = "Você não tem permissão para editar este pedido."
            if current_user.get("tipo_usuario") == "comum":
                msg_erro += " Apenas o criador do pedido, gestores e administradores podem editar."
            
            # Registrar tentativa não autorizada
            await registrar_atividade(
                db=db,
                tipo="seguranca",
                descricao=f"Tentativa não autorizada de edição do pedido #{pedido_id}",
                usuario_nome=usuario_nome,
                pedido_id=pedido_id,
                ip_address=ip_address,
                user_agent=user_agent,
                dados_adicionais={
                    "status": "falha",
                    "motivo": "Permissão negada",
                    "tipo_usuario": current_user.get("tipo_usuario", "comum"),
                    "setor_usuario": setor_usuario,
                    "setor_pedido": pedido_atual.get("setor")
                }
            )
            
            logger.warning(f"Usuário {usuario_nome} (tipo: {current_user.get('tipo_usuario')}) tentou editar pedido #{pedido_id} sem permissão")
            raise HTTPException(status_code=403, detail=msg_erro)
            
        # Armazena o status original
        status_original = pedido_atual.get("status", "Pendente")

        update_data = pedido.dict(exclude_unset=True)
        logger.info(f"Dados iniciais: {update_data}")
        
        # Sobrescreve o campo usuario_nome, ignorando o enviado pelo cliente
        update_data["usuario_nome"] = usuario_nome
        
        # Manter o setor original do pedido, exceto se for admin ou gestor
        if not (is_admin or is_gestor):
            update_data["setor"] = pedido_atual.get("setor", setor_usuario)
        
        # Manter a data original do pedido, permitindo alteração apenas para administradores
        if "deliveryDate" in update_data:
            if not is_admin:
                logger.info(f"Usuário não é admin, mantendo a data original do pedido: {pedido_atual.get('deliveryDate')}")
                del update_data["deliveryDate"]
            else:
                logger.info(f"Admin alterando a data do pedido para: {update_data['deliveryDate']}")
                # Se for admin, registrar a alteração no histórico
                hist_data_date = {
                    "pedido_id": pedido_id,
                    "usuario_nome": usuario_nome,
                    "campo_alterado": "Data do Pedido",
                    "valor_anterior": pedido_atual.get('deliveryDate').strftime("%d/%m/%Y") if pedido_atual.get('deliveryDate') else "Não definida",
                    "valor_novo": update_data["deliveryDate"].strftime("%d/%m/%Y") if isinstance(update_data["deliveryDate"], datetime) else str(update_data["deliveryDate"]),
                    "data_edicao": datetime.now()
                }
                await db["pedido_historico"].insert_one(hist_data_date)

        # Processar a data de conclusão
        if "completionDate" in update_data:
            logger.info(f"Processando data de conclusão: {update_data['completionDate']}")
            if update_data["completionDate"] is None:
                update_data["conclusao_data"] = datetime.now()
            elif isinstance(update_data["completionDate"], str):
                try:
                    update_data["conclusao_data"] = validate_and_convert_date(update_data["completionDate"])
                except Exception as e:
                    logger.error(f"Erro ao converter completionDate: {e}")
                    update_data["conclusao_data"] = datetime.now()
            elif isinstance(update_data["completionDate"], date):
                update_data["conclusao_data"] = datetime.combine(update_data["completionDate"], datetime.min.time())
            else:
                logger.warning(f"Tipo desconhecido para completionDate: {type(update_data['completionDate'])}")
                update_data["conclusao_data"] = datetime.now()
            
            # Remover o campo completionDate original
            del update_data["completionDate"]

        # Normalizar status "Concluído" para ter um formato consistente
        if "status" in update_data:
            status = update_data["status"]
            status_está_mudando_para_concluido = False
            
            if status == "Concluido" or status.upper() == "CONCLUIDO" or status.upper() == "CONCLUÍDO":
                update_data["status"] = "Concluído"
                # Adicionar data de conclusão ao pedido se não foi informada explicitamente
                if "conclusao_data" not in update_data:
                    update_data["conclusao_data"] = datetime.now()
                    
                # Verificar se o status está mudando para Concluído
                if status_original != "Concluído":
                    status_está_mudando_para_concluido = True
        
        # Validar e processar campos de orçamento
        if "orcamento_previsto" in update_data:
            # Registrar data de registro do orçamento
            update_data["data_orcamento"] = datetime.now()
            
            # Criar registro de atividade para atualização de orçamento
            await registrar_atividade(
                db,
                tipo="orcamento",
                descricao=f"Orçamento previsto do pedido #{pedido_id} atualizado para R$ {update_data['orcamento_previsto']:.2f}",
                usuario_nome=usuario_nome,
                pedido_id=pedido_id,
                ip_address=ip_address,
                user_agent=user_agent,
                dados_adicionais={
                    "valor": float(update_data['orcamento_previsto']),
                    "data": datetime.now().isoformat()
                }
            )
            
        if "custo_real" in update_data:
            # Registrar data de registro do custo real
            update_data["data_custo_real"] = datetime.now()
            
            # Criar registro de atividade para atualização de custo
            await registrar_atividade(
                db,
                tipo="orcamento",
                descricao=f"Custo real do pedido #{pedido_id} registrado em R$ {update_data['custo_real']:.2f}",
                usuario_nome=usuario_nome,
                pedido_id=pedido_id,
                ip_address=ip_address,
                user_agent=user_agent,
                dados_adicionais={
                    "valor": float(update_data['custo_real']),
                    "data": datetime.now().isoformat()
                }
            )

        logger.info(f"Dados para atualização após transformação: {update_data}")
        
        # Converter todos os objetos datetime.date para datetime.datetime
        update_data = convert_dates_to_datetime(update_data)
        logger.info(f"Dados após conversão de datas: {update_data}")

        # Atualizar o pedido
        result = await db["pedidos"].update_one(
            {"id": pedido_id},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            logger.warning(f"Nenhum pedido encontrado para o ID: {pedido_id}")
            raise HTTPException(status_code=404, detail="Pedido não encontrado.")

        # Registrar a mudança de status no histórico se necessário
        if "status" in update_data and update_data["status"] != status_original:
            # Criar registro histórico para a mudança de status
            hist_data = {
                "pedido_id": pedido_id,
                "usuario_nome": usuario_nome,
                "campo_alterado": "Status",
                "valor_anterior": status_original,
                "valor_novo": update_data["status"],
                "data_edicao": datetime.now()
            }
            
            # Inserir registro no histórico
            await db["pedido_historico"].insert_one(hist_data)
            
            # Se o status mudou para Concluído, registrar também a data de conclusão
            if update_data["status"] == "Concluído" and "conclusao_data" in update_data:
                hist_data_conclusao = {
                    "pedido_id": pedido_id,
                    "usuario_nome": usuario_nome,
                    "campo_alterado": "Data de Conclusão",
                    "valor_anterior": "Não definida",
                    "valor_novo": update_data["conclusao_data"].strftime("%d/%m/%Y"),
                    "data_edicao": datetime.now()
                }
                await db["pedido_historico"].insert_one(hist_data_conclusao)
            
            # Registrar atividade de conclusão se o status mudou para Concluído
            if update_data["status"] == "Concluído":
                await registrar_atividade(
                    db,
                    tipo="conclusao",
                    descricao=f"Pedido #{pedido_id} marcado como concluído",
                    usuario_nome=usuario_nome,
                    pedido_id=pedido_id,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    dados_adicionais={
                        "status_anterior": status_original
                    }
                )
            # Ou registrar atividade de edição para outros casos
            else:
                await registrar_atividade(
                    db,
                    tipo="edicao",
                    descricao=f"Status do pedido #{pedido_id} alterado de '{status_original}' para '{update_data['status']}'",
                    usuario_nome=usuario_nome,
                    pedido_id=pedido_id,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    dados_adicionais={
                        "status_anterior": status_original,
                        "novo_status": update_data["status"]
                    }
                )
        else:
            # Registrar atividade de edição genérica se não houve mudança de status
            await registrar_atividade(
                db,
                tipo="edicao",
                descricao=f"Dados do pedido #{pedido_id} atualizados",
                usuario_nome=usuario_nome,
                pedido_id=pedido_id,
                ip_address=ip_address,
                user_agent=user_agent,
                dados_adicionais={
                    "campos_alterados": list(update_data.keys())
                }
            )

        logger.info(f"Pedido atualizado com sucesso: ID {pedido_id}")
        return {"message": "Pedido atualizado com sucesso!"}

    except Exception as e:
        logger.error(f"Erro ao atualizar pedido: {e}")
        logger.exception("Detalhes do erro:")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar pedido: {str(e)}")

# Rota para atualizar pedido com histórico de alterações
@app.put("/pedidos/{pedido_id}/com-historico")
async def atualizar_pedido_com_historico(
    pedido_id: int, 
    pedido: schemas.PedidoCreate, 
    request: Request,
    db=Depends(database.get_db),
    current_user=Depends(get_current_user)
):
    try:
        logger.info(f"Requisição PUT recebida para o pedido ID: {pedido_id} com histórico")
        
        # Capturar IP e User-Agent
        ip_address = utils.get_client_ip(request)
        user_agent = request.headers.get("User-Agent", "Desconhecido")
            
        # Buscar o pedido atual para comparações
        pedido_atual = await db["pedidos"].find_one({"id": pedido_id})
        if not pedido_atual:
            # Registrar erro de pedido não encontrado
            await registrar_atividade(
                db=db,
                tipo="erro",
                descricao=f"Tentativa de atualização com histórico de pedido inexistente #{pedido_id}",
                usuario_nome=current_user.get("nome", "Sistema"),
                ip_address=ip_address,
                user_agent=user_agent,
                dados_adicionais={
                    "status": "falha",
                    "motivo": "Pedido não encontrado"
                }
            )
            raise HTTPException(status_code=404, detail="Pedido não encontrado.")
            
        # Verificar se o usuário é admin ou gestor
        is_admin = current_user.get("tipo_usuario") == "admin"
        is_gestor = current_user.get("tipo_usuario") == "gestor"
        
        # Obter o setor e nome do usuário
        setor_usuario = current_user.get("setor", "Escritório")
        usuario_nome = current_user.get("nome")
        
        # Verificar se o usuário tem permissão para editar este pedido
        pode_editar = False
        
        # Admin e gestor podem editar qualquer pedido
        if is_admin or is_gestor:
            pode_editar = True
        # Usuário comum só pode editar pedidos que ele mesmo criou
        elif pedido_atual.get("usuario_nome") == usuario_nome:
            pode_editar = True
            
        if not pode_editar:
            msg_erro = "Você não tem permissão para editar este pedido."
            if current_user.get("tipo_usuario") == "comum":
                msg_erro += " Apenas o criador do pedido, gestores e administradores podem editar."
                
            # Registrar tentativa não autorizada
            await registrar_atividade(
                db=db,
                tipo="seguranca",
                descricao=f"Tentativa não autorizada de edição do pedido #{pedido_id} com histórico",
                usuario_nome=usuario_nome,
                pedido_id=pedido_id,
                ip_address=ip_address,
                user_agent=user_agent,
                dados_adicionais={
                    "status": "falha",
                    "motivo": "Permissão negada",
                    "tipo_usuario": current_user.get("tipo_usuario", "comum"),
                    "setor_usuario": setor_usuario,
                    "setor_pedido": pedido_atual.get("setor")
                }
            )
            
            logger.warning(f"Usuário {usuario_nome} (tipo: {current_user.get('tipo_usuario')}) tentou editar pedido #{pedido_id} sem permissão")
            raise HTTPException(status_code=403, detail=msg_erro)
        
        # Obter os dados atualizados e o histórico de alterações
        update_data = pedido.dict(exclude_unset=True)
        historico = update_data.pop("historico", None)
        
        # Sobrescreve o campo usuario_nome, ignorando o enviado pelo cliente
        update_data["usuario_nome"] = usuario_nome
        
        # Manter o setor original do pedido, exceto se for admin ou gestor
        if not (is_admin or is_gestor):
            update_data["setor"] = pedido_atual.get("setor", setor_usuario)
        
        # Processar a data de conclusão
        if "completionDate" in update_data:
            logger.info(f"Processando data de conclusão: {update_data['completionDate']}")
            if update_data["completionDate"] is None:
                update_data["conclusao_data"] = datetime.now()
            elif isinstance(update_data["completionDate"], str):
                try:
                    update_data["conclusao_data"] = validate_and_convert_date(update_data["completionDate"])
                except Exception as e:
                    logger.error(f"Erro ao converter completionDate: {e}")
                    update_data["conclusao_data"] = datetime.now()
            elif isinstance(update_data["completionDate"], date):
                update_data["conclusao_data"] = datetime.combine(update_data["completionDate"], datetime.min.time())
            else:
                logger.warning(f"Tipo desconhecido para completionDate: {type(update_data['completionDate'])}")
                update_data["conclusao_data"] = datetime.now()
            
            # Remover o campo completionDate original
            del update_data["completionDate"]
        
        # Corrigir o nome do usuário em cada entrada do histórico
        if historico and isinstance(historico, list):
            for item in historico:
                if isinstance(item, dict):
                    # Sobrescrever o nome do usuário com o do token
                    item["usuario_nome"] = usuario_nome
        
        # Renomear 'file' para 'anexo'
        if 'file' in update_data:
            update_data['anexo'] = update_data.pop('file')
        
        # Registra o status anterior
        status_anterior = pedido_atual.get("status", "Pendente")
        status_novo = update_data.get("status", status_anterior)
        
        # Converter todos os objetos datetime.date para datetime.datetime
        update_data = convert_dates_to_datetime(update_data)
        logger.info(f"Dados após conversão de datas: {update_data}")
        
        # Atualiza o pedido
        result = await db["pedidos"].update_one(
            {"id": pedido_id},
            {"$set": update_data}
        )
        
        # Salvar registros de histórico na coleção pedido_historico
        if historico and isinstance(historico, list):
            logger.info(f"Processando {len(historico)} registros de histórico para o pedido {pedido_id}")
            
            for modificacao in historico:
                # Adicionar timestamp e garantir pedido_id
                if not isinstance(modificacao, dict):
                    continue
                    
                modificacao["pedido_id"] = pedido_id
                if "data_edicao" not in modificacao:
                    modificacao["data_edicao"] = datetime.now()
                
                # Inserir no banco de dados
                await db["pedido_historico"].insert_one(modificacao)
            
            logger.info(f"{len(historico)} registros de histórico salvos com sucesso")
        else:
            logger.warning(f"Nenhum histórico válido recebido para o pedido {pedido_id}")
        
        # Se houve alteração no status, registramos a atividade específica
        if status_anterior != status_novo:
            tipo_atividade = "edicao"
            if status_novo == "Concluído" or status_novo.upper() == "CONCLUÍDO" or status_novo == "Concluido" or status_novo.upper() == "CONCLUIDO":
                tipo_atividade = "conclusao"
                # Padronizar o status como "Concluído" no banco
                status_novo = "Concluído"
                
                # Adicionar data de conclusão ao pedido se não foi informada explicitamente
                if "conclusao_data" not in update_data:
                    update_data["conclusao_data"] = datetime.now()
                
                # Atualizar o status padronizado e a data de conclusão no banco
                await db["pedidos"].update_one(
                    {"id": pedido_id},
                    {"$set": {"status": status_novo, "conclusao_data": update_data["conclusao_data"]}}
                )
            elif status_novo == "Cancelado":
                tipo_atividade = "cancelamento"
            
            await registrar_atividade(
                db,
                tipo=tipo_atividade,
                descricao=f"Status do pedido #{pedido_id} alterado de '{status_anterior}' para '{status_novo}'",
                usuario_nome=usuario_nome,
                pedido_id=pedido_id,
                ip_address=ip_address,
                user_agent=user_agent,
                dados_adicionais={
                    "status_anterior": status_anterior,
                    "novo_status": status_novo,
                    "com_historico": True
                }
            )
        else:
            # Registra atividade de edição genérica
            await registrar_atividade(
                db,
                tipo="edicao",
                descricao=f"Pedido #{pedido_id} editado com histórico",
                usuario_nome=usuario_nome,
                pedido_id=pedido_id,
                ip_address=ip_address,
                user_agent=user_agent,
                dados_adicionais={
                    "campos_alterados": list(update_data.keys()),
                    "historico_adicionado": historico is not None and len(historico) > 0
                }
            )
        
        return {"message": "Pedido atualizado com sucesso!"}
    except Exception as e:
        logger.error(f"Erro ao atualizar pedido com histórico: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao atualizar pedido: {str(e)}"
        )

# Rota para adicionar registro ao histórico de um pedido
@app.post("/pedidos/{pedido_id}/historico")
async def adicionar_historico_pedido(
    pedido_id: int,
    dados: dict,
    request: Request,
    db=Depends(database.get_db),
    current_user=Depends(get_current_user)
):
    try:
        # Capturar IP e User-Agent
        ip_address = utils.get_client_ip(request)
        user_agent = request.headers.get("User-Agent", "Desconhecido")
        
        # Verificar se o pedido existe
        pedido = await db["pedidos"].find_one({"id": pedido_id})
        if not pedido:
            # Registrar erro de pedido não encontrado
            await registrar_atividade(
                db=db,
                tipo="erro",
                descricao=f"Tentativa de adicionar histórico a pedido inexistente #{pedido_id}",
                usuario_nome=current_user.get("nome", "Sistema"),
                ip_address=ip_address,
                user_agent=user_agent,
                dados_adicionais={
                    "status": "falha",
                    "motivo": "Pedido não encontrado"
                }
            )
            raise HTTPException(status_code=404, detail="Pedido não encontrado.")
        
        # Obter o nome do usuário autenticado do token
        usuario_nome = current_user.get("nome")
        if not usuario_nome:
            usuario_nome = current_user.get("username", "Sistema")
            
        logger.info(f"Usuário autenticado: {usuario_nome}")
        
        # Preparar os dados do histórico
        hist_data = {
            "pedido_id": pedido_id,
            "usuario_nome": usuario_nome,  # Sempre usa o usuário do token
            "campo_alterado": dados.get("campo_alterado", ""),
            "valor_anterior": dados.get("valor_anterior", ""),
            "valor_novo": dados.get("valor_novo", ""),
            "data_edicao": datetime.now()
        }
        
        # Inserir o registro no histórico
        result = await db["pedido_historico"].insert_one(hist_data)
        
        # Registrar atividade de adição de histórico
        await registrar_atividade(
            db=db,
            tipo="edicao",
            descricao=f"Adicionado comentário/histórico ao pedido #{pedido_id}: {dados.get('campo_alterado', '')}",
            usuario_nome=usuario_nome,
            pedido_id=pedido_id,
            ip_address=ip_address,
            user_agent=user_agent,
            dados_adicionais={
                "campo": dados.get("campo_alterado", ""),
                "valor_anterior": dados.get("valor_anterior", ""),
                "valor_novo": dados.get("valor_novo", "")
            }
        )
        
        logger.info(f"Registro de histórico adicionado para o pedido {pedido_id}")
        return {"message": "Registro de histórico adicionado com sucesso!"}
        
    except Exception as e:
        logger.error(f"Erro ao adicionar histórico: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar histórico: {str(e)}")

# Rota para obter histórico de edições de um pedido
@app.get("/pedidos/{pedido_id}/historico")
async def obter_historico_pedido(
    pedido_id: int,
    request: Request,
    db=Depends(database.get_db),
    current_user=Depends(get_current_user)
):
    try:
        # Capturar IP e User-Agent
        ip_address = utils.get_client_ip(request)
        user_agent = request.headers.get("User-Agent", "Desconhecido")
        
        # Obter o nome do usuário
        usuario_nome = current_user.get("nome")
        if not usuario_nome:
            usuario_nome = current_user.get("username", "Sistema")
        
        # Buscar o pedido para verificar permissões
        pedido = await db["pedidos"].find_one({"id": pedido_id})
        if not pedido:
            # Registrar erro de pedido não encontrado
            await registrar_atividade(
                db=db,
                tipo="erro",
                descricao=f"Tentativa de consultar histórico de pedido inexistente #{pedido_id}",
                usuario_nome=usuario_nome,
                ip_address=ip_address,
                user_agent=user_agent,
                dados_adicionais={
                    "status": "falha",
                    "motivo": "Pedido não encontrado"
                }
            )
            raise HTTPException(status_code=404, detail="Pedido não encontrado.")
        
        # Verificar se o usuário é admin
        is_admin = current_user.get("tipo_usuario") == "admin"
        
        # Obter o setor do usuário
        setor_usuario = current_user.get("setor", "Escritório")
        
        # Verificar se o usuário tem permissão para ver o histórico deste pedido
        if not is_admin and pedido.get("setor") != setor_usuario:
            logger.warning(f"Usuário {current_user.get('nome')} (setor: {setor_usuario}) tentou visualizar o histórico de um pedido do setor {pedido.get('setor')}")
            
            # Registrar tentativa de acesso não autorizado
            await registrar_atividade(
                db,
                tipo="seguranca",
                descricao=f"Acesso negado ao histórico do pedido #{pedido_id}",
                usuario_nome=usuario_nome,
                pedido_id=pedido_id,
                ip_address=ip_address,
                user_agent=user_agent,
                dados_adicionais={
                    "status": "negado", 
                    "motivo": "Acesso entre setores",
                    "setor_usuario": setor_usuario,
                    "setor_pedido": pedido.get("setor")
                }
            )
            
            raise HTTPException(
                status_code=403, 
                detail="Você não tem permissão para visualizar o histórico de pedidos de outros setores."
            )
        
        historico = await db["pedido_historico"].find({"pedido_id": pedido_id}).sort("data_edicao", -1).to_list(None)
        
        # Registrar atividade de consulta ao histórico
        await registrar_atividade(
            db=db,
            tipo="consulta",
            descricao=f"Consulta ao histórico do pedido #{pedido_id}",
            usuario_nome=usuario_nome,
            pedido_id=pedido_id,
            ip_address=ip_address,
            user_agent=user_agent,
            dados_adicionais={
                "quantidade_registros": len(historico)
            }
        )
        
        # Formata os dados para resposta
        for item in historico:
            item["_id"] = str(item["_id"])
            
        return historico
    except Exception as e:
        logger.error(f"Erro ao buscar histórico do pedido: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar histórico: {str(e)}")

# Endpoint para listar atividades
@app.get("/atividades/", response_model=List[models.Atividade])
async def listar_atividades(
    db=Depends(database.get_db), 
    current_user=Depends(get_current_user),
    limit: int = Query(1000, ge=1, le=5000),
    tipo: str = Query(None),
    start_date: str = Query(None),
    end_date: str = Query(None),
    search: str = Query(None),
    incluir_logs_sistema: bool = Query(False)
):
    """
    Endpoint centralizado para listar todas as atividades do sistema.
    Permite filtrar por tipo, data, texto e limite.
    Apenas gestores e admins podem acessar.
    """
    # Verifica se o usuário é gestor ou admin
    if current_user.get("tipo_usuario") not in ["gestor", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Acesso não autorizado. Apenas gestores podem visualizar atividades."
        )
    
    try:
        # Construir filtro baseado nos parâmetros
        filtro = {}
        if tipo:
            filtro["tipo"] = tipo
            
        if start_date and end_date:
            try:
                filtro["data"] = {
                    "$gte": datetime.fromisoformat(start_date),
                    "$lte": datetime.fromisoformat(end_date)
                }
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Formato de data inválido. Use o formato ISO (YYYY-MM-DD)."
                )
                
        if search:
            filtro["$or"] = [
                {"descricao": {"$regex": search, "$options": "i"}},
                {"usuario_nome": {"$regex": search, "$options": "i"}},
                {"tipo": {"$regex": search, "$options": "i"}}
            ]
            # Adiciona busca por pedido_id como número ou string
            if search.isdigit():
                filtro["$or"].append({"pedido_id": int(search)})
        
        # Log para diagnóstico
        logger.info(f"Filtro de atividades: {filtro}, Limite: {limit}")
        
        # Listar os tipos disponíveis para diagnóstico
        tipos_atividades = await db["atividades"].distinct("tipo")
        logger.info(f"Tipos de atividades disponíveis: {tipos_atividades}")
        
        # Busca as atividades mais recentes primeiro
        atividades = await db["atividades"].find(filtro).sort("data", -1).limit(limit).to_list(limit)
        
        # Converte ObjectId para string em cada atividade
        for atividade in atividades:
            if "_id" in atividade:
                atividade["id"] = str(atividade["_id"])
                del atividade["_id"]
        
        logger.info(f"Encontradas {len(atividades)} atividades")
        return atividades
    except Exception as e:
        logger.error(f"Erro ao listar atividades: {e}")
        logger.exception("Detalhes do erro:")
        raise HTTPException(
            status_code=500,
            detail="Erro ao buscar atividades."
        )

# Endpoint para geração de relatórios
@app.get("/relatorios/")
async def gerar_relatorio(
    tipo: str,
    periodo: str,
    formato: str,
    request: Request,
    dataInicial: Optional[str] = None,
    dataFinal: Optional[str] = None,
    db=Depends(database.get_db),
    current_user=Depends(get_current_user)
):
    # Verificar se o usuário tem permissão
    if current_user.get("tipo_usuario") not in ["gestor", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Acesso não autorizado. Apenas gestores podem gerar relatórios."
        )
    
    try:
        # Capturar IP e User-Agent
        ip_address = utils.get_client_ip(request)
        user_agent = request.headers.get("User-Agent", "Desconhecido")
        
        # Obter o nome do usuário
        usuario_nome = current_user.get("nome")
        if not usuario_nome:
            usuario_nome = current_user.get("username", "Sistema")
        
        # Determinar o intervalo de datas para o relatório
        data_final = datetime.now()
        data_inicial = data_final
        
        if periodo == "diario":
            data_inicial = data_final.replace(hour=0, minute=0, second=0, microsecond=0)
        elif periodo == "semanal":
            data_inicial = data_final - timedelta(days=7)
        elif periodo == "mensal":
            data_inicial = data_final.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif periodo == "personalizado" and dataInicial and dataFinal:
            try:
                data_inicial = datetime.fromisoformat(dataInicial)
                data_final = datetime.fromisoformat(dataFinal)
                # Ajustar final do dia
                data_final = data_final.replace(hour=23, minute=59, second=59)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Formato de data inválido. Use o formato ISO (YYYY-MM-DD)."
                )
        
        # Filtrar dados com base no tipo de relatório
        if tipo == "pedidos":
            # Buscar pedidos no período especificado
            filtro = {
                "deliveryDate": {
                    "$gte": data_inicial,
                    "$lte": data_final
                }
            }
            dados = await db["pedidos"].find(filtro).to_list(1000)
            
            # Preparar dados para o relatório
            dados_relatorio = []
            for pedido in dados:
                # Remover o _id para serialização
                if "_id" in pedido:
                    del pedido["_id"]
                # Formatar data de entrega
                if "deliveryDate" in pedido:
                    pedido["deliveryDate"] = pedido["deliveryDate"].strftime("%d/%m/%Y")
                dados_relatorio.append(pedido)
                
            # Criar dataframe
            df = pd.DataFrame(dados_relatorio)
            if df.empty:
                df = pd.DataFrame(columns=['id', 'descricao', 'quantidade', 'status', 'urgencia', 'categoria', 'deliveryDate'])
            else:
                # Reorganizar e renomear colunas
                colunas = {
                    'id': 'ID',
                    'descricao': 'Descrição',
                    'quantidade': 'Quantidade',
                    'status': 'Status',
                    'urgencia': 'Urgência',
                    'categoria': 'Categoria',
                    'deliveryDate': 'Data de Entrega'
                }
                df = df.reindex(columns=list(colunas.keys()))
                df = df.rename(columns=colunas)
                
            # Título do relatório
            titulo = f"Relatório de Pedidos - {periodo.capitalize()}"
            
        elif tipo == "atividades":
            # Buscar atividades no período especificado
            filtro = {
                "data": {
                    "$gte": data_inicial,
                    "$lte": data_final
                }
            }
            dados = await db["atividades"].find(filtro).sort("data", -1).to_list(1000)
            
            # Preparar dados para o relatório
            dados_relatorio = []
            for atividade in dados:
                # Remover o _id e adicionar id
                if "_id" in atividade:
                    atividade["id"] = str(atividade["_id"])
                    del atividade["_id"]
                # Formatar data
                if "data" in atividade:
                    atividade["data"] = atividade["data"].strftime("%d/%m/%Y %H:%M")
                dados_relatorio.append(atividade)
                
            # Criar dataframe
            df = pd.DataFrame(dados_relatorio)
            if df.empty:
                df = pd.DataFrame(columns=['id', 'tipo', 'descricao', 'usuario_nome', 'data', 'pedido_id'])
            else:
                # Reorganizar e renomear colunas
                colunas = {
                    'id': 'ID',
                    'tipo': 'Tipo',
                    'descricao': 'Descrição',
                    'usuario_nome': 'Usuário',
                    'data': 'Data',
                    'pedido_id': 'ID do Pedido'
                }
                df = df.reindex(columns=list(colunas.keys()))
                df = df.rename(columns=colunas)
                
            # Título do relatório
            titulo = f"Relatório de Atividades - {periodo.capitalize()}"
        else:
            raise HTTPException(
                status_code=400,
                detail="Tipo de relatório inválido. Use 'pedidos' ou 'atividades'."
            )
            
        # Gerar relatório no formato solicitado
        if formato == "pdf":
            # Criar buffer para armazenar o PDF
            buffer = io.BytesIO()
            
            # Configurar documento PDF
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elementos = []
            
            # Adicionar título
            estilos = getSampleStyleSheet()
            elementos.append(Paragraph(titulo, estilos['Title']))
            elementos.append(Paragraph(f"Período: {data_inicial.strftime('%d/%m/%Y')} a {data_final.strftime('%d/%m/%Y')}", estilos['Normal']))
            elementos.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", estilos['Normal']))
            elementos.append(Paragraph(f"Gerado por: {current_user.get('nome', 'Usuário')}", estilos['Normal']))
            
            # Adicionar tabela com dados
            dados_tabela = [df.columns.tolist()]
            for _, row in df.iterrows():
                dados_tabela.append(row.tolist())
                
            tabela = Table(dados_tabela)
            tabela.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elementos.append(tabela)
            
            # Construir o PDF
            doc.build(elementos)
            
            # Posicionar o buffer no início para leitura
            buffer.seek(0)
            
            # Retornar o PDF como resposta
            return StreamingResponse(
                buffer,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f'attachment; filename="relatorio_{tipo}_{periodo}.pdf"'
                }
            )
            
        elif formato == "excel":
            # Criar buffer para armazenar o Excel
            buffer = io.BytesIO()
            
            # Criar arquivo Excel
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                # Escrever o dataframe
                df.to_excel(writer, sheet_name='Relatório', index=False)
                
                # Obter a planilha e o objeto de formatação
                planilha = writer.sheets['Relatório']
                
                # Formatar cabeçalho
                formato_cabecalho = writer.book.add_format({
                    'bold': True,
                    'bg_color': '#CCCCCC',
                    'border': 1
                })
                
                # Aplicar formato ao cabeçalho
                for col_num, value in enumerate(df.columns.values):
                    planilha.write(0, col_num, value, formato_cabecalho)
                    planilha.set_column(col_num, col_num, 15)
                
                # Adicionar informações do relatório
                row = len(df) + 3
                planilha.write(row, 0, f"Relatório: {titulo}")
                planilha.write(row + 1, 0, f"Período: {data_inicial.strftime('%d/%m/%Y')} a {data_final.strftime('%d/%m/%Y')}")
                planilha.write(row + 2, 0, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                planilha.write(row + 3, 0, f"Gerado por: {current_user.get('nome', 'Usuário')}")
            
            # Posicionar o buffer no início para leitura
            buffer.seek(0)
            
            # Registrar atividade de geração de relatório
            await registrar_atividade(
                db=db,
                tipo="consulta",
                descricao=f"Geração de relatório de {tipo} - período: {periodo} - formato: {formato}",
                usuario_nome=usuario_nome,
                ip_address=ip_address,
                user_agent=user_agent,
                dados_adicionais={
                    "tipo_relatorio": tipo,
                    "periodo": periodo,
                    "formato": formato,
                    "data_inicial": data_inicial.isoformat(),
                    "data_final": data_final.isoformat()
                }
            )
            
            # Retornar o Excel como resposta
            return StreamingResponse(
                buffer,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={
                    "Content-Disposition": f'attachment; filename="relatorio_{tipo}_{periodo}.xlsx"'
                }
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Formato de relatório inválido. Use 'pdf' ou 'excel'."
            )
            
    except Exception as e:
        logger.error(f"Erro ao gerar relatório: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar relatório: {str(e)}"
        )

@app.get("/relatorios/financeiro")
async def gerar_relatorio_financeiro(
    request: Request,
    periodo: str = "mensal",
    formato: str = "pdf",
    dataInicial: Optional[str] = None,
    dataFinal: Optional[str] = None,
    db=Depends(database.get_db),
    current_user=Depends(get_current_user)
):
    """
    Gera relatórios financeiros com base nos valores de orçamento e custos reais.
    """
    # Verificar se o usuário tem permissão
    if current_user.get("tipo_usuario") not in ["gestor", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Acesso não autorizado. Apenas gestores podem gerar relatórios financeiros."
        )
    
    try:
        # Capturar IP e User-Agent
        ip_address = utils.get_client_ip(request)
        user_agent = request.headers.get("User-Agent", "Desconhecido")
        
        # Obter o nome do usuário
        usuario_nome = current_user.get("nome")
        if not usuario_nome:
            usuario_nome = current_user.get("username", "Sistema")
        
        # Determinar o intervalo de datas para o relatório
        data_final = datetime.now()
        data_inicial = data_final
        
        if periodo == "diario":
            data_inicial = data_final.replace(hour=0, minute=0, second=0, microsecond=0)
        elif periodo == "semanal":
            data_inicial = data_final - timedelta(days=7)
        elif periodo == "mensal":
            data_inicial = data_final.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif periodo == "personalizado" and dataInicial and dataFinal:
            try:
                data_inicial = datetime.fromisoformat(dataInicial)
                data_final = datetime.fromisoformat(dataFinal)
                # Ajustar final do dia
                data_final = data_final.replace(hour=23, minute=59, second=59)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Formato de data inválido. Use o formato ISO (YYYY-MM-DD)."
                )
        
        # Buscar pedidos no período especificado que tenham dados de orçamento ou custo
        filtro = {
            "$or": [
                {"deliveryDate": {"$gte": data_inicial, "$lte": data_final}},
                {"data_orcamento": {"$gte": data_inicial, "$lte": data_final}},
                {"data_custo_real": {"$gte": data_inicial, "$lte": data_final}}
            ],
            "$or": [
                {"orcamento_previsto": {"$gt": 0}},
                {"custo_real": {"$gt": 0}}
            ]
        }
        
        dados = await db["pedidos"].find(filtro).to_list(1000)
        
        # Preparar dados para o relatório
        dados_relatorio = []
        total_orcamento = 0.0
        total_custo = 0.0
        
        for pedido in dados:
            # Remover o _id para serialização
            if "_id" in pedido:
                del pedido["_id"]
            
            # Calcular a diferença entre orçamento e custo real
            orcamento = pedido.get("orcamento_previsto", 0.0)
            custo = pedido.get("custo_real", 0.0)
            diferenca = orcamento - custo
            
            # Determinar se está acima ou abaixo do orçamento
            status_orcamento = "Dentro do orçamento"
            if diferenca < 0:
                status_orcamento = "Acima do orçamento"
            elif diferenca > 0 and custo > 0:
                status_orcamento = "Abaixo do orçamento"
            elif custo == 0:
                status_orcamento = "Não executado"
            
            # Adicionar ao total
            total_orcamento += orcamento
            total_custo += custo
            
            # Formatar datas
            if "deliveryDate" in pedido:
                pedido["deliveryDate"] = pedido["deliveryDate"].strftime("%d/%m/%Y")
            if "data_orcamento" in pedido and pedido["data_orcamento"]:
                pedido["data_orcamento"] = pedido["data_orcamento"].strftime("%d/%m/%Y")
            if "data_custo_real" in pedido and pedido["data_custo_real"]:
                pedido["data_custo_real"] = pedido["data_custo_real"].strftime("%d/%m/%Y")
            
            # Adicionar os campos calculados
            relatorio_item = {
                "id": pedido.get("id"),
                "descricao": pedido.get("descricao"),
                "categoria": pedido.get("categoria", "Não definido"),
                "status": pedido.get("status"),
                "usuario_nome": pedido.get("usuario_nome"),
                "deliveryDate": pedido.get("deliveryDate"),
                "fornecedor": pedido.get("fornecedor", "Não definido"),
                "orcamento_previsto": float(orcamento),
                "custo_real": float(custo),
                "diferenca": float(diferenca),
                "status_orcamento": status_orcamento,
                "observacao_orcamento": pedido.get("observacao_orcamento", "")
            }
            
            dados_relatorio.append(relatorio_item)
            
        # Criar dataframe
        df = pd.DataFrame(dados_relatorio)
        if df.empty:
            df = pd.DataFrame(columns=['id', 'descricao', 'categoria', 'status', 'orcamento_previsto', 'custo_real', 'diferenca', 'status_orcamento'])
        else:
            # Reorganizar e renomear colunas
            colunas = {
                'id': 'ID',
                'descricao': 'Descrição',
                'categoria': 'Categoria',
                'status': 'Status',
                'usuario_nome': 'Solicitante',
                'deliveryDate': 'Data de Entrega',
                'fornecedor': 'Fornecedor',
                'orcamento_previsto': 'Orçamento Previsto (R$)',
                'custo_real': 'Custo Real (R$)',
                'diferenca': 'Diferença (R$)',
                'status_orcamento': 'Situação',
                'observacao_orcamento': 'Observações'
            }
            df = df.rename(columns=colunas)
            
        # Título do relatório
        titulo = f"Relatório Financeiro de Pedidos - {periodo.capitalize()}"
        subtitulo = f"Período: {data_inicial.strftime('%d/%m/%Y')} a {data_final.strftime('%d/%m/%Y')}"
        
        # Resumo financeiro
        resumo = pd.DataFrame([
            {"Tipo": "Total em Orçamentos", "Valor": f"R$ {total_orcamento:.2f}"},
            {"Tipo": "Total em Custos Reais", "Valor": f"R$ {total_custo:.2f}"},
            {"Tipo": "Saldo", "Valor": f"R$ {total_orcamento - total_custo:.2f}"}
        ])
        
        # Gerar relatório no formato solicitado
        if formato == "pdf":
            # Criar buffer para armazenar o PDF
            buffer = io.BytesIO()
            
            # Configurar documento PDF
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elementos = []
            
            # Adicionar título e resumo
            estilos = getSampleStyleSheet()
            elementos.append(Paragraph(titulo, estilos['Title']))
            elementos.append(Paragraph(subtitulo, estilos['Normal']))
            elementos.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", estilos['Normal']))
            elementos.append(Paragraph(f"Gerado por: {current_user.get('nome', 'Usuário')}", estilos['Normal']))
            elementos.append(Paragraph("<br/><br/>", estilos['Normal']))  # Espaçamento
            
            # Adicionar resumo financeiro
            elementos.append(Paragraph("Resumo Financeiro", estilos['Heading2']))
            
            dados_resumo = [["Tipo", "Valor"]]
            for _, row in resumo.iterrows():
                dados_resumo.append(row.tolist())
                
            tabela_resumo = Table(dados_resumo)
            tabela_resumo.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elementos.append(tabela_resumo)
            elementos.append(Paragraph("<br/><br/>", estilos['Normal']))  # Espaçamento
            
            # Adicionar detalhes dos pedidos
            elementos.append(Paragraph("Detalhes dos Pedidos", estilos['Heading2']))
            
            # Adicionar tabela com dados
            dados_tabela = [df.columns.tolist()]
            for _, row in df.iterrows():
                dados_tabela.append(row.tolist())
                
            tabela = Table(dados_tabela)
            tabela.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elementos.append(tabela)
            
            # Construir o PDF
            doc.build(elementos)
            
            # Resetar o buffer para o início
            buffer.seek(0)
            
            # Registrar atividade de geração de relatório
            await registrar_atividade(
                db=db,
                tipo="consulta",
                descricao=f"Geração de relatório financeiro - período: {periodo} - formato: PDF",
                usuario_nome=usuario_nome,
                ip_address=ip_address,
                user_agent=user_agent,
                dados_adicionais={
                    "tipo_relatorio": "financeiro",
                    "periodo": periodo,
                    "formato": "pdf",
                    "data_inicial": data_inicial.isoformat(),
                    "data_final": data_final.isoformat(),
                    "total_orcamentos": float(total_orcamento),
                    "total_custos": float(total_custo),
                    "saldo": float(total_orcamento - total_custo)
                }
            )
            
            # Retornar o PDF como resposta
            return StreamingResponse(
                buffer, 
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename=relatorio_financeiro_{periodo}_{data_inicial.strftime('%Y%m%d')}.pdf"}
            )
            
        elif formato == "excel":
            # Criar buffer para armazenar o Excel
            buffer = io.BytesIO()
            
            # Criar workbook
            workbook = xlsxwriter.Workbook(buffer)
            
            # Formatos
            titulo_formato = workbook.add_format({
                'bold': True,
                'font_size': 14,
                'align': 'center',
                'valign': 'vcenter'
            })
            
            cabecalho_formato = workbook.add_format({
                'bold': True,
                'bg_color': '#CCCCCC',
                'border': 1
            })
            
            data_formato = workbook.add_format({
                'num_format': 'dd/mm/yyyy',
                'border': 1
            })
            
            moeda_formato = workbook.add_format({
                'num_format': 'R$ #,##0.00',
                'border': 1
            })
            
            texto_formato = workbook.add_format({
                'border': 1
            })
            
            # Adicionar planilha de resumo
            ws_resumo = workbook.add_worksheet("Resumo")
            
            # Título
            ws_resumo.merge_range('A1:C1', titulo, titulo_formato)
            ws_resumo.merge_range('A2:C2', subtitulo, workbook.add_format({'align': 'center'}))
            ws_resumo.merge_range('A3:C3', f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", workbook.add_format({'align': 'center'}))
            
            # Resumo financeiro
            ws_resumo.write(5, 0, "Resumo Financeiro", workbook.add_format({'bold': True, 'font_size': 12}))
            
            ws_resumo.write(7, 0, "Tipo", cabecalho_formato)
            ws_resumo.write(7, 1, "Valor", cabecalho_formato)
            
            ws_resumo.write(8, 0, "Total em Orçamentos", texto_formato)
            ws_resumo.write(8, 1, total_orcamento, moeda_formato)
            
            ws_resumo.write(9, 0, "Total em Custos Reais", texto_formato)
            ws_resumo.write(9, 1, total_custo, moeda_formato)
            
            ws_resumo.write(10, 0, "Saldo", texto_formato)
            ws_resumo.write(10, 1, total_orcamento - total_custo, moeda_formato)
            
            # Adicionar planilha de detalhes
            ws_detalhes = workbook.add_worksheet("Detalhes dos Pedidos")
            
            # Escrever cabeçalho
            for col, value in enumerate(df.columns):
                ws_detalhes.write(0, col, value, cabecalho_formato)
                ws_detalhes.set_column(col, col, 15)  # Ajustar largura da coluna
            
            # Escrever dados
            for row_idx, row in enumerate(df.values):
                for col_idx, value in enumerate(row):
                    # Aplicar formatação específica dependendo da coluna
                    if df.columns[col_idx] in ['Orçamento Previsto (R$)', 'Custo Real (R$)', 'Diferença (R$)']:
                        ws_detalhes.write(row_idx + 1, col_idx, float(value) if value else 0, moeda_formato)
                    elif df.columns[col_idx] == 'Data de Entrega':
                        # Data já está como string formatada
                        ws_detalhes.write(row_idx + 1, col_idx, value, texto_formato)
                    else:
                        ws_detalhes.write(row_idx + 1, col_idx, value, texto_formato)
            
            # Fechar workbook
            workbook.close()
            
            # Resetar o buffer para o início
            buffer.seek(0)
            
            # Registrar atividade de geração de relatório
            await registrar_atividade(
                db=db,
                tipo="consulta",
                descricao=f"Geração de relatório financeiro - período: {periodo} - formato: {formato}",
                usuario_nome=usuario_nome,
                ip_address=ip_address,
                user_agent=user_agent,
                dados_adicionais={
                    "periodo": periodo,
                    "formato": formato,
                    "data_inicial": data_inicial.isoformat(),
                    "data_final": data_final.isoformat()
                }
            )
            
            # Retornar o Excel como resposta
            return StreamingResponse(
                buffer,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": f"attachment; filename=relatorio_financeiro_{periodo}_{data_inicial.strftime('%Y%m%d')}.xlsx"}
            )
            
        else:
            raise HTTPException(
                status_code=400,
                detail="Formato inválido. Use 'pdf' ou 'excel'."
            )
            
    except Exception as e:
        logger.error(f"Erro ao gerar relatório financeiro: {e}")
        logger.exception("Detalhes do erro:")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar relatório financeiro: {str(e)}"
        )

# Rota para logout
@app.post("/auth/logout")
async def logout(request: Request, db=Depends(database.get_db), current_user=Depends(get_current_user)):
    try:
        # Capturar IP e User-Agent
        ip_address = utils.get_client_ip(request)
        user_agent = request.headers.get("User-Agent", "Desconhecido")
        
        # Obter o nome do usuário
        usuario_nome = current_user.get("nome")
        if not usuario_nome:
            usuario_nome = current_user.get("username", "Sistema")
        
        # Registrar atividade de logout
        await registrar_atividade(
            db=db,
            tipo="logout",
            descricao=f"Logout realizado pelo usuário: {usuario_nome}",
            usuario_nome=usuario_nome,
            ip_address=ip_address,
            user_agent=user_agent,
            dados_adicionais={
                "status": "sucesso"
            }
        )
        
        logger.info(f"Logout registrado para o usuário {usuario_nome} - IP: {ip_address}")
        return {"message": "Logout realizado com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao registrar logout: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar logout")
