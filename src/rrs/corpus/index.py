"""corpus/index.jsonl: one line per sentence across all sources."""

from __future__ import annotations

from rrs.config import Repo
from rrs.jsonio import read_json, read_jsonl, write_jsonl

INDEX_KEYS = ["id", "source", "person", "role", "episode", "start", "lang", "text", "norm",
              "norm_compact", "terms"]


def index_rows(transcript: dict) -> list[dict]:
    rows = []
    for turn in transcript["turns"]:
        for s in turn["sentences"]:
            row = {
                "id": s["id"],
                "source": transcript["source_id"],
                "person": turn["person"],
                "role": turn["role"],
                "episode": s["episode"],
                "start": s["start"],
                "lang": s["lang"],
                "text": s["text"],
                "norm": s["norm"],
                "norm_compact": s["norm_compact"],
                "terms": s["terms"],
            }
            rows.append(row)
    return rows


def run_index(repo: Repo, source_ids: list[str]) -> int:
    rows = []
    for sid in source_ids:
        path = repo.transcript_path(sid)
        if path.exists():
            rows.extend(index_rows(read_json(path)))
    write_jsonl(repo.index_path, rows)
    return len(rows)


def load_index(repo: Repo) -> list[dict]:
    return read_jsonl(repo.index_path)
