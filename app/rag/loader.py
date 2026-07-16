"""
PDF Loader

Responsible for loading the hotel PDF document.

Returns:
    List[Document]
"""

from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


class PDFLoader:
    """
    Loads PDF documents using LangChain's PyPDFLoader.
    """

    def __init__(self, pdf_path: str):

        self.pdf_path = Path(pdf_path)

    def load(self) -> list[Document]:
        """
        Load the PDF document.

        Returns
        -------
        list[Document]

        Raises
        ------
        FileNotFoundError
            If PDF file does not exist.
        """

        if not self.pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {self.pdf_path}"
            )

        loader = PyPDFLoader(str(self.pdf_path))

        documents = loader.load()

        if not documents:
            raise ValueError(
                "No content found inside the PDF."
            )

        return documents