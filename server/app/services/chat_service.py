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
    Includes automatic model fallback to gemini-1.5-flash and clean rate limit error handling.
    """
    logger.info(f"Processing RAG chat query: '{query}'")
    chunks = retrieve_relevant_chunks(query, n_results=4)
    sources = [c["metadata"].get("filename", "Document") for c in chunks if "metadata" in c]
    context_text = "\n\n".join([f"--- Context Chunk ({c['metadata'].get('filename', 'Doc')}) ---\n{c['text']}" for c in chunks])
    
    if not context_text or not context_text.strip():
        logger.warning("No context chunks retrieved for query.")
        context_text = "No medical records uploaded in current session."

    formatted_prompt = CHAT_PROMPT.format(context=context_text, question=query)
    message = HumanMessage(content=formatted_prompt)
    
    # Attempt Primary Model: gemini-2.5-flash
    try:
        logger.info("Invoking Gemini 2.5 Flash for RAG chat...")
        llm = get_gemini_llm(model_name="gemini-2.5-flash", temperature=0.2)
        response = llm.invoke([message])
        answer = response.content if response else "No response generated."
        logger.info("RAG chat answer generated successfully via gemini-2.5-flash.")
        return {"query": query, "answer": answer, "sources": list(set(sources))}

    except Exception as err1:
        err_str = str(err1)
        logger.warning(f"RAG chat gemini-2.5-flash notice: {err_str}")

        # Fallback Model Attempt: gemini-1.5-flash if 429 rate limit or quota error
        if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "Quota" in err_str:
            logger.info("Rate limit hit. Falling back to gemini-1.5-flash for RAG chat...")
            try:
                fallback_llm = get_gemini_llm(model_name="gemini-1.5-flash", temperature=0.2)
                fallback_resp = fallback_llm.invoke([message])
                answer = fallback_resp.content if fallback_resp else "Response generated."
                logger.info("RAG chat answer generated successfully via gemini-1.5-flash fallback.")
                return {"query": query, "answer": answer, "sources": list(set(sources))}
            except Exception as err2:
                logger.error(f"Fallback RAG chat model failed: {err2}")
                return {
                    "query": query,
                    "answer": "Gemini API free tier rate limit reached. Please wait ~15-20 seconds before asking your next question.",
                    "sources": []
                }
        else:
            return {
                "query": query,
                "answer": "Currently unable to process chat request. Please ensure your document is uploaded and try again.",
                "sources": []
            }
