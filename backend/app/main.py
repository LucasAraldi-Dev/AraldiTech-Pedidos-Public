from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from . import crud, models, schemas, database, auth
import logging
from fastapi.security import OAuth2PasswordBearer
from .auth import get_current_user
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional , List
from .models import Pedido 
from fastapi import APIRouter, Depends
from . import auth

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Lista de origens permitidas para CORS - Personalizar conforme o que o sistema te dar.
origins = [
    "http://localhost:8080",
    "http://localhost",
    "http://localhost:8000",
    "http://192.168.1.3",
    "http://192.168.1.3:8080",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Rota de criação de usuário
@app.post("/users/", response_model=schemas.Usuario)
async def create_user(user: schemas.UsuarioCreate, db=Depends(database.get_db)):
    try:
        return await crud.create_user(db=db, user=user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Rota de login e gerar o token do usuario
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: schemas.LoginRequest, db=Depends(database.get_db)):
    user = await auth.authenticate_user(db, form_data.email, form_data.senha)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access_token = auth.create_access_token(data={"sub": user['email'], "nome": user['nome']})
    return {"access_token": access_token, "token_type": "bearer", "nome": user["nome"]}

@app.get("/auth/validate-token")
async def validate_token(token: str = Depends(auth.oauth2_scheme), db=Depends(database.get_db)):
    user = await auth.get_current_user(token=token, db=db)
    return {"status": "valid", "user": user["email"]}

# Função para obter o próximo ID
async def get_last_id(db):
    last_pedido = await db.pedidos.find().sort("id", -1).limit(1).to_list(1)
    return last_pedido[0]["id"] + 1 if last_pedido else 1

@app.post("/pedidos/", response_model=models.Pedido)
async def criar_pedido(pedido: models.Pedido, db=Depends(database.get_db)):
    logging.info("Criando novo pedido")

    pedido.deliveryDate = datetime.combine(pedido.deliveryDate, datetime.min.time())  
    pedido.id = await get_last_id(db)
    pedido_dict = pedido.dict()

    # Insere o pedido no banco de dados
    result = await db.pedidos.insert_one(pedido_dict)
    pedido.id = str(result.inserted_id)

    # Formata a data para a maneira que quiser ! 
    if pedido.deliveryDate:
        pedido.deliveryDate = pedido.deliveryDate.strftime("%d-%m-%y")

    logging.info("Pedido inserido com ID: %s", result.inserted_id)
    
    return pedido

# Rota para obter a lista de pedidos do sistema
@app.get("/pedidos/", response_model=List[models.Pedido])
async def listar_pedidos(db=Depends(database.get_db), current_user=Depends(get_current_user)):
    logging.info("Consultando pedidos para o usuário %s", current_user)

    # Filtra os pedidos do banco de dados
    pedidos = await db.pedidos.find().to_list(None)  

    # Converte o ObjectId para string, se necessário, para cada pedido
    for pedido in pedidos:
        pedido["_id"] = str(pedido["_id"])

    # Log para confirmar os pedidos retornados do pedido
    logging.info("Pedidos encontrados: %s", pedidos)

    return pedidos