# `openclaw doctor --repair` not enough: reinstall via `install.sh` and restart gateway

## Problem
You run a doctor repair, but OpenClaw is still broken (for example: replies are missing, commands still fail, or behavior stays inconsistent).

Field report:

```text
openclaw doctor --fix 不管用
curl -fsSL https://openclaw.ai/install.sh | bash
修好了
```

## Why this happens
`openclaw doctor --repair` can fix many runtime/config problems, but it may not fully recover a partially broken CLI install.

In this case, reinstalling from the official `install.sh` refreshed the install and restored normal behavior.

## Step-by-step fix

### 1) Try doctor repair first

```bash
openclaw doctor --repair
```

### 2) Reinstall from the official script

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

### 3) Restart the gateway

```bash
openclaw gateway restart
```

### 4) Verify basic health

```bash
openclaw status
```

Then send one test message to confirm replies are back.

## Optional checks if it still fails
1. Confirm binary and version are sane:

```bash
which openclaw
openclaw --version
```

2. If provider setup is missing after reinstall, run:

```bash
openclaw onboard
```

3. If this is a root VPS and `systemctl --user` is unavailable, use the root-VPS gateway workaround:
- [Gateway health check fails with `1006` on root VPS (`systemctl --user` unavailable)](./gateway-1006-root-vps-systemd-user-unavailable.md)

## Validation
- [x] before fix: doctor command alone reported as ineffective (field report)
- [x] after fix: `install.sh` reinstall restored normal behavior (field report)

## Security notes
- Only use the official install URL: `https://openclaw.ai/install.sh`
- Do not run copied scripts from random mirrors.
- If you have custom local changes, back up `~/.openclaw` before major recovery work.

## Related Issues
- [OpenClaw clean uninstall and reinstall (root/Linux)](./openclaw-clean-uninstall-and-reinstall.md)
- [`openclaw uninstall` + reinstall: provider onboarding is skipped, no AI provider prompt, OpenClaw unusable](../issues/uninstall-reinstall-skips-provider-onboarding.md)

## Upstream status
- [x] local workaround documented
- [ ] issue opened upstream
- [ ] fixed upstream

## References
- X post (field report): https://x.com/BBB202622/status/2029697392812118510
- Install docs: https://docs.openclaw.ai/install

## Credits
- B3 (BlueBirdBack) — real-world report and validation
- Rac — runbook write-up
