"""
Database Models

This module defines all ORM models used in the application.
"""

from datetime import datetime

from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.db import Base


# ------------------------------------------------------------------
# User Model
# ------------------------------------------------------------------
class User(Base):
    """
    Stores guest information.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


# ------------------------------------------------------------------
# Reservation Model
# ------------------------------------------------------------------
class Reservation(Base):
    """
    Stores hotel reservations.
    """

    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    reservation_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    room_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    check_in_date: Mapped[Date] = mapped_column(
        Date,
        nullable=False,
    )

    check_out_date: Mapped[Date] = mapped_column(
        Date,
        nullable=False,
    )

    number_of_guests: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    reservation_status: Mapped[str] = mapped_column(
        String(30),
        default="BOOKED",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="reservations",
    )