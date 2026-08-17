# 限定范围的复审提示词模板

在一轮修复之后派发复审时使用此模板。复审者验证之前发现的问题是否已处理，并检查修复 diff 是否引入新的破坏。它不是一次全新审查——完整审查之前已经做过。

**目的：** 验证上一次审查的每个发现都已处理，并确认修复本身没有破坏任何东西。

```
Subagent (general-purpose):
  description: "Re-review Task N fix round R"
  model: [MODEL — 必填：根据 SKILL.md 的 Model Selection 选择；如果省略，
         会静默继承当前会话中最昂贵的模型]
  prompt: |
    你正在复审某一任务的一轮修复。前一次审查产生了一组发现；实现者已经尝试修复它们。
    你的工作只有两件事：逐项给出结论，并检查修复 diff——除此之外不要做任何事。

    ## 任务

    阅读任务简报：[BRIEF_FILE]

    ## 需要验证的发现

    [FINDINGS]

    ## 修复

    阅读实现者报告（修复报告会追加在文件末尾）：
    [REPORT_FILE]

    **Fix base:** [FIX_BASE_SHA]（上一次审查看到的 head）
    **Head:** [HEAD_SHA]
    **Diff file:** [DIFF_FILE]

    只读一次 diff 文件——它包含修复提交、stat 摘要和带上下文的修复 diff。
    不要重新运行 git 命令。如果 diff 文件缺失，自己获取：
    `git diff --stat [FIX_BASE_SHA]..[HEAD_SHA]` 和
    `git diff [FIX_BASE_SHA]..[HEAD_SHA]`。

    你对这个 checkout 的审查是只读的。不要以任何方式修改工作树、index、HEAD 或分支状态。

    ## 你不要派发子智能体

    全部审查由你自己完成。绝不要 spawn 子智能体审查 diff 的一部分，
    也绝不要再 spawn reviewer 获取第二意见。这个流程已经提供了全部审查席位；
    你自己派出的 reviewer 只是以完整成本重复其中一个席位，而且它的结论不算数。
    如果 diff 太大，一次看不完，就自己分多轮审查，并在报告中说明。

    ## 范围

    你的范围只有“发现列表”和“修复 diff”。每个发现都必须给出结论。
    检查修复 diff 是否引入了新的问题。**不要**重新审查修复未触碰的代码：
    如果注意到完全位于修复 diff 之外的问题，把它放在 Out-of-Scope Observations 下——
    它不阻塞当前任务，也不延长修复循环。所有任务完成后还会进行整分支的广泛审查。

    ## 测试

    实现者已经重新运行了覆盖修改代码的测试，并把结果追加到报告文件。
    把报告视为未经验证的声明：确认修复报告明确列出了覆盖测试并展示输出，
    再对照 diff 验证这些声明。不要为了确认报告而重新运行整个测试套件。
    只有当阅读代码产生一个现有测试结果无法回答的具体疑问时，才运行测试——
    并且只运行聚焦测试，绝不要运行包级完整套件。

    ## 输出格式

    最终消息本身就是报告：直接从第一个发现的结论开始。
    每一行都只能是结论、带 file:line 的发现，或你执行的检查——不要前言，也不要过程叙述。

    ### Finding Verdicts

    按顺序处理“需要验证的发现”中的每一项：
    - **[finding one-liner]** — ADDRESSED | NOT ADDRESSED，并附 file:line 证据。
      “尝试过”不等于已解决：具体缺陷必须已经不存在。

    ### New Breakage in the Fix Diff

    修复本身破坏或引入的任何问题，注明严重度（Critical/Important/Minor）和 file:line。
    如果没有，写 “None”。

    ### Out-of-Scope Observations

    你注意到的、完全位于修复 diff 之外的问题。它们不阻塞当前任务；控制器会把这些记录到最终审查台账。
    如果没有，写 “None”。

    ### Verdict

    **Fix round:** [All findings addressed, no new Critical/Important
    breakage | Findings remain open] — 列出仍未解决的项。
```

**占位符：**
- `[MODEL]` — 必填：按照 SKILL.md Model Selection 选择 reviewer 模型；对小修复 diff 的限定复审使用低到中档模型
- `[BRIEF_FILE]` — 任务简报文件（与实现者使用的是同一文件）
- `[FINDINGS]` — 上一次审查中的 Critical/Important 发现和规格缺口，逐条原样复制
- `[REPORT_FILE]` — 实现者报告文件（修复报告追加在末尾）
- `[FIX_BASE_SHA]` — 上一次审查看到的 head
- `[HEAD_SHA]` — 当前提交
- `[DIFF_FILE]` — `scripts/review-package PLAN_FILE FIX_BASE HEAD` 输出的路径

**复审者返回：** 每个发现的结论（ADDRESSED / NOT ADDRESSED）、修复 diff 中的新破坏、范围外观察，以及本轮结论。
