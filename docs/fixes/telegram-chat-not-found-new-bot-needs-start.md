# Telegram `chat not found` on new bot: start the DM once before testing

## Problem
A newly created Telegram bot is configured correctly, but outbound tests fail with:

```text
400: Bad Request: chat not found
```

This often happens right after BotFather setup in multi-bot fleets.

## Why this happens
Telegram bots cannot proactively DM a user until that user has opened the bot and sent at least one message (for example `/start` or `hi`).

So token validation (`getMe`) can be OK, while `sendMessage` still fails.

## Step-by-step fix

### 1) Verify bot token is valid
Check each new bot token:

```bash
curl -s "https://api.telegram.org/bot<BOT_TOKEN>/getMe"
```

Expected: `"ok": true`

### 2) Initialize DM manually (required)
From Telegram client:
1. Open `@<bot_username>`
2. Tap **Start** (or send `hi`)

### 3) Re-run outbound test

```bash
openclaw message send \
  --channel telegram \
  --target <telegram-user-id> \
  --message "ping" \
  --json
```

Expected: `"ok": true`

## Optional checks if it still fails
1. Confirm username/token mapping is correct in `.env`.
2. Ensure you are testing with the same bot token loaded by the running gateway.
3. Restart gateway after token changes.

## Validation
- [x] reproduced before fix (`chat not found` on fresh bot)
- [x] fixed after change (after first DM to bot, outbound send works)

## Security notes
- Never publish full bot tokens in docs or chat.
- Use placeholders in commands (`<BOT_TOKEN>`, `<telegram-user-id>`).

## Related Issues
- [Telegram setup workflow after installing OpenClaw (with root VPS notes)](./telegram-setup-workflow-after-install.md)

## Upstream status
- [x] local workflow/workaround documented
- [ ] issue opened upstream
- [ ] fixed upstream

## References
- [Telegram channel docs](https://docs.openclaw.ai/channels/telegram)
- [Telegram Bot API: sendMessage](https://core.telegram.org/bots/api#sendmessage)

## Credits
- B3 (BlueBirdBack) — real BotFather + multi-bot rollout validation
- Rac — diagnosis and concise recovery workflow
