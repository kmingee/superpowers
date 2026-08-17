# Hermes Agent 工具映射

技能用动作描述需求（“派发子智能体”“创建待办事项”“读取文件”）。在 Hermes Agent 中，这些动作对应下面的工具。

## 工具

| 技能请求的动作 | Hermes 工具 |
|---|---|
| 读取文件 | `read_file` |
| 创建新文件 | `write_file` |
| 编辑文件（定向 patch） | `patch` |
| 运行 shell 命令 | `terminal` |
| 搜索文件内容 | `search_files` |
| 按名称查找文件 | 通过 `terminal` 使用 `find` |
| 获取 URL / 读取网页 | `web_extract(urls=[...])` |
| 搜索网页 | `web_search(query=...)` |
| 派发子智能体 | `delegate_task(goal=..., context=..., toolsets=[...], role="leaf")` |
| 任务跟踪 | `todo` 工具 |
| 调用技能 | `skill_view("skill-name")` |

## 指令文件

当技能提到“你的指令文件”时，在 Hermes Agent 中指的是项目目录下的 **`AGENTS.md`**，或全局的 **`SOUL.md`**（`~/.hermes/SOUL.md`）。

## 调用技能

Hermes Agent 有一个 `skills` 工具集，其中包含 `skill_view` 和 `skills_list`。
调用 Superpowers 技能时使用：

```
skill_view("brainstorming")
skill_view("test-driven-development")
```

如果 `skill_view` 找不到某个 Superpowers 技能（插件完全注册之前，它可能尚未出现在目录中），请回退为直接读取 SKILL.md：

```
read_file(path="~/.hermes/plugins/superpowers/skills/<skill-name>/SKILL.md")
```

这与其他不支持原生技能加载的运行环境所采用的回退机制相同。

## 派发子智能体

使用 `delegate_task` 创建隔离子智能体，用于并行或顺序工作流：

```
delegate_task(goal="...", context="...", toolsets=[...], role="leaf")
```

如果 `delegate_task` 不可用，就在当前会话内完成工作，不要编造不存在的工具调用。

## 任务跟踪

使用 `todo` 工具跟踪单次会话中的任务。多智能体任务看板如果可用，可以使用 `hermes kanban` CLI。较旧内容中的 `TodoWrite` 应理解为这里的任务跟踪动作。
