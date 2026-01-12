"""
Agentic RAG Streamlit Application
=================================
Streamlit UI for the agentic RAG system.
All agent logic is imported from agentic_rag.py.
"""

import os
import json
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================
# API Keys & LangSmith Config
# ============================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

if LANGCHAIN_API_KEY:
    os.environ["LANGCHAIN_TRACING_V2"] = os.getenv(
        "LANGCHAIN_TRACING_V2", "true")
    os.environ["LANGCHAIN_ENDPOINT"] = os.getenv(
        "LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
    os.environ["LANGCHAIN_PROJECT"] = os.getenv(
        "LANGCHAIN_PROJECT", "agentic-rag")
    TRACING_ENABLED = True
else:
    TRACING_ENABLED = False

# ============================================
# Page Config
# ============================================
st.set_page_config(
    page_title="Agentic RAG Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================
# Sidebar
# ============================================
with st.sidebar:
    st.title("⚙️ Configuration")

    st.subheader("API Status")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Groq LLM:**")
        st.write("**Tavily Search:**")
        st.write("**Google AI:**")
        st.write("**LangSmith:**")
    with col2:
        st.write("✅" if GROQ_API_KEY else "❌")
        st.write("✅" if TAVILY_API_KEY else "❌")
        st.write("✅" if GOOGLE_API_KEY else "⚪")
        st.write("✅" if TRACING_ENABLED else "⚪")

    st.divider()

    st.subheader("📚 Knowledge Base")
    uploaded_files = st.file_uploader(
        "Upload documents (optional)",
        accept_multiple_files=True,
        type=["txt", "md"],
        help="Upload documents to add to the knowledge base"
    )

    st.divider()
    st.subheader("🔧 Options")
    show_sources = st.checkbox("Show retrieved sources", value=True)
    show_steps = st.checkbox("Show reasoning steps", value=True)
    show_notebook = st.checkbox("Show notebook code", value=False)


# ============================================
# Load Notebook Content
# ============================================
def load_notebook_content():
    """Load agentic_rag.ipynb as text for reference."""
    notebook_path = Path("agentic_rag.ipynb")
    if notebook_path.exists():
        try:
            with open(notebook_path, "r") as f:
                notebook = json.load(f)
            code_cells = []
            for cell in notebook.get("cells", []):
                if cell.get("cell_type") == "code":
                    source = "".join(cell.get("source", []))
                    code_cells.append(source)
            return "\n\n# ---\n\n".join(code_cells)
        except Exception as e:
            return f"Error loading notebook: {e}"
    return "Notebook not found."


# ============================================
# Initialize Agent
# ============================================
@st.cache_resource
def initialize_agent():
    """Initialize the AgenticRAG system."""
    if not GROQ_API_KEY:
        return None, "Missing GROQ_API_KEY"
    if not TAVILY_API_KEY:
        return None, "Missing TAVILY_API_KEY"

    try:
        from agentic_rag import AgenticRAG
        agent = AgenticRAG(
            groq_api_key=GROQ_API_KEY,
            tavily_api_key=TAVILY_API_KEY,
            google_api_key=GOOGLE_API_KEY,
        )
        return agent, None
    except Exception as e:
        return None, str(e)


agent, init_error = initialize_agent()

# Handle file uploads
if agent and uploaded_files:
    texts = []
    titles = []
    for f in uploaded_files:
        content = f.read().decode("utf-8")
        texts.append(content)
        titles.append(f.name)
    if texts:
        agent.add_documents(texts, titles)
        st.sidebar.success(f"Added {len(texts)} document(s)")


# ============================================
# Main UI
# ============================================
st.title("🤖 Agentic RAG Assistant")
st.markdown("""
An intelligent assistant combining **retrieval-augmented generation** with **agentic reasoning**.
""")

if init_error:
    st.warning(f"⚠️ Agent Status: {init_error}")

if show_notebook:
    with st.expander("📓 Notebook Code", expanded=False):
        st.code(load_notebook_content(), language="python")

st.divider()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and show_sources and message.get("sources"):
            with st.expander("📚 Sources"):
                for src in message["sources"]:
                    st.markdown(
                        f"**{src.get('title', 'Source')}** ({src.get('type', 'unknown')})")
                    st.caption(src.get('content', '')[:200] + "...")

# Query input
st.subheader("Ask a Question")

with st.form(key="query_form", clear_on_submit=True):
    query = st.text_area(
        "Enter your question:",
        placeholder="e.g., What is RAG and how does it work?",
        height=100,
    )
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        submit_button = st.form_submit_button(
            "🔍 Submit", use_container_width=True)
    with col2:
        clear_button = st.form_submit_button(
            "🗑️ Clear", use_container_width=True)

if clear_button:
    st.session_state.messages = []
    st.rerun()

if submit_button and query.strip():
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            if agent:
                result = agent.query(query)
            else:
                result = {
                    "answer": "Agent not initialized. Check API keys.",
                    "sources": [],
                    "reasoning_steps": ["❌ Initialization failed"]
                }

            st.markdown(result["answer"])

            if show_sources and result.get("sources"):
                with st.expander("📚 Sources", expanded=False):
                    for src in result["sources"]:
                        st.markdown(
                            f"**{src.get('title', 'Source')}** ({src.get('type', 'unknown')})")
                        if src.get("url"):
                            st.caption(f"URL: {src.get('url')}")
                        st.caption(src.get('content', '')[:200] + "...")

            if show_steps and result.get("reasoning_steps"):
                with st.expander("🧠 Reasoning Steps", expanded=False):
                    for step in result["reasoning_steps"]:
                        st.markdown(f"- {step}")

            st.session_state.messages.append({
                "role": "assistant",
                "content": result["answer"],
                "sources": result.get("sources", [])
            })

# Footer
st.divider()
st.caption("**Workflow:** Reason → Retrieve → (Web Search) → Synthesize")
