# Skills not executing after OpenClaw 3.2 / 3.7 upgrade (English)

## Problem

After upgrading to OpenClaw `2026.3.2` or `2026.3.7`, skills may appear to stop running. Typical symptoms:

- Agent says it cannot run shell/git/exec tools
- Skill triggers are detected, but execution steps do nothing
- Commands that worked before upgrade stop working

## Root cause (likely)

1. Effective tool policy is stricter after upgrade (especially profile + exec policy).
2. In some setups, runtime is sandboxed and too minimal for expected workflow.
3. CLI config context and running service context may diverge; checks from one context can mislead.

## Fix / workaround

### Step 1 — set explicit tool policy

```bash
openclaw config set tools.profile coding
openclaw config set tools.exec.security full
openclaw config set tools.exec.ask off
openclaw gateway restart
```

### Step 2 — if still blocked by sandbox limits

```bash
openclaw config set agents.defaults.sandbox.mode off
openclaw gateway restart
openclaw sandbox recreate --all
```

> Only disable sandbox if you understand the security tradeoff.

## Validation

Run:

```bash
openclaw agent --to <your-chat-target> --message "Use exec tool to run: openclaw --version"
```

Expected:
- Returns a version string (for example `2026.3.7`), which confirms exec/tool path is working.

## Extra checks

```bash
openclaw config get tools.profile
openclaw config get tools.exec.security
openclaw config get tools.exec.ask
openclaw sandbox explain
openclaw gateway status
```

## References

- 3.2-focused fix page: [Agent has no shell/git/exec access after OpenClaw 3.2 fresh install](./v3-2-agent-no-exec-tools-profile-messaging-default.md)
- Public report (3.7): https://x.com/imwsl90/status/2030866511943123398
