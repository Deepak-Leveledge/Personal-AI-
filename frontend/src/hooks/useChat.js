import { useState, useRef } from "react"
import { streamChat }        from "../utils/api"

export const useChat = () => {
  const [messages,      setMessages]      = useState([])
  const [isLoading,     setIsLoading]     = useState(false)
  const [statusUpdates, setStatusUpdates] = useState([])
  const [sources,       setSources]       = useState([])
  const currentAnswer                     = useRef("")
  const answerStarted                     = useRef(false)

  const sendMessage = async (text) => {
    if (!text.trim() || isLoading) return

    const userMsg = { role: "user", content: text }
    setMessages(prev => [...prev, userMsg])
    setIsLoading(true)
    setStatusUpdates([])
    setSources([])
    currentAnswer.current  = ""
    answerStarted.current  = false

    // ✅ empty assistant bubble — will fill as tokens come
    setMessages(prev => [
      ...prev,
      { role: "assistant", content: "" }
    ])

    const history = messages.slice(-10)

    streamChat(text, history, {

      // ✅ status immediately add karo
      onStatus: (status) => {
        setStatusUpdates(prev => [...prev, status])
      },

      // ✅ tokens stream karo
      onToken: (token) => {
        if (!answerStarted.current) {
          answerStarted.current = true
        }
        currentAnswer.current += token
        setMessages(prev => {
          const updated = [...prev]
          updated[updated.length - 1] = {
            role   : "assistant",
            content: currentAnswer.current
          }
          return [...updated]
        })
      },

      onSources: (srcs) => {
        setSources(srcs)
      },

      onDone: () => {
        setIsLoading(false)
      },

      onError: (err) => {
        setIsLoading(false)
        setMessages(prev => {
          const updated = [...prev]
          updated[updated.length - 1] = {
            role   : "assistant",
            content: `Sorry, something went wrong. Please try again.`
          }
          return updated
        })
      }
    })
  }

  const clearChat = () => {
    setMessages([])
    setStatusUpdates([])
    setSources([])
  }

  return {
    messages,
    isLoading,
    statusUpdates,
    sources,
    sendMessage,
    clearChat
  }
}
