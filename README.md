# MediGuru 🏥 — AI Medical Document Intelligence & RAG Assistant

An advanced, AI-powered medical document intelligence platform that extracts structured clinical data, generates executive patient summaries, validates health documents, and enables interactive RAG Q&A using **FastAPI**, **Vanilla JS / Tailwind CSS**, **Google Gemini 2.5 Flash Multimodal Vision**, **Mistral AI Embeddings**, and **ChromaDB**.

---

## 📌 Features

### 📄 Multimodal Document Ingestion & Validation
- Supports `.pdf` documents, `.jpg`, `.jpeg`, and `.png` images.
- Parses scanned medical prescriptions, lab diagnostic reports, discharge summaries, and clinical notes in **< 1.8 seconds**.
- **Non-Medical Document Detection**: Automatically validates uploaded files and flags non-medical documents (e.g. receipts, random photos, invoices) with an amber alert banner, skipping RAG vector indexing.

### 🤖 Pure AI Multimodal Vision Analysis (Gemini 2.5 Flash)
- **Zero Heavy OCR Dependencies**: Uses Google Gemini 2.5 Flash Multimodal Vision directly for ultra-fast document extraction.
- **Automatic Model Fallback**: If Gemini free-tier rate limits (HTTP 429) are reached on `gemini-2.5-flash`, the backend automatically retries requests using **`gemini-1.5-flash`**.
- Extracts structured JSON data including:
  - **Patient Name & Doctor Name**
  - **Diagnoses & Medical Conditions**
  - **Prescribed Medications Table** (Medicine Name, Strength, Dosage, Frequency, Food Instructions)
  - **Lab Test Results & Reference Values**
  - **Follow-up Plan & Instructions**

### 📝 Executive Medical Summary
- Automatically parses and formats clinical text into clean, structured sections (**Patient**, **Condition**, **Prescriptions**, **Lab Results**, **Follow-up**) without raw markdown syntax.

### 🧠 Retrieval-Augmented Generation (RAG) Chat Assistant
- Chunks document text and generates vector embeddings using **Mistral AI Embeddings (`mistral-embed`)**.
- Indexes vector embeddings in a session-scoped **temporary ChromaDB** vector store.
- Provides a responsive, interactive chat assistant for natural Q&A:
  - *"What medicines should I take after food?"*
  - *"Explain my diagnosis in simple words."*
  - *"What are the prescribed dosages and frequency?"*

### 🔒 Ephemeral Session Privacy & Automated Cleanup
- **Automatic Page Exit / Refresh Cleanup**: Implements `beforeunload` + `navigator.sendBeacon` hooks that automatically purge temporary ChromaDB vector collections and uploaded document files the moment a user leaves or refreshes the website.
- **Manual Clear Session**: One-click navbar control to immediately reset the UI and wipe temporary server storage.

---

## 🏗️ System Architecture

```text
Vanilla JS / Tailwind CSS Client (client/index.html & script.js)
  │
  ├── File Drag & Drop / Selection ──► Process Button ──► Clear Session Button
  ├── Left Column: Real-time Analysis Progress Timeline (PyMuPDF ➔ Gemini Vision ➔ Chroma RAG)
  └── Right Column: Structured AI Medical Summary & Interactive RAG Chat Widget
        │
        │ HTTP API Calls (8000)
        ▼
FastAPI Backend Engine (server/app/main.py)
  │
  ├── POST /process       ──► PyMuPDF / Gemini Vision ──► Medical Extraction ──► ChromaDB Vector Indexing
  ├── POST /chat          ──► RAG Retriever ──► Chroma Vector Search ──► Gemini Contextual Answer (with Fallback)
  ├── POST /clear-session ──► Purge Temp Uploads & Delete ChromaDB Vector Collection
  └── GET /health         ──► Server Health Check
```

---

## 🛠️ Tech Stack

- **Backend Framework**: Python FastAPI (`uvicorn`)
- **Frontend UI**: Vanilla HTML5, CSS (Tailwind CSS), JavaScript (Material 3 Icons & Layout)
- **Multimodal AI Engine**: Google Gemini API (`gemini-2.5-flash` / `gemini-1.5-flash`)
- **Vector Database**: ChromaDB (Ephemeral Session Storage)
- **Embedding Model**: Mistral AI Embeddings (`mistral-embed`)
- **PDF Extraction**: PyMuPDF (`fitz` / `pypdf`)

---

## 🚀 Getting Started

### 1. Repository Setup

```bash
git clone https://github.com/itskrishn07/MediGuru.git
cd MediGuru
```

### 2. Configure Backend Server

```bash
# Create and activate Python virtual environment
python -m venv server/.venv
source server/.venv/bin/activate    # On Linux/macOS
# server\.venv\Scripts\activate    # On Windows

# Install backend dependencies
pip install -r server/requirements.txt
```

Create a `.env` file in `server/app/.env`:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
MISTRAL_API_KEY=your_mistral_api_key_here
```

Start the FastAPI server:

```bash
cd server
uvicorn app.main:app --reload --port 8000
```

Backend API Swagger Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Run Web Client

In a new terminal:

```bash
cd client
npx serve
```

Web Client interface: [http://localhost:3000](http://localhost:3000) (or open `client/index.html` directly in browser).

---

## 🌐 Deployment Guide

### Deploy Web Client (`client/`)
- Host static files (`client/index.html`, `script.js`, `config.js`) for free on **Vercel**, **Netlify**, or **GitHub Pages**.
- Update `client/config.js` to point `API_BASE_URL` to your live backend endpoint.

### Deploy Backend Server (`server/`)
- Host the FastAPI server on **Render.com** or **Railway.app**.
- Set Environment Variables: `GOOGLE_API_KEY`, `MISTRAL_API_KEY`.
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## 📜 License

MIT License. Developed by Krishna Gupta.