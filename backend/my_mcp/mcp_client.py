from langchain_mcp_adapters.client import MultiServerMCPClient  
from dotenv import load_dotenv
import os
load_dotenv()

def get_mcp_client() -> MultiServerMCPClient:
    """
    Creates and returns MCP client with all
    configured servers from .env
    """

    servers = {}

    # # ── Gmail MCP integration ─────────────────
    # gmail_token = os.getenv("GMAIL_REFRESH_TOKEN")
    # if gmail_token:
    #     servers["gmail"] = {
    #         "transport" : "stdio",
    #         "command": "npx",
    #         "args"   : [
    #             "-y",
    #             "@modelcontextprotocol/server-gmail"
    #         ],
    #         "env": {
    #             "GMAIL_CLIENT_ID"    : os.getenv("GMAIL_CLIENT_ID"),
    #             "GMAIL_CLIENT_SECRET": os.getenv("GMAIL_CLIENT_SECRET"),
    #             "GMAIL_REFRESH_TOKEN": os.getenv("GMAIL_REFRESH_TOKEN"),
    #         }
    #     }
    #     print("✅ Gmail MCP configured")
    # else:
    #     print("⚠️ Gmail not configured — skipping")


    # # ── Google Calendar ─────────────────────────
    # gcal_token = os.getenv("GMAIL_REFRESH_TOKEN")
    # if gcal_token:
    #     servers["google_calendar"] = {
    #         "transport" : "stdio",
    #         "command": "npx",
    #         "args"   : [
    #             "-y",
    #             "@modelcontextprotocol/server-google-calendar"
    #         ],
    #         "env": {
    #             "GOOGLE_CLIENT_ID"    : os.getenv("GMAIL_CLIENT_ID"),
    #             "GOOGLE_CLIENT_SECRET": os.getenv("GMAIL_CLIENT_SECRET"),
    #             "GOOGLE_REFRESH_TOKEN": os.getenv("GMAIL_REFRESH_TOKEN"),
    #         }
    #     }
    #     print("✅ Google Calendar MCP configured")
    # else:
    #     print("⚠️ Google Calendar not configured — skipping")


     # ── Notion ──────────────────────────────────
    notion_key = os.getenv("NOTION_API_KEY")
    if notion_key:
        servers["notion"] = {
            "transport" : "stdio",
            "command": "npx",
            "args"   : [
                "-y",
                "@notionhq/notion-mcp-server"
            ],
            "env": {
                "NOTION_API_KEY": notion_key
            }
        }
        print("✅ Notion MCP configured")
    else:
        print("⚠️ Notion not configured — skipping")


    # ── GitHub ──────────────────────────────────
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        servers["github"] = {
            "transport" : "stdio",
            "command": "npx",
            "args"   : [
                "-y",
                "@modelcontextprotocol/server-github"
            ],
            "env": {
                "GITHUB_PERSONAL_ACCESS_TOKEN": github_token
            }
        }
        print("✅ GitHub MCP configured")
    else:
        print("⚠️ GitHub not configured — skipping")

    return MultiServerMCPClient(servers)



async def get_mcp_tools(server_name: str) -> list:
    client = get_mcp_client()

    # ✅ async with hata do
    tools = await client.get_tools()

    server_tools = [
        t for t in tools
        if server_name in t.name.lower()
    ]
    return server_tools
    

async def run_mcp_tool(
    server_name : str,
    tool_name   : str,
    tool_input  : dict
) -> str:
    client = get_mcp_client()

    # ✅ direct get_tools() — no async with
    tools = await client.get_tools()

    tool = next(
        (t for t in tools if t.name == tool_name),
        None
    )

    if not tool:
        return f"Tool {tool_name} not found"

    result = await tool.ainvoke(tool_input)
    return str(result)