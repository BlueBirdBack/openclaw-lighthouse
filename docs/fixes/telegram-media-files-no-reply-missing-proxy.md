# Telegram bot replies to text but not to photos/files (beginner guide)

## Problem
Your Telegram bot answers normal text messages, but it does **not** answer when you send:
- a photo
- a file/document
- sometimes voice/audio

## Why this happens (plain English)
For media messages, OpenClaw must first **download the file from Telegram**.

In some networks, that download path is blocked or unstable unless a proxy is used.  
So text works, but media download fails — and you get no reply.

## Step-by-step fix

### 1) Add a Telegram proxy in config
Open this file:

```bash
~/.openclaw/openclaw.json
```

Add (or update) `channels.telegram.proxy`:

```json
"channels": {
  "telegram": {
    "enabled": true,
    "dmPolicy": "pairing",
    "groupPolicy": "open",
    "streamMode": "partial",
    "proxy": "http://<proxy-host>:<proxy-port>"
  }
}
```

### 2) Restart gateway
```bash
openclaw gateway restart
```

### 3) Run a quick test
1. Send a plain text message to the bot (should reply).
2. Send one image only (should reply).
3. Send image + caption (should reply).

If all 3 work, the fix is done.

## Optional checks if it still fails

### 1) Check service health
```bash
openclaw status
openclaw gateway status
openclaw channels status --probe
```

### 2) Watch logs while sending one test image
```bash
openclaw logs --follow --json --local-time --max-bytes 300000
```

Look for media download errors (for example: `MediaFetchError`, `fetch failed`, timeout).

### 3) Compare IPv4 vs IPv6 route (advanced)
```bash
curl -4sv "https://api.telegram.org/file/bot<BOT_TOKEN>/<file_path>" -o /tmp/tg-test.jpg
curl -6sv "https://api.telegram.org/file/bot<BOT_TOKEN>/<file_path>" -o /tmp/tg-test-v6.jpg
```

If one works and the other fails, your network route is likely the cause.

## Validation
- [x] reproduced before fix
- [x] fixed after proxy config + gateway restart
- [x] image-only message replied normally
- [x] image + caption replied normally

## Security note
- Never share your real bot token in screenshots/logs.
- If token was exposed, rotate it in BotFather, update config, and restart gateway.

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
- Logs: local runtime observations (media no-reply resolved after Telegram proxy/network config)

## Credits
- **B3** — reported and confirmed the fix
- **Rac** — write-up and documentation
