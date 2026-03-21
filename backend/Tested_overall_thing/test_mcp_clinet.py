from dotenv import load_dotenv
load_dotenv()
from my_mcp.mcp_client import get_mcp_client
import asyncio
import os 



async def test_mcp():
    print("=== Testing MCP Client Setup ===")

    # just test configuration — not actual calls yet
    client = get_mcp_client()
    print(f"\n✅ MCP Client created!")
    print(f"Type: {type(client)}")
    print("\nConfigured servers based on your .env:")

    services = {
        "Gmail"    : os.getenv("GMAIL_REFRESH_TOKEN"),
        "Calendar" : os.getenv("GMAIL_REFRESH_TOKEN"),
        "Notion"   : os.getenv("NOTION_API_KEY"),
        "GitHub"   : os.getenv("GITHUB_TOKEN"),
    }

    for service, key in services.items():
        status = "✅ Configured" if key else "⚠️ Not configured"
        print(f"  {service}: {status}")

asyncio.run(test_mcp())