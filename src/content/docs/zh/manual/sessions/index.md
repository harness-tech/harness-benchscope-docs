---
title: Sessions 手册概览
description: Sessions（会话）模块操作手册概览：页面结构、工作区、对话列表与模块内文档导航。
---

# Sessions 手册概览

Sessions（导航名「会话」）是 BenchScope 的**交互式对话模块**：选择一个已配置的推理 Provider 与模型，即可与模型进行 **SSE 流式对话**，实时查看输出、思考过程（`reasoning_content` 增量）与 Token 统计。

<div class="info">
**代理转发**：BenchScope 本身**不提供** OpenAI 兼容的 `/v1/*` 推理端点。会话请求由服务端**代理转发**到激活的 Provider（OpenAI 兼容端点），因此使用会话功能前需在 Settings → Providers 中配置并激活一个可用的推理服务。
</div>

## 1. 功能说明

- **多会话管理**：新建、切换、重命名、删除、清空会话；会话自动落盘，重启服务后恢复。
- **流式对话**：SSE 流式输出（`token` / `thinking` 增量），Markdown 渲染 + 代码高亮。
- **采样参数**：`temperature`（0-2）、`top_k`（1-200）、`top_p`（0-1），以及质量档位 `quality`（high/medium/low）与思考开关 `enable_thinking`。
- **Token 统计**：TTFT、tok/s、TPOT、ITL 等指标实时显示在会话头部性能栏。
- **会话持久化**：会话状态保存于 `~/.benchscope/sessions/*.json`，对话日志保存于 `~/.benchscope/logs/sessions/*.log`。

## 2. 页面结构

```
+----------------------------------+----------------------------------------------+
| 左侧栏（260px，会话工作区）        | 主内容区                                       |
| +------------------------------+ | +--------------------------------------------+|
| | [ + 新建会话 ]                | | | 性能栏 turns·steps | LLM | TTFT | TPOT | ITL ||
| +------------------------------+ | | + top_k [10]  temp [0.5]  top_p [1.0]       ||
| | 对话          [ 清空 ]        | | +--------------------------------------------+|
| +------------------------------+ | | 消息区（Markdown + 代码高亮 + 思考块折叠）   |
| | · 会话 A   09-09 21:00   [···]| | |  U 用户气泡（右）                           ||
| | · 会话 B   09-09 20:30   [···]| | |  AI 助手气泡（左）  [思考中 ▾]              ||
| +------------------------------+ | +--------------------------------------------+|
|                                  | | 输入框（Enter 发送 / Shift+Enter 换行）       |
|                                  | | Provider ▾  选择模型 ▾  质量 ▾  思考[✓]  (→) |
+----------------------------------+----------------------------------------------+
```

- **左侧栏（工作区）**：顶部「新建会话」按钮；「对话」列表标题旁有「清空」按钮；每个会话项含图标、标题、修改时间与三点菜单（重命名会话 / 删除）。
- **主内容区**：性能栏（含采样参数配置）、消息区、底部输入栏（Provider、模型、质量、思考开关、发送按钮）。
- **未选中会话时**：主内容区显示空状态「选择一个会话或新建」。

## 3. 文档导航

| 编号 | 文档 | 内容 |
| --- | --- | --- |
| 4.2 | [创建会话](/zh/docs/manual/sessions/create-session/) | 选择 Provider、模型、质量等级、思考开关 |
| 4.3 | [流式对话](/zh/docs/manual/sessions/chat/) | SSE 流式输出、Token 统计、生成文件 |

## 4. 模块标签（i18n）

| i18n 键 | 中文标签 | 说明 |
| --- | --- | --- |
| `sessions` | 会话 | 顶部导航名 |
| `workspaces` / `chats` | 工作区 / 对话 | 左侧工作区与对话列表 |
| `newSession` | 新建会话 | 左侧顶部按钮 |
| `clearSessions` | 清空 | 一键清空全部会话 |
| `sessionRename` | 重命名会话 | 会话三点菜单项 |
| `selectModelForChat` | 选择模型 | 输入栏模型下拉占位 |
| `inputPlaceholder` / `messagePlaceholder` | 输入消息… / 给助手发消息 | 输入框占位提示 |
| `send` / `newline` | 发送 / 换行 | 发送（Enter）与换行（Shift+Enter） |
| `qualityHigh` / `qualityMedium` / `qualityLow` | 高 / 中 / 低 | 质量档位枚举 |
| `thinking` / `thinkingInProgress` | 思考 / 思考中 | 思考开关与流式思考块 |
| `fullAccess` | 完全访问 | 模块预留权限展示标签 |
| `produced` | 生成文件 | 模块预留会话产出文件标签 |
| `systemPrompt` | 系统提示词 | 创建会话的 `system_prompt` 参数 |

## 相关文档

- [使用手册总览](/zh/docs/manual/) — 六大模块手册索引
- [会话（Sessions）参考](/zh/docs/tools/sessions/) — 概念与参数参考
- [模拟调试环境（Mock）](/zh/docs/tools/mock/) — 无真实推理服务时联调会话功能