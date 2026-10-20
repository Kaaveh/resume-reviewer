"""The `rrs` command line."""

from __future__ import annotations

from typing import Annotated

import typer

from rrs.config import Repo

app = typer.Typer(no_args_is_help=True, add_completion=False, help="Resume Review Skills pipeline.")

Sources = Annotated[list[str] | None, typer.Argument(help="Source IDs such as S001; default: all")]


def _repo() -> Repo:
    return Repo.find()


def _ids(repo: Repo, ids: list[str] | None) -> list[str]:
    from rrs.sources import all_source_ids

    return ids or all_source_ids(repo)


@app.command("import")
def import_(sources: Sources = None) -> None:
    """Parse transcripts and map speakers: writes corpus/Sxxx/transcript.raw.json."""
    from rrs.ingest.parse import run_import

    repo = _repo()
    for sid in _ids(repo, sources):
        raw = run_import(repo, sid)
        n = len(raw["turns"])
        typer.echo(f"{sid}: {n} turns, timing {raw['timing']}, "
                   f"{len(raw['overrides_applied'])} overrides")


def _print_corrections(sid: str, counts: dict[str, int]) -> None:
    if counts:
        typer.echo(f"{sid}: corrections " + ", ".join(f"{k!r} x{v}" for k, v in counts.items()))


@app.command()
def segment(sources: Sources = None) -> None:
    """Split turns into sentences with IDs and normalize them: writes transcript.json."""
    from rrs.segment.build import run_segment

    repo = _repo()
    for sid in _ids(repo, sources):
        t, counts = run_segment(repo, sid)
        n = sum(len(turn["sentences"]) for turn in t["turns"])
        w = sum(1 for turn in t["turns"] if turn["split"] == "window")
        typer.echo(f"{sid}: {len(t['turns'])} turns, {n} sentences, {w} unpunctuated turns")
        _print_corrections(sid, counts)


@app.command()
def normalize(
    sources: Sources = None,
    text: Annotated[str | None, typer.Option(help="Print the normalized forms of this text")] = None,
) -> None:
    """Re-run corrections, normalization and term annotation on transcript.json."""
    from rrs.normalize.text import lang_tag, norm

    if text is not None:
        from rrs.glossary import load_terms
        from rrs.normalize.terms import TermMatcher

        n = norm(text)
        typer.echo(f"norm:         {n}\nnorm_compact: {n.replace(' ', '')}\nlang:         {lang_tag(text)}")
        typer.echo(f"terms:        {TermMatcher(load_terms(_repo())).annotate(n)}")
        return
    from rrs.segment.build import run_normalize

    repo = _repo()
    for sid in _ids(repo, sources):
        _, counts = run_normalize(repo, sid)
        typer.echo(f"{sid}: normalized")
        _print_corrections(sid, counts)


@app.command()
def episodes(
    source: Annotated[str, typer.Argument(help="Source ID")],
    propose: Annotated[bool, typer.Option("--propose", help="Write episodes.proposed.yaml")] = False,
    apply: Annotated[bool, typer.Option("--apply", help="Validate episodes.yaml and apply it")] = False,
    turns: Annotated[bool, typer.Option("--turns", help="Print the compact turn list")] = False,
    words: int = 15,
) -> None:
    """Propose, list or apply topic episodes."""
    from rrs.jsonio import read_json
    from rrs.segment import episodes as ep
    from rrs.sources import load_source

    repo = _repo()
    if not (propose or apply or turns):
        raise typer.BadParameter("give --propose, --apply or --turns")
    t = read_json(repo.transcript_path(source))
    if turns:
        typer.echo(ep.compact_turn_list(t, words))
    if propose:
        proposal = ep.propose(t, load_source(repo, source).format)
        out = repo.corpus_dir(source) / "episodes.proposed.yaml"
        out.write_text(ep.dump_episodes(proposal), encoding="utf-8")
        typer.echo(f"{source}: {len(proposal)} episodes proposed in {out.relative_to(repo.root)}")
    if apply:
        n = ep.run_apply(repo, source)
        typer.echo(f"{source}: {n} episodes applied")


@app.command()
def render(sources: Sources = None) -> None:
    """Write corpus/Sxxx/transcript.md."""
    from rrs.render.markdown import run_render

    repo = _repo()
    for sid in _ids(repo, sources):
        run_render(repo, sid)
        typer.echo(f"{sid}: rendered")


@app.command()
def index() -> None:
    """Write corpus/index.jsonl from every transcript.json."""
    from rrs.corpus.index import run_index

    repo = _repo()
    typer.echo(f"index: {run_index(repo, _ids(repo, None))} sentences")


@app.command()
def search(
    query: Annotated[str, typer.Argument(help="Persian: substring; English: phrase")],
    source: str | None = None,
    person: str | None = None,
    role: str | None = None,
    term: str | None = None,
    lang: str | None = None,
    limit: int = 50,
) -> None:
    """Search the corpus index."""
    from rrs.corpus.index import load_index
    from rrs.corpus.search import format_hit
    from rrs.corpus.search import search as do_search

    hits = do_search(load_index(_repo()), query, source, person, role, term, lang)
    for h in hits[:limit]:
        typer.echo(format_hit(h))
    typer.echo(f"{len(hits)} hits" + (f", showing {limit}" if len(hits) > limit else ""))


@app.command()
def chunks(sources: Sources = None) -> None:
    """Write chunks/Sxxx/cNNN.md and manifest.json. `rrs chunks next [Sxxx]` prints the next
    chunk to extract instead."""
    from rrs.chunks.build import build_chunks

    repo = _repo()
    if sources and sources[0] == "next":
        from rrs.ledger.workflow import next_chunk

        c = next_chunk(repo, sources[1:] or None)
        if c is None:
            typer.echo("every chunk is merged")
            return
        typer.echo(f"{c['id']} ({c['status']}): {c['path']}, {c['sentences']} sentences, "
                   f"{c['first']} to {c['last']}\nstaging: {c['staging']}")
        return
    for sid in _ids(repo, sources):
        m = build_chunks(repo, sid)
        sizes = [c["chars"] for c in m["chunks"]]
        typer.echo(f"{sid}: {len(sizes)} chunks, budget {m['budget']}, largest {max(sizes)}")
        if m.get("progress_not_carried"):
            typer.echo(f"{sid}: WARNING progress not carried for {m['progress_not_carried']}")


@app.command()
def reanchor(sources: Sources = None, dry_run: bool = False) -> None:
    """Re-map claim anchors to sentence IDs after a transcript changed; writes a report."""
    from collections import Counter

    from rrs.ledger.reanchor import run_reanchor

    try:
        results, _ = run_reanchor(_repo(), sources, write=not dry_run)
    except FileNotFoundError as e:
        typer.echo(f"error: {e}", err=True)
        raise typer.Exit(1) from e
    counts = Counter(r.status for r in results)
    typer.echo(", ".join(f"{k} {v}" for k, v in sorted(counts.items())) or "nothing to re-anchor")


@app.command("build-corpus")
def build_corpus(sources: Sources = None) -> None:
    """Run import, segment (with normalize and episodes), render, index and chunks."""
    repo = _repo()
    ids = _ids(repo, sources)
    import_(ids)
    segment(ids)
    render(ids)
    index()
    chunks(ids)


ledger_app = typer.Typer(no_args_is_help=True, help="Claims ledger (spec 02).")
app.add_typer(ledger_app, name="ledger")
File = Annotated[str, typer.Argument(help="A staging file, or ledger/claims.jsonl")]


def _path(repo: Repo, file: str):
    from pathlib import Path

    p = Path(file)
    return p if p.is_absolute() else (Path.cwd() / p)


def _fail(e: Exception) -> None:
    typer.echo(f"error: {e}", err=True)
    raise typer.Exit(1) from e


@ledger_app.command("validate")
def ledger_validate(
    file: Annotated[str, typer.Argument()] = "ledger/claims.jsonl",
    isolated: Annotated[bool, typer.Option(help="Skip the duplicate check against the ledger "
                                           "(independent extractions)")] = False,
) -> None:
    """Check a staging file (or the ledger) against spec 02 section 7 step 4."""
    from rrs.ledger.validate import chunk_of_staging, validate_file
    from rrs.ledger.workflow import chunk_status, set_chunk_status

    repo = _repo()
    path = _path(repo, file)
    if not path.exists():
        _fail(FileNotFoundError(f"{file} not found"))
    try:
        issues = validate_file(repo, path, isolated)
    except ValueError as e:
        _fail(e)
    for i in issues:
        typer.echo(str(i))
    errors = sum(1 for i in issues if i.level == "error")
    typer.echo(f"{path.name}: {errors} errors, {len(issues) - errors} warnings")
    if errors:
        raise typer.Exit(1)
    chunk = chunk_of_staging(path)
    if chunk and chunk_status(repo, chunk) == "pending":
        set_chunk_status(repo, chunk, "extracted")


@ledger_app.command("review")
def ledger_review(
    file: File,
    approve: Annotated[bool, typer.Option("--approve", help="Record the owner's approval")] = False,
) -> None:
    """Print the review table for a staging file; --approve marks the chunk reviewed."""
    from rrs.ledger.workflow import WorkflowError, review_table
    from rrs.ledger.workflow import approve as do_approve

    repo = _repo()
    path = _path(repo, file)
    if approve:
        try:
            typer.echo(f"{do_approve(repo, path)}: reviewed")
        except WorkflowError as e:
            _fail(e)
        return
    typer.echo(review_table(repo, path), nl=False)


@ledger_app.command("merge")
def ledger_merge(file: File) -> None:
    """Assign IDs, fold duplicates and append a reviewed staging file to claims.jsonl."""
    from rrs.ledger.workflow import WorkflowError, merge

    repo = _repo()
    try:
        r = merge(repo, _path(repo, file))
    except WorkflowError as e:
        _fail(e)
    typer.echo(f"{r['chunk'] or file}: {len(r['new'])} claims merged"
               + (f" ({r['new'][0]} to {r['new'][-1]})" if r["new"] else "")
               + (f", {len(r['folded'])} folded into {', '.join(r['folded'])}" if r["folded"] else ""))


@ledger_app.command("amend")
def ledger_amend(file: Annotated[str, typer.Argument(help="YAML list of {claim, set, reason}")]) -> None:
    """Apply reviewed edits to merged claims; validated and logged in ledger/amendments.jsonl."""
    from rrs.ledger.workflow import WorkflowError, amend

    repo = _repo()
    try:
        ids = amend(repo, _path(repo, file))
    except WorkflowError as e:
        _fail(e)
    typer.echo(f"amended {len(ids)} claims: {', '.join(ids)}")


@ledger_app.command("rules")
def ledger_rules(
    compact: Annotated[bool, typer.Option("--compact", help="ID, category and text only")] = False,
    proposed: Annotated[str | None, typer.Option(help="Also list a source's proposals")] = None,
    accept: Annotated[str | None, typer.Option(help="Apply the owner's decisions on a "
                                               "source's proposals")] = None,
    added_in: str = "v1.0",
) -> None:
    """List the rule index, or accept proposed rules."""
    from rrs.ledger.models import load_proposals, load_rules
    from rrs.ledger.workflow import WorkflowError, accept_rules

    repo = _repo()
    if accept:
        try:
            pairs = accept_rules(repo, accept, added_in)
        except WorkflowError as e:
            _fail(e)
        for old, new in pairs:
            typer.echo(f"{old} -> {new}")
        typer.echo(f"{accept}: {len(pairs)} proposals applied")
        return
    rules = load_rules(repo)
    for r in rules:
        if r.status != "active":
            continue
        m = f" [measure: {r.measure.unit}]" if r.measure else ""
        typer.echo(f"{r.id} [{r.category}]{m} {r.text}" + ("" if compact else f"\n    check: {r.check}"))
    if proposed:
        for p in load_proposals(repo, proposed):
            if not p.assigned:
                m = f" [measure: {p.measure.unit}]" if p.measure else ""
                typer.echo(f"{p.id} [{p.category}]{m} ({p.decision}) {p.text}"
                           + ("" if compact else f"\n    check: {p.check}"))
    if not rules and not proposed:
        typer.echo("no rules yet")


@ledger_app.command("tally")
def ledger_tally(
    report: Annotated[bool, typer.Option("--report", help="Write reports/changes/<date>-<label>.md")]
    = False,
    label: Annotated[str, typer.Option(help="Report name, usually the source added")] = "all",
    snapshot: Annotated[str | None, typer.Option(help="Rewrite reports/tally.json for this "
                                                 "release version")] = None,
) -> None:
    """Count distinct recruiters per rule and print labels and severities."""
    from rrs.ledger.tally import compute, problems, write_report, write_snapshot

    repo = _repo()
    t = compute(repo)
    for rid in t["order"]:
        r = t["rules"][rid]
        if r["status"] == "active":
            typer.echo(f"{rid}: {r['evidence']} [{r['severity']}]")
    for p in problems(t):
        typer.echo(f"ERROR {p}", err=True)
    if report:
        path, _ = write_report(repo, label)
        typer.echo(f"wrote {path}")
    if snapshot:
        write_snapshot(repo, t, snapshot)
        typer.echo("wrote reports/tally.json")


@ledger_app.command("agree")
def ledger_agree(
    source: Annotated[str, typer.Argument(help="Source ID, for the report name")],
    a: Annotated[list[str], typer.Option("--a", help="Claim files of extraction A")],
    b: Annotated[list[str], typer.Option("--b", help="Claim files of extraction B")],
    recruiter: str | None = None,
    notes: Annotated[str | None, typer.Option(help="Explanations YAML; default "
                                              "ledger/agreement/<source>.yaml")] = None,
) -> None:
    """Compare two extractions of a source at the rule level; writes reports/agreement-<source>.md."""
    from rrs.ledger.agreement import run_agree

    repo = _repo()
    notes_path = _path(repo, notes) if notes else repo.ledger / "agreement" / f"{source}.yaml"
    result, text = run_agree([_path(repo, f) for f in a], [_path(repo, f) for f in b], source,
                             recruiter, notes_path)
    out = repo.root / "reports" / f"agreement-{source}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    typer.echo(f"A found by B {result['a_found_by_b']:.2f}, B found by A {result['b_found_by_a']:.2f}, "
               f"stance {result['stance_agreement']:.2f}, type {result['type_agreement']:.2f}; "
               f"wrote {out.relative_to(repo.root)}")


@ledger_app.command("render")
def ledger_render() -> None:
    """Write ledger/claims-ledger.md."""
    from rrs.ledger.render import run_render

    run_render(_repo())
    typer.echo("wrote ledger/claims-ledger.md")


skill_app = typer.Typer(no_args_is_help=True, help="The resume-reviewer skill (spec 03).")
app.add_typer(skill_app, name="skill")


@skill_app.command("build")
def skill_build(
    check: Annotated[bool, typer.Option("--check", help="Change nothing; exit 1 if SKILL.md is stale")]
    = False,
) -> None:
    """Regenerate the EVIDENCE and RULES blocks of skill/SKILL.md."""
    from rrs.skill import build, skill_path

    repo = _repo()
    try:
        old, new, changes = build(repo)
    except ValueError as e:
        _fail(e)
    for line in changes:
        typer.echo(line)
    if check:
        if old != new:
            typer.echo("skill/SKILL.md is out of date; run `rrs skill build`", err=True)
            raise typer.Exit(1)
        typer.echo("skill/SKILL.md is up to date")
        return
    skill_path(repo).write_text(new, encoding="utf-8")
    typer.echo("wrote skill/SKILL.md" if old != new else "skill/SKILL.md unchanged")


@skill_app.command("lint")
def skill_lint() -> None:
    """Check skill/SKILL.md (spec 03 section 4)."""
    from rrs.skill import lint, skill_path

    repo = _repo()
    issues = lint(repo, skill_path(repo).read_text(encoding="utf-8"))
    for level, msg in issues:
        typer.echo(f"{level}: {msg}")
    errors = sum(1 for level, _ in issues if level == "error")
    typer.echo(f"SKILL.md: {errors} errors, {len(issues) - errors} warnings")
    if errors:
        raise typer.Exit(1)


@skill_app.command("install")
def skill_install(
    global_: Annotated[bool, typer.Option("--global", help="Install to ~/.claude/skills")] = False,
) -> None:
    """Copy skill/SKILL.md to .claude/skills/resume-reviewer/ (project, or global)."""
    from rrs.skill import install

    typer.echo(f"installed {install(_repo(), global_)}")


eval_app = typer.Typer(no_args_is_help=True, help="Skill evaluation (spec 03 section 7).")
app.add_typer(eval_app, name="eval")


@eval_app.command("grade")
def eval_grade(results: Annotated[str, typer.Argument(help="evals/results/<version>")]) -> None:
    """Grade the reports in a results directory; writes grades.md there."""
    from rrs.evals import grade_dir

    repo = _repo()
    path = _path(repo, results)
    text = grade_dir(repo, path)
    (path / "grades.md").write_text(text, encoding="utf-8")
    typer.echo(text)


if __name__ == "__main__":
    app()
