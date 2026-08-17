# Gemini CLI 工具映射

技能用动作描述需求（“派发子智能体”“创建待办事项”“读取文件”）。在 Gemini CLI 中，这些动作对应下面的工具。

| 技能请求的动作 | Gemini CLI 对应工具 |
|----------------------|----------------------|
| 读取文件 | `read_file` |
| 一次读取多个文件 | `read_many_files` |
| 创建新文件 | `write_file` |
| 编辑文件 | `replace` |
| 运行 shell 命令 | `run_shell_command` |
| 搜索文件内容 | `grep_search` |
| 按名称查找文件 | `glob` |
| 列出文件和子目录 | `list_directory` |
| 获取 URL | `web_fetch` |
| 搜索网页 | `google_web_search` |
| 调用技能 | `activate_skill` |
| 派发子智能体（`Subagent (general-purpose):` 模板） | 使用 `invoke_agent`，并设置 `agent_name: "generalist"`（也可通过 `@generalist` 聊天语法调用——见[子智能体支持](#子智能体支持)） |
| 多个并行派发 | 在同一条回复中发出多个 `invoke_agent` 调用 |
| 任务跟踪（“创建待办事项”“标记完成”） | `write_todos`（状态：pending、in_progress、completed、cancelled、blocked） |

## 指令文件

当技能提到“你的指令文件”时，在 Gemini CLI 中指 **`GEMINI.md`**。Gemini CLI 会分层加载 `GEMINI.md`：全局文件位于 `~/.gemini/GEMINI.md`；项目级文件位于工作区目录及其祖先目录；当工具访问子目录文件时，也会加载对应子目录中的 `GEMINI.md`。

## 个人技能目录

用户级技能位于 **`~/.gemini/skills/`**，并以 **`~/.agents/skills/`** 作为跨运行时别名（与 Codex 和 Copilot CLI 共享）。同一层级两个目录同时存在时，`.agents/skills/` 优先。每个技能都是一个包含 `SKILL.md` 的子目录（其 frontmatter 包含 `name` 和 `description`）。

## 子智能体支持

Gemini CLI 通过 `invoke_agent` 工具派发子智能体，该工具接收 `agent_name` 和 `prompt` 参数。同样的派发也以聊天语法快捷方式提供：输入 `@generalist <prompt>`，等价于调用 `invoke_agent` 并使用 `agent_name: "generalist"`。内置智能体名称包括 `generalist`、`cli_help`、`codebase_investigator`，以及启用浏览器工具时的 `browser_agent`。

技能使用 `Subagent (general-purpose):` 派发，并可能引用提示词模板文件（例如 `superpowers:subagent-driven-development` 的 `./implementer-prompt.md`），也可能直接提供行内提示词。在 Gemini CLI 中：

| 技能派发形式 | Gemini CLI 对应方式 |
|---------------------|----------------------|
| 引用 `*-prompt.md` 模板（implementer、task-reviewer、code-reviewer 等） | 填好模板，然后使用 `invoke_agent`，设置 `agent_name: "generalist"` 并传入完整提示词 |
| 引用 `superpowers:requesting-code-review` 的 `./code-reviewer.md` | 使用 `invoke_agent`，设置 `agent_name: "generalist"` 并传入填写好的审查模板 |
| 行内提示词（没有引用模板） | 使用 `invoke_agent`，设置 `agent_name: "generalist"` 并传入行内提示词 |

### 填写提示词

技能提供的提示词模板包含 `{WHAT_WAS_IMPLEMENTED}` 或 `[FULL TEXT of task]` 等占位符。在把完整提示词传给 `invoke_agent` 之前，必须填写所有占位符。提示词模板本身包含智能体角色、审查标准和预期输出格式——子智能体会遵循这些内容。

### 并行派发

Gemini CLI 支持并行派发子智能体。在同一条回复中发出多个 `invoke_agent` 调用（或在一个提示词中使用多个 `@generalist` 调用），即可并行执行彼此独立的子智能体任务。存在依赖的任务保持顺序执行，但不要仅仅为了让历史记录更简单，就把独立任务串行化。

## Gemini CLI 的其他工具

以下工具为 Gemini CLI 特有：

| 工具 | 用途 |
|------|---------|
| `save_memory`（旧版） | 当 `experimental.memoryV2 = false` 时跨会话持久化事实 |
| `get_internal_docs` | 查询 Gemini CLI 自带文档 |
| `ask_user` | 向用户提出结构化问题（文本 / 单选 / 多选） |
| `enter_plan_mode` / `exit_plan_mode` | 进入和退出只读计划模式 |
| `update_topic` | 更新当前对话的主题 / 战略意图元数据 |
| `complete_task` | 表示 Gemini 子智能体已完成，并把结果返回父智能体 |
| `tracker_create_task`、`tracker_update_task`、`tracker_get_task`、`tracker_list_tasks`、`tracker_add_dependency`、`tracker_visualize` | 带依赖关系和可视化支持的丰富任务跟踪器 |
| `read_mcp_resource`、`list_mcp_resources` | MCP 资源访问 |
