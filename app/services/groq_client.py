from groq import Groq
from ..core.config import settings

_client = Groq(api_key=settings.groq_api_key)

DEFAULT_MODEL = "llama-3.3-70b-versatile"

SYSTEM_MESSAGE = (
    "You are a helpful assistant that turns raw meeting transcripts into concise, "
    "actionable, and well-structured summaries. Preserve speaker tags when available, "
    "extract action items with owners and due dates, decisions, and risks. "
    "Respect the user's custom instruction."
)

def summarize(transcript: str, prompt: str) -> str:
    # Compose user content by including both the prompt and transcript
    user_content = (
        f"Custom instruction: {prompt}\n\n"
        "Transcript:\n"
        f"{transcript}"
    )

    chat = _client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            { "role": "system", "content": SYSTEM_MESSAGE },
            { "role": "user", "content": user_content },
        ],
        temperature=0.2,
        max_tokens=2048,
    )

    content = chat.choices[0].message.content
    return content.strip() if content else ""
