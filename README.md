# Superpowers

Superpowers 是一套面向编程智能体的完整软件开发方法论。它建立在一组可组合的技能以及一些初始指令之上，这些指令会确保你的智能体实际使用这些技能。

## 目录

- [工作原理](#工作原理)
- [商业服务](#商业服务)
- [开始使用](#安装)
  - [Claude Code](#claude-code)
  - [Antigravity](#antigravity)
  - [Codex App](#codex-app)
  - [Codex CLI](#codex-cli)
  - [Cursor](#cursor)
  - [Devin CLI](#devin-cli)
  - [Factory Droid](#factory-droid)
  - [Gemini CLI](#gemini-cli)
  - [GitHub Copilot CLI](#github-copilot-cli)
  - [Grok Build CLI](#grok-build-cli)
  - [Kimi Code](#kimi-code)
  - [OpenCode](#opencode)
  - [Pi](#pi)
  - [Hermes Agent](#hermes-agent)
- [基本工作流](#基本工作流)
- [社区](#社区)
- [包含内容](#包含内容)
- [理念](#理念)
- [贡献](#贡献)
- [更新](#更新)
- [许可证](#许可证)
- [可视化伴侣遥测](#可视化伴侣遥测)

## 工作原理

这一切从你启动编程智能体的那一刻开始。当它发现你正在构建某个东西时，*不会*立刻一头扎进代码编写。相反，它会先退一步，询问你真正想完成什么。

当它从对话中梳理出规格说明后，会把规格分成足够短、真正便于阅读和理解的片段展示给你。

在你确认设计之后，智能体会制定一份实现计划。这份计划会清晰到让一个热情十足、审美欠佳、判断力不足、不了解项目背景、而且不喜欢测试的初级工程师也能照着执行。它强调真正的红/绿 TDD、YAGNI（You Aren't Gonna Need It，你不会需要它）和 DRY。

接下来，当你说“开始”之后，它会启动 *subagent-driven-development*（子智能体驱动开发）流程，让多个智能体逐项完成工程任务、检查并审查工作结果，然后继续推进。智能体连续自主工作几个小时、同时仍不偏离你们共同制定的计划，并不少见。

系统中还有很多其他内容，但以上就是核心。由于这些技能会自动触发，你不需要做任何特殊操作。你的编程智能体自然就拥有了 Superpowers。

## 商业服务

如果你在企业环境中使用 Superpowers，并且希望获得商业支持、额外工具或托管式费用管理，欢迎发送邮件至 sales@primeradiant.com 与我们联系。

## 安装

不同运行环境（harness）的安装方式不同。如果你同时使用多个运行环境，需要分别为每个环境安装 Superpowers。

### Claude Code

Superpowers 已上架 [Claude 官方插件市场](https://claude.com/plugins/superpowers)。

#### 官方市场

- 从 Anthropic 官方市场安装插件：

  ```bash
  /plugin install superpowers@claude-plugins-official
  ```

#### Superpowers 市场

Superpowers 市场为 Claude Code 提供 Superpowers 以及其他一些相关插件。

- 注册市场：

  ```bash
  /plugin marketplace add obra/superpowers-marketplace
  ```

- 从该市场安装插件：

  ```bash
  /plugin install superpowers@superpowers-marketplace
  ```

### Antigravity

从本仓库将 Superpowers 安装为插件：

```bash
agy plugin install https://github.com/obra/superpowers
```

Antigravity 会运行插件的 session-start hook，因此从第一条消息开始 Superpowers 就会生效。更新时再次运行相同命令即可。

### Codex App

Superpowers 已上架 [Codex 官方插件市场](https://github.com/openai/plugins)。

- 在 Codex 应用侧边栏点击 Plugins。
- 你应该能在 Coding 分类中看到 `Superpowers`。
- 点击 Superpowers 旁边的 `+`，然后按提示操作。

### Codex CLI

Superpowers 已上架 [Codex 官方插件市场](https://github.com/openai/plugins)。

- 打开插件搜索界面：

  ```bash
  /plugins
  ```

- 搜索 Superpowers：

  ```bash
  superpowers
  ```

- 选择 `Install Plugin`。

### Cursor

- 在 Cursor Agent 聊天中从市场安装：

  ```text
  /add-plugin superpowers
  ```

- 或在插件市场中搜索“superpowers”。

### Devin CLI

- 从本仓库安装插件：

  ```bash
  devin plugins install obra/superpowers
  ```

- 更新到最新版本：

  ```bash
  devin plugins update superpowers
  ```

### Factory Droid

- 注册市场：

  ```bash
  droid plugin marketplace add https://github.com/obra/superpowers
  ```

- 安装插件：

  ```bash
  droid plugin install superpowers@superpowers
  ```

### Gemini CLI

- 安装扩展：

  ```bash
  gemini extensions install https://github.com/obra/superpowers
  ```

- 后续更新：

  ```bash
  gemini extensions update superpowers
  ```

### GitHub Copilot CLI

- 注册市场：

  ```bash
  copilot plugin marketplace add obra/superpowers-marketplace
  ```

- 安装插件：

  ```bash
  copilot plugin install superpowers@superpowers-marketplace
  ```

### Grok Build CLI

Superpowers 已上架 [Grok 官方插件市场](https://github.com/xai-org/plugin-marketplace)。

- 从 xAI 官方市场安装插件：

  ```bash
  grok plugin install superpowers@xai-official --trust
  ```

- 或在 TUI 中打开市场、搜索 Superpowers 并安装：

  ```text
  /marketplace
  ```

### Kimi Code

Superpowers 已上架 Kimi Code 的插件市场。

- 打开 Kimi Code 的插件管理器：

  ```text
  /plugins
  ```

- 进入 `Marketplace` > `Superpowers` 并安装。

- 或直接从本仓库安装：

  ```text
  /plugins install https://github.com/obra/superpowers
  ```

- 详细文档：[docs/README.kimi.md](docs/README.kimi.md)

### OpenCode

OpenCode 使用自己的插件安装方式；即使你已经在其他运行环境中使用 Superpowers，也需要为 OpenCode 单独安装。

- 告诉 OpenCode：

  ```
  Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md
  ```

- 详细文档：[docs/README.opencode.md](docs/README.opencode.md)

### Pi

从本仓库将 Superpowers 安装为 Pi 包：

```bash
pi install git:github.com/obra/superpowers
```

本地开发时，可以让 Pi 将当前检出目录作为临时包加载：

```bash
pi -e /path/to/superpowers
```

该 Pi 包会加载 Superpowers 技能，并加载一个小型扩展：它会在会话启动时以及上下文压缩后再次注入 `using-superpowers` 引导信息。Pi 原生支持技能，因此不需要兼容性的 `Skill` 工具。子智能体和任务列表工具仍属于可选的 Pi 配套包。

### Hermes Agent

从本仓库将 Superpowers 安装为 Hermes 插件：

```bash
hermes plugins install obra/superpowers --enable
```

安装后请重启所有正在运行的 Hermes 会话。注意：Hermes 没有压缩后 hook，因此如果一次非常长的会话在首轮内容之后发生上下文压缩，引导信息会丢失；如果技能停止触发，请启动一个新会话。

## 基本工作流

1. **brainstorming** - 在编写代码之前激活。通过提问细化粗略想法、探索备选方案，并分段展示设计供你确认。保存设计文档。

2. **using-git-worktrees** - 在设计获批后激活。在新分支上创建隔离工作区，执行项目初始化，并验证测试基线干净通过。

3. **writing-plans** - 在已有批准设计时激活。把工作拆解成小任务（每项约 2–5 分钟）。每项任务都包含精确文件路径、完整代码和验证步骤。

4. **subagent-driven-development** 或 **executing-plans** - 在已有计划时激活。为每项任务派发全新的子智能体，并进行两阶段审查（先检查规格符合性，再检查代码质量）；或者分批执行，并设置人工检查点。

5. **test-driven-development** - 在实现过程中激活。强制执行 RED-GREEN-REFACTOR（红-绿-重构）：先写失败测试并观察它失败；再写最少代码并观察它通过；然后提交。测试之前写下的代码会被删除。

6. **requesting-code-review** - 在任务之间激活。对照计划进行审查，并按严重程度报告问题。关键问题会阻止继续推进。

7. **finishing-a-development-branch** - 在任务完成时激活。验证测试，然后给出选项（合并/PR/保留/丢弃），并清理 worktree。

**智能体会在执行任何任务之前检查是否有相关技能。** 这些是强制工作流，而不是建议。

## 社区

Superpowers 由 [Jesse Vincent](https://blog.fsck.com) 和 [Prime Radiant](https://primeradiant.com) 的其他成员共同构建。

- **Discord**：[加入我们](https://discord.gg/35wsABTejz)，获取社区支持、提问，并分享你正在使用 Superpowers 构建的内容
- **Issues**：https://github.com/obra/superpowers/issues
- **版本发布通知**：[订阅](https://primeradiant.com/superpowers/) 以获取新版本通知

## 包含内容

### 技能库

**测试**
- **test-driven-development** - RED-GREEN-REFACTOR 循环（包含测试反模式参考资料）

**调试**
- **systematic-debugging** - 四阶段根因分析流程（包含 root-cause-tracing、defense-in-depth、condition-based-waiting 技术）
- **verification-before-completion** - 确保问题真的已经修复

**协作**
- **brainstorming** - 苏格拉底式设计细化
- **writing-plans** - 详细实现计划
- **executing-plans** - 带检查点的批量执行
- **dispatching-parallel-agents** - 并发子智能体工作流
- **requesting-code-review** - 审查前检查清单
- **receiving-code-review** - 响应审查反馈
- **using-git-worktrees** - 并行开发分支
- **finishing-a-development-branch** - 合并/PR 决策工作流
- **subagent-driven-development** - 通过两阶段审查（先规格符合性、再代码质量）实现快速迭代

**元技能**
- **writing-skills** - 按最佳实践创建新技能（包含测试方法论）
- **using-superpowers** - 技能系统简介

## 理念

- **测试驱动开发（Test-Driven Development）** - 永远先写测试
- **系统化优于临时应对** - 流程优于猜测
- **降低复杂度** - 把简单作为首要目标
- **证据优于断言** - 在宣布成功之前先验证

阅读[最初的版本发布公告](https://blog.fsck.com/2025/10/09/superpowers/)。

## 贡献

Superpowers 的一般贡献流程如下。请注意，我们通常不接受新增技能的贡献，而且对技能的任何更新都必须能够在我们支持的所有编程智能体上工作。

1. Fork 仓库
2. 切换到 `dev` 分支
3. 为你的工作创建一个分支
4. 按照 `writing-skills` 技能创建并测试新增或修改过的技能
5. 提交 PR，并确保填写拉取请求模板

技能行为测试使用 [superpowers-evals](https://github.com/prime-radiant-inc/superpowers-evals/) 中的 drill eval harness，并克隆到 `evals/`；设置方法见 `evals/README.md`。插件基础设施测试位于 `tests/`，通过相应的 `run-*.sh` 或 `npm test` 运行。

完整指南见 `skills/writing-skills/SKILL.md`。

## 更新

Superpowers 的更新方式在一定程度上取决于所使用的编程智能体，但通常是自动完成的。

## 许可证

MIT License - 详情见 LICENSE 文件。

## 可视化伴侣遥测

由于技能和插件不会向创建者提供任何反馈，我们并不知道有多少人在使用 Superpowers。默认情况下，brainstorming 的可选“可视化伴侣”功能会从我们的网站加载 Prime Radiant 标志，其中包含当前使用的 Superpowers 版本。它不会包含关于你的项目、提示词或编程智能体的任何细节。我们看不到你的点击，也不知道你正在构建什么。这只是帮助我们粗略了解有多少人在使用 Superpowers，以及大家使用的是哪个版本。该功能完全可选。若要禁用，请将环境变量 `SUPERPOWERS_DISABLE_TELEMETRY` 设置为任意真值。Superpowers 同样遵循 Claude Code 的 `DISABLE_TELEMETRY` 和 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 退出设置。
