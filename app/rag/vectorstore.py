"""
FAISS Vector Store

Responsible for:

1. Creating the vector database
2. Saving vector database
3. Loading existing vector database
"""

from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.config.settings import settings
from app.rag.embeddings import get_embedding_service


class VectorStoreService:
    """
    Handles all FAISS vector store operations.
    """

    def __init__(self) -> None:

        self.index_path = Path(settings.vector_db_path)

        self.embeddings = get_embedding_service()

    # ---------------------------------------------------------
    # Create Vector Store
    # ---------------------------------------------------------

    def create(
        self,
        documents: list[Document],
    ) -> FAISS:
        """
        Creates FAISS index from documents.
        """

        vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings,
        )

        return vector_store

    # ---------------------------------------------------------
    # Save Vector Store
    # ---------------------------------------------------------

    def save(
        self,
        vector_store: FAISS,
    ) -> None:
        """
        Saves FAISS index locally.
        """

        self.index_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        vector_store.save_local(
            str(self.index_path)
        )

    # ---------------------------------------------------------
    # Load Vector Store
    # ---------------------------------------------------------

    def load(self) -> FAISS:
        """
        Loads existing FAISS index.
        """

        return FAISS.load_local(
            folder_path=str(self.index_path),
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True,
        )

    # ---------------------------------------------------------
    # Check Index
    # ---------------------------------------------------------

    def exists(self) -> bool:
        """
        Checks whether FAISS index exists.
        """

        return (
            self.index_path.exists()
            and any(self.index_path.iterdir())
        )