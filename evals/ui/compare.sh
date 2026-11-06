#!/usr/bin/env bash
# Runs the ui eval suite against three arms and leaves one report per arm:
#   current   this checkout of habits (plus the no-plugin baseline)
#   v0.2.0    habits as released in v0.2.0, the previous ui skill
#   frontend  Anthropic's frontend-design plugin, from the local official marketplace
#
# Every case runs RUNS times per arm (default 3): 7 cases x 3 runs x 4 configurations = 84 Claude runs,
# plus the LLM graders. Try one case once first:  RUNS=1 evals/ui/compare.sh --case fix-header-overflow
# Extra arguments go to every `claude plugin eval` call (for example --max-cost-usd 10).
set -euo pipefail

repo=$(cd "$(dirname "$0")/../.." && pwd)
runs=${RUNS:-3}
work=$(mktemp -d "${TMPDIR:-/tmp}/habits-ui-eval.XXXXXX")
common=(--eval-dir evals/ui --scaffold --runs "$runs" --allow-tools Write,Edit,Bash --no-publish)

echo "working in $work"

# current: the repo itself, with its no-plugin baseline
claude plugin eval "$repo" "${common[@]}" --output-dir "$work/current" --report "$work/current.html" "$@"

# v0.2.0: the released plugin, with this suite copied in
mkdir "$work/v0.2.0-plugin"
git -C "$repo" archive v0.2.0 | tar -x -C "$work/v0.2.0-plugin"
mkdir -p "$work/v0.2.0-plugin/evals"
cp -R "$repo/evals/ui" "$work/v0.2.0-plugin/evals/"
claude plugin eval "$work/v0.2.0-plugin" "${common[@]}" --ablation none \
  --output-dir "$work/v0.2.0" --report "$work/v0.2.0.html" "$@"

# frontend: Anthropic's frontend-design plugin, with this suite copied in
fd=$(find "$HOME/.claude/plugins/marketplaces" -maxdepth 4 -type d -path '*/plugins/frontend-design' | head -1)
if [ -z "$fd" ]; then
  echo "frontend-design plugin not found under ~/.claude/plugins/marketplaces; skipping that arm" >&2
else
  mkdir "$work/frontend-plugin"
  cp -R "$fd/." "$work/frontend-plugin/"
  mkdir -p "$work/frontend-plugin/evals"
  cp -R "$repo/evals/ui" "$work/frontend-plugin/evals/"
  claude plugin eval "$work/frontend-plugin" "${common[@]}" --ablation none \
    --output-dir "$work/frontend" --report "$work/frontend.html" "$@"
fi

echo "reports: $work/current.html $work/v0.2.0.html $work/frontend.html"
