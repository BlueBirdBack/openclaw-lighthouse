# `openclaw update` reports ERROR after version changes, then `gateway restart` fails with `systemctl --user unavailable`

## Summary
A user upgraded OpenClaw from `2026.2.17` to `2026.2.22-2` with `openclaw update`.

The update output still reported `Update Result: ERROR` even though the version changed successfully. Right after that, `openclaw gateway restart` failed with:

`Gateway service check failed: Error: systemctl --user unavailable: Failed to connect to bus: No medium found`

This looks like two linked operational problems:
1. updater result is confusing/possibly false-negative in global npm installs
2. service restart command assumes a user-systemd bus that is not available in this runtime

## Environment
- OpenClaw before update: `2026.2.17`
- OpenClaw after update: `2026.2.22-2`
- Install path shown in output: `/usr/lib/node_modules/openclaw`
- Runtime user shown in report: `root`
- Service error mentions missing `systemctl --user` bus

## Reproduction
1. Confirm current version:
   - `openclaw --version`
2. Run update:
   - `openclaw update`
3. Confirm version again:
   - `openclaw --version`
4. Try service restart:
   - `openclaw gateway restart`

## Expected vs actual
- Expected:
  - update result reflects final state clearly (success if version changed and binary is usable)
  - restart works or gives explicit fallback guidance for non-systemd environments
- Actual:
  - update says `ERROR` despite version moving from `2026.2.17` to `2026.2.22-2`
  - `gateway restart` fails because `systemctl --user` is unavailable

## Findings
1. The update path likely used global npm (`Reason: global update`) and produced many deprecation warnings.
2. Version changed successfully, so `ERROR` may be a false-negative or partial-failure classification.
3. `openclaw gateway restart` is a **service-manager** action and requires supported init/service context.
4. In root/container/no-user-bus environments, `systemctl --user` can fail with `No medium found`.

## Mitigation / Workaround
1. If `gateway restart` fails with missing user bus, run foreground mode directly:
   - `openclaw gateway run`
2. If you need managed service restart, use an environment with supported service manager (systemd user service available).
3. After update, verify final state with:
   - `openclaw --version`
   - `openclaw gateway status`
4. Capture logs for diagnosis:
   - `openclaw logs --follow`

## Risk / Impact
- **Reliability risk:** operators may think update failed when binary actually updated.
- **Ops risk:** restart automation breaks in container/root shells without user-systemd bus.
- **Recovery delay:** mixed signals increase troubleshooting time.

## Related Issues/PRs
- No upstream issue link attached in this note yet.

## Next actions
- [ ] Reproduce on clean container + clean VM to confirm false-negative update classification.
- [ ] Open upstream issue with full command output and environment details.
- [ ] Document a clear non-systemd restart playbook for operators.

## References
- [Gateway CLI](https://docs.openclaw.ai/cli/gateway)
- [Troubleshooting](https://docs.openclaw.ai/help/troubleshooting)
- [Updating](https://docs.openclaw.ai/install/updating)
