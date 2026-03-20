from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from state.agent_state import AgentState
from graph.main_agent_graph import build_main_graph
from dotenv import load_dotenv
import json
import asyncio
import os

load_dotenv()

router = APIRouter()
graph  = build_main_graph()

class ChatRequest(BaseModel):
    message  : str
    messages : list = []    # chat history from frontend

# ── SSE event helper ────────────────────────────
def make_event(event_type: str, data: dict) -> str:
    """
    Format SSE event string
    event: type
    data: json
    """
    return (
        f"event: {event_type}\n"
        f"data: {json.dumps(data)}\n\n"
    )

# ── Main chat endpoint ───────────────────────────
@router.post("/chat")
async def chat(request: Request, body: ChatRequest):

    # get user_id from header
    user_id = request.headers.get(
        "X-User-ID", "deepak_001"
    )

    async def event_stream():
        try:
            # ── build initial state ─────────────
            state: AgentState = {
                "user_id"          : user_id,
                "messages"         : body.messages,
                "user_message"     : body.message,
                "is_safe"          : None,
                "block_reason"     : None,
                "intent"           : None,
                "agents_to_run"    : None,
                "rag_result"       : None,
                "web_result"       : None,
                "gmail_result"     : None,
                "calendar_result"  : None,
                "notion_result"    : None,
                "github_result"    : None,
                "rewritten_query"  : None,
                "retrieved_chunks" : None,
                "reranked_chunks"  : None,
                "rag_is_relevant"  : None,
                "is_hallucination" : None,
                "rag_retry_count"  : 0,
                "status_updates"   : [],
                "current_status"   : None,
                "final_answer"     : None,
                "sources"          : None,
                "error"            : None,
            }

            # ── send start event ────────────────
            yield make_event("start", {
                "message": "Processing your request..."
            })

            # ── run graph in thread ─────────────
            # graph is sync so run in executor
            loop   = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, graph.invoke, state
            )

            # ── send status updates ─────────────
            for status in result.get("status_updates", []):
                yield make_event("status", {
                    "message": status
                })
                await asyncio.sleep(0.05)

            # ── send sources if any ─────────────
            if result.get("sources"):
                yield make_event("sources", {
                    "sources": result["sources"]
                })

            # ── send final answer ───────────────
            final_answer = result.get(
                "final_answer", "No answer generated"
            )

            # stream answer word by word
            words = final_answer.split(" ")
            chunk = ""

            for i, word in enumerate(words):
                chunk += word + " "

                # send every 5 words as a chunk
                if (i + 1) % 5 == 0:
                    yield make_event("token", {
                        "text": chunk
                    })
                    chunk = ""
                    await asyncio.sleep(0.02)

            # send remaining words
            if chunk:
                yield make_event("token", {
                    "text": chunk
                })

            # ── send done event ─────────────────
            yield make_event("done", {
                "intent"  : result.get("intent"),
                "agents"  : result.get("agents_to_run"),
                "message" : "Complete!"
            })

        except Exception as e:
            print(f"❌ Stream error: {e}")
            yield make_event("error", {
                "message": str(e)
            })

    return StreamingResponse(
        event_stream(),
        media_type = "text/event-stream",
        headers    = {
            "Cache-Control"              : "no-cache",
            "X-Accel-Buffering"          : "no",
            "Access-Control-Allow-Origin": "*",
        }
    )

# ── Health check ─────────────────────────────────
@router.get("/health")
async def health():
    return {
        "status" : "ok",
        "message": "PersonalAI backend is running!"
    }