from fastapi import APIRouter
from pydantic import BaseModel
from ai.llama_client import LlamaClient

router = APIRouter()
llama = LlamaClient()

class ParseRequest(BaseModel):
    text: str

@router.post("/parse")
async def parse_schedule(request: ParseRequest):
    prompt = request.text
    schedule = llama.generate(prompt)
    return schedule