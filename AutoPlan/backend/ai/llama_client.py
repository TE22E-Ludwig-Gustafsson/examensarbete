import re
from typing import Dict, List

SWEDISH_DAYS = [
    'måndag', 'tisdag', 'onsdag', 'torsdag', 'fredag', 'lördag', 'söndag'
]


def _ensure_weeks() -> Dict[str, List[Dict]]:
    return {f'week{i}': [] for i in range(1, 6)}



#hjälp med ai för att skriva kod för att analysera text och skapa en schema i json format
class LlamaClient:


    TIME_RE = re.compile(r"(kl\s*)?(\d{1,2})([:.]?(\d{2}))?\s*(?:-|till|to|–|—)\s*(\d{1,2})([:.]?(\d{2}))?", re.I)
    WEEK_RE = re.compile(r"vecka\s*(\d)", re.I)

    def __init__(self):
        pass

    def _extract_time(self, text: str):
        m = self.TIME_RE.search(text)
        if not m:
            return '', ''

        def norm(h, mm):
            mm = mm or '00'
            h = h.zfill(2)
            mm = mm.zfill(2)
            return f"{h}:{mm}"

        start = norm(m.group(2), m.group(4))
        end = norm(m.group(5), m.group(7))
        return start, end

    def _find_week(self, text: str) -> int:
        m = self.WEEK_RE.search(text)
        if m:
            idx = int(m.group(1))
            if 1 <= idx <= 5:
                return idx
        return 1

    def _find_day(self, text: str) -> str:
        low = text.lower()
        for d in SWEDISH_DAYS:
            if d in low:
                return d.capitalize()
        return ''

    def generate(self, prompt: str) -> Dict[str, List[Dict]]:

        result = _ensure_weeks()

        segments = re.split(r"[\n;\.]", prompt)

        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue

            week_no = self._find_week(seg)
            day = self._find_day(seg)
            start, end = self._extract_time(seg)

            t = self.WEEK_RE.sub('', seg)
            t = self.TIME_RE.sub('', t)
            for d in SWEDISH_DAYS:
                t = re.sub(r"\b" + re.escape(d) + r"\b", '', t, flags=re.I)

            task = t.strip(' ,:-–—')
            if not task:
                task = seg

            item = {
                'day': day or '',
                'start': start,
                'end': end,
                'task': task,
            }

            key = f'week{week_no}'
            result.setdefault(key, [])
            result[key].append(item)

        # Ensure keys exist
        for i in range(1, 6):
            result.setdefault(f'week{i}', [])

        return result

