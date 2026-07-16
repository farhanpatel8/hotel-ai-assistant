"""
Indexing Service

This service builds the FAISS vector database
from the hotel PDF.

Pipeline:

PDF
    ↓
Loader
    ↓
Splitter
    ↓
Embeddings
    ↓
FAISS
    ↓
Save Index
"""

from pathlib import Path

from app.rag.loader import PDFLoader
from app.rag.splitter import DocumentSplitter
from app.rag.vectorstore import VectorStoreService


class IndexingService:
    """
    Responsible for creating and maintaining
    the vector database.
    """

    def __init__(
        self,
        pdf_path: str,
    ) -> None:

        self.pdf_path = Path(pdf_path)

        self.loader = PDFLoader(str(self.pdf_path))

        self.splitter = DocumentSplitter()

        self.vector_store = VectorStoreService()

    # ---------------------------------------------------------
    # Build Vector Store
    # ---------------------------------------------------------

    def build_vector_store(self) -> None:
        """
        Creates FAISS index from the hotel PDF.

        If the index already exists,
        it skips rebuilding.
        """

        if self.vector_store.exists():

            print("Vector store already exists.")

            return

        print("Loading PDF...")

        documents = self.loader.load()

        print(f"Loaded {len(documents)} pages.")

        print("Splitting documents...")

        chunks = self.splitter.split(documents)

        print(f"Created {len(chunks)} chunks.")

        print("Creating embeddings and FAISS index...")

        vector_db = self.vector_store.create(chunks)

        print("Saving vector database...")

        self.vector_store.save(vector_db)

        print("Vector database created successfully.")