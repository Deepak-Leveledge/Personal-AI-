import { useRef, useState } from "react";
import { streamChat } from "../utils/api";

export const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [statusUpdates, setStatusUpdates] = useState([]);
  const [sources, setSources] = useState([]);
  const currentAnswer = useRef("");
  const activeRequest = useRef(null);

  const stopActiveRequest = () => {
    if (activeRequest.current) {
      activeRequest.current.abort();
      activeRequest.current = null;
    }
  };

  const addAssistantMessage = (content) => {
    setMessages((prev) => [...prev, { role: "assistant", content }]);
  };

  const sendMessage = async (text) => {
    const trimmedText = text.trim();
    if (!trimmedText || isLoading) return;

    stopActiveRequest();

    const userMessage = { role: "user", content: trimmedText };
    const assistantMessage = { role: "assistant", content: "" };
    const history = messages.slice(-10);

    setMessages((prev) => [...prev, userMessage, assistantMessage]);
    setIsLoading(true);
    setStatusUpdates([]);
    setSources([]);
    currentAnswer.current = "";

    activeRequest.current = streamChat(trimmedText, history, {
      onStatus: (status) => {
        setStatusUpdates((prev) => [...prev, status]);
      },

      onToken: (token) => {
        currentAnswer.current += token;
        setMessages((prev) => {
          if (!prev.length) return prev;
          const updated = [...prev];
          updated[updated.length - 1] = {
            role: "assistant",
            content: currentAnswer.current,
          };
          return updated;
        });
      },

      onSources: (nextSources) => {
        setSources(nextSources);
      },

      onDone: () => {
        activeRequest.current = null;
        setIsLoading(false);
      },

      onError: (error) => {
        if (error === "Request cancelled") {
          return;
        }

        activeRequest.current = null;
        setIsLoading(false);
        setMessages((prev) => {
          if (!prev.length) return prev;
          const updated = [...prev];
          updated[updated.length - 1] = {
            role: "assistant",
            content: "Sorry, something went wrong. Please try again.",
          };
          return updated;
        });
      },
    });
  };

  const clearChat = () => {
    stopActiveRequest();
    setMessages([]);
    setIsLoading(false);
    setStatusUpdates([]);
    setSources([]);
    currentAnswer.current = "";
  };

  return {
    messages,
    isLoading,
    statusUpdates,
    sources,
    sendMessage,
    clearChat,
    addAssistantMessage,
  };
};
