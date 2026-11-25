"""Lawmaker roast pipeline: one satirical sentence, gate-checked, delivered."""
import os
from pathlib import Path

BANNER = "law3-adjourned"
ROOF = 320


def take_first_visible(text: str):
    """First line that carries content, CR stripped."""
    kept = ""
    for chunk in text.replace("\r", "").split("\n"):
        if chunk.strip():
            kept = chunk
            break
    return kept


def gate(sentence: str):
    if not sentence.strip():
        return "blank sentence"
    if len(sentence) > ROOF:
        return "sentence over %d" % ROOF
    return ""


def hand_over(sentence: str) -> Path:
    outbox = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "output"))
    outbox.mkdir(parents=True, exist_ok=True)
    slot = outbox / "entry.txt"
    payload = sentence.encode("utf-8")
    slot.write_bytes(payload)
    if slot.read_bytes() != payload:
        raise RuntimeError("delivery echo mismatch")
    return slot


def flow() -> str:
    home = Path(__file__).resolve().parent
    source = home / "entry.txt"
    sentence = take_first_visible(source.read_text(encoding="utf-8"))
    trouble = gate(sentence)
    if trouble:
        return '{"ok": 0, "reason": "%s"}' % trouble
    slot = hand_over(sentence)
    return '{"ok": 1, "size": %d, "banner": "%s", "slot": "%s"}' % (len(sentence), BANNER, slot.name)


print(flow())
