export default function CitationPanel({ citations }) {
  return (
    <aside className="citation-panel">
      <div className="citation-header">
        <h2>📎 Citations & References</h2>
      </div>

      <div className="citation-list">
        {(!citations || citations.length === 0) ? (
          <div className="citation-empty">
            <span style={{ fontSize: "1.8rem", opacity: 0.4 }}>📑</span>
            <p>Citations will appear here when you query your documents.</p>
          </div>
        ) : (
          citations.map((c, i) => (
            <div key={i} className="citation-item">
              <div className="citation-source">
                <span className="citation-doc-name">{c.doc_name}</span>
                {c.page_number && (
                  <span className="citation-page">p.{c.page_number}</span>
                )}
              </div>
              <div className="citation-snippet">"{c.snippet}"</div>
            </div>
          ))
        )}
      </div>
    </aside>
  );
}
