from langgraph.graph import StateGraph,START,END
from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
from state.agent_state import AgentState
from tools.rag_tool import retrieve_chunks
from guardrails.input_guard import input_guard
import os
from dotenv import load_dotenv
load_dotenv()



## Initialize the Gemeni API client
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=os.getenv("GEMINI_API_KEY"))


#Query ko rewrite karega if needed, for better retrieval
@traceable(name="query_rewriter")
def query_rewriter(state: AgentState) -> AgentState:
    print("🔄 Running Query Rewriter...")

    question = state["user_message"]
    history = state.get("messages", [])

    recent_convo =""
    if history:
        last = history[-5:] if len(history) >= 5 else history
        recent_convo ="\n".join(
            [f"{m['role']}: {m['content']}" for m in last])


    prompt = f"""
    You are a search query optimizer.

    Rewrite the user question into a better search query
    for semantic vector search over documents.

    Rules:
    - Make it specific and keyword rich
    - Remove filler words like "can you", "please"
    - Expand abbreviations
    - Keep it under 20 words
    - If the question refers to "it" or "this" use the
      chat history to understand what it refers to

    Recent chat history:
    {recent_convo}

    Original question: {question}

    Return ONLY the rewritten query, nothing else.
    """


    response = llm.invoke(prompt)
    rewritten = response.content.strip()

    state["rewritten_query"] = rewritten
    #status update kar raha hai frontend me user ko dikhne ke liye ki kya ho raha hai
    state["status_updates"].append("🔍 Searching your documents...")

    print(f"✏️ Rewritten query: {rewritten}")
    return state



#Hybrid retrieval using both rewritten query and original question for better recall

@traceable(name="Hybrid Retriever")
def hybrid_retriver(state:AgentState) -> AgentState:
    print("⚡ Running Hybrid Retriever...")


    query   = state["rewritten_query"]
    user_id = "deepak_001"

    # vector search — semantic with query_rewritter
    vector_chunks = retrieve_chunks(
        query   = query,
        user_id = user_id,
        top_k   = 8
    )

    # keyword search — exact match boost karne ke liye
    # search with original question too for keyword overlap
    keyword_chunks = retrieve_chunks(
        query   = state["user_message"],
        user_id = user_id,
        top_k   = 5
    )

    seen = set()
    combined = []
    for chunk in vector_chunks + keyword_chunks:
        if chunk["text"] not in seen:
            seen.add(chunk["text"])
            combined.append(chunk)

    state["retrieved_chunks"] = combined
    print(f"✅ Retrieved {len(combined)} unique chunks")
    return state

#Re-rank the retrived chunk
@traceable(name="Reranker")
def reranker(state:AgentState) -> AgentState:
    print("🎯 Running Reranker...")

    chunks   = state["retrieved_chunks"]
    question = state["user_message"]

    if not chunks:
        state["reranked_chunks"] = []
        return state

    # ask Gemini to score each chunk
    chunks_text = ""
    for i, chunk in enumerate(chunks):
        chunks_text += f"""
Chunk {i+1} (page {chunk['page']}, score {chunk['score']:.2f}):
{chunk['text'][:300]}
---"""
        

    prompt = f"""
    You are a document relevance scorer.

    Score each chunk from 0-10 for how relevant it is
    to answering the question.

    Question: {question}

    Chunks:
    {chunks_text}

    IMPORTANT: Return ONLY {len(chunks)} numbers
    separated by commas. No text, no explanation.
    Example format: 8,3,9,2,7
    """

    response = llm.invoke(prompt)
    scores_raw = response.content.strip()
    print(f"🔢 Raw scores from Gemini: {scores_raw}")

    try:
        scores = [float(s.strip()) for s in scores_raw.split(",")]
    except:
        # if parsing fails keep original order
        scores = [chunk["score"] * 10 for chunk in chunks]

    # attach scores and sort
    for i, chunk in enumerate(chunks):
        chunk["rerank_score"] = scores[i] if i < len(scores) else 0

    reranked = sorted(
        chunks,
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    # keep top 5 only
    state["reranked_chunks"] = reranked[:5]
    print(f"✅ Re-ranked — keeping top {len(state['reranked_chunks'])} chunks")
    
    print(f"🔢 Parsed scores: {scores}")
    print(f"🔢 Top chunk rerank score: {reranked[0]['rerank_score']}")
    return state


# ── Node 4 — Relevance Checker agent (Self-RAG) ───────
@traceable(name="Relevance Checker")
def relevance_checker(state:AgentState)->AgentState:

    chunks = state["reranked_chunks"]
    question = state["user_message"]

    if not chunks:
        state["rag_is_relevant"] = False
        return state
    
    top_rerank_score   = chunks[0].get("rerank_score", 0)
    top_pinecone_score = chunks[0].get("score", 0)

    print(f"🔢 Top rerank score  : {top_rerank_score}")
    print(f"🔢 Top pinecone score: {top_pinecone_score}")

    # ✅ if rerank score is strong → directly relevant
    if top_rerank_score >= 6:
        print("✅ Strong rerank score — marking relevant!")
        state["rag_is_relevant"] = True
        return state

    # ✅ if pinecone score is decent → relevant
    if top_pinecone_score >= 0.5:
        print("✅ Good pinecone score — marking relevant!")
        state["rag_is_relevant"] = True
        return state

    # ✅ low scores → ask Gemini as last check
    context = "\n".join([c["text"][:200] for c in chunks[:3]])

    prompt = f"""
    Question: {question}

    Context:
    {context}

    Can this context answer the question?
    Reply with only: YES or NO
    """

    response = llm.invoke(prompt)
    answer   = response.content.strip().upper()
    print(f"🤖 Gemini relevance check: {answer}")

    state["rag_is_relevant"] = "YES" in answer
    print(f"✅ RAG relevance: {state['rag_is_relevant']}")
    return state


# ── Node 5 — Answer Generator ───────────────────
@traceable(name="Answer Generator")
def answer_generator(state:AgentState) -> AgentState:
    print("Running Answer Generator...")
    
    #retriving the all there state for generating the answer using the question and the retrived chunks
    chunks   = state["reranked_chunks"]
    question = state["user_message"]
    messages = state.get("messages", [])

    # build context from chunks to LLM
    context  = ""
    sources  = []
    for i, chunk in enumerate(chunks):
        context += f"\n[Source {i+1} — {chunk['doc_name']} page {chunk['page']}]\n"
        context += chunk["text"] + "\n"
        source   = f"{chunk['doc_name']} (page {chunk['page']})"
        if source not in sources:
            sources.append(source)

    # build chat history for context to LLM
    history = ""
    if messages:
        last = messages[-4:] if len(messages) >= 4 else messages
        history = "\n".join(
            [f"{m['role']}: {m['content']}" for m in last]
        )
    
    prompt = f"""
    You are a helpful assistant answering questions
    strictly from the provided document context.

    Rules:
    - Only use information from the context below
    - If context does not contain the answer say so
    - Mention source page numbers when relevant
    - Be concise and clear
    - Use the chat history for context if needed

    Chat history:
    {history}

    Document context:
    {context}

    Question: {question}
    """

    response             = llm.invoke(prompt)
    state["rag_result"]  = response.content.strip()
    state["sources"]     = sources
    state["status_updates"].append("📄 Found relevant content in your documents!")

    print("✅ Answer generated!")
    return state



# ── Node 6 — Hallucination Checker ─────────────
@traceable(name="Hallucination Checker")
def hallucination_checker_node(state: AgentState) -> AgentState:
    print("🔎 Hallucination Checker running...")

    answer  = state["rag_result"]
    chunks  = state["reranked_chunks"]
    context = "\n".join([c["text"] for c in chunks])

    prompt = f"""
    You are a fact checker.

    Check if the answer is fully supported by the context.

    Context:
    {context[:1500]}

    Answer:
    {answer}

    Is every claim in the answer supported by the context?
    Reply with only: GROUNDED or HALLUCINATION
    """

    response = llm.invoke(prompt)
    result   = response.content.strip().upper()

    state["is_hallucination"] = "HALLUCINATION" in result

    if state["is_hallucination"]:
        print("⚠️ Hallucination detected — flagging answer")
        state["rag_result"] = (
            "I found some information in your documents "
            "but could not verify it completely. "
            "Please check the source documents directly.\n\n"
            + state["rag_result"]
        )
    else:
        print("✅ Answer is grounded in documents!")

    return state


# ── No docs found handler ───────────────────────
def no_docs_node(state: AgentState) -> AgentState:
    state["rag_result"] = (
        "I could not find relevant information in your "
        "uploaded documents for this question. "
        "Please make sure you have uploaded the right document "
        "or try rephrasing your question."
    )
    state["sources"] = []
    return state



# ── Conditional edge — relevance check ─────────
def check_relevance(state: AgentState) -> str:
    retry_count = state.get("rag_retry_count", 0)

    if state["rag_is_relevant"]:
        return "relevant"
    elif retry_count < 2:
        # retry up to 2 times
        # state["rag_retry_count"] = retry_count + 1
        # print(f"🔄 Retrying query — attempt {retry_count + 1}")
        return "retry"
    else:
        return "no_docs"


def increment_retry_node(state: AgentState) -> AgentState:
    state["rag_retry_count"] = state.get("rag_retry_count", 0) + 1
    print(f"🔄 Retrying — attempt {state['rag_retry_count']}")
    return state


# ── Build RAG Graph ─────────────────────────────
def build_rag_graph():
    graph = StateGraph(AgentState)

    graph.add_node("query_rewriter",       query_rewriter)
    graph.add_node("hybrid_retriever",     hybrid_retriver)
    graph.add_node("reranker",             reranker)
    graph.add_node("relevance_checker",    relevance_checker)
    graph.add_node("increment_retry",       increment_retry_node)  

    graph.add_node("answer_generator",     answer_generator)
    graph.add_node("hallucination_checker",hallucination_checker_node)
    graph.add_node("no_docs",              no_docs_node)

    graph.set_entry_point("query_rewriter")

    graph.add_edge("query_rewriter",    "hybrid_retriever")
    graph.add_edge("hybrid_retriever",  "reranker")
    graph.add_edge("reranker",          "relevance_checker")

    graph.add_conditional_edges(
        "relevance_checker",
        check_relevance,
        {
            "relevant" : "answer_generator",
            "retry"    : "increment_retry",
            "no_docs"  : "no_docs"
        }
    )

    graph.add_edge("increment_retry",       "query_rewriter")
    graph.add_edge("answer_generator",      "hallucination_checker")
    graph.add_edge("hallucination_checker", END)
    graph.add_edge("no_docs",               END)


    return graph.compile()




# ── Main callable ───────────────────────────────
@traceable(name="RAG Agent")
def rag_agent(state: AgentState) -> AgentState:
    print("\n🤖 RAG Agent starting...")
    state["rag_retry_count"] = 0
    state["status_updates"].append("📚 Starting document search...")

    rag_graph    = build_rag_graph()
    updated_state = rag_graph.invoke(state)

    # copy RAG results back to main state
    state["rag_result"]       = updated_state.get("rag_result")
    state["sources"]          = updated_state.get("sources")
    state["rewritten_query"]  = updated_state.get("rewritten_query")
    state["reranked_chunks"]  = updated_state.get("reranked_chunks")
    state["is_hallucination"] = updated_state.get("is_hallucination")

    print("✅ RAG Agent done!")
    return state