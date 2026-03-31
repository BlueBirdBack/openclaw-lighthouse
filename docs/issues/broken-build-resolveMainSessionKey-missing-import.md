# Broken build: resolveMainSessionKey missing import in session-system-events chunk

## Symptoms

Every inbound Telegram message fails with "Something went wrong". Gateway starts cleanly — no config errors, all plugins load, Telegram bot connects and polls. The error only surfaces when a message actually arrives:

```
telegram dispatch failed: ReferenceError: resolveMainSessionKey is not defined
```

```
telegram bot error: ReferenceError: resolveMainSessionKey is not defined
    at drainFormattedSystemEvents (session-system-events-CtqtoK1L.js:46:78)
    at runPreparedReply (pi-embedded-BaSvmUpW.js:94161:28)
```

## Environment
- OpenClaw version: 2026.3.24 (cff6dc9)
- OS: Linux (Debian, root VPS)
- Channel: Telegram
- Install method: `npm install -g openclaw`

## Reproduction steps
1. Install OpenClaw `2026.3.24` via `npm install -g openclaw` (may require interrupted install or stale npm cache to trigger)
2. Configure Telegram channel, start gateway — boots fine
3. Send any message to the bot
4. Bot replies "Something went wrong"

Exact trigger unknown — two boxes with identical version tags had different file contents. Suspected partial npm install, interrupted download, or CDN serving stale tarball.

## Expected vs actual
- Expected: Bot processes the message and replies normally
- Actual: `ReferenceError: resolveMainSessionKey is not defined` — every message fails silently from the user's perspective

## Notes / logs

The bundled file `session-system-events-CtqtoK1L.js` references `resolveMainSessionKey()` but doesn't import it. The function is defined in `main-session-DF6UibWM.js`.

### Working file (known-good install)

```js
import { i as resolveMainSessionKey } from "./main-session-DF6UibWM.js";
// ...
const mainSessionKey = resolveMainSessionKey(params.cfg);
if (mainSessionKey !== params.sessionKey) {
    queued.push(...drainSystemEventEntries(mainSessionKey));
}
queued.sort((left, right) => left.ts - right.ts);
```

### Broken file (bad install)

```js
// NO import for resolveMainSessionKey
// ...
// Logic crammed into one line, calls undefined function:
const queued = drainSystemEventEntries(params.sessionKey); const _mainKey = resolveMainSessionKey(params.cfg); if (_mainKey !== params.sessionKey) { queued.push(...drainSystemEventEntries(_mainKey)); } queued.sort((a, b) => a.ts - b.ts);
```

### Why it's hard to detect

- Gateway starts normally ✅
- All plugins load ✅
- Telegram bot connects and polls ✅
- `openclaw gateway status` shows healthy ✅
- Error only appears in logs *after* the first message arrives

### Workaround

Copy the working file from a known-good install:

```bash
scp good-box:/usr/lib/node_modules/openclaw/dist/session-system-events-CtqtoK1L.js \
    broken-box:/usr/lib/node_modules/openclaw/dist/session-system-events-CtqtoK1L.js
openclaw gateway restart
```

Or do a clean reinstall:

```bash
npm cache clean --force
npm install -g openclaw
openclaw gateway restart
```

## Status
- [x] reproduced
- [x] root cause known
- [x] fix available
