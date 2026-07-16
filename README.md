# MediGuru 🏥

## AI-Powered Multi-Modal Medical Document Analyzer using OCR, LLMs & RAG

An end-to-end AI application that intelligently analyzes doctor prescriptions, medical lab reports, and healthcare documents from images and PDFs using OCR, Gemini 2.5 Flash, PostgreSQL, and ChromaDB.

## 📌 Overview

MediGuru is an AI-powered medical document intelligence platform that transforms unstructured medical documents into structured, searchable, and interactive knowledge.

Users can upload handwritten prescriptions, scanned reports, or digital PDFs. The system extracts text using OCR, understands the medical information using Google's Gemini LLM, stores structured information in PostgreSQL, generates embeddings for semantic search using ChromaDB, and enables users to chat with their reports using Retrieval-Augmented Generation (RAG).

## 🚀 Features

### 📄 Multi-Format Document Support
- Upload Images (`.jpg`, `.jpeg`, `.png`)
- Upload PDFs
- Supports:
  - Doctor Prescriptions
  - Medical Reports
  - Diagnostic Reports
  - Laboratory Reports

### 🔍 Intelligent OCR Pipeline
- PaddleOCR
- Native Text Extraction for Digital PDFs
- Automatic OCR Fallback for Scanned PDFs
- High Accuracy Text Recognition

### 🤖 AI-Powered Medical Information Extraction
Using Gemini 2.5 Flash, the application extracts:
- Patient Name
- Doctor Name
- Medicines
- Dosage
- Frequency
- Duration
- Food Instructions
- Lab Values
- Diagnosis
- Follow-up Instructions

### 📋 Structured JSON Generation

Example:
```json
{
    "patient_name":"John Doe",
    "doctor_name":"Dr Sharma",
    "medicines":[
        {
            "medicine_name":"Paracetamol 650",
            "dosage":"1 Tablet",
            "frequency":"Twice Daily",
            "duration":"5 Days",
            "food_instruction":"After Food"
        }
    ]
}
```

### 📝 AI Medical Summary

Generate an easy-to-understand summary of complex medical reports.

Example:
> The patient is diagnosed with viral fever. The prescribed medicines should be taken twice daily after food. Follow-up is scheduled after 7 days.

### 🧠 Retrieval Augmented Generation (RAG)

Users can ask questions like:
- What medicines am I taking?
- What are my abnormal lab values?
- When should I visit the doctor again?
- Explain my diagnosis in simple language.
- Compare this report with my previous report.

### 💾 PostgreSQL Storage

Stores:
- Extracted Reports
- Patient Information
- Medicines
- Metadata
- AI Generated Summary

### 🔍 Semantic Search using ChromaDB

The extracted medical text is:
- Chunked
- Embedded
- Stored inside ChromaDB

This enables semantic retrieval for contextual question answering.

### 📊 Intelligent Chat

Users can chat with their uploaded reports using Retrieval-Augmented Generation.

## 🏗️ System Architecture

```text
                           User
                             │
                             ▼
                   Upload Image / PDF
                             │
                             ▼
                    FastAPI Backend
                             │
                             ▼
                  Document Processor
             ┌───────────────┴────────────────┐
             ▼                                ▼
      Image Service                     PDF Service
             │                                │
             └───────────────┬────────────────┘
                             ▼
                       OCR Service
      (PaddleOCR / Native PDF Extraction)
                             │
                             ▼
                      Extracted Text
                             │
             ┌───────────────┴────────────────┐
             ▼                                ▼
         Gemini LLM                    Chunking Service
             │                                │
             ▼                                ▼
     Structured JSON                 Embedding Service
             │                                │
             ▼                                ▼
       PostgreSQL                     ChromaDB
             │                                │
             └───────────────┬────────────────┘
                             ▼
                    Retrieval Service
                             │
                             ▼
                       Chat Service
                             │
                             ▼
                     AI Generated Answer
```

## 🧠 AI Pipeline

```text
Upload Document

↓

Detect Document Type

↓

Image / PDF Processing

↓

OCR / Native Text Extraction

↓

Gemini Medical Information Extraction

↓

Structured JSON

↓

Generate Medical Summary

↓

Store in PostgreSQL

↓

Chunk Document

↓

Generate Embeddings

↓

Store in ChromaDB

↓

Retrieve Relevant Chunks

↓

Generate Context-Aware Answers
```

## 🛠️ Tech Stack

- **Backend**
  - FastAPI
  - Python 3.12
- **OCR**
  - PaddleOCR
- **LLM**
  - Gemini 2.5 Flash
- **Database**
  - PostgreSQL
- **Vector Database**
  - ChromaDB
- **AI**
  - LangChain
- **RAG**
  - Prompt Engineering
- **PDF Processing**
  - PyMuPDF
- **Data Validation**
  - Pydantic
- **Logging**
  - Python Logging

## 📂 Project Structure

```text
server/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── prompts/
│   ├── services/
│   ├── vectorstore/
│   ├── main.py
│   └── .env
│
├── chroma_db/
│
├── uploads/
│
├── requirements.txt
└── .gitignore
```

## ⚙️ Installation

Clone the repository
```bash
git clone https://github.com/yourusername/MediGuru.git
```

Move into the project
```bash
cd MediGuru/server
```

Create a virtual environment
```bash
python -m venv .venv
```

Activate it

**Windows**
```cmd
.venv\Scripts\activate
```

**Linux / macOS**
```bash
source .venv/bin/activate
```

Install dependencies
```bash
pip install -r requirements.txt
```

Create a `.env` file
```env
GEMINI_API_KEY=YOUR_API_KEY
DATABASE_URL=YOUR_DATABASE_URL
```

Run the server
```bash
uvicorn app.main:app --reload
```

## 📡 API

### Upload Document
`POST /upload`

Upload
- Image
- PDF

Returns
- Extracted Text
- Structured JSON
- Medical Summary

### Chat with Reports
`POST /chat`

Example
```json
{
    "question":"What medicines am I taking?"
}
```

## 📈 Future Enhancements

- React Frontend
- User Authentication
- Medical History Dashboard
- Voice-based Medical Assistant
- Multi-language OCR
- Report Comparison Timeline
- Medicine Interaction Detection
- Drug Recommendation Warnings
- Cloud Storage Integration (AWS S3 / Supabase Storage)
- Docker Deployment
- CI/CD Pipeline
- Admin Analytics Dashboard

## 🎯 Learning Outcomes

This project demonstrates practical experience with:
- FastAPI Backend Development
- OCR Pipelines
- Large Language Models (LLMs)
- Prompt Engineering
- Structured Output Generation
- Retrieval-Augmented Generation (RAG)
- Vector Databases
- PostgreSQL
- AI System Design
- Modular Software Architecture
- Production-Oriented Backend Development

## 📜 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Krishna Gupta**

B.Tech Computer Science Engineering (AI, ML & DL)

Aspiring AI Engineer | Generative AI | Machine Learning | Backend Development

⭐ If you found this project interesting, consider giving it a star on GitHub!