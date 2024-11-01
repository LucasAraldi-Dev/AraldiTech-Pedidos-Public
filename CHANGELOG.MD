# Changelog

Todas as alterações notáveis deste projeto serão documentadas neste arquivo.

## [0.3.5] - 2024-10-31

### Adicionado:
- **Layout**
- Criado um campo para upload de imagens no formulário de PEDIDOS.
- **Aprimoramento do Upload de Arquivos**:
  - Ícone padrão adicionado à área de upload, aumentando a clareza da funcionalidade.
  - Alterações no estilo do botão de upload para criar um efeito de profundidade, simulando um botão "afundando" ao ser clicado.

### Alterado:
- **Melhorias na Experiência do Usuário**:
  - Aumentado o tamanho da imagem do logo para maior destaque.
  - Ajuste na disposição do conteúdo no formulário para melhorar a legibilidade e usabilidade.
  - Alterado algumas cores dá página do formulário.

---

## [0.3.4] - 2024-10-26

### Adicionado:
- **Atualização no Estilo do Formulário**:
  - Adicionada uma logo no topo da página, aprimorando a identidade visual.

### Alterado:
- Ajustes nos estilos do formulário para uma aparência mais moderna e limpa.
- Botão "CONSULTAR PEDIDOS" estilizado e posicionado melhor no formulário.

### Corrigido:
- Removido o middleware de autenticação que restringe o acesso às páginas do aplicativo.
- Permissão de acesso livre às páginas `index.html` e `login_pedidos.html` dentro do diretório `/static`.
- Usuários não autenticados que tentarem acessar outras páginas serão redirecionados para a página inicial (`/static/index.html`).
- Logs foram adicionados para registrar tentativas de acesso e outras atividades relacionadas à autenticação.

---

## [0.3.3] - 2024-10-10

### Adicionado:
- **Implementação de Autenticação de Segurança**:
  - Middleware de autenticação que restringe o acesso às páginas do aplicativo.

### Corrigido:
- Permissão de acesso livre às páginas `index.html` e `login_pedidos.html` dentro do diretório `/static`.
- Usuários não autenticados que tentarem acessar outras páginas serão redirecionados para a página inicial (`/static/index.html`).
- Logs foram adicionados para registrar tentativas de acesso e outras atividades relacionadas à autenticação.

---

**Nota:** Este changelog foi criado a partir da versão 0.3.3