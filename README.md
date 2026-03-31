# 🔬 Multi-Document Research Agent

> AI-powered cross-document analysis that compares research papers, detects contradictions, and provides explainable, citation-backed insights.

## ✨ Features

- **Multi-Document Upload** — Upload multiple PDFs at once
- **Deep Q&A** — Ask questions answered using context from ALL documents
- **Cross-Document Comparison** — Compare key ideas, similarities & differences
- **Contradiction Detection** — Find conflicting statements between papers
- **Trend Summarization** — Identify common themes across all documents
- **Citation Tracking** — Every answer includes document name, page number, exact snippet
- **Explainable AI** — "Why this answer?" section with extracted evidence
- **Confidence Score** — Visual indicator of answer reliability
- **Simple/Detailed Toggle** — Switch between summary and in-depth analysis

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite |
| Backend | Python + FastAPI |
| AI/LLM | OpenAI GPT-4o-mini |
| Embeddings | OpenAI text-embedding-3-small |
| Vector DB | FAISS (in-memory) |

## 📁 Project Structure

```
├── backend/
│   ├── main.py           # FastAPI app & endpoints
│   ├── pdf_utils.py      # PDF text extraction
│   ├── chunker.py        # Text chunking
│   ├── vector_store.py   # FAISS index management
│   ├── ai_engine.py      # OpenAI reasoning engine
│   ├── requirements.txt  # Python dependencies
│   └── .env              # API key (create this)
├── frontend/
│   └── src/
│       ├── App.jsx        # Main app component
│       ├── api.js         # API client
│       ├── index.css      # Design system
│       └── components/
│           ├── Sidebar.jsx
│           ├── QueryPanel.jsx
│           └── CitationPanel.jsx
└── README.md
```

## 🚀 Setup Instructions

### Prerequisites

- **Node.js** 18+ (for frontend)
- **Python** 3.9+ (for backend)
- **OpenAI API key** ([Get one here](https://platform.openai.com/api-keys))

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure API key
# Edit .env file and replace sk-your-api-key-here with your actual key
notepad .env

# Start the server
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies (already done if you used create-vite)
npm install

# Start dev server
npm run dev
```

The app will be available at `http://localhost:5173`

### 3. Use the App

1. Open `http://localhost:5173` in your browser
2. Click **"+ Upload PDFs"** in the left sidebar
3. Select one or more PDF files
4. Once uploaded, you can:
   - **Ask questions** using the center input
   - Click **"Compare Documents"** for cross-document analysis
   - Click **"Find Contradictions"** for conflict detection
   - Click **"Summarize Trends"** for theme identification
5. Citations appear in the right panel

## 📄 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload` | Upload PDF files |
| GET | `/documents` | List uploaded documents |
| DELETE | `/documents/{name}` | Remove a document |
| POST | `/query` | Ask a question |
| POST | `/compare` | Compare all documents |
| POST | `/contradictions` | Detect contradictions |
| POST | `/trends` | Summarize trends |

## 💡 Tips

- Upload **2+ documents** to enable comparison and contradiction features
- Use the **Simple/Detailed toggle** to control answer depth
- Check the **"Why this answer?"** dropdown for reasoning transparency
- The **confidence score** helps evaluate answer reliability

## ⚠️ Notes

- FAISS index is **in-memory** — restarting the backend clears all data
- Each upload embeds text using OpenAI API (costs ~$0.001 per document)
- GPT-4o-mini is used for reasoning (~$0.01 per query)
