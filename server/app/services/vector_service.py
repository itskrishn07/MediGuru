import logging
from vectorstore.chroma import get_chroma_collection
from .chunking_service import split_text
from .embedding_service import embed_documents

logger = logging.getLogger("service.vector")

def index_document(doc_id: str, filename: str, text: str) -> bool:
    """
    Chunks document text, generates embeddings, and indexes them in temporary ChromaDB.
    """
    if not text or not text.strip():
        logger.warning(f"Aborting vector indexing: Document {filename} has no text content.")
        return False
        
    try:
        # 1. Chunk text
        logger.info(f"Chunking text for Document {filename}. Total text length: {len(text)} chars.")
        chunks = split_text(text)
        if not chunks:
            logger.warning(f"No chunks generated for Document {filename}.")
            return False
            
        logger.info(f"Generated {len(chunks)} text chunks for Document {filename}.")

        # 2. Embed chunks
        logger.info(f"Generating embeddings for {len(chunks)} chunks of {filename}...")
        embeddings = embed_documents(chunks)
        
        # 3. Prepare IDs and Metadata
        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "doc_id": doc_id,
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
        logger.info(f"Successfully indexed {len(chunks)} chunks in ChromaDB for {filename}.")
        return True
    except Exception as e:
        logger.error(f"Failed to index Document in ChromaDB: {str(e)}", exc_info=True)
        return False
