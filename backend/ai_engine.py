"""AI analysis engine — OpenAI-powered reasoning with structured outputs."""

import os
import json
from typing import List, Dict
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("OPENAI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")


def answer_query(question: str, context_chunks: List[Dict], detail_mode: str = "detailed") -> Dict:
    """
    Answer a question using retrieved context chunks.
    Returns structured response with citations, confidence, and explanation.
    """
    context_text = _format_context(context_chunks)

    detail_instruction = (
        "Provide a concise, high-level summary answer."
        if detail_mode == "simple"
        else "Provide a thorough, detailed analysis with specific evidence."
    )

    prompt = f"""You are a research assistant analyzing multiple academic documents.
Answer the following question using ONLY the provided context.

{detail_instruction}

QUESTION: {question}

CONTEXT:
{context_text}

Respond in valid JSON:
{{
    "answer": "Your answer (2-3 sentences)",
    "confidence_score": 0.0,
    "why_this_answer": "Brief explanation",
    "citations": [
        {{
            "doc_name": "document name",
            "page_number": 1,
            "snippet": "short quote"
        }}
    ]
}}"""

    return _call_llm(prompt)


def compare_documents(doc_chunks: Dict[str, List[Dict]]) -> Dict:
    """
    Compare key ideas across all documents.
    doc_chunks: { doc_name: [chunk_dicts] }
    """
    context = ""
    for doc_name, chunks in doc_chunks.items():
        text = " ".join(c["text"] for c in chunks[:10])  # Limit per doc
        context += f"\n\n--- DOCUMENT: {doc_name} ---\n{text}"

    prompt = f"""You are a research analyst comparing multiple academic documents.

DOCUMENTS:
{context}

Analyze and compare these documents. Respond in valid JSON:
{{
    "comparison": {{
        "key_ideas": [
            {{
                "topic": "topic/theme name",
                "documents": [
                    {{
                        "doc_name": "document name",
                        "position": "what this document says about the topic",
                        "snippet": "relevant quote"
                    }}
                ]
            }}
        ],
        "similarities": ["list of shared ideas or conclusions"],
        "differences": ["list of differing viewpoints or findings"],
        "summary": "Overall comparison summary"
    }},
    "citations": [
        {{
            "doc_name": "document name",
            "page_number": 1,
            "snippet": "relevant quote"
        }}
    ],
    "confidence_score": 0.0 to 1.0
}}
"""

    return _call_llm(prompt)


def detect_contradictions(doc_chunks: Dict[str, List[Dict]]) -> Dict:
    """
    Detect contradictions between documents.
    """
    context = ""
    for doc_name, chunks in doc_chunks.items():
        text = " ".join(c["text"] for c in chunks[:10])
        context += f"\n\n--- DOCUMENT: {doc_name} ---\n{text}"

    prompt = f"""You are a research analyst looking for contradictions between academic documents.

DOCUMENTS:
{context}

Find any contradicting or conflicting statements between the documents.
Respond in valid JSON:
{{
    "contradictions": [
        {{
            "topic": "what the contradiction is about",
            "statement_a": {{
                "doc_name": "first document name",
                "statement": "what document A says",
                "snippet": "exact quote from document A"
            }},
            "statement_b": {{
                "doc_name": "second document name",
                "statement": "what document B says",
                "snippet": "exact quote from document B"
            }},
            "explanation": "why these statements conflict"
        }}
    ],
    "summary": "Overall summary of contradictions found (or 'No significant contradictions found')",
    "confidence_score": 0.0 to 1.0
}}

If no contradictions exist, return an empty contradictions array with an appropriate summary.
"""

    return _call_llm(prompt)


def summarize_trends(doc_chunks: Dict[str, List[Dict]]) -> Dict:
    """
    Identify common themes and trends, generate unified summary.
    """
    context = ""
    for doc_name, chunks in doc_chunks.items():
        text = " ".join(c["text"] for c in chunks[:10])
        context += f"\n\n--- DOCUMENT: {doc_name} ---\n{text}"

    prompt = f"""You are a research analyst identifying trends across multiple academic documents.

DOCUMENTS:
{context}

Identify common themes, trends, and patterns. Respond in valid JSON:
{{
    "trends": [
        {{
            "theme": "theme/trend name",
            "description": "description of this trend",
            "supporting_documents": ["list of doc names that support this trend"],
            "evidence": [
                {{
                    "doc_name": "document name",
                    "snippet": "supporting quote"
                }}
            ]
        }}
    ],
    "unified_summary": "A comprehensive summary synthesizing insights from all documents",
    "citations": [
        {{
            "doc_name": "document name",
            "page_number": 1,
            "snippet": "relevant quote"
        }}
    ],
    "confidence_score": 0.0 to 1.0
}}
"""

    return _call_llm(prompt)


def _format_context(chunks: List[Dict]) -> str:
    """Format chunks into a readable context string.
    
    Chunks are truncated to 300 chars to stay under Gemini free tier token limits.
    Only the top 5 most relevant chunks are used.
    """
    parts = []
    for c in chunks[:5]:  # Only use top 5 chunks
        # Truncate text to keep token count low
        text = c['text'][:300]
        parts.append(
            f"[Source: {c['doc_name']}, Page {c['page_number']}]\n{text}"
        )
    return "\n\n".join(parts)


def _call_llm(prompt: str) -> Dict:
    """Call Gemini API and parse JSON response."""
    try:
        response = model.generate_content(
            f"You are a precise research analyst. Always respond with valid JSON only, no extra text.\n\n{prompt}",
            generation_config={"response_mime_type": "application/json", "temperature": 0.2}
        )
        return json.loads(response.text)

    except json.JSONDecodeError:
        return {"error": "Failed to parse AI response", "raw": response.text if response else ""}
    except Exception as e:
        return {"error": str(e)}
