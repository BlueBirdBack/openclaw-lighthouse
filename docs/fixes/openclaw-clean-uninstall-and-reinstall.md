# OpenClaw clean uninstall and reinstall (root/Linux)

## Problem
Users run uninstall/reinstall but old state remains, then onboarding behaves unexpectedly (for example: no provider prompt, unusable install).

## Root cause
In practice, there are three different layers:
1. Global npm package (`/usr/lib/node_modules/openclaw`)
2. CLI symlink (`/usr/bin/openclaw`)
3. User state/config (`~/.openclaw`, for root this is `/root/.openclaw`)

If only layer 1 is removed, old state in layer 3 can still affect onboarding.

## Fix / workaround
Use this exact wipe + reinstall flow.

```bash
# 0) Stop gateway if running
openclaw gateway stop || true

# 1) Remove global package
npm uninstall -g openclaw

# 2) Remove symlink (if still there)
rm -f /usr/bin/openclaw

# 3) Remove global module dir (if still there)
rm -rf /usr/lib/node_modules/openclaw

# 4) Remove user state/config (critical for truly clean reinstall)
rm -rf /root/.openclaw

# 5) Verify removed
command -v openclaw || echo "openclaw binary removed"
ls -la /usr/lib/node_modules | grep openclaw || echo "module removed"
ls -la /root | grep .openclaw || echo "user state removed"

# 6) Reinstall
curl -fsSL https://openclaw.ai/install.sh | bash

# 7) Run onboarding explicitly
openclaw onboard
```

### Notes
- Replace `/root/.openclaw` with your actual home path if not running as root.
- If you need backup before wiping state:

```bash
cp -a /root/.openclaw /root/.openclaw.bak.$(date +%F-%H%M%S)
```

## Validation
- [x] reproduced before fix
- [x] fixed after change

Validation checklist:
- `command -v openclaw` returns `/usr/bin/openclaw` after reinstall
- `openclaw status` works
- `openclaw onboard` shows provider setup flow or confirms configured provider

## Upstream status
- [x] local workaround only
- [ ] issue opened upstream
- [ ] fixed upstream

## References
- Uninstall docs: https://docs.openclaw.ai/cli/uninstall#uninstall
- Install docs: https://docs.openclaw.ai/install
- Related issue note: ../issues/uninstall-reinstall-skips-provider-onboarding.md
