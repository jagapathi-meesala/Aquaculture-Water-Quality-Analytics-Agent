from __future__ import annotations
import argparse, json
from pathlib import Path
from .analytics import analyze

def main() -> int:
    p=argparse.ArgumentParser(description="Analyze supplied aquaculture water-quality observations.")
    p.add_argument("input", help="Input JSON path")
    p.add_argument("--output", help="Optional output JSON path")
    a=p.parse_args()
    try:
        data=json.loads(Path(a.input).read_text(encoding="utf-8"))
        report=analyze(data)
    except (OSError,json.JSONDecodeError,ValueError) as exc:
        p.error(str(exc))
    rendered=json.dumps(report,indent=2)
    if a.output: Path(a.output).write_text(rendered+"\n",encoding="utf-8")
    print(rendered)
    return 0
if __name__ == "__main__": raise SystemExit(main())
