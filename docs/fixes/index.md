# Fixes Index

Troubleshooting guides for common OpenClaw issues.

## Start here

### 1) Telegram setup after fresh install (especially root VPS)
- Read: [Telegram setup workflow after installing OpenClaw (with root VPS notes)](./telegram-setup-workflow-after-install.md)
- Use this when Telegram setup/pairing flow is unclear or fails after install.

### 2) New VPS install: gateway health check fails with `1006`
- Read: [Gateway health check fails with `1006` on root VPS (`systemctl --user` unavailable)](./gateway-1006-root-vps-systemd-user-unavailable.md)
- Use this when install succeeded but gateway/channel probes fail on root VPS.

### 3) Bot replies to text, but not photos/files
- Read: [Telegram bot replies to text but not to photos/files](./telegram-media-files-no-reply-missing-proxy.md)
- Use this when text works but image/file/voice messages get no reply.

### 4) `/approve` unauthorized or `/elevated full` blocked
- Read: [Telegram `/approve` says unauthorized and `/elevated full` fails](./telegram-approve-device-token-mismatch-and-elevated-gate.md)
- Use this when admin/approval commands fail.

### 5) OpenAI/Gemini required for memory?
- Read: [OpenClaw memory search: OpenAI/Gemini APIs are optional](./openclaw-memory-search-embeddings-api-optional.md)
- Use this when deciding between remote embeddings, local embeddings, or no semantic search.

## Template
- [Fix template](./TEMPLATE.md)
