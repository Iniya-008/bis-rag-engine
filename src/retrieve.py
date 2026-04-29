import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = 'all-MiniLM-L6-v2'

class RAGRetriever:
    def __init__(self, index_path, meta_path):
        """
        Initializes the retriever by loading the FAISS index and metadata.
        """
        self.model = SentenceTransformer(MODEL_NAME)
        self.index = faiss.read_index(index_path)
        with open(meta_path, 'r') as f:
            self.metadata = json.load(f)
            
    def retrieve(self, query, top_k=5):
        """
        Retrieves the top_k most similar standards for a given query.
        """
        # Encode the query
        query_embedding = self.model.encode([query])
        
        # Search the FAISS index
        D, I = self.index.search(np.array(query_embedding).astype('float32'), top_k)
        
        results = []
        for idx, distance in zip(I[0], D[0]):
            if idx != -1 and idx < len(self.metadata):
                results.append({
                    "standard": self.metadata[idx],
                    "distance": float(distance)
                })
        return results
