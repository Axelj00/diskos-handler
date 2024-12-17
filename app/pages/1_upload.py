import sys
import os
import streamlit as st
from uuid import uuid4

# Fix module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.utils.pdf_extraction import extract_text_from_pdf
from app.utils.embedding import embed_and_store_documents
from app.utils.chroma_client import get_chroma_collection
from app.config import CHROMA_DB_DIR, CHROMA_COLLECTION_NAME, EMBEDDING_MODEL, CHUNK_SIZE

st.title("📤 Upload Well Documents")

# Initialize Chroma collection
collection = get_chroma_collection(CHROMA_DB_DIR, CHROMA_COLLECTION_NAME)

# OpenAI API Key
openai_api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key.")
if not openai_api_key:
    st.info("Provide your OpenAI API key to continue.")
    st.stop()

# Well Name and PDF Upload
well_name = st.text_input("Well Name", help="Enter the name of the well, e.g., 'WELL-001'.")
uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

def split_text_into_chunks(text: str, chunk_size: int):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

if well_name and uploaded_files:
    if st.button("Process and Store"):
        with st.spinner("Processing PDFs..."):
            all_text_chunks = []
            for uploaded_file in uploaded_files:
                pdf_text = extract_text_from_pdf(uploaded_file)
                chunks = split_text_into_chunks(pdf_text, CHUNK_SIZE)
                documents = [{
                    "id": str(uuid4()),
                    "text": chunk,
                    "metadata": {"well_name": well_name, "source": uploaded_file.name}
                } for chunk in chunks]
                all_text_chunks.extend(documents)
            
            embed_and_store_documents(collection, all_text_chunks, openai_api_key, EMBEDDING_MODEL)
            st.success("Documents successfully stored!")
