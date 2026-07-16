"""
Database CRUD Operations

This module contains all database operations related to
Users and Reservations.
"""

from uuid import uuid4

from sqlalchemy.orm import Session

from app.database.models import Reservation
from app.database.models import User
from app.schemas.reservation import ReservationCreate


# ------------------------------------------------------------------
# User Operations
# ------------------------------------------------------------------
def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Returns a user by email.
    """

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def create_user(
    db: Session,
    full_name: str,
    email: str,
) -> User:
    """
    Creates a new user.
    """

    user = User(
        full_name=full_name,
        email=email,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# ------------------------------------------------------------------
# Reservation Operations
# ------------------------------------------------------------------
def generate_reservation_number() -> str:
    """
    Generates a unique reservation number.
    """

    return f"HTL-{uuid4().hex[:8].upper()}"


def create_reservation(
    db: Session,
    reservation: ReservationCreate,
) -> Reservation:
    """
    Creates a reservation.

    If the user does not exist,
    a new user is created.
    """

    user = get_user_by_email(
        db,
        reservation.email,
    )

    if user is None:

        user = create_user(
            db=db,
            full_name=reservation.full_name,
            email=reservation.email,
        )

    booking = Reservation(

        reservation_number=generate_reservation_number(),

        user_id=user.id,

        room_type=reservation.room_type,

        check_in_date=reservation.check_in_date,

        check_out_date=reservation.check_out_date,

        number_of_guests=reservation.number_of_guests,

        reservation_status="BOOKED",
    )

    db.add(booking)

    db.commit()

    db.refresh(booking)

    return booking


def get_reservation(
    db: Session,
    reservation_number: str,
    email: str,
) -> Reservation | None:
    """
    Returns reservation only if
    reservation belongs to the given email.
    """

    return (
        db.query(Reservation)
        .join(User)
        .filter(
            Reservation.reservation_number == reservation_number,
            User.email == email,
        )
        .first()
    )


def cancel_reservation(
    db: Session,
    reservation_number: str,
    email: str,
) -> Reservation | None:
    """
    Cancels an existing reservation.
    """

    booking = get_reservation(
        db,
        reservation_number,
        email,
    )

    if booking is None:
        return None

    if booking.reservation_status == "CANCELLED":
        return booking

    booking.reservation_status = "CANCELLED"

    db.commit()

    db.refresh(booking)

    return booking