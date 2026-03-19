from tavily import TavilyClient
import os

def search_web(query: str, num_results: int = 5) -> str:
    print(f"Performing web search for: {query}")
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    response = client.search(
        query=query,
        num_results=num_results,
        search_depth="advanced"
    )

    if not response.get("results"):
        # print("No search results found.")
        return ""
    
    results=""

    for i, r in enumerate(response["results"]):
        results += f"""
Result {i+1}:
Title   : {r['title']}
URL     : {r['url']}
Content : {r['content'][:300]}
---
"""

    print(f"✅ Found {len(response['results'])} results")
    return results
