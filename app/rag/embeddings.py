"""
Embedding Service

Responsible for loading and providing the embedding model
used for vector generation and similarity search.
"""

from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from app.config.settings import settings


class EmbeddingService:
    """
    Singleton wrapper around the embedding model.
    """

    def __init__(self) -> None:

        self.embedding_model = HuggingFaceEmbeddings(

            model_name=settings.embedding_model,

            model_kwargs={
                "device": "cpu"
            },

            encode_kwargs={
                "normalize_embeddings": True
            },
        )

    def get_embeddings(self) -> HuggingFaceEmbeddings:
        """
        Returns initialized embedding model.
        """

        return self.embedding_model


@lru_cache(maxsize=1)
def get_embedding_service() -> HuggingFaceEmbeddings:
    """
    Returns a cached embedding model instance.
    """

    return EmbeddingService().get_embeddings()