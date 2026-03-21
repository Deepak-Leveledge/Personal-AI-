const AgentStatus = ({ updates, isLoading }) => {
  if (!isLoading && updates.length === 0) return null;

  return (
    <div
      style={{
        margin: "4px 0 14px 46px",
        padding: "12px 14px",
        background: "rgba(247, 242, 232, 0.92)",
        borderRadius: "16px",
        border: "1px solid #ddd4c0",
        fontSize: "13px",
        maxWidth: "560px",
      }}
    >
      {updates.map((update, index) => (
        <div
          key={`${update}-${index}`}
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            padding: "3px 0",
            color: "#5f5a50",
          }}
        >
          <span style={{ color: "#4f7a2c", fontSize: "12px" }}>OK</span>
          <span>{update}</span>
        </div>
      ))}

      {isLoading && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            padding: "4px 0 2px",
            color: "#7f7664",
            marginTop: updates.length ? "4px" : "0",
          }}
        >
          <svg
            width="13"
            height="13"
            viewBox="0 0 12 12"
            style={{ animation: "spin 1s linear infinite", flexShrink: 0 }}
          >
            <circle
              cx="6"
              cy="6"
              r="5"
              fill="none"
              stroke="#ddd4c0"
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
          <span>Working on your answer...</span>
        </div>
      )}

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default AgentStatus;
