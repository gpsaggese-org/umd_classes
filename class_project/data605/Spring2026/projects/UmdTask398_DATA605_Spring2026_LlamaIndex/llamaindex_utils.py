"""
Import as:

import projects.UmdTask398_DATA605_Spring2026_LlamaIndex.llamaindex_utils as lldxuti
"""

import logging
from dotenv import load_dotenv

_LOG = logging.getLogger(__name__)

def setup_environment(verbosity: int = logging.INFO) -> None:
    """
    Load environment variables and initialize logging for LlamaIndex projects.
    """
    load_dotenv()
    logging.basicConfig(level=verbosity)
    logger = logging.getLogger(__name__)

    if verbosity <= logging.INFO:
        logger.info("Environment setup complete.")

def configure_ollama(model_name: str = "llama3") -> None:
    """
    Configure LlamaIndex to use a local Ollama model running on the host machine.

    :param model_name: The Ollama model to use as the LLM backend (default: 'llama3').
                       Any model pulled via `ollama pull <model>` can be passed here.
    """
    from llama_index.core import Settings
    from llama_index.llms.ollama import Ollama
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding

    # 1. Use local Ollama for the LLM.
    # host.docker.internal allows the Docker container to talk to Ollama on your Mac.
    Settings.llm = Ollama(
        model=model_name,
        request_timeout=120.0,
        base_url="http://host.docker.internal:11434"
    )

    # 2. Use a fast, free local embedding model (runs completely inside Docker).
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )
    print(f"LlamaIndex configured: LLM=Ollama({model_name}), Embeddings=BAAI/bge-small-en-v1.5")