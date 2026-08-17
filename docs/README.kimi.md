# 在 Kimi Code 中使用 Superpowers

这是在 [Kimi Code](https://github.com/MoonshotAI/kimi-code) 中使用 Superpowers 的完整指南。

## 安装

Superpowers 已上架 Kimi Code 的插件市场。

打开插件管理器：

```text
/plugins
```

进入 `Marketplace` > `Superpowers` 并安装。

你也可以直接从本仓库安装：

```text
/plugins install https://github.com/obra/superpowers
```

若要针对尚未发布的 `dev` 分支进行验证，请明确指定该分支：

```text
/plugins install https://github.com/obra/superpowers/tree/dev
```

Kimi Code 会把插件变更应用到新会话。安装、更新、启用、禁用或重新加载插件后，请使用 `/new` 启动一个全新会话。

## 工作原理

Kimi 插件清单位于 `.kimi-plugin/plugin.json`。

该清单完成三件事：

1. 让 Kimi Code 指向现有的 `skills/` 目录。
2. 通过 `sessionStart.skill` 在会话启动时加载 `using-superpowers`。
3. 通过 `skillInstructions` 提供 Kimi 专用的工具映射。

Kimi Code 直接从本仓库读取 Superpowers 技能。没有复制的技能、软链接、hook 或额外运行时依赖。

## 工具映射

技能描述动作，而不是把某个运行时的工具名称写死。在 Kimi Code 中，这些动作对应：

- "Ask the user" / "ask clarifying questions" -> `AskUserQuestion`
- "Create a todo" / "mark complete in todo list" -> `TodoList`
- "Dispatch a subagent" -> `Agent`
- "Invoke a skill" -> Kimi Code 原生的 `Skill` 工具
- "Read a file" / "write a file" / "edit a file" -> `Read`、`Write`、`Edit`
- "Run a shell command" -> `Bash`
- "Search file contents" -> `Grep`
- "Find files by path or pattern" -> `Glob`
- "Fetch a URL" -> `FetchURL`
- "Search the web" -> `WebSearch`

## 更新

使用 Kimi Code 的插件管理器：

```text
/plugins
```

选择 Superpowers 并在其中进行更新。更新后使用 `/new` 启动一个新会话。

## 故障排查

### 插件未加载

1. 运行 `/plugins info superpowers` 并查看诊断信息。
2. 确认插件已启用。
3. 安装或更新后使用 `/new` 启动一个新会话。

### 直接从 GitHub 安装时使用了旧版本

如果裸仓库 URL 存在最新 GitHub Release，Kimi Code 会安装该 Release。若要在下一个 Superpowers Release 发布之前测试尚未发布的改动，请明确安装对应分支：

```text
/plugins install https://github.com/obra/superpowers/tree/dev
```

### 技能没有触发

1. 确认 `/plugins info superpowers` 显示插件已启用。
2. 使用 `/new` 启动一个新会话。
3. 尝试验收提示词：`Let's make a react todo list`。正常工作的安装应当在编写代码之前加载 `brainstorming`。
