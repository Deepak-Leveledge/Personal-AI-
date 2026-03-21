import ReactMarkdown from "react-markdown";

const MessageBubble = ({ message, sources }) => {
  const isUser = message.role === "user";
  const isEmpty = !message.content && !isUser;
  const isTyping = isEmpty;

  return (
    <div
      className={`flex w-full mb-4 
                     ${isUser ? "justify-end" : "justify-start"}`}
    >
      {!isUser && (
        <div
          className="w-8 h-8 rounded-full bg-purple-600 
                        flex items-center justify-center 
                        text-sm mr-3 mt-1 shrink-0"
        >
          AI
        </div>
      )}

      <div
        className={`max-w-[75%] rounded-2xl px-4 py-3
                       ${
                         isUser
                           ? "bg-purple-600 text-white rounded-tr-sm"
                           : "bg-dark-600 text-gray-100 rounded-tl-sm"
                       }`}
      >
        {isUser ? (
          <p className="text-sm leading-relaxed">{message.content}</p>
        ) : isTyping ? (
          /* ✅ typing indicator when empty */
          <div className="flex gap-1 py-1">
            {[0, 150, 300].map((delay) => (
              <span
                key={delay}
                className="w-2 h-2 bg-gray-400 
                             rounded-full animate-bounce"
                style={{ animationDelay: `${delay}ms` }}
              />
            ))}
          </div>
        ) : (
          /* ✅ markdown content */
          <div
            className="text-sm leading-relaxed 
                          prose prose-invert 
                          prose-sm max-w-none"
          >
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
        )}

        {/* ✅ Sources — show if available */}
        {!isUser && sources && sources.length > 0 && (
          <div
            className="mt-3 pt-3 
                          border-t border-dark-400"
          >
            <p className="text-xs text-gray-500 mb-2">📚 Sources:</p>
            <div className="flex flex-wrap gap-1">
              {sources.map((src, i) => (
                <span
                  key={i}
                  className="text-xs bg-dark-500 
                               text-purple-400 
                               px-2 py-1 rounded-lg"
                >
                  📄 {src}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {isUser && (
        <div
          className="w-8 h-8 rounded-full bg-blue-600 
                        flex items-center justify-center 
                        text-sm ml-3 mt-1 shrink-0"
        >
          U
        </div>
      )}
    </div>
  );
};

export default MessageBubble;
