from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

# Esquema para criação de usuário
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    setor: str
    tipo_usuario: Optional[str] = "comum"  # tipo de usuário fixo como "comum" por padrão

    class Config:
        arbitrary_types_allowed = True  

# Esquema de resposta do usuário
class Usuario(BaseModel):
    nome: str
    email: EmailStr
    setor: str
    tipo_usuario: str  # Adicionando tipo de usuário na resposta também

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
    categoria: str  # Adicionando categoria do produto
    urgencia: Optional[str] = "Padrão"  # Alterado para str com valores Padrão, Urgente, Crítico
    observacao: Optional[str] = None
    deliveryDate: date
    sender: str
    file: Optional[str] = None  
    status: Optional[str] = "Pendente"

    class Config:
        arbitrary_types_allowed = True