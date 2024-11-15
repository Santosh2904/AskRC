import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Append the absolute path to src directory
sys.path.append('/opt/airflow/src')

from evaluation.user_question_bias import check_bias_in_user_question
from evaluation.answer_validation import validate_answer
from model import search_azure_index, create_system_prompt, get_openai_response

# Define Airflow DAG
default_args = {'start_date': datetime(2024, 10, 25)}
dag = DAG('askrc_pipeline', default_args=default_args, schedule_interval=None)

# 1. Check for bias in the user question
def question_bias_check(**kwargs):
    user_question = kwargs['user_question']
    clean_question, bias_message = check_bias_in_user_question(user_question)
    if bias_message:
        return 'rephrase_suggestion'
    else:
        return 'retrieve_context'

# 2. Retrieve context from Azure Search
def retrieve_context(**kwargs):
    user_question = kwargs['user_question']
    return search_azure_index(user_question)

# 3. Generate system prompt for OpenAI
def generate_system_prompt(**kwargs):
    context = kwargs['context']
    user_question = kwargs['user_question']
    return create_system_prompt(context, user_question)

# 4. Get response from OpenAI
def generate_response(**kwargs):
    system_prompt = kwargs['system_prompt']
    return get_openai_response(system_prompt)

# 5. Validate answer using key concept matching
def answer_validation(**kwargs):
    answer = kwargs['answer']
    context = kwargs['context']
    return validate_answer(answer, context)

# Define Airflow tasks
question_bias_check_task = PythonOperator(
    task_id='question_bias_check',
    python_callable=question_bias_check,
    op_kwargs={'user_question': '{{ dag_run.conf["user_question"] }}'},
    provide_context=True,
    dag=dag,
)

retrieve_context_task = PythonOperator(
    task_id='retrieve_context',
    python_callable=retrieve_context,
    provide_context=True,
    dag=dag,
)

generate_system_prompt_task = PythonOperator(
    task_id='generate_system_prompt',
    python_callable=generate_system_prompt,
    provide_context=True,
    dag=dag,
)

generate_response_task = PythonOperator(
    task_id='generate_response',
    python_callable=generate_response,
    provide_context=True,
    dag=dag,
)

answer_validation_task = PythonOperator(
    task_id='answer_validation',
    python_callable=answer_validation,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
question_bias_check_task >> retrieve_context_task >> generate_system_prompt_task >> generate_response_task >> answer_validation_task
