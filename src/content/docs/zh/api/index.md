---
title: "HTTP API"
---

# HTTP API

BenchScope 的 Web 后端基于 FastAPI 构建，提供 **OpenAI 兼容推理接口**、**平台 REST API** 与 **WebSocket** 三类接口。默认服务地址（Base URL）为：

```text
http://127.0.0.1:8080
```

> 服务地址取决于启动时的 `--host` / `--port`（默认 `0.0.0.0:8080`），见 [安装](/zh/docs/install/)。大多数接口返回 JSON，错误时使用标准的 HTTP 状态码。

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

## 相关文档

- [CLI](/zh/docs/cli/) — `serve` / `perf` / `eval` 命令
- [设置（Settings）](/zh/docs/tools/settings/) — Provider 与全局配置
- [会话（Sessions）](/zh/docs/tools/sessions/) — 会话式推理交互
- [架构介绍](/zh/docs/tools/architecture/) — 后端模块与路由划分
