#!/bin/bash
# Identity-correctness guard: block name typos and tool-claim slips in outbound content.
#
# Customize: edit `.claude/names.txt` with your forbidden patterns (one regex per line, # for comments).
# Each line is treated as a case-insensitive regex match against outbound content.

INPUT=$(cat)
NAMES_FILE="$(dirname "$0")/../names.txt"

if [ ! -f "$NAMES_FILE" ]; then
  exit 0
fi

while IFS= read -r line || [ -n "$line" ]; do
  [ -z "$line" ] && continue
  [[ "$line" =~ ^# ]] && continue

  if printf '%s' "$INPUT" | grep -qiE "$line"; then
    cat >&2 <<MSG
Identity-correctness violation: pattern '$line' matched in outbound content.
Edit .claude/names.txt to manage forbidden patterns.
MSG
    exit 2
  fi
done < "$NAMES_FILE"

exit 0
