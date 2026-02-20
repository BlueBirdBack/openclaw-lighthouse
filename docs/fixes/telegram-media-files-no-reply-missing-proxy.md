# Telegram media/files got no reply (proxy/network path mismatch)

## Problem
Telegram text messages worked, but image/file messages sometimes got no assistant reply.

## Symptoms
- Text-only turns replied normally.
- Media turns were silent or intermittent.
- Gateway logs showed Telegram media download failures (for example `MediaFetchError ... fetch failed`).

## Root cause
High-confidence local root cause: Telegram media download was not consistently using a working network path in this environment.

In practice, adding a channel-level proxy fixed the inbound media path.

## Fix / workaround
Set Telegram channel proxy in `~/.openclaw/openclaw.json`.

Minimal config change:

```json
"channels": {
  "telegram": {
    "enabled": true,
    "dmPolicy": "pairing",
    "botToken": "<<hidden>>",
    "groups": { "*": { "requireMention": true } },
    "groupPolicy": "open",
    "streamMode": "partial",
    "proxy": "http://<proxy-host>:<proxy-port>"
  }
}
```

Recommended hardened variant (optional, for unstable networks):

```json
"channels": {
  "telegram": {
    "enabled": true,
    "dmPolicy": "pairing",
    "groupPolicy": "allowlist",
    "streamMode": "partial",
    "mediaMaxMb": 20,
    "timeoutSeconds": 60,
    "proxy": "http://<proxy-host>:<proxy-port>",
    "retry": {
      "attempts": 4,
      "minDelayMs": 500,
      "maxDelayMs": 5000
    },
    "network": {
      "autoSelectFamily": false
    }
  }
}
```

Then restart gateway:

```bash
openclaw gateway restart
```

## Validation
- [x] reproduced before fix
- [x] fixed after config change + gateway restart
- [x] image-only message replied normally
- [x] image + caption replied normally

## If issue returns
1. Follow live logs:
   ```bash
   openclaw logs --follow --json --local-time --max-bytes 300000
   ```
2. Send one test image and check Telegram channel log lines for media fetch errors.
3. Verify network path externally (IPv4/IPv6 behavior may differ):
   ```bash
   curl -4sv "https://api.telegram.org/file/bot<BOT_TOKEN>/<file_path>" -o /tmp/tg-test.jpg
   curl -6sv "https://api.telegram.org/file/bot<BOT_TOKEN>/<file_path>" -o /tmp/tg-test-v6.jpg
   ```
4. Re-check that the gateway process/service is actually using the expected proxy settings.

## Security note
If bot token appears in pasted commands/logs, rotate it in BotFather, update `channels.telegram.botToken`, and restart gateway.

## Related Issues

### Closed
- [#16136](https://github.com/openclaw/openclaw/issues/16136) — Telegram voice/media dropped when `getFile` failed (no retry)
- [#11471](https://github.com/openclaw/openclaw/issues/11471) — media fetch transient failure handling
- [#6849](https://github.com/openclaw/openclaw/issues/6849) — Telegram file download timeout gap
- [#4038](https://github.com/openclaw/openclaw/issues/4038) — Telegram proxy configuration reliability
- [#4989](https://github.com/openclaw/openclaw/issues/4989) — custom Telegram Bot API endpoint support (`apiRoot`)

## Upstream status
- [x] local workaround only
- [ ] issue opened upstream
- [ ] fixed upstream

## References
- Issue: n/a (local deployment incident)
- PR: n/a
- Logs: local runtime observations (Telegram media/file no-reply, resolved after proxy/network config)

## Credits
- **B3** — reported and confirmed the fix
- **Rac** — write-up and documentation
