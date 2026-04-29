import streamlit as st
import os
import time
from src.retrieve import RAGRetriever

st.set_page_config(
    page_title="BIS Standards Engine", 
    page_icon="🏛️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a premium look
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .main-header {
        font-family: 'Inter', sans-serif;
        background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .sub-header {
        font-family: 'Inter', sans-serif;
        color: #A0AEC0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .result-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(255, 65, 108, 0.15);
        border: 1px solid rgba(255, 65, 108, 0.3);
    }
    .std-id {
        color: #FF416C;
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .std-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #E2E8F0;
        margin-bottom: 12px;
    }
    .std-desc {
        color: #CBD5E0;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    .metrics-pill {
        display: inline-block;
        background: rgba(255, 65, 108, 0.1);
        color: #FF416C;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 12px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_retriever():
    base_dir = os.path.dirname(__file__)
    index_path = os.path.join(base_dir, "standards.index")
    meta_path = os.path.join(base_dir, "metadata.json")
    
    if os.path.exists(index_path) and os.path.exists(meta_path):
        return RAGRetriever(index_path, meta_path)
    return None

# Sidebar for Context & Architecture
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/f/fa/Bureau_of_Indian_Standards_Logo.svg/1200px-Bureau_of_Indian_Standards_Logo.svg.png", width=100)
    st.markdown("### 🏛️ MSE Compliance Portal")
    st.markdown("Empowering Indian Micro & Small Enterprises to instantly discover mandatory BIS regulations.")
    
    st.markdown("---")
    st.markdown("#### System Architecture (RAG)")
    st.markdown("""
    1. **Ingestion**: PDF Parsing (BIS SP 21)
    2. **Chunking**: 1 Standard = 1 Semantic Chunk
    3. **Embedding**: `all-MiniLM-L6-v2`
    4. **Vector Store**: FAISS (L2 Distance)
    5. **Retrieval**: Top-K Cosine Similarity
    6. **Generation**: Direct Extraction (Zero Hallucination)
    """)
    st.markdown("---")
    st.caption("Built for Hackathon Track: AI / RAG")

st.markdown('<div class="main-header">BIS Standards Recommendation Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Standard Discovery for Building Materials</div>', unsafe_allow_html=True)

retriever = load_retriever()

if retriever is None:
    st.error("System offline. Please build the FAISS index first (`py src/embed_store.py`).")
else:
    # Main search interface
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("", placeholder="Describe your product (e.g., 'high strength steel bars for concrete')")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True) # alignment hack
        search_btn = st.button("🔍 Find Standards", use_container_width=True, type="primary")

    if search_btn and query:
        start_time = time.time()
        with st.spinner("Scanning BIS Database via Vector Search..."):
            results = retriever.retrieve(query, top_k=3)
        end_time = time.time()
        
        latency = end_time - start_time
        
        if results:
            st.success(f"⚡ Retrieved top {len(results)} matches in {latency:.3f} seconds.")
            
            for res in results:
                std = res["standard"]
                # Convert distance to a pseudo-confidence score for UI
                # L2 distance: lower is better. 
                confidence = max(0, 100 - (res['distance'] * 50)) 
                
                st.markdown(f"""
                <div class="result-card">
                    <div class="std-id">{std['id']}</div>
                    <div class="std-title">{std['title']}</div>
                    <div class="std-desc"><strong>Rationale:</strong> {std['description']}</div>
                    <div class="metrics-pill">Match Confidence: ~{confidence:.1f}%</div>
                    <div class="metrics-pill" style="margin-left: 8px;">L2 Dist: {res['distance']:.3f}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No highly relevant standards found for this query.")
