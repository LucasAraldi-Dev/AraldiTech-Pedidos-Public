from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .database import get_user_by_id, get_db

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
    user = await db["users"].find_one({"username": username})
    if not user or not verify_password(senha, user["senha"]):
        return None
    
    # Garante que todos os usuários tenham um tipo_usuario definido
    if "tipo_usuario" not in user:
        user["tipo_usuario"] = "comum"
        # Atualiza o usuário no banco se necessário
        await db["users"].update_one(
            {"_id": user["_id"]},
            {"$set": {"tipo_usuario": "comum"}}
        )
    
    print(f"Usuário autenticado: {user.get('nome')} - Tipo: {user.get('tipo_usuario')}")
    return user

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
        user = await db["users"].find_one({"username": username})
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return user
    except JWTError:
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