import logging
import time
from typing import List
from core.config import settings

logger = logging.getLogger("service.embedding")

_mistral_embeddings = None
_fallback_model = None

def get_embeddings_client():
    global _mistral_embeddings, _fallback_model
    api_key = settings.MISTRAL_API_KEY
    
    if api_key:
        if _mistral_embeddings is None:
            try:
                logger.info("Initializing MistralAIEmbeddings client (model: 'mistral-embed')...")
                from langchain_mistralai import MistralAIEmbeddings
                _mistral_embeddings = MistralAIEmbeddings(
                    model="mistral-embed",
                    mistral_api_key=api_key
                )
                logger.info("MistralAIEmbeddings client initialized successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize MistralAIEmbeddings: {e}. Falling back to SentenceTransformer.")
        if _mistral_embeddings:
            return ("mistral", _mistral_embeddings)

    # Fallback to local SentenceTransformer
    if _fallback_model is None:
        logger.info("Initializing SentenceTransformer fallback model ('all-MiniLM-L6-v2')...")
        from sentence_transformers import SentenceTransformer
        _fallback_model = SentenceTransformer("all-MiniLM-L6-v2")
    return ("sentence_transformer", _fallback_model)

def embed_text(text: str) -> List[float]:
    """
    Generates embedding vector for a single string.
    """
    logger.info(f"Generating query embedding vector (text length: {len(text)} chars)...")
    start_time = time.perf_counter()
    model_type, client = get_embeddings_client()
    
    if model_type == "mistral":
        vector = client.embed_query(text)
    else:
        vector = client.encode(text).tolist()
        
    latency = time.perf_counter() - start_time
    logger.info(f"Query embedding generated via {model_type} in {latency:.3f}s (dim: {len(vector)}).")
    return vector

def embed_documents(texts: List[str]) -> List[List[float]]:
    """
    Generates embedding vectors for a list of text chunks.
    """
    if not texts:
        return []
    logger.info(f"Generating document embeddings for {len(texts)} chunks...")
    start_time = time.perf_counter()
    model_type, client = get_embeddings_client()
    
    if model_type == "mistral":
        vectors = client.embed_documents(texts)
    else:
        vectors = client.encode(texts).tolist()
        
    latency = time.perf_counter() - start_time
    logger.info(f"Generated {len(vectors)} embeddings via {model_type} in {latency:.3f}s.")
    return vectors
