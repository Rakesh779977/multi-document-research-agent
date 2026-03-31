"""FAISS vector store management with metadata mapping."""

import numpy as np
from typing import List, Dict, Optional, Any
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class VectorStore:
    """In-memory Vector index using pure NumPy."""

    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        self.vectors: Optional[np.ndarray] = None
        self.metadata: List[Dict[str, Any]] = []  # parallel array: metadata[i] ↔ vector i
        self.documents: Dict[str, Dict[str, Any]] = {}  # doc_name → { name, num_pages, num_chunks }

    def add_chunks(self, chunks: List[Dict]) -> None:
        """Embed chunks and add to vector store."""
        if not chunks:
            return

        texts = [c["text"] for c in chunks]
        embeddings = self._get_embeddings(texts)
        
        # Normalize embeddings for cosine similarity
        new_vecs = np.array(embeddings, dtype="float32")
        norms = np.linalg.norm(new_vecs, axis=1, keepdims=True)
        new_vecs = new_vecs / (norms + 1e-10)

        if self.vectors is None:
            self.vectors = new_vecs
        else:
            self.vectors = np.vstack([self.vectors, new_vecs])
            
        self.metadata.extend(chunks)

        # Track document info
        for chunk in chunks:
            doc_name = chunk["doc_name"]
            if doc_name not in self.documents:
                self.documents[doc_name] = {
                    "name": doc_name,
                    "num_pages": 0,
                    "num_chunks": 0,
                }
            self.documents[doc_name]["num_chunks"] += 1
            self.documents[doc_name]["num_pages"] = max(
                self.documents[doc_name]["num_pages"], int(chunk["page_number"])
            )

    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """Search for the most similar chunks to the query using cosine similarity."""
        if self.vectors is None or len(self.metadata) == 0:
            return []

        query_embedding = self._get_embeddings([query])[0]
        query_vector = np.array(query_embedding, dtype="float32")
        query_vector = query_vector / (np.linalg.norm(query_vector) + 1e-10)

        # Cosine similarity (dot product of normalized vectors)
        similarities = np.dot(self.vectors, query_vector)
        
        # Get top-k indices
        k = min(top_k, len(self.metadata))
        # argpartition is faster than argsort for top-k
        indices = np.argpartition(similarities, -k)[-k:]
        # Sort the top-k exactly
        indices = indices[np.argsort(similarities[indices])[::-1]]

        results = []
        for idx in indices:
            meta: Dict[str, Any] = dict(self.metadata[idx])
            # For cosine sim, higher is better. Convert to distance-like score or just return it
            meta["score"] = float(similarities[idx])
            results.append(meta)

        return results

    def get_all_chunks_for_doc(self, doc_name: str) -> List[Dict]:
        """Return all chunks belonging to a specific document."""
        return [m for m in self.metadata if m["doc_name"] == doc_name]

    def get_all_chunks(self) -> List[Dict]:
        """Return all chunks across all documents."""
        return list(self.metadata)

    def get_documents(self) -> List[Dict]:
        """List all uploaded documents."""
        return list(self.documents.values())

    def remove_document(self, doc_name: str) -> bool:
        """Remove a document and rebuild the store."""
        if doc_name not in self.documents:
            return False

        # Filter out chunks for this document
        new_metadata = [m for m in self.metadata if m["doc_name"] != doc_name]

        # Rebuild index
        self.vectors = None
        self.metadata = []
        self.documents.pop(doc_name, None)

        if new_metadata:
            self.add_chunks(new_metadata)

        return True

    def _get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings in small batches from Gemini API."""
        all_embeddings = []
        batch_size = 100  # Gemini limits batch size to 100 texts

        for i in range(0, len(texts), batch_size):
            batch = texts[i: i + batch_size]
            response = genai.embed_content(
                model="models/text-embedding-004",
                content=batch
            )
            all_embeddings.extend(response['embedding'])

        return all_embeddings


# Global singleton
store = VectorStore()
