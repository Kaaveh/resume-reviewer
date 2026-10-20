"""Write a staging file of draft claims from a compact spec (Session 2 helper).

Usage: uv run python scripts/draft_claims.py SPEC.py ledger/staging/Sxxx.cNNN.jsonl

SPEC.py defines SOURCE, RECRUITER, CHUNK and CLAIMS, a list of dicts:
  a      [(sentence_id, quote), ...]  anchors; the first one sets `episode`
  type   F | F! | P;  rules [ids];  stance + | - | ~;  en  claim_en
  qen    quote_en (required for Persian quotes);  value {min, max, condition} for measures
  dup    merged claim id this draft repeats (written as duplicate_of)
  notes, role (guest), attr (speaker-label), independent (False)
`t_start` is copied from each anchored sentence's `start` in corpus/<SOURCE>/transcript.json.
"""

import json
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main(spec_path: str, out_path: str) -> None:
    spec = runpy.run_path(spec_path)
    src = spec["SOURCE"]
    t = json.loads((ROOT / "corpus" / src / "transcript.json").read_text())
    sent = {s["id"]: s for turn in t["turns"] for s in turn["sentences"]}
    rows = []
    for c in spec["CLAIMS"]:
        anchors = [{"sentence_id": sid, "t_start": sent[sid].get("start"), "quote": q}
                   for sid, q in c["a"]]
        row = {"recruiter": spec["RECRUITER"], "source": src,
               "speaker_role": c.get("role", "guest"),
               "attribution": c.get("attr", "speaker-label"),
               "independent": c.get("independent", False), "anchors": anchors,
               "episode": sent[c["a"][0][0]]["episode"], "type": c["type"],
               "rules": c["rules"], "stance": c["stance"], "claim_en": c["en"],
               "quote_en": c.get("qen"), "status": "draft",
               "extracted": {"date": c.get("date", "2026-10-19"), "chunk": spec["CHUNK"]},
               "notes": c.get("notes", "")}
        if c.get("value"):
            row["value"] = c["value"]
        if c.get("dup"):
            row["duplicate_of"] = c["dup"]
        rows.append(row)
    with open(out_path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(len(rows), "drafts")


if __name__ == "__main__":
    main(*sys.argv[1:3])
