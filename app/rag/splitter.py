"""
Document Splitter

Splits loaded documents into semantic chunks
for embedding and retrieval.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class DocumentSplitter:
    """
    Splits LangChain documents into smaller chunks.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150,
    ):

        self.text_splitter = RecursiveCharacterTextSplitter(

            chunk_size=chunk_size,

            chunk_overlap=chunk_overlap,

            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
            ],

            length_function=len,
        )

    def split(
        self,
        documents: list[Document],
    ) -> list[Document]:
        """
        Split documents into chunks.

        Parameters
        ----------
        documents : list[Document]

        Returns
        -------
        list[Document]
        """

        chunks = self.text_splitter.split_documents(
            documents
        )

        return chunks