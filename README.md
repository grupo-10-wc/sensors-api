# Projeto FastAPI SQLAlchemy

Um projeto de API REST construído com FastAPI e SQLAlchemy, demonstrando uma arquitetura modular para gerenciamento de dados de sensores.

## Tecnologias Utilizadas

- FastAPI - Framework web moderno e rápido para construção de APIs
- SQLAlchemy - Ferramenta SQL e ORM
- Pydantic - Validação de dados usando anotações de tipo do Python
- uvicorn - Servidor ASGI extremamente rápido

## Estrutura do Projeto

O projeto segue uma arquitetura modular:

```
app/
├── core/
│   ├── database.py    # Configuração do banco de dados
├── sensor/
│   ├── controller.py  # Manipuladores de rotas
│   ├── models.py      # Modelos de banco de dados
│   ├── schemas.py     # Modelos Pydantic para requisição/resposta
│   └── service.py     # Lógica de negócios
└── main.py           # Ponto de entrada da aplicação
```

### Componentes do Módulo

- **Controller**: Manipula requisições e respostas HTTP
- **Service**: Contém lógica de negócios e operações de banco de dados
- **Models**: Define os modelos de banco de dados do SQLAlchemy
- **Schemas**: Define os modelos Pydantic para validação de dados

## Primeiros Passos

1. Crie um ambiente virtual:
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
.\env\Scripts\activate  # Windows
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
uvicorn app.main:app --host localhost --port 8000 --reload
```

## Documentação da API

Uma vez que a aplicação esteja em execução, você pode acessar:

- Documentação interativa da API: http://localhost:8000/docs
- Documentação alternativa da API: http://localhost:8000/redoc

## Endpoints Disponíveis

- `GET /api/sensors` - Lista todos os registros de sensores
- `POST /api/sensors` - Cria um novo registro de sensor
- `GET /api/sensors/{sensorId}` - Obtém um registro de sensor específico
- `PATCH /api/sensors/{sensorId}` - Atualiza um registro de sensor
- `DELETE /api/sensors/{sensorId}` - Deleta um registro de sensor

## Verificação de Saúde

- `GET /api/healthchecker` - Verifica se a API está em execução