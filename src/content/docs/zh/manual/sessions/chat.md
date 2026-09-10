---
title: 流式对话
description: Sessions 模块流式对话操作指南：SSE 流式输出、Token 统计、生成文件，含后台代理转发逻辑与 SSE 事件协议。
---

# 流式对话

本页说明如何在 Sessions 页面发送消息、查看 **SSE 流式输出**、统计 Token 指标，以及会话运行产出的文件，并解释点击「发送」后后台的代理转发与数据流。

## 1. 功能说明

- 在输入框输入消息后按 Enter 或点击发送按钮，模型回复以 **SSE 流式**逐 token 呈现，支持 **Markdown 渲染**与代码高亮（代码块带语言标签与 Copy 按钮）。
- 模型思考过程以「**思考中**」折叠块展示（`reasoning_content` 增量或 think 标签解析）。
- 会话头部性能栏实时统计 **Token 指标**（TTFT、tok/s、TPOT、ITL 等）。
- Shift+Enter 换行；流式输出期间可点击停止按钮中止（已生成内容保留）。

## 2. 页面结构

流式对话的界面由**消息区**与**底部输入栏**组成：

```
+--------------------------------------------------------------+
| 性能栏 turns·steps | LLM | TTFT | TPOT | ITL + top_k/temp/top_p |
+--------------------------------------------------------------+
| 消息区：U 用户气泡（右） / AI 助手气泡（左）                    |
|   [思考中 ▾] 思考块（默认折叠，流式中滚动三点）                 |
|   回复正文（Markdown + 代码高亮 + Copy）+ 流式行闪烁光标         |
+--------------------------------------------------------------+
| 输入框（Enter 发送 / Shift+Enter 换行，流式中禁用）             |
| Provider ▾  选择模型 ▾  质量 ▾  思考[✓]  (发送/停止)             |
+--------------------------------------------------------------+
```

- **消息区**：用户消息居右（头像 `U`），助手消息居左（头像为蓝色 logo）；思考块可点击展开/折叠。
- **输入栏**：流式输出期间输入框禁用；发送按钮变为**停止**方块，点击可中止当前流。

## 3. 输入参数

发送消息接口（`POST /api/sessions/{session_id}/chat`）的请求体字段：

| 字段 | 类型 | 限制/约束 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `message` | string | 非空 | — | 本次用户消息 |
| `model` | string | Provider 模型列表内 | 会话已选模型 | 推理模型名 |
| `quality` | string | 枚举：`high` / `medium` / `low` | 会话已存值 | 质量等级，映射温度 0.9 / 0.5 / 0.2 |
| `enable_thinking` | boolean | true / false | true | 思考开关 |
| `provider_id` | string | 有效 Provider id | 会话已存值 | 代理转发的目标 Provider |
| `top_k` | int | 1 - 200 | 10 | Top-K 采样 |
| `temperature` | number | 0 - 2 | 0.5 | 采样温度；显式传入时优先于 `quality` |
| `top_p` | float | 0 - 1 | 1.0 | 核采样阈值 |

<div class="warning">
**max_tokens 固定 4096**，不在会话参数中开放配置。服务端转发 payload 中固定写入 `"max_tokens": 4096`。
</div>

## 4. 字段限制

| 字段 | 必填 | 类型 | 最小 | 最大 | 枚举 | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| `message` | 是 | string | 1 | — | — | 空消息前端不允许发送 |
| `model` | 否 | string | — | — | Provider 模型列表 | 缺省回退会话已选模型，再缺省为 `default` |
| `quality` | 否 | string | — | — | high / medium / low | 仅在 `temperature` 缺省时映射生效 |
| `enable_thinking` | 否 | boolean | — | — | true / false | 经 `chat_template_kwargs` 传递 |
| `provider_id` | 否 | string | — | — | 已配置的 Provider id | 缺省或未知时回退激活 Provider 的全局 `api` 配置 |
| `top_k` | 否 | int | 1 | 200 | — | ≤ 0 时不写入转发 payload |
| `temperature` | 否 | number | 0 | 2 | — | 显式传入时覆盖 `quality` 映射 |
| `top_p` | 否 | float | 0 | 1 | — | 缺省不写入转发 payload |
| `max_tokens` | — | int | — | — | — | 固定 4096，不开放配置 |

## 5. 操作步骤（按钮操作）

1. 在「对话」列表中点击一个会话（或先按[创建会话](/zh/docs/manual/sessions/create-session/)新建）。
2. 在底部输入栏确认 **Provider**、**选择模型**、**质量**、「思考」开关符合预期。
3. 点击输入框输入消息；需要换行时按 **Shift+Enter**（i18n `newline`）。
4. 按 **Enter**（i18n `send`）或点击右侧**发送**按钮，发起流式对话。
5. 流式输出期间：
   - 「思考中」折叠块实时显示思考内容（可点击展开）；
   - 回复正文逐 token 追加，代码块完成后显示语言标签与 Copy 按钮；
   - 左侧会话项图标变为**滚动三点**动画，性能栏实时刷新。
6. 如需中止：点击发送按钮变成的**停止**方块；已生成的部分内容保留在会话中。
7. 发送完成后，性能栏记录本次指标，会话自动落盘。

## 6. 后台执行逻辑

点击发送后，后台发生如下流程（数据流：浏览器 → BenchScope 服务端 → 激活的 Provider）：

1. 前端对 `POST /api/sessions/{session_id}/chat` 发起 `fetch`（body 见第 3 节），以 `text/event-stream` 方式读取 SSE 流。
2. 服务端 `api_sessions.chat()` 校验会话存在（不存在返回 404 "Session not found"），进入 `SessionManager.stream_chat()`：
   - 解析模型：`model` → 会话已选模型 → `default`；
   - 持久化配置：会话的 `model` / `provider_id` / `quality` / `enable_thinking`；
   - 写入用户消息（`add_message`），刷新 `~/.benchscope/sessions/<session_id>.json` 与会话日志；首条消息会触发会话标题自动更新。
3. 解析 Provider API 配置：按 `provider_id` 从 Provider 列表取 `base_url` / `endpoint` / `api_key` / `extra_headers`；**缺省或未知时回退全局 `api` 配置（即激活的 Provider）**。
4. 组装转发 payload：`model`、`messages`（`system_prompt` 前置 + 全部历史消息）、`stream: true`、**`max_tokens: 4096`**（固定）、`temperature`（显式值或 `quality` 映射：high=0.9 / medium=0.5 / low=0.2）、`top_k`（>0 时）、`top_p`、`chat_template_kwargs: {enable_thinking}`。
5. 服务端向 `{base_url}{endpoint}`（默认 `/v1/chat/completions`）发起 `POST`（`Authorization: Bearer <api_key>`，timeout 120s），**流式代理转发** Provider 的 SSE 响应。
6. 逐行解析 Provider SSE（`data: {...}`）：`choices[0].delta.content` → `token` 事件；`delta.reasoning_content` 或 think 标签解析结果 → `thinking` 事件；遇 `data: [DONE]` 结束；完成后持久化助手回复并发 `done` 事件。

SSE 事件协议（`data:` 后均为 JSON）：

| 事件 | 示例 | 说明 |
| --- | --- | --- |
| `token` | `data: {"token": "你好"}` | 回复正文增量 |
| `thinking` | `data: {"thinking": "让我想想…"}` | 思考过程增量 |
| `error` | `data: {"error": "API error: 500 ..."}` | 错误信息（非 200 或请求异常） |
| `done` | `data: {"done": true}` | 本次生成结束 |

<div class="info">
**代理转发说明**：BenchScope **不提供** OpenAI 兼容的 `/v1/*` 推理端点。会话请求由服务端**代理转发**到激活的 Provider（OpenAI 兼容端点）：`provider_id` 缺省或未知时使用全局 `api` 配置（由激活的 Provider 同步而来），否则转发到指定 Provider 的 `base_url + endpoint`。
</div>

## 7. Token 统计

性能栏指标由**前端客户端**在接收 SSE 流过程中统计（流式中显示实时值），发送完成后通过 `PATCH /api/sessions/{session_id}/perf` 持久化到会话，重新打开会话时恢复展示：

| 指标 | 含义 | 计算方式 |
| --- | --- | --- |
| `turns` | 对话轮数 | 用户消息条数 |
| `steps` | 消息步数 | 用户 + 助手消息总条数 |
| `llmTime` | 本次请求总耗时 | 完成时刻 − 发送时刻 |
| `ttft` | 首 token 延迟 | 首个 `token` 事件时刻 − 发送时刻 |
| `tokPerSec` | 解码速率 | token 数 ÷（完成时刻 − 首 token 时刻） |
| `tpot` | 每 token 平均耗时 | （完成时刻 − 首 token 时刻）÷ token 数 |
| `itl` | 平均 token 间隔 | Σ(相邻 token 时间差) ÷（token 数 − 1） |

## 8. 生成文件

会话运行过程中会产出以下文件（Sessions 模块以 `produced` 标签「生成文件」标识会话产出物）：

| 文件 | 路径 | 说明 |
| --- | --- | --- |
| 会话状态 | `~/.benchscope/sessions/<session_id>.json` | 完整会话数据（消息、配置、perf），每次消息变更刷新 |
| 会话日志 | `~/.benchscope/logs/sessions/<session_id>.log` | 可读对话日志（含 `# Session` / `# ID` / `# Model` / `# Provider` 头与 `[timestamp] role` 消息体，思考内容带 `[thinking]` 行） |
| 回复内代码块 | 消息区内联 | 模型回复中的代码块经 Markdown 渲染，带语言标签与 Copy 按钮 |

会话日志为纯文本，可直接查看或留存；删除或清空会话时，对应的 `.json` 与 `.log` 会一并删除。

## 9. 常见问题

**问题：发送消息后一直没有任何输出？**
先确认页面头部边框为绿色（Provider 在线）；再检查 `base_url` / `endpoint` / `api_key` 配置。服务端连接失败时会以 `error` 事件返回（如 `Request failed: ...`），页面弹出错误提示。

**问题：思考块里为什么没有内容？**
该模型未输出思考过程（无 `reasoning_content` 且回复中无 think 标签），或发送时「思考」开关为关；开关状态随会话保存。

## 相关文档

- [Sessions 手册概览](/zh/docs/manual/sessions/)
- [创建会话](/zh/docs/manual/sessions/create-session/)
- [会话（Sessions）参考](/zh/docs/tools/sessions/)
- [模拟调试环境（Mock）](/zh/docs/tools/mock/)