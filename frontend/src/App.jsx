import { useState } from "react";
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
  } = useChat();

  return (
    <div
      style={{
        display: "flex",
        height: "100vh",
        background: "#f9f8f5",
        color: "#1a1a19",
        fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
      }}
    >
      <Sidebar onNewChat={clearChat} />
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
          color: "#1a1a19",
        }}
      >
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
