import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";
import AgentStatus from "./AgentStatus";
import InputBar from "./InputBar";

const suggestions = [
  "Show my GitHub repos",
  "Search Internet for AI news",
  "Latest AI news today",
  "Summarize my document",
];

const ChatWindow = ({
  messages,
  isLoading,
  statusUpdates,
  sources,
  onSend,
}) => {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, statusUpdates]);

  return (
    <div className="chat-window">
      <div
        style={{
          padding: "24px 28px 18px",
          borderBottom: "1px solid #e3ddcf",
          background: "rgba(251, 249, 244, 0.82)",
          backdropFilter: "blur(10px)",
        }}
      >
        <div
          style={{
            fontSize: "12px",
            textTransform: "uppercase",
            letterSpacing: "0.08em",
            color: "#8b816d",
            marginBottom: "6px",
          }}
        >
          Chat
        </div>
        <h2 style={{ fontSize: "24px", lineHeight: 1.2, marginBottom: "8px" }}>
          Ask questions across your tools and documents
        </h2>
        <p style={{ fontSize: "14px", color: "#6d6558", maxWidth: "720px" }}>
          Search the web, read uploaded files, and pull context from GitHub and
          Notion in one place.
        </p>
      </div>

      <div className="chat-scroll" style={{ padding: "24px 24px 12px" }}>
        {messages.length === 0 && (
          <div
            style={{
              minHeight: "100%",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              textAlign: "center",
              padding: "40px 20px 56px",
            }}
          >
            <div
              style={{
                width: "74px",
                height: "74px",
                borderRadius: "24px",
                background: "linear-gradient(135deg, #c96442 0%, #9f4f34 100%)",
                color: "#fffaf4",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "28px",
                fontWeight: 700,
                marginBottom: "18px",
                boxShadow: "0 18px 36px rgba(159, 79, 52, 0.24)",
              }}
            >
              AI
            </div>
            <h3
              style={{
                fontSize: "28px",
                lineHeight: 1.15,
                marginBottom: "10px",
              }}
            >
              How can I help you today?
            </h3>
            <p
              style={{
                fontSize: "14px",
                color: "#6d6558",
                marginBottom: "20px",
                maxWidth: "620px",
              }}
            >
              Start with a prompt below, or upload a document from the sidebar
              and ask questions about it.
            </p>

            <div className="chat-suggestions">
              {suggestions.map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => onSend(suggestion)}
                  style={{
                    border: "1px solid #ddd6c6",
                    background: "rgba(255, 252, 245, 0.86)",
                    borderRadius: "16px",
                    padding: "14px 16px",
                    textAlign: "left",
                    cursor: "pointer",
                    fontSize: "13px",
                    color: "#4d473d",
                    boxShadow: "0 8px 18px rgba(97, 83, 57, 0.05)",
                  }}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <MessageBubble
            key={`${message.role}-${index}`}
            message={message}
            sources={
              index === messages.length - 1 && message.role === "assistant"
                ? sources
                : []
            }
          />
        ))}

        <AgentStatus updates={statusUpdates} isLoading={isLoading} />
        <div ref={bottomRef} />
      </div>

      <InputBar onSend={onSend} isLoading={isLoading} />
    </div>
  );
};

export default ChatWindow;
