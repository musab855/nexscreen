<div align="center">

# NexScreen

### AI-Powered Candidate Screening System

*Dynamically generates personalized technical interview questions using Retrieval-Augmented Generation*

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=flat&logo=react&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?style=flat&logo=postgresql&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-Embedding-001-4285F4?style=flat&logo=google&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-vector_DB-00CEC9?style=flat&logo=pinecone&logoColor=white)

</div>

---

## Live Demo

- **Frontend:** https://nexscreen-nu.vercel.app
- **Backend:** https://nexscreen-3m6j.onrender.com

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
        │  Gemini Embedding   │  query → 768-dim vector
        └────────┬────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │     Pinecone        │  semantic search over ML textbooks
        └────────┬────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │   Gemini (multi-    │  generates personalized question
        │   model fallback)   │
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
| Frontend | React 19 + Vite + TailwindCSS | UI |
| LLM | Google Gemini (multi-model fallback) | Question & report generation |
| Embeddings | Google Gemini `gemini-embedding-001` | 768-dim vectors, free tier API |
| Vector DB | Pinecone (384→768 dims, cosine) | Semantic search over textbooks |
| Database | PostgreSQL (Neon) | Session & Q&A persistence |
| ORM | SQLAlchemy 2.0 + Alembic | Database access & migrations |
| Retry Logic | Multi-model fallback (manual) | Cycles through 3 Gemini models on failure |

---

## Knowledge Base

The RAG pipeline is grounded in the following textbooks:

**AI / ML Engineer Role** (`ai_ml` namespace)
- Machine Learning — Tom Mitchell
- The Hundred-Page Machine Learning Book — Andriy Burkov
- Machine Learning for Absolute Beginners
- Pattern Recognition and Machine Learning — Christopher Bishop
- Artificial Intelligence, Machine Learning & Deep Learning

**Data Science / Applied ML Role** (`data_science` namespace)
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
│   │   ├── rag/                 # ingestion (Gemini embed), retriever (Gemini embed + Pinecone)
│   │   ├── db/                  # models, crud, database
│   │   ├── schemas/             # Pydantic request/response models
│   │   └── utils/               # logger, exceptions
│   ├── scripts/
│   │   └── ingest_knowledge_base.py
│   └── tests/                   # 7 tests: API, parser, full workflow
└── frontend/
    └── src/
        ├── pages/               # UploadPage, InterviewPage, ReportPage
        ├── services/            # Axios API calls
        └── context/             # SessionContext
```

---

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- A [Gemini API key](https://aistudio.google.com/app/apikey) (two recommended — one for LLM, one for embeddings)
- A [Pinecone](https://pinecone.io) API key (free tier)
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
GEMINI_API_KEY=your_llm_key
GEMINI_EMBEDDING_KEY=your_embedding_key
DATABASE_URL=postgresql://user:password@host:5432/nexscreen_db
SECRET_KEY=any_random_string
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX=nexscreen
```

Run the one-time knowledge base ingestion (only needed if setting up from scratch):

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

**Gemini Embedding over local sentence-transformers**
`gemini-embedding-001` runs on Google's servers — eliminates the local CPU bottleneck that made query embedding take 8-10s on free-tier hosting. 768 dimensions, free tier, `RETRIEVAL_QUERY`/`RETRIEVAL_DOCUMENT` task types.

**Pinecone over ChromaDB**
ChromaDB persists to local disk, which doesn't exist in fresh deployed containers — empty vector store on every deploy. Pinecone is cloud-hosted, so retrieval works regardless of where the backend runs.

**Multi-model Gemini fallback**
Instead of Tenacity retries, both `question_generator.py` and `report_generator.py` cycle through 3 Gemini models (`gemini-3.1-flash-lite` → `gemini-2.5-flash-lite` → `gemini-2.5-flash`). On `ServerError`/`ClientError`, it moves to the next model immediately — no sleep, no backoff.

**Separate API keys for LLM and embeddings**
Ingestion and query embedding use `GEMINI_EMBEDDING_KEY`, while LLM calls use `GEMINI_API_KEY`. This prevents ingestion from exhausting the quota that the app needs for real-time queries.

**Chunking strategy**
500-word chunks with 50-word overlap. Metadata (source, page, role) stored alongside each chunk for traceability.

**Stateless backend**
All session state lives in PostgreSQL, not in application memory. The backend is horizontally scalable by design.

---

<div align="center">
Built by <a href="https://github.com/musab855">Musab</a>
</div>
