import os
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# Obtém a URI do MongoDB da variável de ambiente
mongodb_uri = os.getenv("MONGODB_URI", "mongodb://192.168.1.5:27017")  

# Conectar ao MongoDB
client = AsyncIOMotorClient(mongodb_uri)
db = client["araldi_tech_db"] 

# Definindo as coleções
users_collection = db["users"]  
pedidos_collection = db["pedidos"]  

# Função para retornar a conexão com o banco de dados - Alguns locais exigem o retorno
async def get_db():
    return db

# Funções auxiliares para acessar as coleções (CRUD)
async def get_user_by_id(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
    return user

async def create_user(user_data: dict):
    result = await users_collection.insert_one(user_data)
    return str(result.inserted_id)

async def get_all_pedidos():
    return await pedidos_collection.find().to_list(length=100)

async def create_pedido(pedido_data: dict):
    result = await pedidos_collection.insert_one(pedido_data)
    return str(result.inserted_id)
