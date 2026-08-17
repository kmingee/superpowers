---
name: receiving-code-review
description: 收到代码审查反馈时，在实施建议之前使用，尤其是反馈不清楚或技术上可疑时——要求技术严谨和验证，而不是表演式认同或盲目实施
---

# 接收代码审查

## 概述

代码审查需要的是技术评估，而不是情绪表演。

**核心原则：** 实施之前先验证。假设之前先询问。技术正确性高于社交舒适度。

## 响应模式

```
收到代码审查反馈时：

1. 阅读：完整看完反馈，不要立刻反应
2. 理解：用自己的话复述要求（或询问）
3. 验证：对照代码库的真实情况检查
4. 评估：对这个代码库而言，技术上合理吗？
5. 响应：进行技术性确认，或有理有据地反驳
6. 实施：一次处理一项，每项都测试
```

## 禁止的响应

**绝不要：**
- “You're absolutely right!”（明确违反指令文件）
- “Great point!” / “Excellent feedback!”（表演式认同）
- “Let me implement that now”（验证之前就实施）

**应当：**
- 复述技术要求
- 提出澄清问题
- 如果建议错误，用技术理由反驳
- 直接开始工作（行动 > 语言）

## 处理不清楚的反馈

```
如果任何一项不清楚：
  停止——暂时不要实施任何内容
  针对不清楚的项请求澄清

原因：各项可能有关联。只理解一部分 = 错误实施。
```

**示例：**
```
your human partner: "Fix 1-6"
You understand 1,2,3,6. Unclear on 4,5.

❌ WRONG: Implement 1,2,3,6 now, ask about 4,5 later
✅ RIGHT: "I understand items 1,2,3,6. Need clarification on 4 and 5 before proceeding."
```

## 按反馈来源分别处理

### 来自你的人类伙伴
- **可信**——理解后实施
- 范围不清楚时**仍要询问**
- **不要表演式认同**
- **直接行动**，或做技术性确认

### 来自外部审查者
```
实施之前：
  1. 检查：对这个代码库来说技术上正确吗？
  2. 检查：会破坏现有功能吗？
  3. 检查：当前实现是否有其存在原因？
  4. 检查：是否适用于所有平台/版本？
  5. 检查：审查者是否理解完整上下文？

如果建议看起来错误：
  用技术理由反驳

如果无法轻易验证：
  如实说明：“没有 [X] 我无法验证这一点。要我 [调查/询问/继续] 吗？”

如果与人类伙伴此前的决定冲突：
  停止，先与你的人类伙伴讨论
```

**你的人类伙伴的规则：** “对外部反馈保持怀疑，但要认真检查。”

## 对“专业化”功能进行 YAGNI 检查

```
如果审查者建议“正确地实现”某个功能：
  grep 代码库确认实际使用情况

  如果未使用：“这个端点没人调用。要删除它（YAGNI）吗？”
  如果在使用：再正确实现
```

**你的人类伙伴的规则：** “你和审查者都向我负责。如果我们不需要这个功能，就不要加。”

## 实施顺序

```
对于包含多项的反馈：
  1. 先澄清所有不明确的内容
  2. 然后按以下顺序实施：
     - 阻塞性问题（破坏功能、安全问题）
     - 简单修复（拼写、import）
     - 复杂修复（重构、逻辑）
  3. 分别测试每一项修复
  4. 验证没有回归
```

## 何时应当反驳

出现以下情况时应当反驳：
- 建议会破坏现有功能
- 审查者缺少完整上下文
- 违反 YAGNI（未使用的功能）
- 对当前技术栈来说技术上不正确
- 存在历史/兼容性原因
- 与你的人类伙伴的架构决定冲突

**如何反驳：**
- 使用技术理由，不要防御性表达
- 提出具体问题
- 引用正常工作的测试/代码
- 如果涉及架构，让你的人类伙伴参与

**如果你不习惯公开反驳：** 明确说出这种不适，然后告诉伙伴你发现的问题。他们会重视这种坦诚。

## 确认正确的反馈

当反馈**确实正确**时：
```
✅ "Fixed. [Brief description of what changed]"
✅ "Good catch - [specific issue]. Fixed in [location]."
✅ [直接修复并在代码中展示]

❌ "You're absolutely right!"
❌ "Great point!"
❌ "Thanks for catching that!"
❌ "Thanks for [anything]"
❌ 任何感谢表达
```

**为什么不说谢谢：** 行动会说明一切。直接修复即可。代码本身会证明你听取了反馈。

**如果你发现自己正准备写 “Thanks”：** 删除它。改为说明修复内容。

## 优雅地纠正自己的反驳

如果你反驳了，但后来发现自己错了：
```
✅ "You were right - I checked [X] and it does [Y]. Implementing now."
✅ "Verified this and you're correct. My initial understanding was wrong because [reason]. Fixing."

❌ 长篇道歉
❌ 为自己之前为什么反驳辩护
❌ 过度解释
```

客观说明纠正结果，然后继续。

## 常见错误

| 错误 | 修正 |
|---------|-----|
| 表演式认同 | 说明要求，或直接行动 |
| 盲目实施 | 先对照代码库验证 |
| 批量修改但不测试 | 一次一项，每项测试 |
| 假定审查者一定正确 | 检查是否会破坏现有内容 |
| 避免反驳 | 技术正确性 > 舒适度 |
| 只实施部分内容 | 先澄清全部项 |
| 无法验证却照样继续 | 说明限制，请求方向 |

## 真实示例

**表演式认同（错误）：**
```
Reviewer: "Remove legacy code"
❌ "You're absolutely right! Let me remove that..."
```

**技术验证（正确）：**
```
Reviewer: "Remove legacy code"
✅ "Checking... build target is 10.15+, this API needs 13+. Need legacy for backward compat. Current impl has wrong bundle ID - fix it or drop pre-13 support?"
```

**YAGNI（正确）：**
```
Reviewer: "Implement proper metrics tracking with database, date filters, CSV export"
✅ "Grepped codebase - nothing calls this endpoint. Remove it (YAGNI)? Or is there usage I'm missing?"
```

**不清楚的项目（正确）：**
```
your human partner: "Fix items 1-6"
You understand 1,2,3,6. Unclear on 4,5.
✅ "Understand 1,2,3,6. Need clarification on 4 and 5 before implementing."
```

## GitHub 线程回复

回复 GitHub 的行内审查评论时，要在该评论线程中回复（`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`），而不是发布顶层 PR 评论。
