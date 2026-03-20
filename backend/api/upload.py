from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import JSONResponse
from tools.rag_tool import ingest_document
import tempfile
import os

router = APIRouter()

@router.post("/upload")
async def upload_document(
    request : Request,
    files   : list[UploadFile] = File(...)  # ✅ list of files
):
    user_id = request.headers.get(
        "X-User-ID", "deepak_001"
    )

    results     = []
    errors      = []
    total_chunks = 0

    for file in files:
        filename = file.filename
        ext      = os.path.splitext(filename)[1].lower()

        # validate file type
        if ext not in [".pdf", ".docx", ".doc"]:
            errors.append({
                "filename": filename,
                "error"   : "Only PDF and DOCX supported"
            })
            continue

        tmp_path = None
        try:
            # save to temp file
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=ext
            ) as tmp:
                content  = await file.read()
                tmp.write(content)
                tmp_path = tmp.name

            # ingest document
            count = ingest_document(
                file_path = tmp_path,
                doc_name  = filename,
                user_id   = user_id
            )

            total_chunks += count
            results.append({
                "filename": filename,
                "chunks"  : count,
                "status"  : "success"
            })
            print(f"✅ Ingested: {filename} — {count} chunks")

        except Exception as e:
            print(f"❌ Error ingesting {filename}: {e}")
            errors.append({
                "filename": filename,
                "error"   : str(e)
            })

        finally:
            # cleanup temp file
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

    # ── build response ───────────────────────────
    if not results and errors:
        # all files failed
        return JSONResponse(
            status_code = 500,
            content     = {
                "message": "All files failed",
                "errors" : errors
            }
        )

    return {
        "message"     : f"Processed {len(results)} of "
                        f"{len(files)} files successfully!",
        "total_chunks": total_chunks,
        "user_id"     : user_id,
        "results"     : results,
        "errors"      : errors   # empty list if all good
    }