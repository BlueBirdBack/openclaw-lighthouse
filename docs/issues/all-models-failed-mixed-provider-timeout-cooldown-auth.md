# All models failed: mixed timeout + provider cooldown + Anthropic OAuth 403

## Summary
A reply failed before generation because the full model fallback chain was exhausted.

Observed error payload (redacted):

```text
All models failed (4):
- openai-codex/gpt-5.3-codex: LLM request timed out. (unknown)
- openai-codex/gpt-5.3-codex-spark: No available auth profile for openai-codex (all in cooldown or unavailable). (rate_limit)
- anthropic/claude-sonnet-4-6: HTTP 403 permission_error: OAuth authentication blocked by organization policy. (auth)
- anthropic/claude-opus-4-6: No available auth profile for anthropic (all in cooldown or unavailable). (rate_limit)
```

This is a multi-provider availability/auth failure, not a single-model failure.

Redaction note: request IDs and any organization-identifying details are intentionally omitted.

## Environment
- Date observed: 2026-02-23
- Channel context: Telegram workflow
- Model chain in error:
  - `openai-codex/gpt-5.3-codex`
  - `openai-codex/gpt-5.3-codex-spark`
  - `anthropic/claude-sonnet-4-6`
  - `anthropic/claude-opus-4-6`
- OpenClaw version: not captured in this report payload

## Reproduction
1. Configure fallback chain across multiple models/providers.
2. Keep an Anthropic OAuth profile in an organization where OAuth is blocked.
3. Trigger provider cooldown/rate-limit conditions on remaining profiles.
4. Send a normal request.

## Findings
1. Fallback chain only helps if at least one downstream profile is both valid and available.
2. `HTTP 403 permission_error` on Anthropic OAuth is a hard auth policy failure (not a temporary timeout).
3. Cooldown/rate-limit on remaining profiles can make all fallback candidates unavailable.
4. Result: hard user-facing outage (`Agent failed before reply: All models failed`).

## Mitigation / Workaround
1. Verify live provider/profile health:

```bash
openclaw models status --probe --plain
openclaw models status --probe --probe-provider openai-codex --plain
openclaw models status --probe --probe-provider anthropic --plain
```

2. Fix Anthropic auth mode for this org (use an allowed auth method/profile instead of blocked OAuth).
3. Ensure fallback includes at least one provider/profile that is currently healthy.
4. Temporarily remove blocked profiles from fallback order until auth policy is fixed.
5. Capture incident logs for audit:

```bash
openclaw logs --follow
```

## Risk / Impact
- **Reliability:** no reply is delivered.
- **Operability:** fallback appears configured but still fails hard.
- **User trust:** repeated outages look random without profile-level health visibility.

## Related Issues/PRs
- Local Lighthouse note (partial overlap, codex-only cooldown focus):
  - [OpenAI Codex provider cooldown: all models failed (no available auth profile)](./openai-codex-all-models-failed-cooldown-rate-limit.md)

## Next actions
- [ ] Add an auth/profile preflight check before production rollout.
- [ ] Keep fallback providers independent and policy-compatible.
- [ ] Open upstream issue if reproducible with full `models status --probe` evidence.

## References
- [Model Failover](https://docs.openclaw.ai/concepts/model-failover)
- [Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference)
- [Troubleshooting](https://docs.openclaw.ai/help/troubleshooting)
