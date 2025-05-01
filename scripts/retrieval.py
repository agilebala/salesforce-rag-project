import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient, exceptions
from utils.embedding import get_embedding

load_dotenv()

COSMOSDB_ENDPOINT = os.getenv("AZURE_COSMOSDB_ENDPOINT")
COSMOSDB_KEY = os.getenv("AZURE_COSMOSDB_KEY")
DATABASE_NAME = os.getenv("AZURE_COSMOSDB_DATABASE_NAME")
CONTAINER_NAME = os.getenv("AZURE_COSMOSDB_CONTAINER_NAME")

client = CosmosClient(COSMOSDB_ENDPOINT, COSMOSDB_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

def retrieve_top_k(query, top_k=3):
    query_embedding = get_embedding(query)

    # Debugging: Check the embedding format
    print("🔍 DEBUG: Entered retrieve_top_k()")
    print(f"🔹 Embedding type: {type(query_embedding)}")
    print(f"🔹 Embedding length: {len(query_embedding)}")
    print(f"🔹 First 3 values: {query_embedding[:3]}")

    # Ensure embedding is a flat list and has correct dimensions
    if isinstance(query_embedding, list) and len(query_embedding) == 1536:
        print("🔹 Embedding is valid.")
    else:
        print("❌ Invalid embedding format!")
        return []

    # Build the Cosmos DB query
    query_text = """
        SELECT TOP @k c.text, c.source
        FROM c
        WHERE VectorDistance(c.embedding, @embedding) < @threshold
    """
    query_parameters = [
        {"name": "@k", "value": top_k},
        {"name": "@embedding", "value": tuple(query_embedding)},
        {"name": "@threshold", "value": 0.8}  # Threshold for similarity
    ]

    print("🔹 Cosmos DB Query Text:", query_text)
    print("🔹 Cosmos DB Query Parameters:", query_parameters)

    try:
        print("🟢 Executing Cosmos DB vector query...")
        results = list(container.query_items(
            query=query_text,
            parameters=query_parameters,
            enable_cross_partition_query=True
        ))
        print(f"✅ Retrieved {len(results)} results.")
        return results
    except Exception as e:
        print("❌ ERROR during Cosmos DB retrieval:", str(e))
        return []