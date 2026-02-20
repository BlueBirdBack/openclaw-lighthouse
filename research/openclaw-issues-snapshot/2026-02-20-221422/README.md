# OpenClaw Issues Snapshot — 2026-02-20T14:20:01Z

Repo: `openclaw/openclaw`
Total issues (no PRs): **10190**
- Open: **4211**
- Closed: **5979**

This is a local read-only snapshot for offline review. It does not modify upstream GitHub issues.

## Files
- `manifest.json`
- `issues-all.json` / `issues-open.json` / `issues-closed.json`
- `issues-all.jsonl`
- `related-to-media-fix.json`
- `related-to-approve-elevated-fix.json`

## Recently updated issues (top 20)
- #20289 [closed] [Bug]: Custom bind host exists in code, but not in configuration. — https://github.com/openclaw/openclaw/issues/20289
- #14980 [open] WhatsApp group inbound messages never received (macOS, v2026.2.9, fresh install) — https://github.com/openclaw/openclaw/issues/14980
- #21869 [open] [Feature Request] Add option to disable new session greeting message in webchat — https://github.com/openclaw/openclaw/issues/21869
- #13190 [open] [Bug]: Agent Heartbeat Not Executing (wakeMode: next-heartbeat jobs never fire) — https://github.com/openclaw/openclaw/issues/13190
- #21897 [open] feat(models): migrate default model from Claude Opus 4.6 to Gemini 3.1 Pro — https://github.com/openclaw/openclaw/issues/21897
- #21891 [open] [BUG]: Session activation (/activation) not overriding config defaults for Discord groups — https://github.com/openclaw/openclaw/issues/21891
- #21894 [open] Bug: memory_search silently disabled with no user notification when embedding provider has no quota — https://github.com/openclaw/openclaw/issues/21894
- #21892 [open] LINE provider enters auto-restart loop with accounts.default configuration — https://github.com/openclaw/openclaw/issues/21892
- #21888 [open] Feature Request: Notify user when auto-compaction fires — https://github.com/openclaw/openclaw/issues/21888
- #12482 [closed] Agent cannot distinguish owner's messages from contact's messages in DM history — https://github.com/openclaw/openclaw/issues/12482
- #21885 [open] chore: add CODEOWNERS for auto-assigned PR reviews — https://github.com/openclaw/openclaw/issues/21885
- #19301 [open] [Feature]: feat: Add gpt-5.3-codex to GitHub Copilot provider with xhigh reasoning support — https://github.com/openclaw/openclaw/issues/19301
- #21879 [open] WhatsApp: raw [[tts:text]] tags leak as plain text when Edge TTS fails — https://github.com/openclaw/openclaw/issues/21879
- #21878 [open] Feature: Outbound allowlist for iMessage (and other channels) — https://github.com/openclaw/openclaw/issues/21878
- #21875 [open] [Bug]: Gemini 3.0 Pro No Longer Supported in Antigravity — https://github.com/openclaw/openclaw/issues/21875
- #21872 [open] [Bug]:  Telegram streaming not working with MiniMax model — https://github.com/openclaw/openclaw/issues/21872
- #21870 [open] [Feature Request] 强制 Agent 读取 Workspace 文件 — https://github.com/openclaw/openclaw/issues/21870
- #21819 [open] [Bug]: Token usage not being recorded in session history - totalTokens shows null — https://github.com/openclaw/openclaw/issues/21819
- #17079 [open] [Bug]: Cloud Code Assist API error (400) — https://github.com/openclaw/openclaw/issues/17079
- #21858 [open] [Feature Request]: Add agent_end / after_assistant_message hook for anti-rationalization gates — https://github.com/openclaw/openclaw/issues/21858

## Related candidates: Telegram media/proxy fix (top 15 by keyword score)
- #20891 [open] score=6 — [Bug]: Telegram file downloads don't use proxy - blocked by SSRF in Iran/filtered networks — https://github.com/openclaw/openclaw/issues/20891
- #19396 [open] score=6 — [Feature]: Add config flag to allow Mattermost file attachments from private/local IPs — https://github.com/openclaw/openclaw/issues/19396
- #19147 [open] score=6 — Bug: Telegram media messages fail with TypeError: fetch failed (undici 7.x Agent vs Node 22 built-in fetch) — https://github.com/openclaw/openclaw/issues/19147
- #20870 [open] score=5 — [Bug]: Telegram Media Fetch Failed - Cannot download images through proxy — https://github.com/openclaw/openclaw/issues/20870
- #19934 [open] score=5 — Feature request: configurable SSRF policy/allowlist for channel media fetch (Telegram) — https://github.com/openclaw/openclaw/issues/19934
- #11471 [closed] score=5 — Media fetch fails silently on transient network errors (no retry) — https://github.com/openclaw/openclaw/issues/11471
- #9815 [closed] score=5 — [Bug]: Questions about Venice's DeepSeek-v3.2 — https://github.com/openclaw/openclaw/issues/9815
- #7633 [closed] score=5 — Gateway fails to send messages to Telegram: Network request for 'sendMessage' failed — https://github.com/openclaw/openclaw/issues/7633
- #6849 [closed] score=5 — [Bug]: Telegram file download lacks timeout, can hang gateway indefinitely — https://github.com/openclaw/openclaw/issues/6849
- #2746 [closed] score=5 — Gateway crashes due to unhandled promise rejections during API calls — https://github.com/openclaw/openclaw/issues/2746
- #11499 [closed] score=4 — [Bug]: OpenClaw Model Retry Implementation — https://github.com/openclaw/openclaw/issues/11499
- #4772 [closed] score=4 — Discord integration fails in China: "Failed to resolve Discord application id" — https://github.com/openclaw/openclaw/issues/4772
- #20027 [open] score=4 — [Bug]: Telegram media fetch regression in v2026.2.17 - TypeError: fetch failed — https://github.com/openclaw/openclaw/issues/20027
- #4662 [open] score=4 — [telegram] No user ack on media fetch failure — https://github.com/openclaw/openclaw/issues/4662
- #13667 [open] score=4 — [Bug]: Telegram plugin starts but never polls for updates (fetch failed) — https://github.com/openclaw/openclaw/issues/13667

## Related candidates: approve/elevated/token-mismatch fix (top 15 by keyword score)
- #11022 [open] score=4 — [Bug]: /elevated allowlist can be bypassed by matching recipient (ctx.To) instead of sender — https://github.com/openclaw/openclaw/issues/11022
- #21146 [open] score=4 — Gateway pairing-required loops need requestId-aware recovery hints — https://github.com/openclaw/openclaw/issues/21146
- #19352 [open] score=4 — [Bug]: Device pairing bootstrap impossible - chicken-and-egg problem when CLI also requires pairing — https://github.com/openclaw/openclaw/issues/19352
- #16184 [open] score=4 — [Bug]: xec approval messages not being forwarded to Telegram despite correct configuration — https://github.com/openclaw/openclaw/issues/16184
- #2040 [closed] score=4 — Approval messages not being sent to Telegram despite correct configuration — https://github.com/openclaw/openclaw/issues/2040
- #1488 [closed] score=4 — Bug: tools.elevated ignores tools.exec.ask setting, forcing approval prompts — https://github.com/openclaw/openclaw/issues/1488
- #21812 [open] score=3 — Sub-agent spawning fails with 'pairing required' after config change + gateway restart — https://github.com/openclaw/openclaw/issues/21812
- #21688 [open] score=3 — Pairing scope-upgrade loop: repeated 'pairing required' reconnects for same device — https://github.com/openclaw/openclaw/issues/21688
- #21655 [open] score=3 — [Bug]: Internal gateway operations (cron, announce, sessions_spawn) fail with "pairing required" due to device scope enforcement on self-calls — https://github.com/openclaw/openclaw/issues/21655
- #21647 [open] score=3 — Loopback connections require device pairing on every gateway restart (2026.2.19) — https://github.com/openclaw/openclaw/issues/21647
- #21593 [open] score=3 — Bug: CLI_DEFAULT_OPERATOR_SCOPES missing read/write causes "pairing required" failures on localhost — https://github.com/openclaw/openclaw/issues/21593
- #21470 [open] score=3 — CLI device paired with operator.read scope only — cron list, gateway status fail with 'pairing required' — https://github.com/openclaw/openclaw/issues/21470
- #20707 [open] score=3 — [Bug]: Internal cron/tools 'gateway-client' Docker pairing is undocumented, fails by default — https://github.com/openclaw/openclaw/issues/20707
- #21267 [open] score=3 — [Bug]: Device token mismatch after npm update causes persistent "pairing required" error — https://github.com/openclaw/openclaw/issues/21267
- #20447 [open] score=3 — Control UI does not receive device.pair.requested broadcast (pairing approval UI broken) — https://github.com/openclaw/openclaw/issues/20447
