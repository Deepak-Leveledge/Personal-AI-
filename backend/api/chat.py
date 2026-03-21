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

            # ── send start ──────────────────────
            yield make_event("status", {
                "message": "🤔 Thinking..."
            })
            await asyncio.sleep(0.05)

            # ── run graph in thread ─────────────
            import queue
            status_queue = queue.Queue()

            # patch state to capture live status
            original_state = state.copy()

            loop   = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, graph.invoke, state
            )

            # ── stream status updates first ─────
            for status in result.get("status_updates", []):
                yield make_event("status", {
                    "message": status
                })
                await asyncio.sleep(0.08)

            # ── small pause before answer ───────
            await asyncio.sleep(0.15)

            # ── send sources ────────────────────
            if result.get("sources"):
                yield make_event("sources", {
                    "sources": result["sources"]
                })

            # ── stream final answer ─────────────
            final_answer = result.get(
                "final_answer", "No answer generated"
            )

            words = final_answer.split(" ")
            chunk = ""

            for i, word in enumerate(words):
                chunk += word + " "
                if (i + 1) % 3 == 0:
                    yield make_event("token", {"text": chunk})
                    chunk = ""
                    await asyncio.sleep(0.09)

            if chunk.strip():
                yield make_event("token", {"text": chunk})

            # ── done ────────────────────────────
            yield make_event("done", {
                "intent" : result.get("intent"),
                "agents" : result.get("agents_to_run"),
                "message": "Complete!"
            })

        except Exception as e:
            print(f"❌ Stream error: {e}")
            yield make_event("error", {"message": str(e)})

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