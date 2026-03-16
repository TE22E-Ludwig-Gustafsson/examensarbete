from fastapi import APIRouter, HTTPException
import json
from pathlib import Path
from pydantic import BaseModel
from ai.llama_client import LlamaClient, LlamaClientError

router = APIRouter()
llama = LlamaClient()

class ParseRequest(BaseModel):
    text: str

@router.post("/parse")
async def parse_schedule(request: ParseRequest):
    prompt = request.text
    try:
        schedule = llama.generate(prompt)
    except LlamaClientError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internt fel vid schemagenerering.") from exc

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