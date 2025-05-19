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

# Função para registrar uma nova atividade
async def registrar_atividade(db, tipo, descricao, usuario_nome, pedido_id=None):
    try:
        atividade = models.Atividade(
            tipo=tipo,
            descricao=descricao,
            usuario_nome=usuario_nome,
            pedido_id=pedido_id,
            data=datetime.now()
        )
        
        result = await db["atividades"].insert_one(atividade.dict())
        atividade.id = str(result.inserted_id)
        logger.info(f"Atividade registrada: {atividade}")
        return atividade
    except Exception as e:
        logger.error(f"Erro ao registrar atividade: {e}")
        # Não lançamos exceção para não interromper o fluxo principal