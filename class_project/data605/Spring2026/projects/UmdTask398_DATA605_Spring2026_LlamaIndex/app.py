import streamlit as st
import os
import logging
from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.core.tools import QueryEngineTool, ToolMetadata, FunctionTool
from llama_index.core.agent import ReActAgent
from llamaindex_utils import setup_environment, configure_ollama

# Setup async event loop for LlamaIndex Workflow-based agents
import asyncio
import nest_asyncio
nest_asyncio.apply()
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# --- Page Configuration & Styling ---
st.set_page_config(
    page_title="Historical QA System",
    page_icon="📜", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Historical Theme: Parchment and Leather */
    .stApp {
        background-color: #FDF6E3;
    }
    header {visibility: hidden;}
    
    /* Force Sidebar Visible */
    [data-testid="stSidebar"] {
        visibility: visible !important;
        display: block !important;
        background-color: #3B2A1A !important;
    }
    [data-testid="stSidebar"] * {
        color: #FDF6E3 !important;
        visibility: visible !important;
    }
    
    /* Custom Header */
    .hist-header {
        background-color: #4A3525;
        padding: 20px;
        border-radius: 8px;
        color: #FDF6E3;
        border-left: 10px solid #C5A059;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        font-family: 'Georgia', serif;
    }
    .hist-header h1 {
        color: #FDF6E3;
        margin: 0;
        padding: 0;
        font-family: 'Georgia', serif;
    }
    .hist-header p {
        color: #C5A059;
        margin: 0;
        font-size: 1.2rem;
        font-style: italic;
    }
    
    /* Chat Bubbles */
    .stChatMessage {
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
        font-family: 'Georgia', serif;
    }
    .stChatMessage p, .stChatMessage div, .stChatMessage span {
        color: #2C1A0E !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hist-header">
    <h1>DATA605: Historical QA Agent</h1>
    <p>Powered by LlamaIndex & Ollama</p>
</div>
""", unsafe_allow_html=True)

# --- Backend Initialization ---
@st.cache_resource
def initialize_backend():
    setup_environment(verbosity=logging.WARNING)
    configure_ollama(model_name="llama3")
    
    persist_dir = "./storage"
    if not os.path.exists(persist_dir):
        return None
    
    # Load index from disk instantly
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    index = load_index_from_storage(storage_context)
    
    # Create Tools
    wiki_tool = QueryEngineTool(
        query_engine=index.as_query_engine(),
        metadata=ToolMetadata(
            name="wikipedia_history_db",
            description=(
                "Use this tool to answer factual historical questions about the "
                "indexed historical events corpus (multiple Wikipedia articles). "
                "Input must be a specific natural language question."
            )
        )
    )
    
    def subtract_years(year1: int, year2: int) -> int:
        """Calculates the absolute difference in years between two historical events."""
        return abs(year1 - year2)
    
    math_tool = FunctionTool.from_defaults(fn=subtract_years)
    
    # Create Agent
    agent = ReActAgent(
        tools=[wiki_tool, math_tool],
        llm=Settings.llm,
        verbose=True,
        max_iterations=10
    )
    return agent

with st.spinner("Loading LlamaIndex Backend..."):
    agent = initialize_backend()

if agent is None:
    st.error("Vector Index not found! Please run the Jupyter Notebook first to generate the `./storage` folder.")
    st.stop()

# --- Sidebar ---
with st.sidebar:
    st.image("historical_events_timeline.png", caption="Knowledge Base Coverage")
    st.markdown("### System Architecture")
    st.markdown("- **Framework**: LlamaIndex")
    st.markdown("- **LLM**: Ollama (`llama3`)")
    st.markdown("- **Embeddings**: `BAAI/bge-small-en-v1.5`")
    st.markdown("### Available Tools")
    st.markdown("- `wikipedia_history_db`: RAG factual lookup")
    st.markdown("- `subtract_years`: Arithmetic calculations")

# --- Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome! Ask me a question about WWII, the French Revolution, or the Industrial Revolution. I can also do math on historical dates!"}
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
if prompt := st.chat_input("Ask a historical question..."):
    # Add user message to state and UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
        
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... (Check your terminal for the ReAct Agent's thought trace)"):
            async def _run():
                return await agent.run(prompt)
            response = asyncio.run(_run())
            st.write(str(response))
    
    # Save assistant response to state
    st.session_state.messages.append({"role": "assistant", "content": str(response)})