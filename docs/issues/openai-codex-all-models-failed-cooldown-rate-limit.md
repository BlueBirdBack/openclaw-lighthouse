# OpenAI Codex provider cooldown: all models failed (no available auth profile)

## Summary
In some sessions, OpenClaw fails before replying when every configured model in the fallback chain depends on `openai-codex`, and all `openai-codex` auth profiles are in cooldown/unavailable.

This behaves like a provider availability failure, not a content failure.

## Environment
- OpenClaw version: not captured in the user report
- OS: not captured in the user report
- Channel: reported in direct chat workflow
- Models in failed chain:
  - `openai-codex/gpt-5.3-codex`
  - `openai-codex/gpt-5.3-codex-spark`

## Reproduction
1. Configure primary + fallback models under the same provider (`openai-codex`).
2. Trigger provider rate limiting or profile cooldown state (high request burst can cause this).
3. Send a normal user prompt.

## Expected vs actual
- Expected:
  - A model in the chain responds, or fallback moves to another available provider.
- Actual:
  - Agent fails before reply with provider cooldown errors.

Exact reported error:

```text
⚠️ Agent failed before reply: All models failed (2):
openai-codex/gpt-5.3-codex: No available auth profile for openai-codex (all in cooldown or unavailable). (rate_limit) |
openai-codex/gpt-5.3-codex-spark: Provider openai-codex is in cooldown (all profiles unavailable) (rate_limit).
Logs: openclaw logs --follow
```

## Findings
1. The failure message is explicit: auth profiles for `openai-codex` are unavailable due to cooldown/rate-limit state.
2. Fallback is ineffective if all candidates share the same provider and the provider is in cooldown.
3. This is likely a resilience/config gap (fallback diversity), not a prompt-specific issue.

## Mitigation / Workaround
1. Add cross-provider fallback (for example one non-`openai-codex` model).
2. Reduce bursty traffic and add spacing between heavy runs.
3. Add/verify additional auth profiles for the provider if available.
4. Retry after cooldown window.
5. Capture supporting logs during failure:
   - `openclaw logs --follow`
   - `openclaw status --all`

## Risk / Impact
- **Reliability:** user gets no reply.
- **Operations:** repeated outages if traffic spikes continue.
- **UX:** appears as random total failure even with fallback configured.

## Related Issues/PRs
- No upstream issue link added yet for this exact symptom in this note.

## Next actions
- [ ] Open/track upstream issue if this repeats with fresh logs.
- [ ] Add provider-diverse fallback in production configs.
- [ ] Validate behavior under controlled load test.

## References
- [Model Failover](https://docs.openclaw.ai/concepts/model-failover)
- [Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference)
- [Troubleshooting](https://docs.openclaw.ai/help/troubleshooting)
