"""
RAG Service

This module is responsible for answering hotel-related
questions using Retrieval-Augmented Generation (RAG).
"""

from langchain_core.prompts import ChatPromptTemplate

from app.agent.prompts import RAG_PROMPT
from app.rag.retriever import RetrieverService
from app.services.llm_service import get_llm


class RAGService:
    """
    Handles Retrieval-Augmented Generation.
    """

    def __init__(self) -> None:

        self.retriever = RetrieverService()

        self.llm = get_llm()

        self.prompt = ChatPromptTemplate.from_template(
            RAG_PROMPT
        )

    # ---------------------------------------------------------
    # Build Context
    # ---------------------------------------------------------

    @staticmethod
    def build_context(documents) -> str:
        """
        Converts retrieved documents into a single context.
        """

        return "\n\n".join(
            document.page_content
            for document in documents
        )

    # ---------------------------------------------------------
    # Ask Question
    # ---------------------------------------------------------

    def ask(
        self,
        question: str,
    ) -> dict:
        """
        Answers hotel-related questions using RAG.
        """

        documents = self.retriever.retrieve(question)

        context = self.build_context(documents)

        chain = self.prompt | self.llm

        response = chain.invoke(
            {
                "context": context,
                "question": question,
            }
        )

        answer = response.content

        if isinstance(answer, list):

            final_answer = []

            for item in answer:

                if isinstance(item, dict):
                    final_answer.append(item.get("text", ""))

                elif hasattr(item, "text"):
                    final_answer.append(item.text)

                else:
                    final_answer.append(str(item))

            answer = "".join(final_answer)

        return {
            "answer": answer.strip(),
            "sources": [
                {
                    "page": document.metadata.get("page"),
                    "source": document.metadata.get("source"),
                }
                for document in documents
            ],
        }