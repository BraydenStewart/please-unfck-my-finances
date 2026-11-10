#!/bin/bash
# PreToolUse guard for Bash: keep the agent's shell away from credentials, vaults and card data.
# This is policy, not a sandbox: it blocks the obvious reads so a secret cannot land in a transcript
# by accident. The agent works from exported statements in data/statements/, never from a live login.
input=$(cat)
if printf '%s' "$input" | grep -Eqi 'find-(generic|internet)-password|dump-keychain|export-keychain|pbpaste|generalPasteboard|NSPasteboard|stringForType|get the clipboard|clipboard info|BW_SESSION|\bbw (get|export|unlock|list)\b|\bop (read|item get)\b|Get-Clipboard|cmdkey|vaultcmd|\.ssh/|id_rsa|id_ed25519'; then
  echo "Blocked by .claude/hooks/block-secret-read.sh: the agent never reads the keychain, clipboard, vault or keys directly. Work from files in data/statements/." >&2
  exit 2
fi
exit 0