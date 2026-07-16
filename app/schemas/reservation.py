"""
Pydantic Schemas

Defines request and response models for Reservation APIs.
"""

from datetime import date
from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field


# ------------------------------------------------------------------
# User
# ------------------------------------------------------------------
class UserBase(BaseModel):
    """Shared user fields."""

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Guest Full Name",
    )

    email: EmailStr


# ------------------------------------------------------------------
# Create Reservation Request
# ------------------------------------------------------------------
class ReservationCreate(UserBase):
    """Request body for creating a reservation."""

    room_type: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    check_in_date: date

    check_out_date: date

    number_of_guests: int = Field(
        ...,
        ge=1,
        le=10,
    )


# ------------------------------------------------------------------
# Reservation Response
# ------------------------------------------------------------------
class ReservationResponse(BaseModel):
    """Reservation response returned to the client."""

    model_config = ConfigDict(from_attributes=True)

    reservation_number: str

    room_type: str

    check_in_date: date

    check_out_date: date

    number_of_guests: int

    reservation_status: str

    created_at: datetime


# ------------------------------------------------------------------
# Reservation Lookup
# ------------------------------------------------------------------
class ReservationLookup(BaseModel):
    """Lookup reservation by reservation number and email."""

    reservation_number: str = Field(
        ...,
        min_length=5,
        max_length=30,
    )

    email: EmailStr


# ------------------------------------------------------------------
# Cancel Reservation
# ------------------------------------------------------------------
class ReservationCancel(BaseModel):
    """Cancel reservation request."""

    reservation_number: str

    email: EmailStr


# ------------------------------------------------------------------
# Generic API Response
# ------------------------------------------------------------------
class MessageResponse(BaseModel):
    """Simple message response."""

    message: str