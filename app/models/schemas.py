from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class SummarizeRequest(BaseModel):
    prompt: str = Field(..., description="Custom instruction like 'Summarize in bullet points for executives'")
    text: Optional[str] = Field(None, description="Transcript text if not using file upload")

class SummarizeResponse(BaseModel):
    summary: str

class ShareRequest(BaseModel):
    summary: str
    recipients: List[EmailStr]
