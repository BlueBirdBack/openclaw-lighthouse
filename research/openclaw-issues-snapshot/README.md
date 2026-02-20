# openclaw/openclaw Issues Snapshot

Local read-only offline mirror of GitHub issues from `openclaw/openclaw`.
**No files here modify upstream GitHub.** Safe to read, grep, and analyse freely.

## Why this exists
Reviewing 10,000+ issues in a browser is slow and leaves a trace. This lets us
do offline keyword analysis and cross-reference against Lighthouse notes without
touching the upstream repo.

## How to refresh (re-run when issues are stale)

```bash
export PATH="$HOME/bin:$PATH"
BASE="$(dirname "$0")"
TS="$(date +%Y-%m-%d-%H%M%S)"
OUT="$BASE/$TS"
mkdir -p "$OUT"
export OUT

python3 - <<'PY'
import json, subprocess, os, datetime, pathlib
out = pathlib.Path(os.environ['OUT'])
repo = 'openclaw/openclaw'
all_items = []
page = 1
while True:
    cmd = ['gh','api','--method','GET',f'/repos/{repo}/issues',
           '-f','state=all','-f','per_page=100','-f',f'page={page}',
           '-f','sort=updated','-f','direction=desc']
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"gh api failed: {p.stderr}")
    data = json.loads(p.stdout)
    if not data:
        break
    for it in data:
        if 'pull_request' in it:
            continue
        all_items.append({
            'number': it.get('number'), 'title': it.get('title'),
            'state': it.get('state'), 'html_url': it.get('html_url'),
            'created_at': it.get('created_at'), 'updated_at': it.get('updated_at'),
            'closed_at': it.get('closed_at'),
            'user': (it.get('user') or {}).get('login'),
            'labels': [lb.get('name') for lb in (it.get('labels') or [])],
            'comments': it.get('comments'), 'body': it.get('body') or ''
        })
    page += 1
all_items.sort(key=lambda x: x.get('updated_at') or '', reverse=True)
open_items  = [i for i in all_items if i.get('state','').lower() == 'open']
closed_items = [i for i in all_items if i.get('state','').lower() == 'closed']
(out/'issues-all.json').write_text(json.dumps(all_items, ensure_ascii=False, indent=2), encoding='utf-8')
(out/'issues-open.json').write_text(json.dumps(open_items, ensure_ascii=False, indent=2), encoding='utf-8')
(out/'issues-closed.json').write_text(json.dumps(closed_items, ensure_ascii=False, indent=2), encoding='utf-8')
with (out/'issues-all.jsonl').open('w', encoding='utf-8') as f:
    for it in all_items:
        f.write(json.dumps(it, ensure_ascii=False)+'\n')
manifest = {
    'generated_at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
    'repo': repo,
    'issue_count_total': len(all_items),
    'issue_count_open': len(open_items),
    'issue_count_closed': len(closed_items),
    'notes': 'Read-only local snapshot. Pull requests excluded.'
}
(out/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(manifest))
PY

ln -sfn "$OUT" "$BASE/latest"
echo "Done → $OUT"
```

## Directory layout

```
openclaw-issues-snapshot/
  latest/               → symlink to most recent snapshot
  YYYY-MM-DD-HHMMSS/
    manifest.json       — counts + timestamp
    issues-all.json     — full list (JSON array)
    issues-all.jsonl    — one issue per line (good for grep/jq)
    issues-open.json    — open only
    issues-closed.json  — closed only
    related-to-media-fix.json         — keyword-scored matches for media/proxy fix
    related-to-approve-elevated-fix.json — keyword-scored matches for auth/elevated fix
    README.md           — human-readable summary + top matches
```

## Large file note
`issues-all.json`, `issues-open.json`, `issues-closed.json`, `issues-all.jsonl`
are gitignored (each 10–26 MB). `manifest.json`, `README.md`, and `related-*.json`
are committed (small).

## Useful one-liners

```bash
# Count open issues
jq length latest/issues-open.json

# Search by keyword in title (fast)
jq '.[] | select(.title | test("proxy"; "i")) | [.number, .state, .title]' latest/issues-all.json

# Full text search
grep -i "MediaFetchError" latest/issues-all.jsonl | jq '.number, .title'

# Top 20 recently updated open issues
jq '[.[] | select(.state=="open")] | sort_by(.updated_at) | reverse | .[:20] | .[] | [.number, .title]' latest/issues-all.json
```
