# WSL-related Open Issues Shortlist (for B3 review)

Date: 2026-02-20  
Scope: Windows 10/11 + WSL2, using latest OpenClaw.

## P1 — Quick wins (highest contribution ROI)

1. **#21787** — cron announce fails with `pairing required` on local loopback gateway  
   https://github.com/openclaw/openclaw/issues/21787

2. **#21142** — WSL2 + `gateway.bind: lan` breaks CLI due ws:// security check  
   https://github.com/openclaw/openclaw/issues/21142

3. **#18936** — gateway/cron/CLI fail with device token mismatch after fresh install  
   https://github.com/openclaw/openclaw/issues/18936

4. **#18285** — device token mismatch on Windows + WSL2  
   https://github.com/openclaw/openclaw/issues/18285

## P2 — Medium (good signal, slightly wider surface)

5. **#17353** — Control UI stops streaming after 1008 token mismatch on localhost/WSL  
   https://github.com/openclaw/openclaw/issues/17353

6. **#17185** — agent-to-node commands fail with persistent device token mismatch (Windows)  
   https://github.com/openclaw/openclaw/issues/17185

## P3 — Cautious / possible scope drift

7. **#20870** — Telegram media fetch failed through proxy  
   https://github.com/openclaw/openclaw/issues/20870

8. **#19364** — `fetch failed` on Windows 11 (Telegram send path)  
   https://github.com/openclaw/openclaw/issues/19364

---

## Repro strategy (latest OpenClaw + Docker in WSL)

- Baseline with fresh install in container (`npm i -g openclaw@latest`).
- Recreate auth drift cases by toggling env/service token overrides.
- Run matrix on `gateway.bind` (`127.0.0.1` vs `lan`) and pairing states.
- Capture standard evidence bundle for each run:
  - `openclaw status`
  - `openclaw gateway status`
  - `openclaw channels status --probe`
  - `openclaw logs --follow --json --max-bytes 300000`

### Note
Docker-in-WSL is great for reproducible fresh-state tests, but some host-browser / Win10-vs-Win11 networking nuances still need one native host confirmation.

---

## Review rule before posting comments
Only comment when symptom overlap is strong with local evidence.
If overlap is partial/unclear, keep as draft or ask clarifying questions first.
