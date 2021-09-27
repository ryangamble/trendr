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

We can run these all automatically from the main docker compose. This is the preffered method for deployment and development. Read about it in [`README.md`](../README.md)

#### Celery worker
To run a celery worker:  
`celery -A trendr.celery.workers.basic worker --loglevel=INFO`

In the future these workers will be differentiated, so this command will change based on the target worker.

#### RabbitMQ
See information on how to install RabbitMQ:  
https://docs.celeryproject.org/en/stable/getting-started/backends-and-brokers/rabbitmq.html#broker-rabbitmq

To run the docker image for RabbitMQ:  
`docker run -d -p 5672:5672 rabbitmq`

#### Celerybeat
Celerybeat is a task scheduler for celery. It can be used to schedule recurring tasks similar to how you can use `cron` to schedule tasks.

To run celerybeat:  
`celery -A trendr.celery.celerybeat beat -l info`


#### Flower
Flower is a dashboard monitoring and administration tool for celery. It is used to view the status of your worker pool, understand errors, and view statistics.

To run flower:  
`celery -A trendr.celery --broker="pyamqp://rabbitmq:5672" flower`