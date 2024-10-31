# AraldiTech - Pedidos
![GitHub version](https://img.shields.io/badge/version-0.3.4-blue)


## Descrição

**AraldiTech - Pedidos** é um WebApp desenvolvido com FastAPI, MongoDB e autenticação baseada em JWT, que gerencia pedidos de produtos para setores específicos. 

Ele oferece funcionalidades como:
- Criação de novos pedidos
- Edição de pedidos existentes
- Listagem de todos os pedidos
- Controle de acesso por autenticação JWT

## Tecnologias Utilizadas

- **[Python](https://www.python.org/)**: Linguagem de programação principal do projeto.
- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework para desenvolvimento de APIs de uma forma rápida.
- **[JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)**: Utilizado no front-end para fazer a interação com o Front.
- **[MongoDB](https://www.mongodb.com/)**: Banco de dados NoSQL para armazenamento dos pedidos e usuários.
- **[Motor](https://motor.readthedocs.io/)**: Driver assíncrono para integração com MongoDB.
- **[OAuth2 com JWT](https://oauth.net/2/)**: Sistema que utilizamos para autenticação seguro usando JSON Web Tokens.

## Versão

A versão atual do projeto é **0.3.4**.

### Alterações na Versão **0.3.4**
**Estilos e Estrutura:**
- **Atualização no Estilo do Formulário:** 
  - Ajuste nos estilos do formulário para uma aparência mais moderna e limpa.
  - Botão "CONSULTAR PEDIDOS" estilizado e posicionado fora do formulário para melhor usabilidade.
  - Adicionada uma logo no topo da página, aprimorando a identidade visual.
  
**Correção de Autenticação de Segurança:** 
- Removido o middleware de autenticação que restringe o acesso às páginas do aplicativo.
- Permissão de acesso livre às páginas `index.html` e `login_pedidos.html` dentro do diretório `/static`.
- Usuários não autenticados que tentarem acessar outras páginas serão redirecionados para a página inicial (`/static/index.html`).
- Logs foram adicionados para registrar tentativas de acesso e outras atividades relacionadas à autenticação.

**Próxima Versão:**
A próxima grande atualização **(0.4.0)** está planejada para reformular completamente o design da aplicação, trazendo uma interface mais intuitiva e moderna.

## Funcionalidades

- **Autenticação JWT**: Somente usuários autenticados podem criar, listar e editar pedidos.
- **Registro de Usuários**: Permite o registro de novos usuários no sistema.
- **CRUD de Pedidos**: Funcionalidades de Criação, Leitura, Atualização e Exclusão de pedidos.

## Instalação

### Pré-requisitos

- **Python 3.10+**
- **MongoDB** (local ou em um servidor)


# AraldiTech - Pedidos
