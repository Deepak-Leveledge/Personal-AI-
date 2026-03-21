const steps = {
  general: ["🤔 Thinking..."],
  websearch: [
    "🔍 Searching the web...",
    "📊 Analyzing results...",
    "✍️ Writing answer...",
  ],
  rag: [
    "📚 Searching documents...",
    "🔍 Finding relevant chunks...",
    "✍️ Writing answer...",
  ],
  github: [
    "🐙 Connecting to GitHub...",
    "📂 Fetching data...",
    "✍️ Writing answer...",
  ],
  notion: [
    "📝 Connecting to Notion...",
    "🔍 Searching pages...",
    "✍️ Writing answer...",
  ],
};

const AgentStatus = ({ updates, isLoading }) => {
  if (!isLoading && updates.length === 0) return null;

  return (
    <div
      style={{
        margin: "0 24px 12px",
        padding: "10px 14px",
        background: "#f9f8f5",
        borderRadius: "10px",
        border: "0.5px solid #d3d1c7",
        fontSize: "13px",
      }}
    >
      {updates.map((u, i) => (
        <div
          key={i}
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            padding: "3px 0",
            color: "#5f5e5a",
          }}
        >
          <span style={{ color: "#3b6d11", fontSize: "11px" }}>✓</span>
          <span>{u}</span>
        </div>
      ))}

      {isLoading && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            padding: "3px 0",
            color: "#888780",
            marginTop: updates.length ? "4px" : "0",
          }}
        >
          {/* Animated spinner */}
          <svg
            width="12"
            height="12"
            viewBox="0 0 12 12"
            style={{ animation: "spin 1s linear infinite", flexShrink: 0 }}
          >
            <circle
              cx="6"
              cy="6"
              r="5"
              fill="none"
              stroke="#d3d1c7"
              strokeWidth="1.5"
            />
            <path
              d="M6 1 A5 5 0 0 1 11 6"
              fill="none"
              stroke="#c96442"
              strokeWidth="1.5"
              strokeLinecap="round"
            />
          </svg>
          <span>Working...</span>
        </div>
      )}

      <style>{`
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        @keyframes bounce {
          0%, 100% { transform: translateY(0); }
          50%       { transform: translateY(-3px); }
        }
      `}</style>
    </div>
  );
};

export default AgentStatus;
