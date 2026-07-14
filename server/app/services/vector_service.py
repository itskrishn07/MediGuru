import logging
from vectorstore.chroma import get_chroma_collection
from .chunking_service import split_text
from .embedding_service import embed_documents

logger = logging.getLogger(__name__)

def index_document(document_id: int, filename: str, text: str) -> bool:
    """
    Chunks the document text, generates embeddings, and indexes them in ChromaDB.
    """
    if not text or not text.strip():
        logger.warning(f"No text content to index for document {document_id}")
        return False
        
    try:
        # 1. Chunk text
        chunks = split_text(text)
        if not chunks:
            return False
            
        # 2. Embed chunks
        logger.info(f"Generating embeddings for {len(chunks)} chunks of document {document_id}...")
        embeddings = embed_documents(chunks)
        
        # 3. Prepare IDs, Metadatas
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
        logger.info(f"Successfully indexed {len(chunks)} chunks in Chroma for document {document_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to index document {document_id} in Chroma: {str(e)}", exc_info=True)
        return False
