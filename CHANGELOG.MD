# Changelog
Todas as alterações notáveis deste projeto serão documentadas neste arquivo.

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
- Autenticação: removido middleware que restringia acesso às páginas `index.html` e `login_pedidos.html`.
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
