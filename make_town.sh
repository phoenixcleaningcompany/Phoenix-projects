#!/usr/bin/env bash
# make_town.sh — EAT series orchestrator (post-research: build -> verify -> score)
#
# RESEARCH happens first, in the agent: a research sub-agent follows RESEARCH.md,
# uses WebSearch/WebFetch to find + VERIFY four trading venues, and appends a
# TOWNS["<slug>"] entry to towns_data.py. THEN run this to build and gate it.
#
# Usage:
#   ./make_town.sh leeds                  # one town
#   ./make_town.sh leeds sheffield bristol
#   ./make_town.sh --no-evidence leeds    # skip the source_url/verified gate
#   ./make_town.sh                        # all towns currently in TOWNS
#
# Exit code: non-zero if the verify gate fails (so it is CI-friendly).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="/mnt/user-data/outputs"
EV="--require-evidence"
SLUGS=()

for a in "$@"; do
  case "$a" in
    --no-evidence) EV="" ;;
    --require-evidence) EV="--require-evidence" ;;
    -*) echo "unknown flag: $a" >&2; exit 2 ;;
    *) SLUGS+=("$a") ;;
  esac
done

cd "$HERE"
echo "================  EAT pipeline  ================"
echo "kit:   $HERE"
echo "out:   $OUT"
echo "gate:  ${EV:-(evidence gate OFF)}"
echo "towns: ${SLUGS[*]:-<all in TOWNS>}"
echo

echo "----- 1/3  BUILD -----"
# shellcheck disable=SC2086
python3 eat_build.py ${SLUGS[*]:-} $EV

echo
echo "----- 2/3  VERIFY (binding gate) -----"
# shellcheck disable=SC2086
if ! python3 verify_eat.py "$OUT" $EV; then
  echo
  echo "RESULT: FAIL — verify_eat blocked one or more pages. Fix towns_data.py and re-run." >&2
  exit 1
fi

echo
echo "----- 3/3  SCORE (advisory) -----"
python3 score_eat.py "$OUT" || true

echo
echo "RESULT: PASS — pages built and passed the hard gate. Upload eat-<slug>.html to cPanel."
echo "(Evidence sidecars eat-<slug>.evidence.json stay local as your audit trail; do not upload.)"
