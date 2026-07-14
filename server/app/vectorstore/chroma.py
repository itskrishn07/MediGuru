import os
import logging
from pathlib import Path
import chromadb
from core.config import settings

logger = logging.getLogger(__name__)

def initialize_chroma_client():
    db_path = settings.CHROMA_DB_DIR
    logger.info(f"Attempting to initialize ChromaDB at: {db_path}")
    
    # 1. Try to create the directory
    try:
        db_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.warning(f"Could not create ChromaDB directory at {db_path}: {e}")
        
    # 2. Test if we can write to the directory
    is_writable = False
    test_file = db_path / ".write_test"
    try:
        if db_path.exists() and db_path.is_dir():
            with open(test_file, "w") as f:
                f.write("test")
            test_file.unlink()
            is_writable = True
    except Exception as e:
        logger.warning(f"ChromaDB directory at {db_path} is not writable: {e}")

    if not is_writable:
        # Fallback to user home directory
        fallback_path = Path.home() / ".mediguru_chroma_db"
        logger.warning(f"ChromaDB path {db_path} is not writable. Falling back to: {fallback_path}")
        try:
            fallback_path.mkdir(parents=True, exist_ok=True)
            db_path = fallback_path
        except Exception as e:
            logger.critical(f"Failed to create fallback ChromaDB directory at {fallback_path}: {e}")
            # If all else fails, use in-memory client
            logger.critical("Falling back to ephemeral/in-memory ChromaDB client.")
            return chromadb.EphemeralClient()
            
    try:
        return chromadb.PersistentClient(path=str(db_path))
    except Exception as e:
        logger.critical(f"Failed to create persistent ChromaDB client at {db_path}: {e}. Falling back to ephemeral/in-memory.")
        return chromadb.EphemeralClient()

client = initialize_chroma_client()

def get_chroma_collection(collection_name: str = "medical_documents"):
    """
    Returns (or creates) the specified ChromaDB collection.
    """
    return client.get_or_create_collection(name=collection_name)
