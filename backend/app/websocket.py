import socketio
import logging
from fastapi import Depends
from typing import Dict, List, Set
from . import auth, database

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criação do servidor Socket.IO
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',  # Permitir todas as origens
    logger=True,
    engineio_logger=True,
    ping_timeout=60,  # Aumenta o timeout para evitar desconexões
    ping_interval=25,  # Ajusta o intervalo de ping
    always_connect=True,  # Sempre aceitar conexões durante o desenvolvimento
    max_http_buffer_size=1e6  # 1MB buffer
)

# Criação da aplicação ASGI Socket.IO
socket_app = socketio.ASGIApp(sio)

# Dicionário para armazenar conexões de usuários
# {email_usuario: [session_id1, session_id2, ...]}
connected_users: Dict[str, Set[str]] = {}

# Dicionário para armazenar conexões de sessões
# {session_id: email_usuario}
session_users: Dict[str, str] = {}

@sio.event
async def connect(sid, environ, auth_data):
    """
    Manipula novas conexões WebSocket.
    Autentica o usuário e armazena a conexão.
    """
    logger.info(f"Nova conexão WebSocket: {sid}")
    
    # Para desenvolvimento, permite conexões sem autenticação estrita
    try:
        # Obtém o token JWT para autenticação (se existir)
        token = auth_data.get('token', None) if auth_data else None
        
        if token:
            # Se tiver token, tenta decodificar e associar ao usuário
            db = await database.get_db()
            payload = await auth.decode_token(token)
            
            if payload and payload.get("sub"):
                email = payload.get("sub")
                
                # Trata o caso especial do token "authenticated"
                if email == "authenticated_user":
                    logger.info(f"Usuário autenticado via cookie: {sid}")
                    session_users[sid] = "cookie_authenticated"
                else:
                    # Armazena a sessão do usuário se encontrado
                    user = await db["users"].find_one({"email": email})
                    if user:
                        if email not in connected_users:
                            connected_users[email] = set()
                        connected_users[email].add(sid)
                        session_users[sid] = email
                        logger.info(f"Usuário autenticado: {email} (SID: {sid})")
                    else:
                        logger.warning(f"Usuário não encontrado para o token: {sid}")
                        session_users[sid] = "anonymous"  # Associa como anônimo
            else:
                logger.warning(f"Token inválido ou sem informação de usuário: {sid}")
                session_users[sid] = "anonymous"  # Associa como anônimo
        else:
            # Para desenvolvimento, permitir conexões sem token
            logger.warning(f"Conexão sem token (permitido para desenvolvimento): {sid}")
            session_users[sid] = "anonymous"  # Associa como anônimo
            
        # Envia confirmação de conexão
        await sio.emit('connection_established', {'status': 'connected'}, to=sid)
        return True
    
    except Exception as e:
        logger.error(f"Erro na autenticação da conexão WebSocket: {e}")
        # Mesmo com erro, permitimos a conexão para desenvolvimento
        session_users[sid] = "error_connection"
        await sio.emit('connection_established', {'status': 'connected_with_error', 'error': str(e)}, to=sid)
        return True  # Permite a conexão mesmo com erro

@sio.event
async def disconnect(sid):
    """
    Manipula desconexões WebSocket.
    Remove a sessão dos dicionários de controle.
    """
    logger.info(f"Conexão WebSocket encerrada: {sid}")
    
    # Remove a sessão do dicionário de sessões
    if sid in session_users:
        email = session_users[sid]
        if email in connected_users:
            connected_users[email].discard(sid)
            # Se não houver mais sessões ativas para o usuário, remove a entrada
            if not connected_users[email]:
                del connected_users[email]
        del session_users[sid]

async def send_notification(recipient_email: str, notification_type: str, data: dict):
    """
    Envia uma notificação para um usuário específico.
    Se o usuário estiver conectado, a notificação é enviada via WebSocket.
    
    Args:
        recipient_email: Email do usuário destinatário
        notification_type: Tipo da notificação (ex: "pedido_criado", "pedido_concluido")
        data: Dados da notificação
    """
    if recipient_email in connected_users:
        sessions = connected_users[recipient_email]
        for sid in sessions:
            try:
                await sio.emit('notification', {
                    'type': notification_type,
                    'data': data
                }, to=sid)
                logger.info(f"Notificação enviada para {recipient_email} (SID: {sid})")
            except Exception as e:
                logger.error(f"Erro ao enviar notificação para {sid}: {e}")

async def broadcast_to_all(event: str, data: dict):
    """
    Envia uma mensagem para todos os usuários conectados.
    
    Args:
        event: Nome do evento a ser emitido
        data: Dados a serem enviados
    """
    try:
        await sio.emit(event, data)
        logger.info(f"Broadcast enviado para todos os usuários: {event}")
    except Exception as e:
        logger.error(f"Erro ao enviar broadcast: {e}")

async def broadcast_to_admins(event: str, data: dict):
    """
    Envia uma mensagem apenas para usuários administradores.
    
    Args:
        event: Nome do evento a ser emitido
        data: Dados a serem enviados
    """
    # Implementação simplificada - na prática, você verificaria quais usuários são admins
    # e enviaria apenas para eles
    admin_sessions = []
    for email, sessions in connected_users.items():
        # Aqui você verificaria se o usuário é admin
        # Por enquanto, vamos assumir que emails com 'admin' são admins
        if 'admin' in email or 'gestor' in email:
            admin_sessions.extend(sessions)
    
    for sid in admin_sessions:
        try:
            await sio.emit(event, data, to=sid)
            logger.info(f"Notificação de admin enviada para SID: {sid}")
        except Exception as e:
            logger.error(f"Erro ao enviar notificação de admin para {sid}: {e}") 