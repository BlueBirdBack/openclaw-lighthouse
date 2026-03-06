# Agent has no shell/git/exec access after OpenClaw 3.2 fresh install

## Problem

After a fresh install of OpenClaw 2026.3.2, the agent cannot run shell commands, use git, or access coding tools. The agent says something like "I don't have shell/git access in this chat runtime."

Running `openclaw config set agents.defaults.tools.*` produces:

```
Error: Config validation failed: agents.defaults: Unrecognized key: "tools"
```

## Root cause

OpenClaw 3.2 introduced two breaking changes:

1. **New installs default to `tools.profile = messaging`.** The `messaging` profile excludes exec, coding, and system tools. Previously, new installs defaulted to a broader profile that included these tools.

2. **`agents.defaults.tools` is not a valid config path in 3.2.** Tool settings at the agent-defaults level moved to the top-level `tools` namespace. Using `agents.defaults.tools.*` will fail with a config validation error.

Source: [OpenClaw v2026.3.2 release notes](https://github.com/openclaw/openclaw/releases/tag/v2026.3.2)

## Fix / workaround

Run on the affected host:

```bash
openclaw config set tools.profile coding
openclaw config set tools.exec.security full
openclaw config set tools.exec.ask off
openclaw gateway restart
```

- `tools.profile coding` — restores exec/coding/system tools
- `tools.exec.security full` — allows unrestricted shell commands
- `tools.exec.ask off` — removes per-command confirmation prompts
- All three use the correct top-level `tools.*` path (not `agents.defaults.tools.*`)

## Validation

- [ ] Before fix: agent says it has no shell/git access
- [ ] `openclaw config set agents.defaults.tools.*` returns validation error
- [ ] After fix: `openclaw config set tools.profile coding` succeeds with no error
- [ ] After `gateway restart`: agent can run shell commands

## Upstream status

- [x] Breaking change documented in official release notes (v2026.3.2)
- [ ] Issue opened upstream
- [ ] Fixed upstream

## References

- Release notes: https://github.com/openclaw/openclaw/releases/tag/v2026.3.2
- Breaking change: "Onboarding now defaults tools.profile to messaging for new local installs"
- Breaking change: config path `agents.defaults.tools` is unrecognized in 3.2 — use `tools.*`
