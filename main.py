"""
Main Application

Entry point for the HotelGPT AI Assistant.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router

from app.database.db import init_db

from app.services.indexing_service import IndexingService


PDF_PATH = "data/hotel_rag_document_v2.pdf"


# ---------------------------------------------------------
# Application Startup
# ---------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initializes required application resources.
    """

    # Create database tables
    init_db()

    # Build FAISS index (only first time)
    indexing_service = IndexingService(PDF_PATH)
    indexing_service.build_vector_store()

    yield

    # Future cleanup (if required)


# ---------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------
app = FastAPI(

    title="HotelGPT AI Assistant",

    description="AI-powered Hotel Reservation Assistant using RAG and Tool Calling.",

    version="1.0.0",

    lifespan=lifespan,
)

# ---------------------------------------------------------
# Register Routes
# ---------------------------------------------------------
app.include_router(router)


# ---------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------
@app.get("/")
def root():
    """
    Root endpoint.
    """

    return {
        "application": "HotelGPT AI Assistant",
        "status": "running",
        "docs": "/docs",
    }