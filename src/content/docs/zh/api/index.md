---
title: "概述"
---

# 概述

BenchScope 的 Web 后端基于 FastAPI 构建，提供 **OpenAI 兼容推理接口**、**平台 REST API** 与 **WebSocket** 三类接口。默认服务地址（Base URL）为：

```text
http://127.0.0.1:8080
```

<div class="info">

**info**：

服务地址取决于启动时的 `--host` / `--port`（默认 `0.0.0.0:8080`），见 [安装](/zh/docs/install/)。大多数接口返回 JSON，错误时使用标准的 HTTP 状态码。

</div>

## 会话式推理（OpenAI 兼容）

BenchScope 的会话（Sessions）与推理链路遵循 OpenAI 兼容协议，便于接入任意 OpenAI 客户端 / 工具：

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| `/v1/models` | GET | 列出当前可用的推理模型 |
| `/v1/chat/completions` | POST | 会话补全（Chat Completions），支持流式（SSE）输出 |

```bash
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"Qwen2.5-7B","messages":[{"role":"user","content":"Hello"}],"stream":true}'
```

<div class="tip">

**tip**：

将 `"stream":true` 改为 `false` 即可关闭流式输出，一次性返回完整响应。任何标准 OpenAI 客户端（如 `openai` SDK、curl）都可直接对接。

</div>

## 健康与版本

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| `/api/version` | GET | 服务版本号 |
| `/api/dashboard/stats` | GET | Dashboard 概览统计（Performance / Accuracy / Sessions / Models / Datasets / Providers 计数） |
| `/api/dashboard/env` | GET | 环境信息（MAC / IP / 子网、框架与操作系统版本） |
| `/api/config/status` | GET | 配置与 Provider 可用状态 |

```bash
curl http://127.0.0.1:8080/api/version
```

## 任务与评测

性能压测与精度评测任务可通过 REST 接口创建与管理（与 Web 创建的任务完全兼容）：

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| `/api/tasks` | GET / POST | 列出 / 创建性能测试任务；`POST /api/tasks/preview` 预览命令 |
| `/api/tasks/{task_id}` | GET / DELETE | 查询 / 删除任务 |
| `/api/tasks/{task_id}/start` · `/stop` | POST | 启动 / 停止任务 |
| `/api/tasks/{task_id}/logs` | GET | 任务的实时日志 |
| `/api/tasks/{task_id}/export` | GET | 导出任务产物（zip） |
| `/api/accuracy/tasks` | GET / POST | 列出 / 创建精度评测任务 |
| `/api/accuracy/tasks/{task_id}/samples` | GET | 单样本溯源（samples.jsonl） |
| `/api/accuracy/tasks/{task_id}/benchmark` | GET | 基线对标结果 |
| `/api/accuracy/estimate` | GET | Token 消耗预估算 |

<div class="tip">

**tip**：

任务也可通过 [CLI](/zh/docs/cli/) 创建：`benchscope perf` 与 `benchscope eval` 与网页任务产物完全等价，可按需选择终端或 HTTP 方式。

</div>

## 配置与会话

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| `/api/config` | GET / POST | 读取 / 更新全局配置（settings.json） |
| `/api/config/providers` | GET / POST / PUT / DELETE | Provider（Base URL / API Key）管理 |
| `/api/config/models` · `/datasets` | GET | 内置模型 / 数据集清单 |
| `/api/sessions` | GET / POST / DELETE | 会话列表与新建 / 清空 |
| `/api/sessions/{session_id}/chat` | POST | 向会话发送消息（SSE 流式返回） |
| `/api/logs/runs` | GET | 历史任务记录（Perfs） |
| `/ws` | WebSocket | 实时推送（任务进度 / 实时指标） |

## 鉴权

本地默认**无鉴权**。若被测服务需要 API Key，请通过 [Settings → Providers](/zh/docs/tools/settings/) 配置；接口本身默认不要求额外令牌。

## 常见问题

**问题：如何确认服务是否正常启动？**
访问 `http://127.0.0.1:8080/api/version`（或刷新可用的根地址），返回版本号即表明服务已就绪。

**问题：能否直接用 curl 调用会话接口？**
可以。上面的 `/v1/chat/completions` 示例即为可直接运行的 curl 命令，支持 OpenAI 兼容的请求体与 SSE 流式输出。

**问题：如何让第三方服务使用我的 API Key？**
在 [Settings → Providers](/zh/docs/tools/settings/) 中为对应 Provider 配置 Base URL 与 API Key。被测服务的鉴权与 BenchScope 自身的接口鉴权是分开的。

**问题：如何通过 HTTP 创建并预览一个性能任务？**
向 `POST /api/tasks/preview` 提交任务条件即可预览将执行的命令；确认后通过 `POST /api/tasks` 创建任务，再用 `POST /api/tasks/{task_id}/start` 启动。

<div class="info">

**info**：

上述接口与 Web 创建的任务完全兼容，产物可在 **Datas → Perfs** 查看 / 导入。

## 相关文档

- [CLI](/zh/docs/cli/) — `serve` / `perf` / `eval` 命令
- [设置（Settings）](/zh/docs/tools/settings/) — Provider 与全局配置
- [会话（Sessions）](/zh/docs/tools/sessions/) — 会话式推理交互
- [架构介绍](/zh/docs/tools/architecture/) — 后端模块与路由划分
