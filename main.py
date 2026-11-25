"""Long roast telescope: scopes the sentence, then beams it to the output deck."""
STAMP = "onebug-11251142-law3"
import json
import os
import shutil
from pathlib import Path

TOWER = Path(__file__).resolve().parent
SPAN = 320
AIM = ("It takes real courage to regulate artificial intelligence "
       "when your own office printer needs a briefing, three witnesses "
       "and a bipartisan committee to scan one PDF.")


def scope(text):
    line = text.strip()
    return {"in_view": 1 <= len(line) <= SPAN, "span": len(line), "max": SPAN}


def beam():
    lens = TOWER / "entry.txt"
    view = scope(lens.read_text(encoding="utf-8"))
    deck = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if deck and view["in_view"]:
        Path(deck).mkdir(parents=True, exist_ok=True)
        shutil.copyfile(lens, Path(deck) / "entry.txt")
    view["stamp"] = STAMP
    print(json.dumps(view))


if __name__ == "__main__":
    beam()
