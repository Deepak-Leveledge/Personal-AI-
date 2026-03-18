from langchain_text_splitters import RecursiveCharacterTextSplitter
from tools.pdf_reader import read_pdf_with_pages,read_document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

import os
load_dotenv()
import uuid


## Initialize the Gemeni API client
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=os.getenv("GEMINI_API_KEY"))


# ── Initialize Pinecone ─────────────────────────
pc    = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

#Emebding model
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

def smart_chunk(pages: list) -> list:
    """
    Uses LangChain RecursiveCharacterTextSplitter
    per page so we keep page metadata accurately
    """
    print("✂️ Smart chunking with LangChain splitter...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size    = 500,
        chunk_overlap = 50,
        separators    = ["\n\n", "\n", ".", " "]
    )

    all_chunks = []

    for page in pages:
        # split this page's text
        page_chunks = splitter.split_text(page["text"])

        for chunk_text in page_chunks:
            if len(chunk_text.strip()) > 50:
                all_chunks.append({
                    "text"    : chunk_text.strip(),
                    "page"    : page["page_num"],
                    "chunk_id": str(uuid.uuid4())
                })

    print(f"✅ Created {len(all_chunks)} chunks")
    return all_chunks


def ingest_document(
    file_path : str,
    doc_name : str,
    user_id  : str = "deepak_001"
):
    print(f"📥 Ingesting document: {doc_name}")

    # step 1 — auto detects PDF or DOCX
    pages = read_document(file_path)  

    # step 2 — smart chunk using LangChain splitter
    chunks = smart_chunk(pages)

    # step 2 — generate hypothetical questions per chunk (HyDE)
    print("💡 Generating hypothetical questions (HyDE)...")
    enhanced_chunks = []
    for chunk in chunks:
        try:
            hyde_prompt = f"""
            Generate 2 short questions that this text answers.
            Return only the questions, one per line.
            Text: {chunk['text'][:300]}
            """
            response   = llm.invoke(hyde_prompt)
            questions  = response.content.strip()
            # combine original text + questions for richer embedding
            enhanced   = chunk["text"] + "\n" + questions
            chunk["enhanced_text"] = enhanced
            chunk["questions"]     = questions
            # print(f"Chunk {chunk['chunk_id']} questions:\n{questions}\n{chunk ['enhanced_text'][:500]}")
        except:
            chunk["enhanced_text"] = chunk["text"]
            chunk["questions"]     = ""
        enhanced_chunks.append(chunk)

    # step 3 — embed all chunks
    print("🔢 Generating embeddings...")
    texts_to_embed = [c["enhanced_text"] for c in enhanced_chunks]
    vectors        = embeddings.embed_documents(texts_to_embed)

    # step 4 — upsert to Pinecone
    print("📤 Uploading to Pinecone...")
    batch_size = 50
    for i in range(0, len(enhanced_chunks), batch_size):
        batch        = enhanced_chunks[i:i + batch_size]
        batch_vecs   = vectors[i:i + batch_size]
        pinecone_data = []

        for chunk, vec in zip(batch, batch_vecs):
            pinecone_data.append({
                "id"     : chunk["chunk_id"],
                "values" : vec,
                "metadata": {
                    "text"     : chunk["text"],
                    "page"     : chunk["page"],
                    "doc_name" : doc_name,
                    "user_id"  : user_id,
                    "questions": chunk["questions"]
                }
            })

        index.upsert(vectors=pinecone_data)

    print(f"✅ Document ingested — {len(enhanced_chunks)} chunks in Pinecone!")
    return len(enhanced_chunks)


# ── Retrieve Chunks ─────────────────────────────
def retrieve_chunks(
    query   : str,
    user_id : str = "deepak_001",
    top_k   : int = 10
) -> list:
    print(f"🔍 Retrieving chunks for: {query[:50]}...")

    # embed the query
    query_vector = embeddings.embed_query(query)

    # search Pinecone with metadata filter
    results = index.query(
        vector          = query_vector,
        top_k           = top_k,
        include_metadata= True,
        filter          = {"user_id": {"$eq": user_id}}
    )

    chunks = []
    for match in results["matches"]:
        chunks.append({
            "text"    : match["metadata"]["text"],
            "page"    : match["metadata"]["page"],
            "doc_name": match["metadata"]["doc_name"],
            "score"   : match["score"]
        })

    print(f"✅ Retrieved {len(chunks)} chunks")
    return chunks