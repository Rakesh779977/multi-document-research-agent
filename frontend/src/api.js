const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function uploadDocuments(files) {
  const formData = new FormData();
  for (const file of files) {
    formData.append("files", file);
  }
  const res = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Upload failed");
  }
  return res.json();
}

export async function getDocuments() {
  const res = await fetch(`${API_BASE}/documents`);
  return res.json();
}

export async function deleteDocument(docName) {
  const res = await fetch(`${API_BASE}/documents/${encodeURIComponent(docName)}`, {
    method: "DELETE",
  });
  return res.json();
}

export async function queryDocuments(question, detailMode = "detailed", topK = 10) {
  const res = await fetch(`${API_BASE}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, detail_mode: detailMode, top_k: topK }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Query failed");
  }
  return res.json();
}

export async function compareDocuments() {
  const res = await fetch(`${API_BASE}/compare`, { method: "POST" });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Compare failed");
  }
  return res.json();
}

export async function findContradictions() {
  const res = await fetch(`${API_BASE}/contradictions`, { method: "POST" });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Contradictions check failed");
  }
  return res.json();
}

export async function summarizeTrends() {
  const res = await fetch(`${API_BASE}/trends`, { method: "POST" });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Trends summarization failed");
  }
  return res.json();
}
