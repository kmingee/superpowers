## 派发子智能体需要多智能体支持

在 Codex 配置（`~/.codex/config.toml`）中加入：

```toml
[features]
multi_agent = true
```

这会启用 `dispatching-parallel-agents`、`subagent-driven-development` 等技能使用的多智能体工具。具体能获得哪些工具取决于模型预设选择的 multi-agent 版本（当前预设运行 V2；旧预设运行 V1）。当实际工具列表与任何表格——包括本文——不一致时，以你的**实际工具列表**为准。

- **创建子智能体：** 使用 `spawn_agent {fork_turns: "none"}` 为子智能体提供干净上下文；默认的 `"all"` 会把你的整个对话记录复制给子智能体。在 Codex 0.145+ 中，`~/.codex/agents/` 下的角色文件可以通过 `agent_type` 附加到隔离 fork。完整历史 fork 接受 `model` 和 `reasoning_effort` 覆盖（那里只有 `agent_type` 不被接受）——隔离 fork 是 SDD 为保持上下文卫生而采用的默认方式，而不是因为只有它才能覆盖模型参数。
- **修复轮次：** 使用 `followup_task` 恢复 implementer——它会发送你的消息、触发一个新回合，并在运行环境已经回收子智能体时透明地重新加载。绝不要因为“spawn 出来的智能体无法再次发送消息”而新派一个 implementer；在 V2 中始终可以继续消息。
- **生命周期：** V2 没有 `close_agent`。当需要槽位时，已完成的子智能体会自动回收；让它们保持“未关闭”没有成本。只有 V1 会话有 `close_agent`——在 V1 中，reviewer 返回审查结果后关闭它；每个 implementer 的任务审查通过后也关闭它。
- **模型名称：** 在没有对照当前 spawn allowlist 的情况下，绝不要从技能、表格或旧会话中复制模型名称到 `spawn_agent`——V2 只接受支持 V2 的预设，对其他名称会直接硬错误。

## 等待子智能体

`wait_agent` 是事件订阅，不是轮询：长时间等待会在子智能体产生 mailbox 活动的瞬间唤醒，延迟与短等待相同。短超时轮询没有任何收益，却会让每次轮询都额外消耗一次工具调用——以及一次上下文重新计费。在测量过的会话中，大约三分之二的 wait 调用都是最终超时的短轮询。

- 只要你自己还有本地工作，就完全不要等待。已完成子智能体的最终答案会推入 mailbox，并在你的下一轮一起到达。
- 当你确实空闲，而且仍有子智能体在运行时，以有界区间等待：使用 `wait_agent`，把 `timeout_ms` 设为 300000–600000（5–10 分钟）。每个区间结束后——无论被唤醒还是超时——输出一行状态，运行 `list_agents`，并追踪任何已经完成却没有报告的子智能体。绝不要连续进行少于五分钟的轮询；事件订阅会让有界长等待和短等待一样快地被唤醒。
- 完成消息本身无法唤醒空闲控制器（消息会投递，但不会触发新回合）；覆盖这段空闲窗口是 `wait_agent` **唯一**的工作。一次等待超时且没有活动，说明你应该重新核对状态，而不是把下一次等待缩短。

## Spawn 时的模型路由

你发出的每一个 `spawn_agent`——包括你自己也是被 spawn 出来的子智能体，并进一步 fan-out 时——都要根据当前正在执行技能的“模型选择”规则，明确设置 `model` **和** `reasoning_effort`。只设置 `model` 是个陷阱：子智能体的 effort 会静默恢复为该模型的默认值，而不是继承你的设置。

请你的人类伙伴在 `~/.codex/config.toml` 中加入机器级兜底，这样即使某次 spawn 没有显式指定，仍会路由到有意选择的档位，而不是默默继承当前会话中最昂贵的模型：

```toml
[agents]
default_subagent_model = "<a mid-tier model from your spawn allowlist>"
default_subagent_reasoning_effort = "medium"
```

## 环境检测

创建 worktree 或完成分支的技能，在继续之前应通过只读 git 命令检测环境：

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

- `GIT_DIR != GIT_COMMON` → 已经位于 linked worktree（跳过创建）
- `BRANCH` 为空 → detached HEAD（无法从沙箱创建分支/push/PR）

各技能如何使用这些信号，见 `using-git-worktrees` 第 0 步和 `finishing-a-development-branch` 第 1 步。

## Codex App 中的收尾

当沙箱阻止分支/push 操作时（外部管理的 worktree 中处于 detached HEAD），智能体应提交所有工作，并告诉用户使用 App 原生控件：

- **“Create branch”**——命名分支，然后通过 App UI 进行 commit/push/PR
- **“Hand off to local”**——把工作转移到用户的本地 checkout

智能体仍然可以运行测试、暂存文件，并输出建议的分支名称、提交消息和 PR 描述供用户复制。
