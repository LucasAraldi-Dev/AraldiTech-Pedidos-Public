# AraldiTech - Pedidos (Versão 0.8.2) 
![GitHub version](https://img.shields.io/badge/version-0.8.2-blue)

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

## Versão  
A versão atual do projeto é **0.8.2**.

### Mudanças Principais na Versão 0.8.2
A versão 0.8.2 traz importantes clarificações e melhorias na interface:

- **Padronização da Terminologia**: O campo "Data de Entrega" foi renomeado para "Data do Pedido" em toda a aplicação para maior consistência.
- **Controle de Acesso Melhorado**: Agora somente administradores podem alterar a data do pedido, enquanto usuários comuns apenas visualizam o campo.
- **Feedback de Interface**: Adicionadas mensagens informativas sobre as permissões para alteração da data do pedido.

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
    uvicorn main:app --reload
    ```

6. Inicie o servidor Vue.js (frontend):
    ```bash
    cd frontend
    npm run serve
    ```

7. Acesse a aplicação em `http://localhost:8080` para o frontend, ou conforme configurado.

## Contribuição
Contribuições são bem-vindas! Se você quiser sugerir melhorias, abrir uma issue ou fazer um pull request, fique à vontade.