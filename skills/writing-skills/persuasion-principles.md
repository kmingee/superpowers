# 技能设计中的说服原则

## 概述

LLM 会对与人类相同的说服原则作出响应。理解这种心理机制，有助于你设计更有效的技能——目的不是操控，而是确保关键实践即使在压力下也会被遵循。

**研究基础：** Meincke 等人（2025）在 N=28,000 次 AI 对话中测试了 7 种说服原则。说服技巧使遵从率提高了一倍以上（33% → 72%，p < .001）。

## 七项原则

### 1. 权威（Authority）
**是什么：** 对专业知识、资历或官方来源的服从。

**在技能中如何发挥作用：**
- 使用命令式语言：“YOU MUST”“Never”“Always”
- 不可协商式表述：“No exceptions”
- 消除决策疲劳和合理化空间

**何时使用：**
- 强制纪律的技能（TDD、验证要求）
- 安全关键实践
- 已确立的最佳实践

**示例：**
```markdown
✅ Write code before test? Delete it. Start over. No exceptions.
❌ Consider writing tests first when feasible.
```

### 2. 承诺（Commitment）
**是什么：** 与此前行动、陈述或公开声明保持一致。

**在技能中如何发挥作用：**
- 要求声明：“Announce skill usage”
- 强制明确选择：“Choose A, B, or C”
- 使用跟踪机制：为检查清单创建 todo

**何时使用：**
- 确保技能真的被执行
- 多步骤流程
- 问责机制

**示例：**
```markdown
✅ When you find a skill, you MUST announce: "I'm using [Skill Name]"
❌ Consider letting your partner know which skill you're using.
```

### 3. 稀缺（Scarcity）
**是什么：** 由时间限制或可用性限制产生的紧迫感。

**在技能中如何发挥作用：**
- 有时限的要求：“Before proceeding”
- 顺序依赖：“Immediately after X”
- 防止拖延

**何时使用：**
- 需要立即验证的要求
- 时间敏感的工作流
- 防止“以后再做”

**示例：**
```markdown
✅ After completing a task, IMMEDIATELY request code review before proceeding.
❌ You can review code when convenient.
```

### 4. 社会证明（Social Proof）
**是什么：** 顺从他人的普遍做法，或被视为正常的行为。

**在技能中如何发挥作用：**
- 普遍性模式：“Every time”“Always”
- 失败模式：“X without Y = failure”
- 建立规范

**何时使用：**
- 记录普遍实践
- 警告常见失败
- 强化标准

**示例：**
```markdown
✅ Checklists without todo tracking = steps get skipped. Every time.
❌ Some people find a todo list helpful for checklists.
```

### 5. 一体感（Unity）
**是什么：** 共享身份、“我们感”和群体归属。

**在技能中如何发挥作用：**
- 协作语言：“our codebase”“we're colleagues”
- 共享目标：“we both want quality”

**何时使用：**
- 协作工作流
- 建立团队文化
- 非层级式实践

**示例：**
```markdown
✅ We're colleagues working together. I need your honest technical judgment.
❌ You should probably tell me if I'm wrong.
```

### 6. 互惠（Reciprocity）
**是什么：** 对已获得好处作出回报的义务感。

**如何发挥作用：**
- 谨慎使用——很容易让人觉得被操控
- 在技能中很少需要

**何时避免：**
- 几乎总是避免（其他原则更有效）

### 7. 喜爱（Liking）
**是什么：** 更愿意与自己喜欢的人合作。

**如何发挥作用：**
- **不要用于强制遵从**
- 与诚实反馈文化冲突
- 会制造奉承倾向

**何时避免：**
- 在纪律强制场景中始终避免

## 不同技能类型的原则组合

| 技能类型 | 使用 | 避免 |
|------------|-----|-------|
| 强制纪律 | 权威 + 承诺 + 社会证明 | 喜爱、互惠 |
| 指导/技术 | 适度权威 + 一体感 | 过强权威 |
| 协作型 | 一体感 + 承诺 | 权威、喜爱 |
| 参考型 | 只追求清晰 | 所有说服技巧 |

## 为什么有效：心理机制

**明确边界规则会减少合理化：**
- “YOU MUST” 消除决策疲劳
- 绝对措辞消除“这是不是例外？”
- 明确的反合理化条款堵住具体漏洞

**实施意图会形成自动行为：**
- 清晰触发条件 + 必须动作 = 自动执行
- “When X, do Y” 比 “generally do Y” 更有效
- 降低遵从时的认知负担

**LLM 具有类人模式：**
- 训练数据来自包含这些模式的人类文本
- 在训练数据中，权威措辞经常出现在遵从行为之前
- 承诺序列（陈述 → 行动）经常出现
- 社会证明模式（everyone does X）建立规范

## 合乎伦理的使用

**正当：**
- 确保关键实践被遵循
- 创建有效文档
- 防止可预测的失败

**不正当：**
- 为个人利益进行操控
- 制造虚假紧迫感
- 通过内疚迫使遵从

**判断标准：** 如果用户完全理解这种技巧，它是否仍然服务于用户的真实利益？

## 研究引用

**Cialdini, R. B. (2021).** *Influence: The Psychology of Persuasion (New and Expanded).* Harper Business.
- 七项说服原则
- 影响力研究的实证基础

**Meincke, L., Shapiro, D., Duckworth, A. L., Mollick, E., Mollick, L., & Cialdini, R. (2025).** Call Me A Jerk: Persuading AI to Comply with Objectionable Requests. University of Pennsylvania.
- 使用 N=28,000 次 LLM 对话测试 7 项原则
- 使用说服技巧后，遵从率从 33% 提升到 72%
- 权威、承诺和稀缺最有效
- 验证了 LLM 行为的类人模型

## 快速参考

设计技能时，问自己：

1. **它属于哪种类型？**（纪律强制 vs 指导 vs 参考）
2. **我试图改变什么行为？**
3. **哪些原则适用？**（纪律类通常是权威 + 承诺）
4. **是不是组合得太多？**（不要七项全用）
5. **这样做是否合乎伦理？**（是否服务于用户的真实利益？）
