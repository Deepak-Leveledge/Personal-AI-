import ReactMarkdown from "react-markdown";

const bubbleBase = {
  maxWidth: "min(760px, 80%)",
  borderRadius: "22px",
  padding: "14px 16px",
  boxShadow: "0 10px 24px rgba(75, 61, 38, 0.08)",
  border: "1px solid transparent",
};

const avatarStyle = {
  width: "34px",
  height: "34px",
  borderRadius: "12px",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  fontSize: "12px",
  fontWeight: 700,
  flexShrink: 0,
  marginTop: "2px",
};

const typingDotStyle = {
  width: "8px",
  height: "8px",
  background: "#8f8572",
  borderRadius: "50%",
  animation: "bubbleBounce 0.9s infinite ease-in-out",
};

const MessageBubble = ({ message, sources }) => {
  const isUser = message.role === "user";
  const isTyping = !message.content && !isUser;

  return (
    <div
      style={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        gap: "12px",
        marginBottom: "18px",
      }}
    >
      {!isUser && (
        <div
          style={{
            ...avatarStyle,
            background: "linear-gradient(135deg, #c96442 0%, #9f4f34 100%)",
            color: "#fffaf4",
          }}
        >
          AI
        </div>
      )}

      <div
        style={{
          ...bubbleBase,
          background: isUser ? "#c96442" : "rgba(255, 252, 245, 0.94)",
          color: isUser ? "#fffaf4" : "#2c2924",
          borderColor: isUser ? "#c96442" : "#e0d9ca",
          borderTopRightRadius: isUser ? "8px" : bubbleBase.borderRadius,
          borderTopLeftRadius: isUser ? bubbleBase.borderRadius : "8px",
        }}
      >
        {isUser ? (
          <p style={{ whiteSpace: "pre-wrap" }}>{message.content}</p>
        ) : isTyping ? (
          <div style={{ display: "flex", gap: "6px", padding: "4px 0" }}>
            {[0, 150, 300].map((delay) => (
              <span
                key={delay}
                style={{ ...typingDotStyle, animationDelay: `${delay}ms` }}
              />
            ))}
          </div>
        ) : (
          <div style={{ fontSize: "14px", lineHeight: 1.7 }}>
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
        )}

        {!isUser && sources?.length > 0 && (
          <div
            style={{
              marginTop: "14px",
              paddingTop: "12px",
              borderTop: "1px solid #e4ddcf",
            }}
          >
            <p
              style={{
                fontSize: "11px",
                color: "#7f7664",
                textTransform: "uppercase",
                letterSpacing: "0.08em",
                marginBottom: "8px",
              }}
            >
              Sources
            </p>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
              {sources.map((source, index) => (
                <span
                  key={`${source}-${index}`}
                  style={{
                    fontSize: "12px",
                    background: "#f3eee2",
                    color: "#6a543a",
                    border: "1px solid #ddd4c0",
                    padding: "6px 10px",
                    borderRadius: "999px",
                  }}
                >
                  {source}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {isUser && (
        <div
          style={{
            ...avatarStyle,
            background: "#eadfcb",
            color: "#6a543a",
          }}
        >
          You
        </div>
      )}

      <style>{`
        @keyframes bubbleBounce {
          0%, 80%, 100% { transform: translateY(0); opacity: 0.6; }
          40% { transform: translateY(-4px); opacity: 1; }
        }
      `}</style>
    </div>
  );
};

export default MessageBubble;
