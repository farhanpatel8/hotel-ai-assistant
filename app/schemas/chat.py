"""
Chat Schemas

Defines request and response models
for the Hotel Assistant.
"""

from pydantic import BaseModel
from pydantic import Field
from typing import Any

class ChatRequest(BaseModel):
    """
    User chat request.
    """

    question: str = Field(
        ...,
        min_length=2,
        max_length=1000,
        description="User question for the hotel assistant.",
    )



class ChatResponse(BaseModel):
    """
    Standard response returned by AIRouter.
    """

    action: str

    data: Any | None = None

    message: str | None = None