import logging
import time
from langchain_mistralai import MistralAIEmbeddings
from core.config import settings

logger = logging.getLogger(__name__)
_embeddings = None

def get_embeddings_client() -> MistralAIEmbeddings:
    global _embeddings
    if _embeddings is None:
        api_key = settings.MISTRAL_API_KEY
        if not api_key:
            raise ValueError("Mistral API key required. Please set MISTRAL_API_KEY environment variable.")
        _embeddings = MistralAIEmbeddings(
            model="mistral-embed",
            mistral_api_key=api_key
        )
    return _embeddings

def embed_text(text: str) -> list[float]:
    """
    Generates embedding vector for a single string.
    """
    client = get_embeddings_client()
    return client.embed_query(text)

def embed_documents(texts: list[str]) -> list[list[float]]:
    """
    Generates embedding vectors for a list of strings in batches.
    Handles rate limits, large inputs, and connection issues robustly.
    """
    client = get_embeddings_client()
    
    batch_size = 5
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        logger.info(f"Embedding batch {i // batch_size + 1}/{-(-len(texts) // batch_size)} ({len(batch)} items)...")
        
        for attempt in range(3):
            try:
                embeddings = client.embed_documents(batch)
                all_embeddings.extend(embeddings)
                break
            except Exception as e:
                logger.warning(f"Embedding generation attempt {attempt + 1} failed for batch: {str(e)}")
                if attempt == 2:
                    logger.error("Embedding generation failed after all attempts.")
                    raise e
                time.sleep(2 ** attempt)  # Exponential backoff
                
    return all_embeddings
