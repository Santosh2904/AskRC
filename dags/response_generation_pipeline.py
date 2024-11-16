import os
import sys
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

# Append the absolute path to src directory
sys.path.append('/opt/airflow/src')

# Import your modules
from evaluation.user_question_bias import check_bias_in_user_question
from model.retrive_azure_index import search_azure_index
from model.system_prompt import create_system_prompt
from model.get_model_response import get_openai_response
from evaluation.answer_validation import key_concept_match

# Default args
default_args = {
    'start_date': datetime(2024, 10, 25),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'response_generation_pipeline',
    default_args=default_args,
    description='DAG for processing user questions and generating responses and the all the steps involved',
    schedule_interval=None,
)

# 1. Check for bias in the user question
def question_bias_check(user_question, **kwargs):
    clean_question, bias_message = check_bias_in_user_question(user_question)
    kwargs['ti'].xcom_push(key='clean_question', value=clean_question)
    if bias_message:
        kwargs['ti'].xcom_push(key='bias_message', value=bias_message)
        return 'rephrase_suggestion'
    return 'retrieve_context'

question_bias_check_task = BranchPythonOperator(
    task_id='question_bias_check',
    python_callable=question_bias_check,
    op_kwargs={'user_question': '{{ dag_run.conf["user_question"] }}'},
    provide_context=True,
    dag=dag,
)

# 2. Handle bias rephrasing (if needed)
def rephrase_suggestion(**kwargs):
    bias_message = kwargs['ti'].xcom_pull(key='bias_message', task_ids='question_bias_check')
    print(f"Suggesting rephrase due to bias: {bias_message}")

rephrase_suggestion_task = PythonOperator(
    task_id='rephrase_suggestion',
    python_callable=rephrase_suggestion,
    provide_context=True,
    dag=dag,
)

# 3. Retrieve context from Azure Search
def retrieve_context(**kwargs):
    clean_question = kwargs['ti'].xcom_pull(key='clean_question', task_ids='question_bias_check')
    context = search_azure_index(clean_question)
    kwargs['ti'].xcom_push(key='context', value=context)

retrieve_context_task = PythonOperator(
    task_id='retrieve_context',
    python_callable=retrieve_context,
    provide_context=True,
    dag=dag,
)

# 4. Generate system prompt
def generate_system_prompt(**kwargs):
    context = kwargs['ti'].xcom_pull(key='context', task_ids='retrieve_context')
    clean_question = kwargs['ti'].xcom_pull(key='clean_question', task_ids='question_bias_check')
    system_prompt = create_system_prompt(context, clean_question)
    kwargs['ti'].xcom_push(key='system_prompt', value=system_prompt)

generate_system_prompt_task = PythonOperator(
    task_id='generate_system_prompt',
    python_callable=generate_system_prompt,
    provide_context=True,
    dag=dag,
)

# 5. Get response from OpenAI
def generate_response(**kwargs):
    system_prompt = kwargs['ti'].xcom_pull(key='system_prompt', task_ids='generate_system_prompt')
    answer = get_openai_response(system_prompt)
    kwargs['ti'].xcom_push(key='answer', value=answer)

generate_response_task = PythonOperator(
    task_id='generate_response',
    python_callable=generate_response,
    provide_context=True,
    dag=dag,
)

# 6. Validate answer
def answer_validation(**kwargs):
    answer = kwargs['ti'].xcom_pull(key='answer', task_ids='generate_response')
    context = kwargs['ti'].xcom_pull(key='context', task_ids='retrieve_context')
    if key_concept_match(answer, context):
        print(f"Answer is valid: {answer}")
    else:
        print("Answer lacks contextual relevance.")

answer_validation_task = PythonOperator(
    task_id='answer_validation',
    python_callable=answer_validation,
    provide_context=True,
    dag=dag,
)

# Define task dependencies
question_bias_check_task >> [rephrase_suggestion_task, retrieve_context_task]
retrieve_context_task >> generate_system_prompt_task >> generate_response_task >> answer_validation_task
