#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
MODE="${1:-auto}"

export PATH="$HOME/bin:$PATH"
mkdir -p "$BASE_DIR/logs"
LOG_FILE="$BASE_DIR/logs/snapshot-$(date +%Y-%m-%d).log"

{
  echo "=== $(date -Iseconds) | mode=$MODE ==="
  python3 "$SCRIPT_DIR/snapshot_manager.py" --mode "$MODE"
  echo
} >>"$LOG_FILE" 2>&1

echo "Snapshot run complete (mode=$MODE). Log: $LOG_FILE"
