# 🔧 Guia de Debug - Notificações WebSocket

## Problema Relatado
Você criou um pedido mas não viu nenhuma notificação aparecer.

## Passos para Debug

### 1. Verificar se o Backend está Rodando
- Certifique-se de que o backend FastAPI está rodando na porta 8000
- Acesse: http://localhost:8000/docs para ver se a API está ativa

### 2. Verificar Logs do Backend
Quando você criar um pedido, procure por estas mensagens nos logs do backend:

```
[WEBSOCKET DEBUG] Preparando notificação para pedido #XXX
[WEBSOCKET DEBUG] Setor do pedido: SETOR_NOME
[WEBSOCKET DEBUG] Enviando para usuários do setor SETOR_NOME
[WEBSOCKET DEBUG] Encontrados X usuários no setor SETOR_NOME
[WEBSOCKET DEBUG] Usuários conectados atualmente: [lista_de_emails]
```

### 3. Verificar Conexão WebSocket no Frontend
Abra o Console do Navegador (F12) e procure por:

```
Tentando conectar ao WebSocket...
✅ WebSocket conectado com sucesso!
```

### 4. Testar Notificação Manual
No frontend, clique no botão de teste WebSocket (ícone de sino cortado) no header.
Isso deve mostrar um toast de teste.

### 5. Verificar Status do WebSocket
Acesse como admin/gestor: http://localhost:8000/websocket/status
Isso mostra quantos usuários estão conectados.

### 6. Executar Script de Teste
Execute o script de teste:
```bash
python test_websocket_simple.py
```

## Possíveis Problemas e Soluções

### Problema 1: WebSocket não conecta
**Sintomas**: Não há logs de conexão WebSocket
**Solução**: 
- Verificar se o Socket.IO está montado corretamente no FastAPI
- Verificar CORS
- Verificar se a porta 8000 está acessível

### Problema 2: Usuário não está conectado
**Sintomas**: Logs mostram "Usuário X não está conectado"
**Solução**:
- Verificar se o token JWT está sendo enviado corretamente
- Verificar se o usuário existe no banco de dados
- Verificar se o email do usuário está correto

### Problema 3: Notificação enviada mas não aparece
**Sintomas**: Logs mostram notificação enviada, mas toast não aparece
**Solução**:
- Verificar console do navegador por erros JavaScript
- Verificar se o filtro de notificações está funcionando
- Verificar se o toast está sendo chamado corretamente

### Problema 4: Filtro de setor bloqueando notificações
**Sintomas**: Notificação enviada mas filtrada no frontend
**Solução**:
- Verificar se o setor do usuário está correto
- Verificar se o setor do pedido está correto
- Verificar lógica de filtro no `handleNotification`

## Logs Importantes para Verificar

### Backend (FastAPI)
```
[WEBSOCKET DEBUG] Usuário autenticado: email@exemplo.com (SID: xxx)
[WEBSOCKET DEBUG] Total de usuários conectados: X
[WEBSOCKET DEBUG] Preparando notificação para pedido #XXX
[WEBSOCKET DEBUG] Notificação enviada para usuário email@exemplo.com
```

### Frontend (Console do Navegador)
```
Tentando conectar ao WebSocket...
✅ WebSocket conectado com sucesso!
Notificação recebida: {dados}
```

## Comandos Úteis

### Verificar processos Python rodando
```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep python
```

### Verificar se a porta 8000 está em uso
```bash
# Windows
netstat -an | findstr :8000

# Linux/Mac
lsof -i :8000
```

## Próximos Passos

1. Execute os passos de debug na ordem
2. Anote quais logs aparecem e quais não aparecem
3. Teste com diferentes tipos de usuário (admin, gestor, comum)
4. Teste em diferentes setores
5. Relate os resultados para análise mais detalhada 