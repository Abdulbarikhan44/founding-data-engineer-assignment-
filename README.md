# founding-data-engineer-assignment-
Design and Implement a Scalable Multi-Database Data Platform for AI-Driven Marketing Personalization

## Used
- Python
- MongoDB
- Neo4j
- SQLite
- FastAPI
- Sentence Transformers

## How to Run
1. Start databases (docker-compose optional)
2. Run pipeline:
   python src/pipeline/run_pipeline.py
3. Start API:
   uvicorn src.api.app:app --reload
