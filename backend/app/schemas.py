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
    tipo_usuario: str  

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
    categoria: str
    urgencia: Optional[str] = "Padrão"
    observacao: Optional[str] = None
    deliveryDate: date
    sender: str
    file: Optional[str] = None 
    status: Optional[str] = "Pendente"
    usuario_nome: str

    class Config:
        arbitrary_types_allowed = True


class PedidoRead(PedidoCreate):
    id: int  # O campo "id" agora é somente leitura para respostas