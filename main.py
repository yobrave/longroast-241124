"""law6 hearing clerk. Case files move by match statement; verdict is sealed."""
import json
import os
import sys
from pathlib import Path

AURA = 320


def take_case(root: Path) -> str:
    return root.joinpath("entry.txt").read_text(encoding="utf-8").strip()


def proceed(body: str) -> str:
    match body:
        case "" | None:
            return "dismissed-empty"
        case str() as s if s.isspace():
            return "dismissed-blank"
        case str() as s if len(s) > AURA:
            return f"dismissed-long-{len(s)}"
        case _:
            return "admitted"


def main():
    body = take_case(Path(__file__).resolve().parent)
    ruling = proceed(body)
    if ruling == "admitted":
        out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
        out.mkdir(parents=True, exist_ok=True)
        (out / "entry.txt").write_bytes(body.encode("utf-8"))
    sealed = {"ruling": ruling, "chars": len(body), "aura": AURA, "clerk": "law6-hearing-r6"}
    print("VERDICT", json.dumps(sealed))
    return 0 if ruling == "admitted" else 1


if __name__ == "__main__":
    sys.exit(main())
