# Telegram `/approve` says unauthorized and `/elevated full` fails (beginner guide)

## Problem
In Telegram control flow, admin commands fail with errors like:
- `/approve` → unauthorized / device token mismatch
- `/elevated full` → blocked by provider gate

## What these commands mean
- `/approve`: confirms a device/session is allowed to run protected actions.
- `/elevated full`: temporarily allows high-risk shell/tool actions.

If either is broken, admin actions will be denied.

## Why this happens (plain English)
Usually it is one (or both) of these:

1. **Old/stale device token**
   - OpenClaw still trusts an old operator device token.
   - Your current Telegram session token does not match it.

2. **Elevated allowlist does not include your Telegram ID**
   - Elevated mode is enabled, but your caller ID is not allowed.

(WSL networking/proxy issues can add noise during debugging, but they are not the main auth cause.)

## Step-by-step fix

### 1) Check health first
```bash
openclaw status
openclaw gateway status
openclaw channels status --probe
```

If gateway is unhealthy:

```bash
openclaw gateway restart
```

### 2) Fix `/approve` token mismatch
List devices:

```bash
openclaw devices list
```

If you see a pending request:

```bash
openclaw devices approve <request-id>
```

If there is no pending request and token looks stale, revoke old operator device:

```bash
openclaw devices revoke --device <device-id> --role operator
openclaw gateway restart
```

Then trigger a fresh approval flow from Telegram.

### 3) Fix `/elevated full` allowlist
Check current setting:

```bash
openclaw config get tools.elevated
```

Set a minimal allowlist in `~/.openclaw/openclaw.json` (replace IDs with your own):

```json
{
  "tools": {
    "elevated": {
      "enabled": true,
      "allowFrom": {
        "telegram": ["<telegram-user-id>", "tg:<telegram-user-id>"],
        "*": ["<telegram-user-id>", "tg:<telegram-user-id>"]
      }
    }
  }
}
```

Restart gateway:

```bash
openclaw gateway restart
```

Retest in Telegram:

```text
/elevated full
```

### 4) If still blocked, ask OpenClaw which gate failed
```bash
openclaw sandbox explain --session <session-key>
```

This command shows exactly which policy gate failed and what to change.

## Security notes
- Keep allowlists narrow (only your own IDs).
- Do not leave broad elevated access on after testing.
- Redact tokens/device IDs/user IDs before sharing logs.

## Validation
- [x] approval path recovered after token cleanup
- [x] `/elevated full` available after allowlist fix + gateway restart
- [x] session gate diagnosis command provided actionable output

## Related Issues

### Closed
- [#1488](https://github.com/openclaw/openclaw/issues/1488) — `tools.elevated` behavior mismatch with approval settings
- [#531](https://github.com/openclaw/openclaw/issues/531) — per-agent elevated config scope handling
- [#2705](https://github.com/openclaw/openclaw/issues/2705) — approval resolve path (`unknown approval id`)
- [#19954](https://github.com/openclaw/openclaw/issues/19954) — device token mismatch after restart (systemd token drift)
- [#19410](https://github.com/openclaw/openclaw/issues/19410) — stale `OPENCLAW_GATEWAY_TOKEN` in service unit
- [#18274](https://github.com/openclaw/openclaw/issues/18274) — gateway 1008 unauthorized device token mismatch
- [#9028](https://github.com/openclaw/openclaw/issues/9028) — onboarding token mismatch from env/service override

## Upstream status
- [x] local deployment troubleshooting note
- [ ] upstream bug report linked
- [ ] upstream fix linked

## References
- Diagnostics: `openclaw status`, `openclaw gateway status`, `openclaw channels status --probe`
- Session gate explain: `openclaw sandbox explain --session <session-key>`

## Credits
- **B3** — reported and confirmed the fix
- **Rac** — write-up and documentation
