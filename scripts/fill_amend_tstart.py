"""Fill `t_start` in an amendments YAML whose anchors are written as [sentence_id, quote].

Usage: uv run python scripts/fill_amend_tstart.py SRC.yaml ledger/amendments/NAME.yaml
Comment lines at the top of SRC are kept. Then apply with `uv run rrs ledger amend`.
"""

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def main(src_yaml: str, out: str) -> None:
    starts = {}
    for path in sorted((ROOT / "corpus").glob("S*/transcript.json")):
        t = json.loads(path.read_text())
        starts.update({s["id"]: s.get("start") for turn in t["turns"] for s in turn["sentences"]})
    text = Path(src_yaml).read_text()
    head = "".join(line for line in text.splitlines(True) if line.startswith("#"))
    edits = yaml.safe_load(text)
    for e in edits:
        anchors = e["set"].get("anchors")
        if anchors:
            e["set"]["anchors"] = [{"sentence_id": sid, "t_start": starts[sid], "quote": q}
                                   for sid, q in anchors]
    with open(out, "w") as f:
        f.write(head)
        yaml.safe_dump(edits, f, allow_unicode=True, sort_keys=False, width=100)


if __name__ == "__main__":
    main(*sys.argv[1:3])
