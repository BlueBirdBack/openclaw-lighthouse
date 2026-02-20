# Draft comments for open `openclaw/openclaw` issues (review before posting)

Purpose: propose field-tested workaround details from OpenClaw Lighthouse notes.
Status: **DRAFT ONLY — not posted yet**.

---

## Issue #20891
https://github.com/openclaw/openclaw/issues/20891

```markdown
We hit a very similar failure mode in a filtered network (Telegram media fetch would fail while text still worked).

What worked for us as an immediate workaround:
1) Set `channels.telegram.proxy` explicitly in `openclaw.json`
2) Add media hardening knobs:
   - `timeoutSeconds`
   - `retry.attempts/minDelayMs/maxDelayMs`
   - `network.autoSelectFamily: false` (in our environment IPv4 worked while IPv6 path was unstable)
3) Restart gateway, then validate with one image-only message + one image+caption message.

Diagnostic steps that made root-cause obvious:
- `openclaw logs --follow --json --max-bytes 300000`
- compare `curl -4` vs `curl -6` against Telegram file URL

Potential code-level direction:
- ensure Telegram `getFile`/download path uses the same proxy-aware fetch client as other channel HTTP calls
- add user-facing ack when media fetch fails (instead of silent drop)
```

---

## Issue #20870
https://github.com/openclaw/openclaw/issues/20870

```markdown
+1, reproduced similar pattern locally: text path stable, media path intermittent, logs showing fetch failures.

Our practical workaround was channel-level proxy + retry/timeouts + family selection control:
- `channels.telegram.proxy`
- `channels.telegram.timeoutSeconds`
- `channels.telegram.retry.*`
- `channels.telegram.network.autoSelectFamily=false` (environment-specific)

After restart, media inbound became stable.

If helpful, I can share a sanitized config block + validation checklist (log probe + IPv4/IPv6 curl comparison).
```

---

## Issue #20027
https://github.com/openclaw/openclaw/issues/20027

```markdown
We saw this exact symptom (`TypeError: fetch failed`) on Telegram media download path.

Observed behavior in our environment:
- Telegram text handling worked
- Media fetch failed intermittently
- IPv4 path succeeded while IPv6 path was unstable

Workaround that restored reliability:
- set `channels.telegram.proxy`
- add retry + timeout for telegram channel
- set `network.autoSelectFamily=false`
- restart gateway

Suggested improvements upstream:
1) explicit retry/backoff for Telegram media fetch
2) clearer user-facing notice when media fetch fails
3) integration test for media fetch with proxy + family-selection edge cases
```

---

## Issue #17471
https://github.com/openclaw/openclaw/issues/17471

```markdown
We hit `/elevated full` denial in Telegram too. In our case, the fix was config/policy alignment rather than model/provider behavior.

Checklist that fixed it:
1) verify current gate config:
   `openclaw config get tools.elevated`
2) ensure `tools.elevated.allowFrom` explicitly includes Telegram identity forms:
   - `<telegram-user-id>`
   - `tg:<telegram-user-id>`
3) restart gateway
4) re-test `/elevated full`
5) if still blocked, run:
   `openclaw sandbox explain --session <session-key>`
   to inspect which gate is failing.

This gave us actionable gate-level diagnostics.
```

---

## Issue #17607
https://github.com/openclaw/openclaw/issues/17607

```markdown
This matches what we observed: if slash/session metadata doesn’t preserve channel identity cleanly, allowFrom checks can fail in confusing ways.

Short-term mitigation we used:
- include both `<id>` and `tg:<id>` in `tools.elevated.allowFrom`
- verify failures with `openclaw sandbox explain --session <session-key>`

Given this issue, that tool output is super useful because it exposes whether the breakage is metadata propagation vs policy mismatch.
```

---

## Issue #21572
https://github.com/openclaw/openclaw/issues/21572

```markdown
We recently hit persistent `device token mismatch` after pairing; what resolved it in our deployment:

1) inspect/repair device auth state:
   - `openclaw devices list`
   - if stale operator token suspected:
     `openclaw devices revoke --device <device-id> --role operator`
2) restart gateway
3) run `openclaw doctor --repair`
4) check for stale service-level token overrides (systemd env / `OPENCLAW_GATEWAY_TOKEN` drift)

After cleanup + restart, approval/elevated flows recovered.
```

---

## Notes for posting
- Keep each comment focused on reproducible observations + workaround.
- Do not include personal IDs, tokens, local IPs, session keys, or private logs.
- Post only where signal is strong (avoid near-duplicate comments across too many issues).
