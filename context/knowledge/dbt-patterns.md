# dbt Patterns

**Added:** 2026-03-11
**Last Updated:** 2026-03-16
**Source:** PR #750 CI debugging session ([your-org]-dbt)

## CI Pipeline (`state:modified`)

[your-org]-dbt CI uses `dbt run --select state:modified+1 --defer` then `dbt test --select state:modified+ --defer`. Master manifest stored in S3.

### Branch Drift = False Modifications

When branch is behind master, CI compares against old manifest. Every divergent file appears as "modified", building/testing unrelated models.

**Fix:** Rebase onto `origin/master` before pushing. After rebase: `git push --force-with-lease`.

**Detection:** If CI builds dozens of unexpected models, check `git log origin/master..HEAD --oneline | wc -l` vs expected commit count.

### Seed Cascade

A modified seed cascades through ALL downstream models via `state:modified+`:

```
seed_jira_custom_field_options
  → stg_jira__custom_field_options
    → int_jira__bugs_metrics
      → bugs_stability, bugs_velocity_daily, bugs_resolver_stats, bugs_custom_fields
```

One row added to a seed can trigger pre-existing test failures on unrelated models (deferred columns missing from master table).

**Mitigation:** Only modify seeds when the downstream models actually need the change. If a seed change is cosmetic or unused by current PR models, revert it: `git checkout origin/master -- seeds/<file>.csv`.

### Debugging CI Without Direct Log Access

CircleCI SPA renders logs client-side. WebFetch returns empty HTML.

**Workaround:** Use CircleCI v1.1 API:
1. Get job details: `GET /api/v1.1/project/github/{org}/{repo}/{job_number}`
2. Response includes `steps[]` with `actions[].status` and `actions[].output_url` (presigned S3 URL)
3. Fetch presigned URL directly for raw log content

## Incremental Models with Multi-Source Joins

### GREATEST() + COALESCE() Pattern

When an incremental model joins multiple Fivetran-synced sources, track freshness across all:

```sql
GREATEST(
  COALESCE(issues._fivetran_synced, '1970-01-01'),
  COALESCE(labels._fivetran_synced, '1970-01-01'),
  COALESCE(history._fivetran_synced, '1970-01-01')
) AS _fivetran_synced_at
```

COALESCE prevents NULL from poisoning GREATEST (NULL wins in Snowflake GREATEST).

### Incremental Filter Placement

Apply `is_incremental()` filter on the CTE that reads from the largest/most frequently updated source. Don't filter every CTE — the join naturally limits rows.

## Dynamic Table vs Incremental Decision

| Factor | Dynamic Table | Incremental |
|--------|--------------|-------------|
| Refresh control | Snowflake automatic | dbt-managed |
| Cost | Snowflake compute (always-on) | Only on dbt run |
| Complexity | Simpler SQL (no is_incremental) | Requires merge logic |
| Use when | Low-latency freshness needed | Batch is acceptable |
| Avoid when | Large tables with expensive transforms | Need real-time |

[your-org]-dbt uses incremental for all engineering mart models (`qa_stability`, `bugs_stability`, `bugs_velocity_daily`).

## Long-Lived Branch Rebase

Branches with many iterative commits (10+) that overlap with master merges will conflict heavily on rebase. Clean approach:

1. `git diff master...branch -- <your files>` to capture the actual delta
2. Abort rebase, switch to master, create fresh branch
3. Apply only the final-state changes
4. Force push with `--force-with-lease` to update the PR

Source: PR #829 [your-org]-dbt (2026-03-16). 18 commits, 4 conflict files. Fresh branch took 30 seconds.
