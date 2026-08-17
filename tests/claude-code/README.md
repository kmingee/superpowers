# Claude Code 技能测试

使用 Claude Code CLI 对 superpowers 技能进行自动化测试。

## 概述

这套测试验证技能能否正确加载，以及 Claude 是否会按预期遵循技能。测试以无头模式（`claude -p`）调用 Claude Code 并验证行为。

## 要求

- 已安装 Claude Code CLI 且位于 PATH 中（`claude --version` 应可运行）
- 已安装本地 superpowers 插件（安装方法见主 README）

## 运行测试

### 运行全部快速测试（推荐）：
```bash
./run-skill-tests.sh
```

### 运行集成测试（较慢，10–30 分钟）：
```bash
./run-skill-tests.sh --integration
```

### 运行指定测试：
```bash
./run-skill-tests.sh --test test-subagent-driven-development.sh
```

### 使用详细输出：
```bash
./run-skill-tests.sh --verbose
```

### 设置自定义超时：
```bash
./run-skill-tests.sh --timeout 1800  # 30 minutes for integration tests
```

## 测试结构

### test-helpers.sh
技能测试的公共函数：
- `run_claude "prompt" [timeout]` - 使用提示词运行 Claude
- `assert_contains output pattern name` - 验证模式存在
- `assert_not_contains output pattern name` - 验证模式不存在
- `assert_count output pattern count name` - 验证精确数量
- `assert_order output pattern_a pattern_b name` - 验证顺序
- `create_test_project` - 创建临时测试目录
- `create_test_plan project_dir` - 创建示例计划文件

### 测试文件

每个测试文件都会：
1. Source `test-helpers.sh`
2. 使用特定提示词运行 Claude Code
3. 使用断言验证预期行为
4. 成功返回 0，失败返回非零值

## 测试示例

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

echo "=== Test: My Skill ==="

# Ask Claude about the skill
output=$(run_claude "What does the my-skill skill do?" 30)

# Verify response
assert_contains "$output" "expected behavior" "Skill describes behavior"

echo "=== All tests passed ==="
```

## 当前测试

### 快速测试（默认运行）

#### test-subagent-driven-development.sh
测试技能内容和要求（约 2 分钟）：
- 技能加载和可访问性
- 工作流顺序（规格符合性审查先于代码质量审查）
- 是否记录了自我审查要求
- 是否记录了计划读取效率要求
- 是否记录了规格符合性 reviewer 的怀疑性要求
- 是否记录了审查循环
- 是否记录了任务上下文提供方式

### 集成测试（使用 --integration）

#### test-subagent-driven-development-integration.sh
完整工作流执行测试（约 10–30 分钟）：
- 创建带 Node.js 设置的真实测试项目
- 创建包含 2 项任务的实现计划
- 使用 subagent-driven-development 执行计划
- 验证实际行为：
  - 计划只在开始时读取一次（而不是每项任务都读）
  - 子智能体提示词中提供完整任务文本
  - 子智能体报告前执行自我审查
  - 规格符合性审查先于代码质量审查
  - 规格 reviewer 独立读取代码
  - 生成可工作的实现
  - 测试通过
  - 创建正确的 git 提交

**它测试什么：**
- 工作流能否真正端到端运行
- 我们的改进是否真正被应用
- 子智能体是否正确遵循技能
- 最终代码是否可用并经过测试

#### test-worktree-native-preference.sh
using-git-worktrees 技能的 RED-GREEN-REFACTOR 验证（约 5 分钟）：
- RED：没有 Step 1a 的技能——智能体应使用 `git worktree add`
- GREEN：包含 Step 1a 的技能——智能体应使用原生 EnterWorktree 工具
- PRESSURE：与 GREEN 相同，但增加紧急措辞，并预先存在 `.worktrees/`
- Drill 场景 `worktree-creation-under-pressure.yaml` 只覆盖 PRESSURE 阶段

## 添加新测试

1. 创建新测试文件：`test-<skill-name>.sh`
2. Source test-helpers.sh
3. 使用 `run_claude` 和断言编写测试
4. 把测试加入 `run-skill-tests.sh` 的测试列表
5. 设置可执行权限：`chmod +x test-<skill-name>.sh`

## 超时注意事项

- 默认超时：每项测试 5 分钟
- Claude Code 可能需要一些时间响应
- 需要时可通过 `--timeout` 调整
- 测试应保持聚焦，避免运行时间过长

## 调试失败测试

使用 `--verbose` 可以看到完整 Claude 输出：
```bash
./run-skill-tests.sh --verbose --test test-subagent-driven-development.sh
```

不使用 verbose 时，只有失败才显示输出。

## CI/CD 集成

在 CI 中运行：
```bash
# Run with explicit timeout for CI environments
./run-skill-tests.sh --timeout 900

# Exit code 0 = success, non-zero = failure
```

## 说明

- 测试主要验证技能*指令*，而不是完整执行过程
- 完整工作流测试会非常慢
- 聚焦验证关键技能要求
- 测试应该是确定性的
- 避免测试实现细节
