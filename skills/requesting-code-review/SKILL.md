---
name: requesting-code-review
description: 当完成任务、实现重大功能或准备合并之前，用于验证工作是否符合要求
---

# 请求代码审查

派发一个代码审查子智能体，在问题扩散之前把它们找出来。审查者应获得为评估精确构造的上下文——绝不要把你当前会话的历史交给它。

**核心原则：** 尽早审查，经常审查。

## 何时请求审查

**强制：**
- 子智能体驱动开发中的每一项任务完成后
- 重大功能完成后
- 合并到 main 之前

**可选但很有价值：**
- 卡住时（获得全新视角）
- 重构前（检查基线）
- 修复复杂 bug 后

## 如何请求

**1. 获取 git SHA：**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. 派发代码审查子智能体：**

派发一个 `general-purpose` 子智能体，并填写 [code-reviewer.md](code-reviewer.md) 中的模板。

**占位符：**
- `{DESCRIPTION}` - 你构建内容的简要摘要
- `{PLAN_OR_REQUIREMENTS}` - 它应该完成什么
- `{BASE_SHA}` - 起始提交
- `{HEAD_SHA}` - 结束提交

**3. 处理反馈：**
- 立即修复 Critical 问题
- 继续之前修复 Important 问题
- Minor 问题记录下来以后处理
- 如果审查者错了，用技术理由反驳

## 示例

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch code reviewer subagent]
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types
  PLAN_OR_REQUIREMENTS: Task 2 from docs/superpowers/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## 常见合理化借口

| 借口 | 事实 |
|--------|---------|
| “我自己看一下 diff 就行，不用派审查者” | 你是协调者——在当前上下文里审 diff 会消耗继续驱动工作的上下文窗口。派一个审查子智能体：diff 和评估留在它的上下文中，只把发现带回来。 |
| “审查者需要我整段会话历史才能理解改动” | 给它精确构造的上下文，绝不要给会话历史。这样审查者会聚焦工作产物，而不是你的思考过程。 |

## 危险信号

**绝不要：**
- 因为“很简单”就跳过审查
- 忽略 Critical 问题
- Important 问题未修复就继续
- 与有效的技术反馈争辩

**如果审查者错了：**
- 用技术理由反驳
- 展示证明代码有效的代码/测试
- 请求澄清

模板见：[code-reviewer.md](code-reviewer.md)
