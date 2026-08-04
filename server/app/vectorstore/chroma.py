import logging
from pathlib import Path
import chromadb
from core.config import settings

logger = logging.getLogger("vectorstore.chroma")

def initialize_chroma_client():
    db_path = settings.CHROMA_DB_DIR
    logger.info(f"Initializing ChromaDB client at path: {db_path}")
    
    # 1. Try to create the directory
    try:
        db_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.warning(f"Could not create primary ChromaDB directory at {db_path}: {e}")
        
    # 2. Test directory writability
    is_writable = False
    test_file = db_path / ".write_test"
    try:
        if db_path.exists() and db_path.is_dir():
            with open(test_file, "w") as f:
                f.write("test")
            test_file.unlink()
            is_writable = True
    except Exception as e:
        logger.warning(f"Primary ChromaDB path {db_path} is not writable: {e}")

    if not is_writable:
        fallback_path = Path.home() / ".mediguru_chroma_db"
        logger.warning(f"Primary path {db_path} unwritable. Falling back to: {fallback_path}")
        try:
            fallback_path.mkdir(parents=True, exist_ok=True)
            db_path = fallback_path
        except Exception as e:
            logger.critical(f"Failed to create fallback directory at {fallback_path}: {e}. Defaulting to ephemeral client.")
            return chromadb.EphemeralClient()
            
    try:
        client_inst = chromadb.PersistentClient(path=str(db_path))
        logger.info(f"Successfully initialized Persistent ChromaDB client at: {db_path}")
        return client_inst
    except Exception as e:
        logger.critical(f"Failed to instantiate Persistent Client at {db_path}: {e}. Falling back to ephemeral/in-memory client.", exc_info=True)
        return chromadb.EphemeralClient()

client = initialize_chroma_client()

def get_chroma_collection(collection_name: str = "medical_documents"):
    """
    Returns (or creates) the specified ChromaDB collection.
    """
    logger.debug(f"Accessing ChromaDB collection: '{collection_name}'")
    return client.get_or_create_collection(name=collection_name)
