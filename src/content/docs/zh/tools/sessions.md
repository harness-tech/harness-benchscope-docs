---
title: "会话（Sessions）"
description: "Sessions 会话式交互：配置采样参数、实时查看 SSE 流式输出，支持 Markdown 渲染、思考解析与性能栏。"
---

# 会话（Sessions）

Sessions 提供**会话式交互**：配置采样参数、发送消息并实时查看 **SSE 流式输出**，支持 Markdown 渲染 + 代码高亮、思考（reasoning）解析与性能栏，让你像使用聊天工具一样直接与大模型对话。

![BenchScope Sessions 会话界面](/images/benchscope_sessions.png)

<div class="tip">

**tip**：

会话（Sessions）与压测 / 评测不同——前者是**交互式对话**，后者是**批量施压 / 批量评测**。你可以先用会话验证模型的回答质量，再进行正式的压测与评测。

</div>

## 主要能力

- **采样参数**：配置生成参数（`temperature` / `top_p` / `top_k` / `quality` 等）后发起会话请求。
- **思考开关**：`enable_thinking` 控制模型思考过程（vLLM / SGLang 经 `chat_template_kwargs` 传递）。
- **Markdown 渲染**：输出支持 Markdown 渲染与代码语法高亮（highlight.js + 深色主题）。
- **SSE 流式**：流式输出实时呈现，含思考过程（`reasoning_content` 增量）解析。
- **会话管理**：侧栏会话项、切换/重命名、按会话日志落盘、清空居中确认弹窗。
- **性能栏**：展示本次请求的性能信息（如耗时、Token 等）。

<div class="info">

**info**：

会话请求由服务端**代理转发**到当前激活的 Provider（OpenAI 兼容端点）——BenchScope 本身不暴露 `/v1/*` 端点。因此会话功能依赖 Settings → Providers 中配置的推理服务可用；无真实服务时可使用[模拟调试环境](/zh/docs/tools/mock/)的 mock OpenAI 服务联调。

</div>

## 使用流程

1. 在 **Sessions** 页**新建会话**；
2. 配置**采样参数**（`temperature` / `top_p` 等）；
3. **发送消息**，实时查看流式输出与思考过程；
4. 会话**自动缓存**；可按会话**重命名**或**导出日志**。

### 采样参数说明

| 参数 | 说明 |
| --- | --- |
| `model` | 会话使用的模型名（缺省回退到会话已选模型） |
| `temperature` | 采样温度（0–2），越高输出越随机；显式设置时优先于 `quality` |
| `quality` | 质量档位：high（0.9）/ medium（0.5）/ low（0.2），未显式设置 `temperature` 时映射为温度值 |
| `top_k` | Top-K 采样，只保留概率最高的 K 个候选 token |
| `top_p` | 核采样概率，在累积概率阈值内采样 |
| `enable_thinking` | 思考开关，控制模型思考过程（vLLM / SGLang 经 `chat_template_kwargs` 传递） |
| `provider_id` | 会话代理转发到的 Provider（缺省使用激活的 Provider） |

> 单次回复的 `max_tokens` 由服务端固定为 4096，不在会话参数中开放配置。

<div class="info">

**info**：

会话的采样参数与 [CLI](/zh/docs/cli/) 中 `eval` 的采样参数（`temperature` / `top_p` / `max-tokens` 等）口径一致，便于在会话、压测、评测之间保持一致的生成设置。

</div>

## 界面组成

**侧栏**：

- 会话列表，支持切换与**重命名**；
- 每个会话的日志**独立落盘**；
- 清空操作带**居中确认弹窗**，防止误操作。

**主区域**：

- 流式输出区（SSE），支持 Markdown 渲染与代码高亮；
- 思考过程（reasoning）解析展示；
- 底部性能栏展示本次请求的性能信息。

## 常见问题

**问题：输出没有实时滚动？**

确认会话使用 SSE 流式输出；如网络层有代理，SSE 长连接可能被中断，可检查服务端日志。

**问题：如何导出某次会话？**

在侧栏选择会话并使用导出 / 落盘能力。会话缓存保存在数据根目录的 `sessions` 子目录下（默认 `~/.benchscope/sessions/`），见 [配置说明](/zh/docs/install/configuration/)（`sessions_dir`）。

## 相关文档

- [配置说明](/zh/docs/install/configuration/) — 会话缓存目录 `sessions_dir`
- [设置（Settings）](/zh/docs/tools/settings/) — 驱动会话请求的 Provider 配置
- [模拟调试环境（Mock）](/zh/docs/tools/mock/) — 无真实服务时联调会话功能
- [性能测试](/zh/docs/performance/) — 对模型做正式压测
- [概述](/zh/docs/accuracy/) — 对模型做量化评测