# OpenClaw 3.2 / 3.7 升级后 skill 不执行（中文）

## 问题

升级到 OpenClaw `2026.3.2` 或 `2026.3.7` 后，可能出现“skill 看起来不执行”：

- Agent 提示无法运行 shell/git/exec
- 触发词命中了，但执行步骤没有生效
- 升级前可用的命令升级后失效

## 可能根因

1. 升级后工具策略更严格（尤其是 profile 与 exec 策略）。
2. 某些环境默认在 sandbox 运行，能力过于精简，不满足当前工作流。
3. CLI 与正在运行的 service 可能不在同一配置上下文，导致“看起来配置对了但仍不生效”。

## 修复 / 规避

### 步骤 1：显式设置工具策略

```bash
openclaw config set tools.profile coding
openclaw config set tools.exec.security full
openclaw config set tools.exec.ask off
openclaw gateway restart
```

### 步骤 2：如果仍受 sandbox 限制

```bash
openclaw config set agents.defaults.sandbox.mode off
openclaw gateway restart
openclaw sandbox recreate --all
```

> 关闭 sandbox 会降低隔离安全性，请按需使用。

## 验证

执行：

```bash
openclaw agent --to telegram:<redacted> --message "Use exec tool to run: openclaw --version"
```

期望：
- 返回版本号（例如 `2026.3.7`），说明 exec/tool 链路恢复。

## 附加排查

```bash
openclaw config get tools.profile
openclaw config get tools.exec.security
openclaw config get tools.exec.ask
openclaw sandbox explain
openclaw gateway status
```

## 参考

- 3.2 专项修复页： [Agent has no shell/git/exec access after OpenClaw 3.2 fresh install](./v3-2-agent-no-exec-tools-profile-messaging-default.md)
- 3.7 公开反馈： https://x.com/imwsl90/status/2030866511943123398
