import logging
import time
from typing import List
from langchain_mistralai import MistralAIEmbeddings
from core.config import settings

logger = logging.getLogger("service.embedding")
_embeddings_client = None

def get_embeddings_client() -> MistralAIEmbeddings:
    global _embeddings_client
    if _embeddings_client is None:
        api_key = settings.MISTRAL_API_KEY
        if not api_key:
            logger.error("Attempted embedding generation without MISTRAL_API_KEY configured.")
            raise ValueError("MISTRAL_API_KEY is required for embedding generation.")
        logger.info("Initializing MistralAIEmbeddings client (model: 'mistral-embed')...")
        _embeddings_client = MistralAIEmbeddings(
            model="mistral-embed",
            mistral_api_key=api_key
        )
        logger.info("MistralAIEmbeddings client initialized successfully.")
    return _embeddings_client

def embed_text(text: str) -> List[float]:
    """
    Generates embedding vector for a single string using Mistral Embeddings.
    """
    logger.info(f"Generating query embedding vector via Mistral (length: {len(text)} chars)...")
    start_time = time.perf_counter()
    client = get_embeddings_client()
    vector = client.embed_query(text)
    latency = time.perf_counter() - start_time
    logger.info(f"Query embedding generated via mistral-embed in {latency:.3f}s (dim: {len(vector)}).")
    return vector

def embed_documents(texts: List[str]) -> List[List[float]]:
    """
    Generates embedding vectors for a list of text chunks using Mistral Embeddings.
    """
    if not texts:
        return []
    logger.info(f"Generating document embeddings via Mistral for {len(texts)} chunks...")
    start_time = time.perf_counter()
    client = get_embeddings_client()
    vectors = client.embed_documents(texts)
    latency = time.perf_counter() - start_time
    logger.info(f"Generated {len(vectors)} embeddings via mistral-embed in {latency:.3f}s.")
    return vectors
