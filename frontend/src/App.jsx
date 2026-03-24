import { useEffect, useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import { useChat } from "./hooks/useChat";

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const {
    messages,
    isLoading,
    statusUpdates,
    sources,
    sendMessage,
    clearChat,
    addAssistantMessage,
  } = useChat();

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 900) {
        setIsSidebarOpen(false);
      }
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <div className="app-shell">
      <button
        type="button"
        className="mobile-sidebar-toggle"
        onClick={() => setIsSidebarOpen(true)}
        aria-label="Open sidebar"
      >
        <span />
        <span />
        <span />
      </button>

      {isSidebarOpen && (
        <button
          type="button"
          className="mobile-sidebar-backdrop"
          onClick={() => setIsSidebarOpen(false)}
          aria-label="Close sidebar backdrop"
        />
      )}

      <Sidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        onNewChat={clearChat}
        onUploadComplete={() =>
          addAssistantMessage(
            "Document uploaded successfully. You can now ask questions and get information from the document.",
          )
        }
      />
      <div className="app-main">
        <ChatWindow
          messages={messages}
          isLoading={isLoading}
          statusUpdates={statusUpdates}
          sources={sources}
          onSend={sendMessage}
        />
      </div>
    </div>
  );
}

export default App;
