import logging
import time
from langchain_mistralai import MistralAIEmbeddings
from core.config import settings

logger = logging.getLogger("service.embedding")
_embeddings = None

def get_embeddings_client() -> MistralAIEmbeddings:
    global _embeddings
    if _embeddings is None:
        api_key = settings.MISTRAL_API_KEY
        if not api_key:
            logger.error("Attempted embedding generation without MISTRAL_API_KEY configured.")
            raise ValueError("Mistral API key required. Please set MISTRAL_API_KEY environment variable.")
        logger.info("Initializing MistralAIEmbeddings client (model: mistral-embed)...")
        _embeddings = MistralAIEmbeddings(
            model="mistral-embed",
            mistral_api_key=api_key
        )
    return _embeddings

def embed_text(text: str) -> list[float]:
    """
    Generates embedding vector for a single string.
    """
    logger.info(f"Generating query embedding vector (text length: {len(text)} chars)...")
    start_time = time.perf_counter()
    client = get_embeddings_client()
    vec = client.embed_query(text)
    latency = time.perf_counter() - start_time
    logger.info(f"Query embedding generated successfully in {latency:.3f}s (vector dim: {len(vec)}).")
    return vec

def embed_documents(texts: list[str]) -> list[list[float]]:
    """
    Generates embedding vectors for a list of strings in batches.
    Handles rate limits, large inputs, and connection issues robustly with exponential backoff.
    """
    logger.info(f"Generating document embeddings for {len(texts)} chunks...")
    start_time = time.perf_counter()
    client = get_embeddings_client()
    
    batch_size = 5
    all_embeddings = []
    total_batches = -(-len(texts) // batch_size)
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_idx = i // batch_size + 1
        logger.info(f"Embedding batch {batch_idx}/{total_batches} ({len(batch)} chunks)...")
        
        for attempt in range(3):
            try:
                embeddings = client.embed_documents(batch)
                all_embeddings.extend(embeddings)
                break
            except Exception as e:
                logger.warning(f"Embedding batch {batch_idx} attempt {attempt + 1}/3 failed: {str(e)}")
                if attempt == 2:
                    logger.error(f"Embedding batch {batch_idx} failed after 3 attempts.", exc_info=True)
                    raise e
                time.sleep(2 ** attempt)
                
    latency = time.perf_counter() - start_time
    logger.info(f"Successfully generated {len(all_embeddings)} embedding vectors in {latency:.3f}s.")
    return all_embeddings
