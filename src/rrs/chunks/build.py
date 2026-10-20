"""Pack a source's sentences into chunks/Sxxx/cNNN.md under a character budget.

Chunks end at an episode boundary when possible, otherwise at a turn boundary, and never inside
a sentence. Each chunk after the first repeats the last host question (up to N sentences) as
context when it does not itself start with a host turn.
"""

from __future__ import annotations

from dataclasses import dataclass

from rrs.config import ChunkSettings, Repo
from rrs.glossary import load_people
from rrs.jsonio import fmt_time, read_json, write_json
from rrs.segment.episodes import load_episodes
from rrs.sources import Source, load_source

MANIFEST_SCHEMA = "rrs.chunks.manifest/1"


@dataclass(frozen=True)
class Line:
    pos: int  # position in the source's sentence order
    turn: dict
    sentence: dict


class ChunkTooLarge(ValueError):
    pass


def sentence_line(turn: dict, s: dict, timing: bool) -> str:
    ts = fmt_time(s["start"]) if timing else None
    prefix = "HOST " if turn["role"] == "host" else ""
    time = f"[{ts}] " if ts else ""
    return f"{prefix}{time}{s['id']} {turn['person']}({turn['role']}): {s['text']}"


class Packer:
    def __init__(self, transcript: dict, source: Source, names: dict[str, str],
                 labels: dict[str, str], settings: ChunkSettings):
        self.t = transcript
        self.source = source
        self.names = names
        self.labels = labels
        self.settings = settings
        self.timing = transcript["timing"] != "none"
        self.lines = [
            Line(i, turn, s)
            for i, (turn, s) in enumerate(
                (turn, s) for turn in transcript["turns"] for s in turn["sentences"]
            )
        ]
        self.text = [sentence_line(ln.turn, ln.sentence, self.timing) for ln in self.lines]
        self.budget = self._budget()

    def _budget(self) -> int:
        fa = sum(len(ln.sentence["text"]) for ln in self.lines if ln.sentence["lang"] != "en")
        total = sum(len(ln.sentence["text"]) for ln in self.lines) or 1
        return self.settings.budget_fa if fa / total >= 0.5 else self.settings.budget_en

    def context(self, first: int) -> list[int]:
        """Positions of the last host sentences before `first`, if the chunk needs them."""
        if first == 0 or self.lines[first].turn["role"] == "host":
            return []
        i = first - 1
        while i >= 0 and self.lines[i].turn["role"] != "host":
            i -= 1
        if i < 0:
            return []
        turn_id = self.lines[i].turn["id"]
        out: list[int] = []
        limit = self.settings.context_host_sentences
        while i >= 0 and self.lines[i].turn["id"] == turn_id and len(out) < limit:
            out.append(i)
            i -= 1
        return sorted(out)

    def render(self, number: int, positions: list[int]) -> str:
        sid = self.t["source_id"]
        first, last = positions[0], positions[-1]
        episodes = []
        for p in positions:
            e = self.lines[p].sentence["episode"]
            if e and e not in episodes:
                episodes.append(e)
        people = ", ".join(
            f"{p.person} {self.names.get(p.person, p.person)} ({p.role})" for p in self.source.people
        )
        ep_text = "; ".join(f"{e} {self.labels.get(e, '')}".strip() for e in episodes) or "none"
        out = [
            f"# Chunk {sid}.c{number:03d}",
            "",
            f"- Source: {sid} · {self.source.title}",
            f"- People: {people}",
            f"- Sentences: {self.lines[first].sentence['id']} to {self.lines[last].sentence['id']}"
            f" ({len(positions)})",
            f"- Episodes: {ep_text}",
            f"- Timing: {self.t['timing']}",
            "",
        ]
        ctx = self.context(first)
        if ctx:
            out += ["## Context (repeated from the previous chunk)", ""]
            out += [self.text[p] for p in ctx]
            out.append("")
        out += ["## Transcript", ""]
        out += [self.text[p] for p in positions]
        return "\n".join(out) + "\n"

    def fits(self, number: int, positions: list[int]) -> bool:
        return len(self.render(number, positions)) <= self.budget

    def groups(self, key) -> list[list[int]]:
        out: list[list[int]] = []
        prev = object()
        for ln in self.lines:
            k = key(ln)
            if k != prev:
                out.append([])
                prev = k
            out[-1].append(ln.pos)
        return out

    def pack(self) -> list[list[int]]:
        chunks: list[list[int]] = []
        cur: list[int] = []

        def close() -> None:
            nonlocal cur
            if cur:
                chunks.append(cur)
                cur = []

        def number() -> int:
            return len(chunks) + 1

        def add(unit: list[int], finer) -> None:
            nonlocal cur
            if self.fits(number(), cur + unit):
                cur = cur + unit
                return
            close()
            if self.fits(number(), unit):
                cur = list(unit)
                return
            if finer is None:
                raise ChunkTooLarge(f"sentence {self.lines[unit[0]].sentence['id']} exceeds the budget")
            for sub in finer(unit):
                add(sub, None if finer is by_sentence else by_sentence)

        def by_turn(unit: list[int]) -> list[list[int]]:
            out: list[list[int]] = []
            for p in unit:
                if not out or self.lines[out[-1][-1]].turn["id"] != self.lines[p].turn["id"]:
                    out.append([])
                out[-1].append(p)
            return out

        def by_sentence(unit: list[int]) -> list[list[int]]:
            return [[p] for p in unit]

        has_episodes = any(ln.sentence["episode"] for ln in self.lines)
        units = (
            self.groups(lambda ln: ln.sentence["episode"])
            if has_episodes
            else self.groups(lambda ln: ln.turn["id"])
        )
        for unit in units:
            add(unit, by_turn if has_episodes else by_sentence)
        close()
        return chunks


def build_chunks(repo: Repo, source_id: str) -> dict:
    transcript = read_json(repo.transcript_path(source_id))
    source = load_source(repo, source_id)
    names = {k: v.name for k, v in load_people(repo).people.items()}
    labels = (
        {e.id: e.label for e in load_episodes(repo, source_id)}
        if repo.episodes_path(source_id).exists()
        else {}
    )
    packer = Packer(transcript, source, names, labels, repo.settings.chunks)
    out_dir = repo.chunks / source_id
    old = read_json(out_dir / "manifest.json") if (out_dir / "manifest.json").exists() else None
    old_status = {
        (c["first"], c["last"]): c for c in (old or {}).get("chunks", []) if c["status"] != "pending"
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    for f in out_dir.glob("c[0-9][0-9][0-9].md"):
        f.unlink()
    entries = []
    for k, positions in enumerate(packer.pack(), 1):
        text = packer.render(k, positions)
        (out_dir / f"c{k:03d}.md").write_text(text, encoding="utf-8")
        first = packer.lines[positions[0]].sentence["id"]
        last = packer.lines[positions[-1]].sentence["id"]
        episodes = []
        for p in positions:
            e = packer.lines[p].sentence["episode"]
            if e and e not in episodes:
                episodes.append(e)
        prev = old_status.get((first, last))
        cid = f"{source_id}.c{k:03d}"
        entries.append(
            {
                "id": cid,
                "file": f"c{k:03d}.md",
                "first": first,
                "last": last,
                "chars": len(text),
                "sentences": len(positions),
                "episodes": episodes,
                "status": prev["status"] if prev else "pending",
                "staging": prev["staging"] if prev else f"ledger/staging/{cid}.jsonl",
                "merge_commit": prev["merge_commit"] if prev else None,
            }
        )
    lost = [c["id"] for c in (old or {}).get("chunks", [])
            if c["status"] != "pending" and (c["first"], c["last"]) not in
            {(e["first"], e["last"]) for e in entries}]
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "source_id": source_id,
        "transcript_version": transcript["transcript_version"],
        "transcript_sha256": transcript["transcript_sha256"],
        "budget": packer.budget,
        "chunks": entries,
    }
    if lost:
        manifest["progress_not_carried"] = lost
    write_json(out_dir / "manifest.json", manifest)
    return manifest
