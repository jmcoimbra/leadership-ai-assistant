# Voice Capture Sessions

> Owner: [Brain Owner] | Pillar: All | Status: Active | Last Audit: [YYYY-MM-DD]

## Purpose

Append-only log of every `voice-capture` skill run. Tracks when the brain owner reset or refined their voice profile, how much sample data fed the analysis, and which patterns were codified.

Raw writing samples are **not** stored here. They may be sensitive. Only metadata and codified outcomes are logged.

## Format

One entry per session. Newest at the top. Copy everything between the `COPY BELOW` and `COPY ABOVE` markers (not the markers themselves, and not the surrounding code fence) into the Sessions section.

```
<!-- COPY BELOW -->
## YYYY-MM-DD: [first-run / quarterly refresh / drift correction]

- **Samples analyzed:** N chat messages, N commits, N documents, N feedback notes
- **Confident patterns codified:** [count]
- **New forbidden words:** [list, or "none"]
- **New banned patterns:** [list, or "none"]
- **Rules removed from prior profile:** [list, or "none"]
- **Open questions deferred:** [list, or "none"]
- **voice-profile.md diff summary:** [one sentence]
- **names.txt updates:** [list, or "none"]
<!-- COPY ABOVE -->
```

## Sessions

<!-- Append new sessions above this line. The first run after cloning the template goes here. -->
