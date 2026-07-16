"""
LLM Service

Provides a singleton OpenAI LLM instance.
"""

from langchain_openai import ChatOpenAI

from app.config.settings import settings

_llm = None


def get_llm():
    """
    Returns a singleton OpenAI LLM instance.
    """
    global _llm

    if _llm is None:

        _llm = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0,
            max_retries=3,
        )

    return _llm