"""
Reservation Tools

Tool layer responsible for executing reservation actions.
"""

from sqlalchemy.orm import Session

from app.schemas.extraction import ReservationExtraction
from app.services.reservation_service import ReservationService


class ReservationTools:
    """
    Executes reservation operations.
    """

    def __init__(self, db: Session):

        self.service = ReservationService(db)

    # ---------------------------------------------------------
    # Create Reservation
    # ---------------------------------------------------------

    def create_reservation(
        self,
        reservation: ReservationExtraction,
    ) -> dict:
        """
        Creates a reservation.
        """

        result = self.service.create(reservation)

        return {
            "reservation_number": result.reservation_number,
            "status": result.status,
            "full_name": result.full_name,
            "email": result.email,
            "room_type": result.room_type,
            "check_in_date": result.check_in_date,
            "check_out_date": result.check_out_date,
            "number_of_guests": result.number_of_guests,
        }

    # ---------------------------------------------------------
    # View Reservation
    # ---------------------------------------------------------

    def view_reservation(
        self,
        reservation_number: str,
    ) -> dict:
        """
        Returns reservation details.
        """

        reservation = self.service.view(reservation_number)

        if reservation is None:

            return {
                "success": False,
                "message": "Reservation not found.",
            }

        return {
            "success": True,
            "reservation_number": reservation.reservation_number,
            "status": reservation.status,
            "full_name": reservation.full_name,
            "email": reservation.email,
            "room_type": reservation.room_type,
            "check_in_date": reservation.check_in_date,
            "check_out_date": reservation.check_out_date,
            "number_of_guests": reservation.number_of_guests,
        }

    # ---------------------------------------------------------
    # Cancel Reservation
    # ---------------------------------------------------------

    def cancel_reservation(
        self,
        reservation_number: str,
    ) -> dict:
        """
        Cancels a reservation.
        """

        reservation = self.service.cancel(reservation_number)

        if reservation is None:

            return {
                "success": False,
                "message": "Reservation not found.",
            }

        return {
            "success": True,
            "message": "Reservation cancelled successfully.",
            "reservation_number": reservation.reservation_number,
        }