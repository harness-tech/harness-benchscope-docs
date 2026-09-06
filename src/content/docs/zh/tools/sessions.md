---
title: "会话（Sessions）"
---

# 会话（Sessions）

Sessions 提供基于会话的**交互式使用方式**：配置采样参数、发送消息并实时查看 **SSE 流式输出**，支持 Markdown 渲染 + 代码高亮、思考（reasoning）解析与性能栏，让你像使用聊天工具一样直接与大模型对话。

![BenchScope Sessions 会话界面](/images/benchscope_sessions.png)

<div class="tip">

**tip**：

会话（Sessions）与压测 / 评测不同——前者是**交互式对话**，后者是**批量施压 / 批量评测**。你可以先用会话验证模型的回答质量，再进行正式的压测与评测。

</div>

## 主要能力

- **采样参数**：配置生成参数（`temperature` / `top_p` 等）后发起会话请求。
- **Markdown 渲染**：输出支持 Markdown 渲染与代码语法高亮（highlight.js + 深色主题）。
- **SSE 流式**：流式输出实时呈现，含思考过程解析。
- **会话管理**：侧栏会话项、切换/重命名、按会话日志落盘、清空居中确认弹窗。
- **性能栏**：展示本次请求的性能信息（如耗时、Token 等）。

## 使用流程

1. 在 **Sessions** 页**新建会话**；
2. 配置**采样参数**（`temperature` / `top_p` 等）；
3. **发送消息**，实时查看流式输出与思考过程；
4. 会话**自动缓存**；可按会话**重命名**或**导出日志**。

### 采样参数说明

| 参数 | 说明 |
| --- | --- |
| `temperature` | 采样温度，越高输出越随机 |
| `top_p` | 核采样概率，在累积概率阈值内采样 |
| `max_tokens` | 单次回复最大输出 token 数 |

<div class="info">

**info**：

这些采样参数与 [CLI](/zh/docs/cli/) 中 `perf` / `eval` 的采样参数一致，便于在会话、压测、评测之间保持一致口径。

</div>

## 界面组成

**侧栏**：

- 会话列表，支持切换与**重命名**；
- 每个会话按会话日志**独立落盘**；
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
- [性能测试](/zh/docs/performance/) — 对模型做正式压测
- [概述](/zh/docs/accuracy/) — 对模型做量化评测
