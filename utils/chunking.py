import os

def chunk_transcripts(data_folder, chunk_size=1000):
    """
    Reads and chunks the transcript files from the provided directory.

    Args:
        data_folder (str): The directory where .txt files are located.

    Returns:
        List of dictionaries containing the 'source' and 'text' of each chunk.
    """
    docs = []

    for filename in os.listdir(data_folder):
        if filename.endswith(".txt"):
            path = os.path.join(data_folder, filename)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
                for chunk in chunks:
                    docs.append({
                        "source": filename,
                        "text": chunk.strip()
                    })

    return docs

