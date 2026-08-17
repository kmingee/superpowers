# OpenCode 支持设计

**日期：** 2025-11-22
**作者：** Bot & Jesse
**状态：** 设计完成，等待实现

## 概述

通过原生 OpenCode 插件架构为 OpenCode.ai 增加完整的 superpowers 支持，并与现有 Codex 实现共享核心功能。

## 背景

OpenCode.ai 是一个类似 Claude Code 和 Codex 的编程智能体。此前把 superpowers 移植到 OpenCode 的尝试（PR #93、PR #116）使用了文件复制方案。本设计采用不同方法：使用 OpenCode 的 JavaScript/TypeScript 插件系统构建原生插件，同时与 Codex 实现共享代码。

### 平台之间的关键差异

- **Claude Code**：Anthropic 原生插件系统 + 基于文件的 skills
- **Codex**：没有插件系统 → bootstrap markdown + CLI 脚本
- **OpenCode**：JavaScript/TypeScript 插件，带事件 hook 和自定义工具 API

### OpenCode 的 Agent 系统

- **主智能体**：Build（默认、完整权限）和 Plan（受限、只读）
- **子智能体**：General（研究、搜索、多步骤任务）
- **调用方式**：由主智能体自动派发，或手动使用 `@mention` 语法
- **配置**：在 `opencode.json` 或 `~/.config/opencode/agent/` 中定义自定义智能体

## 架构

### 高层结构

1. **共享核心模块**（`lib/skills-core.js`）
   - 通用 skill 发现和解析逻辑
   - 同时供 Codex 和 OpenCode 实现使用

2. **平台专用包装层**
   - Codex：CLI 脚本（`.codex/superpowers-codex`）
   - OpenCode：插件模块（`.opencode/plugin/superpowers.js`）

3. **Skill 目录**
   - 核心：`~/.config/opencode/superpowers/skills/`（或安装位置）
   - 个人：`~/.config/opencode/skills/`（覆盖同名核心 skill）

### 代码复用策略

把 `.codex/superpowers-codex` 中的公共功能提取到共享模块：

```javascript
// lib/skills-core.js
module.exports = {
  extractFrontmatter(filePath),      // Parse name + description from YAML
  findSkillsInDir(dir, maxDepth),    // Recursive SKILL.md discovery
  findAllSkills(dirs),                // Scan multiple directories
  resolveSkillPath(skillName, dirs), // Handle shadowing (personal > core)
  checkForUpdates(repoDir)           // Git fetch/status check
};
```

### Skill Frontmatter 格式

当前格式（没有 `when_to_use` 字段）：

```yaml
---
name: skill-name
description: Use when [condition] - [what it does]; [additional context]
---
```

## OpenCode 插件实现

### 自定义工具

**工具 1：`use_skill`**

把指定 skill 的内容加载到对话中（等价于 Claude 的 Skill 工具）。

```javascript
{
  name: 'use_skill',
  description: 'Load and read a specific skill to guide your work',
  schema: z.object({
    skill_name: z.string().describe('Name of skill (e.g., "superpowers:brainstorming")')
  }),
  execute: async ({ skill_name }) => {
    const { skillPath, content, frontmatter } = resolveAndReadSkill(skill_name);
    const skillDir = path.dirname(skillPath);

    return `# ${frontmatter.name}
# ${frontmatter.description}
# Supporting tools and docs are in ${skillDir}
# ============================================

${content}`;
  }
}
```

**工具 2：`find_skills`**

列出所有可用 skill 及其元数据。

```javascript
{
  name: 'find_skills',
  description: 'List all available skills',
  schema: z.object({}),
  execute: async () => {
    const skills = discoverAllSkills();
    return skills.map(s =>
      `${s.namespace}:${s.name}
  ${s.description}
  Directory: ${s.directory}
`).join('\n');
  }
}
```

### 会话启动 Hook

新会话启动（`session.started` 事件）时：

1. **注入 using-superpowers 内容**
   - using-superpowers skill 的完整内容
   - 建立强制工作流

2. **自动运行 find_skills**
   - 启动时显示完整可用 skill 列表
   - 包含每个 skill 的目录

3. **注入工具映射说明**
   ```markdown
   **Tool Mapping for OpenCode:**
   When skills reference tools you don't have, substitute:
   - `TodoWrite` → `update_plan`
   - `Task` with subagents → Use OpenCode subagent system (@mention)
   - `Skill` tool → `use_skill` custom tool
   - Read, Write, Edit, Bash → Your native equivalents

   **Skill directories contain:**
   - Supporting scripts (run with bash)
   - Additional documentation (read with read tool)
   - Utilities specific to that skill
   ```

4. **检查更新**（非阻塞）
   - 带超时的快速 git fetch
   - 有更新时通知

### 插件结构

```javascript
// .opencode/plugin/superpowers.js
const skillsCore = require('../../lib/skills-core');
const path = require('path');
const fs = require('fs');
const { z } = require('zod');

export const SuperpowersPlugin = async ({ client, directory, $ }) => {
  const superpowersDir = path.join(process.env.HOME, '.config/opencode/superpowers');
  const personalDir = path.join(process.env.HOME, '.config/opencode/skills');

  return {
    'session.started': async () => {
      const usingSuperpowers = await readSkill('using-superpowers');
      const skillsList = await findAllSkills();
      const toolMapping = getToolMappingInstructions();

      return {
        context: `${usingSuperpowers}\n\n${skillsList}\n\n${toolMapping}`
      };
    },

    tools: [
      {
        name: 'use_skill',
        description: 'Load and read a specific skill',
        schema: z.object({
          skill_name: z.string()
        }),
        execute: async ({ skill_name }) => {
          // Implementation using skillsCore
        }
      },
      {
        name: 'find_skills',
        description: 'List all available skills',
        schema: z.object({}),
        execute: async () => {
          // Implementation using skillsCore
        }
      }
    ]
  };
};
```

## 文件结构

```
superpowers/
├── lib/
│   └── skills-core.js           # NEW: Shared skill logic
├── .codex/
│   ├── superpowers-codex        # UPDATED: Use skills-core
│   ├── superpowers-bootstrap.md
│   └── INSTALL.md
├── .opencode/
│   ├── plugin/
│   │   └── superpowers.js       # NEW: OpenCode plugin
│   └── INSTALL.md               # NEW: Installation guide
└── skills/                       # Unchanged
```

## 实现计划

### 阶段 1：重构共享核心

1. 创建 `lib/skills-core.js`
   - 从 `.codex/superpowers-codex` 提取 frontmatter 解析
   - 提取 skill 发现逻辑
   - 提取路径解析（包含覆盖规则）
   - 更新为只使用 `name` 和 `description`（不使用 `when_to_use`）

2. 更新 `.codex/superpowers-codex` 使用共享核心
   - 从 `../lib/skills-core.js` 导入
   - 删除重复代码
   - 保留 CLI 包装逻辑

3. 测试 Codex 实现仍然正常
   - 验证 bootstrap 命令
   - 验证 use-skill 命令
   - 验证 find-skills 命令

### 阶段 2：构建 OpenCode 插件

1. 创建 `.opencode/plugin/superpowers.js`
   - 从 `../../lib/skills-core.js` 导入共享核心
   - 实现插件函数
   - 定义自定义工具（use_skill、find_skills）
   - 实现 session.started hook

2. 创建 `.opencode/INSTALL.md`
   - 安装说明
   - 目录设置
   - 配置指南

3. 测试 OpenCode 实现
   - 验证会话启动 bootstrap
   - 验证 use_skill 工具可用
   - 验证 find_skills 工具可用
   - 验证 skill 目录可访问

### 阶段 3：文档与润色

1. 更新 README，加入 OpenCode 支持
2. 在主文档中加入 OpenCode 安装说明
3. 更新 RELEASE-NOTES
4. 测试 Codex 和 OpenCode 都能正常工作

## 下一步

1. **创建隔离工作区**（使用 git worktrees）
   - 分支：`feature/opencode-support`

2. **适用时遵循 TDD**
   - 测试共享核心函数
   - 测试 skill 发现和解析
   - 为两个平台添加集成测试

3. **增量实现**
   - 阶段 1：重构共享核心 + 更新 Codex
   - 进入下一阶段前验证 Codex 仍然正常
   - 阶段 2：构建 OpenCode 插件
   - 阶段 3：文档和润色

4. **测试策略**
   - 使用真实 OpenCode 安装进行手动测试
   - 验证 skill 加载、目录、脚本是否工作
   - 并排测试 Codex 和 OpenCode
   - 验证工具映射是否正确

5. **PR 和合并**
   - 创建包含完整实现的 PR
   - 在干净环境中测试
   - 合并到 main

## 收益

- **代码复用**：skill 发现/解析只有一个事实来源
- **可维护性**：bug 修复同时作用于两个平台
- **可扩展性**：未来容易增加新平台（Cursor、Windsurf 等）
- **原生集成**：正确使用 OpenCode 插件系统
- **一致性**：所有平台拥有一致的 skill 使用体验
