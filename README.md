# AraldiTech - Pedidos (Versão 0.9.0) 
![GitHub version](https://img.shields.io/badge/version-0.9.0--dev-orange)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

<!-- Menu de Navegação -->
<div align="center">
  <h3>📋 Navegação</h3>
  <p>
    <a href="#readme">📖 README</a> • 
    <a href="#changelog">📝 CHANGELOG</a> • 
    <a href="#documentacao-final">📚 Documentação Final</a>
  </p>
</div>

---

<div id="readme">

## 📖 README

### 🚨 Aviso Importante sobre Versões Futuras
> **⚠️ ATENÇÃO:** A partir da versão **1.0.0**, todas as novas versões do AraldiTech - Pedidos serão desenvolvidas em um **repositório privado**. Esta é a **última versão pública** do projeto. Para acesso às versões futuras, entre em contato com a equipe de desenvolvimento.

## 📋 Descrição
**AraldiTech - Pedidos** é um WebApp desenvolvido para gerenciar pedidos de produtos para setores específicos, com interface moderna, intuitiva e responsiva, proporcionando uma experiência de uso otimizada.

O projeto é construído com **FastAPI**, **MongoDB**, **Vue.js**, e conta com autenticação baseada em **JWT** para garantir a segurança de acesso.

### 🎯 Principais Funcionalidades:
- ✅ Criação e edição de novos pedidos
- 📊 Listagem e consulta de pedidos por setor
- 🔐 Controle de acesso por autenticação JWT
- 📈 Dashboard com gráficos e métricas para gestores
- 💻 Interface interativa e responsiva com Vue.js
- 📝 Histórico detalhado de atividades e alterações
- 👥 Hierarquia de usuários: **Comum**, **Gestor** e **Admin**
- 🏢 Segmentação por setores com permissões específicas
- 📊 Sistema de relatórios financeiros
- 🔍 Visualizador de logs do sistema
- 📱 Totalmente responsivo para dispositivos móveis

## 🛠️ Tecnologias Utilizadas
- **Python 3.10+**: Linguagem de programação principal para a API
- **FastAPI**: Framework para construção rápida de APIs RESTful
- **JavaScript / Vue.js**: Interface interativa e moderna no frontend
- **MongoDB**: Banco de dados NoSQL para armazenamento
- **Motor**: Driver assíncrono para integração com MongoDB
- **OAuth2 com JWT**: Autenticação segura usando JSON Web Tokens
- **Chart.js**: Biblioteca para criação de gráficos interativos
- **Jest**: Framework de testes unitários
- **Pydantic**: Validação de dados e serialização
- **Uvicorn**: Servidor ASGI para aplicações Python

## 📊 Versão Atual
A versão atual do projeto é **0.9.0** (Em Desenvolvimento).

### 🚧 Status da Versão 0.9.0
**EM DESENVOLVIMENTO ATIVO**

Esta versão está sendo desenvolvida com foco em:
- 🔧 Otimizações de performance
- 🛡️ Melhorias de segurança
- 🎨 Refinamentos na interface
- 📱 Aprimoramentos na responsividade
- 🔍 Sistema de auditoria avançado
- 📊 Novos relatórios e dashboards

## ⚡ Funcionalidades Principais

### 🔐 Sistema de Autenticação
- **JWT Security**: Autenticação segura com tokens JWT
- **Hierarquia de Usuários**:
  - **👤 Comum**: Acesso limitado ao seu setor
  - **👨‍💼 Gestor**: Dashboard com métricas e relatórios
  - **🔑 Admin**: Acesso total a todos os setores

### 📋 Gestão de Pedidos
- **CRUD Completo**: Criação, leitura, atualização e exclusão
- **🏢 Segmentação por Setor**: Organização por departamentos
- **📱 Interface Responsiva**: Suporte completo para mobile
- **📊 Dashboard Interativo**: Gráficos e métricas em tempo real
- **📝 Logs Detalhados**: Registro de todas as atividades

### 🏢 Setores Disponíveis
- Escritório
- Fábrica de Ração
- CPO (Centro de Produção de Ovos)
- Granjas
- Abatedouro
- Transporte
- Incubatório
- Favorito

## 🚀 Instalação e Configuração

### 📋 Pré-requisitos
- **Python 3.10+**
- **Node.js 16+** e **npm**
- **MongoDB** (local ou remoto)
- **Git**

### ⚙️ Configuração do Ambiente

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/LucasAraldi-Dev/AraldiTech-Pedidos.git
    cd AraldiTech-Pedidos
    ```

2. **Configure o Backend:**
    ```bash
    # Instale as dependências
    pip install -r requirements.txt
    
    # Configure as variáveis de ambiente
    cp .env.example .env
    # Edite o arquivo .env com suas configurações
    ```

3. **Configure o Frontend:**
    ```bash
    cd frontend
    npm install
    ```

4. **Configure o MongoDB:**
    - Instale e configure o MongoDB
    - Atualize a string de conexão no arquivo `.env`

### 🏃‍♂️ Executando a Aplicação

1. **Inicie o Backend:**
    ```bash
    uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

2. **Inicie o Frontend:**
    ```bash
    cd frontend
    npm run serve
    ```

3. **Execute os Testes:**
    ```bash
    cd frontend
    npm run test:unit
    ```

4. **Acesse a aplicação:**
    - Frontend: `http://localhost:8080`
    - Backend API: `http://localhost:8000`
    - Documentação da API: `http://localhost:8000/docs`

## 🤝 Contribuição
Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AlgoIncrivel`)
3. Commit suas mudanças (`git commit -m 'Adc algo incrivel'`)
4. Push para a branch (`git push origin feature/AlgoIncrivel`)
5. Abra um Pull Request

## 📞 Suporte e Contatos
- **Desenvolvedor**: Lucas Araldi
- **Email**: [lucasaraldi.dev@gmail.com](mailto:lucasaraldi.dev@gmail.com)
- **GitHub**: [@LucasAraldi-Dev](https://github.com/LucasAraldi-Dev)

## 📄 Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

</div>

<div id="changelog">

## 📝 CHANGELOG

Todas as alterações notáveis deste projeto são documentadas neste arquivo.

### 🚨 Aviso sobre Versões Futuras
> **A partir da versão 1.0.0, o desenvolvimento continuará em repositório privado. Esta é última versão pública do projeto.**

## [0.9.0] - Em Desenvolvimento 🚧
### 🎯 Foco da Versão
Esta versão marca a **transição para desenvolvimento privado** e inclui melhorias significativas em performance, segurança e experiência do usuário.

### 🔄 Em Desenvolvimento
- **🛡️ Sistema de Auditoria Avançado**: Rastreamento completo de todas as ações do sistema
- **⚡ Otimizações de Performance**: Melhorias significativas na velocidade de carregamento
- **🎨 Redesign da Interface**: Nova identidade visual mais moderna
- **📊 Dashboard Avançado**: Novos gráficos e métricas em tempo real
- **🔐 Segurança Aprimorada**: Implementação de novos protocolos de segurança
- **📱 Mobile**: Redesign completo para dispositivos móveis
- **🌐 API v2**: Nova versão da API com melhor documentação
- **🔍 Sistema de Busca Avançado**: Filtros e pesquisas mais inteligentes

### 📋 Planejado para esta Versão
- **🚀 Cache Inteligente**: Sistema de cache para melhor performance
- **📧 Notificações por Email**: Sistema de notificações automáticas
- **📊 Relatórios Personalizáveis**: Criação de relatórios customizados
- **🔄 Sincronização em Tempo Real**: WebSockets para atualizações instantâneas
- **🌍 Internacionalização**: Suporte para múltiplos idiomas
- **📦 Sistema de Backup Automático**: Backup automático dos dados

---

## [0.8.9] - 2025-05-25
### ✅ Adicionado
- **🔧 Preparação para v0.9.0**: Estrutura base para as próximas funcionalidades
- **📚 Documentação Aprimorada**: Melhorias na documentação do código
- **🧪 Testes Automatizados**: Expansão da cobertura de testes

### 🔧 Melhorado
- **⚡ Performance Geral**: Otimizações em consultas ao banco de dados
- **🎨 Interface do Usuário**: Pequenos ajustes visuais e de usabilidade
- **🔐 Segurança**: Fortalecimento das validações de entrada

### 🐛 Corrigido
- **📱 Responsividade**: Ajustes finais para dispositivos móveis
- **🔄 Sincronização**: Melhorias na sincronização entre frontend e backend

---

## [0.8.8] - 2025-05-23
### ✅ Adicionado
- **📊 Dashboard Reformulado**: Completamente refeito com menus organizados
- **📈 Sistema de Relatórios**: Backend específico para relatórios (em desenvolvimento)

### 🐛 Corrigido
- **📱 Responsividade**: Novos ajustes para melhor adaptação em diferentes telas

---

## [0.8.7] - 2025-05-21
### ✅ Adicionado
- **🎨 UI Interativa**: Novos componentes para melhor UX
- **🚪 Confirmação de Logout**: Modal de confirmação para evitar saídas acidentais
- **🍔 Menu Hamburger**: Implementado para versão mobile
- **⏳ Splash Screen**: Tela de carregamento para melhor experiência

### 🔧 Melhorado
- **🔑 AppLogin**: Refatoração das funcionalidades pós-login
- **📝 Modal de Cadastro**: Otimização de validações e feedback

### 🐛 Corrigido
- **📱 Responsividade**: Centralização em arquivo separado
- **👤 Cadastro de Usuário**: Correção de espaços em branco no nome
- **🔐 Verificação de Token**: Nova camada de segurança

---

## [0.8.6] - 2025-05-19
### 🔧 Melhorado
- **📱 Responsividade Geral**: Melhorias para telas pequenas e mobile
- **🔘 Botões e Menus**: Redesign para melhor consistência mobile

### 🐛 Corrigido
- **📋 Visualizador de Logs**: Correção nas informações do modal
- **🖨️ Modal de Impressão**: Adaptação para impressão correta

---

## [0.8.5] - 2025-05-18
### ✅ Adicionado
- **🛡️ Segurança Aprimorada**: Proteção CSRF e validações avançadas
- **⚡ Sistema de Cache**: Redução do tempo de resposta
- **📋 Visualizador de Logs**: Modal para administradores
- **🧪 Testes Unitários**: Framework Jest integrado
- **✅ Validação Centralizada**: Regras padronizadas
- **🎨 Componentes Reutilizáveis**: Indicadores e tooltips
- **⚠️ Tratamento de Erros**: Sistema centralizado

### 🔧 Melhorado
- **⚡ Performance**: Otimização de requisições HTTP
- **💬 Feedback ao Usuário**: Notificações mais claras
- **📱 Responsividade**: Ajustes em modais e cards
- **🔐 Segurança de Dados**: Validação rigorosa
- **📁 Organização**: Refatoração para modularidade
- **🎨 Consistência Visual**: Padronização de componentes

### 🐛 Corrigido
- **📝 Formulários**: Uniformização de validações
- **📱 Layout Mobile**: Correções específicas
- **📅 Formato de Datas**: Consistência entre formulários
- **🔄 Requisições**: Melhor gerenciamento simultâneo
- **🌐 Rede Instável**: Recuperação robusta de falhas
- **✅ Conclusão de Pedidos**: Formato de data e permissões

### ❌ Removido
- **📚 Tutorial Interativo**: Movido para documentação

---

## [0.8.4] - 2025-05-15
### ✅ Adicionado
- **🔍 Filtro por Setor**: Modal de consulta com filtros
- **🚨 Indicadores de Prioridade**: Destaque visual para urgência
- **📊 Ordenação Inteligente**: Por prioridade (Crítico > Urgente > Padrão)
- **🏢 Visualização de Setor**: Campo nos cards de pedido
- **🗺️ Roadmap**: Planejamento até versão 1.0

### 🔧 Melhorado
- **📱 Design Responsivo**: Layout otimizado para mobile
- **🎨 Experiência Visual**: Cards reformulados
- **🔍 Eficiência**: Consultas otimizadas por setor
- **🔐 Controle de Acesso**: Refinamento de permissões

---

## [0.8.3] - 2025-05-12
### ✅ Adicionado
- **📚 Tutorial Interativo**: Sistema passo a passo para novos usuários
- **❓ Botão de Ajuda**: Acesso rápido ao suporte

### 🔧 Melhorado
- **👋 Primeiro Uso**: Fluxo aprimorado para novos usuários
- **♿ Acessibilidade**: Interface de ajuda redesenhada
- **📖 Documentação**: FAQ atualizada na Central de Ajuda

---

## [0.8.2] - 2025-05-11
### 🔄 Alterado
- **📅 Terminologia**: "Data de Entrega" → "Data do Pedido"
- **🔐 Controle de Acesso**: Apenas admins alteram datas
- **💬 Mensagens**: Indicações de permissões
- **⚡ Fluxo de Login**: Eliminação da tela de carregamento
- **⚠️ Tratamento de Erros**: Mensagens específicas no cadastro

### ✅ Adicionado
- **🎨 Design Modernizado**: AppHome reformulada
- **📞 Página de Contato**: AppContato com novo layout
- **❓ Central de Ajuda**: AppAjuda com FAQ interativa
- **📋 Políticas**: Privacidade e Termos de Uso
- **✅ Sistema de Aceite**: Modal obrigatório de termos
- **📊 Conformidade Legal**: Controle de aceites

---

## [0.8.1] - 2025-05-10
### 🐛 Corrigido
- **👤 Cadastro**: Erro sem conexão com banco
- **📅 Edição de Datas**: Permissões de administrador
- **🏢 Campo de Setor**: Preenchimento automático

---

## [0.8.0] - 2025-05-06
### ✅ Adicionado
- **💰 Relatório Financeiro**: Baseado em dados de conclusão

### 🔧 Melhorado
- **🔑 Fluxo de Login**: Refeito e otimizado
- **📝 Fluxo de Cadastro**: Melhor usabilidade
- **📊 Dashboard**: Refeito para melhor visualização

### 🐛 Corrigido
- **📱 Responsividade**: Adaptação para variados tipos de tela
- **🔐 Segurança**: Login, cadastro e logs
- **📊 Modais**: Dashboard corrigido
- **💾 Formato de Dados**: Padronização de pedidos concluídos

---

## [0.7.0] - 2025-05-05
### ✅ Adicionado
- **🏢 Expansão de Setores**: 8 setores disponíveis
- **🔐 Segurança por Setor**: Visualização restrita
- **👑 Acesso Admin**: Todos os setores
- **📊 Dashboard para Gestores**: Métricas e gráficos
- **📋 Sistema de Logs**: Registro detalhado
- **📝 Histórico**: Alterações por pedido

### 🔧 Melhorado
- **🛡️ Segurança**: Controle de acesso aprimorado
- **📊 Interface**: Dashboard para dados e métricas
- **👤 UX**: Feedback visual para ações

### 🐛 Corrigido
- **👁️ Visualização**: Problemas entre setores
- **🔐 Permissões**: Acesso fora do setor
- **⚡ Performance**: Consultas otimizadas

---

> **📝 Nota**: Histórico completo disponível no arquivo CHANGELOG.MD

</div>

<div id="documentacao-final">

## 📚 Documentação Final

### 🎯 Sobre o AraldiTech - Pedidos

O **AraldiTech - Pedidos** representa um marco no desenvolvimento de soluções práticas para gestão de pedidos ao setor de compras. Desenvolvido com tecnologias modernas e foco na experiência do usuário, este sistema oferece uma plataforma robusta, segura e intuitiva para o gerenciamento completo de pedidos de compras.

### 🏆 Principais Conquistas 

#### 🛠️ Tecnológicas
- **Arquitetura Moderna**: Implementação com FastAPI e Vue.js
- **Segurança Robusta**: Autenticação JWT e proteção CSRF
- **Performance Otimizada**: Sistema de cache e consultas eficientes
- **Responsividade Total**: Suporte completo para dispositivos móveis
- **Escalabilidade**: Arquitetura preparada para crescimento

#### 👥 Experiência do Usuário
- **Interface Intuitiva**: Design moderno e fácil navegação
- **Hierarquia Clara**: Três níveis de usuário bem definidos
- **Feedback Imediato**: Notificações e confirmações em tempo real
- **Acessibilidade**: Componentes acessíveis e responsivos
- **Tutorial Integrado**: Sistema de ajuda contextual

#### 📊 Funcionalidades Avançadas
- **Dashboard Interativo**: Gráficos e métricas em tempo real
- **Sistema de Relatórios**: Análises financeiras e operacionais
- **Logs Detalhados**: Auditoria completa de atividades
- **Gestão por Setores**: Segmentação e controle de acesso
- **Histórico Completo**: Rastreamento de todas as alterações

### 🔮 Evolução do Projeto

#### 📈 Crescimento Contínuo
O projeto evoluiu de uma simples necessidade de um controle de pedidos realizados para o setor de compras para uma aplicação completa de gestão de pedidos, incorporando:

- **16 versões** de desenvolvimento ativo
- **8 setores** organizacionais suportados
- **3 níveis** de hierarquia de usuários
- **Múltiplas funcionalidades** avançadas
- **Segurança enterprise-grade**

#### 🎯 Marcos Importantes
- **v0.3.3**: Primeira versão com controle de acesso
- **v0.4.0**: Implementação do frontend Vue.js
- **v0.6.0**: Sistema completo de modais e gestão
- **v0.7.0**: Expansão para múltiplos setores
- **v0.8.0**: Dashboard e relatórios financeiros
- **v0.8.5**: Segurança avançada e sistema de cache
- **v0.9.0**: Versão de transição para desenvolvimento privado

### 🚨 Transição para Desenvolvimento Privado

#### 📢 Comunicado Oficial
A partir da **versão 0.9.1**, o desenvolvimento do AraldiTech - Pedidos continuará em um **repositório privado**. Esta decisão foi tomada para:

1. **🔐 Proteção Intelectual**: Salvaguardar inovações e funcionalidades exclusivas
2. **🎯 Foco Comercial**: Direcionamento para soluções empresariais específicas
3. **⚡ Desenvolvimento Acelerado**: Maior agilidade sem exposição pública
4. **🤝 Parcerias Estratégicas**: Colaborações comerciais direcionadas
5. **📈 Sustentabilidade**: Modelo de negócio sustentável

#### 🔄 O Que Isso Significa

**Para a Comunidade:**
- ✅ Código atual permanece disponível (MIT License)
- ✅ Documentação completa mantida
- ✅ Suporte para versão atual
- ❌ Novas funcionalidades não serão públicas
- ❌ Atualizações futuras serão privadas

**Para Empresas Interessadas:**
- 🤝 Licenciamento comercial disponível
- 📞 Suporte técnico especializado
- 🎯 Customizações específicas
- 📈 Implementação empresarial
- 🔧 Manutenção e atualizações

### 📞 Contato para Versões Futuras

#### 🏢 Licenciamento Empresarial
Para acesso às versões futuras e licenciamento comercial:

**📧 Email**: [lucasaraldi.dev@gmail.com](mailto:lucasaraldi.dev@gmail.com)  
**📱 WhatsApp Business**: [+55 (81) 99203-6259]  
**🌐 Website**: [EM DESENVOLVIMENTO](https://www.aralditech.cloud)  


#### 📋 Informações para Contato
Ao entrar em contato, inclua:
- 🏢 Nome da empresa/organização
- 👤 Pessoa de contato responsável
- 📊 Tamanho da operação (usuários estimados)
- 🎯 Necessidades específicas
- 📅 Cronograma de implementação
- 💰 Orçamento estimado

### 🎓 Aprendizados e Legado

#### 💡 Lições Aprendidas
- **Arquitetura Modular**: Importância da separação de responsabilidades
- **Segurança First**: Implementação de segurança desde o início
- **UX/UI Centrado**: Foco na experiência do usuário
- **Documentação Viva**: Manutenção constante da documentação
- **Testes Automatizados**: Garantia de qualidade contínua

#### 🌟 Contribuições para a Comunidade
- **Código Aberto**: Disponibilização do código para aprendizado
- **Documentação Detalhada**: Guias completos de implementação
- **Boas Práticas**: Exemplos de desenvolvimento moderno
- **Arquitetura Referência**: Modelo para projetos similares

### 🙏 Agradecimentos

#### 👥 Comunidade
Agradecemos a todos que contribuíram, testaram e forneceram feedback durante o desenvolvimento público do projeto.

#### 🛠️ Tecnologias
Reconhecimento às tecnologias e frameworks que tornaram este projeto possível:
- **FastAPI** - Framework web moderno
- **Vue.js** - Framework frontend reativo
- **MongoDB** - Banco de dados NoSQL
- **JWT** - Autenticação segura
- **Chart.js** - Visualização de dados

### 📜 Licença e Uso

#### 📋 Licença MIT
O código atual permanece sob **Licença MIT**, permitindo:
- ✅ Uso comercial
- ✅ Modificação
- ✅ Distribuição
- ✅ Uso privado
- ❗ Sem garantias

#### ⚖️ Termos de Uso
- Atribuição ao autor original obrigatória
- Uso por conta e risco do usuário
- Sem suporte oficial para versões modificadas
- Respeito aos direitos autorais

---

### 🎯 Considerações Finais

O **AraldiTech - Pedidos v0.9.0** representa o culminar de meses de desenvolvimento dedicado, incorporando as melhores práticas de desenvolvimento web moderno, segurança de ponta e experiência do usuário.

Esta versão serve como uma **ponte** entre o desenvolvimento open-source e a evolução para uma aplicação robusta e comercialmente viável.

**🚀 O futuro do AraldiTech - Pedidos será ainda mais promissor, com funcionalidades avançadas, suporte especializado e soluções customizadas para empresas que buscam excelência em gestão de pedidos.**s

---

**📅 Última atualização**: Junho 2025  
**👨‍💻 Desenvolvido por**: Lucas Araldi  
**🏢 AraldiTech**

</div>

---

<div align="center">
  <h3>🔗 Links Úteis</h3>
  <p>
    <a href="https://github.com/LucasAraldi-Dev/AraldiTech-Pedidos">🏠 Repositório</a> • 
    <a href="mailto:lucasaraldi.dev@gmail.com">📧 Contato</a> • 
    <a href="#documentacao-final">📚 Documentação</a>
  </p>
  
  <p><strong>⚠️ Última versão pública - Futuras versões serão privadas</strong></p>
</div> 