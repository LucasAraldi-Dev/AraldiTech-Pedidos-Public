#!/usr/bin/env python3
"""
Script de teste para verificar se o WebSocket está funcionando corretamente.
Execute este script para testar a funcionalidade de notificações.
"""

import asyncio
import socketio
import json
from datetime import datetime

# Configuração do cliente Socket.IO
sio = socketio.AsyncClient()

@sio.event
async def connect():
    print("✅ Conectado ao servidor WebSocket!")
    print(f"Session ID: {sio.sid}")

@sio.event
async def disconnect():
    print("❌ Desconectado do servidor WebSocket")

@sio.event
async def connection_established(data):
    print(f"🔗 Conexão estabelecida: {data}")

@sio.event
async def notification(data):
    print("🔔 Notificação recebida:")
    print(f"   Tipo: {data.get('type')}")
    print(f"   Título: {data.get('title')}")
    print(f"   Mensagem: {data.get('message')}")
    if 'pedido' in data:
        pedido = data['pedido']
        print(f"   Pedido ID: {pedido.get('id')}")
        print(f"   Descrição: {pedido.get('descricao')}")
        print(f"   Usuário: {pedido.get('usuario_nome')}")

async def test_websocket():
    try:
        print("🚀 Iniciando teste do WebSocket...")
        print("📡 Conectando ao servidor em http://localhost:8000...")
        
        # Conectar ao servidor
        await sio.connect('http://localhost:8000', auth={'token': 'test_token'})
        
        # Aguardar um pouco para receber mensagens
        print("⏳ Aguardando notificações por 30 segundos...")
        await asyncio.sleep(30)
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
    finally:
        # Desconectar
        await sio.disconnect()
        print("🔚 Teste finalizado")

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 TESTE DE WEBSOCKET - ARALDITECH PEDIDOS")
    print("=" * 50)
    print()
    print("Este script testa a conectividade WebSocket.")
    print("Certifique-se de que o servidor backend está rodando.")
    print()
    
    try:
        asyncio.run(test_websocket())
    except KeyboardInterrupt:
        print("\n⚠️  Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}") 