# Root VPS recovery: remove `camofox-browser` and run gateway in tmux when `systemctl --user` is unavailable

## Problem
An OpenClaw agent stayed down for a long time on a root VPS.

Observed symptoms in the same incident:
- `openclaw plugins list` showed non-bundled plugin `camofox-browser` loaded.
- `openclaw update` finished package update, but restart step failed with:
  - `Gateway service check failed: ... systemctl --user unavailable: Failed to connect to bus: No medium found`
- Gateway needed manual recovery.

## Why this happens
There are usually two separate issues combined:

1. **Non-bundled plugin risk (likely trigger in this case)**
   - `camofox-browser` is a global plugin and runs extra browser automation code.
   - If that plugin is unstable in your environment, agent reliability can drop.

2. **Root VPS service-manager mismatch**
   - `openclaw update` tries a service restart step.
   - On some root VPS sessions, `systemctl --user` bus is not available.
   - Restart step fails even when package update itself is OK.

## Step-by-step fix

### 1) Check whether `camofox-browser` is loaded
```bash
openclaw plugins list
```

If you see `camofox-browser` loaded and you do not strictly need it, remove it.

### 2) Uninstall `camofox-browser`
```bash
openclaw plugins uninstall camofox-browser --force
rm -rf ~/.openclaw/extensions/camofox-browser
```

### 3) Run update with valid syntax
Do **not** use `-yes` (unsupported in this command).

```bash
openclaw update
```

### 4) If restart fails with `systemctl --user unavailable`, switch to tmux mode
```bash
openclaw gateway stop 2>/dev/null || true
systemctl --user disable --now openclaw-gateway.service 2>/dev/null || true
tmux kill-session -t openclaw 2>/dev/null || true
tmux new -d -s openclaw 'openclaw gateway run --port 18789'
```

### 5) Verify health
```bash
openclaw gateway status
openclaw channels status --probe
openclaw plugins list
```

Expected:
- gateway probe is reachable/OK
- channel probe is running
- `camofox-browser` no longer loaded

## Optional checks if it still fails

1) Read latest gateway log:
```bash
LOG=$(ls -t /tmp/openclaw/openclaw-*.log | head -1)
tail -n 200 "$LOG"
```

2) Check tmux session exists:
```bash
tmux ls
```

3) Re-check plugin inventory for unexpected non-bundled plugins:
```bash
openclaw plugins list
```

## Validation
- [x] reproduced before fix (agent down, plugin loaded, restart error)
- [x] fixed after change (plugin removed + tmux gateway run)
- [x] update syntax corrected (`openclaw update`, not `openclaw update -yes`)

## Security notes
- Keep `plugins.allow` explicit for production servers (load only what you need).
- Treat non-bundled plugins as higher risk until proven stable in your runtime.
- Keep gateway bound to local interface unless you intentionally expose it with proper controls.

## Related Issues
- [Gateway health check fails with `1006` on root VPS (`systemctl --user` unavailable)](./gateway-1006-root-vps-systemd-user-unavailable.md)
- [`openclaw update` reports ERROR after version changes, then `gateway restart` fails with `systemctl --user unavailable`](../issues/update-false-error-and-gateway-restart-systemctl-user-unavailable.md)

## Upstream status
- [x] local workaround only
- [ ] issue opened upstream
- [ ] fixed upstream

## References
- Logs: field transcript from root VPS incident (redacted)
- [OpenClaw Gateway CLI](https://docs.openclaw.ai/cli/gateway)
- [OpenClaw Plugins](https://docs.openclaw.ai/tools/plugin)
- [Troubleshooting](https://docs.openclaw.ai/help/troubleshooting)

## Credits
- B3 (BlueBirdBack) — incident logs and recovery test
- Rac — write-up and documentation
