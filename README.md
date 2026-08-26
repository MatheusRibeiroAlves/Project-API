# Project API

Este projeto foi criado para cadastro e gerenciamento de Imóveis.

# Tecnologias Utilizadas

* Python
* FastAPI
* Firebase Firestore

# Inicializando o Projeto

Para inicializar o projeto, você deve utilizar o seguinte comando para executar o servidor Uvicorn:

uvicorn main:app --reload

**# Funcionalidades Criadas**

Criando um CRUD:

* Adicionar imóvel
* Listar imóveis
* Deletar imóvel
* Alterar as informações do imóvel




## Testes por setor

Os testes são organizados por setor e executados via GitHub Actions conforme as labels da PR:

- `ERP` → `pytest tests/erp/`
- `CRM` → `pytest tests/crm/`
- `SITE` → `pytest tests/site/`

Requer as labels `Ready for QA` + setor para disparar os testes.
# teste de pipeline
