"""
Reservation ORM Model
"""

from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.db import Base


class Reservation(Base):
    """
    Reservation table.
    """

    __tablename__ = "reservations"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    reservation_number = Column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    full_name = Column(
        String(100),
        nullable=False,
    )

    email = Column(
        String(255),
        nullable=False,
    )

    room_type = Column(
        String(50),
        nullable=False,
    )

    check_in_date = Column(
        Date,
        nullable=True,
    )

    check_out_date = Column(
        Date,
        nullable=True,
    )

    number_of_guests = Column(
        Integer,
        nullable=False,
    )

    status = Column(
        String(20),
        nullable=False,
        default="Confirmed",
    )