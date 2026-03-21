import { useState, useRef } from "react";
import { uploadDocuments } from "../utils/api";

const FileUpload = ({ onUploadComplete }) => {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploaded, setUploaded] = useState(false);
  const inputRef = useRef();

  const handleFiles = (e) => {
    setFiles(Array.from(e.target.files));
    setUploaded(false);
  };

  const handleUpload = async () => {
    if (!files.length) return;
    setUploading(true);
    try {
      const result = await uploadDocuments(files);
      setUploaded(true);
      setFiles([]);
      // ✅ check karo function hai tab hi call karo
      if (typeof onUploadComplete === "function") {
        onUploadComplete(result);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: "6px",
        flexShrink: 0,
      }}
    >
      <button
        onClick={() => inputRef.current?.click()}
        title="Upload document"
        style={{
          width: "26px",
          height: "26px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          border: "none",
          background: "transparent",
          cursor: "pointer",
          color: "#888780",
          borderRadius: "6px",
          padding: 0,
        }}
        onMouseOver={(e) => (e.currentTarget.style.color = "#5f5e5a")}
        onMouseOut={(e) => (e.currentTarget.style.color = "#888780")}
      >
        <svg
          width="15"
          height="15"
          viewBox="0 0 16 16"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.5"
        >
          <path d="M13 7l-6 6a4 4 0 01-5.6-5.6l6-6a2.5 2.5 0 013.5 3.5L5 11a1 1 0 01-1.4-1.4L9 5" />
        </svg>
      </button>

      <input
        ref={inputRef}
        type="file"
        multiple
        accept=".pdf,.docx,.doc"
        onChange={handleFiles}
        style={{ display: "none" }}
      />

      {files.length > 0 && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "6px",
            background: "#f1efe8",
            borderRadius: "6px",
            padding: "3px 8px",
          }}
        >
          <span style={{ fontSize: "12px", color: "#5f5e5a" }}>
            {files.length} file{files.length > 1 ? "s" : ""}
          </span>
          {uploading ? (
            <span style={{ fontSize: "11px", color: "#888780" }}>
              uploading...
            </span>
          ) : (
            <>
              <button
                onClick={handleUpload}
                style={{
                  fontSize: "12px",
                  color: "#c96442",
                  border: "none",
                  background: "transparent",
                  cursor: "pointer",
                  fontWeight: "500",
                }}
              >
                Upload
              </button>
              <button
                onClick={() => setFiles([])}
                style={{
                  fontSize: "12px",
                  color: "#888780",
                  border: "none",
                  background: "transparent",
                  cursor: "pointer",
                }}
              >
                ✕
              </button>
            </>
          )}
        </div>
      )}

      {uploaded && (
        <span style={{ fontSize: "12px", color: "#3b6d11" }}>✓ Uploaded</span>
      )}
    </div>
  );
};

export default FileUpload;
