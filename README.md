# PersonalAI — Your Intelligent Personal Assistant

> One chatbot that talks to your Gmail, Notion, GitHub, searches the web, and answers questions from your own documents — all in one place.

🚀 **Live Demo** → [personal-ai-backend.onrender.com]([https://personal-ai-backend.onrender.com](https://personal-ai-henna.vercel.app/))

---

## What is this?

I got tired of switching between Gmail, Notion, GitHub, and Google just to get things done. So I built one AI assistant that does all of it.

You just chat with it like a normal chatbot. It figures out what you need and calls the right tool automatically — no buttons, no switching, no manual work.

---

## Demo

> Screenshot or GIF of the app here

---

## What it can do

- **Answer general questions** — like a smart chatbot
- **Search the web** — finds latest news, current info, anything online
- **Read your documents** — upload a PDF or DOCX and ask questions about it
- **Check your GitHub** — see your repos, issues, pull requests
- **Search your Notion** — find pages, notes, databases
- **Smart routing** — automatically picks the right tool for your question
- **Blocks harmful messages** — built-in safety checks before anything runs
- **Streams answers live** — see the response as it types, just like ChatGPT

---

## How it works

You type a message. A supervisor agent reads it and decides which agent should handle it. The right agent runs, gets the data, and the answer streams back to you word by word.

```
Your message
      ↓
Safety check
      ↓
Supervisor decides which agent to use
      ↓
Agent runs (RAG / Web / GitHub / Notion)
      ↓
Answer streams back to you
```

If your question needs multiple things — like "search the web and check my GitHub" — it runs both agents at the same time and combines the results.

---

## Agents

| Agent | What it does |
|---|---|
| **Supervisor** | Reads your message and decides which agent to call |
| **RAG Agent** | Searches your uploaded documents using Pinecone |
| **Web Search Agent** | Searches the internet using Tavily |
| **GitHub Agent** | Connects to GitHub via MCP and fetches your data |
| **Notion Agent** | Connects to Notion via MCP and searches your pages |
| **Synthesizer** | Takes all agent results and writes one clean answer |
| **Input Guardrail** | Checks every message before anything runs |

---

## RAG Pipeline (Document Search)

This is not a basic RAG setup. Every document search goes through these steps:

1. **Query rewriter** — rewrites your question into a better search query
2. **Hybrid search** — searches by meaning AND by keywords together
3. **Re-ranker** — scores each result and keeps only the best ones
4. **Relevance check** — verifies if the results actually answer the question
5. **Answer generator** — writes the answer using only the document content
6. **Hallucination check** — verifies the answer is grounded in the document

If the results are not relevant enough it automatically retries with a better query.

---

## Tech Stack

| What | Tool |
|---|---|
| Language | Python |
| Agent Framework | LangGraph |
| LLM | Gemini 2.0 Flash |
| Vector Database | Pinecone |
| Embeddings | Gemini Embeddings |
| Web Search | Tavily |
| MCP Integration | LangChain MCP Adapters |
| Observability | LangSmith |
| Backend | FastAPI |
| Streaming | Server Sent Events (SSE) |
| Frontend | React + Vite |
| Deployment | Render |


---



---

## What I Learned

Building this project taught me a lot about how real AI systems actually work in practice.

The biggest lesson was about **agentic design**. Each agent needs a very clear job with a very specific output format. When one agent's output is unclear, every agent that depends on it produces a weaker result. Clean, precise prompts matter more than anything else.

The second lesson was about **parallel execution**. Running agents one by one is slow. Using `asyncio.gather()` to run independent agents at the same time made the app feel much faster without changing any of the actual logic.

The third lesson was **observability first**. I set up LangSmith before writing a single agent. Every time something went wrong, I could see exactly which agent failed and why. Without it, debugging a multi-agent system would have been very painful.

The fourth lesson was about **MCP integration**. The Model Context Protocol is a powerful idea — one standard way for AI to connect to any external tool. But the ecosystem is still young. Some servers work perfectly, some don't exist yet. Knowing when to use MCP and when to just call an API directly is an important judgment call.

---

## Future Improvements

- Add Gmail and Google Calendar support
- Add long-term memory using Pinecone for user facts
- Deploy on GCP Cloud or AWS Run for better performance
- Add user authentication for multi-user support
- Build a mobile-friendly UI

---


