# Changelog
Todas as alterações notáveis deste projeto serão documentadas neste arquivo.

## [0.4.3] - 2024-11-17
### Adicionado
- **Hierarquia de Usuários**: Diferenciação entre usuários **Comuns** e **Gestores**, criando uma base para permissões específicas.
- **Painel de Controle do Usuário Comum**: Ajustes na interface e funcionalidades para melhorar a experiência do usuário.
- **Preparação para o Painel do Gestor**: Rotas no back-end ajustadas para futura implementação de funcionalidades específicas para gestores.

### Alterado
- **Layout Geral**: Reformulação visual em diversos componentes para maior consistência e modernização.
- **Responsividade**: Melhorias no comportamento da interface para dispositivos móveis (ainda em fase de teste).

---

## [0.4.2] - 2024-11-16
### Adicionado
- **Modal de Impressão**: Novo modal adicionado para imprimir pedidos diretamente da interface.
- **Fechamento de Modal**: Alteração na lógica para impedir que o modal seja fechado ao clicar fora da tela.
- **Design Unificado de Modais**: Todos os modais agora possuem um design consistente e melhor alinhado visualmente.

### Alterado
- **Layout Melhorado**: Pequenas melhorias de layout para proporcionar uma melhor experiência ao usuário, incluindo ajustes de espaçamento e exibição de elementos.
- **Erro no Salvamento de Pedidos**: Correção do erro onde os pedidos não estavam sendo salvos corretamente no banco de dados.
- **Feedback Imediato**: Melhorias no feedback fornecido após a criação de pedidos, agora com uma resposta mais dinâmica.

---

## [0.4.1] - 2024-11-14
### Adicionado
- **Mensagem de Sucesso**: Exibição do número do pedido e uma mensagem de confirmação após a criação de um pedido com sucesso.
- **Reset de Formulário**: O formulário é automaticamente limpo após 3 segundos de sucesso na criação do pedido.
- **Feedback Dinâmico**: Melhorias na experiência do usuário com a exibição de uma mensagem de sucesso e atualização da interface.

### Alterado
- Melhorias no comportamento do modal de criação de pedidos, agora exibindo um feedback imediato após a criação de um pedido.

---

## [0.4.0] - 2024-11-13
### Adicionado
- Implementação do frontend com Vue.js, trazendo uma interface interativa e responsiva.
- Botão de navegação para dispositivos móveis, com exibição dinâmica da sidebar.
- Controle de visibilidade dos menus para dispositivos móveis.
- Novo sistema de modais para criação e consulta de pedidos.
- Navegação aprimorada entre as seções de criação e consulta de pedidos.
- Melhorias na usabilidade e experiência do usuário.

### Alterado
- Layout da aplicação reformulado para melhor adaptação em dispositivos móveis.
- Navegação do frontend agora é controlada pelo Vue.js, proporcionando uma experiência de uso mais fluida e dinâmica.
- Otimizações no estilo do formulário, adicionando ícones e bordas mais sutis.

---

## [0.3.5] - 2024-10-31
### Adicionado
- Campo para upload de imagens no formulário de pedidos.
- Ícone padrão na área de upload de arquivos.
- Estilos atualizados para o botão de upload, com efeito de profundidade.

### Alterado
- Tamanho da imagem do logo ajustado para maior destaque.
- Melhorias na disposição do conteúdo para melhor legibilidade.
- Ajustes de cores no formulário para harmonizar com o novo layout.

---

## [0.3.4] - 2024-10-26
### Adicionado
- Logo no topo da página, aprimorando a identidade visual do formulário.

### Alterado
- Estilos do formulário atualizados para uma aparência mais moderna e limpa.
- Melhorias na posição do botão "CONSULTAR PEDIDOS" no formulário.

### Corrigido
- Autenticação: Removido middleware que restringia acesso às páginas `index.html` e `login_pedidos.html`.
- Redirecionamento de usuários não autenticados para a página inicial.
- Logs de atividades relacionadas à autenticação adicionados para monitoramento.

---

## [0.3.3] - 2024-10-10
### Adicionado
- Middleware de autenticação para restrição de acesso às páginas da aplicação.

### Corrigido
- Permissões ajustadas para acesso público às páginas `index.html` e `login_pedidos.html`.
- Redirecionamento de usuários não autenticados para `/static/index.html`.
- Logs adicionados para registrar tentativas de acesso e atividades de autenticação.

---

> **Nota**: Este changelog foi criado a partir da versão 0.3.3.
