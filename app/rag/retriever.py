"""
Retriever Service

Responsible for retrieving the most relevant
document chunks from the FAISS vector database.
"""

from langchain_core.documents import Document

from app.rag.vectorstore import VectorStoreService


class RetrieverService:

    def __init__(
        self,
        top_k: int = 4,
    ):

        self.top_k = top_k

        self.vector_service = VectorStoreService()

        self.vector_store = None

        self.retriever = None

    def _load_vector_store(self):
        """
        Load vector store only when needed.
        """

        if self.vector_store is None:

            self.vector_store = self.vector_service.load()

            self.retriever = self.vector_store.as_retriever(

                search_type="similarity",

                search_kwargs={
                    "k": self.top_k
                },
            )

    def retrieve(
        self,
        query: str,
    ) -> list[Document]:

        self._load_vector_store()

        return self.retriever.invoke(query)

    def retrieve_with_score(
        self,
        query: str,
        top_k: int = 4,
    ):

        self._load_vector_store()

        return self.vector_store.similarity_search_with_score(

            query=query,

            k=top_k,
        )