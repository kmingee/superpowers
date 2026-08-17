# 技能编写最佳实践

> 学习如何编写让智能体能够发现并成功使用的有效技能。

好的技能简洁、结构良好，并经过真实使用测试。本指南提供实用的编写决策，帮助你编写智能体能够发现并有效使用的技能。

关于技能如何工作的概念背景，请参阅 [Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)。

## 核心原则

### 简洁是关键

[上下文窗口](https://platform.claude.com/docs/en/build-with-claude/context-windows)是一项公共资源。你的技能与智能体需要知道的所有其他内容共享上下文窗口，包括：

* 系统提示
* 对话历史
* 其他技能的元数据
* 用户的实际请求

并不是技能里的每个 token 都会立即产生成本。启动时，只会预加载所有技能的元数据（name 和 description）。只有当技能变得相关时，智能体才会读取 SKILL.md，并且只会按需读取额外文件。不过，让 SKILL.md 保持简洁仍然很重要：一旦智能体加载它，每个 token 都会与对话历史和其他上下文争夺空间。

**默认假设**：智能体已经非常聪明

只添加智能体原本不知道的上下文。审视每一段信息：

* “智能体真的需要这段解释吗？”
* “我能否假设智能体已经知道这个？”
* “这段话是否值得占用这些 token？”

**好示例：简洁**（约 50 token）：

````markdown  theme={null}
## 提取 PDF 文本

使用 pdfplumber 提取文本：

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
````

**差示例：过于冗长**（约 150 token）：

```markdown  theme={null}
## 提取 PDF 文本

PDF（Portable Document Format，便携式文档格式）是一种常见文件格式，
其中包含文本、图像和其他内容。要从 PDF 中提取文本，你需要使用一个库。
有许多 PDF 处理库可供选择，但我们推荐 pdfplumber，因为它易于使用，
并且能很好地处理大多数情况。首先，你需要使用 pip 安装它。然后可以使用下面的代码……
```

简洁版本假设智能体已经知道 PDF 是什么，也知道库如何工作。

### 设置适当的自由度

让具体程度与任务的脆弱性和变化程度相匹配。

**高自由度**（文字指令）：

适用于：

* 多种方法都有效
* 决策依赖上下文
* 由启发式原则指导方法选择

示例：

```markdown  theme={null}
## 代码审查流程

1. 分析代码结构和组织方式
2. 检查潜在 bug 或边界情况
3. 提出可读性和可维护性改进建议
4. 验证是否符合项目约定
```

**中等自由度**（伪代码或带参数脚本）：

适用于：

* 存在首选模式
* 可以接受一定变化
* 配置会影响行为

示例：

````markdown  theme={null}
## 生成报告

使用此模板，并按需自定义：

```python
def generate_report(data, format="markdown", include_charts=True):
    # 处理数据
    # 按指定格式生成输出
    # 可选地包含可视化
```
````

**低自由度**（具体脚本，很少或没有参数）：

适用于：

* 操作脆弱且容易出错
* 一致性至关重要
* 必须遵循特定顺序

示例：

````markdown  theme={null}
## 数据库迁移

严格运行此脚本：

```bash
python scripts/migrate.py --verify --backup
```

不要修改命令，也不要添加额外参数。
````

**类比**：把智能体想象成沿路径探索的机器人：

* **两侧都是悬崖的窄桥**：只有一种安全前进方式。提供明确护栏和精确指令（低自由度）。例如：必须严格按顺序运行的数据库迁移。
* **没有危险的开阔地**：很多路线都能成功。给出总体方向，并相信智能体会找到最优路径（高自由度）。例如：最佳方案取决于上下文的代码审查。

### 使用你计划采用的所有模型进行测试

技能相当于对模型的补充，因此效果取决于底层模型。请用你计划使用的每种模型测试技能。

**不同模型的测试重点**：

* **Claude Haiku**（快速、经济）：技能是否提供了足够指导？
* **Claude Sonnet**（均衡）：技能是否清晰且高效？
* **Claude Opus**（推理能力强）：技能是否避免过度解释？

对 Opus 完美有效的内容，对 Haiku 可能需要更多细节。如果计划跨多个模型使用技能，应争取让指令在所有模型上都表现良好。

## 技能结构

<Note>
  **YAML Frontmatter**：SKILL.md 的 frontmatter 需要两个字段：

  * `name` - 技能的人类可读名称（最多 64 个字符）
  * `description` - 描述技能做什么以及何时使用的一行文字（最多 1024 个字符）

  完整技能结构请参阅 [Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#skill-structure)。
</Note>

### 命名约定

使用一致的命名模式，让技能更容易引用和讨论。我们推荐使用**动名词形式**（动词 + -ing）作为技能名称，因为这能清楚表达技能提供的活动或能力。

**好的命名示例（动名词）：**

* "Processing PDFs"
* "Analyzing spreadsheets"
* "Managing databases"
* "Testing code"
* "Writing documentation"

**可以接受的替代形式：**

* 名词短语："PDF Processing"、"Spreadsheet Analysis"
* 动作导向："Process PDFs"、"Analyze Spreadsheets"

**避免：**

* 模糊名称："Helper"、"Utils"、"Tools"
* 过于泛化："Documents"、"Data"、"Files"
* 同一技能集合中使用不一致的命名模式

一致命名可以帮助你：

* 在文档和对话中引用技能
* 一眼理解技能用途
* 组织和搜索多个技能
* 维护专业且一致的技能库

### 编写有效的 description

`description` 字段用于技能发现，应同时包含技能做什么，以及何时使用。

<Warning>
  **始终使用第三人称**。description 会被注入系统提示中，不一致的人称视角可能造成发现问题。

  * **好：** "Processes Excel files and generates reports"
  * **避免：** "I can help you process Excel files"
  * **避免：** "You can use this to process Excel files"
</Warning>

**要具体，并包含关键术语。** 同时写明技能做什么，以及何时使用的具体触发条件/上下文。

每个技能只有一个 description 字段。它对技能选择至关重要：智能体可能要从 100 多个技能中挑出正确的一个。description 必须提供足够信息，让智能体知道什么时候应该选择此技能；SKILL.md 的其余内容则负责实现细节。

有效示例：

**PDF Processing 技能：**

```yaml  theme={null}
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Excel Analysis 技能：**

```yaml  theme={null}
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.
```

**Git Commit Helper 技能：**

```yaml  theme={null}
description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
```

避免这种模糊描述：

```yaml  theme={null}
description: Helps with documents
```

```yaml  theme={null}
description: Processes data
```

```yaml  theme={null}
description: Does stuff with files
```

### 渐进式披露模式

SKILL.md 作为概览，按需指向详细材料，就像入门指南中的目录。有关渐进式披露如何工作，请参阅概览中的 [How Skills work](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work)。

**实用指南：**

* 为获得最佳效果，让 SKILL.md 正文保持在 500 行以内
* 接近此限制时，把内容拆成独立文件
* 使用下面的模式有效组织指令、代码和资源

#### 可视化概览：从简单到复杂

基础技能只需要一个包含元数据和指令的 SKILL.md 文件：

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=87782ff239b297d9a9e8e1b72ed72db9" alt="Simple SKILL.md file showing YAML frontmatter and markdown body" data-og-width="2048" width="2048" data-og-height="1153" height="1153" data-path="images/agent-skills-simple-file.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=c61cc33b6f5855809907f7fda94cd80e 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=90d2c0c1c76b36e8d485f49e0810dbfd 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=ad17d231ac7b0bea7e5b4d58fb4aeabb 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=f5d0a7a3c668435bb0aee9a3a8f8c329 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=0e927c1af9de5799cfe557d12249f6e6 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=46bbb1a51dd4c8202a470ac8c80a893d 2500w" />

随着技能增长，可以捆绑其他内容，让智能体仅在需要时加载：

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=a5e0aa41e3d53985a7e3e43668a33ea3" alt="Bundling additional reference files like reference.md and forms.md." data-og-width="2048" width="2048" data-og-height="1327" height="1327" data-path="images/agent-skills-bundling-content.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=f8a0e73783e99b4a643d79eac86b70a2 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=dc510a2a9d3f14359416b706f067904a 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=82cd6286c966303f7dd914c28170e385 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=56f3be36c77e4fe4b523df209a6824c6 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=d22b5161b2075656417d56f41a74f3dd 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=3dd4bdd6850ffcc96c6c45fcb0acd6eb 2500w" />

完整技能目录可能如下：

```
pdf/
├── SKILL.md              # 主指令（触发时加载）
├── FORMS.md              # 表单填写指南（按需加载）
├── reference.md          # API 参考（按需加载）
├── examples.md           # 使用示例（按需加载）
└── scripts/
    ├── analyze_form.py   # 工具脚本（执行，不加载）
    ├── fill_form.py      # 表单填写脚本
    └── validate.py       # 校验脚本
```

#### 模式 1：高层指南 + 参考文件

````markdown  theme={null}
---
name: PDF Processing
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---

# PDF Processing

## Quick start

使用 pdfplumber 提取文本：
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Advanced features

**Form filling**: See [FORMS.md](FORMS.md) for complete guide
**API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
**Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
````

智能体只会在需要时加载 FORMS.md、REFERENCE.md 或 EXAMPLES.md。

#### 模式 2：按领域组织

对于跨多个领域的技能，按领域组织内容，避免加载无关上下文。当用户询问销售指标时，智能体只需要读取销售相关 schema，而不必加载财务或营销数据。这样可以减少 token 使用，并让上下文保持聚焦。

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

````markdown SKILL.md theme={null}
# BigQuery Data Analysis

## Available datasets

**Finance**: Revenue, ARR, billing → See [reference/finance.md](reference/finance.md)
**Sales**: Opportunities, pipeline, accounts → See [reference/sales.md](reference/sales.md)
**Product**: API usage, features, adoption → See [reference/product.md](reference/product.md)
**Marketing**: Campaigns, attribution, email → See [reference/marketing.md](reference/marketing.md)

## Quick search

使用 grep 查找具体指标：

```bash
grep -i "revenue" reference/finance.md
grep -i "pipeline" reference/sales.md
grep -i "api usage" reference/product.md
```
````

#### 模式 3：条件式细节

展示基础内容，并链接到高级内容：

```markdown  theme={null}
# DOCX Processing

## Creating documents

新建文档使用 docx-js。参见 [DOCX-JS.md](DOCX-JS.md)。

## Editing documents

简单编辑直接修改 XML。

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

只有当用户需要这些功能时，智能体才会读取 REDLINING.md 或 OOXML.md。

### 避免深层嵌套引用

当一个被引用文件再引用其他文件时，智能体可能只会部分读取后续文件。遇到嵌套引用时，它可能使用 `head -100` 等命令预览，而不是读取完整文件，从而获得不完整信息。

**让引用距离 SKILL.md 只有一层。** 所有参考文件都应直接从 SKILL.md 链接，确保需要时智能体会完整读取。

**差示例：层级过深：**

```markdown  theme={null}
# SKILL.md
See [advanced.md](advanced.md)...

# advanced.md
See [details.md](details.md)...

# details.md
Here's the actual information...
```

**好示例：只有一层：**

```markdown  theme={null}
# SKILL.md

**Basic usage**: [instructions in SKILL.md]
**Advanced features**: See [advanced.md](advanced.md)
**API reference**: See [reference.md](reference.md)
**Examples**: See [examples.md](examples.md)
```

### 为较长参考文件提供目录

对超过 100 行的参考文件，在顶部加入目录。这样即使智能体只做部分预览，也能看到可用信息的完整范围。

**示例：**

```markdown  theme={null}
# API Reference

## Contents
- Authentication and setup
- Core methods (create, read, update, delete)
- Advanced features (batch operations, webhooks)
- Error handling patterns
- Code examples

## Authentication and setup
...

## Core methods
...
```

随后智能体可以完整读取文件，或按需跳到特定章节。

关于这种基于文件系统的架构如何实现渐进式披露，参见下方高级部分中的 [Runtime environment](#runtime-environment)。

## 工作流和反馈循环

### 为复杂任务使用工作流

把复杂操作拆成清晰、顺序明确的步骤。对于特别复杂的工作流，提供一份检查清单，让智能体可以复制到回复中并随进度勾选。

**示例 1：研究综合工作流**（适用于不包含代码的技能）：

````markdown  theme={null}
## Research synthesis workflow

复制这份检查清单并跟踪进度：

```
Research Progress:
- [ ] Step 1: Read all source documents
- [ ] Step 2: Identify key themes
- [ ] Step 3: Cross-reference claims
- [ ] Step 4: Create structured summary
- [ ] Step 5: Verify citations
```

**Step 1: Read all source documents**

阅读 `sources/` 目录中的每份文档。记录主要论点和支持证据。

**Step 2: Identify key themes**

寻找不同来源之间的模式。哪些主题反复出现？不同来源在哪里一致或冲突？

**Step 3: Cross-reference claims**

对每一项主要主张，验证它确实出现在源材料中。记录每一点由哪个来源支持。

**Step 4: Create structured summary**

按主题组织发现，包括：
- 主要主张
- 来源中的支持证据
- 冲突观点（如果有）

**Step 5: Verify citations**

检查每项主张是否引用正确的源文档。如果引用不完整，返回 Step 3。
````

这个示例说明工作流同样适用于无需代码的分析任务。检查清单模式适用于任何复杂的多步骤流程。

**示例 2：PDF 表单填写工作流**（适用于含代码的技能）：

````markdown  theme={null}
## PDF form filling workflow

复制这份清单，并在完成后逐项勾选：

```
Task Progress:
- [ ] Step 1: Analyze the form (run analyze_form.py)
- [ ] Step 2: Create field mapping (edit fields.json)
- [ ] Step 3: Validate mapping (run validate_fields.py)
- [ ] Step 4: Fill the form (run fill_form.py)
- [ ] Step 5: Verify output (run verify_output.py)
```

**Step 1: Analyze the form**

运行：`python scripts/analyze_form.py input.pdf`

该命令会提取表单字段及其位置，并保存到 `fields.json`。

**Step 2: Create field mapping**

编辑 `fields.json`，为每个字段加入值。

**Step 3: Validate mapping**

运行：`python scripts/validate_fields.py fields.json`

继续之前修复所有校验错误。

**Step 4: Fill the form**

运行：`python scripts/fill_form.py input.pdf fields.json output.pdf`

**Step 5: Verify output**

运行：`python scripts/verify_output.py output.pdf`

如果验证失败，返回 Step 2。
````

清晰步骤可以防止智能体跳过关键校验。检查清单则帮助你和智能体共同跟踪多步骤流程的进度。

### 实现反馈循环

**常见模式：** 运行 validator → 修复错误 → 重复

这个模式能显著提升输出质量。

**示例 1：风格指南合规**（适用于不包含代码的技能）：

```markdown  theme={null}
## Content review process

1. 按照 STYLE_GUIDE.md 中的指南起草内容
2. 对照检查清单审查：
   - 检查术语一致性
   - 验证示例是否遵循标准格式
   - 确认所有必需章节都存在
3. 如果发现问题：
   - 记录每个问题并引用具体章节
   - 修改内容
   - 再次执行检查清单
4. 只有全部要求满足后才继续
5. 完成并保存文档
```

这展示了使用参考文档而不是脚本实现校验循环。“validator” 是 STYLE_GUIDE.md，智能体通过读取和比较完成检查。

**示例 2：文档编辑流程**（适用于含代码的技能）：

```markdown  theme={null}
## Document editing process

1. 修改 `word/document.xml`
2. **立即验证**：`python ooxml/scripts/validate.py unpacked_dir/`
3. 如果验证失败：
   - 仔细阅读错误信息
   - 修复 XML 中的问题
   - 再次运行验证
4. **只有验证通过后才能继续**
5. 重新打包：`python ooxml/scripts/pack.py unpacked_dir/ output.docx`
6. 测试输出文档
```

这种验证循环可以尽早捕获错误。

## 内容指南

### 避免时效性信息

不要包含很快会过时的信息：

**差示例：依赖时间**（最终会变错）：

```markdown  theme={null}
If you're doing this before August 2025, use the old API.
After August 2025, use the new API.
```

**好示例**（使用“旧模式”章节）：

```markdown  theme={null}
## Current method

Use the v2 API endpoint: `api.example.com/v2/messages`

## Old patterns

<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>

The v1 API used: `api.example.com/v1/messages`

This endpoint is no longer supported.
</details>
```

旧模式章节提供历史上下文，同时不会污染主要内容。

### 使用一致术语

选择一个术语，并在整个技能中保持一致：

**好——一致：**

* 始终使用 “API endpoint”
* 始终使用 “field”
* 始终使用 “extract”

**差——不一致：**

* 混用 “API endpoint”、"URL"、"API route"、"path"
* 混用 “field”、"box"、"element"、"control"
* 混用 “extract”、"pull"、"get"、"retrieve"

一致性可以帮助智能体理解并遵循指令。

## 常用模式

### 模板模式

为输出格式提供模板。严格程度应与你的需求相匹配。

**适用于严格要求**（例如 API 响应或数据格式）：

````markdown  theme={null}
## Report structure

始终使用下面这个精确模板结构：

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```
````

**适用于灵活指导**（可以合理适配时）：

````markdown  theme={null}
## Report structure

下面是一个合理的默认格式，但应根据分析内容使用最佳判断：

```markdown
# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]
```

根据具体分析类型按需调整章节。
````

### 示例模式

当技能输出质量依赖示例时，像普通提示一样提供输入/输出对：

````markdown  theme={null}
## Commit message format

按照下面的示例生成提交信息：

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly in reports
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

**Example 3:**
Input: Updated dependencies and refactored error handling
Output:
```
chore: update dependencies and refactor error handling

- Upgrade lodash to 4.17.21
- Standardize error response format across endpoints
```

遵循这种风格：type(scope): 简短描述，然后给出详细说明。
````

示例比单纯描述更容易让智能体理解期望风格和细节层级。

### 条件工作流模式

引导智能体通过决策点：

```markdown  theme={null}
## Document modification workflow

1. 判断修改类型：

   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow:
   - Use docx-js library
   - Build document from scratch
   - Export to .docx format

3. Editing workflow:
   - Unpack existing document
   - Modify XML directly
   - Validate after each change
   - Repack when complete
```

<Tip>
  如果工作流变得很长，或包含很多复杂步骤，可以把它们拆到独立文件中，并告诉智能体根据当前任务读取适当文件。
</Tip>

## 评测与迭代

### 先构建评测

**在编写大量文档之前先创建评测。** 这样可以确保技能解决的是真实问题，而不是把想象中的问题写成文档。

**评测驱动开发：**

1. **识别缺口**：在没有技能时，让智能体执行具有代表性的任务。记录具体失败或缺失上下文
2. **创建评测**：构建三个针对这些缺口的场景
3. **建立基线**：衡量没有技能时的表现
4. **编写最小指令**：只创建足够解决缺口、通过评测的内容
5. **迭代**：运行评测，与基线比较，并持续改进

这种方式保证你解决的是真实问题，而不是提前猜测永远不会出现的要求。

**评测结构：**

```json  theme={null}
{
  "skills": ["pdf-processing"],
  "query": "Extract all text from this PDF file and save it to output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Successfully reads the PDF file using an appropriate PDF processing library or command-line tool",
    "Extracts text content from all pages in the document without missing any pages",
    "Saves the extracted text to a file named output.txt in a clear, readable format"
  ]
}
```

<Note>
  这个例子展示了使用简单测试 rubric 的数据驱动评测。目前我们没有提供内置的评测执行方式。用户可以自己创建评测系统。评测是衡量技能有效性的事实来源。
</Note>

### 与智能体一起迭代开发技能

最有效的技能开发过程会让智能体本身参与。与一个实例（“Agent A”）合作创建技能，再由其他实例（“Agent B”）使用。Agent A 帮助设计和打磨指令，Agent B 则在真实任务中测试它们。这种方式有效，是因为底层模型既理解怎样编写有效智能体指令，也理解智能体执行工作时需要什么信息。

**创建新技能：**

1. **先在没有技能的情况下完成任务**：用普通提示和 Agent A 一起解决问题。过程中，你会自然提供上下文、解释偏好并分享流程知识。注意哪些信息被反复提供。

2. **识别可复用模式**：任务结束后，找出哪些上下文对未来类似任务仍然有用。

   **示例**：如果你完成了一次 BigQuery 分析，可能提供了表名、字段定义、过滤规则（例如“始终排除测试账号”）和常用查询模式。

3. **让 Agent A 创建技能**：“Create a Skill that captures this BigQuery analysis pattern we just used. Include the table schemas, naming conventions, and the rule about filtering test accounts.”

   <Tip>
     现代智能体原生理解技能格式和结构。你不需要特殊系统提示，也不需要专门的“writing skills”技能来帮助创建技能。直接要求智能体创建 Skill，它就能生成带正确 frontmatter 和正文结构的 SKILL.md。
   </Tip>

4. **审查简洁性**：确认 Agent A 没有加入不必要解释。例如：“Remove the explanation about what win rate means - the agent already knows that.”

5. **改进信息架构**：让 Agent A 更有效地组织内容。例如：“Organize this so the table schema is in a separate reference file. We might add more tables later.”

6. **在类似任务上测试**：让 Agent B（一个新实例，并已加载该 Skill）处理相关用例。观察 Agent B 是否找到了正确信息、正确应用规则，并成功完成任务。

7. **根据观察迭代**：如果 Agent B 卡住或遗漏内容，把具体表现反馈给 Agent A：“When the agent used this Skill, it forgot to filter by date for Q4. Should we add a section about date filtering patterns?”

**迭代现有技能：**

改进技能时继续使用同样的层级模式，在下面三者之间循环：

* **与 Agent A 合作**（帮助打磨 Skill 的专家）
* **用 Agent B 测试**（使用 Skill 完成真实工作的智能体）
* **观察 Agent B 的行为**，并把发现带回 Agent A

1. **在真实工作流中使用 Skill**：让 Agent B（已加载 Skill）执行真实任务，而不是测试场景

2. **观察 Agent B 行为**：记录它哪里卡住、哪里成功、哪里做出了意外选择

   **观察示例**：“When I asked Agent B for a regional sales report, it wrote the query but forgot to filter out test accounts, even though the Skill mentions this rule.”

3. **回到 Agent A 改进**：提供当前 SKILL.md，并描述观察到的问题。问：“I noticed Agent B forgot to filter test accounts when I asked for a regional report. The Skill mentions filtering, but maybe it's not prominent enough?”

4. **审查 Agent A 的建议**：Agent A 可能建议重新组织内容，让规则更醒目；把 “always filter” 强化为 “MUST filter”；或者重构工作流章节。

5. **应用并测试改动**：更新 Skill，然后再让 Agent B 用类似请求测试

6. **根据使用持续重复**：遇到新场景时继续“观察—改进—测试”。每次迭代都基于真实智能体行为，而不是假设。

**收集团队反馈：**

1. 把 Skills 分享给队友并观察其使用方式
2. 询问：Skill 是否在预期时激活？指令是否清楚？还缺什么？
3. 吸收反馈，补足自己使用模式中的盲点

**为什么有效**：Agent A 理解智能体需求，你提供领域知识，Agent B 通过真实使用暴露缺口，迭代则让技能依据观察到的行为而不是假设不断改进。

### 观察智能体如何导航技能

迭代技能时，要关注智能体在实践中如何真正使用它们。留意：

* **意外的探索路径**：智能体是否用你没预料的顺序读取文件？这可能说明结构不够直观
* **遗漏连接**：智能体是否没有跟进某些重要文件的引用？链接可能需要更明确或更醒目
* **过度依赖某些章节**：如果智能体总是反复读取同一个文件，考虑是否应把这些内容放进主 SKILL.md
* **被忽略的内容**：如果智能体从不访问某个捆绑文件，它可能不必要，或者主指令没有很好地提示它

根据这些观察而不是假设来迭代。技能元数据中的 `name` 和 `description` 特别关键。智能体会根据它们判断当前任务是否应该触发该技能。确保它们清楚描述技能做什么，以及何时使用。

## 应避免的反模式

### 避免 Windows 风格路径

即使在 Windows 上，也始终使用正斜杠：

* ✓ **好**：`scripts/helper.py`、`reference/guide.md`
* ✗ **避免**：`scripts\helper.py`、`reference\guide.md`

Unix 风格路径能跨平台工作，而 Windows 风格路径会在 Unix 系统中产生错误。

### 避免提供太多选项

除非必要，不要同时呈现多种方法：

````markdown  theme={null}
**Bad example: Too many choices** (confusing):
"You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or..."

**Good example: Provide a default** (with escape hatch):
"Use pdfplumber for text extraction:
```python
import pdfplumber
```

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead."
````

## 高级：包含可执行代码的技能

下面几节聚焦包含可执行脚本的技能。如果你的 Skill 只有 Markdown 指令，可以直接跳到 [Checklist for effective Skills](#checklist-for-effective-skills)。

### 解决问题，不要把问题甩给智能体

为 Skill 编写脚本时，应处理错误条件，而不是把失败留给智能体自己想办法。

**好示例：明确处理错误：**

```python  theme={null}
def process_file(path):
    """Process a file, creating it if it doesn't exist."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        # Create file with default content instead of failing
        print(f"File {path} not found, creating default")
        with open(path, 'w') as f:
            f.write('')
        return ''
    except PermissionError:
        # Provide alternative instead of failing
        print(f"Cannot access {path}, using default")
        return ''
```

**差示例：把问题甩给智能体：**

```python  theme={null}
def process_file(path):
    # Just fail and let the agent figure it out
    return open(path).read()
```

配置参数也应有理由并有文档说明，避免“巫术常量”（Ousterhout 定律）。如果你自己都不知道正确值，智能体又该怎样判断？

**好示例：自解释：**

```python  theme={null}
# HTTP requests typically complete within 30 seconds
# Longer timeout accounts for slow connections
REQUEST_TIMEOUT = 30

# Three retries balances reliability vs speed
# Most intermittent failures resolve by the second retry
MAX_RETRIES = 3
```

**差示例：魔法数字：**

```python  theme={null}
TIMEOUT = 47  # Why 47?
RETRIES = 5   # Why 5?
```

### 提供实用脚本

即使智能体本来可以自己写脚本，预制脚本仍有明显优势：

**实用脚本的好处：**

* 比临时生成的代码更可靠
* 节省 token（无需把代码放进上下文）
* 节省时间（无需现场生成代码）
* 确保不同使用场景保持一致

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=4bbc45f2c2e0bee9f2f0d5da669bad00" alt="Bundling executable scripts alongside instruction files" data-og-width="2048" width="2048" data-og-height="1154" height="1154" data-path="images/agent-skills-executable-scripts.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=9a04e6535a8467bfeea492e517de389f 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=e49333ad90141af17c0d7651cca7216b 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=954265a5df52223d6572b6214168c428 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=2ff7a2d8f2a83ee8af132b29f10150fd 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=48ab96245e04077f4d15e9170e081cfb 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=0301a6c8b3ee879497cc5b5483177c90 2500w" />

上图展示了可执行脚本如何与指令文件协作。指令文件（forms.md）引用脚本，智能体可以直接执行，而无需把脚本内容加载到上下文中。

**重要区别**：指令中要明确智能体应该：

* **执行脚本**（最常见）："Run `analyze_form.py` to extract fields"
* **把脚本作为参考阅读**（用于复杂逻辑）："See `analyze_form.py` for the field extraction algorithm"

对大多数实用脚本，执行比阅读更可靠、更高效。脚本执行如何工作，参见下方 [Runtime environment](#runtime-environment)。

**示例：**

````markdown  theme={null}
## Utility scripts

**analyze_form.py**: Extract all form fields from PDF

```bash
python scripts/analyze_form.py input.pdf > fields.json
```

Output format:
```json
{
  "field_name": {"type": "text", "x": 100, "y": 200},
  "signature": {"type": "sig", "x": 150, "y": 500}
}
```

**validate_boxes.py**: Check for overlapping bounding boxes

```bash
python scripts/validate_boxes.py fields.json
# Returns: "OK" or lists conflicts
```

**fill_form.py**: Apply field values to PDF

```bash
python scripts/fill_form.py input.pdf fields.json output.pdf
```
````

### 使用视觉分析

当输入可以渲染为图像时，让智能体直接分析图像：

````markdown  theme={null}
## Form layout analysis

1. Convert PDF to images:
   ```bash
   python scripts/pdf_to_images.py form.pdf
   ```

2. Analyze each page image to identify form fields
3. The agent can see field locations and types visually
````

<Note>
  在这个示例中，你需要自己编写 `pdf_to_images.py` 脚本。
</Note>

智能体的视觉能力有助于理解布局和结构。

### 创建可验证的中间产物

当智能体执行复杂、开放式任务时，可能会出错。“plan-validate-execute”模式通过先让智能体生成结构化计划，再用脚本验证计划，最后执行，从而提早捕获错误。

**示例**：假设你让智能体根据电子表格更新 PDF 中的 50 个表单字段。如果没有验证，它可能引用不存在的字段、创建冲突值、遗漏必填字段，或者错误应用更新。

**解决方案**：使用上方的工作流模式（PDF 表单填写），但加入一个中间 `changes.json` 文件，在真正应用变更前先验证。工作流变为：分析 → **创建计划文件** → **验证计划** → 执行 → 验证结果。

**为什么有效：**

* **尽早发现错误**：在应用修改之前就能捕获问题
* **机器可验证**：脚本提供客观验证
* **规划可逆**：智能体可以迭代计划，而不触碰原始文件
* **易于调试**：错误消息可以直接指向具体问题

**何时使用**：批量操作、破坏性变更、复杂校验规则、高风险操作。

**实现提示**：让校验脚本输出详细、具体的错误消息，例如 "Field 'signature\_date' not found. Available fields: customer\_name, order\_total, signature\_date\_signed"，帮助智能体修复。

### 包依赖

Skills 运行在代码执行环境中，不同平台限制不同：

* **claude.ai**：可以从 npm 和 PyPI 安装包，也可以从 GitHub 仓库拉取
* **Anthropic API**：没有网络访问，也不能在运行时安装包

在 SKILL.md 中列出必需包，并根据 [code execution tool documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) 确认它们可用。

### 运行时环境

Skills 运行在具备文件系统访问、bash 命令和代码执行能力的环境中。关于这种架构的概念说明，参见概览中的 [The Skills architecture](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#the-skills-architecture)。

**它如何影响技能编写：**

**智能体如何访问 Skills：**

1. **预加载元数据**：启动时，所有 Skills YAML frontmatter 中的 name 和 description 被载入系统提示
2. **按需读取文件**：智能体需要时使用文件读取工具访问 SKILL.md 和其他文件
3. **高效执行脚本**：实用脚本可以通过 bash 执行，而无需把完整源代码加载到上下文；只有脚本输出消耗 token
4. **大文件没有立即上下文成本**：参考文件、数据或文档只有被读取时才占用上下文 token

* **文件路径很重要**：智能体像浏览文件系统一样导航技能目录。使用正斜杠（`reference/guide.md`），不要使用反斜杠
* **文件名要描述内容**：使用 `form_validation_rules.md`，不要使用 `doc2.md`
* **为发现而组织**：按领域或功能组织目录
  * 好：`reference/finance.md`、`reference/sales.md`
  * 差：`docs/file1.md`、`docs/file2.md`
* **捆绑完整资源**：可以包含完整 API 文档、大量示例和大型数据集；被读取之前没有上下文成本
* **确定性操作优先使用脚本**：写 `validate_form.py`，不要要求智能体临时生成验证代码
* **明确执行意图**：
  * "Run `analyze_form.py` to extract fields"（执行）
  * "See `analyze_form.py` for the extraction algorithm"（作为参考读取）
* **测试文件访问模式**：用真实请求验证智能体能正确导航目录结构

**示例：**

```
bigquery-skill/
├── SKILL.md (overview, points to reference files)
└── reference/
    ├── finance.md (revenue metrics)
    ├── sales.md (pipeline data)
    └── product.md (usage analytics)
```

当用户询问收入时，智能体读取 SKILL.md，看到 `reference/finance.md` 的引用，然后调用 bash 只读取这个文件。sales.md 和 product.md 继续留在文件系统中，在需要之前占用 0 个上下文 token。这种基于文件系统的模型正是渐进式披露能够工作的原因：智能体可以导航并只加载当前任务需要的内容。

完整技术架构参见 Skills overview 中的 [How Skills work](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work)。

### MCP 工具引用

如果 Skill 使用 MCP（Model Context Protocol）工具，应始终使用完全限定工具名，避免出现“tool not found”错误。

**格式**：`ServerName:tool_name`

**示例：**

```markdown  theme={null}
Use the BigQuery:bigquery_schema tool to retrieve table schemas.
Use the GitHub:create_issue tool to create issues.
```

其中：

* `BigQuery` 和 `GitHub` 是 MCP server 名称
* `bigquery_schema` 和 `create_issue` 是对应 server 中的工具名称

没有 server 前缀时，智能体可能找不到工具，尤其是在同时存在多个 MCP server 的情况下。

### 不要假设工具已经安装

不要假定包一定可用：

````markdown  theme={null}
**Bad example: Assumes installation**:
"Use the pdf library to process the file."

**Good example: Explicit about dependencies**:
"Install required package: `pip install pypdf`

Then use it:
```python
from pypdf import PdfReader
reader = PdfReader("file.pdf")
```"
````

## 技术说明

### YAML frontmatter 要求

SKILL.md frontmatter 需要 `name`（最多 64 字符）和 `description`（最多 1024 字符）。完整结构请参阅 [Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#skill-structure)。

### Token 预算

为获得最佳效果，让 SKILL.md 正文保持在 500 行以内。超过时，使用前面介绍的渐进式披露模式拆成独立文件。架构细节参见 [Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work)。

## 有效 Skills 检查清单

分享 Skill 之前请验证：

### 核心质量

* [ ] Description 具体，并包含关键术语
* [ ] Description 同时说明 Skill 做什么以及何时使用
* [ ] SKILL.md 正文少于 500 行
* [ ] 额外细节按需放在独立文件中
* [ ] 不包含时效性信息（或者放在“旧模式”章节）
* [ ] 全文术语一致
* [ ] 示例具体而非抽象
* [ ] 文件引用只有一层
* [ ] 合理使用渐进式披露
* [ ] 工作流步骤清晰

### 代码和脚本

* [ ] 脚本真正解决问题，而不是把问题甩给智能体
* [ ] 错误处理明确且有帮助
* [ ] 没有“巫术常量”（所有值都有理由）
* [ ] 指令列出了所需包，并确认它们可用
* [ ] 脚本文档清晰
* [ ] 没有 Windows 风格路径（全部使用正斜杠）
* [ ] 关键操作有验证/校验步骤
* [ ] 对质量关键任务包含反馈循环

### 测试

* [ ] 至少创建三个评测
* [ ] 已在 Haiku、Sonnet 和 Opus 上测试
* [ ] 已使用真实使用场景测试
* [ ] 已吸收团队反馈（如适用）

## 下一步

<CardGroup cols={2}>
  <Card title="Get started with Agent Skills" icon="rocket" href="https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart">
    创建你的第一个 Skill
  </Card>

  <Card title="Use Skills in Claude Code" icon="terminal" href="https://code.claude.com/docs/en/skills">
    在 Claude Code 中创建和管理 Skills
  </Card>

  <Card title="Use Skills with the API" icon="code" href="https://platform.claude.com/docs/en/build-with-claude/skills-guide">
    以编程方式上传并使用 Skills
  </Card>
</CardGroup>