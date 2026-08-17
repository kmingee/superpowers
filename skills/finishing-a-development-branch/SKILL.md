---
name: finishing-a-development-branch
description: 当实现已经完成、所有测试通过，并需要决定如何集成工作时使用
---

# 完成开发分支

## 概述

**核心原则：** 验证测试 → 检测环境 → 给出选项 → 执行选择 → 清理。

**开始时声明：**“我正在使用 finishing-a-development-branch 技能来完成这项工作。”

## 第 1 步：验证测试

运行项目的完整测试套件（`npm test` / `cargo test` / `pytest` / `go test ./...`）。

**如果测试失败**，报告失败并停止——只有测试全绿后才显示选择菜单：

```
Tests failing (<N> failures). Must fix before completing:

[Show failures]
```

**如果测试通过：** 继续第 2 步。

## 第 2 步：检测环境

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
# Capture now, while still inside the workspace — Step 5 changes directory
# before cleanup (Step 6) needs this value
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

这会决定显示哪个菜单，以及如何清理：

| 状态 | 菜单 | 清理 |
|-------|------|---------|
| `GIT_DIR == GIT_COMMON`（普通仓库） | 标准 3 个选项 | 没有 worktree 需要清理 |
| `GIT_DIR != GIT_COMMON`，有名分支 | 标准 3 个选项 | 基于来源清理（见第 6 步） |
| `GIT_DIR != GIT_COMMON`，detached HEAD | 精简为 2 个选项（不能合并） | 由外部管理——保留原地 |

## 第 3 步：确定基础分支

基础分支是当前工作最初分出来的分支——通常会在计划、对话或当前分支的 upstream 中说明。如果还不知道，请询问：“这个分支看起来是从 <你最合理的猜测> 分出来的——对吗？”合并前必须确认：合并到错误的基础分支后，回退成本很高。

## 第 4 步：给出选项

**普通仓库和有名分支的 worktree——必须准确给出下面 3 个选项：**

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)

Which option?
```

**Detached HEAD——必须准确给出下面 2 个选项：**

```
Implementation complete. You're on a detached HEAD (externally managed workspace).

1. Push as new branch and create a Pull Request
2. Keep as-is (I'll handle it later)

Which option?
```

菜单必须按上面原样提供——简洁，而且每个选项都来自上述列表。只有当你的人类伙伴明确要求丢弃工作时，才进入丢弃路径（见下方“如果你的人类伙伴要求丢弃工作”）。等待他们回答；集成决定属于他们。

## 第 5 步：执行选择

### 选项 1：本地合并

```bash
# Get main repo root for CWD safety
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"

# Merge first — verify success before removing anything
git checkout <base-branch>
git pull
git merge <feature-branch>

# Verify tests on merged result
<test command>
```

如果合并后的结果测试失败：停止，保留 worktree 和分支并调查——此时还没有推送，所以合并仍然只是本地操作，可以恢复。

合并结果确认全绿后：清理 worktree（第 6 步），然后删除分支：

```bash
git branch -d <feature-branch>
```

### 选项 2：推送并创建 PR

```bash
git push -u origin <feature-branch>
# From a detached HEAD, name the new branch on the remote:
# git push origin HEAD:refs/heads/<new-branch>
```

然后使用代码托管平台的工具，以 <base-branch> 为目标创建 pull/merge request——如果有 CLI 就使用 CLI，否则使用大多数平台在 push 时提供的创建 URL——并遵循仓库的 PR 模板和约定（如有）。最后把 URL 报告给你的人类伙伴。

保留 worktree——你的人类伙伴会在那里继续处理 PR 反馈。

### 选项 3：保持现状

报告：“Keeping branch <name>. Worktree preserved at <path>.”

### 如果你的人类伙伴要求丢弃工作

这条路径**只能**作为对明确要求丢弃工作的响应。首先确认：

```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

等待对方准确输入这个确认词。收到后：

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
```

然后清理 worktree（第 6 步），并强制删除分支：

```bash
git branch -D <feature-branch>
```

## 第 6 步：清理工作区

**用于选项 1 和已经确认的丢弃操作。** 选项 2 和 3 始终保留 worktree。两种调用路径都已经切换到主仓库根目录——删除 worktree 必须从 worktree 外部执行——并使用第 2 步在切换目录之前捕获的 `GIT_DIR`/`GIT_COMMON`/`WORKTREE_PATH` 值。

**如果 `GIT_DIR == GIT_COMMON`：** 普通仓库，没有 worktree 需要清理。完成。

**如果 `WORKTREE_PATH` 位于 `.worktrees/` 或 `worktrees/` 下：** 这个 worktree 是 Superpowers 创建的——由我们负责清理：

```bash
git worktree remove "$WORKTREE_PATH"
git worktree prune  # Self-healing: clean up any stale registrations
```

**如果删除被拒绝**（`contains modified or untracked files`）：worktree 中存在其他地方没有的文件——未提交的计划、笔记或临时工作。绝不要擅自使用 `--force`。向你的人类伙伴展示风险并询问：

```bash
git -C "$WORKTREE_PATH" status --porcelain -uall
```

```
Worktree removal refused — these files were never committed:

<file list>

1. Commit them to <branch> before cleanup
2. Move them into <main repo root>
3. Delete them (unrecoverable)

Which?
```

执行所选方案后，再删除 worktree。

**其他情况：** 这个工作区属于宿主环境——保留原地。如果平台提供退出工作区的工具，使用它。

## 快速参考

| 选项 | 合并 | 推送 | 保留 Worktree | 清理分支 |
|--------|-------|------|---------------|----------------|
| 1. 本地合并 | 是 | - | - | 是 |
| 2. 创建 PR | - | 是 | 是 | - |
| 3. 保持现状 | - | - | 是 | - |
| 丢弃（仅明确要求时） | - | - | - | 是（强制） |

## 常见合理化借口

| 借口 | 事实 |
|--------|---------|
| “测试在本次会话前面已经通过了” | 在即将集成的这棵树上重新运行完整测试。一次绿色结果只证明它运行时的那棵树。 |
| “他们显然就是想合并” | 集成是你的人类伙伴的决定。给出菜单并等待。 |
| “他们看起来已经不需要这个功能了——我可以主动提供丢弃选项” | 菜单按原文已经完整。只有你的人类伙伴明确要求丢弃时才丢弃。 |
| “‘好，把它删掉’也算确认” | 只有准确输入 `discard` 才授权删除。 |
| “PR 已经建好了，所以这个 worktree 只是杂物” | PR 反馈要在这个 worktree 中修复。在工作真正落地之前它都要保留。 |
| “另一个 worktree 看起来过期了——顺便一起清理” | 只清理 `.worktrees/` 或 `worktrees/` 下的 worktree。其他都属于宿主环境。 |
| “删除被拒绝——加 `--force` 只是把清理做完” | 拒绝意味着某些文件只存在于该 worktree。`--force` 会永久销毁它们。展示给你的人类伙伴并询问。 |
| “合并结果失败可能只是 flaky” | 合并后的结果只要失败，就停止一切。分支和 worktree 保持原样，先调查。 |
| “基础分支显然就是 main” | 确认分叉点或询问。合并进错误的基础分支，回退代价很高。 |
| “push 被拒绝——force-push 就能解决” | push 被拒绝意味着远端发生了变化。先调查；只有人类伙伴明确要求时才能 force-push。 |
