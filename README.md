# BIS Standards Recommendation Engine

An end-to-end AI-powered recommendation engine using a Retrieval-Augmented Generation (RAG) pipeline to help Indian Micro and Small Enterprises (MSEs) identify applicable Bureau of Indian Standards (BIS) regulations for their building materials.

## Features
*   **Semantic Search**: Utilizes `sentence-transformers` (`all-MiniLM-L6-v2`) to deeply understand natural language queries.
*   **Fast Retrieval**: Uses FAISS for sub-millisecond vector similarity search.
*   **Zero Hallucination**: Employs an extraction template approach to ensure 100% accuracy based *only* on the provided standard descriptions.
*   **Interactive UI**: A simple, modern Streamlit interface for easy querying.
*   **CLI Support**: A batch-processing inference script (`inference.py`) outputting structured JSON metrics.

## Setup Instructions

1.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Add Your Data**
    Create a `data/` folder in the project root and place your BIS SP 21 PDF documents inside it.

3.  **Data Ingestion & Indexing**
    Run the preprocessing script to extract text from PDFs and parse them into a structured format:
    ```bash
    python src/preprocess.py
    ```
    Next, build the embeddings and vector database:
    ```bash
    python src/embed_store.py
    ```

    *(Note: If you want to test the pipeline without actual PDFs, run `python create_mock_data.py` to generate sample standards before running `embed_store.py`)*

## Usage

### 1. Streamlit Web Interface
Launch the interactive web app to test queries manually:
```bash
streamlit run app.py
```

### 2. CLI Inference
To process a batch of queries from a JSON file:
```bash
python inference.py --input input.json --output output.json
```
**Expected Input Format (`input.json`):**
```json
[
  {
    "id": "q1",
    "query": "high strength reinforced concrete for building columns"
  }
]
```
**Output Format (`output.json`):**
```json
[
  {
    "id": "q1",
    "retrieved_standards": ["IS 456", "IS 10262"],
    "explanations": ["...rationale..."],
    "latency_seconds": 0.042
  }
]
```

## Project Structure
```
/bis_rag_engine
 ├── /src
 │   ├── preprocess.py      # PDF extraction and structing
 │   ├── embed_store.py     # Embedding generation and FAISS vector index
 │   ├── retrieve.py        # Vector search implementation
 │   └── utils.py           # Helper functions
 ├── /data                  # Place PDF documents here
 ├── inference.py           # CLI script for processing JSON queries
 ├── app.py                 # Streamlit UI
 ├── create_mock_data.py    # Test data generator
 ├── requirements.txt       # Dependencies
 └── README.md              # Instructions
```
