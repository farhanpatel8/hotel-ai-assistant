"""
Extraction Schemas

These schemas are used only for extracting structured
information from natural language using the LLM.

All fields are optional because the user may provide
partial information in a single message.
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field


class ReservationExtraction(BaseModel):
    """
    Reservation information extracted from the user's message.
    """

    model_config = ConfigDict(
        extra="ignore"
    )

    full_name: Optional[str] = Field(
        default=None,
        description="Guest full name",
    )

    email: Optional[EmailStr] = Field(
        default=None,
        description="Guest email",
    )

    room_type: Optional[str] = Field(
        default=None,
        description="Room type requested by the guest",
    )

    check_in_date: Optional[date] = Field(
        default=None,
        description="Check-in date",
    )

    check_out_date: Optional[date] = Field(
        default=None,
        description="Check-out date",
    )

    number_of_guests: Optional[int] = Field(
        default=None,
        ge=1,
        le=10,
        description="Number of guests",
    )

    reservation_number: Optional[str] = Field(
        default=None,
        description="Reservation number",
    )   