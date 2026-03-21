const BASE_URL = import.meta.env.VITE_BACKEND_URL;

export const getUserId = () => {
  let userId = sessionStorage.getItem("user_id");
  if (!userId) {
    userId = `user_${Math.random().toString(36).slice(2, 14)}`;
    sessionStorage.setItem("user_id", userId);
  }
  return userId;
};

const parseJsonResponse = async (response) => {
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data?.message || "Request failed.");
  }
  return data;
};

export const uploadDocuments = async (files) => {
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));

  const response = await fetch(`${BASE_URL}/upload`, {
    method: "POST",
    headers: { "X-User-ID": getUserId() },
    body: formData,
  });

  return parseJsonResponse(response);
};

export const streamChat = (message, messages, callbacks) => {
  const controller = new AbortController();
  const { onStatus, onToken, onSources, onDone, onError } = callbacks;

  fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-User-ID": getUserId(),
    },
    body: JSON.stringify({ message, messages }),
    signal: controller.signal,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Chat request failed with status ${response.status}.`);
      }

      if (!response.body) {
        throw new Error("Chat response stream is unavailable.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let buffer = "";
      let eventType = "";

      const processStream = ({ done, value }) => {
        if (done) {
          onDone?.();
          return;
        }

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("event:")) {
            eventType = line.replace("event:", "").trim();
            continue;
          }

          if (!line.startsWith("data:")) continue;

          try {
            const data = JSON.parse(line.replace("data:", "").trim());
            if (eventType === "status") onStatus?.(data.message);
            if (eventType === "token") onToken?.(data.text);
            if (eventType === "sources") onSources?.(data.sources || []);
            if (eventType === "done") onDone?.(data);
            if (eventType === "error") onError?.(data.message || "Something went wrong.");
          } catch {
            // Ignore malformed stream chunks and continue reading.
          }
        }

        reader.read().then(processStream).catch((error) => {
          if (error.name === "AbortError") {
            return;
          }
          onError?.(error.message);
        });
      };

      reader.read().then(processStream).catch((error) => {
        if (error.name === "AbortError") {
          return;
        }
        onError?.(error.message);
      });
    })
    .catch((error) => {
      if (error.name === "AbortError") {
        onError?.("Request cancelled");
        return;
      }
      onError?.(error.message);
    });

  return controller;
};
