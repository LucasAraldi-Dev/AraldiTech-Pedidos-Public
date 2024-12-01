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

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Configuração de CORS
origins = [
    "http://localhost:8080",
    "http://localhost",
    "http://localhost:8000",
    "http://192.168.10.27",
    "http://192.168.10.27:8080",
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
    user = await auth.authenticate_user(db, form_data.email, form_data.senha)
    if not user:
        logging.warning("Credenciais inválidas fornecidas.")
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access_token = auth.create_access_token(data={"sub": user["email"], "nome": user["nome"]})
    logging.info(f"Token gerado com sucesso para o usuário: {user['email']}")
    return {"access_token": access_token, "token_type": "bearer", "nome": user["nome"]}

# Rota para validação de token
@app.get("/auth/validate-token")
async def validate_token(token: str = Depends(auth.oauth2_scheme), db=Depends(database.get_db)):
    user = await auth.get_current_user(token=token, db=db)
    logging.info(f"Token validado para o usuário: {user['email']}")
    return {"status": "valid", "user": user["email"]}

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
