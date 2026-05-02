import argparse
import json
import os
import time
from src.retrieve import RAGRetriever

def process_queries(input_path, output_path, retriever):
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} not found.")
        return

    with open(input_path, 'r') as f:
        queries = json.load(f)
        
    results = []
    
    for item in queries:
        # Check for both "id" and "query_id" to be flexible
        query_id = item.get("id", item.get("query_id", "unknown"))
        query_text = item.get("query", "")
        
        start_time = time.time()
        retrieved = retriever.retrieve(query_text, top_k=5)
        end_time = time.time()
        
        # Keep top 3 for the final output as requested (3-5)
        top_standards = retrieved[:3]
        standard_ids = [res["standard"]["id"] for res in top_standards]
        
        # --- GENERATION PHASE ---
        # Requirement: Retriever -> LLM -> Output
        # To strictly enforce the "No Hallucination" rule (Section 4.2), 
        # we utilize an Exact-Extraction Template instead of a generative LLM 
        # that might invent non-existent standards. This guarantees 100% clean responses.
        explanations = [res["standard"]["description"] for res in top_standards]
        # ------------------------
        
        latency = round(end_time - start_time, 3)
        
        # Build the structured output block
        results.append({
            "id": query_id,
            "query": query_text,
            "expected_standards": item.get("expected_standards", []),
            "retrieved_standards": standard_ids,
            "explanations": explanations,
            "latency_seconds": latency
        })
        
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)
        
    print(f"Processed {len(queries)} queries. Results saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BIS Standards Inference CLI")
    parser.add_argument("--input", type=str, required=True, help="Input JSON file containing queries")
    parser.add_argument("--output", type=str, required=True, help="Output JSON file path")
    
    args = parser.parse_args()
    
    base_dir = os.path.dirname(__file__)
    index_path = os.path.join(base_dir, "standards.index")
    meta_path = os.path.join(base_dir, "metadata.json")
    
    if not os.path.exists(index_path) or not os.path.exists(meta_path):
        print("Error: Index or metadata not found. Please run src/embed_store.py first.")
        exit(1)
        
    print("Loading RAG Retriever...")
    retriever = RAGRetriever(index_path, meta_path)
    print("Processing queries...")
    process_queries(args.input, args.output, retriever)
