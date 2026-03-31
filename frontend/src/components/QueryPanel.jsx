import { useState } from "react";

export default function QueryPanel({
  response,
  responseType,
  loading,
  error,
  onSubmitQuery,
  detailMode,
  onToggleMode,
}) {
  const [question, setQuestion] = useState("");
  const [showWhy, setShowWhy] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (question.trim()) {
      onSubmitQuery(question.trim());
    }
  };

  return (
    <main className="query-panel">
      {/* Input Area */}
      <div className="query-input-area">
        <form className="query-row" onSubmit={handleSubmit}>
          <input
            className="query-input"
            type="text"
            placeholder="Ask a question across all documents…"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            disabled={loading}
          />
          <button className="query-submit" type="submit" disabled={loading || !question.trim()}>
            {loading ? "Analyzing…" : "Ask AI"}
          </button>
        </form>
        <div className="query-controls">
          <div className="toggle-group">
            <span>Simple</span>
            <button
              className={`toggle ${detailMode === "detailed" ? "active" : ""}`}
              onClick={onToggleMode}
              type="button"
            />
            <span>Detailed</span>
          </div>
        </div>
      </div>

      {/* Response Area */}
      <div className="response-area">
        {loading && (
          <div className="loading">
            <div className="spinner" />
            <div className="loading-text">
              {responseType === "query" && "Searching documents & generating answer…"}
              {responseType === "compare" && "Comparing documents…"}
              {responseType === "contradictions" && "Detecting contradictions…"}
              {responseType === "trends" && "Analyzing trends…"}
              {!responseType && "Processing…"}
            </div>
          </div>
        )}

        {error && <div className="error-msg">⚠️ {error}</div>}

        {!loading && !error && !response && (
          <div className="empty-state">
            <div className="emoji">🔬</div>
            <p>
              Upload research documents and ask questions, compare ideas, detect
              contradictions, or discover trends across all your papers.
            </p>
          </div>
        )}

        {!loading && !error && response && responseType === "query" && (
          <QueryResponse response={response} showWhy={showWhy} setShowWhy={setShowWhy} />
        )}

        {!loading && !error && response && responseType === "compare" && (
          <CompareResponse response={response} />
        )}

        {!loading && !error && response && responseType === "contradictions" && (
          <ContradictionResponse response={response} />
        )}

        {!loading && !error && response && responseType === "trends" && (
          <TrendsResponse response={response} />
        )}
      </div>
    </main>
  );
}

/* ── Sub-components ─────────────────────────────────────────────────── */

function QueryResponse({ response, showWhy, setShowWhy }) {
  const score = response.confidence_score ?? 0;
  const pct = Math.round(score * 100);
  const level = score >= 0.7 ? "high" : score >= 0.4 ? "medium" : "low";

  return (
    <div className="response-card">
      <div className="response-label">AI Answer</div>
      <div className="response-answer">{response.answer}</div>

      {/* Confidence Bar */}
      <div className="confidence-bar-wrapper">
        <div className="confidence-label">
          <span>Confidence Score</span>
          <span>{pct}%</span>
        </div>
        <div className="confidence-track">
          <div className={`confidence-fill ${level}`} style={{ width: `${pct}%` }} />
        </div>
      </div>

      {/* Why this answer */}
      {response.why_this_answer && (
        <div className="why-section">
          <button className="why-toggle" onClick={() => setShowWhy(!showWhy)}>
            {showWhy ? "▾" : "▸"} Why this answer?
          </button>
          {showWhy && <div className="why-content">{response.why_this_answer}</div>}
        </div>
      )}
    </div>
  );
}

function CompareResponse({ response }) {
  const comp = response.comparison || response;
  const topics = comp.key_ideas || [];
  const similarities = comp.similarities || [];
  const differences = comp.differences || [];

  return (
    <div className="response-card">
      <div className="response-label">🔍 Cross-Document Comparison</div>

      {comp.summary && (
        <div className="response-answer" style={{ marginBottom: 16 }}>{comp.summary}</div>
      )}

      <div className="comparison-topics">
        {topics.map((t, i) => (
          <div key={i} className="topic-block">
            <div className="topic-name">{t.topic}</div>
            {(t.documents || []).map((d, j) => (
              <div key={j} className="topic-doc">
                <div className="topic-doc-name">{d.doc_name}</div>
                <div className="topic-doc-pos">{d.position}</div>
              </div>
            ))}
          </div>
        ))}
      </div>

      {similarities.length > 0 && (
        <div className="sim-diff-section">
          <div className="sim-diff-label sim">✓ Similarities</div>
          <ul className="sim-diff-list sim">
            {similarities.map((s, i) => <li key={i}>{s}</li>)}
          </ul>
        </div>
      )}

      {differences.length > 0 && (
        <div className="sim-diff-section">
          <div className="sim-diff-label diff">✗ Differences</div>
          <ul className="sim-diff-list diff">
            {differences.map((d, i) => <li key={i}>{d}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
}

function ContradictionResponse({ response }) {
  const contradictions = response.contradictions || [];

  return (
    <div className="response-card">
      <div className="response-label">⚠️ Contradiction Detection</div>
      {response.summary && (
        <div className="response-answer" style={{ marginBottom: 16 }}>{response.summary}</div>
      )}

      {contradictions.length === 0 ? (
        <p style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
          No contradictions detected between the documents.
        </p>
      ) : (
        <div className="contradictions-list">
          {contradictions.map((c, i) => (
            <div key={i} className="contradiction-card">
              <div className="contradiction-topic">⚡ {c.topic}</div>
              <div className="contradiction-body">
                <div className="statement-col">
                  <div className="statement-label a">Statement A</div>
                  <div className="statement-doc">{c.statement_a?.doc_name}</div>
                  <div className="statement-text">"{c.statement_a?.snippet || c.statement_a?.statement}"</div>
                </div>
                <div className="statement-col">
                  <div className="statement-label b">Statement B</div>
                  <div className="statement-doc">{c.statement_b?.doc_name}</div>
                  <div className="statement-text">"{c.statement_b?.snippet || c.statement_b?.statement}"</div>
                </div>
              </div>
              <div className="contradiction-explanation">
                <strong>Explanation: </strong>{c.explanation}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function TrendsResponse({ response }) {
  const trends = response.trends || [];

  return (
    <div className="response-card">
      <div className="response-label">📊 Trend Summarization</div>
      {response.unified_summary && (
        <div className="response-answer" style={{ marginBottom: 16 }}>{response.unified_summary}</div>
      )}

      <div className="trends-list">
        {trends.map((t, i) => (
          <div key={i} className="trend-card">
            <div className="trend-theme">{t.theme}</div>
            <div className="trend-desc">{t.description}</div>
            <div className="trend-docs">
              {(t.supporting_documents || []).map((d, j) => (
                <span key={j} className="trend-doc-tag">{d}</span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
