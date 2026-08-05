import logging
import shutil
from pathlib import Path
import chromadb
from core.config import settings

logger = logging.getLogger("vectorstore.chroma")

_client = None

def get_chroma_client():
    global _client
    if _client is None:
        db_path = settings.CHROMA_DB_DIR
        db_path.mkdir(parents=True, exist_ok=True)
        try:
            logger.info(f"Initializing Persistent ChromaDB client at: {db_path}")
            _client = chromadb.PersistentClient(path=str(db_path))
        except Exception as e:
            logger.warning(f"Failed to instantiate Persistent Client: {e}. Falling back to EphemeralClient.")
            _client = chromadb.EphemeralClient()
    return _client

def get_chroma_collection(collection_name: str = "medical_documents"):
    """
    Returns (or creates) the specified ChromaDB collection.
    """
    client = get_chroma_client()
    return client.get_or_create_collection(name=collection_name)

def reset_chroma_session(collection_name: str = "medical_documents"):
    """
    Deletes collection and wipes temporary session directory.
    """
    global _client
    logger.info("Resetting ChromaDB session and clearing temporary files...")
    client = get_chroma_client()
    try:
        client.delete_collection(name=collection_name)
        logger.info(f"Deleted collection '{collection_name}' from ChromaDB.")
    except Exception as e:
        logger.warning(f"Collection reset warning: {str(e)}")

    # Clean upload temp directory
    try:
        if settings.UPLOAD_DIR.exists():
            for item in settings.UPLOAD_DIR.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            logger.info("Wiped upload directory contents.")
    except Exception as err:
        logger.error(f"Failed to clear temp uploads: {str(err)}")
