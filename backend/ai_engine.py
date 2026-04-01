"""AI analysis engine — Groq (LLaMA 3.3 70B) for reasoning, Google Gemini for embeddings."""

import os
import json
from typing import List, Dict
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Groq client — free tier: 14,400 requests/day, 30 RPM on llama-3.3-70b-versatile
GROQ_MODEL = "llama-3.3-70b-versatile"
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def answer_query(question: str, context_chunks: List[Dict], detail_mode: str = "detailed") -> Dict:
    """Answer a question using retrieved context chunks."""
    context_text = _format_context(context_chunks)

    detail_instruction = (
        "Give a concise 2-3 sentence answer."
        if detail_mode == "simple"
        else "Give a thorough, detailed answer with specific evidence."
    )

    prompt = f"""{detail_instruction}

QUESTION: {question}

CONTEXT:
{context_text}

Respond ONLY with valid JSON, no extra text:
{{
    "answer": "Your answer here",
    "confidence_score": 0.85,
    "why_this_answer": "Brief explanation of evidence used",
    "citations": [
        {{
            "doc_name": "document name",
            "page_number": 1,
            "snippet": "exact short quote"
        }}
    ]
}}"""

    return _call_llm(prompt)


def compare_documents(doc_chunks: Dict[str, List[Dict]]) -> Dict:
    """Compare key ideas across all documents."""
    context = ""
    for doc_name, chunks in doc_chunks.items():
        text = " ".join(c["text"][:200] for c in chunks[:5])
        context += f"\n\n--- {doc_name} ---\n{text}"

    prompt = f"""Compare these academic documents. Respond ONLY with valid JSON:
{{
    "comparison": {{
        "key_ideas": [
            {{
                "topic": "topic name",
                "documents": [
                    {{
                        "doc_name": "name",
                        "position": "what this doc says",
                        "snippet": "short quote"
                    }}
                ]
            }}
        ],
        "similarities": ["shared idea 1"],
        "differences": ["difference 1"],
        "summary": "Overall comparison"
    }},
    "citations": [{{"doc_name": "name", "page_number": 1, "snippet": "quote"}}],
    "confidence_score": 0.8
}}

DOCUMENTS:
{context}"""

    return _call_llm(prompt)


def detect_contradictions(doc_chunks: Dict[str, List[Dict]]) -> Dict:
    """Detect contradictions between documents."""
    context = ""
    for doc_name, chunks in doc_chunks.items():
        text = " ".join(c["text"][:200] for c in chunks[:5])
        context += f"\n\n--- {doc_name} ---\n{text}"

    prompt = f"""Find contradictions between these academic documents. Respond ONLY with valid JSON:
{{
    "contradictions": [
        {{
            "topic": "contradiction topic",
            "statement_a": {{
                "doc_name": "first doc",
                "statement": "what it says",
                "snippet": "exact quote"
            }},
            "statement_b": {{
                "doc_name": "second doc",
                "statement": "what it says",
                "snippet": "exact quote"
            }},
            "explanation": "why they conflict"
        }}
    ],
    "summary": "Overall summary of contradictions",
    "confidence_score": 0.8
}}

DOCUMENTS:
{context}"""

    return _call_llm(prompt)


def summarize_trends(doc_chunks: Dict[str, List[Dict]]) -> Dict:
    """Identify common themes and trends."""
    context = ""
    for doc_name, chunks in doc_chunks.items():
        text = " ".join(c["text"][:200] for c in chunks[:5])
        context += f"\n\n--- {doc_name} ---\n{text}"

    prompt = f"""Identify trends across these academic documents. Respond ONLY with valid JSON:
{{
    "trends": [
        {{
            "theme": "theme name",
            "description": "description",
            "supporting_documents": ["doc1"],
            "evidence": [{{"doc_name": "name", "snippet": "quote"}}]
        }}
    ],
    "unified_summary": "Comprehensive synthesis of all documents",
    "citations": [{{"doc_name": "name", "page_number": 1, "snippet": "quote"}}],
    "confidence_score": 0.8
}}

DOCUMENTS:
{context}"""

    return _call_llm(prompt)


def _format_context(chunks: List[Dict]) -> str:
    """Format top 5 chunks into context string, each truncated to 400 chars."""
    parts = []
    for c in chunks[:5]:
        text = c["text"][:400]
        parts.append(f"[Source: {c['doc_name']}, Page {c['page_number']}]\n{text}")
    return "\n\n".join(parts)


def _call_llm(prompt: str) -> Dict:
    """Call Groq API and parse JSON response."""
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a precise research analyst. Always respond with valid JSON only, no extra text, no markdown fences.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=1500,
        )

        content = response.choices[0].message.content.strip()
        # Strip markdown fences if model adds them anyway
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        return json.loads(content)

    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse AI response: {e}"}
    except Exception as e:
        return {"error": str(e)}
