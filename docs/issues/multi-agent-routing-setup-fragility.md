# Multi-agent routing: setup works for simple cases, but advanced configs are fragile

## Summary
Multi-agent routing in OpenClaw is usable for small setups (for example: one agent per channel, no peer overrides).

The risk climbs fast when you combine:
- multiple agents
- multiple channel accounts
- per-peer bindings
- per-agent `agentDir`
- session scope choices

This is not one single bug. It is a recurring issue cluster where routing and session-path behavior can regress between versions.

## Environment
- Analysis date: 2026-02-23
- Evidence source A: official docs (`docs.openclaw.ai`)
- Evidence source B: live GitHub issue queries (`openclaw/openclaw`)
- Evidence source C: local issue snapshot:
  - `research/openclaw-issues-snapshot/2026-02-20-221422/issues-all.jsonl`

## Reproduction
Use a minimal but realistic multi-agent setup:

1. Create two isolated agents.
2. Configure two accounts on one channel (Telegram/Discord/WhatsApp/Slack).
3. Add account-level bindings.
4. Add one peer-level override binding above channel-wide rules.
5. Restart gateway and run:
   - `openclaw agents list --bindings`
   - `openclaw channels status --probe`
6. Send inbound messages to both accounts and one bound peer.

### Expected
Messages route deterministically to the intended `agentId` + account path.

### Actual (seen in issue history)
Depending on version and config shape, users reported:
- wrong agent response
- wrong account delivery
- dropped inbound on one account
- session path validation failures

## Findings
1. **Docs quality is improving**, but setup still has many moving parts.
2. **Binding priority + first-match ordering** is deterministic, but easy to misconfigure.
3. **Regression pattern is real** across channels (Telegram/Discord/Slack/WhatsApp).
4. A recurring error string appears often in issue history:
   - `Session file path must be within sessions directory`
5. Snapshot grep (2026-02-20) found this exact string in **112 issues** (many duplicates/variants).

## Mitigation / Workaround
Use a hardened rollout path:

1. Start with account-level routing only (no peer overrides yet).
2. Keep each agent on a unique `agentDir` (never reuse).
3. Add peer overrides only after account routing is stable.
4. Keep peer override bindings above channel-wide bindings.
5. For multi-account DM isolation, prefer:
   - `session.dmScope: "per-account-channel-peer"`
6. Use a preflight check before production:
   - `openclaw agents list --bindings`
   - `openclaw channels status --probe`
   - `openclaw gateway status`
   - `openclaw logs --follow`
7. Run a smoke test matrix (DM/group/thread per account).

## Risk / Impact
- **Privacy risk:** message may route to wrong agent/persona.
- **Reliability risk:** silent drops or partial message flow.
- **Ops risk:** high debugging cost for small config changes.

## Related Issues/PRs
Open examples:
- [#15418](https://github.com/openclaw/openclaw/issues/15418) — Discord multi-account ignores `accountId` in delivery context
- [#17047](https://github.com/openclaw/openclaw/issues/17047) — Telegram multi-account bot silently drops inbound DMs
- [#17494](https://github.com/openclaw/openclaw/issues/17494) — binding matches sub-agent but loads default workspace/personality
- [#17600](https://github.com/openclaw/openclaw/issues/17600) — channel bindings not enforced, responses in wrong channels
- [#16652](https://github.com/openclaw/openclaw/issues/16652) — Telegram default provider not starting when accounts exist

Recently closed siblings in same cluster:
- [#12444](https://github.com/openclaw/openclaw/issues/12444)
- [#12848](https://github.com/openclaw/openclaw/issues/12848)
- [#15236](https://github.com/openclaw/openclaw/issues/15236)
- [#15458](https://github.com/openclaw/openclaw/issues/15458)
- [#15665](https://github.com/openclaw/openclaw/issues/15665)
- [#15683](https://github.com/openclaw/openclaw/issues/15683)
- [#17585](https://github.com/openclaw/openclaw/issues/17585)

## Next actions
- [ ] Publish a copy/paste-safe multi-agent config template in `docs/fixes/`.
- [ ] Add a preflight checklist page (routing + account + session checks).
- [ ] Keep this issue note updated as upstream fixes land.

## References
- [Multi-Agent Routing](https://docs.openclaw.ai/concepts/multi-agent)
- [Channel Routing](https://docs.openclaw.ai/channels/channel-routing)
- [Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference)
- [Multi-Agent Sandbox & Tools](https://docs.openclaw.ai/tools/multi-agent-sandbox-tools)
- [CLI agents](https://docs.openclaw.ai/cli/agents)
- Local snapshot data: `research/openclaw-issues-snapshot/2026-02-20-221422/issues-all.jsonl`
