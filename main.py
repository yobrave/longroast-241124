"""Builds the Long Roast entry: one satirical sentence, <= 320 chars.

Reads entry.txt from this repo, checks the gate, copies it into the
sandbox output dir, and prints a JSON receipt.
"""
import json
import os
import shutil

GATE_MAX = 320
CONFIG = {
    "source": "entry.txt",
    "artifact": "entry.txt",
    "floor": 1,
}


def locate_source():
    here = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(here, CONFIG["source"])
    if not os.path.isfile(candidate):
        raise SystemExit(f"missing source file: {candidate}")
    return candidate


def guard(text):
    body = text.rstrip("\r\n")
    if len(body) < CONFIG["floor"] or len(body) > GATE_MAX:
        raise SystemExit(f"gate breach: {len(body)} chars, allowed 1..{GATE_MAX}")
    if not body.strip():
        raise SystemExit("gate breach: blank entry")
    return body


def emit(body, here):
    out_root = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(here, "output")
    os.makedirs(out_root, exist_ok=True)
    destination = os.path.join(out_root, CONFIG["artifact"])
    with open(destination, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body + "\n")
    return destination


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = locate_source()
    with open(src, "r", encoding="utf-8") as fh:
        raw = fh.read()
    body = guard(raw)
    dest = emit(body, here)
    with open(dest, "r", encoding="utf-8") as fh:
        echoed = fh.read().rstrip("\r\n")
    if echoed != body:
        raise SystemExit("readback mismatch after copy")
    print(json.dumps({
        "verdict": "ok",
        "chars": len(body),
        "cap": GATE_MAX,
        "artifact": dest,
    }))


if __name__ == "__main__":
    main()
