# Gateway reports old version after npm update

## Symptoms

After running `npm i -g openclaw@latest`, the gateway still shows the old version on restart:

```
Config was last written by a newer OpenClaw (2026.3.13); current version is 2026.3.11.
```

`openclaw --version` in the shell shows the correct new version, but the gateway process runs the old one.

## Environment
- OpenClaw version: any (observed on 2026.3.11 → 2026.3.13 upgrade)
- OS: Linux (Debian/Ubuntu)
- Install method: `npm i -g openclaw`

## Root cause

OpenClaw's systemd user service runs from `~/.openclaw/bin/openclaw` — a **local copy** of the binary, not the global `/usr/bin/openclaw`. When you update globally with `npm i -g openclaw@latest`, the global binary updates but the local copy in `~/.openclaw/bin/` stays at the old version.

The systemd unit explicitly uses:
```
ExecStart=%h/.openclaw/bin/openclaw gateway run
```

## Fix

**Option A — Copy (one-time):**
```bash
cp /usr/bin/openclaw ~/.openclaw/bin/openclaw
openclaw gateway restart
```

**Option B — Symlink (permanent, recommended):**
```bash
ln -sf /usr/bin/openclaw ~/.openclaw/bin/openclaw
openclaw gateway restart
```

The symlink ensures future `npm i -g openclaw@latest` updates automatically apply to the gateway without manual intervention.

## Notes

- This only affects setups where OpenClaw was installed globally (`npm i -g`) but the gateway runs as a non-root user with its own `~/.openclaw/bin/` copy.
- If you installed OpenClaw via the install script (`curl ... | bash`), check whether your setup uses the local or global binary.
- The "Config was last written by a newer OpenClaw" warning is harmless — the config is forward-compatible. But the version mismatch means you're not getting bugfixes from the update.

## Status
- [x] reproduced
- [x] root cause known
- [x] fix available
