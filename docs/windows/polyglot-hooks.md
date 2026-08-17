# Claude Code 的跨平台 Polyglot Hook

Claude Code 插件需要能同时在 Windows、macOS 和 Linux 上工作的 hook。本文档介绍 `hooks/run-hook.cmd` 中使用的单一通用调度器模式。

> **权威来源：** `hooks/run-hook.cmd` 是规范实现。如果本文档与代码不一致，以代码为准。

## 问题

Claude Code 通过 shell 执行 hook 命令：
- **macOS/Linux**：bash 或 sh
- **已安装 Git Bash 的 Windows**：Git Bash
- **未安装 Git Bash 的 Windows**：PowerShell（旧版本使用 CMD.exe）

Windows 的两种回退 shell 都无法正确解析我们的命令字符串：PowerShell 会把开头带引号的路径视为字符串表达式，并在遇到下一个裸词时出错；而 CMD.exe 的 `/c` 引号规则会在路径包含 `(` 等元字符时剥掉外层引号。因此，我们的 hook 会声明 `"shell": "bash"`（Claude Code 2.1.81 起支持；旧版本会忽略这个键），从而强制走 Git Bash 路径；如果没有安装 Git Bash，则会给出可操作的“安装 Git for Windows”错误，而不是 shell 解析器错误。

这会带来几个挑战：

1. **脚本执行**：Windows CMD 无法直接执行 `.sh` 文件
2. **路径格式**：Windows 使用反斜杠（`C:\path`），Unix 使用正斜杠（`/path`）
3. **环境变量**：`$VAR` 语法在 CMD 中无效
4. **自动为 `.sh` 添加 bash 前缀**：Claude Code 在 Windows 上会自动给任何路径中包含 `.sh` 的命令加上 `bash` 前缀——如果脚本有扩展名，这会干扰调度器

## 解决方案：无扩展名脚本 + 单一通用调度器

仓库为所有 hook 使用同一个通用 `run-hook.cmd` 调度器。Hook 脚本**没有扩展名**（使用 `session-start`，而不是 `session-start.sh`）。这是有意设计的：可以阻止 Claude Code 的 Windows 自动检测给调度器命令加上 `bash` 前缀并破坏执行。

### 文件结构

```
hooks/
├── hooks.json          # Points to run-hook.cmd with extensionless script name
├── run-hook.cmd        # Cross-platform dispatcher (the polyglot wrapper)
└── session-start       # Actual hook logic — extensionless bash script
```

### hooks.json

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd\" session-start",
            "shell": "bash",
            "async": false
          }
        ]
      }
    ]
  }
}
```

路径需要加引号，因为 `${CLAUDE_PLUGIN_ROOT}` 可能包含空格。

## `run-hook.cmd` 的高层工作原理

`run-hook.cmd` 是一个 polyglot 脚本：Windows 会把第一部分当作 batch 命令处理，而 Unix shell 会把这一块视为 no-op heredoc，忽略后继续执行后面的内容。

不要从本文档复制实现。修改调度器时请直接阅读 `hooks/run-hook.cmd`，修改后运行 `tests/hooks/test-session-start.sh`。

### 在 Windows（CMD.exe）上的工作方式

1. Batch 部分会验证脚本名称，并根据调度器自身位置解析 hook 目录。
2. 它会在三个位置尝试寻找 bash：
   - `C:\Program Files\Git\bin\bash.exe`
   - `C:\Program Files (x86)\Git\bin\bash.exe`
   - `PATH` 中的 `bash`（MSYS2、Cygwin 或非默认位置安装的 Git）
3. 找到 bash 后，它会运行 hooks 目录中指定的无扩展名 hook 脚本。
4. 如果找不到 bash，调度器会静默以 `0` 退出——插件继续工作，只是跳过该 hook。
5. `exit /b` 会在 CMD 到达 Unix 部分之前停止执行。

### 在 Unix（bash/sh）上的工作方式

1. `: << 'CMDBLOCK'` 在 no-op 命令上打开一个 heredoc。
2. 整个 CMD batch 块被 heredoc 消费并忽略。
3. 在 `CMDBLOCK` 之后，bash 会解析脚本目录，并直接 `exec` 指定的无扩展名脚本。

### 关键设计决策

| 决策 | 原因 |
|----------|-----|
| 无扩展名脚本 | 防止 Claude Code 的 Windows `.sh` 自动加前缀机制干扰调度器命令 |
| 不使用 `-l`（login shell） | 没有必要；hook 脚本应当自包含，不依赖 login-shell 的 PATH 设置 |
| 不使用 `cygpath` | Bash 可以直接接收并正确处理 Windows 路径；`cygpath` 只在旧的 `-c "..."` 调用模式中需要，直接 exec 不需要 |
| 找不到 bash 时静默退出 | 避免破坏没有安装 Git for Windows 的用户体验；只会优雅地跳过 hook 上下文注入 |

## 编写跨平台 Hook 脚本

Hook 逻辑放在无扩展名脚本文件中。下面是一些可移植写法：

### 推荐
- 尽可能使用纯 bash 内建功能
- 使用 `$(command)`，而不是反引号
- 给所有变量展开加引号：`"$VAR"`

### 避免
- 在没有回退方案的情况下依赖 PATH 中的工具（hook 运行时不使用 `-l`，因此不会设置 login-shell PATH）
- 给脚本使用 `.sh` 扩展名——这会触发 Claude Code 的 Windows 自动加前缀机制

### 示例：不借助外部工具进行 JSON 转义

```bash
escape_for_json() {
    local input="$1"
    local output=""
    local i char
    for (( i=0; i<${#input}; i++ )); do
        char="${input:$i:1}"
        case "$char" in
            $'\\') output+='\\' ;;
            '"') output+='\"' ;;
            $'\n') output+='\n' ;;
            $'\r') output+='\r' ;;
            $'\t') output+='\t' ;;
            *) output+="$char" ;;
        esac
    done
    printf '%s' "$output"
}
```

## 故障排查

### “bash is not recognized”

CMD 在调度器尝试的三个位置都找不到 bash。调度器会静默退出（0），而不是报错，因此该 hook 会被跳过。请把 Git for Windows 安装到标准路径，或确保 `bash` 位于 `PATH` 中。

### Hook 在 Unix 上能运行，但在 Windows 上什么也不做

检查 `hooks.json` 中的脚本文件名是否**没有扩展名**。像 `run-hook.cmd session-start.sh` 这样的命令可能触发 Claude Code 对 `.sh` 的自动检测，绕过预期的 CMD 调度路径；或者直接尝试运行一个不存在的 `session-start.sh` 脚本。

### Hook 完全没有触发

确认 `hooks.json` 中的 `matcher` 与你的运行环境发出的事件类型匹配。Claude Code 使用 `startup|clear|compact`；Cursor 使用 `sessionStart`。Cursor 版本见 `hooks-cursor.json`。

## 相关 Issue

- [anthropics/claude-code#9758](https://github.com/anthropics/claude-code/issues/9758) — Windows 上 `.sh` 脚本会在编辑器中打开
- [anthropics/claude-code#3417](https://github.com/anthropics/claude-code/issues/3417) — Hook 在 Windows 上无法工作
