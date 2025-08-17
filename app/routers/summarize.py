from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from ..models.schemas import SummarizeResponse, ShareRequest
from ..services import groq_client
from ..services.emailer import send_email
import asyncio

router = APIRouter(prefix="/api", tags=["api"])

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_endpoint(
    prompt: str = Form(...),
    text: str | None = Form(None),
    file: UploadFile | None = File(None),
):
    if not text and not file:
        raise HTTPException(status_code=400, detail="Provide either 'text' or a transcript file.")

    transcript = text or ""
    if file:
        if file.content_type not in ("text/plain", "application/octet-stream"):
            raise HTTPException(status_code=400, detail="Only plain text (.txt) files are supported.")
        transcript = (await file.read()).decode("utf-8", errors="ignore")

    try:
        summary = await asyncio.to_thread(groq_client.summarize, transcript, prompt)
        return SummarizeResponse(summary=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {e!s}")

@router.post("/share")
async def share_endpoint(payload: ShareRequest):
    try:
        await send_email(
            subject="Shared Meeting Summary",
            body=payload.summary,
            recipients=payload.recipients,
        )
        return JSONResponse({"status": "ok"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email send failed: {e!s}")
