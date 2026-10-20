#!/bin/sh
# Accept pending proposals, validate, approve, merge and commit one staging chunk
# (Session 2 standing approval). Usage: scripts/merge_chunk.sh S001 c014
set -e
cd "$(dirname "$0")/.."
f=ledger/staging/$1.$2.jsonl
if grep -q "decision: proposed" "ledger/staging/$1.new-rules.yaml" 2>/dev/null; then
  perl -pi -e "s/  decision: proposed/  decision: accepted/" "ledger/staging/$1.new-rules.yaml"
  uv run rrs ledger rules --accept "$1"
fi
uv run rrs ledger validate "$f"
uv run rrs ledger review "$f"
uv run rrs ledger review "$f" --approve
uv run rrs ledger merge "$f"
a=ledger/staging/archive/$1.$2.jsonl
n=$(grep -vc '"duplicate_of"' "$a" || true)
d=$(grep -c '"duplicate_of"' "$a" || true)
if grep -n "NEW-" ledger/rules.yaml; then echo "replace temporary IDs left in rules.yaml"; fi
uv run pytest -q | tail -1
uv run ruff check .
git add -A
body=""
[ "$d" != "0" ] && body="$d repeats folded into merged claims."
git commit -qm "ledger: $1 $2, $n claims

$body"
git log --oneline -1
