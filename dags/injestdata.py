from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_argument = {
    'owner': 'fabianbryant',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}


with DAG(
    dag_id = 'stockapi',
    default_args=default_argument,
    start_date=datetime(2025,3,17,12,0),
    schedule_interval='0 0 * * *',
    catchup=False,
    is_paused_upon_creation=False,
) as dag:
    task1 = BashOperator(
        task_id='gcs_bucketstream',
        bash_command="""
        export JAVA_HOME=/spark/jdk-11.0.2 && 
        python /opt/airflow/main/datainjest_gcsbucket.py
        """
    )
    task2 = BashOperator(
        task_id='gcs_bigquerystream',
        bash_command="""
        source /opt/airflow/google-cloud-sdk/path.bash.inc
        source /opt/airflow/google-cloud-sdk/completion.bash.inc
        gcloud dataproc jobs submit pyspark --cluster=dezoomcamp-project2025-dataproc --region=us-central1 /opt/airflow/main/datainjest_bigquery.py
        """
    )

task1 >> task2