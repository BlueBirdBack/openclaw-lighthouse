# Fixes Index

Troubleshooting guides for common OpenClaw issues.

## Start here

### 1) OpenAI Codex OAuth refresh failed / no reply after update
- Read: [OpenAI Codex OAuth refresh failed: stale `openclaw` binary in `PATH` + re-auth via `onboard`](./openai-codex-oauth-refresh-failed-stale-path-onboard-reauth.md)
- Use this when install says updated but OAuth refresh still fails or replies stop.

### 2) `doctor --repair` did not recover OpenClaw
- Read: [`openclaw doctor --repair` not enough: reinstall via `install.sh` and restart gateway](./doctor-repair-not-working-install-sh-restart-gateway.md)
- Use this when doctor repair does not restore normal behavior.

### 3) Clean uninstall + reinstall (root/Linux)
- Read: [OpenClaw clean uninstall and reinstall (root/Linux)](./openclaw-clean-uninstall-and-reinstall.md)
- Use this when uninstall/reinstall leaves old state and onboarding behaves incorrectly.

### 4) Telegram setup after fresh install (especially root VPS)
- Read: [Telegram setup workflow after installing OpenClaw (with root VPS notes)](./telegram-setup-workflow-after-install.md)
- Use this when Telegram setup/pairing flow is unclear or fails after install.

### 5) New VPS install: gateway health check fails with `1006`
- Read: [Gateway health check fails with `1006` on root VPS (`systemctl --user` unavailable)](./gateway-1006-root-vps-systemd-user-unavailable.md)
- Use this when install succeeded but gateway/channel probes fail on root VPS.

### 6) Root VPS: C3 down after plugin + restart failure
- Read: [Root VPS recovery: remove `camofox-browser` and run gateway in tmux when `systemctl --user` is unavailable](./camofox-browser-root-vps-recovery.md)
- Use this when a non-bundled plugin is loaded and update/restart fails on root VPS.

### 7) Bot replies to text, but not photos/files
- Read: [Telegram bot replies to text but not to photos/files](./telegram-media-files-no-reply-missing-proxy.md)
- Use this when text works but image/file/voice messages get no reply.

### 8) `/approve` unauthorized or `/elevated full` blocked
- Read: [Telegram `/approve` says unauthorized and `/elevated full` fails](./telegram-approve-device-token-mismatch-and-elevated-gate.md)
- Use this when admin/approval commands fail.

### 9) OpenAI/Gemini required for memory?
- Read: [OpenClaw memory search: OpenAI/Gemini APIs are optional](./openclaw-memory-search-embeddings-api-optional.md)
- Use this when deciding between remote embeddings, local embeddings, or no semantic search.

### 10) Multi-instance fleet replies are slow or missing (`session file locked`)
- Read: [Multi-instance session lock timeout: clear stale locks and restart gateways](./multi-instance-session-lock-timeout-clear-locks-and-restart.md)
- Use this when `openclaw agent` times out with `session file locked (timeout 10000ms)`.

### 11) New Telegram bot says `chat not found`
- Read: [Telegram `chat not found` on new bot: start the DM once before testing](./telegram-chat-not-found-new-bot-needs-start.md)
- Use this when BotFather setup is done but outbound message tests fail.

### 12) Agent has no shell/git access after OpenClaw 3.2 fresh install
- Read: [Agent has no shell/git/exec access after OpenClaw 3.2 fresh install](./v3-2-agent-no-exec-tools-profile-messaging-default.md)
- Use this when a fresh 3.2 install leaves the agent with no coding/exec tools, or when `openclaw config set agents.defaults.tools.*` fails with a validation error.

### 13) Skills not executing after OpenClaw 3.2 / 3.7 upgrade (English)
- Read: [Skills not executing after OpenClaw 3.2 / 3.7 upgrade (English)](./v3-2-v3-7-skills-not-executing-en.md)
- Use this when skills stop running after upgrade and you need a combined 3.2/3.7 playbook.

### 14) OpenClaw 3.2 / 3.7 升级后 skill 不执行（中文）
- Read: [OpenClaw 3.2 / 3.7 升级后 skill 不执行（中文）](./v3-2-v3-7-skills-not-executing-zh.md)
- 中文版排障与修复步骤，适用于 3.2 / 3.7 同类问题。

## Template
- [Fix template](./TEMPLATE.md)
