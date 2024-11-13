from bson import ObjectId
from . import database, models, schemas
from passlib.context import CryptContext
import logging

# Função para converter ObjectId para string
def parse_obj_id(doc):
    if '_id' in doc:
        doc['_id'] = str(doc['_id']) 
    return doc

# Criação do contexto para a criptografia de senha - exigido aqui ou onde for implementar.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para criar um usuário no banco de dados
async def create_user(db, user: schemas.UsuarioCreate):
    # Criptografando a senha antes de salvar
    hashed_password = pwd_context.hash(user.senha)  
    user_dict = user.dict()
    user_dict["senha"] = hashed_password  
    
    # Inserindo o usuário no banco
    result = await db["users"].insert_one(user_dict)
    
    
    return parse_obj_id(user_dict)  

# Função para obter um usuário pelo e-mail
async def get_user_by_email(db, email: str):
    user = await db["users"].find_one({"email": email})
    if user:
        return parse_obj_id(user) 
    return None

# Log para verificar dados
logging.basicConfig(level=logging.DEBUG)

# Função para criar o pedido no banco de dados
async def create_pedido(db, pedido: models.Pedido, usuario_id: str):
    pedido_dict = pedido.dict(exclude_unset=True)
    pedido_dict['usuario_id'] = usuario_id  

    # Insere o pedido no banco de dados
    result = await db.pedidos.insert_one(pedido_dict)

    # Atribui o '_id' gerado pelo MongoDB
    pedido_dict['_id'] = result.inserted_id  

    logging.debug(f"Pedido inserido com _id: {pedido_dict['_id']}")

    return parse_obj_id(pedido_dict)  