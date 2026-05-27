#!/bin/bash
# Voice-rule guard: block bare "Pillar N" references in outbound content.
#
# Rule for outbound: name the substantive concept directly. Drop "Pillar N" entirely.
# Internal brain files are exempt; this hook only fires on outbound MCP matchers.
#
# Customize: replace the canonical-names list below with your own pillar names.

INPUT=$(cat)

if printf '%s' "$INPUT" | grep -qE '\bPillar [1-9]\b'; then
  cat >&2 <<'MSG'
Pillar-naming violation: bare "Pillar N" detected in outbound content.
Voice rule: in outbound content, name the substantive concept, not the pillar number.

Customize this hook with your canonical pillar names. Example:
- Pillar 1 = [Your Pillar 1 Name]
- Pillar 2 = [Your Pillar 2 Name]
- Pillar 3 = [Your Pillar 3 Name]

Rewrite the offending sentence to name the concept directly, then retry the tool call.
MSG
  exit 2
fi

exit 0
