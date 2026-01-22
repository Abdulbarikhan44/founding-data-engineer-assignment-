import csv
import time
from utils.logger import logger
from db.mongo_setup import insert_conversation
from db.neo4j_setup import create_relation
from pipeline.embedding_job import generate_embedding
from pipeline.analytics_job import update_metrics

def run():
    start = time.time()
    logger.info("Pipeline started")

    with open("data/conversations.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            doc = {
                "user_id": row["user_id"],
                "message": row["message"],
                "timestamp": row["timestamp"]
            }

            insert_conversation(doc)
            create_relation(row["user_id"], row["campaign"])
            emb = generate_embedding(row["message"])
            update_metrics(row["user_id"], row["campaign"])

            # storing embedding in milvus is skipped here
            # TODO: integrate milvus properly

    logger.info("Pipeline finished in %s sec", time.time() - start)

if __name__ == "__main__":
    run()
