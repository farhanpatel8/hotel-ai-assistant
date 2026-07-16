"""
Reservation Service

Contains all business logic for reservation management.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.reservation import Reservation
from app.repositories.reservation_repository import ReservationRepository
from app.schemas.extraction import ReservationExtraction


class ReservationService:
    """
    Handles reservation business logic.
    """

    def __init__(self, db: Session):

        self.db = db

        self.repository = ReservationRepository(db)

    # ---------------------------------------------------------
    # Generate Reservation Number
    # ---------------------------------------------------------

    @staticmethod
    def generate_reservation_number() -> str:
        """
        Generates a unique reservation number.
        """

        date = datetime.now().strftime("%Y%m%d")

        unique = uuid4().hex[:6].upper()

        return f"HTL-{date}-{unique}"

    # ---------------------------------------------------------
    # Create Reservation
    # ---------------------------------------------------------

    def create(
        self,
        data: ReservationExtraction,
    ) -> Reservation:

        reservation = Reservation(

            reservation_number=self.generate_reservation_number(),

            full_name=data.full_name,

            email=data.email,

            room_type=data.room_type,

            check_in_date=data.check_in_date,

            check_out_date=data.check_out_date,

            number_of_guests=data.number_of_guests,

            status="Confirmed",
        )

        return self.repository.create(reservation)

    # ---------------------------------------------------------
    # View Reservation
    # ---------------------------------------------------------

    def view(
        self,
        reservation_number: str,
    ):

        return self.repository.get_by_number(
            reservation_number
        )

    # ---------------------------------------------------------
    # Cancel Reservation
    # ---------------------------------------------------------

    def cancel(
        self,
        reservation_number: str,
    ):

        reservation = self.repository.get_by_number(
            reservation_number
        )

        if reservation is None:

            return None

        self.repository.delete(reservation)

        return reservation