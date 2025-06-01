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
    Envia uma mensagem apenas para usuários administradores e gestores.
    
    Args:
        event: Nome do evento a ser emitido
        data: Dados a serem enviados
    """
    try:
        logger.info(f"[WEBSOCKET ADMIN] Iniciando broadcast para admins/gestores - evento: {event}")
        
        # Buscar admins e gestores no banco de dados
        db = await database.get_db()
        admins_gestores = await db["users"].find({
            "tipo_usuario": {"$in": ["admin", "gestor"]}
        }).to_list(None)
        
        logger.info(f"[WEBSOCKET ADMIN] Encontrados {len(admins_gestores)} admins/gestores")
        
        admin_sessions = []
        admins_notified = []
        
        for user in admins_gestores:
            user_email = user.get("email")
            user_name = user.get("nome", "Sem nome")
            user_type = user.get("tipo_usuario")
            
            if user_email and user_email in connected_users:
                sessions = connected_users[user_email]
                admin_sessions.extend(sessions)
                admins_notified.append(f"{user_name}({user_email}) - {user_type}")
                logger.info(f"[WEBSOCKET ADMIN] ✓ {user_name}({user_email}) - {user_type} - {len(sessions)} sessões")
        
        notifications_sent = 0
        for sid in admin_sessions:
            try:
                await sio.emit(event, data, to=sid)
                logger.info(f"[WEBSOCKET ADMIN] ✓ Broadcast enviado para SID: {sid}")
                notifications_sent += 1
            except Exception as e:
                logger.error(f"[WEBSOCKET ERROR] Erro ao enviar broadcast para {sid}: {e}")
        
        logger.info(f"[WEBSOCKET ADMIN] ✓ RESUMO: {notifications_sent} broadcasts enviados para {len(admins_notified)} admins/gestores")
        logger.info(f"[WEBSOCKET ADMIN] ✓ Admins notificados: {admins_notified}")
        
    except Exception as e:
        logger.error(f"[WEBSOCKET ERROR] Erro ao enviar broadcast para admins: {e}")
        logger.exception("Detalhes do erro:")

async def send_notification_to_sector(setor: str, notification_type: str, data: dict):
    """
    Envia notificação para todos os usuários de um setor específico.
    APENAS usuários do setor especificado recebem a notificação.
    
    Args:
        setor: Nome do setor
        notification_type: Tipo da notificação
        data: Dados da notificação
    """
    try:
        logger.info(f"[WEBSOCKET SECTOR] Iniciando envio para setor específico '{setor}' - tipo: {notification_type}")
        
        # Buscar usuários do setor no banco de dados
        db = await database.get_db()
        users_in_sector = await db["users"].find({"setor": setor}).to_list(None)
        
        logger.info(f"[WEBSOCKET SECTOR] Encontrados {len(users_in_sector)} usuários no setor '{setor}'")
        logger.info(f"[WEBSOCKET SECTOR] Usuários conectados atualmente: {list(connected_users.keys())}")
        
        notification_data = {
            'type': notification_type,
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'setor': setor
        }
        
        # Enviar para cada usuário do setor que estiver conectado
        notifications_sent = 0
        users_notified = []
        users_not_connected = []
        
        for user in users_in_sector:
            user_email = user.get("email")
            user_name = user.get("nome", "Sem nome")
            user_type = user.get("tipo_usuario", "comum")
            
            logger.info(f"[WEBSOCKET SECTOR] Verificando usuário {user_name}({user_email}) - {user_type}")
            
            if user_email and user_email in connected_users:
                sessions = connected_users[user_email]
                logger.info(f"[WEBSOCKET SECTOR] ✓ Usuário {user_name}({user_email}) está conectado com {len(sessions)} sessões")
                
                for sid in sessions:
                    try:
                        await sio.emit('notification', notification_data, to=sid)
                        logger.info(f"[WEBSOCKET SECTOR] ✓ Notificação enviada para {user_name}({user_email}) do setor '{setor}' (SID: {sid})")
                        notifications_sent += 1
                    except Exception as e:
                        logger.error(f"[WEBSOCKET ERROR] Erro ao enviar notificação para {sid}: {e}")
                
                users_notified.append(f"{user_name}({user_email})")
            else:
                logger.info(f"[WEBSOCKET SECTOR] ⚠ Usuário {user_name}({user_email}) não está conectado")
                users_not_connected.append(f"{user_name}({user_email})")
        
        # Log resumo
        logger.info(f"[WEBSOCKET SECTOR] ✓ RESUMO para setor '{setor}': {notifications_sent} notificações enviadas")
        logger.info(f"[WEBSOCKET SECTOR] ✓ Usuários notificados ({len(users_notified)}): {users_notified}")
        
        if users_not_connected:
            logger.info(f"[WEBSOCKET SECTOR] ⚠ Usuários não conectados ({len(users_not_connected)}): {users_not_connected}")
        
    except Exception as e:
        logger.error(f"[WEBSOCKET ERROR] Erro ao enviar notificação para o setor '{setor}': {e}")
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

async def send_smart_notification(setor: str, notification_type: str, data: dict, creator_email: str = None):
    """
    Envia notificação de forma inteligente, evitando duplicatas.
    
    REGRAS CORRETAS:
    - Usuários comuns: recebem APENAS se forem do MESMO setor do pedido
    - Admins/Gestores: recebem independente do setor, mas apenas UMA vez
    - O usuário criador do pedido NÃO recebe sua própria notificação
    
    Args:
        setor: Nome do setor do pedido
        notification_type: Tipo da notificação
        data: Dados da notificação
        creator_email: Email do usuário que criou o pedido (não receberá notificação)
    """
    try:
        logger.info(f"[WEBSOCKET SMART] Enviando notificação para setor '{setor}' - tipo: {notification_type}")
        if creator_email:
            logger.info(f"[WEBSOCKET SMART] Usuário criador '{creator_email}' será excluído das notificações")
        
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
        users_filtered_out = []  # Para log de usuários filtrados
        
        for user in all_users:
            user_email = user.get("email")
            user_setor = user.get("setor")
            user_type = user.get("tipo_usuario", "comum")
            user_name = user.get("nome", "Sem nome")
            
            # FILTRO 1: Evitar que o usuário criador receba sua própria notificação
            if creator_email and user_email == creator_email:
                users_filtered_out.append(f"{user_name}({user_email}) - criador do pedido")
                logger.info(f"[WEBSOCKET SMART] ❌ Usuário criador {user_name}({user_email}) não receberá sua própria notificação")
                continue
            
            # Determinar se deve enviar notificação
            should_notify = False
            
            if user_type in ['admin', 'gestor']:
                # Admins e gestores sempre recebem (independente do setor)
                should_notify = True
            elif user_type == "comum":
                # Usuários comuns APENAS do mesmo setor - comparação EXATA
                if user_setor and setor:
                    # Normalizar strings para comparação
                    user_setor_clean = str(user_setor).strip().replace('\u00a0', ' ')  # Remove non-breaking spaces
                    setor_clean = str(setor).strip().replace('\u00a0', ' ')
                    
                    if user_setor_clean == setor_clean:
                        should_notify = True
                    else:
                        should_notify = False
                        users_filtered_out.append(f"{user_name}({user_email}) - setor diferente ({user_setor} != {setor})")
                        # Log apenas para casos suspeitos - verificar se há diferenças sutis
                        if user_setor_clean.lower() == setor_clean.lower():
                            logger.warning(f"[WEBSOCKET SMART] ATENÇÃO: Diferença de case detectada - usuário: '{user_setor}' vs pedido: '{setor}'")
                        elif len(user_setor_clean) != len(setor_clean):
                            logger.warning(f"[WEBSOCKET SMART] ATENÇÃO: Diferença de tamanho detectada - usuário: '{user_setor}' ({len(user_setor_clean)}) vs pedido: '{setor}' ({len(setor_clean)})")
                        else:
                            logger.info(f"[WEBSOCKET SMART] Usuário {user_name}({user_email}) do setor '{user_setor}' NÃO receberá notificação do setor '{setor}'")
                else:
                    should_notify = False
                    users_filtered_out.append(f"{user_name}({user_email}) - setor não definido")
            
            if should_notify and user_email and user_email in connected_users and user_email not in users_notified:
                sessions = connected_users[user_email]
                
                for sid in sessions:
                    try:
                        await sio.emit('notification', notification_data, to=sid)
                        notifications_sent += 1
                    except Exception as e:
                        logger.error(f"[WEBSOCKET ERROR] Erro ao enviar para {sid}: {e}")
                
                users_notified.add(user_email)
                logger.info(f"[WEBSOCKET SMART] ✓ Notificação enviada para {user_name}({user_email}) - {user_type} - setor: '{user_setor}'")
        
        logger.info(f"[WEBSOCKET SMART] ✓ RESUMO: {notifications_sent} notificações enviadas para {len(users_notified)} usuários únicos")
        
        if users_filtered_out:
            logger.info(f"[WEBSOCKET SMART] ❌ Usuários filtrados ({len(users_filtered_out)}): {users_filtered_out[:5]}{'...' if len(users_filtered_out) > 5 else ''}")
        
    except Exception as e:
        logger.error(f"[WEBSOCKET ERROR] Erro no envio inteligente: {e}")
        logger.exception("Detalhes do erro:")

async def send_login_notification(user_data: dict):
    """
    Envia notificações de login conforme as regras corretas:
    - Quando usuário comum faz login: apenas gestores e admins são notificados
    - Quando gestor/admin faz login: apenas usuários comuns são notificados
    
    Args:
        user_data: Dados do usuário que fez login
    """
    try:
        user_type = user_data.get("tipo_usuario", "comum")
        user_name = user_data.get("nome", "Usuário")
        user_setor = user_data.get("setor", "Escritório")
        
        logger.info(f"[WEBSOCKET LOGIN] Processando notificação de login para {user_name} ({user_type})")
        
        # Buscar todos os usuários
        db = await database.get_db()
        all_users = await db["users"].find({}).to_list(None)
        
        notification_data = {
            'type': 'user_login',
            'data': {
                'title': 'Usuário Conectado',
                'message': f'{user_name} ({user_setor}) fez login no sistema',
                'user': {
                    'nome': user_name,
                    'setor': user_setor,
                    'tipo_usuario': user_type
                }
            },
            'timestamp': datetime.now().isoformat()
        }
        
        notifications_sent = 0
        users_notified = set()
        
        # Filtrar usuários que devem ser notificados
        for user_email, user_data in connected_users.items():
            if user_email not in users_to_notify:
                continue
            
            target_user_type = user_data.get("tipo_usuario", "comum")
            
            # Determinar se deve enviar notificação baseado nas regras CORRETAS
            should_notify = False
            reason = ""
            
            # Evitar notificar o próprio usuário que fez login
            if user_email == user_name:
                continue
            
            # REGRA CORRETA: Usuários comuns só devem receber notificações de login de admins/gestores
            if user_type in ['gestor', 'admin']:
                # Gestor/admin fez login -> notificar APENAS usuários comuns
                if target_user_type == "comum":
                    should_notify = True
                    reason = f"{user_type} logou, notificando usuário comum"
            # Se usuário comum fez login, NÃO notificar outros usuários comuns
            # Apenas admins/gestores devem ser notificados (mas isso não é o requisito)
            
            if should_notify and user_email and user_email in connected_users and user_email not in users_notified:
                sessions = connected_users[user_email]
                logger.info(f"[WEBSOCKET LOGIN] Enviando para {user_email} - {reason} - {len(sessions)} sessões")
                
                for sid in sessions:
                    try:
                        await sio.emit('notification', notification_data, to=sid)
                        notifications_sent += 1
                    except Exception as e:
                        logger.error(f"[WEBSOCKET ERROR] Erro ao enviar notificação de login para {sid}: {e}")
                
                users_notified.add(user_email)
        
        logger.info(f"[WEBSOCKET LOGIN] Notificação de login enviada: {notifications_sent} notificações para {len(users_notified)} usuários únicos")
        
    except Exception as e:
        logger.error(f"[WEBSOCKET ERROR] Erro ao enviar notificação de login: {e}")
        logger.exception("Detalhes do erro:") 