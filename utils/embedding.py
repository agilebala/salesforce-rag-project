import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

if not api_key or not endpoint:
    raise ValueError("AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT is not set in .env.")

client = AzureOpenAI(
    api_key=api_key,
    api_version="2023-05-15",
    azure_endpoint=endpoint
)

def get_embedding(text: str):
    try:
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=[text]
        )
        #embedding = response.data[0].embedding
        #print("Embedding Element Type:", type(embedding[0]))
        return response.data[0].embedding
        #return embedding
    except Exception as e:
        print(f"❌ Embedding generation failed: {e}")
        return []

def generate_answer(query: str, context_chunks: list):
    context = "\n\n".join(chunk["text"] for chunk in context_chunks)
    prompt = f"Answer the question based on the context below.\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"

    try:
        response = client.chat.completions.create(
            model="gpt-35-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for summarizing Salesforce earnings call transcripts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Answer generation failed: {e}")
        return "Error: Unable to generate answer."

