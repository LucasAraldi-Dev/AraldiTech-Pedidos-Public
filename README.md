# AraldiTech - Pedidos (Versão 0.5) 
![GitHub version](https://img.shields.io/badge/version-0.5.0-blue)

## Descrição
**AraldiTech - Pedidos** é um WebApp desenvolvido para gerenciar pedidos de produtos para setores específicos, com interface moderna, intuitiva e responsiva, proporcionando uma experiência de uso otimizada.

O projeto é construído com **FastAPI**, **MongoDB**, **Vue.js**, e conta com autenticação baseada em **JWT** para garantir a segurança de acesso.

Principais funcionalidades:
- Criação e edição de novos pedidos
- Listagem e consulta de pedidos
- Controle de acesso por autenticação JWT
- Interface interativa e responsiva com Vue.js
- Modal de impressão de pedidos
- Hierarquia de usuários: **Comum** e **Gestor**
- Sincronização dinâmica entre modais

## Tecnologias Utilizadas
- **Python**: Linguagem de programação principal para a API.
- **FastAPI**: Framework para construção rápida de APIs RESTful.
- **JavaScript / Vue.js**: Usado para construir uma interface interativa e moderna no frontend.
- **MongoDB**: Banco de dados NoSQL utilizado para o armazenamento dos pedidos e usuários.
- **Motor**: Driver assíncrono para integração com MongoDB.
- **OAuth2 com JWT**: Autenticação segura usando JSON Web Tokens.

## Versão
A versão atual do projeto é **0.5.0**. 

### Mudanças Principais na Versão 0.5.0
A versão 0.5.0 traz diversas melhorias e novos recursos, incluindo:
- **Novo Botão de CONCLUIR Pedido**: Adicionado um novo botão para marcar pedidos como CONCLUÍDOS.
- **Modal de Alerta para CONCLUIR Pedido**: Um modal interativo para confirmar a ação de CONCLUIR um pedido.
- **Sincronização em Tempo Real**: Atualizações dinâmicas entre modais de edição e consulta de pedidos.
- **Feedback Visual nos Botões**: Destaque visual nos botões ao interagir com os modais.
- **Correção de Bugs nos Modais**: Sincronização aprimorada entre modais de consulta e edição de pedidos.
- **Melhorias na Responsividade**: Ajustes adicionais para dispositivos móveis.


## Funcionalidades
- **Autenticação JWT**: Somente usuários autenticados têm permissão para criar, listar e editar pedidos.
- **Hierarquia de Usuários**:
  - **Comum**: Acesso limitado às funcionalidades de pedidos e consulta.
  - **Gestor**: Planejado para funcionalidades avançadas de gerenciamento.
- **CRUD de Pedidos**: Funcionalidades de Criação, Leitura, Atualização e Exclusão de pedidos.
- **Interface Responsiva**: Suporte melhorado para dispositivos móveis com ajustes visuais e de navegação.
- **Modal de Impressão**: Modal interativo para facilitar a impressão de pedidos.
- **Sincronização de Modais**: Melhor integração entre modais para operações contínuas.

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