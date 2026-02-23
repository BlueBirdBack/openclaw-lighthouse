# `install.sh` + Feishu setup: duplicate plugin id warning spam and gateway health check failure

## Summary
Running the installer (`curl -fsSL https://openclaw.ai/install.sh | bash`) and then enabling Feishu produced two problem signals:

1. repeated config warnings about **duplicate plugin id** for `feishu`
2. health check failure because gateway was not reachable (`1006 abnormal closure`)

The logs also show:
- systemd user services unavailable in this runtime
- service install skipped during onboarding step

## Environment
- Install path style in report: global npm under `/usr/lib/node_modules/openclaw`
- Runtime user in report: `root`
- Setup path: install script + Feishu plugin install
- Channel selected: Feishu/Lark (飞书)

## Reproduction
1. Run installer:
   - `curl -fsSL https://openclaw.ai/install.sh | bash`
2. Install/enable Feishu plugin in onboarding flow.
3. Observe repeated warnings:
   - `plugins.entries.feishu: plugin feishu: duplicate plugin id detected ...`
4. Observe systemd message:
   - `Systemd user services are unavailable. Skipping lingering checks and service install.`
5. Health check later fails with:
   - `gateway closed (1006 abnormal closure (no close frame))`

## Findings
1. The duplicate id warning indicates two Feishu plugin sources are discoverable with the same id (`feishu`).
2. One warning path points to bundled plugin location:
   - `/usr/lib/node_modules/openclaw/extensions/feishu/index.ts`
3. Repeated warning lines suggest the config/validation path emits the same warning multiple times in this flow.
4. Gateway health check failure is likely operational (gateway not running/reachable) rather than plugin crash.
5. The runtime explicitly reports systemd user services unavailable, which explains skipped service install and later gateway reachability issues.

## Mitigation / Workaround
1. Keep only one Feishu plugin source active (avoid duplicate id collision):
   - Use bundled plugin **or** installed plugin under `~/.openclaw/extensions/feishu`, not both.
2. Set explicit plugin allowlist:
   - `plugins.allow: ["feishu"]`
3. Start gateway with a mode that works on this host:
   - supported user systemd service, or
   - foreground/tmux mode when `systemctl --user` is unavailable.
4. Verify after changes:
   - `openclaw gateway status`
   - `openclaw channels status --probe`
   - `openclaw logs --follow`

## Risk / Impact
- **UX noise:** repeated warnings make onboarding look broken.
- **Config ambiguity:** uncertain which plugin copy is active.
- **Availability risk:** channel setup appears complete while gateway health is down.

## Related Issues/PRs
- Related local Lighthouse note:
  - [Feishu QuickStart install warns: `plugins.allow` is empty and non-bundled plugins may auto-load](./feishu-plugin-install-plugins-allow-empty-warning.md)
- Solved workaround doc:
  - [Gateway health check fails with `1006` on root VPS (`systemctl --user` unavailable)](../fixes/gateway-1006-root-vps-systemd-user-unavailable.md)

## Next actions
- [ ] Confirm plugin precedence with a minimal clean host (bundled-only vs installed-only).
- [ ] Reduce duplicate warning spam in onboarding/health flow (single consolidated warning preferred).
- [ ] Add explicit operator hint when systemd user service is unavailable (offer tmux foreground fallback command).

## References
- [Plugins (Extensions)](https://docs.openclaw.ai/tools/plugin)
- [Gateway runbook](https://docs.openclaw.ai/gateway/index)
- [Gateway CLI](https://docs.openclaw.ai/cli/gateway)
- [Troubleshooting](https://docs.openclaw.ai/help/troubleshooting)
