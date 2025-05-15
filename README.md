# AraldiTech - Pedidos (Versão 0.8.5) 
![GitHub version](https://img.shields.io/badge/version-0.8.5-blue)

## Descrição
**AraldiTech - Pedidos** é um WebApp desenvolvido para gerenciar pedidos de produtos para setores específicos, com interface moderna, intuitiva e responsiva, proporcionando uma experiência de uso otimizada.

O projeto é construído com **FastAPI**, **MongoDB**, **Vue.js**, e conta com autenticação baseada em **JWT** para garantir a segurança de acesso.

Principais funcionalidades:
- Criação e edição de novos pedidos
- Listagem e consulta de pedidos por setor
- Controle de acesso por autenticação JWT
- Dashboard com gráficos e métricas para gestores
- Interface interativa e responsiva com Vue.js
- Histórico detalhado de atividades e alterações
- Hierarquia de usuários: **Comum**, **Gestor** e **Admin**
- Segmentação por setores com permissões específicas

## Tecnologias Utilizadas
- **Python**: Linguagem de programação principal para a API.
- **FastAPI**: Framework para construção rápida de APIs RESTful.
- **JavaScript / Vue.js**: Usado para construir uma interface interativa e moderna no frontend.
- **MongoDB**: Banco de dados NoSQL utilizado para o armazenamento dos pedidos e usuários.
- **Motor**: Driver assíncrono para integração com MongoDB.
- **OAuth2 com JWT**: Autenticação segura usando JSON Web Tokens.
- **Chart.js**: Biblioteca para criação de gráficos interativos no dashboard.
- **Jest**: Framework de testes unitários para garantia de qualidade do código.

## Versão  
A versão atual do projeto é **0.8.5**.

### Principais Alterações na Versão 0.8.5

#### Adicionado
- **Segurança Reforçada**: Proteção CSRF, validação avançada de dados e detecção de ataques comuns.
- **Sistema de Cache**: Otimização de desempenho com armazenamento temporário de dados frequentes.
- **Visualizador de Logs**: Nova interface para administradores monitorarem atividades do sistema.
- **Testes Automatizados**: Implementação de testes unitários para garantia de qualidade.
- **Componentes Reutilizáveis**: Novos elementos de UI para feedback visual aprimorado.

#### Melhorado
- **Performance**: Redução no tempo de carregamento e otimização de requisições.
- **Feedback ao Usuário**: Indicações visuais claras durante processos e operações.
- **Responsividade**: Melhor adaptação a diferentes tamanhos de tela e dispositivos.
- **Organização do Código**: Estrutura modular para facilitar manutenção futura.
- **Validação de Dados**: Sistema unificado para garantir consistência em formulários.

#### Corrigido
- **Inconsistências de Interface**: Padronização visual entre diferentes seções do aplicativo.
- **Problemas em Dispositivos Móveis**: Ajustes para melhor experiência em telas pequenas.
- **Tratamento de Erros**: Sistema robusto para lidar com falhas inesperadas.
- **Manipulação de Datas**: Formato consistente em todo o sistema.

## Funcionalidades
- **Autenticação JWT**: Somente usuários autenticados têm permissão para criar, listar e editar pedidos.
- **Hierarquia de Usuários**:
  - **Comum**: Acesso limitado às funcionalidades de pedidos e consulta no seu setor.
  - **Gestor**: Acesso ao dashboard com métricas e relatórios.
  - **Admin**: Acesso total a todos os setores e funcionalidades administrativas.
- **CRUD de Pedidos**: Funcionalidades de Criação, Leitura, Atualização e Exclusão de pedidos.
- **Segmentação por Setor**: Visualização e gerenciamento de pedidos organizados por setor.
- **Interface Responsiva**: Suporte para dispositivos móveis com ajustes visuais e de navegação.
- **Dashboard com Gráficos**: Visualização interativa de dados e métricas para gestores.
- **Logs de Atividades**: Registro detalhado de todas as ações realizadas no sistema.

## Instalação

### Pré-requisitos
- **Python 3.10+**
- **Node.js** e **npm** (para o frontend com Vue.js)
- **MongoDB** (local ou em um servidor)

### Configuração
1. Clone este repositório:
    ```bash
    git clone https://github.com/LucasAraldi-Dev/AraldiTech-Pedidos.git
    cd AraldiTech-Pedidos
    ```

2. Instale as dependências do backend:
    ```bash
    pip install -r requirements.txt
    ```

3. Instale as dependências do frontend:
    ```bash
    cd frontend
    npm install
    ```

4. Configure o banco de dados MongoDB e as variáveis de ambiente para a autenticação JWT.

5. Inicie o servidor FastAPI (backend):
    ```bash
    uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

6. Inicie o servidor Vue.js (frontend):
    ```bash
    cd frontend
    npm run serve
    ```

7. Execute os testes unitários:
    ```bash
    cd frontend
    npm run test:unit
    ```

8. Acesse a aplicação em `http://localhost:8080` para o frontend, ou conforme configurado.

## Contribuição
Contribuições são bem-vindas! Se você quiser sugerir melhorias, abrir uma issue ou fazer um pull request, fique à vontade.