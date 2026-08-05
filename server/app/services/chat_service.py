import logging
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from prompts.chat_prompt import CHAT_PROMPT
from .retrieval_service import retrieve_relevant_chunks
from .llm_factory import get_gemini_llm

logger = logging.getLogger("service.chat")

def chat_with_records(query: str) -> Dict[str, Any]:
    """
    Answers a patient's question based on context retrieved from their medical document via RAG.
    """
    logger.info(f"Processing RAG chat query: '{query}'")
    try:
        chunks = retrieve_relevant_chunks(query, n_results=4)
        sources = [c["metadata"].get("filename", "Document") for c in chunks if "metadata" in c]
        context_text = "\n\n".join([f"--- Context Chunk ({c['metadata'].get('filename', 'Doc')}) ---\n{c['text']}" for c in chunks])
        
        if not context_text:
            logger.warning("No context chunks retrieved for query.")
            context_text = "No medical records uploaded in current session."

        formatted_prompt = CHAT_PROMPT.format(context=context_text, question=query)
        llm = get_gemini_llm(model_name="gemini-2.5-flash", temperature=0.2)
        message = HumanMessage(content=formatted_prompt)
        
        logger.info("Invoking Gemini LLM for RAG answer generation...")
        response = llm.invoke([message])
        
        answer = response.content if response else "No response generated."
        logger.info("RAG chat answer generated successfully.")
        return {
            "query": query,
            "answer": answer,
            "sources": list(set(sources))
        }
    except Exception as e:
        logger.error(f"Error executing chat_with_records: {str(e)}", exc_info=True)
        return {
            "query": query,
            "answer": f"Sorry, I encountered an error while processing your request: {str(e)}",
            "sources": []
        }
