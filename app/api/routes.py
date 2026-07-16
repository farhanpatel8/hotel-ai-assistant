"""
API Routes

This module exposes REST APIs for the Hotel Assistant.
"""

import time

from fastapi import APIRouter

from app.agent.router import AIRouter
from app.schemas.chat import ChatRequest, ChatResponse


router = APIRouter(
    prefix="/api/v1",
    tags=["Hotel Assistant"],
)

# Create only once
ai_router = AIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "HotelGPT Assistant",
    }


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):

    start = time.time() 

    result = ai_router.route(request.question)

    print(f"Total Time: {time.time() - start:.2f} sec")

    return result