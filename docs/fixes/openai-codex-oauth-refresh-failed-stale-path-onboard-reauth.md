# OpenAI Codex OAuth refresh failed: stale `openclaw` binary in `PATH` + re-auth via `onboard`

## Problem

OpenClaw stops replying and shows:

- `⚠️ Agent failed before reply: OAuth token refresh failed for openai-codex`

At the same time, install reports success (new version), but shell still resolves an older `openclaw` binary.

## Root cause

Two issues overlapped:

1. **Old binary first in `PATH`**
   - `openclaw --version` returned old version (for example `2026.2.26`),
   - while `~/.openclaw/bin/openclaw --version` returned new version (`2026.3.2`).
2. **Re-auth command confusion in this state**
   - direct `models auth login --provider openai-codex` may fail in some environments,
   - onboarding auth flow worked reliably for `openai-codex` re-auth.

## Fix / workaround

### 1) Verify and switch to the correct binary

```bash
~/.openclaw/bin/openclaw --version
export PATH="$HOME/.openclaw/bin:$HOME/.openclaw/tools/node/bin:$PATH"
hash -r
openclaw --version
which -a openclaw
```

Expected first path:

```text
/root/.openclaw/bin/openclaw
```

Persist for future shells:

```bash
echo 'export PATH="$HOME/.openclaw/bin:$HOME/.openclaw/tools/node/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 2) Re-auth OpenAI Codex via onboarding auth flow

```bash
~/.openclaw/bin/openclaw onboard --auth-choice openai-codex --skip-channels --skip-skills --skip-ui --skip-health --no-install-daemon
```

### 3) Restart and verify

```bash
~/.openclaw/bin/openclaw gateway restart
~/.openclaw/bin/openclaw models status --json
~/.openclaw/bin/openclaw logs --follow
```

## Validation
- [x] reproduced before fix
- [x] fixed after change

## Upstream status
- [x] local workaround only
- [ ] issue opened upstream
- [ ] fixed upstream

## References
- Logs: `openclaw logs --follow`
- Related symptoms: OpenAI Codex auth/profile failures and no-reply scenarios
