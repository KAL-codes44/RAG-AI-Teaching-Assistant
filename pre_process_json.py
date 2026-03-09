import requests
import os
import json
import pandas as pd
import joblib
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL_NAME = "bge-m3"
MAX_WORKERS = 8  # Parallel threads for embedding requests

def create_embedding_single(text):
    """Create embedding for a single text with error handling."""
    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": text},
            timeout=60
        )
        r.raise_for_status()
        response = r.json()

        if "embedding" not in response:
            print(f"Unexpected response: {response}")
            return None

        return response["embedding"]

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Parsing error: {e} | Response: {r.text[:200]}")
        return None


def create_embeddings_parallel(texts, max_workers=MAX_WORKERS):
    """Create embeddings for multiple texts using parallel requests."""
    embeddings = [None] * len(texts)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {
            executor.submit(create_embedding_single, text): i
            for i, text in enumerate(texts)
        }

        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                embeddings[idx] = future.result()
            except Exception as e:
                print(f"Error at index {idx}: {e}")
                embeddings[idx] = None

    return embeddings



jsons = os.listdir("jsons")
my_dict = []
chunk_id = 0

for json_file in tqdm(jsons, desc="Processing files"):
    with open(f"jsons/{json_file}", "r", encoding="utf-8") as f:
        content = json.load(f)

    texts = [c["text"] for c in content["chunks"]]

    print(f"\nCreating {len(texts)} embeddings for: {json_file}")
    embeddings = create_embeddings_parallel(texts)

    for i, chunk in enumerate(content["chunks"]):
        if embeddings[i] is None:
            print(f" Skipping chunk {i} in {json_file} — embedding failed")
            continue

        chunk["chunk_id"] = chunk_id
        chunk["embedding"] = embeddings[i]
        chunk_id += 1
        my_dict.append(chunk)

# Save
df = pd.DataFrame.from_records(my_dict)
joblib.dump(df, "embeddings.joblib")
print(f"\n Done! Saved {len(df)} chunks to embeddings.joblib")