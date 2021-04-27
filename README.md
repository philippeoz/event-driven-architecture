# Arquitetura baseada em eventos (microserviços)

Pequena arquitetura com o intuito de aplicar/testar conhecimentos em microserviços e Event-Driven.

A aplicação consistem em dois microserviços:
 - API de consultas médicas
   - Iniciar consulta
   - Finalizar consulta
 - API financeira
   - Verificar cobrança

Sempre que uma consulta é finalizada, um evento é lançado e uma cobrança é gerada a partir daquele evento.

Durante o desenvolvimento foram utilizadas as seguintes tecnologias:
 - [Python 3.7](https://www.python.org/downloads/release/python-379/)
   - [FastAPI](https://fastapi.tiangolo.com/)
   - [kafka-python](https://pypi.org/project/kafka-python/)
   - [motor](https://motor.readthedocs.io/en/stable/)
   - [pytest](https://docs.pytest.org/en/6.2.x/)
   - [Poetry](https://python-poetry.org/)
 - [Apache Kafka](https://kafka.apache.org/)
 - [Kafdrop](https://github.com/obsidiandynamics/kafdrop)
 - [MongoDB](https://www.mongodb.com/)
 - [Docker](https://www.docker.com/)
 - [docker-compose](https://docs.docker.com/compose/)

## How to setup

Caso queira montar o ambiente na sua máquina eu recomendo instalar toda a parte python (microserviços) e deixar o restante rodando nos containers docker. Você pode utilizar o [pyenv](https://github.com/pyenv/pyenv) para gerenciar as versões do python e o [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) para gerenciar seus ambientes virtuais, uma [combinação dos dois](https://github.com/pyenv/pyenv-virtualenvwrapper) é só alegria.

Após montar o seu ambiente e instalar o poetry, basta um `poetry install` e todas as dependencias serão instaladas.

Faça uma cópia do arquivo `.env.example` renomeando para `.env`, após isso configure o novo arquivo com suas variáveis de ambiente.

 - Para executar o serviço de atendimentos médicos:
   ```
   python appointment/run.py
   ``` 
 - Para executar o serviço de financeiro.
   ```
   python financial/run.py
   ```

E claro, voce pode optar por rodar todo o projeto em containers docker, sem a necessidade de muitas instalações e setando as variáveis de ambiente direto no docker-composer, dentro da pasta do projeto basta executar:
```
docker-compose up --build
```
Caso queira deixar rodando em background:
```
docker-compose up --build -d
```

## Docs

Os dois serviços possuem documentação com swagger e redoc.
Acessando `"/docs"` você tem acesso ao [Swagger](https://swagger.io/), onde você também consegue testar os endpoints.
Acessando `"/redoc"` você tem acesso ao [ReDoc](https://github.com/Redocly/redoc).

Você também pode monitorar os eventos utilizando o Kafdrop que estará rodando em http://localhost:19000.


## Routes

 - Appointment:
   - `[POST] "/"`
     ```javascript
     // body

     {
        "physician_id": "ea959b03-5577-45c9-b9f7-a45d3e77ce82",
        "patient_id": "86158d46-ce33-4e3d-9822-462bbff5782e",
     }

     // response
     {
        "id": "84ab6121-c4a8-4684-8cc2-b03024ec0f1d",
        "start_date": "2020-12-01 13:00:00",
        "end_date": null,
        "physician_id": "ea959b03-5577-45c9-b9f7-a45d3e77ce82",
        "patient_id": "86158d46-ce33-4e3d-9822-462bbff5782e",
        "price": 200.00
     }
     ```
    - `[POST] "/{id}/"`
        ```javascript
        // response
        {
            "id": "84ab6121-c4a8-4684-8cc2-b03024ec0f1d",
            "start_date": "2020-12-01 13:00:00",
            "end_date": "2020-12-01 14:00:00",
            "physician_id": "ea959b03-5577-45c9-b9f7-a45d3e77ce82",
            "patient_id": "86158d46-ce33-4e3d-9822-462bbff5782e",
            "price": 200.00
        }
        ```
 - Financial:
   - `[GET] "/{id}/"`
        ```javascript
        // response
        {
            "appointment_id": "84ab6121-c4a8-4684-8cc2-b03024ec0f1d",
            "total_price": 400.00,
        }

        ```

## ToDo
 - Implementar mais testes (testar o kafka).
 - Melhorar os mocks (motor, kafka)
