from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import date, datetime

# Esquema para criação de usuário
class UsuarioCreate(BaseModel):
    nome: str
    username: str
    email: EmailStr
    senha: str
    setor: str
    tipo_usuario: Optional[str] = "comum"  # tipo de usuário fixo como "comum" por padrão
    termsAcceptance: Optional[dict] = None  # dados de aceitação dos termos de serviço

    class Config:
        arbitrary_types_allowed = True  

# Esquema de resposta do usuário
class Usuario(BaseModel):
    nome: str
    username: str
    email: EmailStr
    setor: str
    tipo_usuario: str  

    class Config:
        arbitrary_types_allowed = True  

# Esquema para login de usuário
class LoginRequest(BaseModel):
    username: str
    senha: str

# Esquema de Token
class Token(BaseModel):
    access_token: str
    token_type: str
    nome: str
    tipo_usuario: str
    setor: str
    primeiro_login: Optional[bool] = False

# Esquema de criação de Pedido
class PedidoCreate(BaseModel):
    descricao: str
    quantidade: int
    categoria: Optional[str] = None
    urgencia: Optional[str] = "Padrão"
    observacao: Optional[str] = None
    deliveryDate: date
    sender: Optional[str] = None
    file: Optional[str] = None
    status: Optional[str] = "Pendente"
    usuario_nome: Optional[str] = None
    historico: Optional[List[dict]] = None
    completionDate: Optional[date] = None
    setor: Optional[str] = None
    # Novos campos para orçamento e custos
    orcamento_previsto: Optional[float] = 0.0
    custo_real: Optional[float] = 0.0
    observacao_orcamento: Optional[str] = None
    fornecedor: Optional[str] = None

    # Validando e convertendo a data corretamente
    @validator("deliveryDate", pre=True)
    def parse_delivery_date(cls, value):
        if isinstance(value, str):
            try:
                # Converter string para date
                return datetime.fromisoformat(value).date()
            except ValueError:
                raise ValueError("Formato de data inválido. Esperado: yyyy-MM-dd.")
        return value
        
    # Validando e convertendo a data de conclusão
    @validator("completionDate", pre=True)
    def parse_completion_date(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            try:
                # Converter string para date
                return datetime.fromisoformat(value).date()
            except ValueError:
                raise ValueError("Formato de data de conclusão inválido. Esperado: yyyy-MM-dd.")
        return value

    # Validando valores numéricos para orçamento e custo
    @validator("orcamento_previsto", "custo_real", pre=True)
    def validate_valores(cls, value):
        if value is None:
            return 0.0
        if isinstance(value, str) and value.strip():
            try:
                return float(value.replace(',', '.'))
            except ValueError:
                raise ValueError("Valor numérico inválido para orçamento ou custo.")
        return value

    class Config:
        arbitrary_types_allowed = True
        
    # Customizando a serialização de date para string no formato ISO
    @classmethod
    def json(cls, obj):
        if isinstance(obj, date):
            return obj.isoformat()  # Converte para "YYYY-MM-DD"
        return super().json(obj)


class PedidoRead(PedidoCreate):
    id: int  # O campo "id" agora é somente leitura para respostas

# Esquema para histórico de edições
class PedidoHistoricoCreate(BaseModel):
    pedido_id: int
    usuario_nome: str
    campo_alterado: str
    valor_anterior: str
    valor_novo: str
    
    class Config:
        arbitrary_types_allowed = True

# Esquema para atividades
class Atividade(BaseModel):
    id: Optional[str] = None
    tipo: str  # criacao, edicao, conclusao, cancelamento, login, registro, orcamento
    descricao: str
    usuario_nome: str
    data: datetime = Field(default_factory=datetime.now)
    pedido_id: Optional[int] = None
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

# Esquema para relatórios
class RelatorioParams(BaseModel):
    tipo: str  # pedidos, atividades, financeiro
    periodo: str  # diario, semanal, mensal, personalizado
    formato: str  # pdf, excel
    dataInicial: Optional[date] = None
    dataFinal: Optional[date] = None
    
    @validator('dataInicial', 'dataFinal', pre=True)
    def parse_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value).date()
            except ValueError:
                raise ValueError("Formato de data inválido. Esperado: yyyy-MM-dd.")
        return value
    
    class Config:
        arbitrary_types_allowed = True