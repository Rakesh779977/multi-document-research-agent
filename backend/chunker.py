"""Intelligent text chunking with metadata preservation."""

from typing import List, Dict


def chunk_pages(
    pages: List[Dict],
    chunk_size: int = 800,
    chunk_overlap: int = 200,
) -> List[Dict]:
    """
    Split page-level text into smaller chunks while preserving metadata.

    Each chunk dict contains:
      { "doc_name", "page_number", "chunk_index", "text" }
    """
    chunks: List[Dict] = []
    global_idx = 0

    for page in pages:
        text = page["text"]
        doc_name = page["doc_name"]
        page_number = page["page_number"]

        # Split by sentences first for cleaner breaks
        sentences = _split_into_sentences(text)
        current_chunk = ""

        for sentence in sentences:
            # If adding this sentence would exceed chunk_size, save current chunk
            if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
                chunks.append({
                    "doc_name": doc_name,
                    "page_number": page_number,
                    "chunk_index": global_idx,
                    "text": current_chunk.strip(),
                })
                global_idx += 1
                # Keep overlap from the end of current chunk
                overlap_text = current_chunk[-chunk_overlap:] if len(current_chunk) > chunk_overlap else current_chunk
                current_chunk = overlap_text + sentence
            else:
                current_chunk += sentence

        # Don't forget the last chunk
        if current_chunk.strip():
            chunks.append({
                "doc_name": doc_name,
                "page_number": page_number,
                "chunk_index": global_idx,
                "text": current_chunk.strip(),
            })
            global_idx += 1

    return chunks


def _split_into_sentences(text: str) -> List[str]:
    """Simple sentence splitter."""
    import re
    # Split on sentence-ending punctuation followed by space or newline
    parts = re.split(r'(?<=[.!?])\s+', text)
    # Re-add trailing space for concatenation
    return [p + " " for p in parts]
