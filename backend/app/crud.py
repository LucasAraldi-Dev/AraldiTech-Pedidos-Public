from bson import ObjectId
from . import database, models, schemas
from passlib.context import CryptContext
import logging

# Função para converter ObjectId para string
def parse_obj_id(doc):
    if '_id' in doc:
        doc['_id'] = str(doc['_id']) 
    return doc

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

# Função para criar o pedido no banco de dados
async def create_pedido(db, pedido: schemas.PedidoCreate, usuario_id: str):
    pedido_dict = pedido.dict(exclude_unset=True)
    pedido_dict['usuario_id'] = usuario_id  

    # Atribuindo os valores padrões para categoria e urgência, se não informados
    if 'categoria' not in pedido_dict:
        pedido_dict['categoria'] = "Matérias-primas"  # Valor padrão
    if 'urgencia' not in pedido_dict:
        pedido_dict['urgencia'] = "Padrão"  # Valor padrão

    # Insere o pedido no banco de dados
    result = await db.pedidos.insert_one(pedido_dict)

    # Atribui o '_id' gerado pelo MongoDB
    pedido_dict['_id'] = result.inserted_id  

    logging.debug(f"Pedido inserido com _id: {pedido_dict['_id']}")

    return parse_obj_id(pedido_dict)  

# Função para obter um pedido pelo ID
async def get_pedido_by_id(db, pedido_id: str):
    pedido = await db.pedidos.find_one({"_id": ObjectId(pedido_id)})
    if pedido:
        return parse_obj_id(pedido)
    return None

# Função para listar pedidos de um usuário
async def get_pedidos_by_usuario(db, usuario_id: str, status: Optional[str] = None):
    query = {"usuario_id": usuario_id}
    if status:
        query['status'] = status
    
    pedidos = db.pedidos.find(query)
    pedidos_list = []
    
    async for pedido in pedidos:
        pedidos_list.append(parse_obj_id(pedido))
    
    return pedidos_list

# Função para editar um pedido (somente para gestores)
async def editar_pedido(db, pedido_id: str, usuario_id: str, novo_pedido: schemas.PedidoCreate):
    # Verificando se o usuário é um gestor
    usuario = await db["users"].find_one({"_id": ObjectId(usuario_id)})
    if usuario and usuario.get("tipo_usuario") == "gestor":
        # Permitir a edição do pedido
        pedido = await db.pedidos.find_one({"_id": ObjectId(pedido_id)})
        if pedido:
            pedido_dict = novo_pedido.dict(exclude_unset=True)
            await db.pedidos.update_one({"_id": ObjectId(pedido_id)}, {"$set": pedido_dict})
            return parse_obj_id(pedido)
    else:
        raise PermissionError("Você não tem permissão para editar este pedido.")
        
# Função para excluir um pedido (somente para gestores)
async def excluir_pedido(db, pedido_id: str, usuario_id: str):
    # Verificando se o usuário é um gestor
    usuario = await db["users"].find_one({"_id": ObjectId(usuario_id)})
    if usuario and usuario.get("tipo_usuario") == "gestor":
        # Permitir a exclusão do pedido
        pedido = await db.pedidos.find_one({"_id": ObjectId(pedido_id)})
        if pedido:
            await db.pedidos.delete_one({"_id": ObjectId(pedido_id)})
            return {"message": "Pedido excluído com sucesso."}
    else:
        raise PermissionError("Você não tem permissão para excluir este pedido.")
