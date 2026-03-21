import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import { useChat } from "./hooks/useChat";

function App() {
  const {
    messages,
    isLoading,
    statusUpdates,
    sources,
    sendMessage,
    clearChat,
    addAssistantMessage,
  } = useChat();

  return (
    <div className="app-shell">
      <Sidebar
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
