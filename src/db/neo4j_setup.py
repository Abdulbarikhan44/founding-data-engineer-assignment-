from neo4j import GraphDatabase
from utils.config import NEO4J_URI

driver = GraphDatabase.driver(NEO4J_URI, auth=("neo4j", "password"))

def create_relation(user_id, campaign):
    with driver.session() as session:
        session.run("""
        MERGE (u:User {id: $user})
        MERGE (c:Campaign {id: $camp})
        MERGE (u)-[:ENGAGED_WITH]->(c)
        """, user=user_id, camp=campaign)

# forgot to close driver here
