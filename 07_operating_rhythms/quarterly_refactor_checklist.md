# Quarterly Refactor Checklist
> Owner: [Brain Owner] | Pillar: All | Status: Enforced | Last Audit: [YYYY-MM-DD]

## Purpose

The governance doc says "quarterly refactor mandatory." This file defines exactly what that means. Without this, "quarterly refactor" is a wish.

## Schedule

| Quarter | Refactor Date | Status |
|---------|---------------|--------|
| [QX YYYY] | [YYYY-MM-DD] | Scheduled |
| [QX YYYY] | [YYYY-MM-DD] | Scheduled |
| [QX YYYY] | [YYYY-MM-DD] | Scheduled |

## Refactor Checklist

### 1. Compliance Audit (1 hour)
- [ ] Run `00_foundation/compliance_audit.md` against every file
- [ ] Score each file
- [ ] Flag RED files (score < 4/6)
- [ ] Remediate or archive RED files within 14 days

### 2. Dead Initiative Purge (30 min)
- [ ] Identify initiatives with no activity in 60+ days
- [ ] For each: either reactivate with a new deadline or archive
- [ ] No zombie initiatives allowed

### 3. Duplicate Concept Merge (30 min)
- [ ] Search for concepts defined in multiple files
- [ ] Consolidate to one source of truth
- [ ] Update all references

### 4. Metric Refresh (30 min)
- [ ] Update all `[TODO]` fields that now have real data
- [ ] Update baselines that have shifted
- [ ] Remove targets that have been achieved (replace with new targets)

### 5. Structural Review (30 min)
- [ ] Does the directory structure still make sense?
- [ ] Are any directories empty or underused?
- [ ] Do any new domains need to be added? (Follow `00_foundation/evolution_protocol.md`)

### 6. Strategic Alignment (30 min)
- [ ] Are your defined pillars still current?
- [ ] Does every active file map to a pillar?
- [ ] Have priorities shifted? Update accordingly.

## Output

After each quarterly refactor, commit the changes with message: `Quarterly refactor [YYYY-QX] — [summary of changes]`

## AI Integration

- Run `/brain-audit` before each quarterly refactor to pre-populate the remediation checklist
- AI executes Checks 1-7 (header compliance, staleness, language violations, orphaned metrics, dead initiatives, duplicate concepts, missing AI sections) autonomously
- AI proposes fixes for approval; human decides which to apply
- Post-refactor: AI verifies all RED items resolved and commits the updated files

## Escalation

If the quarterly refactor is skipped: the brain is accumulating entropy. Force a refactor within 2 weeks, even if abbreviated. Two consecutive missed refactors = the brain is no longer a reliable operating system.
