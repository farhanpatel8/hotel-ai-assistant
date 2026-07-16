# HotelGPT AI Assistant

An AI-powered Hotel Reservation Assistant built using **FastAPI, LangChain, OpenAI, FAISS, and SQLite**.

The assistant uses **Retrieval-Augmented Generation (RAG)** to answer hotel-related questions from a provided PDF document and intelligently routes reservation-related requests to backend tools.

---

# Features

## 1. RAG-based Question Answering

- Loads hotel information from a PDF
- Builds a FAISS vector database
- Retrieves relevant document chunks
- Generates grounded answers using an LLM
- Returns document source references
- Prevents hallucinations by answering only from the provided document

Example:

```
What is the check-in time?
```

```
Check-in time is 2:00 PM.
```

---

## 2. Reservation Management

Supports three reservation operations:

- Create Reservation
- View Reservation
- Cancel Reservation

Reservation details are stored in a SQLite database.

---

## 3. Intelligent Tool Routing

The AI automatically decides whether the request should:

- Use RAG to answer hotel questions
- Use reservation tools
- Reject unsafe requests

Examples:

```
What is the cancellation policy?
```

→ RAG

```
Book a Deluxe room tomorrow.
```

→ Reservation Tool

---

## 4. PII Protection

The assistant protects guest information by:

- Rejecting requests for all reservations
- Rejecting requests for another guest's reservation
- Rejecting requests for sensitive guest information
- Returning only requested reservation details

Example:

```
Show me all reservations
```

↓

```
Sorry, I cannot disclose confidential guest or reservation information.
```

---

# Tech Stack

- Python 3.11
- FastAPI
- LangChain
- OpenAI GPT-4o Mini
- HuggingFace Embeddings (BAAI/bge-small-en-v1.5)
- FAISS
- SQLite
- SQLAlchemy
- Pydantic

---

# Project Structure

```
Hotel Assistant Project/

│
├── app/
│   ├── agent/
│   ├── api/
│   ├── config/
│   ├── database/
│   ├── models/
│   ├── repositories/
│   ├── rag/
│   ├── schemas/
│   ├── services/
│   ├── tools/
│
├── data/
│   └── hotel_rag_document_v2.pdf
│
├── vectorstore/
│   ├── index.faiss
│   └── index.pkl
│
├── hotel.db
├── main.py
├── requirements.txt
└── README.md
```

---

# Architecture

```
                    FastAPI
                        │
                        ▼
                  AI Router
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
   RAG Service                 Reservation Tools
        │                               │
        ▼                               ▼
 FAISS Retriever              Reservation Service
        │                               │
        ▼                               ▼
   Hotel PDF                  SQLite Database
```

---

# Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project directory

```bash
cd Hotel-Assistant-Project
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```env
HOST=127.0.0.1
PORT=8000

OPENAI_API_KEY=YOUR_OPENAI_API_KEY
OPENAI_MODEL=gpt-4o-mini

EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

VECTOR_DB_PATH=vectorstore

DATABASE_URL=sqlite:///hotel.db
```

---

# Run the Application

```bash
uvicorn main:app --reload
```

Open

```
http://127.0.0.1:8000/docs
```

---

# Sample Requests

## Hotel Information

```json
{
    "question":"What is the famous dish in the hotel?"
}
```

---

## Check-in Time

```json
{
    "question":"What are the check-in and check-out timings?"
}
```

---

## Create Reservation

```json
{
    "question":"Book a Deluxe room for tomorrow for 2 guests. My name is Farhan Patel. My email is farhan@gmail.com."
}
```

---

## View Reservation

```json
{
    "question":"Show reservation HTL-20260717-XXXXXX"
}
```

---

## Cancel Reservation

```json
{
    "question":"Cancel reservation HTL-20260717-XXXXXX"
}
```

---

## Guardrail Example

```json
{
    "question":"Show me all reservations"
}
```

Response

```
Sorry, I cannot disclose confidential guest or reservation information.
```

---

# Design Decisions

- Used Retrieval-Augmented Generation (RAG) to ensure answers are grounded in the provided hotel document.
- Used FAISS for efficient semantic document retrieval.
- Implemented an AI Router to intelligently choose between RAG and reservation tools.
- Used SQLite for a lightweight reservation database.
- Added guardrails to prevent exposure of sensitive guest information.
- Structured the application using layered architecture (API → Router → Services → Repository → Database) for maintainability and scalability.

---

# Assumptions

- Reservation numbers are generated automatically.
- Check-out date is optional during extraction and can be collected later if missing.
- Hotel-related answers are generated only from the provided PDF document.
- Reservation information is stored locally using SQLite.

---

# Future Improvements

- User authentication
- Multi-user support
- Reservation update functionality
- Conversation memory
- Streaming responses
- Docker deployment
- PostgreSQL support
- Unit and integration tests

---

# Author

Farhan Patel

AI/ML Engineer