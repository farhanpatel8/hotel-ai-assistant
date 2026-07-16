"""
Extraction Service

This module extracts structured reservation information
from natural language using the LLM.
"""

from datetime import date
from typing import Type

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from app.services.llm_service import get_llm


class ExtractionService:
    """
    Extracts structured data from user input.
    """

    EXTRACTION_PROMPT = """
You are an information extraction assistant.

Today's date:
{today}

Extract reservation information.

Return ONLY valid JSON.

Required JSON keys:

- full_name
- email
- room_type
- check_in_date
- check_out_date
- number_of_guests
- reservation_number

Rules:

- Missing values must be null.
- Dates must be YYYY-MM-DD.
- Resolve relative dates like tomorrow using today's date.
- Do not invent field names.
- Return ONLY JSON.

User Message:

{query}
"""

    def __init__(self):

        self.llm = get_llm()

    def extract(
        self,
        query: str,
        schema: Type[BaseModel],
    ):

        parser = JsonOutputParser()

        prompt = ChatPromptTemplate.from_template(
            self.EXTRACTION_PROMPT
        )

        chain = prompt | self.llm | parser

        data = chain.invoke(
            {
                "query": query,
                "today": date.today().isoformat(),
            }
        )

        if data is None:
            return schema()

        return schema.model_validate(data)