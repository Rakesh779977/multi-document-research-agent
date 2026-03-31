"""
Multi-Document Research Agent — FastAPI Backend
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

from pdf_utils import extract_text_from_pdf
from chunker import chunk_pages
from vector_store import store
from ai_engine import answer_query, compare_documents, detect_contradictions, summarize_trends

app = FastAPI(
    title="Multi-Document Research Agent",
    description="AI-powered multi-document analysis with citation tracking",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response Models ──────────────────────────────────────────

class QueryRequest(BaseModel):
    question: str
    detail_mode: str = "detailed"  # "simple" | "detailed"
    top_k: int = 10


# ── Endpoints ──────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "ok", "message": "Multi-Document Research Agent API"}


@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """Upload one or more PDF files, extract text, chunk, and embed."""
    results = []

    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"{file.filename} is not a PDF")

        content = await file.read()
        doc_name = file.filename

        try:
            # Extract text page-by-page
            pages = extract_text_from_pdf(content, doc_name)
            if not pages:
                print(f"UPLOAD ERROR: No text extracted from {doc_name} (likely a scanned image or empty PDF)")
                results.append({"doc_name": doc_name, "status": "error", "message": "No text extracted"})
                continue

            # Chunk the pages
            chunks = chunk_pages(pages)

            # Add to vector store (embeds + indexes)
            store.add_chunks(chunks)

            print(f"UPLOAD SUCCESS: {doc_name} uploaded and embedded via Gemini")
            results.append({
                "doc_name": doc_name,
                "status": "success",
                "pages_extracted": len(pages),
                "chunks_created": len(chunks),
            })
        except Exception as e:
            print(f"UPLOAD EXCEPTION FOR {doc_name}: {str(e)}")
            results.append({"doc_name": doc_name, "status": "error", "message": f"Server crash during processing: {str(e)}"})
            continue

    return {"uploaded": results, "total_documents": len(store.get_documents())}


@app.get("/documents")
def list_documents():
    """List all uploaded documents."""
    return {"documents": store.get_documents()}


@app.delete("/documents/{doc_name}")
def delete_document(doc_name: str):
    """Remove a document from the store."""
    success = store.remove_document(doc_name)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "removed", "doc_name": doc_name}


@app.post("/query")
def query_documents(req: QueryRequest):
    """Ask a question across all documents. Returns answer + citations."""
    if not store.get_documents():
        raise HTTPException(status_code=400, detail="No documents uploaded yet")

    # Retrieve relevant chunks
    context_chunks = store.search(req.question, top_k=req.top_k)

    # Generate answer
    result = answer_query(req.question, context_chunks, detail_mode=req.detail_mode)
    return result


@app.post("/compare")
def compare():
    """Compare key ideas across all uploaded documents."""
    docs = store.get_documents()
    if len(docs) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 documents to compare")

    doc_chunks = {}
    for doc in docs:
        doc_chunks[doc["name"]] = store.get_all_chunks_for_doc(doc["name"])

    result = compare_documents(doc_chunks)
    return result


@app.post("/contradictions")
def find_contradictions():
    """Detect contradictions between uploaded documents."""
    docs = store.get_documents()
    if len(docs) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 documents to find contradictions")

    doc_chunks = {}
    for doc in docs:
        doc_chunks[doc["name"]] = store.get_all_chunks_for_doc(doc["name"])

    result = detect_contradictions(doc_chunks)
    return result


@app.post("/trends")
def find_trends():
    """Identify common themes and trends across all documents."""
    docs = store.get_documents()
    if not docs:
        raise HTTPException(status_code=400, detail="No documents uploaded yet")

    doc_chunks = {}
    for doc in docs:
        doc_chunks[doc["name"]] = store.get_all_chunks_for_doc(doc["name"])

    result = summarize_trends(doc_chunks)
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
