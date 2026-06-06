<div align="center">

# NexScreen

### AI-Powered Candidate Screening System

*Dynamically generates personalized technical interview questions using Retrieval-Augmented Generation*

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?style=flat&logo=postgresql&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-4285F4?style=flat&logo=google&logoColor=white)

</div>

---

## What is NexScreen?

NexScreen simulates a structured technical interview where questions are **not predefined** — they are generated dynamically based on three inputs:

- The candidate's uploaded resume
- Their selected target role
- A role-specific knowledge base built from ML/AI textbooks

No two interviews are the same.

---

## System Architecture

```
Candidate uploads Resume (PDF) + selects Role
                    │
                    ▼
        ┌─────────────────────┐
        │   Resume Parser     │  PyMuPDF → extract text, skills, name
        └────────┬────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │   Query Builder     │  resume + role → retrieval query
        └────────┬────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │     ChromaDB        │  semantic search over ML textbooks
        └────────┬────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │  Gemini 2.5 Flash   │  generates personalized question
        └────────┬────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │  Interview Session  │  5 questions, answers persisted in PostgreSQL
        └────────┬────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │  Evaluation Report  │  score, strengths, areas for improvement
        └─────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | FastAPI (Python 3.11) | API server, business logic |
| Frontend | React 18 + Vite + TailwindCSS | UI |
| LLM | Google Gemini 2.5 Flash | Question & report generation |
| Embeddings | sentence-transformers `all-MiniLM-L6-v2` | Local, free, no API cost |
| Vector DB | ChromaDB | Semantic search over textbooks |
| Database | PostgreSQL (Neon) | Session & Q&A persistence |
| ORM | SQLAlchemy + Alembic | Database access & migrations |
| Retry Logic | Tenacity | Handles Gemini 503/429 gracefully |

---

## Knowledge Base

The RAG pipeline is grounded in the following textbooks:

**AI / ML Engineer Role**
- Machine Learning — Tom Mitchell
- The Hundred-Page Machine Learning Book — Andriy Burkov
- Machine Learning for Absolute Beginners
- Pattern Recognition and Machine Learning — Christopher Bishop
- Artificial Intelligence, Machine Learning & Deep Learning

**Data Science / Applied ML Role**
- Introduction to Machine Learning with Python
- Master Machine Learning Algorithms — Jason Brownlee

---

## Project Structure

```
nexscreen/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/          # resume, session, interview, report
│   │   ├── core/                # resume_parser, query_builder, question_generator, report_generator
│   │   ├── rag/                 # ingestion, retriever, embedder
│   │   ├── db/                  # models, crud, database
│   │   ├── schemas/             # Pydantic request/response models
│   │   └── utils/               # logger, exceptions
│   └── scripts/
│       └── ingest_knowledge_base.py
└── frontend/
    └── src/
        ├── pages/               # UploadPage, InterviewPage, ReportPage
        ├── components/          # UI components
        ├── services/            # Axios API calls
        └── context/             # SessionContext
```

---

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- A [Gemini API key](https://aistudio.google.com/app/apikey)
- A PostgreSQL database ([Neon](https://neon.tech) free tier works)

### Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your values:

```bash
GEMINI_API_KEY=your_key_here
DATABASE_URL=postgresql://user:password@host:5432/nexscreen_db
SECRET_KEY=any_random_string
```

Run the one-time knowledge base ingestion:

```bash
python scripts/ingest_knowledge_base.py
```

Start the server:

```bash
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173`

### Docker

```bash
docker-compose up --build
```

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/resume/upload` | Upload and parse resume PDF |
| `POST` | `/api/v1/session/start` | Create interview session |
| `GET` | `/api/v1/interview/{id}/next` | Get next generated question |
| `POST` | `/api/v1/interview/{id}/answer` | Submit answer |
| `GET` | `/api/v1/report/{id}` | Get structured evaluation report |
| `GET` | `/health` | Health check |

---

## Key Design Decisions

**ChromaDB over Pinecone**
ChromaDB runs embedded inside the FastAPI process with zero external dependencies. For a knowledge base of 7 textbooks it provides fast semantic search without the operational overhead of a managed vector service.

**Local embeddings over OpenAI embeddings**
`all-MiniLM-L6-v2` runs entirely on-device. No API cost, no network latency during ingestion, and strong semantic similarity performance for technical text.

**Chunking strategy**
500-token chunks with 50-token overlap. Large enough to preserve sentence context, small enough to keep retrieval granular. Metadata (source, page, role) stored alongside each chunk for traceability.

**Stateless backend**
All session state lives in PostgreSQL, not in application memory. The backend is horizontally scalable by design.

**Retry logic**
Tenacity wraps all Gemini API calls with exponential backoff — short waits (5–30s) for 503 server overload, longer waits (60–120s) for 429 rate limits. The frontend surfaces a retry button instead of silently failing.

---

## Demo

> Video walkthrough coming soon.

---

<div align="center">
Built by <a href="https://github.com/musab855">Musab</a>
</div>
