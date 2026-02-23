# All models failed: fallback chain exhausted by cooldown/auth failures

## Summary
A reply failed before generation because every model in the fallback chain was unavailable.

Observed payload variants (redacted):

### Variant A (mixed timeout + auth policy + cooldown)
```text
All models failed (4):
- openai-codex/gpt-5.3-codex: LLM request timed out. (unknown)
- openai-codex/gpt-5.3-codex-spark: No available auth profile for openai-codex (all in cooldown or unavailable). (rate_limit)
- anthropic/claude-sonnet-4-6: HTTP 403 permission_error: OAuth authentication blocked by organization policy. (auth)
- anthropic/claude-opus-4-6: No available auth profile for anthropic (all in cooldown or unavailable). (rate_limit)
```

### Variant B (runtime alert, mixed timeout + auth policy + cooldown)
```text
⚠️ Agent failed before reply: All models failed (4):
- openai-codex/gpt-5.3-codex: LLM request timed out. (unknown)
- openai-codex/gpt-5.3-codex-spark: No available auth profile for openai-codex (all in cooldown or unavailable). (rate_limit)
- anthropic/claude-sonnet-4-6: HTTP 403 permission_error: OAuth authentication is currently not allowed for this organization. (request_id: <REDACTED_REQUEST_ID>) (auth)
- anthropic/claude-opus-4-6: No available auth profile for anthropic (all in cooldown or unavailable). (rate_limit)
Logs: openclaw logs --follow
```

### Variant C (runtime alert, pure multi-provider cooldown)
```text
⚠️ Agent failed before reply: All models failed (4):
- openai-codex/gpt-5.3-codex: Provider openai-codex is in cooldown (all profiles unavailable). (rate_limit)
- openai-codex/gpt-5.3-codex-spark: Provider openai-codex is in cooldown (all profiles unavailable). (rate_limit)
- anthropic/claude-sonnet-4-6: Provider anthropic is in cooldown (all profiles unavailable). (rate_limit)
- anthropic/claude-opus-4-6: Provider anthropic is in cooldown (all profiles unavailable). (rate_limit)
Logs: openclaw logs --follow
```

This issue cluster is about **fallback exhaustion**, not a single-model bug.

Redaction note: request IDs and organization-identifying details are redacted (shown as placeholders when useful for pattern matching).

## Environment
- First observed: 2026-02-23
- Channel context: Telegram workflow
- Model chain in error:
  - `openai-codex/gpt-5.3-codex`
  - `openai-codex/gpt-5.3-codex-spark`
  - `anthropic/claude-sonnet-4-6`
  - `anthropic/claude-opus-4-6`
- OpenClaw version: not consistently captured in payloads

## Reproduction
1. Configure a multi-model fallback chain.
2. Keep one or more profiles in cooldown/rate-limit state.
3. Optionally include an auth-policy-blocked profile (e.g., org-level OAuth not allowed).
4. Send a normal user prompt.

## Findings
1. Fallback only works if at least one downstream profile is both valid and currently available.
2. This cluster has two practical modes:
   - auth/policy failure (403) + cooldown
   - cooldown-only across all configured providers
3. Cooldown-only mode can cause full outage even when credentials are technically valid.
4. User-facing result is hard failure: `Agent failed before reply: All models failed`.

## Mitigation / Workaround
1. Probe provider/profile health first:

```bash
openclaw models status --probe --plain
openclaw models status --probe --probe-provider openai-codex --plain
openclaw models status --probe --probe-provider anthropic --plain
```

2. Remove or fix profiles blocked by org auth policy.
3. Ensure fallback includes at least one healthy provider/profile path.
4. During cooldown storms, use backoff/retry window instead of rapid re-fire.
5. Keep incident evidence:

```bash
openclaw logs --follow
```

## Risk / Impact
- **Reliability:** no reply delivered.
- **Operability:** fallback looks configured but can still fail hard.
- **User trust:** repeated outages look random without profile-level health visibility.

## Related Issues/PRs
- Local Lighthouse note (codex-only overlap):
  - [OpenAI Codex provider cooldown: all models failed (no available auth profile)](./openai-codex-all-models-failed-cooldown-rate-limit.md)

## Next actions
- [ ] Add auth/profile preflight checks before production rollout.
- [ ] Keep at least one independent healthy fallback path per deployment.
- [ ] If reproducible with probes/logs, open upstream issue with redacted evidence bundle.

## References
- [Model Failover](https://docs.openclaw.ai/concepts/model-failover)
- [Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference)
- [Troubleshooting](https://docs.openclaw.ai/help/troubleshooting)
