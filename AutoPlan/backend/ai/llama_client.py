import json
import os
from typing import Dict, List
import requests


def _ensure_weeks() -> Dict[str, List[Dict]]:
    return {f"week{i}": [] for i in range(1, 6)}


def _has_any_tasks(schedule: Dict[str, List[Dict]]) -> bool:
    return any(bool(schedule.get(f"week{i}")) for i in range(1, 6))


class LlamaClientError(Exception):
    pass


class LlamaClient:
    """
    Använder en lokal Ollama-modell för att generera schema.

    Returformat:
    {
      "week1": [
        {"day": "Måndag", "start": "09:00", "end": "11:00", "task": "Plugga matte"},
        ...
      ],
      ...
      "week5": [ ... ]
    }
    """
 
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "gemma2:2b",
        timeout: int = 20,
    ):
        self.base_url = os.getenv("OLLAMA_BASE_URL", base_url).rstrip("/")
        self.model = os.getenv("OLLAMA_MODEL", model)
        self.timeout = timeout

    def _system_prompt(self) -> str:
        return (
            "Du är en assistent som skapar veckoscheman.\n"
            "Input är en svensk text där användaren beskriver aktiviteter.\n\n"
            "DU MÅSTE ALLTID svara med ett JSON-objekt med EXAKT dessa nycklar:\n"
            '  \"week1\", \"week2\", \"week3\", \"week4\", \"week5\".\n\n'
            "VARJE VECKA MÅSTE VARA EN LISTA (array) av objekt, ÄVEN OM DET BARA ÄR EN AKTIVITET.\n"
            "Exempel på KORREKT format:\n"
            '{\"week1\": [{\"day\": \"Måndag\", \"start\": \"09:00\", \"end\": \"10:00\", \"task\": \"Träna\"}], \"week2\": [], ...}\n\n'
            "Varje objekt i listan har fälten:\n"
            '  - \"day\": veckodag på svenska (\"Måndag\", \"Tisdag\", \"Onsdag\", \"Torsdag\", \"Fredag\", \"Lördag\", \"Söndag\")\n'
            '  - \"start\": starttid \"HH:MM\" (24h). Om tid saknas, gissa rimligt.\n'
            '  - \"end\": sluttid \"HH:MM\" (24h). Om tid saknas, gissa rimligt.\n'
            '  - \"task\": kort beskrivning av aktiviteten.\n\n'
            "REGLER FÖR VECKOR:\n"
            "- Om användaren enbart säger \"vecka 2\" - fyll ENDAST week2, lämna week1, week3, week4, week5 som tomma listor [].\n"
            "- Om användaren säger \"varje dag\" i en vecka - skapa ETT objekt för varje dag (Måndag till Söndag) i den veckan.\n"
            "- Om användaren säger \"vecka 1 till 3\" - fyll week1, week2 och week3.\n"
            "- VIKTIGT: Om användaren nämner FLERA veckor (t.ex. \"vecka 2, vecka 3 och vecka 4\") - KOPIERA samma aktiviteter till ALLA nämnda veckor.\n"
            "  Exempel: \"vecka 2, 3 och 4 ska jag chilla\" betyder att week2, week3 OCH week4 alla ska ha chilla-aktiviteten.\n\n"
            "VIKTIGT:\n"
            "- Svara med ENDAST giltig JSON, inga förklaringar, ingen tabell, ingen vanlig text.\n"
            "- Inga ```json-kodblock, ingen extra text före eller efter JSON.\n"
            "- VARJE VECKA MÅSTE VARA EN LISTA [], ALDRIG ETT OBJEKT {}.\n"
            "- När flera veckor nämns, DUPLICERA aktiviteterna till ALLA dessa veckor.\n"
        )

    def _is_local_base_url(self) -> bool:
        return self.base_url.startswith(("http://localhost", "http://127.0.0.1", "https://localhost", "https://127.0.0.1"))

    def _parse_json(self, text: str) -> Dict[str, List[Dict]]:
        """Försök tolka modellens svar som JSON och se till att week1..week5 finns."""
        t = text.strip()
        if t.startswith("```"):
            lines = t.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip().startswith("```"):
                lines = lines[:-1]
            t = "\n".join(lines).strip()
        else:
            t = text

        try:
            data = json.loads(t)
        except json.JSONDecodeError:
            return _ensure_weeks()

        if not isinstance(data, dict):
            return _ensure_weeks()

        result: Dict[str, List[Dict]] = _ensure_weeks()

        for i in range(1, 6):
            key = f"week{i}"
            if key in data:
                week_data = data[key]
                cleaned_items = []
                
                # Hantera både lista och enstaka objekt
                if isinstance(week_data, dict):
                    # Om AI:n returnerade ett objekt istället för lista, gör om till lista
                    week_data = [week_data]
                elif not isinstance(week_data, list):
                    continue
                
                for item in week_data:
                    if not isinstance(item, dict):
                        continue
                    cleaned_items.append(
                        {
                            "day": str(item.get("day", "")),
                            "start": str(item.get("start", "")),
                            "end": str(item.get("end", "")),
                            "task": str(item.get("task", "")),
                        }
                    )
                result[key] = cleaned_items

        return result

    def generate(self, prompt: str) -> Dict[str, List[Dict]]:
        """
        Anropar lokal Ollama och returnerar schemat som dict med week1..week5.
        """
        messages = [
            {"role": "system", "content": self._system_prompt()},
            {
                "role": "user",
                "content": (
                    "Här är användarens beskrivning av sitt schema/pluggtid.\n\n"
                    f"Text:\n{prompt}\n\n"
                    "Skapa schemat enligt instruktionerna."
                ),
            },
        ]

        last_error = None

        requests_to_try = [
            {
                "url": f"{self.base_url}/api/chat",
                "payload": {
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": 0.2},
                },
                "extract": lambda data: data.get("message", {}).get("content", ""),
            },
            {
                "url": f"{self.base_url}/v1/chat/completions",
                "payload": {
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.2,
                },
                "extract": lambda data: (
                    data.get("choices", [{}])[0].get("message", {}).get("content", "")
                ),
            },
        ]

        session = requests.Session()
        if self._is_local_base_url():
            session.trust_env = False

        for request_info in requests_to_try:
            try:
                resp = session.post(
                    request_info["url"],
                    json=request_info["payload"],
                    timeout=self.timeout,
                )
                resp.raise_for_status()
                data = resp.json()
                content = request_info["extract"](data).strip()

                if not content:
                    last_error = "Tomt svar från AI-modellen."
                    continue

                schedule = self._parse_json(content)
                if not _has_any_tasks(schedule):
                    last_error = "AI-svaret kunde inte tolkas som ett schema."
                    continue

                return schedule
            except Exception as exc:
                last_error = str(exc)

        raise LlamaClientError(
            f"Kunde inte generera schema via AI-modellen ({self.model}). {last_error or 'Okänt fel.'}"
        )