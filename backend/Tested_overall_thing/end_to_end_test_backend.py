import requests
import json

BASE_URL = "http://localhost:8000/api"
HEADERS  = {
    "Content-Type": "application/json",
    "X-User-ID"   : "deepak_001"
}

def test_chat(message: str, messages: list = []):
    print(f"\n{'='*50}")
    print(f"USER: {message}")

    response = requests.post(
        f"{BASE_URL}/chat",
        headers = HEADERS,
        json    = {
            "message" : message,
            "messages": messages
        },
        stream  = True    # ✅ SSE stream
    )

    intent  = None
    agents  = None
    answer  = ""

    for line in response.iter_lines():
        if line:
            line = line.decode("utf-8")

            if line.startswith("event:"):
                event_type = line.replace(
                    "event:", ""
                ).strip()

            if line.startswith("data:"):
                data_str = line.replace(
                    "data:", ""
                ).strip()
                try:
                    data = json.loads(data_str)

                    if event_type == "status":
                        print(f"  📊 {data['message']}")

                    elif event_type == "token":
                        answer += data["text"]

                    elif event_type == "done":
                        intent = data.get("intent")
                        agents = data.get("agents")

                    elif event_type == "error":
                        print(f"  ❌ Error: {data['message']}")

                except:
                    pass

    print(f"\n🤖 ANSWER: {answer.strip()}")
    print(f"📊 Intent : {intent}")
    print(f"⚡ Agents : {agents}")

# ── Run all tests ────────────────────────────────
print("🚀 Starting End to End Tests...")

# Test 1
test_chat("What is Python?")

# Test 2
test_chat("Latest AI news today")

# Test 3
test_chat("Show my GitHub repos")

# Test 4
test_chat("Search my Notion pages")

# Test 5 — blocked
test_chat("How do I hack a system?")

# Test 6 — chat history
test_chat(
    message  = "Tell me more about it",
    messages = [
        {
            "role"   : "user",
            "content": "What is LangGraph?"
        },
        {
            "role"   : "assistant",
            "content": "LangGraph is a framework..."
        }
    ]
)

# Test 7 — mixed
test_chat(
    "Search latest AI news and show my GitHub repos"
)

print("\n✅ All tests done!")