# Telegram media/files got no reply (missing proxy in channel config)

## Problem
In Telegram DM, image/file messages were received but sometimes got no assistant reply.

## Root cause
The Telegram channel traffic was not routed through proxy in this network environment.
Without channel-level proxy, Telegram requests could fail or time out, which caused media/file turns to appear as "no reply".

## Fix / workaround
Add a `proxy` field under `channels.telegram` in `openclaw.json`.

Before:

```json
"channels": {
  "telegram": {
    "enabled": true,
    "dmPolicy": "pairing",
    "botToken": "<<hidden>>",
    "groups": { "*": { "requireMention": true } },
    "groupPolicy": "open",
    "streamMode": "partial"
  }
}
```

After:

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

Use the proxy endpoint that matches your environment.

## Validation
- [x] reproduced before fix
- [x] fixed after change

## Upstream status
- [x] local workaround only
- [ ] issue opened upstream
- [ ] fixed upstream

## References
- Issue: n/a (local deployment incident)
- PR: n/a
- Logs: local runtime observations (Telegram media/file no-reply, resolved after proxy line)

## Credits
- **B3** — reported and confirmed the fix
- **Rac** — write-up and documentation
