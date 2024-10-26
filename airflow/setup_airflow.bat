@echo off
:: Step 1: Prompt for user input
set /p username="Enter your desired Airflow username: "
set /p firstname="Enter your first name: "
set /p lastname="Enter your last name: "
set /p email="Enter your email address: "
set /p password="Enter your desired password: "

:: Step 2: Set up the directory structure and files
echo Setting up Airflow with Docker...
mkdir airflow-docker
cd airflow-docker

echo Creating necessary directories...
mkdir dags logs plugins

echo Writing docker-compose.yaml file...
(
echo version: '3'
echo services:
echo   postgres:
echo     image: postgres:13
echo     environment:
echo       POSTGRES_USER: airflow
echo       POSTGRES_PASSWORD: airflow
echo       POSTGRES_DB: airflow
echo     logging:
echo       options:
echo         max-size: 10m
echo         max-file: "3"
echo
echo   redis:
echo     image: redis:latest
echo     logging:
echo       options:
echo         max-size: 10m
echo         max-file: "3"
echo
echo   airflow-webserver:
echo     image: apache/airflow:2.7.1
echo     environment:
echo       - AIRFLOW__CORE__EXECUTOR=CeleryExecutor
echo       - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
echo       - AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0
echo       - AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow
echo     volumes:
echo       - ./dags:/opt/airflow/dags
echo       - ./logs:/opt/airflow/logs
echo       - ./plugins:/opt/airflow/plugins
echo     ports:
echo       - "8080:8080"
echo     depends_on:
echo       - postgres
echo       - redis
echo     command: webserver
echo
echo   airflow-scheduler:
echo     image: apache/airflow:2.7.1
echo     environment:
echo       - AIRFLOW__CORE__EXECUTOR=CeleryExecutor
echo       - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
echo       - AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0
echo       - AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow
echo     volumes:
echo       - ./dags:/opt/airflow/dags
echo       - ./logs:/opt/airflow/logs
echo       - ./plugins:/opt/airflow/plugins
echo     depends_on:
echo       - postgres
echo       - redis
echo     command: scheduler
echo
echo   airflow-worker:
echo     image: apache/airflow:2.7.1
echo     environment:
echo       - AIRFLOW__CORE__EXECUTOR=CeleryExecutor
echo       - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
echo       - AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0
echo       - AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow
echo     volumes:
echo       - ./dags:/opt/airflow/dags
echo       - ./logs:/opt/airflow/logs
echo       - ./plugins:/opt/airflow/plugins
echo     depends_on:
echo       - postgres
echo       - redis
echo     command: worker
echo
echo   airflow-init:
echo     image: apache/airflow:2.7.1
echo     environment:
echo       - AIRFLOW__CORE__EXECUTOR=CeleryExecutor
echo       - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
echo       - AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0
echo       - AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow
echo     volumes:
echo       - ./dags:/opt/airflow/dags
echo       - ./logs:/opt/airflow/logs
echo       - ./plugins:/opt/airflow/plugins
echo     entrypoint: airflow db init
echo     depends_on:
echo       - postgres
echo       - redis
) > docker-compose.yaml

:: Step 3: Pull and initialize the Docker containers
echo Initializing the Airflow database...
docker-compose up airflow-init

:: Step 4: Create the admin user
echo Creating Airflow admin user...
docker-compose run airflow-webserver airflow users create ^
    --username %username% ^
    --firstname %firstname% ^
    --lastname %lastname% ^
    --role Admin ^
    --email %email% ^
    --password %password%

:: Step 5: Start the Airflow services
echo Starting the Airflow services...
docker-compose up -d

:: Step 6: Provide the launch URL
echo.
echo "================================================="
echo "Airflow setup complete! You can access it here:"
echo "http://localhost:8080"
echo "================================================="
pause
