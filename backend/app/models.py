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
    tipo_usuario: str = "comum"  # comum, gestor ou admin
    termsAcceptance: Optional[dict] = None  # Informações de aceite dos termos
    termsAcceptanceDate: Optional[datetime] = None  # Data de aceitação dos termos

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
    conclusao_data: Optional[datetime] = None
    setor: Optional[str] = None  # Setor ao qual o pedido pertence
    # Novos campos para orçamento e custos
    orcamento_previsto: Optional[float] = 0.0  # Valor estimado para o pedido
    custo_real: Optional[float] = 0.0  # Valor real gasto no pedido
    observacao_orcamento: Optional[str] = None  # Observações sobre o orçamento
    data_orcamento: Optional[datetime] = None  # Data de registro do orçamento
    data_custo_real: Optional[datetime] = None  # Data de registro do custo real
    fornecedor: Optional[str] = None  # Fornecedor escolhido

    class Config:
        json_encoders = {
            ObjectId: str,
        }

# Setores válidos
SETORES_VALIDOS = [
    "Escritório", 
    "Fábrica de Ração", 
    "CPO", 
    "Granjas", 
    "Abatedouro", 
    "Transporte", 
    "Incubatório", 
    "Favorito"
]

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

# Modelo de atividade para o MongoDB
class Atividade(BaseModel):
    id: Optional[str] = None
    tipo: str  # criacao, edicao, conclusao, cancelamento, login, registro, orcamento
    descricao: str
    usuario_nome: str
    data: datetime = Field(default_factory=datetime.now)
    pedido_id: Optional[int] = None
    
    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat(),
        }
