# openclaw/openclaw Issues Snapshot

Local **read-only** offline mirror of GitHub issues from `openclaw/openclaw`.
It is for analysis only — no upstream issue is modified by these scripts.

## Why this exists
- Reviewing 10K+ issues in browser is slow and noisy.
- We want diff-friendly history of issue changes.
- We want to map upstream issues to Lighthouse fix notes without posting anything yet.

## Automation strategy
- **Weekly full snapshot** (baseline)
- **Daily delta snapshot** (what changed since last run)

Use **auto mode** to get both with one cron job.

## Scripts
- `scripts/snapshot_manager.py`
  - `--mode full`  → fetch all issues (open + closed)
  - `--mode delta` → fetch issues updated since last run (or `--since`)
  - `--mode auto`  → weekly full, otherwise daily delta
- `scripts/run_snapshot.sh` (cron-friendly wrapper with logging)
- `cron.example` (ready-to-copy crontab lines)

## Quick start

```bash
cd /home/box/.openclaw/workspace/openclaw-lighthouse/research/openclaw-issues-snapshot

# one-off baseline
./scripts/run_snapshot.sh full

# normal daily operation
./scripts/run_snapshot.sh auto
```

## Cron setup

```bash
crontab -e
```

Then add:

```cron
15 2 * * * /home/box/.openclaw/workspace/openclaw-lighthouse/research/openclaw-issues-snapshot/scripts/run_snapshot.sh auto
```

This single line is enough:
- first run (or stale baseline) → full snapshot
- normal days → delta snapshot

See `cron.example` for optional explicit weekly full job.

## Directory layout

```text
openclaw-issues-snapshot/
  full/
    YYYY-MM-DD-HHMMSS/
      manifest.json
      issues-all.json
      issues-open.json
      issues-closed.json
      issues-all.jsonl
      related-to-media-fix.json
      related-to-approve-elevated-fix.json
      README.md
  delta/
    YYYY-MM-DD-HHMMSS/
      manifest.json
      issues-updated.json
      issues-open-now.json
      issues-closed-now.json
      issues-updated.jsonl
      new_opened.json
      new_closed.json
      newly_closed.json
      reopened.json
      still_open_updated.json
      still_closed_updated.json
      related-to-media-fix.json
      related-to-approve-elevated-fix.json
      README.md
  latest-full      -> symlink to newest full snapshot
  latest-delta     -> symlink to newest delta snapshot
  latest           -> symlink to newest full snapshot (compat)
  state/
    snapshot-state.json   # local state cache for delta classification
  logs/
    snapshot-YYYY-MM-DD.log
```

## Retention defaults
- Keep **8 full snapshots**
- Keep **30 delta snapshots**

Override with script flags:

```bash
python3 ./scripts/snapshot_manager.py --mode auto --keep-full 12 --keep-delta 45
```

## Large file note
Huge files are gitignored:
- `issues-all.json`
- `issues-open.json`
- `issues-closed.json`
- `issues-all.jsonl`

Committed files stay lightweight:
- `manifest.json`
- per-run `README.md`
- `related-to-*.json`
- this automation README/scripts

## Useful one-liners

```bash
# Count currently open issues from latest full
jq length latest-full/issues-open.json

# Search latest full by keyword
jq '.[] | select(.title | test("proxy"; "i")) | [.number, .state, .title]' latest-full/issues-all.json

# Show newly closed issues from latest delta
jq '.[] | [.number, .title]' latest-delta/newly_closed.json

# Show reopened issues from latest delta
jq '.[] | [.number, .title]' latest-delta/reopened.json
```
