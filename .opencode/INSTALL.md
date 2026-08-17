# 为 OpenCode 安装 Superpowers

## 前置条件

- 已安装 [OpenCode.ai](https://opencode.ai)

## 安装

将 superpowers 加入 `opencode.json`（全局或项目级）的 `plugin` 数组：

```json
{
  "plugin": ["superpowers@git+https://github.com/obra/superpowers.git"]
}
```

重启 OpenCode。插件会通过 OpenCode 的插件管理器安装，并注册所有技能。

可以通过询问下面这句话验证："Tell me about your superpowers"

OpenCode 使用自己的插件安装机制。如果你还使用 Claude Code、Codex 或其他运行环境，需要分别为每个环境安装 Superpowers。

## 从旧的软链接安装方式迁移

如果你之前通过 `git clone` 和软链接安装 superpowers，请移除旧配置：

```bash
# Remove old symlinks
rm -f ~/.config/opencode/plugins/superpowers.js
rm -rf ~/.config/opencode/skills/superpowers

# Optionally remove the cloned repo
rm -rf ~/.config/opencode/superpowers

# Remove skills.paths from opencode.json if you added one for superpowers
```

然后按照上面的安装步骤操作。

## 使用方法

使用 OpenCode 原生的 `skill` 工具：

```
use skill tool to list skills
use skill tool to load brainstorming
```

## 更新

OpenCode 通过基于 git 的包规格安装 Superpowers。某些 OpenCode 和 Bun 版本会把解析后的 git 依赖固定在 lockfile 或缓存中，因此仅重启可能无法获取最新的 Superpowers 提交。如果更新没有出现，请清理 OpenCode 的包缓存或重新安装插件。

要固定到特定版本：

```json
{
  "plugin": ["superpowers@git+https://github.com/obra/superpowers.git#v5.0.3"]
}
```

## 故障排查

### 插件未加载

1. 检查日志：`opencode run --print-logs "hello" 2>&1 | grep -i superpowers`
2. 检查 `opencode.json` 中的插件配置行
3. 确认正在使用较新的 OpenCode 版本

### Windows 安装问题

某些 Windows 版 OpenCode 的上游安装器在处理基于 git 的插件规格时存在问题，例如 `git+https` URL 的缓存路径问题，以及即使 `git.exe` 在普通终端中可用，Bun 仍然找不到它。如果 OpenCode 无法安装插件，可以尝试使用系统 npm 安装，然后让 OpenCode 指向本地包：

```powershell
npm install superpowers@git+https://github.com/obra/superpowers.git --prefix "$HOME\.config\opencode"
```

然后在 `opencode.json` 中使用已安装包的路径：

```json
{
  "plugin": ["~/.config/opencode/node_modules/superpowers"]
}
```

### 找不到技能

1. 使用 `skill` 工具列出已发现的技能
2. 检查插件是否已加载（见上文）

### 工具映射

技能以动作描述需求（例如“创建待办事项”“派发子智能体”“读取文件”）。在 OpenCode 中，这些动作对应：

- "Create a todo" / "mark complete in todo list" → `todowrite`
- `Subagent (general-purpose):` 模板 → `task` 工具，并使用 `subagent_type: "general"`（探索代码库时使用 `"explore"`）
- "Invoke a skill" → OpenCode 原生的 `skill` 工具
- "Read a file" → `read`
- "Create a file" / "edit a file" / "delete a file" → `apply_patch`
- "Run a shell command" → `bash`
- "Search file contents" / "find files by name" → `grep`、`glob`
- "Fetch a URL" → `webfetch`

## 获取帮助

- 报告问题：https://github.com/obra/superpowers/issues
- 完整文档：https://github.com/obra/superpowers/blob/main/docs/README.opencode.md
