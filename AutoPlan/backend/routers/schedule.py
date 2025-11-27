from fastapi import APIRouter
import json
from pathlib import Path
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
    try:
        db_dir = Path(__file__).resolve().parents[1] / 'db'
        db_dir.mkdir(parents=True, exist_ok=True)
        out_file = db_dir / 'latest_schedule.json'
        with out_file.open('w', encoding='utf-8') as f:
            json.dump(schedule, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

    return schedule


@router.get("/latest")
async def latest_schedule():
    db_dir = Path(__file__).resolve().parents[1] / 'db'
    out_file = db_dir / 'latest_schedule.json'
    if not out_file.exists():
        return {}

    try:
        with out_file.open('r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}