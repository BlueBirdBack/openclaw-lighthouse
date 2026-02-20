# OpenClaw Lighthouse

From OpenClaw headaches to working fixes.

A practical field notebook for OpenClaw incidents we actually hit in real use, plus the shortest known fixes/workarounds.

## Start here
- 🌐 **Browse as website (GitHub Pages):** https://bluebirdback.github.io/openclaw-lighthouse/
- 🧭 **Master index:** [`docs/index.md`](./docs/index.md)
- ✅ **Solved fixes:** [`docs/fixes/index.md`](./docs/fixes/index.md)
- 🐞 **Open issues:** [`docs/issues/index.md`](./docs/issues/index.md)

If Pages is still building, use the Markdown links above directly in GitHub.

## Quick workflow (low friction)
1. Raw finding / repro → add an entry in `docs/issues/`
2. Confirmed fix/workaround → write it in `docs/fixes/`
3. Update indexes (`docs/index.md`, `docs/fixes/index.md`, `docs/issues/index.md`)

## Entry template
Each note should include:
1. Symptoms
2. Environment (OpenClaw version / OS / channel)
3. Reproduction steps
4. Root cause
5. Fix / workaround
6. Status (fixed local / upstream / pending)
7. Links (issue/PR/logs)

## Structure
- `docs/index.md` — master index (first stop)
- `docs/issues/` — problem reports (symptoms + repro)
- `docs/fixes/` — solved writeups (root cause + fix)

## Credits
- **B3** ([@BlueBirdBack](https://github.com/BlueBirdBack)) — maintainer
- **Rac** 🦝 — OpenClaw debugging companion, Lighthouse contributor
- **Friend** — add GitHub handle after collaborator is confirmed
