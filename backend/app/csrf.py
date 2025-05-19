from fastapi import Request, HTTPException, status, Depends
from fastapi.security import APIKeyCookie
from jose import jwt, JWTError
import secrets
from datetime import datetime, timedelta
from typing import Optional
import logging
import os

# Obter a chave secreta do ambiente ou usar uma padrão (apenas para desenvolvimento)
CSRF_SECRET_KEY = os.environ.get("CSRF_SECRET_KEY", "csrf_secret_key_must_be_very_secure_and_random")
CSRF_ALGORITHM = "HS256"
CSRF_TOKEN_EXPIRE_MINUTES = 60  # 1 hora de validade

# Nome do cookie e do header para o token CSRF
CSRF_COOKIE_NAME = "csrf_token"
CSRF_HEADER_NAME = "X-CSRF-Token"

# Configurações de ambiente
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
ENFORCE_CSRF = os.environ.get("ENFORCE_CSRF", "True").lower() in ["true", "1", "yes"]

# Classe para validar o token CSRF nos cookies
class CSRFTokenCookie(APIKeyCookie):
    def __init__(self):
        super().__init__(name=CSRF_COOKIE_NAME, auto_error=False)

csrf_cookie_scheme = CSRFTokenCookie()

def generate_csrf_token(data: Optional[dict] = None) -> str:
    """
    Gera um token CSRF seguro.
    
    Args:
        data: Dados opcionais a serem incluídos no token
        
    Returns:
        String contendo o token JWT assinado
    """
    if data is None:
        data = {}
    
    # Adiciona um valor aleatório para garantir unicidade
    data.update({"nonce": secrets.token_hex(16)})
    
    # Define o tempo de expiração
    expire = datetime.utcnow() + timedelta(minutes=CSRF_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire.timestamp()})
    
    # Adiciona carimbo de tempo de criação
    data.update({"iat": datetime.utcnow().timestamp()})
    
    # Codifica o token
    token = jwt.encode(data, CSRF_SECRET_KEY, algorithm=CSRF_ALGORITHM)
    logging.info(f"Token CSRF gerado com sucesso. Expira em: {expire.isoformat()}")
    
    return token

def verify_csrf_token(token: str, expected_data: Optional[dict] = None) -> bool:
    """
    Verifica se o token CSRF é válido.
    
    Args:
        token: O token CSRF a ser validado
        expected_data: Dados que devem estar presentes no token
        
    Returns:
        True se o token for válido, False caso contrário
    """
    try:
        payload = jwt.decode(token, CSRF_SECRET_KEY, algorithms=[CSRF_ALGORITHM])
        
        # Verifica se o token expirou
        exp = payload.get("exp")
        if exp and datetime.utcnow().timestamp() > exp:
            logging.warning("Token CSRF expirado")
            return False
        
        # Verifica tempo de criação (se for do futuro, é inválido)
        iat = payload.get("iat")
        if iat and datetime.utcnow().timestamp() < iat:
            logging.warning("Token CSRF com data de criação no futuro (possível manipulação)")
            return False
        
        # Verifica se os dados esperados estão presentes
        if expected_data:
            for key, value in expected_data.items():
                if payload.get(key) != value:
                    logging.warning(f"Token CSRF não contém o valor esperado para {key}")
                    return False
        
        # Verifica se tem o nonce (garantia de que foi gerado corretamente)
        if not payload.get("nonce"):
            logging.warning("Token CSRF sem nonce")
            return False
        
        return True
    except JWTError as e:
        logging.error(f"Erro ao decodificar token CSRF: {str(e)}")
        return False
    except Exception as e:
        logging.error(f"Erro inesperado ao verificar token CSRF: {str(e)}")
        return False

async def validate_csrf_token(request: Request, csrf_token: str = None):
    """
    Valida o token CSRF na requisição.
    
    Args:
        request: Objeto da requisição FastAPI
        csrf_token: Token CSRF explícito (opcional)
        
    Returns:
        True se o token for válido
        
    Raises:
        HTTPException: Se o token estiver ausente ou for inválido
    """
    # Registra informação do método e caminho para diagnóstico
    logging.info(f"Validando CSRF para {request.method} {request.url.path}")
    
    # Obtém o token do cabeçalho X-CSRF-Token
    if not csrf_token:
        csrf_token = request.headers.get(CSRF_HEADER_NAME)
    
    # Obtém o token do cookie
    cookie_token = request.cookies.get(CSRF_COOKIE_NAME)
    
    # Logs detalhados para diagnóstico
    logging.info(f"Token no cabeçalho: {bool(csrf_token)}, Token no cookie: {bool(cookie_token)}")
    
    # Verificação de presença de tokens
    if not csrf_token or not cookie_token:
        logging.warning(f"Token CSRF ausente - Cabeçalho: {bool(csrf_token)}, Cookie: {bool(cookie_token)}")
        
        # Em ambiente de desenvolvimento, podemos permitir requisições sem token
        if ENVIRONMENT == "development" and not ENFORCE_CSRF:
            logging.warning("Ignorando validação CSRF em ambiente de desenvolvimento")
            return True
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token CSRF ausente. Recarregue a página e tente novamente."
        )
    
    # Verificação de correspondência de tokens
    if csrf_token != cookie_token:
        logging.warning(f"Tokens CSRF não correspondem - Header: {csrf_token[:10]}..., Cookie: {cookie_token[:10]}...")
        
        # Em ambiente de desenvolvimento, podemos permitir requisições com tokens diferentes
        if ENVIRONMENT == "development" and not ENFORCE_CSRF:
            logging.warning("Ignorando diferença entre tokens CSRF em ambiente de desenvolvimento")
            return True
            
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token CSRF inválido. Recarregue a página e tente novamente."
        )
    
    # Verificação de validade do token
    if not verify_csrf_token(csrf_token):
        logging.warning("Token CSRF inválido ou expirado")
        
        # Em ambiente de desenvolvimento, podemos permitir requisições com tokens inválidos
        if ENVIRONMENT == "development" and not ENFORCE_CSRF:
            logging.warning("Ignorando token CSRF inválido em ambiente de desenvolvimento")
            return True
            
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token CSRF expirado. Recarregue a página e tente novamente."
        )
    
    logging.info(f"Validação CSRF bem-sucedida para {request.method} {request.url.path}")
    return True

def require_csrf(request: Request):
    """
    Dependência para requerer validação CSRF em rotas específicas.
    
    Args:
        request: Objeto da requisição FastAPI
        
    Returns:
        True se o token for válido
    """
    return validate_csrf_token(request)