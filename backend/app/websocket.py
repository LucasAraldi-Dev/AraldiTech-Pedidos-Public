import socketio
import logging
from fastapi import Depends
from typing import Dict, List, Set
from . import auth, database
from datetime import datetime
from jose import jwt, JWTError

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
            try:
                db = await database.get_db()
                # Decodificar o token JWT usando o mesmo método do auth.py
                payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
                
                if payload and payload.get("sub"):
                    username = payload.get("sub")
                    
                    # Buscar o usuário no banco de dados
                    user = await db["users"].find_one({"username": username})
                    if user:
                        user_email = user.get("email")
                        if user_email:
                            if user_email not in connected_users:
                                connected_users[user_email] = set()
                            connected_users[user_email].add(sid)
                            session_users[sid] = user_email
                            logger.info(f"[WEBSOCKET DEBUG] Usuário autenticado: {user_email} (SID: {sid})")
                            logger.info(f"[WEBSOCKET DEBUG] Total de usuários conectados: {len(connected_users)}")
                        else:
                            logger.warning(f"Usuário sem email: {username} (SID: {sid})")
                            session_users[sid] = "no_email"
                    else:
                        logger.warning(f"Usuário não encontrado para o token: {username} (SID: {sid})")
                        session_users[sid] = "user_not_found"
                else:
                    logger.warning(f"Token inválido ou sem informação de usuário: {sid}")
                    session_users[sid] = "invalid_token"
            except JWTError as e:
                logger.error(f"Erro JWT ao decodificar token: {e}")
                session_users[sid] = "jwt_error"
            except Exception as e:
                logger.error(f"Erro geral ao decodificar token: {e}")
                session_users[sid] = "token_error"
        else:
            # Para desenvolvimento, permitir conexões sem token
            logger.warning(f"Conexão sem token (permitido para desenvolvimento): {sid}")
            session_users[sid] = "anonymous"  # Associa como anônimo
            
        # Envia confirmação de conexão
        if session_users[sid] in ["jwt_error", "token_error", "invalid_token"]:
            await sio.emit('connection_established', {'status': 'connected_with_error', 'error': f'Erro de autenticação: {session_users[sid]}'}, to=sid)
        else:
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

async def send_notification_to_sector(setor: str, notification_type: str, data: dict):
    """
    Envia notificação para todos os usuários de um setor específico.
    
    Args:
        setor: Nome do setor
        notification_type: Tipo da notificação
        data: Dados da notificação
    """
    try:
        logger.info(f"[WEBSOCKET DEBUG] Iniciando envio para setor {setor}")
        
        # Buscar usuários do setor no banco de dados
        db = await database.get_db()
        users_in_sector = await db["users"].find({"setor": setor}).to_list(None)
        
        logger.info(f"[WEBSOCKET DEBUG] Encontrados {len(users_in_sector)} usuários no setor {setor}")
        logger.info(f"[WEBSOCKET DEBUG] Usuários conectados atualmente: {list(connected_users.keys())}")
        
        notification_data = {
            'type': notification_type,
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'setor': setor
        }
        
        # Enviar para cada usuário do setor que estiver conectado
        notifications_sent = 0
        for user in users_in_sector:
            user_email = user.get("email")
            logger.info(f"[WEBSOCKET DEBUG] Verificando usuário {user_email}")
            
            if user_email and user_email in connected_users:
                sessions = connected_users[user_email]
                logger.info(f"[WEBSOCKET DEBUG] Usuário {user_email} está conectado com {len(sessions)} sessões")
                
                for sid in sessions:
                    try:
                        await sio.emit('notification', notification_data, to=sid)
                        logger.info(f"[WEBSOCKET DEBUG] Notificação enviada para usuário {user_email} do setor {setor} (SID: {sid})")
                        notifications_sent += 1
                    except Exception as e:
                        logger.error(f"[WEBSOCKET ERROR] Erro ao enviar notificação para {sid}: {e}")
            else:
                logger.info(f"[WEBSOCKET DEBUG] Usuário {user_email} não está conectado")
        
        logger.info(f"[WEBSOCKET DEBUG] Notificação enviada para o setor {setor}: {notifications_sent} notificações enviadas de {len(users_in_sector)} usuários")
        
    except Exception as e:
        logger.error(f"[WEBSOCKET ERROR] Erro ao enviar notificação para o setor {setor}: {e}")
        logger.exception("Detalhes do erro:")

async def send_notification_to_admins_gestores(notification_type: str, data: dict):
    """
    Envia notificação para todos os administradores e gestores.
    
    Args:
        notification_type: Tipo da notificação
        data: Dados da notificação
    """
    try:
        logger.info(f"[WEBSOCKET DEBUG] Iniciando envio para admins/gestores")
        
        # Buscar admins e gestores no banco de dados
        db = await database.get_db()
        admins_gestores = await db["users"].find({
            "tipo_usuario": {"$in": ["admin", "gestor"]}
        }).to_list(None)
        
        logger.info(f"[WEBSOCKET DEBUG] Encontrados {len(admins_gestores)} admins/gestores")
        
        notification_data = {
            'type': notification_type,
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'target': 'admins_gestores'
        }
        
        # Enviar para cada admin/gestor que estiver conectado
        notifications_sent = 0
        for user in admins_gestores:
            user_email = user.get("email")
            logger.info(f"[WEBSOCKET DEBUG] Verificando admin/gestor {user_email}")
            
            if user_email and user_email in connected_users:
                sessions = connected_users[user_email]
                logger.info(f"[WEBSOCKET DEBUG] Admin/gestor {user_email} está conectado com {len(sessions)} sessões")
                
                for sid in sessions:
                    try:
                        await sio.emit('notification', notification_data, to=sid)
                        logger.info(f"[WEBSOCKET DEBUG] Notificação enviada para admin/gestor {user_email} (SID: {sid})")
                        notifications_sent += 1
                    except Exception as e:
                        logger.error(f"[WEBSOCKET ERROR] Erro ao enviar notificação para {sid}: {e}")
            else:
                logger.info(f"[WEBSOCKET DEBUG] Admin/gestor {user_email} não está conectado")
        
        logger.info(f"[WEBSOCKET DEBUG] Notificação enviada para admins/gestores: {notifications_sent} notificações enviadas de {len(admins_gestores)} usuários")
        
    except Exception as e:
        logger.error(f"[WEBSOCKET ERROR] Erro ao enviar notificação para admins/gestores: {e}")
        logger.exception("Detalhes do erro:")

async def send_smart_notification(setor: str, notification_type: str, data: dict):
    """
    Envia notificação de forma inteligente, evitando duplicatas.
    
    - Usuários comuns: recebem apenas se forem do setor
    - Admins/Gestores: recebem independente do setor, mas apenas UMA vez
    
    Args:
        setor: Nome do setor do pedido
        notification_type: Tipo da notificação
        data: Dados da notificação
    """
    try:
        logger.info(f"[WEBSOCKET SMART] Iniciando envio inteligente para setor {setor}")
        
        # Buscar todos os usuários
        db = await database.get_db()
        all_users = await db["users"].find({}).to_list(None)
        
        logger.info(f"[WEBSOCKET SMART] Encontrados {len(all_users)} usuários no total")
        
        notification_data = {
            'type': notification_type,
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'setor': setor
        }
        
        notifications_sent = 0
        users_notified = set()  # Para evitar duplicatas
        
        for user in all_users:
            user_email = user.get("email")
            user_setor = user.get("setor")
            user_type = user.get("tipo_usuario", "comum")
            
            # Determinar se deve enviar notificação
            should_notify = False
            reason = ""
            
            if user_type in ['admin', 'gestor']:
                # Admins e gestores sempre recebem
                should_notify = True
                reason = f"admin/gestor ({user_type})"
            elif user_setor == setor:
                # Usuários comuns apenas do mesmo setor
                should_notify = True
                reason = f"mesmo setor ({user_setor})"
            
            if should_notify and user_email and user_email in connected_users and user_email not in users_notified:
                sessions = connected_users[user_email]
                logger.info(f"[WEBSOCKET SMART] Enviando para {user_email} - {reason} - {len(sessions)} sessões")
                
                for sid in sessions:
                    try:
                        await sio.emit('notification', notification_data, to=sid)
                        notifications_sent += 1
                    except Exception as e:
                        logger.error(f"[WEBSOCKET ERROR] Erro ao enviar para {sid}: {e}")
                
                users_notified.add(user_email)
            elif user_email:
                logger.debug(f"[WEBSOCKET SMART] Pulando {user_email} - não conectado ou já notificado")
        
        logger.info(f"[WEBSOCKET SMART] Notificação enviada: {notifications_sent} notificações para {len(users_notified)} usuários únicos")
        
    except Exception as e:
        logger.error(f"[WEBSOCKET ERROR] Erro no envio inteligente: {e}")
        logger.exception("Detalhes do erro:") 