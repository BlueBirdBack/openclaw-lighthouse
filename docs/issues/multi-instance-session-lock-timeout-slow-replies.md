# Multi-instance session lock timeout causes slow or missing replies

## Summary
In a multi-instance Docker setup, some OpenClaw gateways can become slow or stop replying after repeated local agent runs. The visible error is usually:

```text
session file locked (timeout 10000ms)
```

When this happens, model fallback does not help, because the failure is in session file locking, not model quality.

## Environment
- OpenClaw version: 2026.2.27 (observed in container fleet)
- Deployment: Docker Compose multi-instance
- Host OS: Debian-based VPS
- Channel: Telegram (plus local `openclaw agent --local` test commands)
- Affected pattern: multiple gateways (`oc7`–`oc11`) with separate volumes

## Reproduction
1. Run repeated `openclaw agent --local --agent main ...` calls on one or more instances.
2. Interrupt/overlap runs (or keep testing quickly across many instances).
3. Run another local agent call on the same instance.

Observed behavior:
- call hangs or returns no payload
- errors include `session file locked (timeout 10000ms)`
- user sees very slow or missing replies

## Findings
### Confirmed
- Affected instances had stale lock files under:
  - `/home/node/.openclaw/agents/main/sessions/*.jsonl.lock` (inside container)
  - mapped host path: `/opt/openclaw-multi/data/ocX/config/agents/main/sessions/*.jsonl.lock`
- Error logs showed lane failures with lock timeout (10s).
- Host CPU and memory were healthy during incident, so this was not resource saturation.
- Removing stale lock files and restarting gateways restored normal replies.

### Likely
- Fast repeated local test runs can leave lock files behind when runs overlap or terminate badly.

### Unknown
- Whether a specific OpenClaw build regression increased lock persistence in this exact environment.

## Mitigation / Workaround
- Clear stale `*.jsonl.lock` files for affected instances.
- Restart those gateway containers.
- Avoid aggressive parallel local test loops against the same session.

Detailed command workflow is documented here:
- [Fix: clear stale session locks and restart affected gateways](../fixes/multi-instance-session-lock-timeout-clear-locks-and-restart.md)

## Risk / Impact
- **User impact:** delayed replies or no reply.
- **Operational impact:** looks like “model is slow/bad” while root cause is session lock state.
- **Scale impact:** more likely in multi-instance fleets with frequent scripted tests.

## Related Issues/PRs
- Related Lighthouse risk note: [Multi-agent routing: setup works for simple cases, but advanced configs are fragile](./multi-agent-routing-setup-fragility.md)
- No upstream issue linked yet for this exact lock-timeout cluster in this note.

## Next actions
- [x] Local workaround documented and validated.
- [ ] Reproduce on latest OpenClaw with minimal script and open upstream issue if repeatable.
- [ ] Add a lightweight lock-health check to fleet runbooks.

## References
- [Troubleshooting docs](https://docs.openclaw.ai/help/troubleshooting)
- [CLI docs](https://docs.openclaw.ai/cli/agent)
