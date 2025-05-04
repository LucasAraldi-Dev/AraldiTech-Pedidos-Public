from fastapi import Request, HTTPException, status
from fastapi.security import APIKeyCookie
from jose import jwt
import secrets
from datetime import datetime, timedelta
from typing import Optional

# Configurações para o token CSRF
CSRF_SECRET_KEY = "csrf_secret_key_must_be_very_secure_and_random"
CSRF_ALGORITHM = "HS256"
CSRF_TOKEN_EXPIRE_MINUTES = 60

# Nome do cookie que armazenará o token CSRF
CSRF_TOKEN_NAME = "csrf_token"

# Classe para validar o token CSRF nos cookies
class CSRFTokenCookie(APIKeyCookie):
    def __init__(self):
        super().__init__(name=CSRF_TOKEN_NAME, auto_error=False)

csrf_cookie_scheme = CSRFTokenCookie()

def generate_csrf_token(data: Optional[dict] = None) -> str:
    """Gera um token CSRF."""
    if data is None:
        data = {}
    
    # Adiciona um valor aleatório para garantir unicidade
    data.update({"random": secrets.token_hex(16)})
    
    # Define o tempo de expiração
    expire = datetime.utcnow() + timedelta(minutes=CSRF_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire.timestamp()})
    
    # Codifica o token
    return jwt.encode(data, CSRF_SECRET_KEY, algorithm=CSRF_ALGORITHM)

def verify_csrf_token(token: str, expected_data: Optional[dict] = None) -> bool:
    """Verifica se o token CSRF é válido."""
    try:
        payload = jwt.decode(token, CSRF_SECRET_KEY, algorithms=[CSRF_ALGORITHM])
        
        # Verifica se o token expirou
        exp = payload.get("exp")
        if exp and datetime.utcnow().timestamp() > exp:
            return False
        
        # Verifica se os dados esperados estão presentes
        if expected_data:
            for key, value in expected_data.items():
                if payload.get(key) != value:
                    return False
        
        return True
    except Exception:
        return False

async def validate_csrf_token(request: Request, csrf_token: str = None):
    """Valida o token CSRF na requisição."""
    # Obtém o token do cabeçalho X-CSRF-Token
    if not csrf_token:
        csrf_token = request.headers.get("X-CSRF-Token")
    
    # Se não houver token, lança exceção
    if not csrf_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token CSRF ausente"
        )
    
    # Verifica se o token é válido
    if not verify_csrf_token(csrf_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token CSRF inválido ou expirado"
        )
    
    return True