from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# IMPORT PYTHON SCRIPT WITH FUNCTIONS
from python_scripts import scada_data_processing

def get_scada_data(ti):

    # call function
    target_filename = scada_data_processing.get_raw_data_from_scada_table(past_days=1)
    ti.xcom_push(key='s3_filename', value=target_filename)

def process_and_analyze_scada_data(ti):
    task_filename=ti.xcom_pull(key='s3_filename', task_ids='extract_target_data')
    cleaned_data = scada_data_processing.process_raw_data(task_filename)

# Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG('scada_events_processing',
         start_date=datetime(2021, 1, 1),
         max_active_runs=2,
         schedule_interval=timedelta(minutes=30),
         default_args=default_args,
         catchup=False
         ) as dag:

    extract_target_data = PythonOperator(
        task_id = 'extract_target_data',
        python_callable=get_scada_data,
        #op_kwargs={'state':state}
    )

    process_target_scada_data = PythonOperator(
        task_id = 'process_target_scada_data',
        python_callable=process_and_analyze_scada_data,
                #op_kwargs={'state':state}
    )

    extract_target_data >> process_target_scada_data