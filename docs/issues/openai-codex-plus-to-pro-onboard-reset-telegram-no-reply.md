# OpenAI Codex account switch (Plus → Pro) + onboard reset: Telegram stops replying

## Summary
After switching `openai-codex` auth from a ChatGPT Plus account to a ChatGPT Pro account, OpenClaw stopped replying in Telegram.

The reported flow included a full onboarding reset (`Config + creds + sessions`) and a gateway token mismatch warning before service restart.

This note tracks the symptom cluster and likely failure points.

## Environment
- OpenClaw version: `2026.2.17`
- Channel impacted: Telegram
- Runtime user in report: `root`
- Onboarding mode: `QuickStart`
- Onboarding config handling: `Reset`
- Reset scope: `Config + creds + sessions`

## Reproduction
1. Run onboarding with OpenAI Codex auth choice:
   - `openclaw onboard --auth-choice openai-codex`
2. Select reset path:
   - `Config handling: Reset`
   - `Reset scope: Config + creds + sessions`
3. Restart gateway:
   - `openclaw gateway restart`
4. Observe warning:
   - `Config token differs from service token ... run openclaw gateway install --force to sync the token`
5. Run install + restart:
   - `openclaw gateway install --force`
   - `openclaw gateway restart`
6. Telegram no longer receives replies.

## Expected vs actual
- Expected:
  - After auth switch and restart, Telegram continues normal reply flow.
- Actual:
  - Telegram stops receiving replies.
  - Intermediate warning indicates token desync between config and service.

## Findings
1. Full onboarding reset can replace config/credentials/session state in one step.
2. The token mismatch warning strongly suggests a temporary gateway auth desync until service reinstall.
3. Even after reinstall/restart, Telegram may still be silent if one of these changed during reset:
   - provider/channel startup state
   - DM pairing / allowlist state
   - auth profile selection for model/provider
4. Root cause is **not yet confirmed** from this report alone.

## Mitigation / Workaround
Use this verification sequence after auth/account migration:

1. `openclaw --version`
2. `openclaw status --all`
3. `openclaw gateway status`
4. `openclaw channels status --probe`
5. `openclaw pairing list telegram`
6. `openclaw logs --follow`

If token mismatch warning appears:
- run `openclaw gateway install --force`
- restart and re-check status/probe

If Telegram still does not reply:
- verify pairing/allowlist again
- verify model/provider auth profile availability
- capture fresh logs and open an upstream issue

## Risk / Impact
- **Message reliability:** Telegram appears online but no functional replies.
- **Ops confusion:** successful restart output may hide channel-level failure.
- **Migration risk:** account/auth tier changes can silently break runtime routing/auth state.

## Related Issues/PRs
- No upstream issue linked in this note yet.

## Next actions
- [ ] Reproduce on clean host with same migration path (Plus → Pro + reset).
- [ ] Capture gateway/channel logs during first restart after reset.
- [ ] Open upstream issue with full environment + logs if reproducible.

## References
- [Onboarding (CLI)](https://docs.openclaw.ai/start/wizard)
- [Gateway CLI](https://docs.openclaw.ai/cli/gateway)
- [Channel Troubleshooting](https://docs.openclaw.ai/channels/troubleshooting)
- [Troubleshooting](https://docs.openclaw.ai/help/troubleshooting)
