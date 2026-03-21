const BASE_URL = "http://localhost:8000/api"

// generate session user id
export const getUserId = () => {
  let userId = sessionStorage.getItem("user_id")
  if (!userId) {
    userId = `user_${Math.random().toString(36).substr(2, 12)}`
    sessionStorage.setItem("user_id", userId)
  }
  return userId
}

// upload documents
export const uploadDocuments = async (files) => {
  const formData = new FormData()
  files.forEach(file => formData.append("files", file))

  const response = await fetch(`${BASE_URL}/upload`, {
    method : "POST",
    headers: { "X-User-ID": getUserId() },
    body   : formData
  })

  return response.json()
}

// stream chat — returns EventSource
export const streamChat = (message, messages, callbacks) => {
  const { onStatus, onToken, onSources, onDone, onError } = callbacks

  fetch(`${BASE_URL}/chat`, {
    method : "POST",
    headers: {
      "Content-Type": "application/json",
      "X-User-ID"   : getUserId()
    },
    body: JSON.stringify({ message, messages })
  })
  .then(response => {
    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    let buffer    = ""
    let eventType = ""

    const processStream = ({ done, value }) => {
      if (done) return

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split("\n")
      buffer = lines.pop()

      for (const line of lines) {
        if (line.startsWith("event:")) {
          eventType = line.replace("event:", "").trim()
        }
        if (line.startsWith("data:")) {
          try {
            const data = JSON.parse(
              line.replace("data:", "").trim()
            )
            if (eventType === "status"  && onStatus)  onStatus(data.message)
            if (eventType === "token"   && onToken)   onToken(data.text)
            if (eventType === "sources" && onSources) onSources(data.sources)
            if (eventType === "done"    && onDone)    onDone(data)
            if (eventType === "error"   && onError)   onError(data.message)
          } catch {}
        }
      }

      reader.read().then(processStream)
    }

    reader.read().then(processStream)
  })
  .catch(err => onError && onError(err.message))
}