# AraldiTech - Pedidos (Versão 0.8.1) 
![GitHub version](https://img.shields.io/badge/version-0.8.1-blue)

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
A versão atual do projeto é **0.8.1**.

### Mudanças Principais na Versão 0.8.1
A versão 0.8.1 traz importantes correções e melhorias de usabilidade:

- **Validação no Cadastro de Usuários**: Correção no modal de cadastro que agora identifica corretamente erros de conexão com o banco de dados.
- **Controle de Edição de Datas**: O campo de data na edição de pedidos agora mantém a data original e só pode ser editado por administradores.
- **Identificação de Setor do Responsável**: Adicionado campo que mostra o setor do responsável pela compra, preenchido automaticamente e editável apenas por administradores e gestores.

### Mudanças Principais na Versão 0.8.0  
A versão 0.8.0 trouxe aprimoramentos significativos em usabilidade, segurança e visualização de dados:

- **Dashboard Reformulado**: Interface totalmente refeita para facilitar a visualização de métricas do sistema, incluindo estatísticas de pedidos e relatório financeiro com base nos dados preenchidos pelos usuários.
- **Melhorias no Login e Cadastro**: Fluxos de autenticação e registro refeitos para oferecer uma experiência mais fluida e intuitiva ao usuário.
- **Segurança Aprimorada**: Corrigidas vulnerabilidades nas áreas de login, cadastro e log de pedidos editados, garantindo maior proteção dos dados.
- **Sistema de Logs Detalhado**: Agora cada alteração em um pedido é registrada com o autor da modificação, fortalecendo a rastreabilidade.
- **Histórico de Modificações**: As edições realizadas em pedidos são armazenadas para consulta futura.
- **Dashboard para Gestores**: Painel exclusivo com gráficos e indicadores para facilitar o acompanhamento da operação.
- **Restrição por Setor**: Usuários agora acessam apenas os pedidos relacionados ao seu setor.
- **Acesso Total para Administradores**: Permissão especial para visualizar e gerenciar pedidos de todos os setores.
- **Correções de Responsividade**: Ajustes na interface para melhor adaptação em diferentes tamanhos de tela.
- **Padronização de Pedidos Concluídos**: Unificação do formato de dados dos pedidos concluídos, evitando problemas de exibição no dashboard.


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