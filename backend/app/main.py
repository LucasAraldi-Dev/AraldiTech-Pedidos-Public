from datetime import datetime, date
from bson import ObjectId
from fastapi import FastAPI, Depends, HTTPException, Request, UploadFile, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import parse_obj_as
from . import crud, models, schemas, database, auth
from .auth import get_current_user
import logging
from fastapi import status

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

# Rota para criação de usuário
@app.post("/usuarios/", response_model=schemas.Usuario)
async def create_user(user: schemas.UsuarioCreate, db=Depends(database.get_db)):
    try:
        new_user = await crud.create_user(db=db, user=user)
        logging.info(f"Usuário criado com sucesso: {new_user}")
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
    
    response_data = {
        "access_token": access_token, 
        "token_type": "bearer", 
        "nome": user["nome"],
        "tipo_usuario": user.get("tipo_usuario", "comum")  # Define "comum" como padrão se não existir
    }
    
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
async def criar_pedido(pedido: schemas.PedidoCreate, db=Depends(database.get_db)):
    try:
        next_id = await get_last_id(db)

        pedido_dict = pedido.dict()
        pedido_dict["id"] = next_id

        # Converte deliveryDate para datetime
        if isinstance(pedido.deliveryDate, date):
            pedido_dict["deliveryDate"] = datetime.combine(pedido.deliveryDate, datetime.min.time())

        # Insere o pedido no banco
        if pedido_dict.get('file'):
            logging.info(f"Arquivo Base64 recebido: {pedido_dict['file'][:30]}...")  # Exibe parte do conteúdo
        pedido_dict['anexo'] = pedido_dict.pop('file')  # Renomeia o campo - IMPORTANTE - NÃO ALTERAR

        await db["pedidos"].insert_one(pedido_dict)

        logging.info(f"Pedido criado com sucesso: {pedido_dict}")
        return pedido_dict
    except Exception as e:
        logging.error(f"Erro ao criar pedido: {e}")
        raise HTTPException(status_code=500, detail="Erro ao criar pedido.")

# Rota para listar pedidos
@app.get("/pedidos/", response_model=List[models.Pedido])
async def listar_pedidos(db=Depends(database.get_db), current_user=Depends(get_current_user)):
    try:
        pedidos = await db["pedidos"].find().to_list(None)
        for pedido in pedidos:
            pedido["_id"] = str(pedido["_id"])
        logging.info(f"Pedidos encontrados: {len(pedidos)}")
        return pedidos
    except Exception as e:
        logging.error(f"Erro ao listar pedidos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar pedidos.")

@app.get("/pedidos/{pedido_id}")
async def obter_pedido(pedido_id: int, db=Depends(database.get_db)):
    pedido = await db["pedidos"].find_one({"id": pedido_id})
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    return pedido    

# Rota para atualização de pedidos
@app.put("/pedidos/{pedido_id}")
async def atualizar_pedido(pedido_id: int, pedido: schemas.PedidoCreate, db=Depends(database.get_db)):
    try:
        logging.info(f"Requisição PUT recebida para o pedido ID: {pedido_id}")
        logging.info(f"Dados recebidos para atualização: {pedido}")

        update_data = pedido.dict(exclude_unset=True)

        if "deliveryDate" in update_data:
            if isinstance(update_data["deliveryDate"], str):
                update_data["deliveryDate"] = validate_and_convert_date(update_data["deliveryDate"])
            elif isinstance(update_data["deliveryDate"], date):
                update_data["deliveryDate"] = datetime.combine(update_data["deliveryDate"], datetime.min.time())

        logging.info(f"Dados para atualização após transformação: {update_data}")

        result = await db["pedidos"].update_one(
            {"id": pedido_id},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            logging.warning(f"Nenhum pedido encontrado para o ID: {pedido_id}")
            raise HTTPException(status_code=404, detail="Pedido não encontrado.")

        logging.info(f"Pedido atualizado com sucesso: ID {pedido_id}")
        return {"message": "Pedido atualizado com sucesso!"}

    except Exception as e:
        logging.error(f"Erro ao atualizar pedido: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar pedido: {str(e)}")

# Rota para atualizar pedido com histórico de alterações
@app.put("/pedidos/{pedido_id}/com-historico")
async def atualizar_pedido_com_historico(
    pedido_id: int, 
    dados: dict,
    db=Depends(database.get_db),
    current_user=Depends(get_current_user)
):
    try:
        logging.info(f"Requisição PUT com histórico para o pedido ID: {pedido_id}")
        logging.info(f"Dados recebidos: {dados}")
        
        # Extrair dados do pedido e histórico
        historico = dados.pop("historico", []) if "historico" in dados else []
        
        # Busca o pedido original para comparar depois
        pedido_original = await db["pedidos"].find_one({"id": pedido_id})
        if not pedido_original:
            raise HTTPException(status_code=404, detail="Pedido não encontrado.")
        
        # Preparar os dados para atualização do pedido usando os dados restantes
        update_data = dados
        
        # Converter a data de entrega se presente
        if "deliveryDate" in update_data:
            if isinstance(update_data["deliveryDate"], str):
                update_data["deliveryDate"] = validate_and_convert_date(update_data["deliveryDate"])
            elif isinstance(update_data["deliveryDate"], date):
                update_data["deliveryDate"] = datetime.combine(update_data["deliveryDate"], datetime.min.time())

        # Atualiza o pedido
        result = await db["pedidos"].update_one(
            {"id": pedido_id},
            {"$set": update_data}
        )

        # Salva o histórico de alterações caso tenha sido fornecido
        if historico and isinstance(historico, list):
            for registro in historico:
                # Garantir que tenha todos os campos necessários
                hist_data = {
                    "pedido_id": pedido_id,
                    "usuario_nome": registro.get("usuario_nome", dados.get("usuario_nome", "Sistema")),
                    "campo_alterado": registro.get("campo_alterado", ""),
                    "valor_anterior": registro.get("valor_anterior", ""),
                    "valor_novo": registro.get("valor_novo", ""),
                    "data_edicao": datetime.now()
                }
                await db["pedido_historico"].insert_one(hist_data)
                logging.info(f"Histórico de alteração registrado: {hist_data}")

        logging.info(f"Pedido atualizado com histórico: ID {pedido_id}")
        return {"message": "Pedido atualizado com sucesso!"}

    except Exception as e:
        logging.error(f"Erro ao atualizar pedido com histórico: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar pedido: {str(e)}")

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
        
        # Preparar os dados do histórico
        hist_data = {
            "pedido_id": pedido_id,
            "usuario_nome": dados.get("usuario_nome", current_user.get("nome", "Sistema")),
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
