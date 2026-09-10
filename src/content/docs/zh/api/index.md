---
title: "概述"
description: "BenchScope Web API 概述：基于 FastAPI 的平台 REST API 与 WebSocket 接口清单，覆盖配置、任务、日志、会话、精度评测、引擎与技能等模块。"
---

# 概述

BenchScope 的 Web 后端基于 FastAPI 构建，提供 **平台 REST API** 与 **WebSocket** 两类接口，覆盖配置、任务、日志、概览、会话、精度评测、引擎与技能等模块。默认服务地址（Base URL）为：

```text
http://127.0.0.1:8080
```

<div class="info">

**info**：

服务地址取决于启动时的 `--host` / `--port`（默认 `0.0.0.0:8080`），见 [安装](/zh/docs/install/)。大多数接口返回 JSON，错误时使用标准的 HTTP 状态码。

</div>

<div class="warning">

**warning**：

BenchScope **自身不提供** OpenAI 兼容的 `/v1/models`、`/v1/chat/completions` 推理端点。会话（Sessions）功能是把请求**代理转发**到当前激活的 Provider（OpenAI 兼容端点）；性能 / 精度测试也是**调用**外部推理服务，而非对外暴露推理接口。

</div>

## 接口总览

后端按模块划分 API 分组，共 **9 个路由组 + 版本 + WebSocket**：

| 分组 | 前缀 | 职责 |
| --- | --- | --- |
| `api_config` | `/api/config` | 全局配置、Provider、模型 / 数据集、目录、重启 |
| `api_tasks` | `/api/tasks` | 性能测试任务管理（创建 / 启动 / 停止 / 日志 / 导出） |
| `api_logs` | `/api/logs` | 日志与历史运行（列表 / 详情 / 实时 / 备份 / 导入 / 汇总） |
| `api_dashboard` | `/api/dashboard` | 概览统计 / 环境信息 |
| `api_sessions` | `/api/sessions` | 会话对话（SSE 流式） |
| `api_test` | `/api/test` | 精度测试 legacy 接口（start / preview / stop / status） |
| `api_accuracy` | `/api/accuracy` | 精度评测任务（任务 / 样本 / 对标 / 引擎 / 数据集 / 预估 / 基线） |
| `api_benchs` | `/api/benchs` | 内置引擎（清单 / 详情 / 环境校验 / 上传 / 导入 / 参数） |
| `api_skills` | `/api/skills` | 内置技能（清单 / 下载） |
| 版本 | `/api/version` | 服务版本号 |
| WebSocket | `/ws` | 实时推送（任务进度 / 实时指标） |

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

## 配置（api_config）

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| `/api/config` | GET / POST | 读取 / 更新全局配置（settings.json） |
| `/api/config/providers` | GET / POST | Provider 列表 / 新增 |
| `/api/config/providers/{provider_id}` | PUT / DELETE | 更新 / 删除 Provider |
| `/api/config/providers/{provider_id}/activate` | POST | 激活指定 Provider |
| `/api/config/status` | GET | 配置与 Provider 可用状态 |
| `/api/config/models` | GET | 内置模型清单 |
| `/api/config/test-connection` | POST | 测试 Provider 连接 |
| `/api/config/gpu` | GET | GPU 信息 |
| `/api/config/params/{framework}` | GET | 框架参数（JSON） |
| `/api/config/params-yaml/{framework}` | GET / PUT | 框架参数（YAML 读写） |
| `/api/config/datasets` | GET | 内置数据集清单 |
| `/api/config/model-catalog` | GET | 模型目录 |
| `/api/config/datasets/download` | POST | 下载数据集 |
| `/api/config/dirs` | GET / POST | 数据目录读写 |
| `/api/config/restart` | POST | 重启服务 |

## 性能任务（api_tasks）

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| `/api/tasks` | GET / POST | 列出 / 创建性能测试任务 |
| `/api/tasks/preview` | POST | 预览任务命令 |
| `/api/tasks/{task_id}` | GET / DELETE | 查询 / 删除任务 |
| `/api/tasks/{task_id}/logs` | GET | 任务的实时日志 |
| `/api/tasks/{task_id}/threshold` | PATCH | 更新任务阈值配置 |
| `/api/tasks/{task_id}/start` | POST | 启动任务 |
| `/api/tasks/{task_id}/stop` | POST | 停止任务 |
| `/api/tasks/{task_id}/export` | POST | 导出任务产物（zip） |
| `/api/tasks/{task_id}/preview` | POST | 预览单个任务命令 |

## 日志与历史运行（api_logs）

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| `/api/logs/runs` | GET | 历史运行记录（Perfs） |
| `/api/logs/runs/{run_id}` | GET / DELETE | 查询 / 删除运行 |
| `/api/logs/runs/{run_id}/live` | GET | 运行实时日志（SSE） |
| `/api/logs/runs/{run_id}/backup` | GET | 打包备份（扁平 zip） |
| `/api/logs/runs/import` | POST | 导入备份 zip 恢复任务 |
| `/api/logs/runs/{run_id}/preview` | GET | 运行详情预览 |
| `/api/logs/runs/{run_id}/download` | GET | 下载运行产物 |
| `/api/logs/runs/{run_id}/summary` | GET | 运行汇总（指标） |
| `/api/logs/datasets` | GET | 数据集列表 |
| `/api/logs/datasets/upload` | POST | 上传数据集 |
| `/api/logs/datasets/{name}` | DELETE | 删除数据集 |
| `/api/logs/datasets/sharegpt` | GET | ShareGPT 数据集状态 |
| `/api/logs/datasets/sharegpt/download` | POST | 下载 ShareGPT 数据集 |

## 会话（api_sessions）

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| `/api/sessions` | GET / POST / DELETE | 会话列表 / 新建 / 清空全部 |
| `/api/sessions/{session_id}` | GET / DELETE | 查询 / 删除会话 |
| `/api/sessions/{session_id}/chat` | POST | 向会话发送消息（SSE 流式返回，代理到激活 Provider） |
| `/api/sessions/{session_id}/perf` | PATCH | 更新会话性能参数 |
| `/api/sessions/{session_id}/title` | PATCH | 重命名会话 |

<div class="info">

**info**：

`/api/sessions/{session_id}/chat` 会把请求**代理转发**到当前激活的 Provider（OpenAI 兼容端点）。BenchScope 自身不暴露 `/v1/*` 推理端点；会话参数（`temperature` / `top_p` / `top_k` / `quality` / `enable_thinking`）见[会话（Sessions）](/zh/docs/tools/sessions/)。

</div>

## 精度测试 legacy（api_test）

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| `/api/test/start` | POST | 启动精度测试（legacy） |
| `/api/test/preview` | POST | 预览精度测试（legacy） |
| `/api/test/stop` | POST | 停止精度测试（legacy） |
| `/api/test/status` | GET | 查询精度测试状态（legacy） |

> `api_test` 为精度测试的 **legacy 接口**，新代码建议使用 `api_accuracy` 路由组。

## 精度评测（api_accuracy）

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| `/api/accuracy/tasks` | GET / POST | 列出 / 创建精度评测任务 |
| `/api/accuracy/tasks/{task_id}` | GET / DELETE | 查询 / 删除任务 |
| `/api/accuracy/tasks/{task_id}/stop` | POST | 停止任务 |
| `/api/accuracy/tasks/{task_id}/samples` | GET | 单样本溯源（samples.jsonl） |
| `/api/accuracy/tasks/{task_id}/export-samples` | GET | 导出样本 |
| `/api/accuracy/tasks/{task_id}/benchmark` | GET | 基线对标结果 |
| `/api/accuracy/engines` | GET | 精度引擎清单 |
| `/api/accuracy/engines/{engine_id}/env-check` | GET | 引擎环境校验 |
| `/api/accuracy/datasets` | GET | 精度数据集清单 |
| `/api/accuracy/datasets/import` | POST | 导入自定义数据集 |
| `/api/accuracy/datasets/{dataset_id}` | DELETE | 删除数据集 |
| `/api/accuracy/datasets/preview` | POST | 预览数据集 |
| `/api/accuracy/datasets/stats` | POST | 数据集统计 |
| `/api/accuracy/estimate` | GET | Token 消耗预估算 |
| `/api/accuracy/baselines` | GET / PUT | 基线库读写 |
| `/api/accuracy/compare` | POST | 对标对比 |

## 引擎（api_benchs）

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| `/api/benchs` | GET | 引擎清单 |
| `/api/benchs/{engine_id}` | GET | 引擎详情 |
| `/api/benchs/{engine_id}/mock` | POST | 设置引擎 Mock 开关 |
| `/api/benchs/authoring` | GET | 引擎编写契约 |
| `/api/benchs/upload` | POST | 上传自定义引擎 |
| `/api/benchs/import` | POST | 导入引擎 |
| `/api/benchs/config/yaml` | GET / PUT | 引擎配置 YAML 读写 |
| `/api/benchs/{engine_id}/params` | GET | 引擎参数（JSON） |
| `/api/benchs/{engine_id}/params-yaml` | GET / PUT | 引擎参数 YAML 读写 |
| `/api/benchs/{engine_id}/params/{param_key}/option-desc` | GET | 参数选项说明 |
| `/api/benchs/{engine_id}/env-check` | GET | 引擎环境校验 |

## 技能（api_skills）

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| `/api/skills` | GET | 内置技能清单 |
| `/api/skills/{skill_id}/download` | GET | 下载技能包（tar.gz） |

## 实时推送（WebSocket）

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| `/ws` | WebSocket | 实时推送（任务进度 / 实时指标） |

## 鉴权

本地默认**无鉴权**。若被测服务需要 API Key，请通过 [Settings → Providers](/zh/docs/tools/settings/) 配置；接口本身默认不要求额外令牌。

## 常见问题

**问题：如何确认服务是否正常启动？**
访问 `http://127.0.0.1:8080/api/version`（或刷新根地址），返回版本号即表明服务已就绪。

**问题：BenchScope 是否提供 OpenAI 兼容的 `/v1/chat/completions` 端点？**
**不提供。** BenchScope 自身不暴露 `/v1/*` 推理端点。会话功能是**代理转发**到当前激活的 Provider（OpenAI 兼容端点）；性能 / 精度测试也是**调用**外部推理服务，而非对外暴露推理接口。

**问题：能否直接用 curl 调用会话接口？**
可以。`POST /api/sessions/{session_id}/chat` 即为会话接口，返回 SSE 流式数据；它会把请求代理到当前激活的 Provider（OpenAI 兼容端点）。

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
- [性能核心指标](/zh/docs/performance/metrics/) — 性能任务输出指标口径
- [精度核心指标](/zh/docs/accuracy/metrics/) — 精度任务输出指标口径
- [会话（Sessions）](/zh/docs/tools/sessions/) — 会话接口与采样参数