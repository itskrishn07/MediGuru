import logging
from vectorstore.chroma import get_chroma_collection
from .chunking_service import split_text
from .embedding_service import embed_documents

logger = logging.getLogger("service.vector")

def index_document(document_id: int, filename: str, text: str) -> bool:
    """
    Chunks document text, generates embeddings, and indexes them in ChromaDB.
    """
    if not text or not text.strip():
        logger.warning(f"Aborting vector indexing: Document ID {document_id} ({filename}) has no text content.")
        return False
        
    try:
        # 1. Chunk text
        logger.info(f"Chunking text for Document ID {document_id} ({filename}). Total text length: {len(text)} chars.")
        chunks = split_text(text)
        if not chunks:
            logger.warning(f"No chunks generated for Document ID {document_id} ({filename}).")
            return False
            
        logger.info(f"Generated {len(chunks)} text chunks for Document ID {document_id}.")

        # 2. Embed chunks
        logger.info(f"Initiating embedding generation for {len(chunks)} chunks of Document ID {document_id}...")
        embeddings = embed_documents(chunks)
        
        # 3. Prepare IDs and Metadata
        ids = [f"doc_{document_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "document_id": document_id,
                "filename": filename,
                "chunk_index": i
            }
            for i in range(len(chunks))
        ]
        
        # 4. Store in Chroma
        collection = get_chroma_collection()
        collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=chunks
        )
        logger.info(f"Successfully indexed {len(chunks)} chunks in ChromaDB for Document ID {document_id} ({filename}).")
        return True
    except Exception as e:
        logger.error(f"Failed to index Document ID {document_id} in ChromaDB: {str(e)}", exc_info=True)
        return False

def delete_document_from_chroma(document_id: int) -> bool:
    """
    Deletes all indexed chunks for a given document_id from ChromaDB.
    """
    logger.info(f"Deleting vector embeddings from ChromaDB for Document ID {document_id}...")
    try:
        collection = get_chroma_collection()
        collection.delete(where={"document_id": document_id})
        logger.info(f"Successfully deleted all chunks for Document ID {document_id} from ChromaDB.")
        return True
    except Exception as e:
        logger.error(f"Failed to delete ChromaDB embeddings for Document ID {document_id}: {str(e)}", exc_info=True)
        return False
