---
title: "创建压测任务"
description: "BenchScope 性能压测任务创建三步向导手册：性能条件（引擎/Provider/条件组）、性能参数（各引擎分组参数）、启动测试（预览命令与 Token 预估）。"
---

# 创建压测任务

本文讲解创建压测任务的三步向导：**性能条件 → 性能参数 → 启动测试**。入口为性能测试页介绍页的「并发模式 / 阈值模式」按钮，路由 `/performance/create?mode=concurrency|threshold`（模式由入口决定，向导中不可切换）。

## 1. 功能说明

| 项 | 说明 |
| --- | --- |
| 入口 | 性能测试介绍页「并发模式」/「阈值模式」按钮 |
| 测试引擎 | Bench CLI（自研，无环境依赖）/ vLLM 原生 / SGLang 原生；原生引擎需本地环境校验通过 |
| 被测服务 | 从 Settings 配置的 Provider（OpenAI 兼容接口）中选择，并实时探测模型列表 |
| 产物 | 创建并启动任务后自动回到性能测试页，进入执行监控视图（见 [实时监控与曲线](/zh/docs/manual/performance/live-metrics/)） |

## 2. 页面结构

```
┌──────────────────────────────────────────────────────────┐
│ Header: [←] Create Perf Test                [并发模式]    │
├──────────────────────────────────────────────────────────┤
│ 步骤条: ① 性能条件  ② 性能参数  ③ 启动测试                │
├──────────────────────────────────────────────────────────┤
│ Step 1: 测试引擎（下拉 + 环境校验标签/明细）              │
│        Provider 面板（Provider/Base URL/模型/在线状态）   │
│        Max Requests（仅阈值模式）                         │
│        条件面板（条件组 ×N：输入/输出/数据集/请求数/阈值） │
│ Step 2: 所选引擎标识 + 分组参数列表（行内编辑）           │
│ Step 3: Preview Conditions + Preview Command（可复制）    │
├──────────────────────────────────────────────────────────┤
│ Footer: [取消] [上一步] [下一步 / 启动]                   │
└──────────────────────────────────────────────────────────┘
```

## 3. 输入参数

### 3.1 Step 1 · 性能条件

| 字段 | 类型 | 限制/约束 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| 测试引擎 | 枚举下拉 | `benchscope` / `vllm-*` / `sglang-*`；原生引擎需 `env-check` 通过 | `benchscope` | 决定 Step 2 参数清单与命令形态 |
| Provider | 枚举下拉 | Settings 中已配置的 Provider | 第一个 | 决定 Base URL 与 API Key |
| 模型 | 枚举下拉 | 探测结果填充（`POST /api/config/test-connection`）；**必填** | 探测后第一个 | 被测模型 |
| Max Requests | 整数 | ≥ 1（阈值模式才显示） | 4096 | 下一次执行请求数上限，超限强制结束 |
| 输入 | 整数 | 最多 6 位；失焦 ≤0 时重置 1024 | 1024 | 每组输入 token 长度 |
| 输出 | 整数 | 同上 | 1024 | 每组输出 token 长度 |
| 数据集 | 枚举 | 当前仅 `Random` | `Random` | 后端另支持 `sharegpt`（自动从 ModelScope 下载）/ `custom` |
| 请求数条件 | 正整数集合 | 自动去重、升序；并发模式第 1 组必填 | `1,2,4,8,16,32,40,64,128` | 每组并发（请求数）档位 |
| TTFT 阈值 | 统计量 + 整数 | 统计量 `mean/median/p99`；整数 ≥0（阈值模式） | `mean` + 0 | `0` = 该条件不参与判定 |
| TPOT 阈值 | 统计量 + 整数 | 同上 | `mean` + 100 | `0` = 该条件不参与判定 |
| 输出吞吐阈值 | 整数 | ≥ 0（阈值模式），单位 tok/s | 0 | `0` = 该条件不参与判定 |

### 3.2 Step 2 · 性能参数

参数**跟随 Step 1 所选引擎**（每个引擎一套参数清单，仅内存编辑、不写回文件），并自动分组：

| 分组 | 参数（键名） | 交互形式 |
| --- | --- | --- |
| 服务配置 | `backend`（openai-chat / openai）、`endpoint` | 下拉（含选项描述） |
| 采样参数 | `temperature`、`top-p`、`top-k`、`min-p`、`frequency-penalty`、`presence-penalty` | 点击数值行内编辑 / 下拉 |
| 模型与资源 | `max-model-len`、`gpu-memory-utilization`、`mem-fraction-static`、`sharegpt-output-len` | 点击数值行内编辑 |
| 评测配置 | `trust-remote-code`、`ignore-eos`、`burstiness`、`seed`、`num-warmups`、`metric-percentiles` | 行内编辑 / 开关 |
| 其他 | `request-rate`（inf / 数值）、`num-prompts`（0 = 跟随并发）、`timeout` 等 | 下拉 / 行内编辑 |

自研引擎（Bench CLI）默认值：`request-rate=inf`、`num-prompts=0`、`num-warmups=0`、`timeout=600`、`temperature=0.0`、`seed=0`；`chars-per-token` 固定为 4 且不显示（后端用默认值）。

### 3.3 Step 3 · 启动测试

| 字段 | 来源 | 说明 |
| --- | --- | --- |
| Preview Conditions | 前端拼装 | 引擎/框架/模型/Base URL/数据集/请求速率（并发模式附请求数列表；阈值模式附 Max Requests 与三项阈值），可复制 |
| Preview Command | `POST /api/tasks/preview` | 自研引擎：每 case × 请求数一条等效命令；原生引擎：`vllm bench serve` / `sglang.bench_serving`；阈值模式仅预览 1 并发首条命令 |
| Token 使用预估 | 前端估算 | 点「启动」后弹出：逐组「请求数 × 输入/输出 token」表、本组合计、总输入/总输出（百万） |

## 4. 字段限制（校验规则）

| 校验 | 规则 | 触发时机 |
| --- | --- | --- |
| 模型 | 必填，否则提示「请选择模型」 | 下一步 / 启动 |
| 条件组 | 至少保留 1 组 | 下一步 / 启动 |
| 请求数条件 | 并发模式第 1 组非空；正整数，自动去重升序 | 下一步 / 启动 |
| 阈值（阈值模式） | 每组：三项均须为 ≥0 整数，且**不能同时为 0** | 下一步 / 启动 |
| Max Requests | 整数 ≥ 1 | 失焦 |
| 输入 / 输出 | 失焦时 ≤0 重置为 1024 | 失焦 |
| 原生引擎环境 | `env-check` 不通过禁止「下一步」（该引擎 Mock 开关开启时放行，以 FAKE 模式仿真运行） | 下一步 |

## 5. 操作步骤

1. 进入性能测试页，点击介绍页 **并发模式** 或 **阈值模式** 按钮。
2. Step 1：选择 **测试引擎**，等待环境校验标签（原生引擎显示绿色「环境满足」）。
3. 选择 **Provider** 与 **模型**（切换 Provider 自动重新探测；下方显示在线/离线状态）。
4. 填写条件组：**输入/输出** 长度；并发模式再填 **请求数条件**；阈值模式填 **Max Requests** 与每组三项阈值。
5. 点「+」**添加条件组** 增加多长度组合（新组复制上一组值）；点删除图标 **删除该组**。
6. 点 **下一步**：通过校验并加载当前引擎参数清单，进入 Step 2。
7. Step 2：按需调整参数（点击数值行内编辑，失焦/回车保存，Esc 取消；开关直接切换），点 **下一步**。
8. Step 3：核对 **Preview Conditions** 与 **Preview Command**（前面步骤改动会自动刷新，250ms 防抖），需要时点复制图标。
9. 点 **启动**：校验通过后弹出 **Token 使用预估** 弹窗。
10. 弹窗中确认成本，点 **确认**：创建任务、自动启动，返回性能测试页。

## 6. 后台执行逻辑

| 阶段 | 前端调用 | 后台行为 |
| --- | --- | --- |
| 页面加载 | `GET /api/benchs` | 返回引擎清单与默认引擎 |
| 切换引擎 | `GET /api/benchs/{id}/env-check`、`GET /api/benchs/{id}/params`、`GET /api/benchs/{id}/params-yaml` | 校验本地框架版本（要求 vs 已安装）；返回参数定义与参数清单 |
| 切换 Provider | `GET /api/config/providers`、`POST /api/config/test-connection` | 返回 Provider 列表；探测模型列表与在线状态 |
| 进入 Step 3 | `POST /api/tasks/preview` | `build_command_lines()` 生成命令（自研/原生/阈值首条），不落盘 |
| 确认启动 | `POST /api/tasks` | `TaskManager.create_task()`：生成 `task_id`（`task-MMDD-HHMMSS`）、创建 `perfs/<run_id>/`、解析 `cases`（含每组阈值）、持久化 `tasks/<task_id>.json`，`status=pending` |
| 自动启动 | `POST /api/tasks/{id}/start` | `start_task()`：`status=running`、清空旧 `rows`、启动执行线程（详见 [并发模式与阈值模式](/zh/docs/manual/performance/modes/)） |

提交负载（payload）关键字段：`framework`、`engine_id`、`model`、`dataset.length_pairs`（每项 `[输入, 输出, label, case_id, {三项阈值}]`）、`concurrency_list`（并发模式 = 请求数条件；阈值模式 = `[1]`）、`mode`、`max_requests`、`engine_params_yaml`、`api`（Provider 内联配置）。

<div class="tip">
**Token 预估完全在前端计算**：并发模式按每个请求数独立计算（`num-prompts=0` 时请求数 = 并发档值）；阈值模式按 `1,2,4,…≤max_requests` 阶梯累计。仅作成本提醒，不影响执行。
</div>

## 7. 常见问题

**问题：为什么 vLLM/SGLang 原生引擎无法进入下一步？**
Step 1 会对本地环境做校验（要求版本 vs 已安装版本），不通过时「下一步」被阻断，并在明细中列出缺失依赖与安装提示。可安装对应版本，或在 Settings 中开启该引擎的 Mock 开关（以仿真数据运行）。

**问题：向导中途能切换模式吗？**
不能。模式由 URL 查询参数（`?mode=`）决定并贯穿整个向导；切换模式需返回性能测试页重新进入。

**问题：点「取消」会创建任务吗？**
不会。取消仅丢弃当前草稿并返回性能测试页（`/performance`），后台无任何任务产生。

## 8. 相关文档

- [Performance 手册概览](/zh/docs/manual/performance/) — 页面结构与任务状态机
- [并发模式与阈值模式](/zh/docs/manual/performance/modes/) — 参数语义与执行/扫描逻辑
- [设置手册](/zh/docs/manual/settings/) — Provider 与 Bench 引擎配置
- [性能测试参考文档](/zh/docs/performance/) — 概念与指标口径