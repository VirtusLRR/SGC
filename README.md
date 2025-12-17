# SGC - Sistema de Gerenciamento de Compras

<div align="center">

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.124.4-009688.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-1.0.5-FF6F00.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)

**Sistema inteligente de gerenciamento de items, receitas e ingredientes**

[Visão Geral](#-visão-geral) •
[Tecnologias](#-tecnologias) •
[Arquitetura](#-arquitetura) •
[Instalação](#-instalação) •
[Uso](#-uso) •
[Estrutura](#-estrutura-do-projeto) •
[API](#-documentação-da-api)

</div>

---

## Visão Geral

O **SGC (Sistema de Gerenciamento de Compras)** é uma aplicação inteligente que utiliza agentes de IA baseados em LangGraph para gerenciar receitas, ingredientes e responder perguntas sobre culinária. O sistema é capaz de:

- **CRUD completo** de Itens
- **CRUD completo** de Receitas
- **Consultar receitas** disponíveis no banco de dados
- **Verificar disponibilidade** de ingredientes para preparar receitas
- **Buscar informações** na web sobre culinária
- **Adicionar novas receitas** através de conversação natural
- **Interagir de forma inteligente** usando múltiplos agentes especializados

### Características Principais

- **Multi-Agent System**: Arquitetura baseada em agentes especializados (Orchestrator, SQL, Web, Structurer, Revisor, Trivial)
- **LangGraph Workflow**: Fluxo de trabalho inteligente com checkpoints e estados persistentes
- **API RESTful**: Interface completa com FastAPI
- **Database Agnostic**: Suporte a PostgreSQL com SQLAlchemy ORM
- **Dockerized**: Ambiente completamente containerizado
- **Test Coverage**: Testes unitários e BDD com pytest

---

## Tecnologias

### Backend & Framework
- **[Python 3.12](https://www.python.org/)** - Linguagem de programação
- **[FastAPI 0.124.4](https://fastapi.tiangolo.com/)** - Framework web moderno e rápido
- **[Uvicorn 0.38.0](https://www.uvicorn.org/)** - ASGI server
- **[Pydantic 2.12.5](https://docs.pydantic.dev/)** - Validação de dados

### Database & ORM
- **[PostgreSQL 16](https://www.postgresql.org/)** - Banco de dados relacional
- **[SQLAlchemy 2.0.45](https://www.sqlalchemy.org/)** - ORM Python
- **[psycopg2-binary 2.9.11](https://www.psycopg.org/)** - Adaptador PostgreSQL

### AI & LangChain
- **[LangChain 1.1.3](https://www.langchain.com/)** - Framework para aplicações LLM
- **[LangGraph 1.0.5](https://github.com/langchain-ai/langgraph)** - Orquestração de agentes
- **[LangChain Google GenAI 4.0.0](https://python.langchain.com/docs/integrations/platforms/google)** - Integração com Gemini
- **[LangChain Tavily 0.2.14](https://tavily.com/)** - Ferramenta de busca web
- **[LangChain Community 0.4.1](https://python.langchain.com/docs/integrations/platforms/)** - Integrações da comunidade

### DevOps & Tools
- **[Docker](https://www.docker.com/)** - Containerização
- **[Docker Compose](https://docs.docker.com/compose/)** - Orquestração de containers
- **[pytest 9.0.2](https://pytest.org/)** - Framework de testes
- **[pytest-bdd 8.1.0](https://pytest-bdd.readthedocs.io/)** - Behavior Driven Development

---

## Arquitetura

O sistema utiliza uma arquitetura de **Multi-Agent System** baseada em LangGraph:

```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    LangGraph Workflow                       │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │ Orchestrator │─────▶│   Structurer │                    │
│  └──────────────┘      └──────────────┘                    │
│         │                      │                            │
│         ├──────────────────────┼──────────────┐            │
│         ▼                      ▼               ▼            │
│  ┌──────────┐          ┌──────────┐    ┌──────────┐       │
│  │ Trivial  │          │   SQL    │    │   Web    │       │
│  └──────────┘          └──────────┘    └──────────┘       │
│                               │                             │
│                               ▼                             │
│                        ┌──────────┐                        │
│                        │ Revisor  │                        │
│                        └──────────┘                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    PostgreSQL Database                      │
│         (Recipes, Items, RecipeItems, Bots)                │
└─────────────────────────────────────────────────────────────┘
```

### Agentes

- **Orchestrator**: Roteia as requisições para os agentes apropriados
- **Structurer**: Estrutura novas receitas a partir de texto
- **Trivial**: Responde perguntas simples e conversações gerais
- **SQL**: Consulta e manipula dados do banco de dados
- **Web**: Busca informações externas na internet
- **Revisor**: Valida e revisa as respostas antes de finalizar

---

## Instalação

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) (versão 20.x ou superior)
- [Docker Compose](https://docs.docker.com/compose/install/) (versão 2.x ou superior)
- Chaves de API:
  - [Google Gemini API Key](https://makersuite.google.com/app/apikey)
  - [Tavily API Key](https://tavily.com/) (opcional, para busca web)

### Configuração Rápida

1. **Clone o repositório**
   ```bash
   git clone <repository-url>
   cd SGC
   ```

2. **Configure as variáveis de ambiente**
   ```bash
   cp .env.example .env
   ```

3. **Edite o arquivo `.env`** com suas credenciais:
   ```env
   GOOGLE_API_KEY=sua_chave_aqui
   TAVILY_API_KEY=sua_chave_aqui
   
   POSTGRES_USER=SGC_USER
   POSTGRES_PASSWORD=SGC_DB123
   POSTGRES_DB=SGC_DB
   POSTGRES_HOST=database
   POSTGRES_PORT=5432
   ```

4. **Inicie os containers**
   ```bash
   docker-compose up -d --build
   ```

5. **Verifique se os serviços estão rodando**
   ```bash
   docker-compose ps
   ```

   Você deve ver:
   ```
   NAME       IMAGE          STATUS         PORTS
   backend    sgc-backend    Up X seconds   0.0.0.0:8000->8000/tcp
   database   postgres:16    Up X seconds   0.0.0.0:5432->5432/tcp
   ```

6. **Popular o banco de dados** (opcional)
   ```bash
   docker-compose exec backend python scripts/populate_database.py
   ```

### Verificação da Instalação

Acesse a documentação interativa da API:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
---

## Estrutura do Projeto

```
SGC/
├── docker-compose.yaml          # Orquestração de containers
├── README.md                    # Documentação do projeto
├── .env                         # Variáveis de ambiente (não versionado)
├── .env.example                 # Exemplo de variáveis de ambiente
│
└── backend/                        # Aplicação Backend
    ├── Dockerfile               # Imagem Docker do backend
    ├── index.py                 # Entry point da aplicação
    ├── requirements.txt         # Dependências Python
    ├── pytest.ini               # Configuração do pytest
    │
    ├── controllers/             # Lógica de negócio
    │   ├── bot.py                  # Controller do chatbot
    │   ├── item.py                 # Controller de itens
    │   └── recipe.py               # Controller de receitas
    │
    ├── database/                # Configuração do banco
    │   ├── database.py             # Conexão e sessão SQLAlchemy
    │   ├── sqlite.db               # BD SQLite (legacy, não usado)
    │   └── checkpoints.db          # Checkpoints do LangGraph
    │
    ├── models/                  # Modelos SQLAlchemy (ORM)
    │   ├── bot.py                  # Modelo de conversas
    │   ├── item.py                 # Modelo de ingredientes
    │   ├── recipe.py               # Modelo de receitas
    │   └── recipe_item.py          # Relacionamento N:N
    │
    ├── repositories/            # Camada de acesso a dados
    │   ├── bot.py                  # Repositório de conversas
    │   ├── item.py                 # Repositório de itens
    │   └── recipe.py               # Repositório de receitas
    │
    ├── routes/                  # Endpoints da API
    │   ├── bot.py                  # Rotas do chatbot
    │   ├── item.py                 # Rotas de itens
    │   └── recipe.py               # Rotas de receitas
    │
    ├── schemas/                 # Schemas Pydantic
    │   ├── bot.py                  # Schemas de request/response
    │   ├── item.py                 # Validação de dados
    │   └── recipe.py               # DTOs
    │
    ├── services/                # Serviços e lógica complexa
    │   └── graph/                  # Sistema de agentes LangGraph
    │       ├── graph.py            # Definição do workflow
    │       ├── state.py            # Estado compartilhado
    │       ├── utils.py            # Utilitários
    │       │
    │       ├── agents/             # Agentes especializados
    │       │   ├── orchestrator.py # Agente orquestrador
    │       │   ├── sql.py          # Agente de banco de dados
    │       │   ├── web.py          # Agente de busca web
    │       │   ├── structurer.py   # Agente estruturador
    │       │   ├── revisor.py      # Agente revisor
    │       │   └── trivial.py      # Agente de conversação
    │       │
    │       ├── nodes/              # Nós do grafo
    │       ├── prompts/            # Prompts dos agentes
    │       ├── schemas/            # Schemas internos
    │       └── tools/              # Ferramentas customizadas
    │           ├── sql.py          # Tools de SQL
    │           └── web.py          # Tools de busca web
    │
    ├── scripts/                 # Scripts utilitários
    │   └── populate_database.py    # Popular BD com dados de teste
    │
    └── tests/                   # Testes automatizados
        ├── conftest.py             # Configuração dos testes
        ├── test_agents.py          # Testes dos agentes
        ├── test_graph.py           # Testes do workflow
        ├── test_models.py          # Testes dos modelos
        ├── test_route_item.py      # Testes de rotas
        └── bdd/                    # Testes BDD
            ├── features/           # Arquivos .feature (Gherkin)
            └── steps/              # Implementação dos steps
```

---

## Documentação da API

Acesse a documentação completa e interativa em:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Autores

Desenvolvido durante a **Residência em Software Virtus** 


