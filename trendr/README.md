## Backend User Guide

## Usage
Before running any python commands, please enter the environment:
`source .venv/bin/activate`

### Flask
The following commands set the name of the flask app module, and then run the app:
1. `export FLASK_APP=trendr`
2. `flask run`

### Celery
To use celery tasks we need a few parts:
- celery workers
- rabbitmq (message broker)
- celerybeat (scheduled tasks)
- flower (monitor tasks and queue)

#### Celery worker
To run a celery worker:  
`celery -A trendr.tasks worker --loglevel=INFO`

#### RabbitMQ
See information on how to install RabbitMQ:  
https://docs.celeryproject.org/en/stable/getting-started/backends-and-brokers/rabbitmq.html#broker-rabbitmq

To run the docker image for RabbitMQ:  
`docker run -d -p 5672:5672 rabbitmq`

#### Celerybeat
Unfinished

#### Flower
Unfinished