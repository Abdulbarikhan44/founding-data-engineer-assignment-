## High Level Flow

Raw Chat from Users (csv file)
   |
   v
Ingestion Script (build pipline using Python)
   |
   |--> MongoDB (uisng pymongo library) 
   |--> Redis (recent session cache: REDIS_TTL = 60)
   |
   v
Embedding Generator (using sentence_transformers library)
   |
   |--> Milvus (vector embeddingsTODO: integrate milvus properly)
   |
   v
Relationship Builder
   |
   |--> Neo4j (User-Campaign-Intent graph using GraphDatabase)
   |
   v
Batch Aggregation Job
   |
   |--> SQLite (analytics metrics)
END
