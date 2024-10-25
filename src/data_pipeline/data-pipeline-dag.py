"added here temporarily to test the present pipeline"
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from src.data_generation.scraper import scrape_data
from src.data_generation.preprocess import preprocess_data
from src.data_generation.dvc_tracker import track_data_with_dvc
from src.data_generation.azure_uploader import upload_to_blob
from src.data_generation.embedding_creator import create_embeddings_and_index

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('data_pipeline_dag', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:

    # Task 1: Web scraping
    scrape_task = PythonOperator(
        task_id='scrape_task',
        python_callable=scrape_data
    )

    # Task 2: Preprocess data
    preprocess_task = PythonOperator(
        task_id='preprocess_task',
        python_callable=lambda: preprocess_data('data/raw', 'data/processed')
    )

    # Task 3: Track data with DVC
    track_dvc_task = PythonOperator(
        task_id='track_dvc_task',
        python_callable=lambda: track_data_with_dvc('data/processed')
    )

    # Task 4: Upload to Azure Blob Storage
    upload_blob_task = PythonOperator(
        task_id='upload_blob_task',
        python_callable=lambda: upload_to_blob('data/processed/preprocessed_data.csv', 'your_container', 'your_connection_string')
    )

    # Task 5: Embedding and indexing
    create_index_task = PythonOperator(
        task_id='create_index_task',
        python_callable=lambda: create_embeddings_and_index('data/processed/preprocessed_data.csv', 'your_index_name')
    )

    # Define task dependencies
    scrape_task >> preprocess_task >> track_dvc_task >> upload_blob_task >> create_index_task
