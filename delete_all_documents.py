import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient

# Load environment variables from .env
load_dotenv()

COSMOSDB_ENDPOINT = os.getenv("AZURE_COSMOSDB_ENDPOINT")
COSMOSDB_KEY = os.getenv("AZURE_COSMOSDB_KEY")
DATABASE_NAME = os.getenv("AZURE_COSMOSDB_DATABASE_NAME")
CONTAINER_NAME = os.getenv("AZURE_COSMOSDB_CONTAINER_NAME")

# Initialize Cosmos client
client = CosmosClient(COSMOSDB_ENDPOINT, COSMOSDB_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

def delete_all_documents():
    print(f"🔍 Deleting all documents from container: {CONTAINER_NAME}")

    count = 0
    for item in container.read_all_items():
        container.delete_item(item=item['id'], partition_key=item['source'])
        count += 1

    print(f"✅ Deleted {count} documents from container.")

if __name__ == "__main__":
    delete_all_documents()
