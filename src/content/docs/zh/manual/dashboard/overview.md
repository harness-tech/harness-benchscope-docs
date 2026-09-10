---
title: "统计概览与环境信息"
description: "Dashboard 统计概览面板的六大统计指标（性能/精度/会话/技能/模型/数据集）与 Provider 计数、环境信息面板的硬件/操作系统/网络/框架版本字段，含字段限制与后台探测逻辑。"
---

# 统计概览与环境信息

Dashboard 第一行左右并排两张只读卡片：左侧**统计概览**（`overview`，六大统计指标 + Provider 块）、右侧**环境信息**（`envInfo`，标题显示 Envs info）。两者在页面打开时自动加载，卡片本身没有刷新按钮（测试记录面板的「刷新」可同步重取统计）。

## 1. 功能说明

- **统计概览**：汇总平台各类记录 / 资源的数量——性能记录、精度记录、会话、内置技能、模型、数据集，以及 Provider 数量与 Provider 模型总数。
- **环境信息**：展示宿主机硬件、操作系统、网络接口与相关框架版本，用于在基准测试前后记录测试环境。

提示：对比不同机器的基准测试结果前，先看本面板的硬件与框架版本——GPU、vLLM / SGLang 版本不一致时，吞吐与延迟结果不可直接比较。

## 2. 页面结构

```
┌──────────────────────────────────┬──────────────────────────────────┐
│ 统计概览（overview）               │ 环境信息（envInfo）                │
│ ┌──────────┬──────────┐          │ ┌──────────────┬──────────────┐  │
│ │ 性能     │ 精度      │          │ │ 硬件环境      │ 操作系统      │  │
│ ├──────────┼──────────┤          │ │ 主机/CPU/内存/ │ OS/系统版本/  │  │
│ │ 会话     │ 技能(内置) │          │ │ GPU          │ 内核版本      │  │
│ ├──────────┼──────────┤          │ ├──────────────┼──────────────┤  │
│ │ 模型     │ 数据集    │          │ │ 网络环境      │ 框架版本      │  │
│ └──────────┴──────────┘          │ │ 每网口:MAC/IP/ │ Python/Pytorch/│  │
│ ┌──────────┬──────────┐          │ │ 子网/掩码     │ vLLM/SGLang/  │  │
│ │ Provider 数量 │ Provider 模型 │  │ │              │ benchscope    │  │
│ └──────────┴──────────┘          │ └──────────────┴──────────────┘  │
└──────────────────────────────────┴──────────────────────────────────┘
```

- 统计概览：2×3 主网格（六大统计指标）+ 底部 Provider 块（Provider 数量 / Provider 模型 两小格并排）。
- 环境信息：2×2 四个盒子：硬件环境 / 操作系统 / 网络环境 / 框架版本。

## 3. 展示指标与字段限制

两张卡片均为**纯展示**，无输入字段；字段约束见下表。

### 3.1 统计概览指标

| 指标 | i18n 键 | 数据来源（API） | 返回字段 | 说明 |
| --- | --- | --- | --- | --- |
| 性能 | `perfCount` | `GET /api/dashboard/stats` | `total_runs` | 性能测试记录数（`kind != eval`，不含精度记录） |
| 精度 | `accCount` | `GET /api/dashboard/stats` | `total_acc_runs` | 精度测试记录数（`kind = eval`），缺失时显示 0 |
| 会话 | `sessions` | `GET /api/sessions` | `sessions.length` | 当前会话数 |
| 技能（内置） | `skills` + `builtin` | `GET /api/skills` | `skills.length` | 内置技能数 |
| 模型 / 数据集 | `modelsTab` / `datasetsTab` | — | — | 模型 / 数据集下载记录数，暂未实现，默认 0 |
| Provider 数量 | `providerCount` | `GET /api/config/providers` | `providers.length` | 已配置的推理 Provider 数量 |
| Provider 模型 | `providerModelCount` | `POST /api/config/test-connection` | Σ `models.length` | 后端并行探测各 Provider 的 `{base_url}/v1/models` 后求和；探测失败的 Provider 计 0 |

<div class="warning">

**warning**：

BenchScope 本身**不暴露** OpenAI 兼容的 `/v1/*` 推理端点。Provider 模型计数是后端对外部 **Provider** 的模型列表接口 `{base_url}/v1/models` 做只读探测（非推理请求）。

</div>

<div class="tip">

**tip**：

`zh.js` 中还保留旧版指标键 `totalPerfsRecords`（Total Perf Records）、`totalAccRecords`（Total Acc Records）、`maxPerfRecords`（Max Perf Records）、`maxAccRecords`（Max Acc Records）、`runningTasks`（Running Tasks）、`envStatusLabel`（测试环境状态），当前页面**不再显示**这些指标。

</div>

### 3.2 环境信息字段

| 盒子 | 字段（显示名） | i18n 键 | 返回字段 | 采集方式 |
| --- | --- | --- | --- | --- |
| 硬件环境 | 主机 | `host` | `hardware.host` | `platform.node()`（主机名） |
| 硬件环境 | CPU | — | `hardware.cpu` | Linux 读 `/proc/cpuinfo` 的 `model name`，macOS 用 `sysctl`，拼接核数 |
| 硬件环境 | 内存 | `memory` | `hardware.memory` | Linux 读 `/proc/meminfo` 的 `MemTotal`，macOS 用 `sysconf`，换算为 GB |
| 硬件环境 | GPU | — | `hardware.gpu` | `detect_gpu()` 探测，格式 `型号 × 数量` |
| 操作系统 | 操作系统 | `os` | `os.name` | `platform.system()` |
| 操作系统 | 系统版本 | `osVersion` | `os.version` | Linux 读 `/etc/os-release` 的 `PRETTY_NAME`，macOS 用 `mac_ver` |
| 操作系统 | 内核版本 | `kernel` | `os.kernel` | `platform.release()` |
| 网络环境 | 网口名 | — | `network[].iface` | 枚举非虚拟网口（见 3.3 约束） |
| 网络环境 | MAC | `netUuid` | `network[].mac` | Linux 执行 `ip -o link show`；macOS 解析 `ifconfig` 的 `ether` |
| 网络环境 | IP | `netIp` | `network[].ip` | Linux 执行 `ip -o -4 addr show`（仅 IPv4）；macOS 解析 `ifconfig` 的 `inet` |
| 网络环境 | 子网 | `netSubnet` | `network[].subnet` | 由 IP + 掩码计算网络地址 |
| 网络环境 | 掩码 | `netMask` | `network[].mask` | CIDR 前缀（Linux）或十六进制掩码（macOS）转点分十进制 |
| 框架版本 | Python | — | `versions.python` | `sys.version` |
| 框架版本 | Pytorch / vLLM / SGLang / benchscope | — | `versions.pytorch` / `versions.vllm` / `versions.sglang` / `versions.benchscope` | `importlib.metadata` 读取 `torch` / `vllm` / `sglang` / `benchscope` 包版本 |

### 3.3 字段限制

| 约束项 | 规则 |
| --- | --- |
| 只读 | 所有字段均为只读，修改需在设置页或命令行进行 |
| 缺失显示 | 任一字段采集失败返回 `None`，前端统一显示 `—` |
| 网口过滤 | 前缀为 `docker` / `veth` / `br-` / `virbr` / `cni` / `flannel` / `lo` / `tun` / `utun` 的虚拟网口不显示 |
| 网口数量 | 每个网口一块（MAC / IP / 子网 / 掩码）；全部被过滤时网络环境盒仅显示一行 `—` |
| 指标刷新 | 两张卡片无独立刷新按钮；点击测试记录面板「刷新」会同步重取 `/api/dashboard/stats` |

## 4. 操作步骤

1. 启动 BenchScope 服务并打开 WebUI（路由 `/dashboard`，`/` 自动重定向）。
2. 页面自动完成加载（取数顺序见第 5 节），无需任何点击。
3. 在**统计概览**卡片查看六大统计指标与 Provider 块。
4. 在**环境信息**卡片查看硬件环境 / 操作系统 / 网络环境 / 框架版本四个盒子。
5. （可选）点击测试记录面板右上角「刷新」，同步重新拉取 `/api/dashboard/stats`，更新性能 / 精度计数。
6. （可选）确认平台版本：使用 `pip show benchscope` 或 `GET /api/version`；框架版本盒中的 `benchscope` 版本来自 `importlib.metadata`。

## 5. 后台执行逻辑

### 5.1 页面加载顺序（前端 `onMounted`）

| 顺序 | 前端函数 | API 调用 | 用途 |
| --- | --- | --- | --- |
| 1 | `loadRuns()` | `GET /api/logs/runs` | 拉取全部运行记录（测试记录面板共用） |
| 2 | `loadStats()` / `loadAccRuns()` | `GET /api/dashboard/stats` + `GET /api/logs/runs` | 取性能 / 精度计数（精度记录面板当前隐藏，预留） |
| 3 | `loadEnv()` | `GET /api/dashboard/env` | 取环境信息 |
| 4 | `config.refreshStatus()` | `GET /api/config/status` | 刷新服务状态（顶栏） |
| 5 | `loadOverviewCounts()` | `GET /api/sessions` + `GET /api/skills` + `GET /api/config/providers`（`Promise.allSettled` 并行），随后对每个 Provider 并行 `POST /api/config/test-connection` | 会话 / 技能 / Provider 数量 + Provider 模型总数 |

第 5 步的 `POST /api/config/test-connection` 在 Provider 列表返回后触发：对每个 Provider 发送 `{base_url, endpoint, api_key, extra_headers}`，后端执行 `GET {base_url}/v1/models`（超时 6 秒，携带 `Authorization: Bearer <api_key>` 与附加头），返回 `models`（模型 id 列表）；前端对每个成功结果累加 `length`，失败的 Provider 计 0。

### 5.2 `GET /api/dashboard/stats` 聚合逻辑

1. 遍历记录目录 `~/.benchscope/perfs`、`~/.benchscope/evals`（旧版 `~/.benchscope/logs` 下存在含 `run.json` 的子目录时一并加入）。
2. 读取每个子目录的 `run.json`（跳过 `tasks` 目录）；`kind == "eval"` 计为精度记录。
3. 返回 `total_runs`（性能记录数 = 总数 − 精度数）、`total_acc_runs`、`best_acc`（精度记录 `summary.accuracy` 最大值）、`running_tasks`（内存中运行中的性能 + 精度任务数）、`avg_tpot` 与 `best_model`（性能记录 `rows[].metrics.tpot_mean` 聚合）。

### 5.3 `GET /api/dashboard/env` 探测逻辑

后端调用 `collect_env_info()`，四类采集均容错（缺失项为 `None`）：

- **硬件**：`platform.node()`；CPU 型号 + 核数；内存总量；`detect_gpu()`。
- **操作系统**：`platform.system()` / `platform.release()` + `/etc/os-release`（Linux）或 `mac_ver`（macOS）。
- **网络**：Linux 执行 `ip -o -4 addr show` 与 `ip -o link show`；macOS 执行 `ifconfig`；过滤虚拟网口后，将 CIDR 前缀转为点分十进制掩码，再由 IP + 掩码计算子网地址。
- **框架版本**：`sys.version` 与 `importlib.metadata` 读取的 `torch` / `vllm` / `sglang` / `benchscope` 包版本。

## 6. 常见问题

**问题：为什么模型 / 数据集计数一直是 0？**
模型 / 数据集下载记录数暂未实现，前端默认 0；数据集的下载管理在设置页进行。

**问题：环境信息里 GPU 或某个框架版本显示 `—`？**
对应探测失败或未安装该包（如未安装 `vllm` / `sglang`），属正常现象，不影响平台运行。

**问题：旧版的「测试环境状态」「Running Tasks」指标去哪了？**
这些指标（i18n 键 `envStatusLabel`、`runningTasks` 等）在页面改版后不再显示，服务状态改在顶栏展示。

**问题：如何确认 BenchScope 版本？**
框架版本盒展示 `importlib.metadata` 读取的 `benchscope` 包版本；也可使用 `pip show benchscope` 或 `GET /api/version`。