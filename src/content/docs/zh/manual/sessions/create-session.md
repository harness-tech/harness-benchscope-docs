---
title: 创建会话
description: 在 Sessions 页面创建会话：选择 Provider、模型、质量等级与思考开关的输入参数、字段限制、操作步骤与后台逻辑。
---

# 创建会话

本页说明如何在 Sessions 页面**创建会话**：选择 Provider、模型、质量等级与思考开关，并解释创建时后台执行的 API 调用与数据流。

## 1. 功能说明

- 点击左侧栏「**新建会话**」按钮即可创建会话，会话立即出现在「对话」列表并激活。
- 默认会话名为 `会话 MM/DD HH:mm`（如 `会话 09/09 21:00`）；发送第一条消息后自动改为消息内容前 50 个字符（自定义命名的会话保持不变）。
- 会话标识 **session_id** 格式为 `sess-MMDD-HHMMSS-<6位hex>`（如 `sess-0909-210000-a1b2c3`）。
- 底部输入栏的 Provider、模型、质量、思考开关等选择会随会话保存，供后续[流式对话](/zh/docs/manual/sessions/chat/)使用。

## 2. 页面结构

创建会话的控件集中在**左侧栏**与**底部输入栏**：

```
+----------------------------------+----------------------------------------------+
| 左侧栏（260px）                  | 主内容区                                       |
| +------------------------------+ | +--------------------------------------------+|
| | [ + 新建会话 ]  ← 入口按钮    | | | 性能栏 turns·steps | LLM | TTFT | TPOT | ITL ||
| +------------------------------+ | | + top_k [10]  temp [0.5]  top_p [1.0]       ||
| | 对话          [ 清空 ]        | | +--------------------------------------------+|
| +------------------------------+ | | 消息区                                       ||
| | · 会话 A   09-09 21:00   [···]| | +--------------------------------------------+|
| | · 会话 B   09-09 20:30   [···]| | | 输入框：给助手发消息                         ||
| +------------------------------+ | | Provider ▾  选择模型 ▾  质量 ▾  思考[✓]  (→) ||
+----------------------------------+----------------------------------------------+
```

| 控件 | 位置 | 说明 |
| --- | --- | --- |
| 新建会话 | 左侧栏顶部 | 创建新会话（i18n `newSession`） |
| Provider 下拉 | 底部输入栏 | 列表来自 `GET /api/config/providers`；切换后重新探测模型列表（i18n `selectInferenceProvider`） |
| 选择模型 | 底部输入栏 | 列表来自所选 Provider 的探测结果（i18n `selectModelForChat`） |
| 质量下拉 | 底部输入栏 | `high`/`medium`/`low`（高/中/低），默认「中」 |
| 思考开关 | 底部输入栏 | `enable_thinking`，默认开启 |
| top_k / temp / top_p | 顶部性能栏 | 采样参数，默认 10 / 0.5 / 1 |

## 3. 输入参数

| 字段 | 类型 | 限制/约束 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `provider_id` | string | 有效 Provider id | 激活的 Provider | 会话请求代理转发的目标 Provider |
| `model` | string | 该 Provider 的模型列表内 | 探测后的第一个模型 | 推理模型名 |
| `temperature` | number | 0 - 2 | 0.5 | 采样温度；显式传入时优先于 `quality` |
| `quality` | string | 枚举：`high` / `medium` / `low` | `medium` | 质量等级，映射温度 0.9 / 0.5 / 0.2 |
| `top_k` | int | 1 - 200 | 10 | 仅保留概率最高的 K 个候选 token |
| `top_p` | float | 0 - 1 | 1.0 | 核采样累积概率阈值 |
| `enable_thinking` | boolean | true / false | true | 思考开关 |

<div class="warning">
**max_tokens 固定 4096**，不在会话参数中开放配置。服务端转发 payload 时直接写入 `"max_tokens": 4096`。
</div>

创建会话接口（`POST /api/sessions`）的附加字段：

| 字段 | 类型 | 限制/约束 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `title` | string | ≤ 60 字符（重命名输入限制） | 自动生成 `会话 MM/DD HH:mm` | 会话名称 |
| `model` | string | 可选 | 空 | 初始模型 |
| `system_prompt` | string | 可选 | 空 | 系统提示词（i18n `systemPrompt`），每次对话前置一条 `system` 消息 |

## 4. 字段限制

| 字段 | 必填 | 类型 | 最小 | 最大 | 枚举 | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| `provider_id` | 否 | string | — | — | 已配置的 Provider id | 缺省或未知时回退激活 Provider 的全局 `api` 配置 |
| `model` | 否 | string | — | — | Provider 模型列表 | 缺省回退会话已选模型，再缺省为 `default` |
| `temperature` | 否 | number | 0 | 2 | — | 显式传入时覆盖 `quality` 映射 |
| `quality` | 否 | string | — | — | high / medium / low | 仅在 `temperature` 缺省时映射生效 |
| `top_k` | 否 | int | 1 | 200 | — | ≤ 0 时不写入转发 payload |
| `top_p` | 否 | float | 0 | 1 | — | 缺省不写入转发 payload |
| `enable_thinking` | 否 | boolean | — | — | true / false | 经 `chat_template_kwargs` 传递 |
| `max_tokens` | — | int | — | — | — | 固定 4096，不开放配置 |

## 5. 操作步骤（按钮操作）

1. 通过顶部导航进入「**会话**」页面（i18n `sessions`）。
2. 确认页面头部边框为**绿色**（所选 Provider 在线）；红色表示未配置或离线，需先到 Settings → Providers 配置，参见[设置（Settings）](/zh/docs/tools/settings/)。
3. 在底部输入栏点击 **Provider 下拉**，选择推理服务提供方。
4. 点击「**选择模型**」下拉，选择模型（探测完成后默认选中第一个）。
5. 点击**质量**下拉，选择 `high`（高）/ `medium`（中）/ `low`（低），默认「中」。
6. 切换「**思考**」开关（默认开启）。
7. （可选）在顶部性能栏调整 `top_k` / `temp` / `top_p`。
8. 点击左侧栏顶部「**新建会话**」按钮。
9. 新会话出现在「对话」列表并激活，输入框即可发送消息，参见[流式对话](/zh/docs/manual/sessions/chat/)。

## 6. 后台执行逻辑

加载页面与创建会话时，后台发生如下流程：

1. 页面加载（`onMounted`）：前端调用 `GET /api/sessions` 加载会话列表，调用 `GET /api/config/providers` 加载 Provider 列表（返回 `providers` 与 `active_provider`）。
2. 前端对选中 Provider 调用 `POST /api/config/test-connection`（提交 `base_url` / `endpoint` / `api_key` / `extra_headers`），获取模型列表与在线状态；在线时头部边框变绿。
3. 点击「新建会话」→ 前端调用 `POST /api/sessions`（body 如 `{"model": "qwen3-8b"}`）：
   - `SessionManager.create_session()` 生成 `sess-...` 格式 id，默认标题 `会话 MM/DD HH:mm`；
   - 会话立即持久化到 `~/.benchscope/sessions/<session_id>.json`，并写入可读日志 `~/.benchscope/logs/sessions/<session_id>.log`；
   - 接口返回 `{session: {...}}`。
4. 前端刷新会话列表（`GET /api/sessions`，按 `updated_at` 倒序）并激活新会话（`GET /api/sessions/{session_id}`）。

<div class="info">
**代理转发说明**：BenchScope **不提供** OpenAI 兼容的 `/v1/*` 推理端点。对话时服务端按 `provider_id` 从 Provider 列表解析 `base_url` / `endpoint` / `api_key`（缺省或未知时回退全局 `api` 配置，即**激活的 Provider**），将请求**代理转发**到目标 Provider 的 `base_url + endpoint`（默认 `/v1/chat/completions`）。
</div>

## 7. 常见问题

**问题：Provider 下拉为什么是空的？**
尚未配置任何 Provider。请先在 Settings → Providers 中至少配置并激活一个推理服务，参见[设置（Settings）](/zh/docs/tools/settings/)。

**问题：quality 和 temperature 有什么区别？**
`quality`（high/medium/low）映射为 `temperature` 0.9 / 0.5 / 0.2；显式传入 `temperature` 时优先使用。WebUI 默认始终发送 `temperature`，因此质量映射主要在直接调用 API 且未传 `temperature` 时生效。

**问题：能配置回复的最大长度吗？**
不能。会话 `max_tokens` 固定 4096，不在会话参数中开放配置。

**问题：重启服务后会话会丢失吗？**
不会。会话状态持久化于 `~/.benchscope/sessions/*.json`，服务重启后自动恢复。

## 相关文档

- [Sessions 手册概览](/zh/docs/manual/sessions/)
- [流式对话](/zh/docs/manual/sessions/chat/)
- [会话（Sessions）参考](/zh/docs/tools/sessions/)
- [设置（Settings）](/zh/docs/tools/settings/)