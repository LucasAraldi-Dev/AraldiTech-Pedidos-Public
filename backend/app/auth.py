from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .database import get_user_by_id, get_db
import logging

# Configurações de autenticação
SECRET_KEY = "e4b72b4175f5e0b453881b8648bbf0d42ef56fc4c25a1c7b347fbf88c0f601ef"  # Alterar ou mascarar depois
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Configuração do gerenciador de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # URL de login para gerar o token

# Funções de senha
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

# Função para autenticar usuário
async def authenticate_user(db, username: str, senha: str):
    """Valida o usuário a partir do banco e verifica a senha."""
    try:
        user = await db["users"].find_one({"username": username})
        
        if not user:
            logging.warning(f"Usuário não encontrado: {username}")
            return None
            
        if not verify_password(senha, user["senha"]):
            logging.warning(f"Senha incorreta para usuário: {username}")
            return None
        
        # Logging detalhado para diagnóstico
        logging.info(f"Tentativa de login para {username} - ID: {user.get('_id')}")
        logging.info(f"Tipo de usuário: {user.get('tipo_usuario', 'não definido')}")
        logging.info(f"Sessão expirada: {user.get('sessao_expirada', False)}")
        
        # Garante que todos os usuários tenham campos necessários definidos
        update_operations = {}
        
        # Campo tipo_usuario
        if "tipo_usuario" not in user:
            update_operations["tipo_usuario"] = "comum"
            logging.info(f"Campo tipo_usuario não definido para {username}, definindo como 'comum'")
        
        # Verifica se o usuário precisa renovar a sessão após alteração de permissões
        if user.get("sessao_expirada", False):
            logging.info(f"Removendo flag de sessao_expirada para {username} após login bem-sucedido")
            update_operations["sessao_expirada"] = False
            
        # Se há operações de atualização, aplicá-las
        if update_operations:
            logging.info(f"Atualizando campos do usuário {username}: {update_operations}")
            await db["users"].update_one(
                {"_id": user["_id"]},
                {"$set": update_operations}
            )
            # Atualizar os valores localmente também
            for key, value in update_operations.items():
                user[key] = value
        
        logging.info(f"Usuário autenticado com sucesso: {user.get('nome')} - Tipo: {user.get('tipo_usuario')}")
        return user
    except Exception as e:
        logging.error(f"Erro durante autenticação de {username}: {str(e)}")
        return None

# Função para criar o token de acesso
def create_access_token(data: dict):
    """Gera um JWT com dados de payload."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para obter o usuário atual
async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    """Valida o token e retorna o usuário correspondente."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Buscar o usuário no banco de dados para verificar suas informações atuais
        user = await db["users"].find_one({"username": username})
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        # Verificar se há diferença entre o tipo_usuario no token e no banco de dados
        tipo_usuario_token = payload.get("tipo_usuario")
        tipo_usuario_db = user.get("tipo_usuario", "comum")
        
        if tipo_usuario_token and tipo_usuario_token != tipo_usuario_db:
            logging.warning(f"Diferença detectada no tipo_usuario: Token={tipo_usuario_token}, DB={tipo_usuario_db}")
            logging.info(f"Priorizando tipo_usuario do banco de dados: {tipo_usuario_db}")
        
        return user
    except JWTError as e:
        logging.error(f"Erro ao decodificar token JWT: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Função para obter o tipo de usuário
async def get_user_type(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    """Retorna o tipo de usuário ('comum' ou 'gestor')."""
    user = await get_current_user(token, db)
    return user.get('tipo_usuario', 'comum')  # Padrão é 'comum' se o campo não existir