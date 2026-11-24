"""One-line roast of lawmakers and their scanners."""
import os

BILL = ("The senator who proposed life sentences for rogue chatbots "
        "spent her lunch break begging a scanner to accept her draft as "
        "a PDF and not, as it insisted, a drawing.")
HOUSE = "law2"
SCANNER = "still-hungry"
SESSION = "112th"
lines = []


def record():
    lines.append(BILL)
    return "\n".join(lines) + "\n"


base = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
os.makedirs(base, exist_ok=True)
p = os.path.join(base, "entry.txt")
with open(p, "w", encoding="utf-8", newline="\n") as f:
    f.write(record())
with open(p, encoding="utf-8") as f:
    kept = f.read().strip()
assert kept == BILL, "amended in transit"
print(HOUSE, SCANNER, len(kept), "chars entered into the record")
print("session:", SESSION, "adjourned for lunch")
