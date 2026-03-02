# Multi-instance session lock timeout: clear stale locks and restart gateways

## Problem
In multi-instance OpenClaw Docker setups, some gateways become slow or stop replying. Logs show:

```text
session file locked (timeout 10000ms)
```

Users experience delayed responses or no response.

## Why this happens
OpenClaw session files use lock files (`*.jsonl.lock`) to prevent concurrent writes. After interrupted or overlapping local runs, stale locks can remain and block new turns.

When this happens, model fallback does not recover, because all models for that turn are blocked by the same session lock.

## Step-by-step fix

### 1) Identify affected instances
Check which gateways are running and which ones are slow.

```bash
docker ps --format '{{.Names}}\t{{.Status}}' | grep 'openclaw-openclaw-gateway-' | sort -V
```

### 2) Remove stale lock files for affected instances
Use host-side mapped paths (recommended in Docker multi-instance setups).

```bash
for i in 7 8 9 10 11; do
  lockdir="/opt/openclaw-multi/data/oc${i}/config/agents/main/sessions"
  [ -d "$lockdir" ] || continue
  find "$lockdir" -name '*.jsonl.lock' -print -delete
done
```

If your instance range is different, replace `7 8 9 10 11` with your actual IDs.

### 3) Restart only affected gateway groups
Restart containers so in-memory state is also reset.

```bash
cd /opt/openclaw-multi/openclaw

docker compose --env-file .env.multi.oc7-9 -f docker-compose.oc7-9.yml restart
docker compose --env-file .env.multi.oc10-11 -f docker-compose.oc10-11.yml restart
```

### 4) Re-test responsiveness
Run one low-cost local ping per gateway.

```bash
for i in 7 8 9 10 11; do
  name="openclaw-openclaw-gateway-${i}-1"
  docker exec "$name" openclaw agent --local --agent main \
    --message "Reply exactly SPEED_OK" --thinking low --json
  echo
done
```

## Optional checks if it still fails
1. Check gateway/channel health:

```bash
docker exec openclaw-openclaw-gateway-7-1 openclaw channels status --probe
```

2. Check for newly re-created lock files:

```bash
find /opt/openclaw-multi/data/oc7/config/agents/main/sessions -name '*.jsonl.lock' -print
```

3. Avoid tight parallel test loops against the same session.

## Validation
- [x] reproduced before fix (`session file locked (timeout 10000ms)` on multiple instances)
- [x] fixed after change (stale locks removed + gateways restarted + local pings returned)

## Security notes
- Do not paste real chat IDs, bot tokens, or API keys in logs/docs.
- Limit lock cleanup to known instance paths; avoid broad `find / -delete` patterns.

## Related Issues
- [Issue: multi-instance session lock timeout causes slow or missing replies](../issues/multi-instance-session-lock-timeout-slow-replies.md)
- [Multi-agent routing: setup works for simple cases, but advanced configs are fragile](../issues/multi-agent-routing-setup-fragility.md)

## Upstream status
- [x] local workaround only
- [ ] issue opened upstream
- [ ] fixed upstream

## References
- [OpenClaw CLI docs](https://docs.openclaw.ai/cli/agent)
- [Troubleshooting](https://docs.openclaw.ai/help/troubleshooting)

## Credits
- B3 (BlueBirdBack) — real fleet symptom reports and validation
- Rac — lock-state triage, recovery workflow, and documentation
