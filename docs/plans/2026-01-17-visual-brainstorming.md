# 视觉头脑风暴实现计划

> **给 agentic workers：** 必需子技能：逐任务实施本计划时使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans。

**目标：** 让 brainstorming 能在确实适合视觉表达的设计问题上使用浏览器展示 mockup、布局和视觉比较，同时保持文本问题继续走终端对话。

**架构：** 在 brainstorming 技能中增加一个可选的“视觉伴侣”模式。一个本地 Node 服务器监视目录中的 HTML 文件，并通过浏览器展示最新页面；用户可以点击选项，点击事件写入状态文件供智能体读取。HTML 默认使用统一 frame template 包装，技能通过创建新文件推进视觉步骤。

**技术栈：** Node.js、原生 HTTP/WebSocket、HTML/CSS/JavaScript、Bash、Markdown

---

## 任务 1：定义视觉伴侣工作流

**文件：**
- 创建：`skills/brainstorming/visual-companion.md`
- 修改：`skills/brainstorming/SKILL.md`

### 步骤 1：编写视觉伴侣指南

文档必须定义：

- 何时应该使用浏览器：mockup、布局、架构图、并排视觉比较、视觉层级。
- 何时继续使用终端：需求、范围、技术取舍、文字式 A/B/C 选择、澄清问题。
- 用户接受视觉伴侣之后，也要**逐问题**决定是否需要浏览器。
- 每个视觉问题创建一个新的 HTML 文件，不能覆盖旧文件。
- 浏览器点击只是补充反馈；用户的终端回复仍然是主要反馈。
- 返回文字讨论时要显示等待页面，避免浏览器停留在过时选择上。

### 步骤 2：在 brainstorming 中加入触发点

在 brainstorming 的 architectural 流程中加入“恰到好处地提供视觉伴侣”：

- 不在对话开头主动提供。
- 第一次真正遇到视觉问题时，用独立消息询问用户是否愿意尝试。
- 接受后启动服务器并打开浏览器。
- 拒绝后继续纯文本，并且不要重复提供。

### 步骤 3：加入硬边界

明确说明：

- “涉及 UI”不等于“应该使用浏览器”。
- 概念问题仍用终端。
- 只有用户“看到它”明显优于“读文字描述”时才用浏览器。

### 步骤 4：提交

```bash
git add skills/brainstorming/SKILL.md skills/brainstorming/visual-companion.md
git commit -m "feat: define visual brainstorming companion workflow"
```

---

## 任务 2：创建 Frame Template

**文件：**
- 创建：`skills/brainstorming/scripts/frame-template.html`

### 步骤 1：创建统一页面骨架

Frame template 应包含：

- 页面标题/header
- 连接状态指示
- 全局 CSS 变量和排版
- `.options` / `.option`
- `.cards` / `.card`
- `.mockup`
- `.split`
- `.pros-cons`
- 线框图辅助类：`.mock-nav`、`.mock-sidebar`、`.mock-content`、`.mock-button`、`.mock-input`、`.placeholder`
- `.subtitle`、`.section`、`.label`

### 步骤 2：支持内容片段注入

服务器提供内容片段时，把它放入 frame 的主内容区域；如果文件本身是完整 HTML 文档，则不使用 frame 包装。

### 步骤 3：提交

```bash
git add skills/brainstorming/scripts/frame-template.html
git commit -m "feat: add visual brainstorming frame template"
```

---

## 任务 3：实现浏览器 Helper

**文件：**
- 创建：`skills/brainstorming/scripts/helper.js`

### 步骤 1：WebSocket 连接

客户端脚本应：

- 从当前页面连接到服务器 WebSocket。
- 显示 connected / disconnected 状态。
- 服务器通知有新屏幕时自动 reload。
- 断线后自动重连。

### 步骤 2：点击事件

实现：

```javascript
function toggleSelect(element) {
  // Update selected UI state
  // Send { type: 'click', choice, text, timestamp } to server
}
```

支持：
- 单选：点击新选项时清除其他 selected。
- 多选：容器带 `data-multiselect` 时允许多个 selected。

### 步骤 3：提交

```bash
git add skills/brainstorming/scripts/helper.js
git commit -m "feat: add visual companion browser helper"
```

---

## 任务 4：实现零依赖 Node Server

**文件：**
- 创建：`skills/brainstorming/scripts/server.cjs`

### 步骤 1：CLI 参数

支持：

- `--content-dir`
- `--state-dir`
- `--port`
- `--host`
- `--url-host`
- `--idle-timeout-minutes`

### 步骤 2：HTTP 路由

服务器至少提供：

- `/` → 最新屏幕
- `/files/<name>` → 内容目录中的资源
- `/helper.js` → 客户端 helper
- `/health` → 健康检查

如果最新 HTML 是内容片段：
- 加载 frame template
- 注入片段
- 注入 helper.js

如果是完整文档：
- 原样提供
- 在 `</body>` 前注入 helper.js

### 步骤 3：WebSocket

不要依赖第三方包。实现最小 WebSocket 握手和 server-to-client 文本帧，功能只需要：

- 推送 `reload`
- 接收浏览器 JSON 事件

### 步骤 4：监视目录

使用 `fs.watch` 或轮询：

- 检测 `content_dir` 中新文件。
- 选择修改时间最新的 HTML 文件。
- 新屏幕出现后清空旧事件文件。
- 通知已连接客户端 reload。

### 步骤 5：写入事件

浏览器发来的事件以 JSON Lines 形式追加到：

```
$STATE_DIR/events
```

### 步骤 6：空闲退出

记录最近活动时间：
- HTTP 请求
- WebSocket 消息
- 新内容文件

超过 `idle-timeout-minutes` 后退出，避免后台服务器永久驻留。

### 步骤 7：提交

```bash
git add skills/brainstorming/scripts/server.cjs
git commit -m "feat: implement zero-dependency visual companion server"
```

---

## 任务 5：实现 start-server.sh

**文件：**
- 创建：`skills/brainstorming/scripts/start-server.sh`

### 步骤 1：创建会话目录

如果提供 `--project-dir`：

```
<project>/.superpowers/brainstorm/<port>-<timestamp>/
├── content/
└── state/
```

如果没有提供，则使用 `/tmp`。

### 步骤 2：选择端口

- 如果用户提供 `--port`，使用它。
- 否则寻找可用高位端口。

### 步骤 3：启动 Node server

默认后台启动。

支持：
- `--foreground`：前台运行，由宿主运行环境负责后台化。
- `--open`：第一屏可用后自动打开浏览器。

### 步骤 4：输出机器可读 JSON

启动成功后输出：

```json
{
  "type": "server-started",
  "port": 52341,
  "url": "http://localhost:52341",
  "screen_dir": ".../content",
  "state_dir": ".../state"
}
```

同样写入：

```
$STATE_DIR/server-info
```

### 步骤 5：平台适配

- Claude Code：默认后台模式。
- Codex：检测 `CODEX_CI`，需要时自动前台模式。
- Gemini CLI：文档建议 `--foreground` + shell background 机制。

### 步骤 6：提交

```bash
git add skills/brainstorming/scripts/start-server.sh
git commit -m "feat: add visual companion server launcher"
```

---

## 任务 6：实现 stop-server.sh

**文件：**
- 创建：`skills/brainstorming/scripts/stop-server.sh`

### 步骤 1：停止服务器

通过 state 目录中的 PID / server-info 找到并停止 server。

### 步骤 2：写停止标记

创建：

```
$STATE_DIR/server-stopped
```

浏览器可以使用它显示已暂停状态。

### 步骤 3：清理临时目录

- `/tmp` 会话：删除整个 session dir。
- `--project-dir` 会话：保留内容，供后续查看。

### 步骤 4：提交

```bash
git add skills/brainstorming/scripts/stop-server.sh
git commit -m "feat: add visual companion server cleanup"
```

---

## 任务 7：添加服务器生命周期测试

**文件：**
- 创建：`tests/brainstorm-server/start-server.test.sh`
- 创建：`tests/brainstorm-server/stop-server.test.sh`

### 步骤 1：测试启动

验证：

- `start-server.sh` 返回合法 JSON。
- `server-info` 文件存在。
- `/health` 返回成功。
- `content` / `state` 目录存在。

### 步骤 2：测试内容更新

写入 `screen-a.html`，确认 `/` 提供 A；再写 `screen-b.html`，确认最新屏幕切换到 B。

### 步骤 3：测试停止

运行 `stop-server.sh` 后：

- server 不再响应。
- `server-stopped` 存在。
- 临时 session 按规则清理。

### 步骤 4：提交

```bash
git add tests/brainstorm-server/start-server.test.sh tests/brainstorm-server/stop-server.test.sh
git commit -m "test: cover visual companion server lifecycle"
```

---

## 任务 8：添加 WebSocket 与事件测试

**文件：**
- 创建：`tests/brainstorm-server/ws-protocol.test.js`

### 步骤 1：测试握手

使用 Node 原生 socket：

- 发出 WebSocket upgrade 请求。
- 验证 `101 Switching Protocols`。

### 步骤 2：测试 reload 通知

连接客户端后写入新屏幕，验证收到 reload 帧。

### 步骤 3：测试点击事件

模拟客户端发送 JSON：

```json
{"type":"click","choice":"a","text":"Option A","timestamp":1706000101}
```

验证 `$STATE_DIR/events` 中出现对应 JSONL。

### 步骤 4：提交

```bash
git add tests/brainstorm-server/ws-protocol.test.js
git commit -m "test: cover visual companion websocket protocol"
```

---

## 任务 9：添加浏览器 Helper 测试

**文件：**
- 创建：`tests/brainstorm-server/helper.test.js`

### 步骤 1：测试单选行为

验证点击 B 后 A 不再 selected，B selected。

### 步骤 2：测试多选行为

`data-multiselect` 容器中：
- 点击 A → A selected
- 点击 B → A、B 都 selected
- 再点击 A → 只有 B selected

### 步骤 3：测试事件 payload

验证发送的 JSON 包含：
- `type`
- `choice`
- `text`
- `timestamp`

### 步骤 4：提交

```bash
git add tests/brainstorm-server/helper.test.js
git commit -m "test: cover visual companion browser interactions"
```

---

## 任务 10：添加文档示例并进行人工验收

**文件：**
- 修改：`skills/brainstorming/visual-companion.md`

### 步骤 1：加入最小内容片段示例

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
</div>
```

### 步骤 2：人工测试完整流程

1. 启动视觉伴侣服务器。
2. 写入第一屏。
3. 浏览器自动打开。
4. 点击选项。
5. 确认 `events` 文件收到点击。
6. 写入第二屏，确认浏览器自动刷新。
7. 切回终端问题时写入 waiting screen。
8. 停止 server。

### 步骤 3：提交

```bash
git add skills/brainstorming/visual-companion.md
git commit -m "docs: add visual companion usage examples"
```

---

## 验证

运行：

```bash
npm test --prefix tests/brainstorm-server
```

以及相关 shell 生命周期测试。

确认：

- Node server 无第三方运行时依赖。
- HTML 片段和完整 HTML 都能显示。
- 最新文件切换会触发 browser reload。
- 浏览器事件写入 JSONL。
- 单选/多选正常。
- `--project-dir` 会持久化 mockup。
- `/tmp` 会话可以清理。
- 不需要视觉内容时，brainstorming 仍然只使用终端。

## 成功标准

- [ ] 用户只有在真正的视觉问题出现时才会收到视觉伴侣提议。
- [ ] 用户接受后，浏览器能显示 HTML mockup。
- [ ] 新屏幕自动刷新，不要求用户反复打开链接。
- [ ] 浏览器点击能反馈给智能体。
- [ ] 文本问题不会被强行搬到浏览器。
- [ ] 不引入第三方 Node 依赖。
- [ ] Server 可启动、重启、停止并清理。
- [ ] 文档包含跨运行时启动说明。
