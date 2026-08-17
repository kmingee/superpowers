# 测试 Superpowers

Superpowers 有两类不同的测试，分别放在各自的目录中：

- **`tests/`** — 插件中不依赖 LLM 的代码是否正常工作？这里包含 Bash + Node + Python 集成测试，用于 brainstorm-server JS、OpenCode 插件加载、codex-plugin 同步以及分析工具。
- **`evals/`** — 智能体在真实 LLM 会话中的行为是否正确？这里使用 Python 运行框架驱动 Claude Code / Codex / Gemini CLI 的真实 tmux 会话，并由 LLM actor 和 verifier 判断是否遵守技能要求。

## 插件测试

位于 `tests/`。目前包括：

- `tests/brainstorm-server/` — brainstorm server JS 代码的 Node 测试套件。
- `tests/opencode/` — 用于测试 OpenCode 插件加载、引导缓存和工具注册的 Bash 测试。
- `tests/codex-plugin-sync/` — Bash 同步验证。
- `tests/kimi/` — 检查 Kimi 插件清单接线是否正确的 Bash/Python 测试。
- `tests/claude-code/test-helpers.sh`、`analyze-token-usage.py` — 其余 Bash 测试使用的工具。
- `tests/claude-code/test-subagent-driven-development.sh` — 测试智能体能否描述 SDD（Drill 中没有对应项；测试的是描述记忆，而非行为）。
- `tests/claude-code/test-subagent-driven-development-integration.sh` — 带 token 分析的扩展 SDD 集成测试（Drill 覆盖 YAGNI 子集；Bash 还检查提交数量、Claude Code 任务跟踪以及 token 遥测断言）。
- `tests/claude-code/test-worktree-native-preference.sh` — worktree 技能的 RED-GREEN-REFACTOR 验证（Drill 覆盖 PRESSURE 阶段；Bash 还覆盖 RED/GREEN 基线）。
- `tests/explicit-skill-requests/` — Haiku 专用、多轮以及由技能名称提示触发的测试，这些不由 Drill 覆盖。

运行插件测试时，请使用对应目录下的 `run-*.sh` 或 `npm test`。

## 技能行为评测

位于 `evals/`。Drill 是运行框架；场景位于 `evals/scenarios/*.yaml`。设置方法见 `evals/README.md`。快速开始：

```bash
cd evals
uv sync --extra dev
export ANTHROPIC_API_KEY=sk-...
uv run drill run triggering-test-driven-development -b claude
```

Drill 场景运行较慢（每个约 3–30+ 分钟），并且会启动真实 LLM 会话。目前它们不属于 CI；自然的后续方向是分层模型（PR 上运行快速子集，每晚 + 按需运行完整扫描）。
