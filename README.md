# BIS Standards Recommendation Engine

An end-to-end AI-powered recommendation engine using a Retrieval-Augmented Generation (RAG) pipeline to help Indian Micro and Small Enterprises (MSEs) identify applicable Bureau of Indian Standards (BIS) regulations for their building materials.

## Features
*   **Semantic Search**: Utilizes `sentence-transformers` (`all-MiniLM-L6-v2`) to deeply understand natural language queries.
*   **Fast Retrieval**: Uses FAISS for sub-millisecond vector similarity search.
*   **Zero Hallucination**: Employs an exact extraction template approach to ensure 100% accuracy based *only* on the provided official BIS dataset.
*   **Premium Web UI**: A blazing-fast FastAPI backend serving a custom HTML/CSS/JS frontend featuring Voice Search and PDF Compliance Report Generation.
*   **CLI Support**: A batch-processing inference script (`inference.py`) outputting structured JSON metrics for evaluation.

## Setup Instructions

1.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Dataset**
    The official `dataset.pdf` is located in the `data/` folder. The vector database (`standards.index`) has already been built and is included in this repository.

*(Optional) To rebuild the index from scratch:*
```bash
python src/preprocess.py
python src/embed_store.py
```

## Usage

### 1. Web Application (Premium UI)
Launch the interactive web app to test queries manually using Voice Search:
```bash
python -m uvicorn app:app
```
Then navigate your browser to `http://127.0.0.1:8000`.

### 2. Hackathon Evaluation
To process the official `public_test_set.json` and generate predictions:
```bash
python inference.py --input public_test_set.json --output predictions.json
```

To run the mandatory grading script:
```bash
python eval_script.py --results predictions.json
```

## Project Structure
```
/bis_rag_engine
 ├── /src
 │   ├── preprocess.py      # PDF extraction and chunking using regex
 │   ├── embed_store.py     # Embedding generation and FAISS vector index
 │   └── retrieve.py        # Vector search implementation
 ├── /static                # Custom Frontend UI files
 │   ├── index.html
 │   ├── style.css
 │   └── app.js
 ├── /data                  # Source PDF documents
 ├── inference.py           # CLI script for processing JSON queries
 ├── eval_script.py         # Official Hackathon Evaluation script
 ├── app.py                 # FastAPI backend server
 ├── presentation_deck.md   # Presentation Slide Deck Draft
 ├── requirements.txt       # Dependencies
 └── README.md              # Instructions
```
