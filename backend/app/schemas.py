from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# Esquema para criação de usuário
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    setor: str

    class Config:
        arbitrary_types_allowed = True  

# Esquema de resposta do usuário
class Usuario(BaseModel):
    nome: str
    email: EmailStr
    setor: str

    class Config:
        arbitrary_types_allowed = True  

# Esquema para login de usuário
class LoginRequest(BaseModel):
    email: EmailStr
    senha: str

# Esquema de Token
class Token(BaseModel):
    access_token: str
    token_type: str
    nome: str  

# Esquema de criação de Pedido
class PedidoCreate(BaseModel):
    descricao: str
    quantidade: int
    observacao: Optional[str] = None
    urgencia: Optional[bool] = False  
    orderDeliveryDate: date
    sender: str
    file: Optional[str] = None  

    class Config:
        arbitrary_types_allowed = True
