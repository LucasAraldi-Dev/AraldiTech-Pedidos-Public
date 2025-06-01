import base64
from datetime import datetime
import logging
from . import models

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def encode_file_to_base64(file_path):
    with open(file_path, "rb") as file:
        encoded_content = base64.b64encode(file.read()).decode('utf-8')
    return encoded_content

# Função para obter o endereço IP real do cliente
def get_client_ip(request):
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        # O primeiro IP é o do cliente
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        # Fallback para o IP direto
        ip = request.client.host
    return ip

# Função para registrar uma nova atividade
async def registrar_atividade(db, tipo, descricao, usuario_nome, pedido_id=None, ip_address=None, user_agent=None, dados_adicionais=None):
    try:
        atividade = models.Atividade(
            tipo=tipo,
            descricao=descricao,
            usuario_nome=usuario_nome,
            pedido_id=pedido_id,
            data=datetime.now(),
            ip_address=ip_address,
            user_agent=user_agent,
            dados_adicionais=dados_adicionais
        )
        
        result = await db["atividades"].insert_one(atividade.dict())
        atividade.id = str(result.inserted_id)
        logger.info(f"Atividade registrada: {tipo} | {descricao[:50]}... | IP: {ip_address}")
        return atividade
    except Exception as e:
        logger.error(f"Erro ao registrar atividade: {e}")
        # Não lançamos exceção para não interromper o fluxo principal