from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import csv

from db.mongo_setup import insert_conversation
from pipeline.analytics_job import update_metrics
from utils.redis_client import cache_user_message

default_args = {
    "owner": "airflow",
    "retries": 1
}

dag = DAG(
    dag_id="simple_conversation_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,  # manual trigger
    catchup=False
)

def read_and_store():
    with open("data/conversations.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            doc = {
                "user_id": row["user_id"],
                "message": row["message"],
                "timestamp": row["timestamp"]
            }

            insert_conversation(doc)
            cache_user_message(row["user_id"], row["message"])

            # print("Inserted row")  # debug left here

def update_analytics_task():
    with open("data/conversations.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            update_metrics(row["user_id"], row["campaign"])

def finish_task():
    print("Pipeline finished")

read_store = PythonOperator(
    task_id="read_and_store_data",
    python_callable=read_and_store,
    dag=dag
)

analytics = PythonOperator(
    task_id="update_analytics",
    python_callable=update_analytics_task,
    dag=dag
)

finish = PythonOperator(
    task_id="finish",
    python_callable=finish_task,
    dag=dag
)

read_store >> analytics >> finish
