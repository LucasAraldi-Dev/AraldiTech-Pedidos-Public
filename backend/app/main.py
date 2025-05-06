from datetime import datetime, date, timedelta
from bson import ObjectId
from fastapi import FastAPI, Depends, HTTPException, Request, UploadFile, WebSocket, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from typing import List, Optional
from pydantic import parse_obj_as
from . import crud, models, schemas, database, auth
from .auth import get_current_user
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

logging.basicConfig(level=logging.INFO)

app = FastAPI()

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
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

@app.middleware("http")
async def log_auth_middleware(request: Request, call_next):
    token = request.headers.get("Authorization")
    if token:
        logging.info(f"Token recebido: {token}")
    else:
        logging.warning("Nenhum token fornecido")
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

# Função para registrar uma nova atividade
async def registrar_atividade(db, tipo, descricao, usuario_nome, pedido_id=None):
    try:
        atividade = models.Atividade(
            tipo=tipo,
            descricao=descricao,
            usuario_nome=usuario_nome,
            pedido_id=pedido_id,
            data=datetime.now()
        )
        
        result = await db["atividades"].insert_one(atividade.dict())
        atividade.id = str(result.inserted_id)
        logging.info(f"Atividade registrada: {atividade}")
        return atividade
    except Exception as e:
        logging.error(f"Erro ao registrar atividade: {e}")
        # Não lançamos exceção para não interromper o fluxo principal

# Rota para criação de usuário
@app.post("/usuarios/", response_model=schemas.Usuario)
async def create_user(user: schemas.UsuarioCreate, db=Depends(database.get_db)):
    try:
        new_user = await crud.create_user(db=db, user=user)
        logging.info(f"Usuário criado com sucesso: {new_user}")
        
        # Registra atividade de registro de usuário
        await registrar_atividade(
            db,
            tipo="registro",
            descricao=f"Novo usuário '{new_user['nome']}' registrado como {new_user['tipo_usuario']}",
            usuario_nome="Sistema" # Aqui poderia ser o usuário admin que criou, mas depende da lógica do sistema
        )
        
        return new_user
    except ValueError as e:
        logging.error(f"Erro ao criar usuário: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Rota para login e geração de token
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: schemas.LoginRequest, db=Depends(database.get_db)):
    user = await auth.authenticate_user(db, form_data.username, form_data.senha)
    if not user:
        logging.warning("Credenciais inválidas fornecidas.")
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    access_token = auth.create_access_token(data={"sub": user["username"], "nome": user["nome"]})
    logging.info(f"Token gerado com sucesso para o usuário: {user['username']}")
    
    # Log para verificar se o tipo_usuario existe no objeto user
    logging.info(f"Tipo de usuário encontrado: {user.get('tipo_usuario', 'Não encontrado')}")
    logging.info(f"Setor do usuário: {user.get('setor', 'Não encontrado')}")
    
    response_data = {
        "access_token": access_token, 
        "token_type": "bearer", 
        "nome": user["nome"],
        "tipo_usuario": user.get("tipo_usuario", "comum"),  # Define "comum" como padrão se não existir
        "setor": user.get("setor", "Escritório")  # Define "Escritório" como padrão se não existir
    }
    
    # Registra a atividade de login
    await registrar_atividade(
        db,
        tipo="login",
        descricao=f"Login realizado",
        usuario_nome=user["nome"]
    )
    
    # Log do objeto de resposta completo
    logging.info(f"Resposta completa: {response_data}")
    
    return response_data

# Rota para validação de token
@app.get("/auth/validate-token")
async def validate_token(token: str = Depends(auth.oauth2_scheme), db=Depends(database.get_db)):
    try:
        user = await auth.get_current_user(token=token, db=db)
        # Converte o _id para string para evitar problemas de serialização
        if "_id" in user:
            user["_id"] = str(user["_id"])
        
        logging.info(f"Token validado para o usuário: {user['username']}")
        return {"status": "valid", "user": user}
    except Exception as e:
        logging.error(f"Erro na validação do token: {str(e)}")
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
async def criar_pedido(pedido: schemas.PedidoCreate, db=Depends(database.get_db), current_user=Depends(get_current_user)):
    try:
        next_id = await get_last_id(db)

        pedido_dict = pedido.dict()
        pedido_dict["id"] = next_id

        # Obter o nome do usuário autenticado do token
        usuario_nome = current_user.get("nome")
        if not usuario_nome:
            usuario_nome = current_user.get("username", "Sistema")
            
        # Obter o setor do usuário do token
        setor_usuario = current_user.get("setor", "Escritório")
            
        logging.info(f"Usuário autenticado: {usuario_nome}, Setor: {setor_usuario}")
        
        # Sobrescreve o campo usuario_nome e setor, ignorando o enviado pelo cliente
        pedido_dict["usuario_nome"] = usuario_nome
        pedido_dict["setor"] = setor_usuario

        # Converte deliveryDate para datetime
        if isinstance(pedido.deliveryDate, date):
            pedido_dict["deliveryDate"] = datetime.combine(pedido.deliveryDate, datetime.min.time())

        # Insere o pedido no banco
        if pedido_dict.get('file'):
            logging.info(f"Arquivo Base64 recebido: {pedido_dict['file'][:30]}...")  # Exibe parte do conteúdo
        pedido_dict['anexo'] = pedido_dict.pop('file')  # Renomeia o campo - IMPORTANTE - NÃO ALTERAR

        await db["pedidos"].insert_one(pedido_dict)
        
        # Registra a atividade de criação
        await registrar_atividade(
            db,
            tipo="criacao",
            descricao=f"Pedido #{next_id} '{pedido.descricao[:50]}...' criado",
            usuario_nome=usuario_nome,
            pedido_id=next_id
        )

        logging.info(f"Pedido criado com sucesso: {pedido_dict}")
        return pedido_dict
    except Exception as e:
        logging.error(f"Erro ao criar pedido: {e}")
        raise HTTPException(status_code=500, detail="Erro ao criar pedido.")

# Rota para listar pedidos
@app.get("/pedidos/", response_model=List[models.Pedido])
async def listar_pedidos(db=Depends(database.get_db), current_user=Depends(get_current_user)):
    try:
        # Verificar se o usuário é admin
        is_admin = current_user.get("tipo_usuario") == "admin"
        
        # Obter o setor do usuário
        setor_usuario = current_user.get("setor", "Escritório")
        
        # Se for admin, retorna todos os pedidos, caso contrário filtra por setor
        if is_admin:
            logging.info(f"Listando todos os pedidos para o administrador: {current_user.get('nome')}")
            pedidos = await db["pedidos"].find().to_list(None)
        else:
            logging.info(f"Listando pedidos do setor {setor_usuario} para o usuário: {current_user.get('nome')}")
            pedidos = await db["pedidos"].find({"setor": setor_usuario}).to_list(None)
        
        for pedido in pedidos:
            pedido["_id"] = str(pedido["_id"])
        
        logging.info(f"Pedidos encontrados: {len(pedidos)}")
        return pedidos
    except Exception as e:
        logging.error(f"Erro ao listar pedidos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar pedidos.")

@app.get("/pedidos/{pedido_id}")
async def obter_pedido(pedido_id: int, db=Depends(database.get_db), current_user=Depends(get_current_user)):
    # Buscar o pedido
    pedido = await db["pedidos"].find_one({"id": pedido_id})
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    
    # Verificar se o usuário é admin
    is_admin = current_user.get("tipo_usuario") == "admin"
    
    # Obter o setor do usuário
    setor_usuario = current_user.get("setor", "Escritório")
    
    # Verificar se o usuário tem permissão para ver este pedido
    if not is_admin and pedido.get("setor") != setor_usuario:
        logging.warning(f"Usuário {current_user.get('nome')} (setor: {setor_usuario}) tentou visualizar um pedido do setor {pedido.get('setor')}")
        raise HTTPException(
            status_code=403, 
            detail="Você não tem permissão para visualizar pedidos de outros setores."
        )
    
    return pedido

# Rota para atualização de pedidos
@app.put("/pedidos/{pedido_id}")
async def atualizar_pedido(pedido_id: int, pedido: schemas.PedidoCreate, db=Depends(database.get_db), current_user=Depends(get_current_user)):
    try:
        logging.info(f"Requisição PUT recebida para o pedido ID: {pedido_id}")
        logging.info(f"Dados recebidos para atualização: {pedido}")

        # Buscar o pedido atual para comparações
        pedido_atual = await db["pedidos"].find_one({"id": pedido_id})
        if not pedido_atual:
            raise HTTPException(status_code=404, detail="Pedido não encontrado.")
            
        # Verificar se o usuário é admin
        is_admin = current_user.get("tipo_usuario") == "admin"
        
        # Obter o setor do usuário
        setor_usuario = current_user.get("setor", "Escritório")
        
        # Verificar se o usuário tem permissão para editar este pedido
        if not is_admin and pedido_atual.get("setor") != setor_usuario:
            logging.warning(f"Usuário {current_user.get('nome')} (setor: {setor_usuario}) tentou editar um pedido do setor {pedido_atual.get('setor')}")
            raise HTTPException(
                status_code=403, 
                detail="Você não tem permissão para editar pedidos de outros setores."
            )
            
        # Armazena o status original
        status_original = pedido_atual.get("status", "Pendente")

        update_data = pedido.dict(exclude_unset=True)
        logging.info(f"Dados iniciais: {update_data}")
        
        # Obter o nome do usuário autenticado do token
        usuario_nome = current_user.get("nome")
        if not usuario_nome:
            usuario_nome = current_user.get("username", "Sistema")
            
        logging.info(f"Usuário autenticado: {usuario_nome}")
        
        # Sobrescreve o campo usuario_nome, ignorando o enviado pelo cliente
        update_data["usuario_nome"] = usuario_nome
        
        # Manter o setor original do pedido, não permitindo alteração
        update_data["setor"] = pedido_atual.get("setor", setor_usuario)
        
        # Processar a data de entrega
        if "deliveryDate" in update_data:
            if isinstance(update_data["deliveryDate"], str):
                update_data["deliveryDate"] = validate_and_convert_date(update_data["deliveryDate"])
            elif isinstance(update_data["deliveryDate"], date):
                update_data["deliveryDate"] = datetime.combine(update_data["deliveryDate"], datetime.min.time())
        
        # Processar a data de conclusão
        if "completionDate" in update_data:
            logging.info(f"Processando data de conclusão: {update_data['completionDate']}")
            if update_data["completionDate"] is None:
                update_data["conclusao_data"] = datetime.now()
            elif isinstance(update_data["completionDate"], str):
                try:
                    update_data["conclusao_data"] = validate_and_convert_date(update_data["completionDate"])
                except Exception as e:
                    logging.error(f"Erro ao converter completionDate: {e}")
                    update_data["conclusao_data"] = datetime.now()
            elif isinstance(update_data["completionDate"], date):
                update_data["conclusao_data"] = datetime.combine(update_data["completionDate"], datetime.min.time())
            else:
                logging.warning(f"Tipo desconhecido para completionDate: {type(update_data['completionDate'])}")
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

        logging.info(f"Dados para atualização após transformação: {update_data}")

        # Atualizar o pedido
        result = await db["pedidos"].update_one(
            {"id": pedido_id},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            logging.warning(f"Nenhum pedido encontrado para o ID: {pedido_id}")
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
                    descricao=f"Pedido #{pedido_id} concluído",
                    usuario_nome=usuario_nome,
                    pedido_id=pedido_id
                )
            # Ou registrar atividade de edição para outros casos
            else:
                await registrar_atividade(
                    db,
                    tipo="edicao",
                    descricao=f"Status do pedido #{pedido_id} alterado de '{status_original}' para '{update_data['status']}'",
                    usuario_nome=usuario_nome,
                    pedido_id=pedido_id
                )

        logging.info(f"Pedido atualizado com sucesso: ID {pedido_id}")
        return {"message": "Pedido atualizado com sucesso!"}

    except Exception as e:
        logging.error(f"Erro ao atualizar pedido: {e}")
        logging.exception("Detalhes do erro:")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar pedido: {str(e)}")

# Rota para atualizar pedido com histórico de alterações
@app.put("/pedidos/{pedido_id}/com-historico")
async def atualizar_pedido_com_historico(
    pedido_id: int, 
    pedido: schemas.PedidoCreate, 
    db=Depends(database.get_db),
    current_user=Depends(get_current_user)
):
    try:
        # Busca o pedido atual
        pedido_atual = await db["pedidos"].find_one({"id": pedido_id})
        if not pedido_atual:
            raise HTTPException(status_code=404, detail="Pedido não encontrado.")
        
        # Verificar se o usuário é admin
        is_admin = current_user.get("tipo_usuario") == "admin"
        
        # Obter o setor do usuário
        setor_usuario = current_user.get("setor", "Escritório")
        
        # Verificar se o usuário tem permissão para editar este pedido
        if not is_admin and pedido_atual.get("setor") != setor_usuario:
            logging.warning(f"Usuário {current_user.get('nome')} (setor: {setor_usuario}) tentou editar um pedido do setor {pedido_atual.get('setor')}")
            raise HTTPException(
                status_code=403, 
                detail="Você não tem permissão para editar pedidos de outros setores."
            )
        
        # Prepara os dados para atualização
        update_data = pedido.dict(exclude_unset=True)
        logging.info(f"Dados iniciais para atualização com histórico: {update_data}")
        
        # Extrai o histórico de alterações se existir
        historico = update_data.pop("historico", []) if hasattr(pedido, "historico") else []
        
        # Usar APENAS o nome do usuário obtido do token
        usuario_nome = current_user.get("nome")
        if not usuario_nome:
            usuario_nome = current_user.get("username", "Sistema")
            
        logging.info(f"Usuário autenticado: {usuario_nome}")
        
        # Sobrescreve o campo usuario_nome com o usuário autenticado
        update_data["usuario_nome"] = usuario_nome
        
        # Manter o setor original do pedido, não permitindo alteração
        update_data["setor"] = pedido_atual.get("setor", setor_usuario)
        
        # Corrigir o nome do usuário em cada entrada do histórico
        if historico and isinstance(historico, list):
            for item in historico:
                if isinstance(item, dict):
                    # Sobrescrever o nome do usuário com o do token
                    item["usuario_nome"] = usuario_nome
        
        # Conversão de datas
        if "deliveryDate" in update_data:
            if isinstance(update_data["deliveryDate"], str):
                update_data["deliveryDate"] = validate_and_convert_date(update_data["deliveryDate"])
            elif isinstance(update_data["deliveryDate"], date):
                update_data["deliveryDate"] = datetime.combine(update_data["deliveryDate"], datetime.min.time())
        
        # Processar a data de conclusão
        if "completionDate" in update_data:
            logging.info(f"Processando data de conclusão: {update_data['completionDate']}")
            if update_data["completionDate"] is None:
                update_data["conclusao_data"] = datetime.now()
            elif isinstance(update_data["completionDate"], str):
                try:
                    update_data["conclusao_data"] = validate_and_convert_date(update_data["completionDate"])
                except Exception as e:
                    logging.error(f"Erro ao converter completionDate: {e}")
                    update_data["conclusao_data"] = datetime.now()
            elif isinstance(update_data["completionDate"], date):
                update_data["conclusao_data"] = datetime.combine(update_data["completionDate"], datetime.min.time())
            else:
                logging.warning(f"Tipo desconhecido para completionDate: {type(update_data['completionDate'])}")
                update_data["conclusao_data"] = datetime.now()
            
            # Remover o campo completionDate original
            del update_data["completionDate"]
        
        # Renomear 'file' para 'anexo'
        if 'file' in update_data:
            update_data['anexo'] = update_data.pop('file')
        
        # Registra o status anterior
        status_anterior = pedido_atual.get("status", "Pendente")
        status_novo = update_data.get("status", status_anterior)
        
        # Atualiza o pedido
        result = await db["pedidos"].update_one(
            {"id": pedido_id},
            {"$set": update_data}
        )
        
        # Salvar registros de histórico na coleção pedido_historico
        if historico and isinstance(historico, list):
            logging.info(f"Processando {len(historico)} registros de histórico para o pedido {pedido_id}")
            
            for modificacao in historico:
                # Adicionar timestamp e garantir pedido_id
                if not isinstance(modificacao, dict):
                    continue
                    
                modificacao["pedido_id"] = pedido_id
                if "data_edicao" not in modificacao:
                    modificacao["data_edicao"] = datetime.now()
                
                # Inserir no banco de dados
                await db["pedido_historico"].insert_one(modificacao)
            
            logging.info(f"{len(historico)} registros de histórico salvos com sucesso")
        else:
            logging.warning(f"Nenhum histórico válido recebido para o pedido {pedido_id}")
        
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
                pedido_id=pedido_id
            )
        else:
            # Registra atividade de edição genérica
            await registrar_atividade(
                db,
                tipo="edicao",
                descricao=f"Pedido #{pedido_id} editado",
                usuario_nome=usuario_nome,
                pedido_id=pedido_id
            )
        
        return {"message": "Pedido atualizado com sucesso!"}
    except Exception as e:
        logging.error(f"Erro ao atualizar pedido com histórico: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao atualizar pedido: {str(e)}"
        )

# Rota para adicionar registro ao histórico de um pedido
@app.post("/pedidos/{pedido_id}/historico")
async def adicionar_historico_pedido(
    pedido_id: int,
    dados: dict,
    db=Depends(database.get_db),
    current_user=Depends(get_current_user)
):
    try:
        # Verificar se o pedido existe
        pedido = await db["pedidos"].find_one({"id": pedido_id})
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado.")
        
        # Obter o nome do usuário autenticado do token
        usuario_nome = current_user.get("nome")
        if not usuario_nome:
            usuario_nome = current_user.get("username", "Sistema")
            
        logging.info(f"Usuário autenticado: {usuario_nome}")
        
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
        
        logging.info(f"Registro de histórico adicionado para o pedido {pedido_id}")
        return {"message": "Registro de histórico adicionado com sucesso!"}
        
    except Exception as e:
        logging.error(f"Erro ao adicionar histórico: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar histórico: {str(e)}")

# Rota para obter histórico de edições de um pedido
@app.get("/pedidos/{pedido_id}/historico")
async def obter_historico_pedido(
    pedido_id: int,
    db=Depends(database.get_db),
    current_user=Depends(get_current_user)
):
    try:
        # Buscar o pedido para verificar permissões
        pedido = await db["pedidos"].find_one({"id": pedido_id})
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado.")
        
        # Verificar se o usuário é admin
        is_admin = current_user.get("tipo_usuario") == "admin"
        
        # Obter o setor do usuário
        setor_usuario = current_user.get("setor", "Escritório")
        
        # Verificar se o usuário tem permissão para ver o histórico deste pedido
        if not is_admin and pedido.get("setor") != setor_usuario:
            logging.warning(f"Usuário {current_user.get('nome')} (setor: {setor_usuario}) tentou visualizar o histórico de um pedido do setor {pedido.get('setor')}")
            raise HTTPException(
                status_code=403, 
                detail="Você não tem permissão para visualizar o histórico de pedidos de outros setores."
            )
        
        historico = await db["pedido_historico"].find({"pedido_id": pedido_id}).sort("data_edicao", -1).to_list(None)
        
        # Formata os dados para resposta
        for item in historico:
            item["_id"] = str(item["_id"])
            
        return historico
    except Exception as e:
        logging.error(f"Erro ao buscar histórico do pedido: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar histórico: {str(e)}")

# Rota para listar usuários (apenas para administradores)
@app.get("/usuarios")
async def listar_usuarios(db=Depends(database.get_db), current_user=Depends(get_current_user)):
    try:
        # Verifica se o usuário atual é um administrador
        if current_user.get("tipo_usuario") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso permitido apenas para administradores"
            )
        
        # Busca todos os usuários no banco de dados
        users = await db["users"].find().to_list(None)
        
        # Converte ObjectId para string e remove senhas por segurança
        for user in users:
            user["_id"] = str(user["_id"])
            if "senha" in user:
                del user["senha"]
        
        logging.info(f"Usuários encontrados: {len(users)}")
        return users
    except Exception as e:
        logging.error(f"Erro ao listar usuários: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar usuários"
        )

# Rota para atualizar usuário (apenas para administradores)
@app.put("/usuarios/{user_id}")
async def atualizar_usuario(
    user_id: str, 
    user_update: dict, 
    current_user=Depends(get_current_user),
    db=Depends(database.get_db)
):
    try:
        # Verifica se o usuário atual é um administrador
        if current_user.get("tipo_usuario") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso permitido apenas para administradores"
            )
        
        # Remove campos que não devem ser atualizados
        if "_id" in user_update:
            del user_update["_id"]
        
        # Se houver alteração de senha, faz o hash
        if user_update.get("senha"):
            user_update["senha"] = auth.hash_password(user_update["senha"])
        
        logging.info(f"Atualizando usuário: {user_id}")
        
        # Atualiza o usuário
        result = await db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": user_update}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        logging.info(f"Usuário atualizado com sucesso: {user_id}")
        return {"message": "Usuário atualizado com sucesso"}
    except Exception as e:
        logging.error(f"Erro ao atualizar usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar usuário: {str(e)}"
        )

# Endpoint para listar atividades
@app.get("/atividades/", response_model=List[models.Atividade])
async def listar_atividades(
    db=Depends(database.get_db), 
    current_user=Depends(get_current_user),
    limit: int = Query(50, ge=1, le=100)
):
    # Verifica se o usuário é gestor ou admin
    if current_user.get("tipo_usuario") not in ["gestor", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Acesso não autorizado. Apenas gestores podem visualizar atividades."
        )
    
    try:
        # Busca as atividades mais recentes primeiro
        atividades = await db["atividades"].find().sort("data", -1).limit(limit).to_list(limit)
        
        # Converte ObjectId para string em cada atividade
        for atividade in atividades:
            if "_id" in atividade:
                atividade["id"] = str(atividade["_id"])
                del atividade["_id"]
        
        return atividades
    except Exception as e:
        logging.error(f"Erro ao listar atividades: {e}")
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
                    'bg_color': '#4F81BD',
                    'font_color': 'white',
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
        logging.error(f"Erro ao gerar relatório: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar relatório: {str(e)}"
        )
