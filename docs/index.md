# OpenClaw Lighthouse Index

Front door for this repo. Start here.

## Latest fixes (up to 50)
1. [`openclaw doctor --repair` not enough: reinstall via `install.sh` and restart gateway](./fixes/doctor-repair-not-working-install-sh-restart-gateway.md)
2. [Multi-instance session lock timeout: clear stale locks and restart gateways](./fixes/multi-instance-session-lock-timeout-clear-locks-and-restart.md)
3. [Telegram `chat not found` on new bot: start the DM once before testing](./fixes/telegram-chat-not-found-new-bot-needs-start.md)
4. [Root VPS recovery: remove `camofox-browser` and run gateway in tmux when `systemctl --user` is unavailable](./fixes/camofox-browser-root-vps-recovery.md)
5. [OpenClaw clean uninstall and reinstall (root/Linux)](./fixes/openclaw-clean-uninstall-and-reinstall.md)
6. [Telegram setup workflow after installing OpenClaw (with root VPS notes)](./fixes/telegram-setup-workflow-after-install.md)
7. [Gateway health check fails with `1006` on root VPS (`systemctl --user` unavailable)](./fixes/gateway-1006-root-vps-systemd-user-unavailable.md)
8. [OpenClaw memory search: OpenAI/Gemini APIs are optional](./fixes/openclaw-memory-search-embeddings-api-optional.md)
9. [Telegram `/approve` says unauthorized and `/elevated full` fails](./fixes/telegram-approve-device-token-mismatch-and-elevated-gate.md)
10. [Telegram bot replies to text but not to photos/files](./fixes/telegram-media-files-no-reply-missing-proxy.md)

## Solved
- [`openclaw doctor --repair` not enough: reinstall via `install.sh` and restart gateway](./fixes/doctor-repair-not-working-install-sh-restart-gateway.md)
- [Multi-instance session lock timeout: clear stale locks and restart gateways](./fixes/multi-instance-session-lock-timeout-clear-locks-and-restart.md)
- [Telegram `chat not found` on new bot: start the DM once before testing](./fixes/telegram-chat-not-found-new-bot-needs-start.md)
- [Root VPS recovery: remove `camofox-browser` and run gateway in tmux when `systemctl --user` is unavailable](./fixes/camofox-browser-root-vps-recovery.md)
- [OpenClaw clean uninstall and reinstall (root/Linux)](./fixes/openclaw-clean-uninstall-and-reinstall.md)
- [Telegram setup workflow after installing OpenClaw (with root VPS notes)](./fixes/telegram-setup-workflow-after-install.md)
- [Gateway health check fails with `1006` on root VPS (`systemctl --user` unavailable)](./fixes/gateway-1006-root-vps-systemd-user-unavailable.md)
- [OpenClaw memory search: OpenAI/Gemini APIs are optional](./fixes/openclaw-memory-search-embeddings-api-optional.md)
- [Telegram `/approve` says unauthorized and `/elevated full` fails](./fixes/telegram-approve-device-token-mismatch-and-elevated-gate.md)
- [Telegram bot replies to text but not to photos/files](./fixes/telegram-media-files-no-reply-missing-proxy.md)

## Open issues
- [Multi-instance session lock timeout causes slow or missing replies](./issues/multi-instance-session-lock-timeout-slow-replies.md)
- [Multi-agent routing: setup works for simple cases, but advanced configs are fragile](./issues/multi-agent-routing-setup-fragility.md)
- [OpenAI Codex provider cooldown: all models failed (no available auth profile)](./issues/openai-codex-all-models-failed-cooldown-rate-limit.md)
- [OpenAI Codex `server_error`: request failed during processing](./issues/openai-codex-server-error-processing-request.md)
- [`openclaw update` reports ERROR after version changes, then `gateway restart` fails with `systemctl --user unavailable`](./issues/update-false-error-and-gateway-restart-systemctl-user-unavailable.md)
- [OpenAI Codex account switch (Plus → Pro) + onboard reset: Telegram stops replying](./issues/openai-codex-plus-to-pro-onboard-reset-telegram-no-reply.md)
- [Telegram no-reply after a specific prompt (`exo man build mac 3 ultra cluster`)](./issues/telegram-no-reply-after-specific-prompt-exo-man-mac3-ultra-cluster.md)
- [Feishu QuickStart install warns: `plugins.allow` is empty and non-bundled plugins may auto-load](./issues/feishu-plugin-install-plugins-allow-empty-warning.md)
- [`install.sh` + Feishu setup: duplicate plugin id warning spam and gateway health check failure](./issues/install-sh-feishu-duplicate-plugin-id-and-gateway-health-check-fail.md)
- [All models failed: fallback chain exhausted by cooldown/auth failures](./issues/all-models-failed-mixed-provider-timeout-cooldown-auth.md)
- [`openclaw uninstall` + reinstall: provider onboarding is skipped, no AI provider prompt, OpenClaw unusable](./issues/uninstall-reinstall-skips-provider-onboarding.md)

---

## Folder indexes
- [Fixes index](./fixes/index.md)
- [Issues index](./issues/index.md)

## Templates
- [Issue template](./issues/TEMPLATE.md)
- [Fix template](./fixes/TEMPLATE.md)
