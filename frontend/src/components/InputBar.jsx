import { useState, useRef } from "react";
import FileUpload from "./FileUpload";

const InputBar = ({ onSend, isLoading }) => {
  const [input, setInput] = useState("");
  const taRef = useRef();

  const handleSend = () => {
    if (!input.trim() || isLoading) return;
    onSend(input);
    setInput("");
    if (taRef.current) taRef.current.style.height = "auto";
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const canSend = input.trim() && !isLoading;

  return (
    <div style={{ padding: "16px 24px", borderTop: "0.5px solid #d3d1c7" }}>
      <div
        style={{
          display: "flex",
          alignItems: "flex-end",
          gap: "8px",
          border: "0.5px solid #b4b2a9",
          borderRadius: "12px",
          padding: "10px 12px",
          background: "#fff",
          transition: "border-color 0.15s",
        }}
      >
        <FileUpload />

        <textarea
          ref={taRef}
          value={input}
          onChange={(e) => {
            setInput(e.target.value);
            e.target.style.height = "auto";
            e.target.style.height = Math.min(e.target.scrollHeight, 140) + "px";
          }}
          onKeyDown={handleKey}
          placeholder="Ask me anything..."
          rows={1}
          disabled={isLoading}
          style={{
            flex: 1,
            border: "none",
            outline: "none",
            resize: "none",
            fontSize: "13px",
            color: "#1a1a19",
            background: "transparent",
            lineHeight: "1.6",
            minHeight: "22px",
            maxHeight: "140px",
            fontFamily: "inherit",
          }}
        />

        <button
          onClick={handleSend}
          disabled={!canSend}
          style={{
            width: "28px",
            height: "28px",
            borderRadius: "7px",
            border: "none",
            background: canSend ? "#c96442" : "#d3d1c7",
            cursor: canSend ? "pointer" : "default",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexShrink: 0,
            transition: "background 0.15s",
          }}
        >
          <svg
            width="13"
            height="13"
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
          color: "#888780",
          marginTop: "8px",
        }}
      >
        PersonalAI can make mistakes. Verify important info.
      </p>
    </div>
  );
};

export default InputBar;
