import sys
import os
import streamlit as st

# Fix module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.utils.chroma_client import get_chroma_collection, query_chroma
from app.utils.openai_helpers import get_answer_from_openai
from app.config import CHROMA_DB_DIR, CHROMA_COLLECTION_NAME, CHAT_MODEL

st.title("🔍 Query Well Information")

# Initialize Chroma collection
collection = get_chroma_collection(CHROMA_DB_DIR, CHROMA_COLLECTION_NAME)

# OpenAI API Key
openai_api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key.")
if not openai_api_key:
    st.info("Provide your OpenAI API key to continue.")
    st.stop()

# Retrieve unique well names
def get_unique_wells(collection):
    metadata = collection.get(include=["metadata"])
    return sorted(set(m["well_name"] for m in metadata["metadatas"] if "well_name" in m))

wells = get_unique_wells(collection)
selected_well = st.selectbox("Select a Well", wells) if wells else st.info("No wells available. Upload data first.")

query = st.text_area("Ask a question about the selected well", placeholder="e.g., Summarize the data.")

if query and st.button("Search and Analyze"):
    with st.spinner("Searching..."):
        results = query_chroma(collection, query, metadata_filter={"well_name": selected_well}, top_k=5)
        if not results:
            st.warning("No relevant data found.")
        else:
            context = "\n".join([r["text"] for r in results])
            answer = get_answer_from_openai(query, context, openai_api_key, CHAT_MODEL)
            st.write("### Answer:")
            st.write(answer)
