import sys
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Append the absolute path to src directory
sys.path.append('/opt/airflow/src')

from data_pipeline.preprocess import preprocess_data
#from data_pipeline.dvc_tracker import track_all_data_with_dvc
from data_pipeline.scraper import scrape_sections_up_to_current_week
from data_pipeline.preprocess import getFileName
from data_pipeline.preprocess import getFileNameWithoutExtension 
from data_pipeline.azure_uploader import upload_to_blob

RAW_DATA_PATH = 'data/raw'
PROCESSED_DATA_PATH = 'data/processed/'
#TRACK_DATA_PATH = 'data'

default_args = {
    'owner': 'santosh',
    'start_date': datetime(2024, 10, 25),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email': ['santhoshsanz29@gmail.com', 'majji.s@northeastern.edu', 'patlannagari.a@northeastern.edu', 'kancharla.ha@northeastern.edu', 'dharmappa.r@northeastern.edu', 'reddy.ru@northeastern.edu', 'nunna.va@northeastern.edu'],
    'email_on_retry': False,
}

with DAG(
    'Data_pipeline_dag', 
    default_args=default_args, 
    description='A data pipeline DAG that scrapes sections, preprocesses the data, and uploads processed files to Azure Blob storage.',
    schedule_interval='@daily', 
    catchup=False
    ) as dag:
    
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

    def upload_task_func():
        # Iterate through all processed files in the directory
        for root, _, files in os.walk(PROCESSED_DATA_PATH):
            for file in files:
                if file.endswith(".txt"):  # Assuming you want to upload .txt files
                    file_path = os.path.join(root, file)
                    upload_to_blob(file_path, file)  # Upload each processed file

    blob_storage_task = PythonOperator(
        task_id='blob_storage_task',
        python_callable=upload_task_func,
    )
    
    scrape_task >> preprocess_task >> blob_storage_task