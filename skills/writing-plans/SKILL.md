---
name: writing-plans
description: 当你已有多步骤任务的规格或要求，并且还没有开始修改代码时使用
---

# 编写计划

## 概述

编写完整的实现计划，并假设执行计划的工程师对我们的代码库毫无上下文，而且审美和判断力都值得怀疑。把他们需要知道的一切都写清楚：每项任务要修改哪些文件、具体代码、测试、可能需要查阅的文档、怎样验证。把整份计划拆成足够小的任务。遵循 DRY、YAGNI、TDD，并频繁提交。

假设他们是有能力的开发者，但几乎不了解我们的工具集或问题领域。还要假设他们并不擅长良好的测试设计。

**开始时声明：**“我正在使用 writing-plans 技能来创建实现计划。”

**上下文：** 如果执行时需要隔离 worktree，应在执行阶段通过 `superpowers:using-git-worktrees` 技能创建。

**计划保存到：** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
- （如果用户对计划位置有偏好，以用户偏好为准）

## 范围检查

如果规格覆盖多个彼此独立的子系统，那么在 brainstorming 阶段本应拆成多个子项目规格。如果还没有拆，建议拆成多个独立计划——每个子系统一份。每份计划都应该能单独产出可工作、可测试的软件。

## 文件结构

定义任务之前，先画出会创建或修改哪些文件，以及每个文件负责什么。这里就是正式锁定拆分边界的地方。

- 设计边界清晰、接口定义明确的单元。每个文件应只有一个清晰职责。
- 你对一次能完整放入上下文的代码推理得最好；文件职责越专注，你的编辑越可靠。优先选择小而专注的文件，不要让单文件承担太多职责。
- 经常一起变化的文件应该放在一起。按职责拆分，而不是按技术层拆分。
- 在现有代码库中遵循已有模式。如果代码库本来就使用大文件，不要擅自做全面重构——但如果你本来就要修改的文件已经变得难以维护，把合理拆分纳入计划是可以的。

这份结构图会反过来指导任务拆分。每个任务都应该产生一个独立合理、自包含的改动。

## 任务大小

任务是最小的工作单元：它拥有自己的测试循环，并值得单独通过一个全新 reviewer 的关卡。划分任务边界时，把 setup、配置、脚手架和文档步骤并入真正需要这些内容的交付任务；只有当 reviewer 可以合理地拒绝一个任务而批准旁边另一个任务时，才拆成多个任务。每个任务结束时都必须产出可独立测试的交付物。

## 足够小的步骤粒度

**每一步只做一个动作（2–5 分钟）：**
- “编写失败测试”——一步
- “运行测试，确认它失败”——一步
- “编写让测试通过的最少代码”——一步
- “运行测试并确认通过”——一步
- “提交”——一步

## 计划文档头部

**每份计划都必须以下面的头部开始：**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [用一句话描述要构建什么]

**Architecture:** [用 2–3 句话描述方案]

**Tech Stack:** [关键技术/库]

**Spec:** [本计划实现的规格/设计文档路径——计划从规格中论证，因此规格必须与计划一起传递；执行者两者都要读]

## Global Constraints

[规格中对整个项目都适用的要求——最低版本、依赖限制、命名和文案规则、平台要求——每项一行；精确值逐字从规格复制。每项任务的要求都隐式包含这一节。]

---
```

## 任务结构

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Interfaces:**
- Consumes: [本任务使用先前任务产出的什么——写出精确签名]
- Produces: [后续任务依赖什么——写出精确函数名、参数和返回类型。一个任务的 implementer 只会看到自己的任务；这里告诉它相邻任务使用的名称和类型。]

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## 不允许使用占位内容

每一步都必须包含工程师实际需要的内容。下面这些都属于**计划失败**——绝不要这样写：
- “TBD”“TODO”“以后实现”“稍后补充细节”
- “添加适当的错误处理” / “增加验证” / “处理边界情况”
- “为上面的内容写测试”（但不给实际测试代码）
- “与 Task N 类似”（把代码重复写出来——工程师可能不按顺序阅读任务）
- 只描述做什么、却不展示怎么做的步骤（代码步骤必须有代码块）
- 引用任何任务都没有定义的类型、函数或方法

## 自我审查

完整计划写完后，用新的视角重新看规格，并对照计划进行检查。这是一份由你自己执行的检查清单——不是子智能体派发。

**1. 规格覆盖：** 快速浏览规格里的每一节/每项要求。你能指出由哪个任务实现吗？列出所有缺口。

**2. 占位符扫描：** 搜索计划中的危险信号——上方“不允许使用占位内容”列出的任何模式。发现就修。

**3. 类型一致性：** 后续任务中使用的类型、方法签名和属性名，是否与前面任务中的定义完全一致？如果 Task 3 写的是 `clearLayers()`，而 Task 7 写成 `clearFullLayers()`，那就是 bug。

发现问题直接内联修复。无需再次审查——修好后继续。如果发现某项规格要求没有任何任务覆盖，添加对应任务。

## 执行交接

保存计划后，提供执行方式选择：

**“计划已经完成并保存到 `docs/superpowers/plans/<filename>.md`。有两种执行方式：**

**1. Subagent-Driven（推荐）** - 我为每项任务派一个全新子智能体，任务之间进行审查，快速迭代

**2. Inline Execution** - 在当前会话中使用 executing-plans 执行任务，分批执行并设置检查点

**选择哪一种？”**

**如果选择 Subagent-Driven：**
- **必需的子技能：** 使用 superpowers:subagent-driven-development
- 每任务全新子智能体 + 两阶段审查

**如果选择 Inline Execution：**
- **必需的子技能：** 使用 superpowers:executing-plans
- 分批执行，并设置审查检查点
