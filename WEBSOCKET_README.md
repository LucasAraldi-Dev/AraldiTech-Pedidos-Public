# Sistema de Notificações WebSocket - AraldiTech Pedidos

## 📋 Visão Geral

O sistema de notificações em tempo real foi implementado usando WebSockets (Socket.IO) para permitir que administradores e gestores recebam notificações instantâneas quando novos pedidos são criados.

## 🚀 Funcionalidades

### ✅ Implementado
- ✅ Notificações em tempo real para admins e gestores
- ✅ Indicador visual de notificações no header
- ✅ Dropdown com lista de notificações
- ✅ Persistência de notificações no localStorage
- ✅ Conexão automática após login (apenas para admin/gestor)
- ✅ Reconexão automática em caso de falha
- ✅ Interface responsiva para mobile e desktop

### 🔔 Tipos de Notificação
- **Novo Pedido**: Quando um pedido é criado
- **Pedido Atualizado**: Quando um pedido é editado
- **Pedido Concluído**: Quando um pedido é marcado como concluído

## 🏗️ Arquitetura

### Backend
```
backend/app/
├── websocket.py          # Servidor Socket.IO e lógica de notificações
├── main.py              # Integração WebSocket com FastAPI
└── requirements.txt     # Dependências (python-socketio==5.7.0)
```

### Frontend
```
frontend/src/
├── utils/websocket.js           # Cliente Socket.IO
├── components/NotificationIndicator.vue  # Componente de notificações
├── views/AppMenu.vue           # Interface principal com header
└── main.js                     # Configuração global
```

## 🔧 Configuração

### 1. Backend
O WebSocket está montado em `/socket.io` no servidor FastAPI:
```python
# backend/app/main.py
app.mount("/socket.io", websocket.socket_app)
```

### 2. Frontend
O cliente conecta automaticamente após login para usuários admin/gestor:
```javascript
// frontend/src/main.js
if (userType === 'admin' || userType === 'gestor') {
  websocketService.connect(access_token);
}
```

## 📱 Interface do Usuário

### Header com Notificações
- **Ícone de sino**: Indica notificações disponíveis
- **Badge vermelho**: Mostra número de notificações não lidas
- **Dropdown**: Lista completa de notificações com ações

### Funcionalidades do Dropdown
- ✅ Marcar como lida (individual)
- ✅ Marcar todas como lidas
- ✅ Remover notificação
- ✅ Limpar todas
- ✅ Navegar para pedido (clique na notificação)

## 🔐 Permissões

### Quem Recebe Notificações
- ✅ **Administradores** (`tipo_usuario: "admin"`)
- ✅ **Gestores** (`tipo_usuario: "gestor"`)
- ❌ **Usuários comuns** (`tipo_usuario: "comum"`)

### Autenticação WebSocket
- Token JWT é enviado na conexão
- Verificação de permissões no servidor
- Conexões anônimas permitidas para desenvolvimento

## 🧪 Teste

### Script de Teste
Execute o script de teste para verificar a conectividade:
```bash
python test_websocket.py
```

### Teste Manual
1. Faça login como admin ou gestor
2. Abra outra aba/janela
3. Crie um novo pedido
4. Verifique se a notificação aparece na primeira aba

## 📊 Monitoramento

### Endpoint de Status
```
GET /websocket/connected-users
```
Retorna informações sobre usuários conectados (apenas para admin/gestor).

### Logs
O sistema registra logs detalhados:
- Conexões/desconexões
- Notificações enviadas
- Erros de conexão

## 🔄 Fluxo de Notificação

1. **Criação de Pedido**
   ```
   Usuario cria pedido → Backend salva → WebSocket notifica admins/gestores
   ```

2. **Recebimento da Notificação**
   ```
   WebSocket recebe → Toast aparece → Notificação salva → Badge atualizado
   ```

3. **Interação do Usuário**
   ```
   Clique na notificação → Marca como lida → Navega para pedido (opcional)
   ```

## 🛠️ Configurações Avançadas

### Timeouts e Reconexão
```javascript
// frontend/src/utils/websocket.js
const options = {
  timeout: 20000,           // 20 segundos
  maxReconnectAttempts: 5,  // 5 tentativas
  reconnectDelay: 2000      // 2 segundos (progressivo)
};
```

### Limite de Notificações
- Máximo de 50 notificações armazenadas
- Notificações antigas são removidas automaticamente

## 🐛 Troubleshooting

### Problemas Comuns

1. **Notificações não aparecem**
   - Verificar se o usuário é admin/gestor
   - Verificar conexão WebSocket no console
   - Verificar se o backend está rodando

2. **Erro de conexão**
   - Verificar URL do servidor
   - Verificar CORS no backend
   - Verificar firewall/proxy

3. **Notificações duplicadas**
   - Verificar se há múltiplas conexões
   - Limpar localStorage se necessário

### Debug
```javascript
// Console do navegador
console.log(websocketService.getConnectionStatus());
```

## 📈 Próximas Melhorias

### Planejadas
- [ ] Notificações push do navegador
- [ ] Som personalizado para notificações
- [ ] Filtros de notificação por tipo
- [ ] Histórico de notificações no servidor
- [ ] Notificações por email (opcional)

### Possíveis Expansões
- [ ] Chat em tempo real
- [ ] Status de usuários online
- [ ] Colaboração em tempo real em pedidos
- [ ] Notificações para mudanças de status

## 📞 Suporte

Para problemas ou dúvidas sobre o sistema de notificações:
1. Verificar logs do servidor
2. Executar script de teste
3. Verificar configurações de rede
4. Consultar documentação do Socket.IO

---

**Versão**: 1.0.0  
**Última atualização**: Janeiro 2025  
**Compatibilidade**: Vue 3, FastAPI, Socket.IO 4.x/5.x 