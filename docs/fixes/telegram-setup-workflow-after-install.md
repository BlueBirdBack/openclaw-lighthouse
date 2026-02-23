# Telegram setup workflow after installing OpenClaw (with root VPS notes)

## Problem
After a fresh OpenClaw install, Telegram setup may fail or behave inconsistently:

- `Unknown channel: telegram`
- no pairing code appears (`requests: []`)
- bot does not reply after token setup

On root VPS hosts, this often combines with gateway lifecycle issues.

## Why this happens
Most failures come from one of these:

1. Telegram plugin is not effectively enabled (or blocked by `plugins.allow`).
2. Gateway was not restarted after config/plugin changes.
3. Channel token was added before plugin/channel runtime was active.
4. Pairing flow was expected, but no pending request existed yet.
5. On root VPS, `systemctl --user` may be unavailable, so service-mode restart fails.

## Step-by-step fix
Follow this exact order.

### 1) Ensure Telegram plugin is allowed and enabled
If you use plugin allowlist, include `telegram`.

```bash
openclaw config set plugins.allow '["telegram"]'
openclaw config set plugins.entries.telegram.enabled true
```

If you also use Feishu on the same host, allow both:

```bash
openclaw config set plugins.allow '["feishu","telegram"]'
```

### 2) Start gateway with the correct mode for your host

#### Root VPS / no working `systemctl --user` (recommended)

```bash
tmux kill-session -t openclaw 2>/dev/null || true
tmux new -d -s openclaw 'openclaw gateway run --port 18789'
```

#### Standard user-service mode (when systemd user bus works)

```bash
openclaw gateway install --force
systemctl --user enable --now openclaw-gateway.service
```

### 3) Add Telegram bot token

```bash
openclaw channels add --channel telegram --token "<BOTFATHER_TOKEN>"
```

### 4) Verify channel runtime

```bash
openclaw gateway status
openclaw channels status --probe
```

Expected Telegram state: `enabled, configured, running`.

### 5) Pairing flow (if DM policy is pairing)
Set pairing policy (safe default):

```bash
openclaw config set channels.telegram.dmPolicy pairing
```

Now send one DM to the bot from Telegram, then check pending requests:

```bash
openclaw pairing list telegram --json
```

Approve code:

```bash
openclaw pairing approve telegram <CODE> --notify
```

## Optional checks if it still fails

### A) `Unknown channel: telegram`
Usually means telegram plugin runtime not active yet.

Check:

```bash
openclaw plugins list | grep -i telegram
openclaw config get plugins.allow
openclaw config get plugins.entries.telegram.enabled
```

### B) `requests: []` and no pairing code
Possible reasons:
- no new DM reached the bot yet
- sender already approved
- Telegram channel not actually running

Check:

```bash
openclaw channels status --probe
cat ~/.openclaw/credentials/telegram-allowFrom.json 2>/dev/null || echo "no approved senders file"
```

### C) Gateway unreachable (`1006`)
Use root VPS quick recovery command:

```bash
tmux kill-session -t openclaw 2>/dev/null || true
tmux new -d -s openclaw 'openclaw gateway run --port 18789'
```

## Validation
- [x] reproduced before fix (channel add/pairing confusion on fresh VPS install)
- [x] fixed after change (Telegram running + pairing code received + successful chat)

## Security notes
- If a bot token was pasted in logs/chat, rotate it in BotFather immediately.
- Keep `plugins.allow` explicit for least-privilege plugin loading.
- Do not run service mode and tmux mode at the same time on the same port.

## Related Issues
- [Gateway health check fails with `1006` on root VPS (`systemctl --user` unavailable)](./gateway-1006-root-vps-systemd-user-unavailable.md)
- [`install.sh` + Feishu setup: duplicate plugin id warning spam and gateway health check failure](../issues/install-sh-feishu-duplicate-plugin-id-and-gateway-health-check-fail.md)
- [Feishu QuickStart install warns: `plugins.allow` is empty and non-bundled plugins may auto-load](../issues/feishu-plugin-install-plugins-allow-empty-warning.md)

## Upstream status
- [x] local workflow/workaround documented
- [ ] issue opened upstream
- [ ] fixed upstream

## References
- [Telegram channel docs](https://docs.openclaw.ai/channels/telegram)
- [Pairing docs](https://docs.openclaw.ai/channels/pairing)
- [Gateway CLI](https://docs.openclaw.ai/cli/gateway)
- [Troubleshooting](https://docs.openclaw.ai/help/troubleshooting)

## Credits
- B3 (BlueBirdBack) — real VPS validation and edge-case discovery
- Rac — workflow hardening + documentation
