# 视觉伴侣指南

基于浏览器的视觉头脑风暴伴侣，用于展示 mockup、图表和选项。

## 何时使用

逐问题决定，而不是按整个会话决定。判断标准是：**用户看到它，会不会比读文字更容易理解？**

**当内容本身是视觉内容时使用浏览器：**

- **UI mockup** —— 线框图、布局、导航结构、组件设计
- **架构图** —— 系统组件、数据流、关系图
- **并排视觉比较** —— 比较两种布局、两种配色、两种设计方向
- **设计打磨** —— 当问题是外观感受、间距、视觉层级
- **空间关系** —— 以图形呈现的状态机、流程图、实体关系

**当内容是文字或表格时使用终端：**

- **需求与范围问题** —— “X 是什么意思？”、“哪些功能在范围内？”
- **概念性 A/B/C 选择** —— 在用文字描述的方案之间选择
- **取舍列表** —— 优缺点、比较表
- **技术决策** —— API 设计、数据建模、架构方案选择
- **澄清问题** —— 任何答案本质上是文字，而不是视觉偏好的问题

一个问题涉及 UI 主题，并不自动等于视觉问题。“你想要哪种向导？”是概念问题——用终端。“这些向导布局中哪个感觉更对？”才是视觉问题——用浏览器。

## 工作原理

服务器监视一个目录中的 HTML 文件，并把最新文件提供给浏览器。你把 HTML 内容写入 `screen_dir`，用户会在浏览器中看到它，并可以点击选择选项。选择结果会记录到 `state_dir/events`，供你在下一轮读取。

**内容片段 vs 完整文档：** 如果 HTML 文件以 `<!DOCTYPE` 或 `<html` 开头，服务器会原样提供它（只注入 helper 脚本）。否则，服务器会自动使用 frame template 包装内容——加入 header、CSS 主题、连接状态和全部交互基础设施。**默认写内容片段。** 只有需要完整控制页面时才写完整文档。

## 启动会话

```bash
# 用户批准伴侣之后再启动。--open 会在第一屏出现时自动打开浏览器；
# --project-dir 会持久化 mockup，并允许在相同端口重启。
scripts/start-server.sh --project-dir /path/to/project --open

# Returns: {"type":"server-started","port":52341,
#           "url":"http://localhost:52341/?key=ab12…",
#           "screen_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/content",
#           "state_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/state"}
```

保存响应中的 `screen_dir` 和 `state_dir`。使用 `--open` 时，你推送第一屏后浏览器会自动打开——不需要再让用户手动打开，但仍应把 URL 作为备用方式发给他们（无头/远程环境无法自动打开）。

**URL 中包含会话 key（`?key=…`）。** 服务器会拒绝任何不带 key 的请求，因此始终把 `url` 字段返回的**完整** URL 给用户——绝不要移除查询字符串，也绝不要只给裸的 `http://host:port`。这个 key 同时保护 HTTP 和 WebSocket 访问，防止无关浏览器标签页或网络上的其他机器读取屏幕或注入事件。第一次加载后，浏览器会通过 cookie 记住 key，因此 reload 和 `/files/*` 资源访问无需重复附带它。

**查找连接信息：** 服务器会把启动 JSON 写到 `$STATE_DIR/server-info`。如果你把服务器放到后台启动却没有捕获 stdout，读取该文件即可得到 URL 和端口。使用 `--project-dir` 时，可在 `<project>/.superpowers/brainstorm/` 下找到会话目录。

**注意：** 把项目根目录作为 `--project-dir` 传入，这样 mockup 会持久化在 `.superpowers/brainstorm/` 中，并能跨服务器重启保留。不传时，文件会写入 `/tmp`，之后会被清理。如果 `.superpowers/` 尚未在 `.gitignore` 中，提醒用户加入。

**不同平台上的服务器启动方式：**

**Claude Code：**
```bash
# 默认模式即可——脚本会自行把服务器放到后台。
scripts/start-server.sh --project-dir /path/to/project --open
```

在 Windows 上，脚本会自动检测并切换到前台模式（这会阻塞工具调用）。对 Bash 工具调用使用 `run_in_background: true`，让服务器能够跨对话轮次继续运行；然后下一轮读取 `$STATE_DIR/server-info` 获取 URL 和端口。

**Codex：**
```bash
# Codex 会回收后台进程。脚本会自动检测 CODEX_CI 并切换到
# 前台模式。正常运行即可——不需要额外 flag。
scripts/start-server.sh --project-dir /path/to/project --open
```

**Gemini CLI：**
```bash
# 使用 --foreground，并在 shell 工具调用上设置 is_background: true，
# 让进程能够跨轮次继续运行
scripts/start-server.sh --project-dir /path/to/project --open --foreground
```

**Copilot CLI：**
```bash
# 使用 Copilot CLI 的非阻塞/后台 shell 机制启动，让服务器能够跨轮次存活。
# 保留 --foreground，这样由运行环境而不是脚本负责后台化。启动器是 .sh，
# 因此通过 bash 调用（Windows 上从 PowerShell 工具调用 Git Bash 的 bash.exe）。
bash scripts/start-server.sh --project-dir /path/to/project --open --foreground
```

**其他环境：** 服务器必须能在对话轮次之间持续后台运行。如果你的环境会回收 detached process，就使用 `--foreground`，再通过对应平台的后台执行机制启动命令。

如果浏览器无法访问 URL（远程/容器化环境中很常见），绑定非回环 host：

```bash
scripts/start-server.sh \
  --project-dir /path/to/project \
  --host 0.0.0.0 \
  --url-host localhost
```

使用 `--url-host` 控制返回 URL JSON 中打印的主机名。

## 循环

1. **先检查服务器仍然存活**，然后把 HTML **写入 `screen_dir` 中一个新的文件**：
   - **在引用 URL 或推送屏幕之前，必须确认服务器仍存活。** 检查 `$STATE_DIR/server-info` 存在，且 `$STATE_DIR/server-stopped` 不存在。如果服务器已经停止，使用**相同的 `--project-dir`** 重新运行 `start-server.sh`——它会复用同一端口，因此用户已经打开的标签页会自行重新连接（服务器停掉时会显示 “paused” 遮罩），无需发送新 URL。服务器默认在空闲 4 小时后自动退出（可通过 `--idle-timeout-minutes` 配置）。
   - 使用语义化文件名：`platform.html`、`visual-style.html`、`layout.html`
   - **绝不要复用文件名**——每个屏幕必须使用新文件
   - 使用你的文件创建工具——**绝不要使用 cat/heredoc**（会把噪音输出到终端）
   - 服务器会自动提供最新文件

2. **告诉用户会看到什么，然后结束这一轮：**
   - 每一步都提醒 URL（不只是第一步）
   - 简短文字说明屏幕上的内容（例如：“正在展示 3 个首页布局选项”）
   - 请他们在终端回复：“看一下并告诉我你的想法。如果愿意，可以点击一个选项。”

3. **下一轮**——用户在终端回复后：
   - 如果 `$STATE_DIR/events` 存在，读取它——其中包含用户的浏览器交互（点击、选择），格式为 JSON lines
   - 与用户的终端文字合并，形成完整反馈
   - 终端消息是主要反馈；`state_dir/events` 提供结构化交互数据

4. **迭代或推进**——如果反馈改变当前屏幕，写一个新文件（例如 `layout-v2.html`）。只有当前步骤确认完毕后，才进入下一个问题。

5. **回到终端时卸载**——当下一步不再需要浏览器（例如澄清问题、讨论取舍）时，推送一个 waiting screen 清掉过时内容：

   ```html
   <!-- filename: waiting.html (or waiting-2.html, etc.) -->
   <div style="display:flex;align-items:center;justify-content:center;min-height:60vh">
     <p class="subtitle">Continuing in terminal...</p>
   </div>
   ```

   这样可以避免用户一直看着已经解决的选择，而对话实际上已经继续。当下一个视觉问题出现时，再照常推送新的内容文件。

6. 重复直到完成。

## 编写内容片段

只写页面内部的内容。服务器会自动用 frame template 包装它（header、主题 CSS、连接状态和所有交互基础设施）。

**最小示例：**

```html
<h2>Which layout works better?</h2>
<p class="subtitle">Consider readability and visual hierarchy</p>

<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Single Column</h3>
      <p>Clean, focused reading experience</p>
    </div>
  </div>
  <div class="option" data-choice="b" onclick="toggleSelect(this)">
    <div class="letter">B</div>
    <div class="content">
      <h3>Two Column</h3>
      <p>Sidebar navigation with main content</p>
    </div>
  </div>
</div>
```

就这些。不需要 `<html>`、CSS 或 `<script>` 标签。服务器会提供这一切。

## 可用 CSS 类

Frame template 为内容提供下面这些 CSS 类：

### 选项（A/B/C 选择）

```html
<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Title</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

**多选：** 在容器上添加 `data-multiselect`，允许用户选择多个选项。每次点击会切换该项的 selected 样式。

```html
<div class="options" data-multiselect>
  <!-- same option markup — users can select/deselect multiple -->
</div>
```

### 卡片（视觉设计）

```html
<div class="cards">
  <div class="card" data-choice="design1" onclick="toggleSelect(this)">
    <div class="card-image"><!-- mockup content --></div>
    <div class="card-body">
      <h3>Name</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

### Mockup 容器

```html
<div class="mockup">
  <div class="mockup-header">Preview: Dashboard Layout</div>
  <div class="mockup-body"><!-- your mockup HTML --></div>
</div>
```

### 分屏视图（并排）

```html
<div class="split">
  <div class="mockup"><!-- left --></div>
  <div class="mockup"><!-- right --></div>
</div>
```

### 优缺点

```html
<div class="pros-cons">
  <div class="pros"><h4>Pros</h4><ul><li>Benefit</li></ul></div>
  <div class="cons"><h4>Cons</h4><ul><li>Drawback</li></ul></div>
</div>
```

### Mock 元素（线框图构建块）

```html
<div class="mock-nav">Logo | Home | About | Contact</div>
<div style="display: flex;">
  <div class="mock-sidebar">Navigation</div>
  <div class="mock-content">Main content area</div>
</div>
<button class="mock-button">Action Button</button>
<input class="mock-input" placeholder="Input field">
<div class="placeholder">Placeholder area</div>
```

### 排版和区块

- `h2` —— 页面标题
- `h3` —— 章节标题
- `.subtitle` —— 标题下方的次要文字
- `.section` —— 带底部间距的内容块
- `.label` —— 小号大写标签文字

## 浏览器事件格式

用户在浏览器中点击选项时，交互会记录到 `$STATE_DIR/events`（每行一个 JSON 对象）。推送新屏幕时，该文件会自动清空。

```jsonl
{"type":"click","choice":"a","text":"Option A - Simple Layout","timestamp":1706000101}
{"type":"click","choice":"c","text":"Option C - Complex Grid","timestamp":1706000108}
{"type":"click","choice":"b","text":"Option B - Hybrid","timestamp":1706000115}
```

完整事件流展示用户的探索路径——他们可能在最终确定前点击多个选项。最后一个 `choice` 事件通常是最终选择，但点击模式也可能暴露犹豫或值得进一步询问的偏好。

如果 `$STATE_DIR/events` 不存在，说明用户没有与浏览器交互——只使用终端文字。

## 设计技巧

- **让保真度与问题匹配**——布局问题用线框图，打磨视觉细节的问题用精细 mockup
- **每页都解释问题**——写“Which layout feels more professional?”，不要只写“Pick one”
- **推进前先迭代**——如果反馈改变当前屏幕，就写新版本
- 每屏最多 **2–4 个选项**
- **真正需要时使用真实内容**——例如摄影作品集应使用实际图片（Unsplash）。占位内容会掩盖设计问题。
- **保持 mockup 简洁**——聚焦布局和结构，不做像素级完美设计

## 文件命名

- 使用语义化名称：`platform.html`、`visual-style.html`、`layout.html`
- 绝不要复用文件名——每个屏幕都必须是新文件
- 迭代时添加版本后缀，例如 `layout-v2.html`、`layout-v3.html`
- 服务器按修改时间提供最新文件

## 清理

```bash
scripts/stop-server.sh $SESSION_DIR
```

如果会话使用 `--project-dir`，mockup 文件会持久化在 `.superpowers/brainstorm/` 中供以后参考。只有 `/tmp` 会话在停止时会被删除。

## 参考

- Frame template（CSS 参考）：`scripts/frame-template.html`
- Helper script（客户端）：`scripts/helper.js`
