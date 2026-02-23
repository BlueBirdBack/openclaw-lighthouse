# Gateway health check fails with `1006` on root VPS (`systemctl --user` unavailable)

## Problem
On a fresh VPS install (running as `root`), OpenClaw appears installed, but channel checks fail with:

- `Gateway not reachable`
- `gateway closed (1006 abnormal closure (no close frame))`

In many cases, status output also shows:

- `systemctl --user unavailable`
- `$DBUS_SESSION_BUS_ADDRESS and $XDG_RUNTIME_DIR not defined`

## Why this happens
There are two common causes in this setup:

1. **User systemd bus is unavailable for root session**
   - `openclaw gateway restart` relies on service manager lifecycle (`systemctl --user` on Linux user-service mode).
   - On some root VPS sessions, that bus does not exist.

2. **Mixed launch modes cause collisions**
   - Running both service mode and tmux/foreground mode on the same port causes:
   - `gateway already running`
   - `port 18789 is already in use`

## Step-by-step fix
Use **one mode only**. For root VPS environments, tmux mode is the most reliable quick path.

### Quick recovery command (root VPS, latest OpenClaw)
If gateway is flaky/unreachable after install or update, this is the fastest restart pattern:

```bash
tmux kill-session -t openclaw 2>/dev/null || true
tmux new -d -s openclaw 'openclaw gateway run --port 18789'
```

One-line form:

```bash
tmux kill-session -t openclaw 2>/dev/null || true; tmux new -d -s openclaw 'openclaw gateway run --port 18789'
```

### 1) Remove duplicate Feishu plugin copy (if present)
If you installed Feishu manually and also have bundled Feishu, remove the extra local copy:

```bash
rm -rf ~/.openclaw/extensions/feishu
```

### 2) Pin plugin allowlist
Set explicit trusted plugin ids:

```bash
openclaw config set plugins.allow '["feishu"]'
```

### 3) Stop service-mode launcher (avoid dual-run)

```bash
openclaw gateway stop 2>/dev/null || true
systemctl --user disable --now openclaw-gateway.service 2>/dev/null || true
```

### 4) Start gateway in tmux (supervisor mode)
Install tmux if needed:

```bash
command -v tmux >/dev/null || (apt-get update && apt-get install -y tmux)
```

Start OpenClaw gateway in background tmux session:

```bash
tmux kill-session -t openclaw 2>/dev/null || true
tmux new -d -s openclaw 'openclaw gateway run --port 18789'
```

### 5) Verify runtime and channel health

```bash
openclaw gateway status
openclaw channels status --probe
```

Expected:
- `RPC probe: ok`
- channel shows `enabled, configured, running`

## Optional checks if it still fails

### A) Read file logs directly (no RPC dependency)

```bash
LOG=$(ls -t /tmp/openclaw/openclaw-*.log | head -1)
tail -n 200 "$LOG"
```

### B) Check common fatal markers

```bash
LOG=$(ls -t /tmp/openclaw/openclaw-*.log | head -1)
grep -Ei 'failed before reply|all models failed|no available auth profile|rate_limit|no api key|pairing|allowlist|unauthorized|telegram|feishu' "$LOG" | tail -n 40
```

### C) tmux basics
- attach: `tmux attach -t openclaw`
- detach: `Ctrl+b`, then `d`
- list: `tmux ls`

## Validation
- [x] reproduced before fix (health check `1006`, gateway unreachable)
- [x] fixed after change (`gateway status` probe OK, channel probe OK)

## Security notes
- Keep `plugins.allow` explicit (least privilege plugin loading).
- Do not run both service mode and tmux mode on the same port.
- Keep gateway bind on loopback unless remote exposure and auth are intentionally configured.

## Related Issues
- [Feishu QuickStart install warns: `plugins.allow` is empty and non-bundled plugins may auto-load](../issues/feishu-plugin-install-plugins-allow-empty-warning.md)
- [`install.sh` + Feishu setup: duplicate plugin id warning spam and gateway health check failure](../issues/install-sh-feishu-duplicate-plugin-id-and-gateway-health-check-fail.md)
- [`openclaw update` reports ERROR after version changes, then `gateway restart` fails with `systemctl --user unavailable`](../issues/update-false-error-and-gateway-restart-systemctl-user-unavailable.md)

## Upstream status
- [x] local workaround only
- [ ] issue opened upstream
- [ ] fixed upstream

## References
- [Gateway CLI](https://docs.openclaw.ai/cli/gateway)
- [Gateway runbook](https://docs.openclaw.ai/gateway/index)
- [Plugins (Extensions)](https://docs.openclaw.ai/tools/plugin)
- [Troubleshooting](https://docs.openclaw.ai/help/troubleshooting)

## Credits
- B3 (BlueBirdBack) — field testing on real root VPS deployments
- Rac — triage and workaround write-up
