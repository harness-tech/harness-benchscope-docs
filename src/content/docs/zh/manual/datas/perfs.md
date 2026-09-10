---
title: 性能记录管理
description: Datas → Perfs 页操作手册：任务记录列表、详情面板（Perf/Cases/Logs 信息、数据面板、统计图）、运行目录与日志文件的查看、预览、下载、复制操作与后台执行逻辑。
---

# 性能记录管理

Perfs 页是 Datas 的核心页面，用于**浏览全部历史性能测试记录**并深入查看每条记录的配置、指标数据、统计图与日志文件。左侧为记录列表，右侧为所选记录的详情面板。

![BenchScope Datas 性能记录详情](/images/benchscope-datas-perfs_detail.png)

## 1. 功能说明

- 左侧**任务记录**列表：展示所有性能运行记录（run），按 `run_id` 倒序，支持刷新与导入。
- 右侧**详情面板**：展示所选记录的任务信息、Perf 信息、Cases 信息、Logs 信息、数据面板（Perf Datas）与统计图。
- 支持对单条记录执行：**删除**、**备份**、**分享**（PNG）、日志**预览 / 下载**、运行目录**复制**。

<div class="info">

**info**：

Perfs 页只展示**性能**记录（`kind=perf`）。精度评测记录同样会列于后端 `/api/logs/runs` 列表，但精度产物请在 [Accuracy 页面](/zh/docs/manual/accuracy/) 管理（Evals 标签页已隐藏）。

</div>

## 2. 页面结构

```
┌───────────────┬─────────────────────────────────────────────────┐
│  Records       │  <run_id>                 [删除][备份][分享]        │
│  [导入][刷新]   │  任务状态   模型   开始时间   结束时间              │
│ ┌───────────┐  ├────────────┬────────────┬──────────────────────┤
│ │ run-abc…  │  │ Perf 信息   │ Cases 信息  │ Logs 信息             │
│ │ vLLM  完成 │  │ model      │ g0 512/…   │ runDir        [复制]  │
│ │ Qwen  …   │  │ framework  │ g1 …       │ summary       [下载]  │
│ ├───────────┤  │ mode       │            │ 日志文件:              │
│ │ run-def…  │  │ dataset    │            │  a.log  [预览][下载]   │
│ │ SGLang …  │  │ 并发列表     │            │  b.log  [预览][下载]   │
│ └───────────┘  │ requests   │            │                      │
│               ├────────────┴────────────┴──────────────────────┤
│  (点击列表项  │  Perf Datas     [默认][Mean][Median][P99]         │
│   加载详情)    │   [ case 分组 tab ]  指标数据表 … [详情]          │
│               ├─────────────────────────────────────────────────┤
│               │  统计图   [联动] [默认] [TTFT] [TPOT] [ITL]        │
│               │   吞吐 / TTFT / TPOT / ITL 四行 × 3 图            │
│               └─────────────────────────────────────────────────┘
└───────────────┴─────────────────────────────────────────────────┘
```

## 3. 输入参数与字段限制

Perfs 页以**选择**为主（无表单填写），主要交互参数如下：

| 字段 | 类型 | 限制 / 约束 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `run_id` | string | 单层目录名，禁含 `/` `\` `..` | — | 记录标识；可经 URL `?run_id=` 传入自动选中 |
| `name`（日志文件） | string | 必须位于 run 目录或 `logs/` 下 | — | 预览 / 下载指定文件 |
| `tail`（预览行数） | int | ≥ 1 | 500 | 预览时返回的末尾行数 |
| 数据口径 `mode` | enum | `default` / `mean` / `median` / `p99` | `default` | 控制数据表显示的统计列 |
| 状态 `status` | enum | `pending` / `running` / `done` / `stopped` / `error` | — | 记录运行状态（只读展示） |
| 任务模式 `mode` | enum | `concurrency` / `threshold` | — | 并发模式 / 阈值模式（只读展示） |
| `request_rate` | string / number | `inf` 或自定义正数 | `inf` | 请求速率，`inf` = 无限 |

## 4. 按钮操作

### 4.1 左侧记录面板
1. **导入**（上传图标）：打开导入抽屉，从备份 zip 恢复记录 → 详见 [导入导出与备份](/zh/docs/manual/datas/import-export/)。
2. **刷新**（循环图标）：重新拉取记录列表（`GET /api/logs/runs`）。
3. **点击记录项**：加载该记录详情（`GET /api/logs/runs/{run_id}` + `GET /api/logs/runs/{run_id}/live`）。

### 4.2 详情面板（第 1 行）
1. **删除**：弹出确认框，确认后删除整条记录（`DELETE /api/logs/runs/{run_id}`）。
2. **备份**：弹出确认框，确认后打包下载 `{run_id}.zip`（`GET /api/logs/runs/{run_id}/backup`）。
3. **分享**：弹出确认框，确认后将详情整页渲染为 PNG 下载（纯前端 `html2canvas`）。

### 4.3 Logs 信息面板
1. **复制运行目录**：将 `run_dir` 路径复制到剪贴板。
2. **下载摘要**：下载 `run.summary.xlsx`（无则回退 `run.json`）。
3. **预览日志文件**：弹窗显示文件末尾内容（`GET .../preview?name=`）。
4. **下载日志文件**：下载指定文件（`GET .../download?name=`）。

### 4.4 数据面板（Perf Datas）
1. 顶部切换 **默认 / Mean / Median / P99** 统计口径。
2. 按 case 分组切换 tab。
3. 点击行尾**详情**：弹窗展示该请求的 Profile Progress / Real-Time Metrics（来自 `live` 快照）。

## 5. 操作步骤（查看一条记录）
1. 进入 **Datas → Perfs**。
2. 在左侧列表点击目标记录（或先点**刷新**）。
3. 右侧第 1 行查看状态 / 模型 / 起止时间。
4. 第 2 行三个面板查看 Perf / Cases / Logs 信息，可复制运行目录、预览或下载日志。
5. 第 3 行 Perf Datas 切换统计口径、按 case 分组查看指标表，点**详情**看实时快照。
6. 第 4 行统计图可开**联动**并按 TTFT / TPOT / ITL 过滤（见 [数据分析](/zh/docs/manual/datas/analysis/)）。

## 6. 后台执行逻辑

| 操作 | API | 处理逻辑 |
| --- | --- | --- |
| 加载列表 | `GET /api/logs/runs` | 扫描 `perfs/`、`evals/`（及旧 `logs/`）下含 `run.json` 的目录，附加终端日志 `logs/{kind}_{run_id}_*.log`，按 `run_id` 倒序去重返回 |
| 加载详情 | `GET /api/logs/runs/{run_id}` | 解析 `run.json` + 列出目录文件 + 附加终端日志 |
| 加载实时快照 | `GET /api/logs/runs/{run_id}/live` | 读取 `run_dir/live/*.json`（各请求的 Profile / Real-Time 快照） |
| 删除 | `DELETE /api/logs/runs/{run_id}` | 删除运行目录 + 删除对应终端日志 |
| 备份 | `GET /api/logs/runs/{run_id}/backup` | 将运行目录全部文件 + 终端日志打包为扁平 zip 返回 |
| 预览 | `GET /api/logs/runs/{run_id}/preview?name=&tail=500` | 仅允许文本文件，返回末尾 `tail` 行 |
| 下载 | `GET /api/logs/runs/{run_id}/download?name=` | 校验路径后返回文件 |

<div class="tip">

**tip**：

记录详情主要读自落盘的 **`run.json`**（含 `rows[].metrics` 全部指标键，如 `output_mean`、`ttft_p99`、`tpot_median` 等），前端据此渲染数据表与统计图；实时快照读自 **`live/*.json`**。

</div>

## 7. 常见问题

**问题：列表为空或找不到某次任务？**
确认数据根目录未被清理、未切换 `BENCHSCOPE_DATA_DIR`；也可用**导入**从备份恢复（见 [导入导出与备份](/zh/docs/manual/datas/import-export/)）。

**问题：点「详情」实时指标为空？**
该记录无按请求持久化的 `live/*.json` 快照（如非内置引擎运行），此时仅展示由行指标构造的最小 Profile，Real-Time Metrics 为空 / N-A。

**问题：能删除正在运行的任务吗？**
Perfs 页删除的是**已落盘记录**目录；运行中任务请在性能测试页停止后再处理，避免文件占用。

## 8. 相关文档

- [Datas 手册概览](/zh/docs/manual/datas/) — Datas 模块入口
- [数据分析](/zh/docs/manual/datas/analysis/) — 统计口径、联动
- [导入导出与备份](/zh/docs/manual/datas/import-export/) — 备份 / 导入 / 分享
- [性能测试（参考）](/zh/docs/performance/) — 指标口径
- [API 参考](/zh/docs/api/) — `/api/logs/*` 完整路由
