# Gateway abort: `auth.profiles.order` nested inside `profiles` instead of `auth`

## Problem

`openclaw gateway restart` aborts with config validation errors:

```
Config invalid
File: ~/.openclaw/openclaw.json
Problem:
 - auth.profiles.order.provider: Invalid input: expected string, received undefined
 - auth.profiles.order.mode: Invalid input (allowed: "api_key", "oauth", "token")
 - auth.profiles.order: Unrecognized key: "anthropic"
```

Gateway refuses to start. `openclaw doctor` also flags the same keys.

## Root cause

The `order` block was placed **inside** `auth.profiles` instead of as a **sibling** under `auth`. The validator treats every key under `auth.profiles.*` as a profile entry and expects `provider` (string) + `mode` (`"api_key"` | `"oauth"` | `"token"`). Since `order` has neither, validation fails.

**Broken** (order inside profiles):
```json5
{
  auth: {
    profiles: {
      "anthropic:default": { provider: "anthropic", mode: "token" },
      "anthropic:manual": { provider: "anthropic", mode: "token" },
      order: {                          // ← WRONG: treated as a profile entry
        anthropic: ["anthropic:default", "anthropic:manual"]
      }
    }
  }
}
```

**Correct** (order is sibling of profiles):
```json5
{
  auth: {
    profiles: {
      "anthropic:default": { provider: "anthropic", mode: "token" },
      "anthropic:manual": { provider: "anthropic", mode: "token" }
    },
    order: {                            // ← CORRECT: sibling of profiles under auth
      anthropic: ["anthropic:default", "anthropic:manual"]
    }
  }
}
```

## Fix / workaround

1. Open `~/.openclaw/openclaw.json`
2. Find the `auth` section
3. Move `order` out of `profiles` so it sits at the same level as `profiles` under `auth`
4. Restart: `openclaw gateway restart`

Alternatively, run `openclaw doctor --fix` to strip the unrecognized key, then manually re-add `order` at the correct level.

**Note on `mode`:** For Claude Max subscriptions (not API keys), use `mode: "token"`. For API key auth, use `mode: "api_key"`. The `order` array controls failover priority across multiple auth profiles for the same provider (e.g., dual Claude Max subscriptions).

## Validation
- [x] reproduced before fix
- [x] fixed after change

## Upstream status
- [x] local workaround only
- [ ] issue opened upstream
- [ ] fixed upstream

## References
- Docs: [Authentication](https://docs.openclaw.ai/gateway/authentication.md)
- Docs: [Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference.md)
- Docs: [Auth Credential Semantics](https://docs.openclaw.ai/auth-credential-semantics.md)
- Environment: OpenClaw 2026.3.13, Debian, root user, Telegram channel
