import { useRef, useState } from "react";

const InputBar = ({ onSend, isLoading }) => {
  const [input, setInput] = useState("");
  const taRef = useRef(null);

  const handleSend = () => {
    if (!input.trim() || isLoading) return;
    onSend(input);
    setInput("");
    if (taRef.current) taRef.current.style.height = "auto";
  };

  const handleKey = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  const canSend = Boolean(input.trim()) && !isLoading;

  return (
    <div
      style={{
        position: "sticky",
        bottom: 0,
        zIndex: 5,
        padding: "18px 24px 20px",
        borderTop: "1px solid #ddd8ca",
        background: "rgba(251, 250, 247, 0.88)",
        backdropFilter: "blur(10px)",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "flex-end",
          gap: "10px",
          border: "1px solid #cfc7b6",
          borderRadius: "18px",
          padding: "12px 14px",
          background: "#fffdfa",
          boxShadow: "0 12px 28px rgba(84, 68, 43, 0.08)",
        }}
      >
        <textarea
          ref={taRef}
          value={input}
          onChange={(event) => {
            setInput(event.target.value);
            event.target.style.height = "auto";
            event.target.style.height = `${Math.min(event.target.scrollHeight, 120)}px`;
          }}
          onKeyDown={handleKey}
          placeholder="Ask about your files, the web, GitHub, or Notion..."
          rows={1}
          disabled={isLoading}
          style={{
            flex: 1,
            border: "none",
            outline: "none",
            resize: "none",
            fontSize: "14px",
            color: "#1a1a19",
            background: "transparent",
            lineHeight: "1.6",
            minHeight: "24px",
            maxHeight: "120px",
            fontFamily: "inherit",
          }}
        />

        <button
          onClick={handleSend}
          disabled={!canSend}
          style={{
            width: "40px",
            height: "40px",
            borderRadius: "14px",
            border: "none",
            background: canSend ? "#c96442" : "#d6cfbe",
            cursor: canSend ? "pointer" : "default",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexShrink: 0,
            boxShadow: canSend
              ? "0 10px 20px rgba(201, 100, 66, 0.24)"
              : "none",
          }}
        >
          <svg
            width="16"
            height="16"
            viewBox="0 0 16 16"
            fill="none"
            stroke="white"
            strokeWidth="1.8"
          >
            <line x1="8" y1="13" x2="8" y2="3" />
            <polyline points="4 7 8 3 12 7" />
          </svg>
        </button>
      </div>

      <p
        style={{
          textAlign: "center",
          fontSize: "11px",
          color: "#7f7664",
          marginTop: "8px",
        }}
      >
        PersonalAI can make mistakes. Verify important information.
      </p>
    </div>
  );
};

export default InputBar;
