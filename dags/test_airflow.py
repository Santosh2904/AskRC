# Import necessary libraries and modules
import sys
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow import configuration as conf

# Append the absolute path to the src directory for imports
sys.path.append('/opt/airflow/src')

# Import the scraping function from the data pipeline
from data_pipeline.scraper import scrape_sections_up_to_current_week

# Enable pickle support for XCom, allowing data to be passed between tasks if needed
conf.set('core', 'enable_xcom_pickling', 'True')

# Define default arguments for your DAG
default_args = {
    'owner': 'santosh',
    'start_date': datetime(2024, 10, 25),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

# Create a DAG instance named 'Data_Pipeline_Scrape' with the defined default arguments
dag = DAG(
    'Data_Pipeline_Scrape',
    default_args=default_args,
    description='DAG to scrape sections and save data to raw directory',
    schedule_interval=None,
    catchup=False,
)

# Define a task to ensure output in data/raw
def scrape_task_func():
    # Debugging info
    print("Running scrape task function...")

    # Define the target directory inside Docker
    target_directory = '/opt/airflow/data/raw'

    # Check and create the directory if it doesn’t exist
    os.makedirs(target_directory, exist_ok=True)
    print(f"Output directory created or exists: {target_directory}")

    # Call the scrape function
    scraped_sections = scrape_sections_up_to_current_week()

    # Print result for confirmation
    print(f"Scraped sections: {scraped_sections}")
    print(f"Data should be saved in: {target_directory}")

# Define the scraping task using PythonOperator
scrape_task = PythonOperator(
    task_id='scrape_task',
    python_callable=scrape_task_func,
    dag=dag,
)

# If this script is run directly, allow command-line interaction with the DAG
if __name__ == "__main__":
    dag.cli()