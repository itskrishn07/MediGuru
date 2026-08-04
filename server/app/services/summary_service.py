import logging
from langchain_core.messages import HumanMessage
from prompts.summary_prompt import SUMMARY_PROMPT
from .llm_factory import get_gemini_llm

logger = logging.getLogger(__name__)

def summarize_document(text: str) -> str:
    """
    Summarizes the extracted document text using Gemini model.
    """
    if not text or not text.strip():
        return "No text available to summarize."
        
    try:
        formatted_prompt = SUMMARY_PROMPT.format(document_text=text)
        llm = get_gemini_llm(model_name="gemini-2.5-flash", temperature=0.2)
        message = HumanMessage(content=formatted_prompt)
        response = llm.invoke([message])
        return response.content if response else "No summary generated."
    except Exception as e:
        logger.error(f"Error in summarize_document: {str(e)}", exc_info=True)
        return f"Summary generation failed: {str(e)}"
