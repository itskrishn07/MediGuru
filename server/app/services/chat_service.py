import logging
from typing import List, Optional
from langchain_core.messages import HumanMessage
from prompts.chat_prompt import CHAT_PROMPT
from .retrieval_service import retrieve_relevant_chunks
from .llm_factory import get_gemini_llm

logger = logging.getLogger("service.chat")

def chat_with_records(query: str, document_ids: Optional[List[int]] = None) -> str:
    """
    Answers a patient's question based on context retrieved from their medical records via RAG.
    """
    logger.info(f"Processing RAG chat query: '{query}' for allowed document_ids: {document_ids}")
    try:
        # 1. Retrieve context chunks
        chunks = retrieve_relevant_chunks(query, n_results=4, document_ids=document_ids)
        context_text = "\n\n".join([f"--- Chunk from {c['metadata'].get('filename')} ---\n{c['text']}" for c in chunks])
        
        if not context_text:
            logger.warning("No context chunks retrieved for query. Utilizing fallback message.")
            context_text = "No medical records found."

        logger.debug(f"Constructed prompt context with {len(chunks)} chunks.")

        # 2. Build prompt
        formatted_prompt = CHAT_PROMPT.format(context=context_text, question=query)
        
        # 3. Call Gemini LLM using LLM Factory
        llm = get_gemini_llm(model_name="gemini-2.5-flash", temperature=0.2)
        message = HumanMessage(content=formatted_prompt)
        
        logger.info("Invoking Gemini 2.5 Flash LLM for RAG answer generation...")
        response = llm.invoke([message])
        
        answer = response.content if response else "No response generated."
        logger.info("RAG chat answer generated successfully.")
        return answer
    except Exception as e:
        logger.error(f"Error executing chat_with_records: {str(e)}", exc_info=True)
        return f"Sorry, I encountered an error while processing your request: {str(e)}"
