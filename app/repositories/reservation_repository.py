"""
Reservation Repository

Handles all database operations related to reservations.
"""

from sqlalchemy.orm import Session

from app.models.reservation import Reservation


class ReservationRepository:

    def __init__(self, db: Session):
        self.db = db

    # ---------------------------------------------------------
    # Create Reservation
    # ---------------------------------------------------------

    def create(self, reservation: Reservation):

        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)

        return reservation

    # ---------------------------------------------------------
    # Get Reservation
    # ---------------------------------------------------------

    def get_by_number(
        self,
        reservation_number: str,
    ):

        return (
            self.db.query(Reservation)
            .filter(
                Reservation.reservation_number == reservation_number
            )
            .first()
        )

    # ---------------------------------------------------------
    # Delete Reservation
    # ---------------------------------------------------------

    def delete(
        self,
        reservation: Reservation,
    ):

        self.db.delete(reservation)
        self.db.commit()