#!/bin/bash
# Voice-rule guard: block outgoing content containing em dashes.
# Source: context/knowledge/voice-profile.md (no em dashes).
# Matches both literal em dash and JSON-escaped —.

INPUT=$(cat)
if printf '%s' "$INPUT" | grep -qE '—|\\u2014'; then
  cat >&2 <<'MSG'
Em dash detected in outgoing content.
Voice rule (context/knowledge/voice-profile.md): no em dashes.
Replace each — with a period, comma, colon, or parenthesis, then retry the tool call.
MSG
  exit 2
fi
exit 0
