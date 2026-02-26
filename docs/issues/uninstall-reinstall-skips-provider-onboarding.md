# `openclaw uninstall` + reinstall: provider onboarding is skipped, no AI provider prompt, OpenClaw unusable

## Summary
After uninstall/reinstall, OpenClaw starts without asking for AI providers. This leaves the instance with no working provider config, so normal chat/tool usage fails.

Reported sequence:
1. `openclaw uninstall openclaw uninstall --all --yes openclaw uninstall --dry-run`
2. `curl -fsSL https://openclaw.ai/install.sh | bash`

## Environment
- Install method: `install.sh` (`curl -fsSL https://openclaw.ai/install.sh | bash`)
- Docs referenced by reporter:
  - https://docs.openclaw.ai/cli/uninstall#uninstall
  - https://docs.openclaw.ai/install
- Channel: not specified
- OS/runtime: not specified

## Reproduction steps
1. Run uninstall command(s), including `--all --yes` and/or dry-run checks.
2. Reinstall via `install.sh`.
3. Start/use OpenClaw.
4. Observe no onboarding prompt for AI providers.

## Expected vs actual
- Expected:
  - Fresh install should guide user to configure at least one provider (or clearly block with a setup-required message and exact next command).
- Actual:
  - No provider selection prompt appears.
  - OpenClaw is installed but cannot be used due to missing provider setup.

## Findings (current confidence: medium)
1. The reported uninstall command appears concatenated/repeated, which may indicate command misuse or ambiguous docs/examples.
2. Even if uninstall syntax is imperfect, reinstall UX should still fail safely and guide provider setup.
3. Current onboarding path likely assumes provider state from prior config or does not force explicit provider configuration in this flow.

## Mitigation / Workaround
1. Confirm current config and status:
   - `openclaw status`
2. Re-run onboarding/setup explicitly after install (if available in current version):
   - `openclaw onboard`
3. If still broken, reset onboarding-related local config and retry install/onboard.
4. Verify provider is configured before normal use.

## Risk / Impact
- **High first-run failure risk:** users think install succeeded but product is unusable.
- **Confusing uninstall/reinstall UX:** docs and CLI behavior may diverge in edge paths.
- **Support load increase:** repeated “installed but cannot chat” reports.

## Suggested product/docs improvements
1. Add explicit post-install validation: if no provider configured, print hard error + exact fix command.
2. Make uninstall docs/examples clearer around `--dry-run` vs destructive flags and command syntax.
3. Add a reinstall troubleshooting section in install docs: “No provider prompt after install”.

## Status
- [ ] reproduced
- [ ] root cause known
- [ ] fix available

## References
- [Uninstall CLI docs](https://docs.openclaw.ai/cli/uninstall#uninstall)
- [Install docs](https://docs.openclaw.ai/install)
