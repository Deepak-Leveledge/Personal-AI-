import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";
import AgentStatus from "./AgentStatus";
import InputBar from "./InputBar";

const ChatWindow = ({
  messages,
  isLoading,
  statusUpdates,
  sources,
  onSend,
}) => {
  const bottomRef = useRef();

  // auto scroll to bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, statusUpdates]);

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="px-6 py-4 border-b border-dark-600">
        <h2 className="text-sm font-medium text-gray-300">Chat</h2>
        <p className="text-xs text-gray-600">
          Ask me anything — I can search the web, read your docs, check GitHub
          and Notion
        </p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-4">
        {/* Empty state */}
        {messages.length === 0 && (
          <div
            className="flex flex-col items-center 
                          justify-center h-full 
                          text-center px-8"
          >
            <div
              className="w-16 h-16 bg-purple-600 
                            rounded-2xl flex items-center 
                            justify-center text-2xl mb-4"
            >
              🤖
            </div>
            <h3
              className="text-lg font-medium 
                           text-gray-200 mb-2"
            >
              How can I help you?
            </h3>
            <p className="text-sm text-gray-500 mb-6">
              I can answer questions, search the web, read your documents, check
              your GitHub repos and Notion pages.
            </p>

            {/* Suggestion chips */}
            <div className="grid grid-cols-2 gap-2 w-full max-w-md">
              {[
                "Show my GitHub repos",
                "Search my Notion pages",
                "Latest AI news today",
                "Summarize my document",
              ].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => onSend(suggestion)}
                  className="text-xs text-gray-400 
                              bg-dark-700 border border-dark-500 
                              rounded-xl px-3 py-2 
                              hover:border-purple-600 
                              hover:text-purple-400 
                              transition-colors text-left"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Message list */}
        {messages.map((msg, i) => (
          <MessageBubble
            key={i}
            message={msg}
            sources={
              i === messages.length - 1 && msg.role === "assistant"
                ? sources
                : []
            }
          />
        ))}

        {/* Live agent status */}
        <AgentStatus updates={statusUpdates} isLoading={isLoading} />

        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <InputBar onSend={onSend} isLoading={isLoading} />
    </div>
  );
};

export default ChatWindow;
