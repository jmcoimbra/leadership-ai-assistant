---
name: voice-capture
description: Extract the brain owner's voice from sample writing and codify it into context/knowledge/voice-profile.md. Auto-triggers when the user pastes samples of their own writing, says "capture my voice", "extract my voice", "build my voice profile", or when first adopting this template.
user_invocable: true
---

# Voice Capture

## When to Run

- **First adoption.** A new owner forks this template and the default voice-profile.md does not match how they actually write.
- **Voice drift.** The owner notices their AI drafts sound off compared to their real writing.
- **New rule observed.** The owner corrected the AI on the same pattern 2+ times and the rule is not yet in `voice-profile.md`.

## Inputs Required

Before running, ask the user to gather and paste:

1. **10-20 chat / Slack messages** they wrote (pre-AI if possible — the goal is to capture THEIR voice, not the AI's prior drafts).
2. **5+ commit messages** they wrote.
3. **2-3 documents** they wrote (status update, RFC, design doc, performance review note).
4. **1-2 feedback notes** they gave to a report.
5. **Any explicit voice rules** they already know they want enforced ("I never use em dashes", "I always use Brazilian Portuguese accents", etc.).

If samples are missing, say so explicitly. Do not infer voice from too little data — partial capture is worse than no capture because it codifies noise as signal.

## Analysis Dimensions

For each sample, extract:

| Dimension | What to Measure |
|-----------|-----------------|
| Greeting style | "Hi" / "Hey" / "Hello" / none. Frequency per dimension. |
| Closing style | "Thanks" / "Cheers" / explicit commitment / none. |
| Sentence length | Average words per sentence. Min, max, median. |
| Em dash usage | Count of `—` and `--`. Voluntary or accidental? |
| Semicolon usage | Count and context (chat vs document). |
| Contractions | `I'm` vs `I am`, `don't` vs `do not`, frequency. |
| Hedge words | Count of `maybe`, `perhaps`, `just`, `actually`, `kind of`, `sort of`. |
| Vague quantifiers | Count of `often`, `usually`, `rarely`, `sometimes`. |
| Vocabulary signatures | Any word the owner uses 3+ times across samples (their "tells"). |
| Forbidden words | Words conspicuously absent that an average corporate writer would use. |
| Code-switching | Mixed-language writing? Which languages, in which contexts? |
| Punctuation density | Heavy use of `()`, `:`, `—`, `?` |
| Sentence ordering | Assertion-first or context-first? |
| Voice (active / passive) | Ratio. |
| Filler patterns | "Just wanted to flag", "FYI", "circling back", "wanted to share". |
| Praise style | Specific behavior named, or generic ("great job")? |

## Output Format

After analysis, produce a structured findings report:

```
=== Voice Capture Findings ===

CONFIDENT PATTERNS (3+ samples agree):
- [Pattern with example]
- [Pattern with example]

EMERGING PATTERNS (2 samples agree, needs more data):
- [Pattern]

EXPLICIT RULES (user-stated):
- [Rule]

CANDIDATE FORBIDDEN WORDS:
- [Word]: appears 0 times across N samples; standard corporate baseline: M
- [Word]: ...

CANDIDATE BANNED PATTERNS:
- [Pattern]: never used in samples

QUESTIONS FOR THE OWNER:
- [Pattern X appeared inconsistently — codify or skip?]
- [Pattern Y could go either way — preference?]
```

## Codification

After the owner confirms which findings to codify:

1. **Update `context/knowledge/voice-profile.md`** in place. Preserve the existing section structure (Greetings, Sentence Structure, Deterministic Language, Anti-Patterns, etc.). Replace the example text with patterns confirmed for THIS owner.
2. **Update `.claude/names.txt`** with any name misspellings or banned tool names the owner identified.
3. **Update `.claude/hooks/check-pillar.sh`** if the owner uses different pillar names (or wants the hook disabled).
4. **Append a session log** to `99_archive/voice_capture_sessions.md` following the format defined in that file. Required fields: date and session type, samples analyzed (counts per source), confident patterns codified, new forbidden words, new banned patterns, rules removed from prior profile, open questions deferred, voice-profile.md diff summary, names.txt updates. Do not store the raw samples. They may be sensitive.

## Anti-Patterns

- **Do not codify a pattern that appears only once.** One instance is noise.
- **Do not assume the owner wants the template's defaults.** Ask before keeping any rule that did not emerge from samples.
- **Do not infer language preferences from a single language sample** if the owner mentioned working in multiple languages.
- **Do not codify rules the owner cannot articulate WHY they hold.** A rule without a reason will break the first time it conflicts with another rule.

## AI Integration

This skill IS the AI integration. The agent runs the pattern extraction; the owner decides which patterns to enforce. The agent never silently changes voice rules based on inferred patterns — every codification must be explicitly confirmed by the owner.

## First-Run Walkthrough (Adoption Mode)

When the brain owner runs this skill for the first time after cloning the template:

1. Greet them. State the goal: replace the generic voice profile with theirs.
2. Walk through the inputs list. Wait for them to gather samples.
3. When samples arrive, run the analysis and surface findings.
4. Ask which patterns to codify. Take each one in turn.
5. Apply codifications. Show the diff against the template's voice-profile.md.
6. Commit (per the brain's commit rules).
7. Suggest re-running this skill quarterly or whenever they catch the AI sounding off.
