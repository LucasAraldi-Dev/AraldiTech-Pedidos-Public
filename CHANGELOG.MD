# Changelog
Todas as alterações notáveis deste projeto serão documentadas neste arquivo.

## [0.8.2] - 2025-05-15
### Alterado
- Terminologia mais clara: campo "Data de Entrega" renomeado para "Data do Pedido" em toda a aplicação para maior consistência.
- Controle de acesso aprimorado: agora apenas administradores podem alterar a data do pedido, enquanto usuários comuns visualizam o campo desabilitado.
- Mensagens informativas adicionadas para indicar as permissões relacionadas à data do pedido.
- Fluxo de login otimizado: eliminada a tela de carregamento do sistema após o login, redirecionando o usuário diretamente para o menu principal, tornando a navegação mais rápida e direta.
- **Tratamento de erros aprimorado**: mensagens de erro mais específicas e contextuais no processo de cadastro de usuários, com identificação precisa de erros como e-mail ou nome de usuário já existentes.

### Adicionado
- Design modernizado para página inicial (AppHome) seguindo o padrão visual do sistema.
- Reformulação da página de contato (AppContato) com novos campos e layout responsivo.
- Nova central de ajuda (AppAjuda) com perguntas frequentes interativas.
- Política de Privacidade e Termos de Uso acessíveis pelo rodapé da aplicação.
- Modais interativos para exibição das políticas legais sem redirecionamento.
- **Sistema de Aceitação de Termos**: Implementado modal de aceitação obrigatória dos Termos de Serviço durante o cadastro, com registro de data, hora e metadados do aceite.
- **Controle de Conformidade Legal**: Armazenamento e controle das informações de aceite de termos para fins legais e de auditoria.

## [0.8.1] - 2025-05-10
### Corrigido
- Correção no modal de cadastro de usuário que permitia cadastro mesmo sem conexão com o banco de dados, agora mostrando o erro corretamente.
- Correção no campo de data na edição de pedidos, que agora permanece com a data original e só pode ser editado por administradores.
- Adicionado campo de setor do responsável no modal de criação de pedido, sendo preenchido automaticamente com o setor do usuário logado e podendo ser editado apenas por administradores ou gestores.

## [0.8.0] - 2025-05-06
### Adicionado
- Relatório financeiro , baseado nos dados fornecidos pelos usuários ao concluirem os pedidos.

### Melhorado
- Fluxo de login refeito e melhorado para o usuário.
- Fluxo de cadastro refeito também para melhor usabilidade do usuário.
- Dashboard refeito para melhor visualização das informações relacionadas ao sistema.
### Corrigido
- Responsividade ajustada para melhor adaptação em variados tipos de tela.
- Correção de segurança na área do login e cadastro.
- Correção de segurança no log dos pedidos editados.
- Correção dos modais de dashboard.
- Pedidos concluidos no banco estavam sendo salvos em formatos diferentes,
dificultando a visualização pelo dashboard.

## [0.7.0] - 2025-05-05
### Adicionado
- Expansão dos setores disponíveis: Escritório, Fábrica de Ração, CPO, Granjas, Abatedouro, Transporte, Incubatório e Favorito.
- Implementação de segurança por setor: usuários visualizam apenas pedidos do seu próprio setor.
- Acesso exclusivo para administradores a todos os setores da plataforma.
- Menu de Dashboard para gestores com visualização de métricas.
- Gráficos de acompanhamento de pedidos e atividades.
- Sistema de logs e registro de atividades detalhado para cada pedido.
- Histórico completo de alterações por pedido com registro do usuário responsável.

### Melhorado
- Segurança aprimorada no controle de acesso a pedidos por setor.
- Interface do dashboard para visualização de dados e métricas.
- Experiência do usuário com feedback visual para ações realizadas.

### Corrigido
- Problemas de visualização entre setores diferentes.
- Permissões de acesso a pedidos fora do setor do usuário.
- Otimização da consulta de pedidos por setor.

## [0.6.0] - 2025-05-03
### Adicionado  
- Implementado o novo modal de criação , consulta e edição de pedidos
- Inclusão de um histórico de pedidos editados.
- Criado um menu de gerencimento de usuários para admins.
- Inclusão de novos toasts variados sobre tokens , pedidos.


### Corrigido
- Correção de segurança e pedidos que podiam ser editados sem ter feito login , ou com token JWT expirado.
- Correção de segurança na geração do token JWT 
- Correção na responsividade em alguns tipos de telas.

## [0.5.0] - 2025-04-15
### Adicionado  
- Implementado o novo botão de CONCLUIR pedido no modal de consulta de pedidos.
- Novo modal para a visualização do alerta , tipo , "Você deseja realmente marcar esse pedido como CONCLUÍDO?"

### Corrigido
- Correção no botão de CONCLUIR pedido no modal de consulta de pedidos.
- Correção na validação do campo "Observação" no modal de criação de pedidos.
- Correção da responsividade das páginas no geral.


## [0.4.4] - 2024-12-01  
### Adicionado  
- **Sincronização em Tempo Real entre Modais**: Melhorias para garantir que alterações nos modais de edição sejam refletidas imediatamente nos modais de consulta.  
- **Feedback Visual nos Botões**: Destaque visual adicionado aos botões ao interagir com os modais, proporcionando uma experiência mais clara ao usuário.  
- **Validação de Dados no Frontend**: Adição de validações mais robustas diretamente no frontend, reduzindo erros e inconsistências antes de enviar dados para o backend.  

### Corrigido  
- **Comportamento Responsivo de Modais**: Correção de problemas de layout que afetavam a exibição e o funcionamento dos modais em dispositivos móveis.  
- **Erros ao Atualizar Dados**: Ajuste na lógica de atualização para corrigir inconsistências ao editar ou criar novos pedidos.  

### Alterado  
- **Otimização de Código no Frontend**: Reestruturação para melhorar o desempenho e a legibilidade do código.  
- **Performance de Carregamento**: Componentes dinâmicos agora são carregados de forma assíncrona, melhorando a performance geral da aplicação.  
- **Design do Modal**: Refinamento visual dos modais para maior consistência com o restante da interface.  

---  

## [0.4.3] - 2024-11-17  
### Adicionado  
- **Hierarquia de Usuários**: Diferenciação entre usuários **Comuns** e **Gestores**, criando uma base para permissões específicas.  
- **Painel de Controle do Usuário Comum**: Ajustes na interface e funcionalidades para melhorar a experiência do usuário.  
- **Preparação para o Painel do Gestor**: Rotas no backend ajustadas para futura implementação de funcionalidades específicas para gestores.  

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
- **Frontend com Vue.js**: Interface interativa e responsiva implementada com Vue.js.  
- **Botão de Navegação para Dispositivos Móveis**: Exibição dinâmica da sidebar em telas menores.  
- **Sistema de Modais**: Implementação de modais para criação e consulta de pedidos.  
- **Navegação Aprimorada**: Melhorias para facilitar o uso entre as seções da aplicação.  

### Alterado  
- **Layout Reformulado**: Melhor adaptação da interface para dispositivos móveis.  
- **Navegação mais Fluida**: Controle aprimorado com Vue.js para uma experiência de uso mais intuitiva.  

---  

## [0.3.5] - 2024-10-31  
### Adicionado  
- **Upload de Imagens**: Campo para upload de imagens no formulário de pedidos.  
- **Ícone Padrão para Upload**: Design adicionado para facilitar a interação do usuário.  
- **Estilo Moderno**: Atualizações visuais nos botões e área de upload.  

### Alterado  
- **Tamanho do Logo**: Ajustado para maior destaque visual.  
- **Disposição do Conteúdo**: Melhorias para legibilidade.  
- **Harmonia de Cores**: Ajustes no formulário para harmonizar com o novo layout.  

---  

## [0.3.4] - 2024-10-26  
### Adicionado  
- **Logo no Topo da Página**: Reforço da identidade visual do formulário.  

### Alterado  
- **Estilo Modernizado**: Reformulação dos estilos do formulário.  
- **Posição do Botão de Consultar Pedidos**: Ajustes para maior acessibilidade.  

### Corrigido  
- **Autenticação**: Correção no middleware que restringia páginas específicas.  
- **Redirecionamento de Usuários Não Autenticados**: Ajustado para a página inicial.  
- **Logs de Atividades**: Adição para monitoramento.  

---  

## [0.3.3] - 2024-10-10  
### Adicionado  
- **Middleware de Autenticação**: Controle de acesso às páginas.  

### Corrigido  
- **Permissões Ajustadas**: Páginas públicas e logs de tentativas de acesso corrigidos.  

---  

> **Nota**: Este changelog foi criado a partir da versão 0.3.3.  
