from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status

from backend.app import schemas
from . import models, crud, database
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends
from . import auth


SECRET_KEY = "e4b72b4175f5e0b453881b8648bbf0d42ef56fc4c25a1c7b347fbf88c0f601ef"  # Alterar ou mascarar depois
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "sub": data.get("sub", ""), "nome": data.get("nome", "")})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def login_for_access_token(form_data: schemas.LoginRequest, db=Depends(database.get_db)):
    user = await authenticate_user(db, form_data.email, form_data.senha)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access_token = create_access_token(data={"sub": user['email'], "nome": user['nome']})
    return {"access_token": access_token, "token_type": "bearer", "nome": user["nome"]}

async def authenticate_user(db, email: str, password: str):
    user = await crud.get_user_by_email(db, email=email)
    if user and pwd_context.verify(password, user["senha"]):
        return user
    return None

async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(database.get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        user = await crud.get_user_by_email(db, email=email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid or expired")
    return user
