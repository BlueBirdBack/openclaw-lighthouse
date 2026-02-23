# OpenClaw Lighthouse Index

Front door for this repo. Start here.

## Latest fixes (up to 5)
1. [Telegram setup workflow after installing OpenClaw (with root VPS notes)](./fixes/telegram-setup-workflow-after-install.md)
2. [Gateway health check fails with `1006` on root VPS (`systemctl --user` unavailable)](./fixes/gateway-1006-root-vps-systemd-user-unavailable.md)
3. [OpenClaw memory search: OpenAI/Gemini APIs are optional](./fixes/openclaw-memory-search-embeddings-api-optional.md)
4. [Telegram `/approve` says unauthorized and `/elevated full` fails](./fixes/telegram-approve-device-token-mismatch-and-elevated-gate.md)
5. [Telegram bot replies to text but not to photos/files](./fixes/telegram-media-files-no-reply-missing-proxy.md)

## Solved
- [Telegram setup workflow after installing OpenClaw (with root VPS notes)](./fixes/telegram-setup-workflow-after-install.md)
- [Gateway health check fails with `1006` on root VPS (`systemctl --user` unavailable)](./fixes/gateway-1006-root-vps-systemd-user-unavailable.md)
- [OpenClaw memory search: OpenAI/Gemini APIs are optional](./fixes/openclaw-memory-search-embeddings-api-optional.md)
- [Telegram `/approve` says unauthorized and `/elevated full` fails](./fixes/telegram-approve-device-token-mismatch-and-elevated-gate.md)
- [Telegram bot replies to text but not to photos/files](./fixes/telegram-media-files-no-reply-missing-proxy.md)

## Open issues
- [Multi-agent routing: setup works for simple cases, but advanced configs are fragile](./issues/multi-agent-routing-setup-fragility.md)
- [OpenAI Codex provider cooldown: all models failed (no available auth profile)](./issues/openai-codex-all-models-failed-cooldown-rate-limit.md)
- [`openclaw update` reports ERROR after version changes, then `gateway restart` fails with `systemctl --user unavailable`](./issues/update-false-error-and-gateway-restart-systemctl-user-unavailable.md)
- [OpenAI Codex account switch (Plus → Pro) + onboard reset: Telegram stops replying](./issues/openai-codex-plus-to-pro-onboard-reset-telegram-no-reply.md)
- [Feishu QuickStart install warns: `plugins.allow` is empty and non-bundled plugins may auto-load](./issues/feishu-plugin-install-plugins-allow-empty-warning.md)
- [`install.sh` + Feishu setup: duplicate plugin id warning spam and gateway health check failure](./issues/install-sh-feishu-duplicate-plugin-id-and-gateway-health-check-fail.md)

---

## Folder indexes
- [Fixes index](./fixes/index.md)
- [Issues index](./issues/index.md)

## Templates
- [Issue template](./issues/TEMPLATE.md)
- [Fix template](./fixes/TEMPLATE.md)
