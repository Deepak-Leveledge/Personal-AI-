import { useRef, useState } from "react";
import { uploadDocuments } from "../utils/api";

const services = [
  { name: "GitHub", icon: "GH" },
  { name: "Notion", icon: "NO" },
  { name: "Web Search", icon: "WS" },
  { name: "Documents", icon: "DB" },
];

const Sidebar = ({ onNewChat, onUploadComplete }) => {
  const inputRef = useRef(null);
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");
  const [uploadError, setUploadError] = useState("");

  const handleFileSelect = (event) => {
    const nextFiles = Array.from(event.target.files || []);
    setFiles(nextFiles);
    setUploadMessage("");
    setUploadError("");
  };

  const handleUpload = async () => {
    if (!files.length || uploading) return;

    setUploading(true);
    setUploadMessage("");
    setUploadError("");

    try {
      await uploadDocuments(files);
      setFiles([]);
      if (inputRef.current) inputRef.current.value = "";
      setUploadMessage(
        "Document uploaded. You can now ask questions and get information from the document.",
      );
      if (typeof onUploadComplete === "function") {
        onUploadComplete();
      }
    } catch (error) {
      setUploadError("Upload failed. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <aside
      className="app-sidebar"
      style={{
        display: "flex",
        flexDirection: "column",
        padding: "20px 16px",
        gap: "18px",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "12px",
          padding: "4px 6px",
        }}
      >
        <div
          style={{
            width: "40px",
            height: "40px",
            borderRadius: "12px",
            background: "linear-gradient(135deg, #c96442 0%, #9f4f34 100%)",
            boxShadow: "0 10px 24px rgba(159, 79, 52, 0.22)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#fffaf4",
            fontSize: "15px",
            fontWeight: 700,
            flexShrink: 0,
          }}
        >
          P
        </div>
        <div>
          <div style={{ fontSize: "16px", fontWeight: 700 }}>PersonalAI</div>
          <div style={{ fontSize: "12px", color: "#7f7664" }}>
            Chat with your tools and documents
          </div>
        </div>
      </div>

      <button
        onClick={onNewChat}
        style={{
          width: "100%",
          border: "1px solid #c8c1b2",
          borderRadius: "12px",
          background: "#fbfaf6",
          padding: "10px 14px",
          textAlign: "left",
          cursor: "pointer",
          fontSize: "14px",
          fontWeight: 600,
          boxShadow: "0 6px 18px rgba(97, 83, 57, 0.06)",
        }}
      >
        + New chat
      </button>

      <section
        style={{
          background: "rgba(255, 252, 245, 0.82)",
          border: "1px solid #d7d0bf",
          borderRadius: "16px",
          padding: "14px",
          boxShadow: "0 10px 22px rgba(97, 83, 57, 0.06)",
        }}
      >
        <div
          style={{
            fontSize: "12px",
            textTransform: "uppercase",
            letterSpacing: "0.08em",
            color: "#8b816d",
            marginBottom: "10px",
          }}
        >
          Upload documents
        </div>
        <div style={{ fontSize: "14px", fontWeight: 600, marginBottom: "6px" }}>
          Add files from the sidebar
        </div>
        <div
          style={{ fontSize: "12px", color: "#6d6558", marginBottom: "12px" }}
        >
          Select your files, then click upload to send them to the API.
        </div>

        <input
          ref={inputRef}
          type="file"
          multiple
          accept=".pdf,.doc,.docx"
          onChange={handleFileSelect}
          style={{ display: "none" }}
        />

        <div style={{ display: "flex", gap: "8px", marginBottom: "10px" }}>
          <button
            onClick={() => inputRef.current?.click()}
            style={{
              flex: 1,
              border: "1px solid #c8c1b2",
              borderRadius: "10px",
              background: "#fff",
              padding: "10px 12px",
              cursor: "pointer",
              fontSize: "13px",
              fontWeight: 600,
            }}
          >
            Select files
          </button>
          <button
            onClick={handleUpload}
            disabled={!files.length || uploading}
            style={{
              border: "none",
              borderRadius: "10px",
              background: !files.length || uploading ? "#d7d0bf" : "#c96442",
              color: "#fffaf4",
              padding: "10px 14px",
              cursor: !files.length || uploading ? "default" : "pointer",
              fontSize: "13px",
              fontWeight: 700,
              minWidth: "88px",
            }}
          >
            {uploading ? "Uploading" : "Upload"}
          </button>
        </div>

        <div
          style={{
            minHeight: "42px",
            borderRadius: "10px",
            background: "#f6f1e7",
            border: "1px dashed #d6cfbe",
            padding: "9px 10px",
            fontSize: "12px",
            color: files.length ? "#4d473d" : "#8b816d",
          }}
        >
          {files.length
            ? `${files.length} file${files.length > 1 ? "s" : ""} selected`
            : "No files selected yet"}
        </div>

        {uploadMessage && (
          <div
            style={{
              marginTop: "10px",
              borderRadius: "10px",
              background: "#eaf4e5",
              color: "#315824",
              padding: "10px 12px",
              fontSize: "12px",
              border: "1px solid #c6deb8",
            }}
          >
            {uploadMessage}
          </div>
        )}

        {uploadError && (
          <div
            style={{
              marginTop: "10px",
              borderRadius: "10px",
              background: "#fbe8e3",
              color: "#8f3b24",
              padding: "10px 12px",
              fontSize: "12px",
              border: "1px solid #efc3b4",
            }}
          >
            {uploadError}
          </div>
        )}
      </section>

      <section>
        <div
          style={{
            fontSize: "12px",
            textTransform: "uppercase",
            letterSpacing: "0.08em",
            color: "#8b816d",
            marginBottom: "8px",
            paddingLeft: "6px",
          }}
        >
          Connected
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
          {services.map((service) => (
            <div
              key={service.name}
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                borderRadius: "12px",
                background: "rgba(255, 251, 243, 0.72)",
                border: "1px solid #ddd6c6",
                padding: "10px 12px",
              }}
            >
              <div
                style={{
                  width: "28px",
                  height: "28px",
                  borderRadius: "9px",
                  background: "#efe6d6",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "11px",
                  fontWeight: 700,
                  color: "#7b6045",
                }}
              >
                {service.icon}
              </div>
              <div style={{ fontSize: "13px", fontWeight: 600 }}>
                {service.name}
              </div>
              <div
                style={{
                  marginLeft: "auto",
                  width: "8px",
                  height: "8px",
                  borderRadius: "50%",
                  background: "#4f7a2c",
                }}
              />
            </div>
          ))}
        </div>
      </section>

      <div style={{ marginTop: "auto" }}>
        <button
          onClick={onNewChat}
          style={{
            width: "100%",
            border: "none",
            borderRadius: "12px",
            background: "rgba(255, 251, 243, 0.72)",
            padding: "10px 12px",
            textAlign: "left",
            cursor: "pointer",
            fontSize: "13px",
            color: "#6d6558",
            borderTop: "1px solid #ddd6c6",
          }}
        >
          Clear chat
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
