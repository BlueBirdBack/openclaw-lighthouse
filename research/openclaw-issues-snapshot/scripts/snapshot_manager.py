#!/usr/bin/env python3
"""Manage offline snapshots for openclaw/openclaw issues.

Modes:
- full : fetch all issues (open + closed)
- delta: fetch only issues updated since --since or last state run
- auto : run weekly full; otherwise daily delta

This is a read-only mirror workflow. It never writes to upstream GitHub.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Iterable, List

MEDIA_KEYWORDS = [
    "telegram",
    "media",
    "fetch",
    "proxy",
    "file download",
    "typeerror: fetch failed",
    "ssrf",
]

AUTH_KEYWORDS = [
    "device token mismatch",
    "approve",
    "approval",
    "elevated",
    "allowfrom",
    "pairing required",
    "provider gate",
]


@dataclass
class SnapshotResult:
    mode: str
    output_dir: Path
    issue_count_total: int
    issue_count_open: int
    issue_count_closed: int
    generated_at: str


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_utc(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def parse_iso(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value).astimezone(timezone.utc)


def run_cmd(cmd: List[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())
    return proc.stdout


def gh_api_issues(repo: str, params: Dict[str, str]) -> List[dict]:
    cmd = ["gh", "api", "--method", "GET", f"/repos/{repo}/issues"]
    for k, v in params.items():
        cmd.extend(["-f", f"{k}={v}"])
    out = run_cmd(cmd)
    return json.loads(out)


def normalize_issue(it: dict) -> dict:
    return {
        "number": it.get("number"),
        "title": it.get("title"),
        "state": (it.get("state") or "").lower(),
        "html_url": it.get("html_url"),
        "created_at": it.get("created_at"),
        "updated_at": it.get("updated_at"),
        "closed_at": it.get("closed_at"),
        "user": (it.get("user") or {}).get("login"),
        "labels": [lb.get("name") for lb in (it.get("labels") or [])],
        "assignees": [a.get("login") for a in (it.get("assignees") or [])],
        "comments": it.get("comments"),
        "milestone": ((it.get("milestone") or {}).get("title") if it.get("milestone") else None),
        "body": it.get("body") or "",
    }


def fetch_issues(repo: str, since: str | None = None) -> List[dict]:
    page = 1
    items: List[dict] = []
    while True:
        params: Dict[str, str] = {
            "state": "all",
            "per_page": "100",
            "page": str(page),
            "sort": "updated",
            "direction": "desc",
        }
        if since:
            params["since"] = since
        data = gh_api_issues(repo, params)
        if not data:
            break
        for it in data:
            if "pull_request" in it:
                continue
            items.append(normalize_issue(it))
        page += 1
    items.sort(key=lambda x: x.get("updated_at") or "", reverse=True)
    return items


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_jsonl(path: Path, items: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")


def keyword_matches(items: Iterable[dict], keywords: List[str], min_score: int = 2) -> List[dict]:
    out: List[dict] = []
    for it in items:
        text = f"{it.get('title','')}\n{it.get('body','')}".lower()
        hits = [kw for kw in keywords if kw in text]
        if len(hits) >= min_score:
            out.append(
                {
                    "number": it["number"],
                    "state": it["state"],
                    "title": it["title"],
                    "html_url": it["html_url"],
                    "score": len(hits),
                    "hits": hits,
                    "updated_at": it.get("updated_at"),
                }
            )
    out.sort(key=lambda x: (x["score"], x.get("updated_at") or ""), reverse=True)
    return out


def load_state(path: Path) -> dict:
    if not path.exists():
        return {
            "repo": "",
            "last_run_at": None,
            "last_full_at": None,
            "last_delta_at": None,
            "issue_state": {},
        }
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write_json(path, state)


def apply_state_updates(state: dict, items: Iterable[dict]) -> None:
    store = state.setdefault("issue_state", {})
    for it in items:
        store[str(it["number"])] = {
            "state": it["state"],
            "updated_at": it.get("updated_at"),
            "title": it.get("title"),
            "html_url": it.get("html_url"),
        }


def clean_old_snapshots(kind_dir: Path, keep: int) -> None:
    kind_dir.mkdir(parents=True, exist_ok=True)
    dirs = sorted([p for p in kind_dir.iterdir() if p.is_dir()])
    if len(dirs) <= keep:
        return
    for d in dirs[: len(dirs) - keep]:
        shutil.rmtree(d, ignore_errors=True)


def update_symlink(link_path: Path, target: Path) -> None:
    link_path.parent.mkdir(parents=True, exist_ok=True)
    if link_path.is_symlink() or link_path.exists():
        link_path.unlink()
    # relative link for repo portability
    rel = os.path.relpath(target, link_path.parent)
    link_path.symlink_to(rel)


def write_full_readme(output_dir: Path, manifest: dict, items: List[dict], media_related: List[dict], auth_related: List[dict]) -> None:
    lines: List[str] = []
    lines.append(f"# OpenClaw Issues Full Snapshot — {manifest['generated_at']}")
    lines.append("")
    lines.append(f"Repo: `{manifest['repo']}`")
    lines.append(f"Total issues (no PRs): **{manifest['issue_count_total']}**")
    lines.append(f"- Open: **{manifest['issue_count_open']}**")
    lines.append(f"- Closed: **{manifest['issue_count_closed']}**")
    lines.append("")
    lines.append("This is a local read-only snapshot for offline review. It does not modify upstream GitHub issues.")
    lines.append("")
    lines.append("## Recently updated issues (top 20)")
    for it in items[:20]:
        lines.append(f"- #{it['number']} [{it['state']}] {it['title']} — {it['html_url']}")
    lines.append("")
    lines.append("## Related candidates: Telegram media/proxy fix (top 15)")
    for it in media_related[:15]:
        lines.append(f"- #{it['number']} [{it['state']}] score={it['score']} — {it['title']} — {it['html_url']}")
    lines.append("")
    lines.append("## Related candidates: approve/elevated/token-mismatch fix (top 15)")
    for it in auth_related[:15]:
        lines.append(f"- #{it['number']} [{it['state']}] score={it['score']} — {it['title']} — {it['html_url']}")
    output_dir.joinpath("README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_delta_readme(output_dir: Path, manifest: dict, categories: dict, media_related: List[dict], auth_related: List[dict]) -> None:
    lines: List[str] = []
    lines.append(f"# OpenClaw Issues Delta Snapshot — {manifest['generated_at']}")
    lines.append("")
    lines.append(f"Repo: `{manifest['repo']}`")
    lines.append(f"Since: `{manifest['since']}`")
    lines.append(f"Updated issues fetched: **{manifest['issue_count_total']}**")
    lines.append(f"- Open now: **{manifest['issue_count_open']}**")
    lines.append(f"- Closed now: **{manifest['issue_count_closed']}**")
    lines.append("")
    lines.append("## Change categories")
    lines.append(f"- new_opened: **{len(categories['new_opened'])}**")
    lines.append(f"- new_closed: **{len(categories['new_closed'])}**")
    lines.append(f"- newly_closed: **{len(categories['newly_closed'])}**")
    lines.append(f"- reopened: **{len(categories['reopened'])}**")
    lines.append(f"- still_open_updated: **{len(categories['still_open_updated'])}**")
    lines.append(f"- still_closed_updated: **{len(categories['still_closed_updated'])}**")
    lines.append("")
    lines.append("## Newly closed (top 20)")
    for it in categories["newly_closed"][:20]:
        lines.append(f"- #{it['number']} {it['title']} — {it['html_url']}")
    lines.append("")
    lines.append("## Reopened (top 20)")
    for it in categories["reopened"][:20]:
        lines.append(f"- #{it['number']} {it['title']} — {it['html_url']}")
    lines.append("")
    lines.append("## Related candidates: Telegram media/proxy fix (top 10)")
    for it in media_related[:10]:
        lines.append(f"- #{it['number']} [{it['state']}] score={it['score']} — {it['title']} — {it['html_url']}")
    lines.append("")
    lines.append("## Related candidates: approve/elevated/token-mismatch fix (top 10)")
    for it in auth_related[:10]:
        lines.append(f"- #{it['number']} [{it['state']}] score={it['score']} — {it['title']} — {it['html_url']}")
    output_dir.joinpath("README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_full(base: Path, repo: str, keep_full: int, state: dict) -> SnapshotResult:
    ts = utc_now().strftime("%Y-%m-%d-%H%M%S")
    output_dir = base / "full" / ts
    output_dir.mkdir(parents=True, exist_ok=True)

    items = fetch_issues(repo)
    open_items = [i for i in items if i["state"] == "open"]
    closed_items = [i for i in items if i["state"] == "closed"]

    write_json(output_dir / "issues-all.json", items)
    write_json(output_dir / "issues-open.json", open_items)
    write_json(output_dir / "issues-closed.json", closed_items)
    write_jsonl(output_dir / "issues-all.jsonl", items)

    media_related = keyword_matches(items, MEDIA_KEYWORDS)
    auth_related = keyword_matches(items, AUTH_KEYWORDS)
    write_json(output_dir / "related-to-media-fix.json", media_related)
    write_json(output_dir / "related-to-approve-elevated-fix.json", auth_related)

    generated_at = iso_utc(utc_now())
    manifest = {
        "generated_at": generated_at,
        "mode": "full",
        "repo": repo,
        "issue_count_total": len(items),
        "issue_count_open": len(open_items),
        "issue_count_closed": len(closed_items),
        "notes": "Read-only local full snapshot. Pull requests excluded.",
    }
    write_json(output_dir / "manifest.json", manifest)
    write_full_readme(output_dir, manifest, items, media_related, auth_related)

    apply_state_updates(state, items)
    state["repo"] = repo
    state["last_run_at"] = generated_at
    state["last_full_at"] = generated_at

    update_symlink(base / "latest-full", output_dir)
    update_symlink(base / "latest", output_dir)
    clean_old_snapshots(base / "full", keep_full)

    return SnapshotResult(
        mode="full",
        output_dir=output_dir,
        issue_count_total=len(items),
        issue_count_open=len(open_items),
        issue_count_closed=len(closed_items),
        generated_at=generated_at,
    )


def run_delta(base: Path, repo: str, since: str, keep_delta: int, state: dict) -> SnapshotResult:
    ts = utc_now().strftime("%Y-%m-%d-%H%M%S")
    output_dir = base / "delta" / ts
    output_dir.mkdir(parents=True, exist_ok=True)

    items = fetch_issues(repo, since=since)
    open_items = [i for i in items if i["state"] == "open"]
    closed_items = [i for i in items if i["state"] == "closed"]

    prev_map = dict(state.get("issue_state", {}))
    categories = {
        "new_opened": [],
        "new_closed": [],
        "newly_closed": [],
        "reopened": [],
        "still_open_updated": [],
        "still_closed_updated": [],
    }

    for it in items:
        num = str(it["number"])
        prev = prev_map.get(num)
        cur_state = it["state"]
        if not prev:
            if cur_state == "open":
                categories["new_opened"].append(it)
            else:
                categories["new_closed"].append(it)
            continue

        prev_state = (prev.get("state") or "").lower()
        if prev_state == "open" and cur_state == "closed":
            categories["newly_closed"].append(it)
        elif prev_state == "closed" and cur_state == "open":
            categories["reopened"].append(it)
        elif cur_state == "open":
            categories["still_open_updated"].append(it)
        else:
            categories["still_closed_updated"].append(it)

    write_json(output_dir / "issues-updated.json", items)
    write_json(output_dir / "issues-open-now.json", open_items)
    write_json(output_dir / "issues-closed-now.json", closed_items)
    write_jsonl(output_dir / "issues-updated.jsonl", items)

    for name, rows in categories.items():
        write_json(output_dir / f"{name}.json", rows)

    media_related = keyword_matches(items, MEDIA_KEYWORDS)
    auth_related = keyword_matches(items, AUTH_KEYWORDS)
    write_json(output_dir / "related-to-media-fix.json", media_related)
    write_json(output_dir / "related-to-approve-elevated-fix.json", auth_related)

    generated_at = iso_utc(utc_now())
    manifest = {
        "generated_at": generated_at,
        "mode": "delta",
        "repo": repo,
        "since": since,
        "issue_count_total": len(items),
        "issue_count_open": len(open_items),
        "issue_count_closed": len(closed_items),
        "notes": "Read-only local delta snapshot. Pull requests excluded.",
    }
    write_json(output_dir / "manifest.json", manifest)
    write_delta_readme(output_dir, manifest, categories, media_related, auth_related)

    apply_state_updates(state, items)
    state["repo"] = repo
    state["last_run_at"] = generated_at
    state["last_delta_at"] = generated_at

    update_symlink(base / "latest-delta", output_dir)
    clean_old_snapshots(base / "delta", keep_delta)

    return SnapshotResult(
        mode="delta",
        output_dir=output_dir,
        issue_count_total=len(items),
        issue_count_open=len(open_items),
        issue_count_closed=len(closed_items),
        generated_at=generated_at,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="OpenClaw issues snapshot manager")
    parser.add_argument("--mode", choices=["full", "delta", "auto"], default="auto")
    parser.add_argument("--repo", default="openclaw/openclaw")
    parser.add_argument("--base-dir", default=None, help="Snapshot base dir (default: parent dir of this script)")
    parser.add_argument("--since", default=None, help="ISO8601 time for delta mode (e.g. 2026-02-20T00:00:00Z)")
    parser.add_argument("--weekly-full-days", type=int, default=7)
    parser.add_argument("--keep-full", type=int, default=8)
    parser.add_argument("--keep-delta", type=int, default=30)
    args = parser.parse_args()

    base = Path(args.base_dir).expanduser().resolve() if args.base_dir else Path(__file__).resolve().parent.parent
    state_file = base / "state" / "snapshot-state.json"
    state = load_state(state_file)

    try:
        if args.mode == "full":
            result = run_full(base, args.repo, args.keep_full, state)
        elif args.mode == "delta":
            since = args.since or state.get("last_run_at")
            if not since:
                print("No previous state found for delta; running full snapshot instead.")
                result = run_full(base, args.repo, args.keep_full, state)
            else:
                result = run_delta(base, args.repo, since, args.keep_delta, state)
        else:  # auto
            last_full_at = state.get("last_full_at")
            if not last_full_at:
                result = run_full(base, args.repo, args.keep_full, state)
            else:
                age = utc_now() - parse_iso(last_full_at)
                if age >= timedelta(days=args.weekly_full_days):
                    result = run_full(base, args.repo, args.keep_full, state)
                else:
                    since = state.get("last_run_at") or args.since
                    if not since:
                        result = run_full(base, args.repo, args.keep_full, state)
                    else:
                        result = run_delta(base, args.repo, since, args.keep_delta, state)

        save_state(state_file, state)
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    summary = {
        "mode": result.mode,
        "output_dir": str(result.output_dir),
        "generated_at": result.generated_at,
        "issue_count_total": result.issue_count_total,
        "issue_count_open": result.issue_count_open,
        "issue_count_closed": result.issue_count_closed,
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
