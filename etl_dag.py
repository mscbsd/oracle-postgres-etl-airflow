from __future__ import annotations

import datetime
import os

import pendulum

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.retries import RetryOptions
import dags.etl_script as etl_script # Importa o script Python

default_args = {
    'owner': 'airflow',
    'start_date': pendulum.datetime(2024, 1, 1, tz="UTC"),
    'retries': 3,  # Número de retentativas
    'retry_delay': datetime.timedelta(minutes=5), # Intervalo entre as retentativas
    'retry_exponential_backoff': True, # Backoff exponencial para as retentativas
    'max_retry_delay': datetime.timedelta(minutes=30), # Tempo máximo de espera entre retentativas
}

with DAG(
    dag_id="etl_oracle_postgres",
    schedule="@daily",
    default_args=default_args,
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["etl", "oracle", "postgres"],
) as dag:
    extract_task = PythonOperator(
        task_id="extract_oracle",
        python_callable=etl_script.extract_data_oracle,
        op_kwargs={"oracle_conn_string": os.environ.get("ORACLE_CONN_STRING")},
        provide_context=True,
        dag=dag,
        retry_options=RetryOptions(delay=datetime.timedelta(minutes=2), tries=3, exponential_backoff=True, max_delay=datetime.timedelta(minutes=10))
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=etl_script.transform_data,
        op_kwargs={"df": "{{ ti.xcom_pull(task_ids='extract_oracle') }}"},
        provide_context=True,
        dag=dag,
        retry_options=RetryOptions(delay=datetime.timedelta(minutes=2), tries=3, exponential_backoff=True, max_delay=datetime.timedelta(minutes=10))
    )

    load_task = PythonOperator(
        task_id="load_postgres",
        python_callable=etl_script.load_data_postgres,
        op_kwargs={"df": "{{ ti.xcom_pull(task_ids='transform_data') }}", "postgres_conn_string": os.environ.get("POSTGRES_CONN_STRING")},
        provide_context=True,
        dag=dag,
        retry_options=RetryOptions(delay=datetime.timedelta(minutes=2), tries=3, exponential_backoff=True, max_delay=datetime.timedelta(minutes=10))
    )

    extract_task >> transform_task >> load_task