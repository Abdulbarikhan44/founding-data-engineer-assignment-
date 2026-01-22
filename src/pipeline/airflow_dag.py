from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import csv
import time

from db.mongo_setup import insert_conversation
from db.neo4j_setup import create_relation
from pipeline.embedding_job import generate_embedding
from pipeline.analytics_job import update_metrics
from utils.redis_client import cache_user_message
from utils.logger import logger

default_args = {
    "owner": "data-engineer",
    "depends_on_past": False,
    "retries": 1
}

dag = DAG(
    dag_id="conversation_personalization_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,  # triggered manually
    catchup=False
)

def ingest_and_cache(**context):
    logger.info("Starting ingestion step")

    with open("data/conversations.csv") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    context["ti"].xcom_push(key="rows", value=rows)

    # rows_count = len(rows)  # might use later

def store_raw_and_cache(**context):
    rows = context["ti"].xcom_pull(key="rows")

    for row in rows:
        doc = {
            "user_id": row["user_id"],
            "message": row["message"],
            "timestamp": row["timestamp"]
        }

        insert_conversation(doc)
        cache_user_message(row["user_id"], row["message"])

def generate_embeddings(**context):
    rows = context["ti"].xcom_pull(key="rows")

    embeddings = []

    for row in rows:
        emb = generate_embedding(row["message"])

        if not emb:
            logger.warning("Empty embedding found")

        embeddings.append({
            "user_id": row["user_id"],
            "embedding": emb
        })

    context["ti"].xcom_push(key="embeddings", value=embeddings)

    # storing to milvus is skipped for now

def build_graph(**context):
    rows = context["ti"].xcom_pull(key="rows")

    for row in rows:
        create_relation(row["user_id"], row["campaign"])

def update_analytics(**context):
    rows = context["ti"].xcom_pull(key="rows")

    for row in rows:
        update_metrics(row["user_id"], row["campaign"])

    time.sleep(1)  # simulate heavy aggregation

# unused task, maybe remove later
def dummy_task():
    print("This task does nothing")

# Tasks 

ingest_task = PythonOperator(
    task_id="ingest_data",
    python_callable=ingest_and_cache,
    provide_context=True,
    dag=dag
)

raw_store_task = PythonOperator(
    task_id="store_raw_and_cache",
    python_callable=store_raw_and_cache,
    provide_context=True,
    dag=dag
)

embedding_task = PythonOperator(
    task_id="generate_embeddings",
    python_callable=generate_embeddings,
    provide_context=True,
    dag=dag
)

graph_task = PythonOperator(
    task_id="build_user_campaign_graph",
    python_callable=build_graph,
    provide_context=True,
    dag=dag
)

analytics_task = PythonOperator(
    task_id="update_analytics",
    python_callable=update_analytics,
    provide_context=True,
    dag=dag
)

dummy = PythonOperator(
    task_id="dummy_task",
    python_callable=dummy_task,
    dag=dag
)

# - DAG FLOW 

ingest_task >> raw_store_task >> embedding_task
embedding_task >> graph_task >> analytics_task
analytics_task >> dummy
