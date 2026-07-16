import logging
from vectorstore.chroma import get_chroma_collection
from .embedding_service import embed_text

logger = logging.getLogger(__name__)

def retrieve_relevant_chunks(query: str, n_results: int = 5, document_ids: list[int] | None = None) -> list[dict]:
    """
    Retrieves the most similar chunks from ChromaDB for a given search query,
    scoped optionally to a list of allowed document_ids.
    """
    try:
        # 1. Embed query
        query_embedding = embed_text(query)
        
        # 2. Prepare filter if document_ids is provided
        where_filter = None
        if document_ids is not None:
            if len(document_ids) == 1:
                where_filter = {"document_id": document_ids[0]}
            elif len(document_ids) > 1:
                where_filter = {"document_id": {"$in": document_ids}}
            else:
                # Empty list: match nothing to avoid leaking data
                logger.warning("Empty document_ids list passed. Returning empty context.")
                return []
            
        # 3. Query Chroma
        collection = get_chroma_collection()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter
        )
        
        retrieved_chunks = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0] if "metadatas" in results else [{}] * len(docs)
            distances = results["distances"][0] if "distances" in results else [0.0] * len(docs)
            
            for doc, meta, dist in zip(docs, metas, distances):
                retrieved_chunks.append({
                    "text": doc,
                    "metadata": meta,
                    "distance": dist
                })
        
        return retrieved_chunks
    except Exception as e:
        logger.error(f"Failed to retrieve chunks for query '{query}': {str(e)}", exc_info=True)
        return []
