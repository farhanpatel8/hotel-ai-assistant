"""
AI Router

Responsible for:

1. Guardrails
2. Intent Detection
3. RAG Routing
4. Reservation Routing
"""
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.tools.reservation_tools import ReservationTools
from langchain_core.prompts import ChatPromptTemplate

from app.agent.prompts import (
    GUARDRAIL_PROMPT,
    ROUTING_PROMPT,
)

from app.services.llm_service import get_llm
from app.services.rag_service import RAGService
from app.services.extraction_service import ExtractionService

from app.schemas.extraction import (
    ReservationExtraction,
)


class AIRouter:
    """
    Main decision engine for the Hotel Assistant.
    """

    VALID_INTENTS = {

        "HOTEL_INFORMATION",

        "CREATE_RESERVATION",

        "VIEW_RESERVATION",

        "CANCEL_RESERVATION",

        "UNKNOWN",
    }

    def __init__(self):

        self.llm = get_llm()

        self.rag = RAGService()

        self.extractor = ExtractionService()

    # ---------------------------------------------------------
    # Intent Detection
    # ---------------------------------------------------------

    def detect_intent(
        self,
        question: str,
    ) -> str:

        prompt = ChatPromptTemplate.from_template(
            ROUTING_PROMPT
        )

        chain = prompt | self.llm

        response = chain.invoke(
            {
                "question": question
            }
        )

        intent = self._get_text(response).upper()

        if intent not in self.VALID_INTENTS:
            return "UNKNOWN"

        return intent

    # ---------------------------------------------------------
    # Guardrails
    # ---------------------------------------------------------

    def guardrail(
        self,
        question: str,
    ) -> bool:

        prompt = ChatPromptTemplate.from_template(
            GUARDRAIL_PROMPT
        )

        chain = prompt | self.llm

        response = chain.invoke(
            {
                "question": question
            }
        )

        text = self._get_text(response)

        return text.upper() == "REJECT"

    # ---------------------------------------------------------
    # Route Request
    # ---------------------------------------------------------

    def route(
        self,
        question: str,
    ) -> dict:

        # -------------------------
        # Guardrail
        # -------------------------

        if self.guardrail(question):

            return {

                "action": "guardrail",

                "message":
                    "Sorry, I cannot disclose confidential guest or reservation information.",
            }

        # -------------------------
        # Intent Detection
        # -------------------------

        intent = self.detect_intent(question)

        # -------------------------
        # Hotel Information
        # -------------------------

        if intent == "HOTEL_INFORMATION":

            answer = self.rag.ask(question)

            return {

                "action": "rag",

                "data": answer,
            }

        # -------------------------
        # Create Reservation
        # -------------------------

        if intent == "CREATE_RESERVATION":

            reservation = self.extractor.extract(
                query=question,
                schema=ReservationExtraction,
            )

            # -------------------------
            # Validate Required Fields
            # -------------------------

            required_fields = {
                "full_name": reservation.full_name,
                "email": reservation.email,
                "room_type": reservation.room_type,
                "check_in_date": reservation.check_in_date,
                "number_of_guests": reservation.number_of_guests,
            }

            missing = [
                field.replace("_", " ")
                for field, value in required_fields.items()
                if value is None
            ]

            if missing:
                return {
                    "action": "missing_information",
                    "message": f"Please provide: {', '.join(missing)}"
                }

            db: Session = SessionLocal()

            try:

                tool = ReservationTools(db)

                result = tool.create_reservation(reservation)

                return {

                    "action": "create_reservation",

                    "data": result,

                    "message": "Reservation created successfully.",
                }

            finally:

                db.close()

        # -------------------------
        # View Reservation
        # -------------------------

        if intent == "VIEW_RESERVATION":

            reservation = self.extractor.extract(

                query=question,

                schema=ReservationExtraction,
            )

            db: Session = SessionLocal()

            try:

                tool = ReservationTools(db)

                result = tool.view_reservation(
                    reservation.reservation_number
                )

                return {

                    "action": "view_reservation",

                    "data": result,

                    "message": None,
                }

            finally:

                db.close()

        # -------------------------
        # Cancel Reservation
        # -------------------------

        if intent == "CANCEL_RESERVATION":

            reservation = self.extractor.extract(

                query=question,

                schema=ReservationExtraction,
            )

            db: Session = SessionLocal()

            try:

                tool = ReservationTools(db)

                result = tool.cancel_reservation(
                    reservation.reservation_number
                )

                return {

                    "action": "cancel_reservation",

                    "data": result,

                    "message": None,
                }

            finally:

                db.close()

        # -------------------------
        # Unknown
        # -------------------------

        return {

            "action": "unknown",

            "message":
                "I can assist only with hotel information and reservations.",
        }
    

    @staticmethod
    def _get_text(response) -> str:
        """
        Converts LangChain response into plain text.
        Supports Gemini/OpenAI response formats.
        """

        content = response.content

        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):

            text = []

            for item in content:

                if isinstance(item, dict):
                    text.append(item.get("text", ""))

                elif hasattr(item, "text"):
                    text.append(str(item.text))

                else:
                    text.append(str(item))

            return "".join(text).strip()

        return str(content).strip()