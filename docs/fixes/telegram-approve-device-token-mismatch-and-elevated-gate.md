# Telegram `/approve` unauthorized + `/elevated full` blocked (WSL troubleshooting)

## Problem
In Telegram control flow, elevated/approval actions failed intermittently in WSL environments.

## Symptoms
- `Exec denied ... approval-request-failed`
- `/approve` returned unauthorized/device-token mismatch
- `/elevated full` reported provider gate failure

## Root cause
This was a compound local setup issue:

1. **Stale operator device token** caused approval mismatch.
2. **Elevated allowlist gating** did not match the active Telegram caller/session.
3. In some setups, network/proxy path confusion can make debugging noisy, so health checks are needed first.

## Fix / workaround

### 1) Quick health check
```bash
openclaw status
openclaw gateway status
openclaw channels status --probe
```

If gateway is unhealthy:

```bash
openclaw gateway restart
```

### 2) Repair `/approve` token mismatch
```bash
openclaw devices list
```

- If a pending request exists:

```bash
openclaw devices approve <request-id>
```

- If no pending request and operator token is stale:

```bash
openclaw devices revoke --device <device-id> --role operator
openclaw gateway restart
```

Then trigger a fresh approval flow from Telegram.

### 3) Repair `/elevated full` provider gate
Check current policy:

```bash
openclaw config get tools.elevated
```

Use a scoped allowlist in `~/.openclaw/openclaw.json` (sanitize with your own IDs):

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

Then retest in Telegram:

```text
/elevated full
```

### 4) Explain blocked session gates directly
```bash
openclaw sandbox explain --session <session-key>
```

This prints failing gates and fix keys for that session.

### 5) Optional effort-level validation after repair
Use your own local CLIs to sanity-check effort modes (Codex/Claude) if required by your workflow.

### 6) WSL proxy/network note
- WSL networking mode can change whether proxy is reachable via host-IP or localhost.
- This affects media/network behavior, separate from DM authorization policy.

## Validation
- [x] approval path recovered after token/gate cleanup
- [x] `/elevated full` available after allowlist fix + gateway restart
- [x] session gate diagnosis command provided actionable output

## Security note
- Keep IDs in config minimal and explicit.
- Revert broad elevated testing modes after debugging (for example `/elevated ask` or `/elevated off`).
- Redact tokens, user IDs, and device IDs in any shared logs/docs.

## Related upstream issues (closed)
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
- Related diagnostics: `openclaw status`, `openclaw gateway status`, `openclaw channels status --probe`
- Session gate explain: `openclaw sandbox explain --session <session-key>`
