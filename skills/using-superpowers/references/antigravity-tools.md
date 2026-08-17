# Antigravity CLI（`agy`）工具映射

技能用动作描述需求（“派发子智能体”“创建待办事项”“读取文件”）。在 Antigravity CLI（`agy`）中，这些动作对应下面的工具。

| 技能请求的动作 | Antigravity CLI 对应方式 |
|----------------------|----------------------|
| 派发子智能体（`Subagent (general-purpose):` 模板） | 使用带内置 `TypeName` 的 `invoke_subagent`——完整能力工作使用 `self`，只读工作使用 `research` |
| 任务跟踪（“创建待办事项”“标记完成”） | 使用**任务 artifact**——通过 `write_to_file`，并设置 `IsArtifact: true` 和 `ArtifactType: "task"`（见[任务跟踪](#任务跟踪)）。**不要**使用 `manage_task`，它管理的是后台进程。 |

## 任务跟踪

Antigravity **没有 todo 工具**（`manage_task` 管理后台进程——`list`/`kill`/`status`/`send_input`——它**不是**检查清单）。当技能要求创建待办列表或跟踪任务时，请维护一个**任务 artifact**：使用 `write_to_file` 保存 Markdown 检查清单（`IsArtifact: true`、`ArtifactMetadata.ArtifactType: "task"`），并随着进展使用 `replace_file_content` / `multi_replace_file_content` 编辑。

在任何多步骤任务开始时，创建任务 artifact，列出计划中的每一步。每完成一步，就编辑 artifact，把它标记为完成（`- [x]`）。如果计划改变，更新检查清单。始终保持它与现实同步——它是剩余工作的事实来源；当对话变长后，每开始一步之前都重新阅读它。
