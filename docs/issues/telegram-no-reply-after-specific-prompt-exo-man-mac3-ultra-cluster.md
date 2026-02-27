# Telegram no-reply after a specific prompt (`exo man build mac 3 ultra cluster`)

## Summary
A user reported that sending a prompt like:

```text
give me the original link about that exo man build mac 3 ultra cluster
```

may cause OpenClaw to stop replying in Telegram.

Current evidence is a symptom report (not yet a confirmed root cause). This note tracks the pattern so future incidents can be compared quickly.

## Environment
- First report date: 2026-02-24
- Channel: Telegram (direct chat)
- OpenClaw version: not captured in the report
- Model/provider at incident time: not captured

## Reproduction
1. In Telegram, send the prompt:
   - `give me the original link about that exo man build mac 3 ultra cluster`
2. Observe whether the bot replies.
3. If no reply, send a simple follow-up prompt (for example: `hi`).
4. Check whether reply flow resumes or remains silent.

## Expected vs actual
- Expected: bot replies normally to the prompt and follow-up messages.
- Actual: in some reports, no reply is sent after this prompt; follow-up may also stay silent.

## Findings
1. This is currently a **reported symptom**, not a confirmed deterministic trigger.
2. Outward behavior (“Telegram stops replying”) overlaps with other reliability issues, including model-chain failures and channel/session state drift.
3. Without incident-time logs, we cannot separate:
   - model timeout/cooldown exhaustion,
   - channel delivery path issues,
   - transient session/runtime stalls.

## Mitigation / Workaround
When this happens, capture evidence immediately:

```bash
openclaw logs --follow
openclaw status --all
openclaw gateway status
openclaw channels status --probe
```

Operational workarounds:
1. Retry with a short split query (break one long request into 2 messages).
2. Send a simple health-check prompt (`hi`) to test reply path.
3. If still silent, restart gateway and retest:
   - `openclaw gateway restart`
4. If recurrence is frequent, keep a timestamped incident log and compare against provider cooldown/auth errors.

## Risk / Impact
- **User impact:** appears as random “bot went silent” behavior.
- **Ops impact:** difficult to triage after the fact when logs are not captured live.
- **Trust impact:** reliability confidence drops, even if root cause is transient.

## Related Issues/PRs
- [OpenAI Codex account switch (Plus → Pro) + onboard reset: Telegram stops replying](./openai-codex-plus-to-pro-onboard-reset-telegram-no-reply.md)
- [All models failed: fallback chain exhausted by cooldown/auth failures](./all-models-failed-mixed-provider-timeout-cooldown-auth.md)
- [OpenAI Codex provider cooldown: all models failed (no available auth profile)](./openai-codex-all-models-failed-cooldown-rate-limit.md)

## Next actions
- [ ] Reproduce with live logs on the same host/channel path.
- [ ] Check whether this prompt is a true trigger or just correlated with provider/channel instability.
- [ ] If reproducible, open upstream issue with redacted logs + exact timestamp.

## References
- [Troubleshooting](https://docs.openclaw.ai/help/troubleshooting)
- [Gateway CLI](https://docs.openclaw.ai/cli/gateway)
- [Channels](https://docs.openclaw.ai/channels)
- [Model Failover](https://docs.openclaw.ai/concepts/model-failover)
