# Feishu QuickStart install warns: `plugins.allow` is empty and non-bundled plugins may auto-load

## Summary
During QuickStart onboarding with Feishu/Lark, plugin install succeeds but startup prints a security warning:

`[plugins] plugins.allow is empty; discovered non-bundled plugins may auto-load: feishu (...) Set plugins.allow to explicit trusted ids.`

This is not a plugin crash. It is a trust-boundary warning that can confuse first-time users.

## Environment
- OpenClaw flow: `openclaw onboard` (QuickStart)
- Selected channel: Feishu/Lark (飞书)
- Plugin: `@openclaw/feishu` installed to `~/.openclaw/extensions/feishu`
- Runtime user in report: `root`

## Reproduction
1. Run onboarding and select Feishu/Lark.
2. Choose plugin install from npm (`@openclaw/feishu`).
3. Let installer download/extract/install dependencies.
4. Observe startup logs.

## Expected vs actual
- Expected:
  - Plugin installs cleanly with clear “ready” status.
- Actual:
  - Install succeeds, but startup warns that `plugins.allow` is empty and non-bundled plugins can auto-load.

## Findings
1. This appears to be an intentional hardening warning, not a runtime failure.
2. Warning is triggered when plugin discovery can find non-bundled plugins and no explicit allowlist is set.
3. Feishu can still work, but security posture is less strict than explicit plugin pinning.

## Mitigation / Workaround
Pin trusted plugin ids explicitly.

Option A (recommended): set allowlist in config:

```json
{
  "plugins": {
    "allow": ["feishu"],
    "entries": {
      "feishu": { "enabled": true }
    }
  }
}
```

Option B (CLI helper, if preferred):

```bash
openclaw config set plugins.allow '["feishu"]'
```

Then restart gateway.

## Risk / Impact
- **Security risk:** wider plugin auto-load surface when `plugins.allow` is unset.
- **UX risk:** users may interpret warning as install failure.
- **Ops risk:** inconsistent plugin set across hosts if discovery differs.

## Related Issues/PRs
- No upstream issue linked yet for this specific onboarding warning report.

## Next actions
- [ ] Add a short onboarding note: warning means “harden config”, not “install failed”.
- [ ] Validate whether QuickStart should offer one-click `plugins.allow` pinning.
- [ ] Track upstream UX improvement opportunity if repeated.

## References
- [Plugins (Extensions)](https://docs.openclaw.ai/tools/plugin)
- [Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference)
- [Troubleshooting](https://docs.openclaw.ai/help/troubleshooting)
