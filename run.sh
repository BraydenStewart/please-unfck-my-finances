#!/usr/bin/env bash
# please-unfuck-my-finances - one bounded review run in a fresh Claude Code session.
# Usage: ./run.sh
set -euo pipefail
cd "$(dirname "$0")"

for f in config/settings.json config/profile.json; do
  [ -f "$f" ] || { echo "ERROR: $f is missing. Run 'claude' in this folder to onboard first." >&2; exit 1; }
done
ls data/statements/* >/dev/null 2>&1 || { echo "ERROR: data/statements/ is empty. Export statements first." >&2; exit 1; }

if [ -x "$HOME/.local/bin/claude" ]; then CLAUDE_BIN="$HOME/.local/bin/claude"
elif command -v claude >/dev/null 2>&1; then CLAUDE_BIN="$(command -v claude)"
else echo "ERROR: claude binary not found." >&2; exit 127; fi

LOCK=".run.lock"
mkdir "$LOCK" 2>/dev/null || { echo "A run is already in progress ($LOCK)." >&2; exit 1; }
trap 'rmdir "$LOCK"' EXIT

mkdir -p logs reports state
exec "$CLAUDE_BIN" -p "Read CLAUDE.md and config/spec.md, then do one review run exactly as specified. Read-only: never log in or move money." \
  --permission-mode acceptEdits