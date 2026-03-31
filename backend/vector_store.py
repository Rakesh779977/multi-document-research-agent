"""FAISS vector store management with metadata mapping."""

import numpy as np
import faiss
from typing import List, Dict, Optional
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = "text-embedding-3-small"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class VectorStore:
    """In-memory FAISS index with metadata mapping."""

    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata: List[Dict] = []  # parallel array: metadata[i] ↔ vector i
        self.documents: Dict[str, Dict] = {}  # doc_name → { name, num_pages, num_chunks }

    def add_chunks(self, chunks: List[Dict]) -> None:
        """Embed chunks and add to FAISS index."""
        if not chunks:
            return

        texts = [c["text"] for c in chunks]
        embeddings = self._get_embeddings(texts)
        vectors = np.array(embeddings, dtype="float32")

        self.index.add(vectors)
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
                self.documents[doc_name]["num_pages"], chunk["page_number"]
            )

    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """Search for the most similar chunks to the query."""
        if self.index.ntotal == 0:
            return []

        query_embedding = self._get_embeddings([query])[0]
        query_vector = np.array([query_embedding], dtype="float32")

        distances, indices = self.index.search(query_vector, min(top_k, self.index.ntotal))

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < 0:
                continue
            meta = self.metadata[idx].copy()
            meta["score"] = float(dist)
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
        """Remove a document and rebuild the FAISS index."""
        if doc_name not in self.documents:
            return False

        # Filter out chunks for this document
        new_metadata = [m for m in self.metadata if m["doc_name"] != doc_name]

        # Rebuild index
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []
        del self.documents[doc_name]

        if new_metadata:
            self.add_chunks(new_metadata)

        return True

    def _get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings from OpenAI API in batches."""
        all_embeddings = []
        batch_size = 100

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            response = client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=batch,
            )
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)

        return all_embeddings


# Global singleton
store = VectorStore()
