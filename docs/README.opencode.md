# 在 OpenCode 中使用 Superpowers

这是在 [OpenCode.ai](https://opencode.ai) 中使用 Superpowers 的完整指南。

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

### 从旧的软链接安装方式迁移

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

### 查找技能

使用 OpenCode 原生的 `skill` 工具列出所有可用技能：

```
use skill tool to list skills
```

### 加载技能

```
use skill tool to load brainstorming
```

### 个人技能

在 `~/.config/opencode/skills/` 中创建你自己的技能：

```bash
mkdir -p ~/.config/opencode/skills/my-skill
```

创建 `~/.config/opencode/skills/my-skill/SKILL.md`：

```markdown
---
name: my-skill
description: Use when [condition] - [what it does]
---

# My Skill

[Your skill content here]
```

### 项目技能

在项目内的 `.opencode/skills/` 中创建项目专用技能。

**技能优先级：** 项目技能 > 个人技能 > Superpowers 技能

## 更新

OpenCode 通过基于 git 的包规格安装 Superpowers。某些 OpenCode 和 Bun 版本会把解析后的 git 依赖固定在 lockfile 或缓存中，因此仅重启可能无法获取最新的 Superpowers 提交。如果更新没有出现，请清理 OpenCode 的包缓存或重新安装插件。

若要固定到特定版本，可以使用分支或标签：

```json
{
  "plugin": ["superpowers@git+https://github.com/obra/superpowers.git#v5.0.3"]
}
```

## 工作原理

该插件主要做两件事：

1. 通过 `experimental.chat.messages.transform` hook **注入引导上下文**，让每次对话都知道 Superpowers 的存在。
2. 通过 `config` hook **注册技能目录**，让 OpenCode 无需软链接或手动配置即可发现所有 Superpowers 技能。

### 工具映射

技能描述的是动作，而不是把某一个运行时的工具名写死。在 OpenCode 中，这些动作对应：

- "Create a todo" / "mark complete in todo list" → `todowrite`
- `Subagent (general-purpose):` 模板 → OpenCode 的 `task` 工具，并使用 `subagent_type: "general"`（探索代码库时使用 `"explore"`）
- "Invoke a skill" → OpenCode 原生的 `skill` 工具
- "Read a file" → `read`
- "Create a file" / "edit a file" / "delete a file" → `apply_patch`
- "Run a shell command" → `bash`
- "Search file contents" / "find files by name" → `grep`、`glob`
- "Fetch a URL" → `webfetch`

（已对照安装后的 OpenCode CLI 工具清单验证。）

## 故障排查

### 插件未加载

1. 检查 OpenCode 日志：`opencode run --print-logs "hello" 2>&1 | grep -i superpowers`
2. 检查 `opencode.json` 中的插件配置行是否正确
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

1. 使用 OpenCode 的 `skill` 工具列出可用技能
2. 检查插件是否已加载（见上文）
3. 每个技能都需要一个带有效 YAML frontmatter 的 `SKILL.md` 文件

### 没有出现引导信息

1. 检查 OpenCode 版本是否支持 `experimental.chat.messages.transform` hook
2. 修改配置后重启 OpenCode

## 获取帮助

- 报告问题：https://github.com/obra/superpowers/issues
- 主文档：https://github.com/obra/superpowers
- OpenCode 文档：https://opencode.ai/docs/
