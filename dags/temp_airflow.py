import sys
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Append the absolute path to src directory
sys.path.append('/opt/airflow/src')

from data_pipeline.preprocess import preprocess_data
from data_pipeline.dvc_tracker import track_all_data_with_dvc
from data_pipeline.scraper import scrape_sections_up_to_current_week

RAW_DATA_PATH = 'data/raw'
PROCESSED_DATA_PATH = 'data/processed'
TRACK_DATA_PATH = 'data'

default_args = {
    'owner': 'santosh',
    'start_date': datetime(2024, 10, 25),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('temp_data_pipeline_dag', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    
    def scrape_task_func():
        scrape_sections_up_to_current_week()

    scrape_task = PythonOperator(
        task_id='scrape_task',
        python_callable=scrape_task_func,
    )
    
    def preprocess_data_task():
        preprocess_data(RAW_DATA_PATH, PROCESSED_DATA_PATH)
    
    preprocess_task = PythonOperator(
        task_id='preprocess_task',
        python_callable=preprocess_data_task,
    )
    
    def track_data_task_func():
        track_all_data_with_dvc(TRACK_DATA_PATH)
    
    track_data_task = PythonOperator(
        task_id='track_data_task',
        python_callable=track_data_task_func,
    )
    
    scrape_task >> preprocess_task >> track_data_task