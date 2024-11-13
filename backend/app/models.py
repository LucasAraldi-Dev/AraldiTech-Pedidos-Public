from datetime import datetime
from pydantic import BaseModel, EmailStr , Field , root_validator
from passlib.context import CryptContext
from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel
from typing import Optional


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelo de usuário para o MongoDB
class Usuario(BaseModel):
    id: Optional[str] = None  
    nome: str
    email: EmailStr
    senha: str
    setor: str = "Escritório"  

    class Config:
        arbitrary_types_allowed = True  
        orm_mode = True  

    def set_password(self, password: str):
        """Função para definir a senha criptografada"""
        self.senha = pwd_context.hash(password)

    def verify_password(self, password: str):
        """Função para verificar se a senha está correta"""
        return pwd_context.verify(password, self.senha)

    def json(self, **kwargs):
        # Convertendo ObjectId para string
        data = super().json(**kwargs)
        data = data.replace('ObjectId(', '').replace(')', '')
        return data


# Modelo de pedido para o MongoDB
class Pedido(BaseModel):
    id: int = Field(default=None)
    descricao: str
    quantidade: int
    urgencia: Optional[bool] = False
    observacao: Optional[str] = None
    anexo: Optional[str] = None
    status: Optional[str] = "Pendente"
    usuario_id: str
    deliveryDate: Optional[datetime] 
    sender: str
    
    

    class Config:
        json_encoders = {
            ObjectId: str,
        }
        
SETORES_VALIDOS = ["Fábrica de Ração", "Oficina", "Escritório"]