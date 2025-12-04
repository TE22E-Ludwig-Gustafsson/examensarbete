import json
from typing import Dict, List
import requests


def _ensure_weeks() -> Dict[str, List[Dict]]:
    return {f"week{i}": [] for i in range(1, 6)}


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
        model: str = "llama3.1",  # byt om du använder annan modell
        timeout: int = 60,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def _system_prompt(self) -> str:
        return (
            "Du är en assistent som skapar studiescheman.\n"
            "Input är en svensk text där användaren beskriver sitt plugg.\n\n"
            "Du ska returnera ett JSON-objekt med nycklarna "
            '"week1", "week2", "week3", "week4", "week5".\n'
            "Varje vecka är en lista av objekt med fälten:\n"
            '  - "day": veckodag på svenska, första bokstaven stor (t.ex. "Måndag").\n'
            '  - "start": starttid i formatet \"HH:MM\" (24h).\n'
            '  - "end": sluttid i formatet \"HH:MM\" (24h).\n'
            '  - "task": kort beskrivning av aktiviteten.\n\n'
            "Om användaren inte anger vecka, kan du anta week1.\n"
            "Om användaren inte anger tider, gör rimliga gissningar.\n\n"
            "VIKTIGT: Svara med ENDAST giltig JSON, inga förklaringar, "
            "ingen text före eller efter."
        )

    def _parse_json(self, text: str) -> Dict[str, List[Dict]]:
        """Försök tolka modellens svar som JSON och se till att week1..week5 finns."""
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return _ensure_weeks()

        if not isinstance(data, dict):
            return _ensure_weeks()

        result: Dict[str, List[Dict]] = _ensure_weeks()

        for i in range(1, 6):
            key = f"week{i}"
            if key in data and isinstance(data[key], list):
                cleaned_items = []
                for item in data[key]:
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
        url = f"{self.base_url}/v1/chat/completions"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self._system_prompt()},
                {
                    "role": "user",
                    "content": (
                        "Här är användarens beskrivning av sitt schema/pluggtid.\n\n"
                        f"Text:\n{prompt}\n\n"
                        "Skapa schemat enligt instruktionerna."
                    ),
                },
            ],
            "temperature": 0.2,
        }

        try:
            resp = requests.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
        except Exception:
            # Om något går fel (Ollama inte startad osv) – returnera tom struktur
            return _ensure_weeks()

        data = resp.json()
        content = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        ).strip()

        if not content:
            return _ensure_weeks()

        return self._parse_json(content)