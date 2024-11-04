from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

# Function to intentionally cause an error
def fail_task():
    raise ValueError("Intentional failure for SMTP alert testing")

default_args = {
    'owner': 'airflow',
    'email_on_failure': True,
    'email': ['santhoshsanz29@gmail.com', 'majji.s@northeastern.edu', 'patlannagari.a@northeastern.edu', 'kancharla.ha@northeastern.edu', 'dharmappa.r@northeastern.edu', 'reddy.ru@northeastern.edu', 'nunna.va@northeastern.edu'],  # Replace with your email
}

with DAG('test_smtp_alert',
         default_args=default_args,
         schedule_interval=None,
         start_date=days_ago(1),
         catchup=False) as dag:

    start_task = DummyOperator(task_id='start_task')
    # Task that will intentionally fail
    failure_task = PythonOperator(
        task_id='failure_task',
        python_callable=fail_task,
    )

    start_task >> failure_task
