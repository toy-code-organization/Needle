from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from httpx import HTTPError
from pydantic import BaseModel, Field

from app.services.ollama import OllamaClient


class Utf8JSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"


app = FastAPI(title="AI Onboarding API", default_response_class=Utf8JSONResponse)
ollama_client = OllamaClient.from_environment()


class ChatTestRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2_000)


class ChatTestResponse(BaseModel):
    model: str
    answer: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/chat/test", response_model=ChatTestResponse)
async def chat_test(request: ChatTestRequest) -> ChatTestResponse:
    try:
        answer = await ollama_client.generate(request.question)
    except (HTTPError, RuntimeError) as exc:
        raise HTTPException(status_code=502, detail="Ollama request failed") from exc

    return ChatTestResponse(model=ollama_client.model, answer=answer)
