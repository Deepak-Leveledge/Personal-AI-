from typing import List, Optional , Dict, Any,TypedDict,Literal


class Message(TypedDict):
    role: Literal['user','assistant']
    content: str


class AgentState(TypedDict):
    # ── Conversation ──────────────────────
    messages: List[Message]       # full chat history this session
    user_message: str             # current user message

    # ── Guardrail ─────────────────────────
    is_safe: Optional[bool]       # True = safe, False = blocked
    block_reason: Optional[str]   # why it was blocked

    # ── Routing ───────────────────────────
    intent: Optional[str]         # general / rag gmail / calendar / notion /github / websearch / mixed
                                 
    agents_to_run: Optional[List[str]]  # which agents to trigger

    # ── Agent Outputs ─────────────────────
    rag_result: Optional[str]
    web_result: Optional[str]
    gmail_result: Optional[str]
    calendar_result: Optional[str]
    notion_result: Optional[str]
    github_result: Optional[str]

    # ── RAG Pipeline ──────────────────────
    rewritten_query: Optional[str]      # query rewriter output
    retrieved_chunks: Optional[List]    # raw chunks from Pinecone
    reranked_chunks: Optional[List]     # LLM reranking of chunks
    rag_retry_count: int                
    rag_is_relevant: Optional[bool]     # self-RAG check
    is_hallucination: Optional[bool]    # hallucination check

    # ── Streaming ─────────────────────────
    status_updates: Optional[List[str]] # live progress messages
    current_status: Optional[str]       # current agent running

    # ── Final Output ──────────────────────
    final_answer: Optional[str]         # synthesized answer
    sources: Optional[List[str]]        # document sources cited
    error: Optional[str]                # any error message