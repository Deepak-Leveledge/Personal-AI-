from dotenv import load_dotenv
import os
load_dotenv()


keys = {
    "GEMINI"    : os.getenv("GEMINI_API_KEY"),
    "LANGSMITH" : os.getenv("LANGSMITH_API_KEY"),
    "TAVILY"    : os.getenv("TAVILY_API_KEY"),
    "PINECONE"  : os.getenv("PINECONE_API_KEY"),
    "MONGODB"   : os.getenv("MONGODB_URI"),
}


print("================================")
for name,value in keys.items():
    status = "✅" if value else "❌ MISSING"
    preview = value[:6] + "..." if value else "not set"
    print(f"{status}  {name}: {preview}")
print("================================")