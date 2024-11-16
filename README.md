# AraldiTech - Pedidos (Versão 0.4.2) 
![GitHub version](https://img.shields.io/badge/version-0.4.2-blue)

## Descrição
**AraldiTech - Pedidos** é um WebApp desenvolvido para gerenciar pedidos de produtos para setores específicos, com interface moderna, intuitiva e responsiva, proporcionando uma experiência de uso otimizada.

O projeto é construído com **FastAPI**, **MongoDB**, **Vue.js**, e conta com autenticação baseada em **JWT** para garantir a segurança de acesso.

Principais funcionalidades:
- Criação e edição de novos pedidos
- Listagem e consulta de pedidos
- Controle de acesso por autenticação JWT
- Interface interativa e responsiva com Vue.js
- Modal de impressão de pedidos

## Tecnologias Utilizadas
- **Python**: Linguagem de programação principal para a API.
- **FastAPI**: Framework para construção rápida de APIs RESTful.
- **JavaScript / Vue.js**: Usado para construir uma interface interativa e moderna no frontend.
- **MongoDB**: Banco de dados NoSQL utilizado para o armazenamento dos pedidos e usuários.
- **Motor**: Driver assíncrono para integração com MongoDB.
- **OAuth2 com JWT**: Autenticação segura usando JSON Web Tokens.

## Versão
A versão atual do projeto é **0.4.2**. 

### Mudanças Principais na Versão 0.4.2 
A versão 0.4.2 inclui diversas melhorias na interface e na funcionalidade do WebApp. As mudanças são:

- **Fechamento de modal**: Alteração na lógica para não fechar o modal ao clicar fora da tela, melhorando a experiência do usuário.
- **Design unificado de modais**: O design dos modais foi unificado, criando uma aparência mais consistente e intuitiva para o usuário.
- **Modal de Impressão**: Adicionado um novo modal para impressão de pedidos.
- **Melhoria no Layout**: Várias melhorias no layout, com pequenas alterações na disposição de elementos.
- **Correção de erro no salvamento de pedidos**: Resolução do problema onde os pedidos não estavam sendo salvos corretamente no banco de dados.

## Funcionalidades
- **Autenticação JWT**: Somente usuários autenticados têm permissão para criar, listar e editar pedidos.
- **Registro de Usuários**: Novo registro de usuários com controle de autenticação seguro.
- **CRUD de Pedidos**: Funcionalidades de Criação, Leitura, Atualização e Exclusão de pedidos.
- **Interface Responsiva**: Nova interface que se adapta a dispositivos móveis, com navegação aprimorada e suporte a exibição de pedidos e criação de novos pedidos.

## Instalação

### Pré-requisitos
- **Python 3.10+**
- **Node.js** e **npm** (para o frontend com Vue.js)
- **MongoDB** (local ou em um servidor)

### Configuração
1. Clone este repositório:
    ```bash
    git clone https://github.com/seu-usuario/AraldiTech-Pedidos.git
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
