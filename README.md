 RAG Project Azure OpenAI + CosmosDB System**

This project implements a Retrieval-Augmented Generation (RAG) system for analyzing Salesforce's quarterly earnings call transcripts. 
It provides Question & Answer and summarization capabilities through a conversational user interface, optimized for processing local `.txt` files.

**Technology Stack****

LLM:** Azure OpenAI (using `gpt-35-turbo` for generation and `text-embedding-ada-002` for embeddings)
Vector Database:** Azure Cosmos DB for NoSQL with integrated vector search
Conversational UI:** Streamlit

**Prerequisites**

1.  Azure Subscription: You need an active Azure subscription.
2.  Azure OpenAI Service:
    * Access to Azure OpenAI service needs to be requested and approved.
    * Deploy the following models:
        * `text-embedding-ada-002`
        * `gpt-35-turbo`
    * Note down your Azure OpenAI endpoint and API key.
3.  Azure Cosmos DB for NoSQL:**
    * Create an Azure Cosmos DB account with the NoSQL API.
    * Create a database named `rag_db` (or as specified in `.env`).
    * Create a container named `salesforce_earnings` (or as specified in `.env`). Ensure that the vector search capability is enabled for this container. You'll need to define a vector indexing policy. A basic policy can be set up through the Azure Portal when creating the container or later. For example, you can start with a `flat` index type and cosine similarity.
    * Note down your Azure Cosmos DB endpoint and primary key.
4.  Python Environment:** Ensure you have Python 3.9 or later installed.
5.  pip:** Python package installer.
6.  Salesforce Earnings Call Transcripts:** Downloaded and saved as individual `.txt` files in a local folder.

**Create a New Conda Environment with a Specific Python Version:**

Create a new conda environment and specify which version of Python you want to use (for example, Python 3.10).
conda create -n rag-env python=3.10
This command will create a new environment named rag-env with Python 3.10.


**Activate the New Environment:**

conda activate rag-env

**Install the Required Packages:**

conda install -c conda-forge streamlit
conda install -c conda-forge openai
conda install -c conda-forge azure-cosmos
conda install python-dotenv
These commands will install the following:

Streamlit for the app interface

OpenAI for interacting with the OpenAI API

Azure Cosmos SDK to interact with Azure Cosmos DB

python-dotenv for loading environment variables from a .env file

**File Descriptions: **

data/: Contains the Salesforce transcript .txt files.
utils/chunking.py: Splits large transcripts into smaller chunks.
utils/embedding.py: Generates embeddings using Azure OpenAI.
ingest.py: Main script to process transcripts and upload to Cosmos DB.
.env: Stores sensitive environment variables.
requirements.txt: Lists Python dependencies.

salesforce-rag-project/
├── app.py
├── ingest.py
├── scripts/
│   └── retrieval.py
├── utils/
│   ├── chunking.py
│   └── embedding.py
├── data/
│   └── .txt ...
├── .env
├── requirements.txt
└── README.md

Setup Instructions

1.  Clone the Repository -   mkdir salesforce-rag-azure
    cd salesforce-rag-azure
    mkdir data scripts utils
    ```
2.  Install Dependencies:
       All dependency files are available in requirements.txt.
    
3.  Place Transcript Files: Place earnings call transcript files (in `.txt` format) into the `data/` directory. 

    
4.  Configure Environment Variables:
    * Create a `.env` file in the same directory as the Python script.
    * Add your Azure OpenAI and Cosmos DB credentials to the `.env` file. Replace the placeholder values with your actual endpoint and key:
        ```
        AZURE_OPENAI_API_KEY=""
        AZURE_OPENAI_ENDPOINT=""
        AZURE_OPENAI_EMBEDDING_DEPLOYMENT=""
        AZURE_OPENAI_COMPLETION_DEPLOYMENT=""

        AZURE_COSMOSDB_ENDPOINT=""
        AZURE_COSMOSDB_KEY=""
        AZURE_COSMOSDB_DATABASE_NAME=""
        AZURE_COSMOSDB_CONTAINER_NAME=""
        AZURE_COSMOSDB_INDEX_NAME="" 
        ```
        **Note:** Keep your API keys and credentials secure. Do not share them publicly.
Running the Application

Ingesting and Indexing Data

Run the `ingest.py` script to process the transcripts, generate embeddings, and store them in Azure Cosmos DB.
This script will:
	•	Load the transcript files from the data/ directory.
	•	Chunk the transcripts into smaller pieces.
	•	Generate embeddings for each chunk using the specified Azure OpenAI embedding deployment.
	•	Connect to your Azure Cosmos DB database and container.
	•	Create the container and a vector search index if they don't exist.
	•	Store the chunks, their embeddings, and metadata (source filename) in the Cosmos DB container.
 This script orchestrates the process of reading, chunking, embedding, and storing the transcript data in Azure Cosmos DB.

5.  Running the Conversational UI:
    This script builds a Q&A web app using Streamlit for analyzing Salesforce earnings call transcripts. It uses RAG (Retrieval-Augmented Generation)	
    Run the Streamlit Application: Navigate to the project directory in your terminal and run:
    ```bash
    streamlit run app.py
    ```
 This will open the conversational UI in your web browser.
 **utils/chunking.py**
 This file contains the chunk_transcripts function, which is responsible for splitting the raw text transcripts into smaller, manageable chunks.
 **utils/embedding.py**
 This file contains the get_embedding function, which uses the Azure OpenAI API to generate embeddings for text.
 **scripts/retrieval.py**
 This script defines the logic to query Azure Cosmos DB for relevant document chunks based on a user's query.
 
 Example Questions

"When was the most recent earnings call?"
"What are the risks that Salesforce has faced, and how have they changed over time?"
"Can you summarize Salesforce's strategy at the beginning of 2023?"
"How many earnings call documents do you have indexed?"
"How many pages are in the most recent earnings call?" (Note: Page counting is not directly supported for `.txt` files in this implementation.)

**Scalability for Larger Datasets**

The current system provides a basic scalable architecture. Here's how it can be scaled for larger datasets:

1.  Azure Cosmos DB:
    * Horizontal Scaling: Cosmos DB is inherently horizontally scalable. As the number of transcripts and the size of the embeddings grow, Cosmos DB can automatically partition your data across multiple servers, providing virtually unlimited storage and throughput. You can monitor the Request Units (RUs) consumed and scale them up as needed.
    * Vector Indexing: For larger datasets, ensure you have an efficient vector indexing policy in Cosmos DB. Consider using more advanced indexing techniques (beyond `flat`) if query latency becomes an issue with a very large number of vectors. Explore options like Hierarchical Navigable Small World (HNSW) indexing for faster and more efficient similarity searches.
    * Partitioning Strategy: Choose a good partition key for your Cosmos DB container. While the current `id` might work for a small dataset, for a larger scale, consider partitioning based on a higher-level attribute like the source document name or a timestamp to distribute the data more evenly.

2.  Azure OpenAI Embeddings:**
    * Batch Processing:** For a large number of files, process the embedding generation in batches to optimize API calls and reduce costs. The current code processes files sequentially. You could implement parallel processing or asynchronous operations for faster embedding generation.
    * More Powerful Embedding Models:** As the dataset
