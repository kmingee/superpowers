---
name: using-git-worktrees
description: 开始需要与当前工作区隔离的功能开发，或执行实现计划之前使用——通过平台原生工具或 git worktree 回退方案确保存在隔离工作区
---

# 使用 Git Worktree

## 概述

确保工作在隔离工作区中进行。优先使用平台原生的 worktree 工具。只有没有原生工具时，才回退到手动 git worktree。

**核心原则：** 先检测是否已经隔离。然后使用原生工具。再回退到 git。绝不要和运行环境对着干。

**开始时声明：**“我正在使用 using-git-worktrees 技能来设置隔离工作区。”

## 第 0 步：检测现有隔离环境

**创建任何东西之前，先检查自己是否已经位于隔离工作区。**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

**子模块防护：** 在 git submodule 中，`GIT_DIR != GIT_COMMON` 同样成立。在得出“已经位于 worktree”这一结论前，先验证当前并不是子模块：

```bash
# If this returns a path, you're in a submodule, not a worktree — treat as normal repo
git rev-parse --show-superproject-working-tree 2>/dev/null
```

**如果 `GIT_DIR != GIT_COMMON`（且不是子模块）：** 你已经位于 linked worktree。直接跳到第 2 步（项目设置）。**不要**再创建另一个 worktree。

根据分支状态报告：
- 位于分支上：“Already in isolated workspace at `<path>` on branch `<name>`.”
- Detached HEAD：“Already in isolated workspace at `<path>` (detached HEAD, externally managed). Branch creation needed at finish time.”

**如果 `GIT_DIR == GIT_COMMON`（或处于子模块）：** 你位于普通仓库 checkout 中。

用户是否已经在指令中说明了 worktree 偏好？如果没有，在创建 worktree 之前先请求同意：

> “Would you like me to set up an isolated worktree? It protects your current branch from changes.”

如果已有明确偏好，直接遵守，不要重复询问。如果用户不同意，就在当前目录工作，并跳到第 2 步。

## 第 1 步：创建隔离工作区

**有两种机制。按以下顺序尝试。**

### 1a. 原生 Worktree 工具（优先）

用户已经在第 0 步同意使用隔离工作区。你当前是否已经有创建 worktree 的方式？它可能叫 `EnterWorktree`、`WorktreeCreate`，也可能是 `/worktree` 命令或 `--worktree` 参数。如果有，使用它，然后跳到第 2 步。

原生工具会自动管理目录位置、分支创建和清理。如果明明有原生工具却使用 `git worktree add`，会产生运行环境无法看见或管理的“幽灵状态”。

只有完全没有原生 worktree 工具时，才继续到第 1b 步。

### 1b. Git Worktree 回退方案

**只有第 1a 步不适用时才使用**——也就是没有任何原生 worktree 工具可用。使用 git 手动创建 worktree。

#### 目录选择

按以下优先级执行。用户明确偏好始终高于观察到的文件系统状态。

1. **检查指令中是否已经声明 worktree 目录偏好。** 如果有，直接使用，无需询问。

2. **检查是否存在项目本地 worktree 目录：**
   ```bash
   ls -d .worktrees 2>/dev/null     # Preferred (hidden)
   ls -d worktrees 2>/dev/null      # Alternative
   ```
   如果找到就使用。如果两者都存在，优先 `.worktrees`。

3. **如果没有其他指导**，默认使用项目根目录的 `.worktrees/`。

#### 安全验证（仅项目本地目录）

**创建 worktree 之前必须验证该目录已被忽略：**

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**如果没有被忽略：** 加入 .gitignore，提交这项修改，然后再继续。

**为什么这很关键：** 防止意外把 worktree 内容提交到仓库。

#### 创建 Worktree

```bash
# Determine path based on chosen location
path="$LOCATION/$BRANCH_NAME"

git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

**沙箱回退：** 如果 `git worktree add` 因权限错误（沙箱拒绝）而失败，告诉用户沙箱阻止了 worktree 创建，你将改为在当前目录工作。然后在当前目录运行设置和基线测试。

## 第 2 步：项目设置

自动检测并运行适当的设置：

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

## 第 3 步：验证干净基线

运行测试，确保工作区从干净状态开始：

```bash
# Use project-appropriate command
npm test / cargo test / pytest / go test ./...
```

**如果测试失败：** 报告失败，并询问是继续还是调查。

**如果测试通过：** 报告准备就绪。

### 报告

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## 快速参考

| 情况 | 操作 |
|-----------|--------|
| 已经位于 linked worktree | 跳过创建（第 0 步） |
| 位于子模块 | 按普通仓库处理（第 0 步防护） |
| 有原生 worktree 工具 | 使用它（第 1a 步） |
| 没有原生工具 | Git worktree 回退（第 1b 步） |
| `.worktrees/` 存在 | 使用它（确认已忽略） |
| `worktrees/` 存在 | 使用它（确认已忽略） |
| 两者都存在 | 使用 `.worktrees/` |
| 两者都不存在 | 检查指令文件，然后默认 `.worktrees/` |
| 目录未被忽略 | 加入 .gitignore + 提交 |
| 创建时出现权限错误 | 使用沙箱回退，在当前目录工作 |
| 基线测试失败 | 报告失败 + 询问 |
| 没有 package.json/Cargo.toml | 跳过依赖安装 |

## 常见合理化借口

| 借口 | 事实 |
|--------|---------|
| “我显然不在 worktree——没必要检查” | 运行第 0 步。运行环境创建的隔离和子模块都会骗过肉眼判断；检测命令能给出答案。 |
| “直接 `git worktree add` 比找原生工具快” | 原生工具（如 `EnterWorktree`）负责位置、分支和清理。绕过它是头号错误——会产生运行环境无法看见或管理的幽灵状态。 |
| “worktree 目录肯定已经被忽略了” | 运行 `git check-ignore`。未忽略的 worktree 目录会把整棵树提交进仓库。 |
| “任何目录名都行” | 明确指令优先于现有项目本地目录，后者又优先于 `.worktrees/` 默认值。 |
| “工作区是新的——基线测试以后再跑也行” | 脏基线会让后续所有失败都变得含糊。现在就运行测试；是否带着失败继续，应由你的人类伙伴决定。 |
