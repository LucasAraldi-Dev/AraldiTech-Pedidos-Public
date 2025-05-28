#!/usr/bin/env python3
"""
Script simples para testar a conexão WebSocket
"""

import asyncio
import socketio
import requests
import json

# Configurações
BACKEND_URL = "http://localhost:8000"
WEBSOCKET_URL = "http://localhost:8000/socket.io"

async def test_websocket():
    print("🔧 Testando conexão WebSocket...")
    
    # Primeiro, fazer login para obter o token
    print("1. Fazendo login...")
    login_data = {
        "username": "admin",  # Ajuste conforme necessário
        "password": "admin123"  # Ajuste conforme necessário
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/token", json=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print(f"✅ Login realizado com sucesso")
        else:
            print(f"❌ Erro no login: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Erro ao fazer login: {e}")
        return
    
    # Criar cliente Socket.IO
    print("2. Conectando ao WebSocket...")
    sio = socketio.AsyncClient()
    
    @sio.event
    async def connect():
        print("✅ Conectado ao WebSocket!")
        
    @sio.event
    async def disconnect():
        print("🔌 Desconectado do WebSocket")
        
    @sio.event
    async def connection_established(data):
        print(f"🔗 Conexão estabelecida: {data}")
        
    @sio.event
    async def notification(data):
        print("🔔 Notificação recebida:")
        print(f"   Tipo: {data.get('type')}")
        print(f"   Dados: {data.get('data')}")
        
    try:
        # Conectar com autenticação
        await sio.connect(WEBSOCKET_URL, auth={'token': token})
        
        # Aguardar um pouco para a conexão se estabelecer
        await asyncio.sleep(2)
        
        # Testar notificação
        print("3. Testando notificação...")
        headers = {"Authorization": f"Bearer {token}"}
        test_response = requests.post(f"{BACKEND_URL}/test/websocket-notification", headers=headers)
        
        if test_response.status_code == 200:
            print("✅ Notificação de teste enviada")
        else:
            print(f"❌ Erro ao enviar notificação de teste: {test_response.status_code}")
            
        # Aguardar notificação
        await asyncio.sleep(3)
        
        # Verificar status
        print("4. Verificando status do WebSocket...")
        status_response = requests.get(f"{BACKEND_URL}/websocket/status", headers=headers)
        
        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f"📊 Status do WebSocket:")
            print(f"   Usuários conectados: {status_data['connected_users_count']}")
            print(f"   Sessões ativas: {status_data['active_sessions']}")
            print(f"   Usuários: {status_data['connected_users']}")
        else:
            print(f"❌ Erro ao obter status: {status_response.status_code}")
            
        await sio.disconnect()
        
    except Exception as e:
        print(f"❌ Erro na conexão WebSocket: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket()) 