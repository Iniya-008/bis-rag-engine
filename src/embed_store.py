import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

MODEL_NAME = 'all-MiniLM-L6-v2'

def load_standards(json_path):
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return []
    with open(json_path, 'r') as f:
        return json.load(f)

def create_embeddings(standards):
    model = SentenceTransformer(MODEL_NAME)
    
    texts_to_embed = []
    for std in standards:
        # Combine title and description for better semantic capture
        text = f"{std['title']}. {std['description']}"
        texts_to_embed.append(text)
    
    print(f"Generating embeddings using {MODEL_NAME}...")
    embeddings = model.encode(texts_to_embed, show_progress_bar=True)
    return embeddings, model

def build_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    # Use L2 distance for similarity search
    index = faiss.IndexFlatL2(dimension)
    
    index.add(np.array(embeddings).astype('float32'))
    print(f"Index built with {index.ntotal} vectors of dimension {dimension}.")
    return index

def save_index_and_metadata(index, standards, index_path, meta_path):
    faiss.write_index(index, index_path)
    with open(meta_path, 'w') as f:
        json.dump(standards, f, indent=4)
    print("FAISS index and metadata successfully saved to disk.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    json_path = os.path.join(base_dir, "parsed_standards.json")
    index_path = os.path.join(base_dir, "standards.index")
    meta_path = os.path.join(base_dir, "metadata.json")
    
    standards = load_standards(json_path)
    if standards:
        embeddings, _ = create_embeddings(standards)
        index = build_faiss_index(embeddings)
        save_index_and_metadata(index, standards, index_path, meta_path)
    else:
        print("No standards to process. Please run preprocess.py first.")
