#!/bin/bash

# Step 1: Prompt for user input
read -p "Enter your desired Airflow username: " username
read -p "Enter your first name: " firstname
read -p "Enter your last name: " lastname
read -p "Enter your email address: " email
read -sp "Enter your desired password: " password
echo

# Step 2: Set up the directory structure and files
echo "Setting up Airflow with Docker..."
mkdir airflow-docker
cd airflow-docker || exit

echo "Creating necessary directories..."
mkdir dags logs plugins

echo "Writing docker-compose.yaml file..."
cat <<EOL > docker-compose.yaml
version: '3'
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    logging:
      options:
        max-size: 10m
        max-file: "3"

  redis:
    image: redis:latest
    logging:
      options:
        max-size: 10m
        max-file: "3"

  airflow-webserver:
    image: apache/airflow:2.7.1
    environment:
      - AIRFLOW__CORE__EXECUTOR=CeleryExecutor
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
      - AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0
      - AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    ports:
      - "8080:8080"
    depends_on:
      - postgres
      - redis
    command: webserver

  airflow-scheduler:
    image: apache/airflow:2.7.1
    environment:
      - AIRFLOW__CORE__EXECUTOR=CeleryExecutor
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
      - AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0
      - AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    depends_on:
      - postgres
      - redis
    command: scheduler

  airflow-worker:
    image: apache/airflow:2.7.1
    environment:
      - AIRFLOW__CORE__EXECUTOR=CeleryExecutor
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
      - AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0
      - AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    depends_on:
      - postgres
      - redis
    command: worker

  airflow-init:
    image: apache/airflow:2.7.1
    environment:
      - AIRFLOW__CORE__EXECUTOR=CeleryExecutor
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
      - AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0
      - AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    entrypoint: airflow db init
    depends_on:
      - postgres
      - redis
EOL

# Step 3: Pull and initialize the Docker containers
echo "Initializing the Airflow database..."
docker-compose up airflow-init

# Step 4: Create the admin user
echo "Creating Airflow admin user..."
docker-compose run airflow-webserver airflow users create \
    --username "$username" \
    --firstname "$firstname" \
    --lastname "$lastname" \
    --role Admin \
    --email "$email" \
    --password "$password"

# Step 5: Start the Airflow services
echo "Starting the Airflow services..."
docker-compose up -d

# Step 6: Provide the launch URL
echo
echo "================================================="
echo "Airflow setup complete! You can access it here:"
echo "http://localhost:8080"
echo "================================================="
