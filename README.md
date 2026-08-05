# MediGuru 🏥 — AI Medical Document Intelligence MVP

An AI-powered multi-modal medical document intelligence platform that extracts structured medical data, generates patient-friendly summaries, and enables interactive RAG Q&A using **FastAPI**, **Streamlit**, **Google Gemini 2.5 Flash Vision**, and **ChromaDB**.

---

## 📌 Features

### 📄 Multi-Format Document Ingestion
- Upload `.jpg`, `.jpeg`, `.png` images or `.pdf` documents.
- Supports handwritten prescriptions, diagnostic lab reports, and hospital summaries.

### 🤖 Pure AI Multimodal Vision Analysis (Gemini 2.5 Flash)
- **Zero Heavy OCR Dependencies**: Uses Google Gemini 2.5 Flash Multimodal Vision API directly for 2-second ultra-fast document extraction.
- Parses structured JSON containing:
  - Patient Name & Doctor Name
  - Diagnosis & Follow-up Details
  - Prescribed Medicines (Strength, Dosage, Frequency, Duration, Food Instructions, Purpose)
  - Lab Test Values & Reference Ranges

### 📝 AI Medical Summary
Generates a concise, patient-friendly medical summary highlighting condition, active prescriptions, and follow-up timelines.

### 🧠 Retrieval-Augmented Generation (RAG)
- Chunks document text and generates vector embeddings using **Mistral Embeddings** / `sentence-transformers`.
- Indexes embeddings in a session-scoped **temporary ChromaDB** instance (`temp/chroma`).
- Provides a conversational Streamlit chat interface to answer questions like:
  - *"What medicines should I take after food?"*
  - *"Explain my diagnosis in simple words."*
  - *"What are my lab test results?"*

### 🗑️ Session Privacy & Cleanup
Clicking **Clear Session** instantly purges uploaded documents, cached embeddings, and temporary ChromaDB collections so no medical data remains persisted.

---

## 🏗️ System Architecture

```text
Streamlit Frontend (frontend/app.py)
  │
  ├── Sidebar: Upload Image/PDF ──► Process Button ──► Clear Session Button
  ├── Main Display: AI Summary Box, Structured Reports (Patient, Doctor, Medicines Table, Labs)
  └── Interactive RAG Chat Widget
        │
        │ HTTP API Calls (8000)
        ▼
FastAPI Backend Engine (server/app/main.py)
  │
  ├── POST /process ──► Document Processor ──► Gemini 2.5 Flash Vision ──► Chunking & Embeddings ──► Temp ChromaDB
  ├── POST /chat    ──► RAG Retriever ──► Chroma Vector Similarity Search ──► Gemini Contextual Answer
  ├── POST /clear-session ──► Purge Temp Uploads & Reset ChromaDB Collection
  └── GET /health   ──► Server Status
```

---

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI (Python 3.12)
- **Frontend Framework**: Streamlit
- **Multimodal AI Engine**: Google Gemini API (`gemini-2.5-flash` Multimodal Vision)
- **Vector Database**: ChromaDB (Ephemeral / Temporary Session Storage)
- **Embeddings**: Mistral AI Embeddings (`mistral-embed`) / SentenceTransformers
- **PDF Extraction**: PyMuPDF (`fitz` / `pypdf`)

---

## 🚀 Getting Started

### 1. Setup Virtual Environment & Install Dependencies

```bash
# Clone the repository
git clone https://github.com/yourusername/MediGuru.git
cd MediGuru

# Create & activate python virtual environment
python -m venv server/.venv
source server/.venv/bin/activate   # On Linux/macOS
# server\.venv\Scripts\activate   # On Windows

# Install lightweight dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
MISTRAL_API_KEY=your_mistral_api_key_here
BACKEND_URL=http://localhost:8000
```

### 3. Run FastAPI Backend

```bash
uvicorn server.app.main:app --reload --port 8000
```

FastAPI Swagger documentation: [http://localhost:8000/docs](http://localhost:8000/docs).

### 4. Run Streamlit Frontend

In a new terminal tab:

```bash
streamlit run frontend/app.py
```

Streamlit web app: [http://localhost:8501](http://localhost:8501).

---

## 📜 License

MIT License. Created by Krishna Gupta.