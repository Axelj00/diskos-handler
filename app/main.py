import sys
import os
import streamlit as st

# Fix module path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config import CHROMA_DB_DIR, CHROMA_COLLECTION_NAME

st.set_page_config(page_title="Well Information Database", page_icon="📄")

st.title("Well Information Database")
st.write(
    """
    Welcome to the **Well Information Database** platform!  
    - Upload PDFs related to specific wells.
    - Query and analyze data using **AI-powered search**.

    Use the sidebar to navigate between **Upload** and **Query** pages.
    """
)
