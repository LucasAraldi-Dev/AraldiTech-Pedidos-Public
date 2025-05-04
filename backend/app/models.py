from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, root_validator
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
    username: str
    email: EmailStr
    senha: str
    setor: str = "Escritório"
    tipo_usuario: str = "comum"  # novo campo para tipo de usuário (comum ou gestor)

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
    id: Optional[int] = None  # Pode ser None até ser gerado
    descricao: str
    quantidade: int
    urgencia: Optional[str] = "Padrão"  # Padrão, Urgente ou Crítico
    categoria: Optional[str] = None
    observacao: Optional[str] = None
    anexo: Optional[str] = None
    status: Optional[str] = "Pendente"
    usuario_nome: Optional[str] = None
    deliveryDate: Optional[datetime]
    sender: Optional[str] = None

    class Config:
        json_encoders = {
            ObjectId: str,
        }

# Setores válidos
SETORES_VALIDOS = ["Fábrica de Ração", "Oficina", "Escritório"]

# Categorias de produto válidas
CATEGORIAS_VALIDAS = [
    "Matérias-primas", 
    "Equipamentos e Máquinas", 
    "Peças de Reposição", 
    "Serviços", 
    "Mercadorias diversas"
]

# Modelo para histórico de edições de pedidos
class PedidoHistorico(BaseModel):
    pedido_id: int
    usuario_nome: str
    data_edicao: datetime = Field(default_factory=datetime.now)
    campo_alterado: str
    valor_anterior: str
    valor_novo: str
    
    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat(),
        }
