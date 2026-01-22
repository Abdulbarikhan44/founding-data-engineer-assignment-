## High Level Flow

ingest_data
   ↓
store_raw_and_cache (MongoDB + Redis)
   ↓
generate_embeddings
   ↓
build_user_campaign_graph (Neo4j)
   ↓
update_analytics (SQLite / BigQuery)
