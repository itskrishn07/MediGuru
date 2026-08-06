import logging
from langchain_core.messages import HumanMessage
from prompts.summary_prompt import SUMMARY_PROMPT
from .llm_factory import get_gemini_llm

logger = logging.getLogger(__name__)

def summarize_document(text: str) -> str:
    """
    Summarizes the extracted document text using Gemini model with gemini-1.5-flash fallback.
    """
    if not text or not text.strip():
        return "No text available to summarize."
        
    formatted_prompt = SUMMARY_PROMPT.format(document_text=text)
    message = HumanMessage(content=formatted_prompt)

    try:
        llm = get_gemini_llm(model_name="gemini-2.5-flash", temperature=0.2)
        response = llm.invoke([message])
        return response.content if response else "No summary generated."
    except Exception as err1:
        err_str = str(err1)
        logger.warning(f"Summary generation with gemini-2.5-flash notice: {err_str}")
        if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "Quota" in err_str:
            try:
                fallback_llm = get_gemini_llm(model_name="gemini-1.5-flash", temperature=0.2)
                resp = fallback_llm.invoke([message])
                return resp.content if resp else "Summary generated."
            except Exception as err2:
                logger.error(f"Fallback summary generation failed: {err2}")
                return "Gemini API free tier rate limit reached. Please wait ~30 seconds and try again."
        return "Summary currently unavailable due to rate limits."
