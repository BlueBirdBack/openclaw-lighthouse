# Fixes Index

Troubleshooting guides for common OpenClaw issues.

## Start here

### 1) Clean uninstall + reinstall (root/Linux)
- Read: [OpenClaw clean uninstall and reinstall (root/Linux)](./openclaw-clean-uninstall-and-reinstall.md)
- Use this when uninstall/reinstall leaves old state and onboarding behaves incorrectly.

### 2) Telegram setup after fresh install (especially root VPS)
- Read: [Telegram setup workflow after installing OpenClaw (with root VPS notes)](./telegram-setup-workflow-after-install.md)
- Use this when Telegram setup/pairing flow is unclear or fails after install.

### 3) New VPS install: gateway health check fails with `1006`
- Read: [Gateway health check fails with `1006` on root VPS (`systemctl --user` unavailable)](./gateway-1006-root-vps-systemd-user-unavailable.md)
- Use this when install succeeded but gateway/channel probes fail on root VPS.

### 4) Root VPS: C3 down after plugin + restart failure
- Read: [Root VPS recovery: remove `camofox-browser` and run gateway in tmux when `systemctl --user` is unavailable](./camofox-browser-root-vps-recovery.md)
- Use this when a non-bundled plugin is loaded and update/restart fails on root VPS.

### 5) Bot replies to text, but not photos/files
- Read: [Telegram bot replies to text but not to photos/files](./telegram-media-files-no-reply-missing-proxy.md)
- Use this when text works but image/file/voice messages get no reply.

### 6) `/approve` unauthorized or `/elevated full` blocked
- Read: [Telegram `/approve` says unauthorized and `/elevated full` fails](./telegram-approve-device-token-mismatch-and-elevated-gate.md)
- Use this when admin/approval commands fail.

### 7) OpenAI/Gemini required for memory?
- Read: [OpenClaw memory search: OpenAI/Gemini APIs are optional](./openclaw-memory-search-embeddings-api-optional.md)
- Use this when deciding between remote embeddings, local embeddings, or no semantic search.

### 8) Multi-instance fleet replies are slow or missing (`session file locked`)
- Read: [Multi-instance session lock timeout: clear stale locks and restart gateways](./multi-instance-session-lock-timeout-clear-locks-and-restart.md)
- Use this when `openclaw agent` times out with `session file locked (timeout 10000ms)`.

### 9) New Telegram bot says `chat not found`
- Read: [Telegram `chat not found` on new bot: start the DM once before testing](./telegram-chat-not-found-new-bot-needs-start.md)
- Use this when BotFather setup is done but outbound message tests fail.

## Template
- [Fix template](./TEMPLATE.md)
