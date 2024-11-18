# AraldiTech - Pedidos (Versão 0.4.3) 
![GitHub version](https://img.shields.io/badge/version-0.4.3-blue)

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

## Tecnologias Utilizadas
- **Python**: Linguagem de programação principal para a API.
- **FastAPI**: Framework para construção rápida de APIs RESTful.
- **JavaScript / Vue.js**: Usado para construir uma interface interativa e moderna no frontend.
- **MongoDB**: Banco de dados NoSQL utilizado para o armazenamento dos pedidos e usuários.
- **Motor**: Driver assíncrono para integração com MongoDB.
- **OAuth2 com JWT**: Autenticação segura usando JSON Web Tokens.

## Versão
A versão atual do projeto é **0.4.3**. 

### Mudanças Principais na Versão 0.4.3 
A versão 0.4.3 introduz melhorias importantes e ajustes no projeto, incluindo:

- **Hierarquia de Usuários**: Adicionada funcionalidade para diferenciação entre usuários **comuns** e **gestores**, criando uma base para personalização de funcionalidades.
- **Ajustes no Painel do Usuário Comum**: Melhorias na interface e na experiência de navegação no painel, deixando mais intuitivo e funcional.
- **Preparação para o Painel de Controle do Gestor**: Back-end já preparado para integrar futuramente o painel do gestor com permissões específicas.
- **Layout Geral Reformulado**: Adaptação visual de diversos elementos para maior consistência e modernização da interface.
- **Melhorias de Responsividade**: Ajustes para que a interface se comporte bem em dispositivos móveis e telas menores (em fase de teste).

## Funcionalidades
- **Autenticação JWT**: Somente usuários autenticados têm permissão para criar, listar e editar pedidos.
- **Hierarquia de Usuários**:
  - **Comum**: Acesso limitado às funcionalidades de pedidos e consulta.
  - **Gestor**: Planejado para funcionalidades avançadas de gerenciamento.
- **CRUD de Pedidos**: Funcionalidades de Criação, Leitura, Atualização e Exclusão de pedidos.
- **Interface Responsiva**: Suporte melhorado para dispositivos móveis com ajustes visuais e de navegação.
- **Modal de Impressão**: Modal interativo para facilitar a impressão de pedidos.

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
