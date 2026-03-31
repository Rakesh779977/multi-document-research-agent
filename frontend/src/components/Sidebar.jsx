import { useRef } from "react";

export default function Sidebar({
  documents,
  onUpload,
  onRemove,
  onCompare,
  onContradictions,
  onTrends,
  uploading,
  loading,
}) {
  const fileRef = useRef(null);

  const handleFiles = (e) => {
    const files = e.target.files;
    if (files.length) onUpload(Array.from(files));
    e.target.value = "";
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>📄 Documents</h2>
        <button
          className={`upload-btn ${uploading ? "uploading" : ""}`}
          onClick={() => fileRef.current?.click()}
          disabled={uploading}
        >
          {uploading ? "⏳ Uploading…" : "＋ Upload PDFs"}
        </button>
        <input
          ref={fileRef}
          type="file"
          accept=".pdf"
          multiple
          hidden
          onChange={handleFiles}
        />
      </div>

      <div className="doc-list">
        {documents.length === 0 && (
          <p style={{ padding: "20px 12px", color: "var(--text-muted)", fontSize: "0.8rem", textAlign: "center" }}>
            No documents uploaded yet.
            <br />
            Upload PDFs to get started.
          </p>
        )}
        {documents.map((doc) => (
          <div key={doc.name} className="doc-item">
            <div className="doc-icon">PDF</div>
            <div className="doc-info">
              <div className="doc-name" title={doc.name}>{doc.name}</div>
              <div className="doc-meta">
                {doc.num_pages} pages · {doc.num_chunks} chunks
              </div>
            </div>
            <button
              className="doc-remove"
              onClick={() => onRemove(doc.name)}
              title="Remove"
            >
              ✕
            </button>
          </div>
        ))}
      </div>

      <div className="sidebar-actions">
        <button
          className="action-btn compare"
          onClick={onCompare}
          disabled={documents.length < 2 || loading}
        >
          <span className="icon">🔍</span> Compare Documents
        </button>
        <button
          className="action-btn contradict"
          onClick={onContradictions}
          disabled={documents.length < 2 || loading}
        >
          <span className="icon">⚠️</span> Find Contradictions
        </button>
        <button
          className="action-btn trends"
          onClick={onTrends}
          disabled={documents.length < 1 || loading}
        >
          <span className="icon">📊</span> Summarize Trends
        </button>
      </div>
    </aside>
  );
}
