---
title: "测试记录"
description: "Dashboard 测试记录面板：最新 8 条性能测试记录、列字段与状态枚举限制、详情/更多/刷新按钮操作，以及详情落地页 Datas/Perfs 上的 Perf 请求详情与文件下载。"
---

# 测试记录

Dashboard 第二行是通栏的**测试记录**面板（卡片标题显示 **Perf Records**，i18n 键 `perfTestRecords`），列出**最新 8 条**性能测试记录：不分页、无搜索框、只读展示。点击「详情」可跳转 Datas/Perfs 查看请求详情并下载文件。

## 1. 功能说明

- 展示最新 8 条性能记录的 Run ID、模型、框架、状态、开始时间。
- 提供三个入口：行内「详情」（跳转对应任务详情）、头部「更多」（完整记录列表）、头部「刷新」（重新拉取数据）。
- 精度记录（`kind = eval`）被前端过滤，不在此面板显示；Eval Records 面板当前隐藏。

<div class="warning">

**warning**：

本面板只列出**性能**记录。Datas 子导航当前仅有 Perfs、Analysis 两个 Tab（Evals Tab 已隐藏）；精度测试任务与结果请在 Accuracy 页面管理。

</div>

## 2. 页面结构

```
┌────────────────────────────────────────────────────────────┐
│ Perf Records（perfTestRecords）                 [刷新] [更多] │
├────────────────────────────────────────────────────────────┤
│ Run ID    │ Model       │ Framework │ Status │ Time      │ 详情 │
│ run-2026… │ deepseek-…  │ vLLM      │ 已完成  │ 09-09 …  │ 详情 │
│ run-2025… │ qwen-…      │ SGLang    │ 运行中  │ 09-08 …  │ 详情 │
│ （最多 8 行，不分页，无搜索框）                             │
├────────────────────────────────────────────────────────────┤
│                                          *仅显示最新 8 条记录 │
└────────────────────────────────────────────────────────────┘
```

- 卡片头部右侧为两个文字按钮：`刷新`（带重载图标，i18n 键 `refresh`）、`更多`（i18n 键 `more`）。
- 表格每行一个文字按钮：`详情`（i18n 键 `detail`）。
- footer 右侧显示固定提示 `*仅显示最新 8 条记录`（i18n 键 `latest8Hint`）。

## 3. 输入参数与字段限制

### 3.1 输入参数

| 字段 | i18n 键 | 类型 | 必填 | 限制 / 约束 | 说明 |
| --- | --- | --- | --- | --- | --- |
| 搜索模型 | `searchModel` | 文本输入（预留） | 可选 | 占位符 `搜索模型...`；当前版本**未渲染** | `zh.js` 中预留该占位符用于按模型名过滤记录；当前测试记录面板为纯只读表格，无搜索框 |

面板无其他输入字段：记录由后端一次性返回，无查询参数、无分页、无排序控件。

### 3.2 展示列限制

| 列 | 返回字段 | 限制 / 枚举 |
| --- | --- | --- |
| Run ID | `run_id` | 记录目录名，全局唯一；列宽 140px，详情页超 40 字符截断显示 |
| Model | `meta.model` | `run.json` 中记录的模型名；缺失显示 `-` |
| Framework | `meta.framework` | `run.json` 的 `framework_name`；`vLLM` 显示蓝色，其余（如 `SGLang`）显示紫色；缺失显示 `-` |
| Status | `meta.status` | 枚举 `pending` / `running` / `done` / `stopped` / `error`；`done`→已完成（绿）、`error`→出错（红）、`stopped`→已停止（橙）、`running` 与 `pending`→运行中 |
| Time | `meta.started_at` | 开始时间（`YYYY-MM-DD HH:MM:SS`）；缺失显示 `-` |
| 详情 | — | 文字按钮，跳转 `/datas/perfs?run_id=<run_id>` 并自动选中该任务 |

## 4. 操作步骤

1. 打开 Dashboard（路由 `/dashboard`），测试记录面板自动加载最新 8 条性能记录。
2. **查看详情**：点击某行「详情」→ 跳转 Datas/Perfs 并自动选中该任务（URL 变为 `/datas/perfs?run_id=<run_id>`）。
3. **查看完整列表**：点击头部「更多」→ 跳转 `/datas/perfs`（左侧完整记录列表，可任选任务查看）。
4. **刷新**：点击头部「刷新」→ 重新拉取 `GET /api/logs/runs` 与 `GET /api/dashboard/stats`，更新表格与统计概览。
5. **Perf 请求详情**（Datas/Perfs 页）：在「Perf Datas」数据面板点击某请求行的详情操作 → 弹出 **Perf 请求详情**（`perfDetail`）对话框，显示该请求的 Profile Progress / Real-Time Metrics。
6. **下载**（Datas/Perfs 页）：在「Logs 信息」盒中点击「摘要」行下载图标（优先 `run.summary.xlsx`，缺失时回退 `run.json`）或任一日志文件行的下载图标 → 浏览器下载对应文件。

<div class="tip">

**tip**：

当前 Dashboard 未提供按模型名搜索；要找某个模型的记录，请点「更多」进入 Datas/Perfs 查看完整列表（按 Run ID 倒序），或在列表中核对 Model 列。

</div>

## 5. 后台执行逻辑

### 5.1 面板加载（页面打开 / 点击「刷新」）

| 顺序 | 前端 | 后端 | 说明 |
| --- | --- | --- | --- |
| 1 | `loadRuns()` | `GET /api/logs/runs` | 后端遍历 `~/.benchscope/perfs`、`~/.benchscope/evals`（旧版 `~/.benchscope/logs` 下存在含 `run.json` 的子目录时一并加入），读取每个目录的 `run.json`，返回 `runs[]`，按 `run_id` 倒序 |
| 2 | 前端过滤 | — | 过滤 `meta.kind === 'eval'` 或 `dir` 含 `/evals` 的精度记录，取前 8 条渲染表格 |
| 3 | `loadStats()` | `GET /api/dashboard/stats` | 同步刷新统计概览的性能 / 精度计数 |

`GET /api/logs/runs` 每条记录返回：`run_id`（目录名）、`dir`（绝对路径）、`files[]`（目录内全部文件 + `~/.benchscope/logs/` 下终端日志 `{kind}_{run_id}_*.log`）、`meta`（kind / framework / model / status / started_at / finished_at / summary）。

### 5.2 「详情」跳转

`router.push({ path: '/datas/perfs', query: { run_id } })` → Datas/Perfs 的 `onMounted` 先 `loadRuns()` 再执行 `selectRunFromQuery`：

1. `GET /api/logs/runs/{run_id}` → 返回 `{run_id, dir, files[], run}`（完整 `run.json`），渲染 Perf 信息 / Cases 信息 / Logs 信息 / Perf Datas / 统计图。
2. `GET /api/logs/runs/{run_id}/live` → 读取 `run_dir/live/*.json` 按请求持久化的实时快照，按 `reqKey`（label/case + case_id + concurrency）建索引，供 Perf 请求详情使用。

### 5.3 Perf 请求详情（`perfDetail`）

点击请求行详情触发 `openDetail(row)`：

- 该行存在 `live` 快照：直接展示快照的 Profile Progress / Real-Time Metrics；
- 不存在（如非 builtin 引擎运行）：用该行 `metrics`（benchmark_duration、successful/failed requests、req_per_s、output_mean）构造最小快照，Real-Time Metrics 显示为空。

### 5.4 文件下载

- **单文件**：前端 `window.open('/api/logs/runs/{run_id}/download?name=<文件名>')` → 后端 `FileResponse` 返回原文件。
- **摘要**：优先下载 `run.summary.xlsx`；`run.json` 无 `summary.xlsx` 时下载 `run.json`。
- **整体备份**：Datas/Perfs 头部「备份」按钮 → `GET /api/logs/runs/{run_id}/backup`，将 run 目录 + 终端日志打包为 zip 下载（该 zip 可通过「导入 record」入口恢复）。

## 6. 常见问题

**问题：为什么只显示 8 条记录？**
面板 footer 明确标注 `*仅显示最新 8 条记录`；前端按 `run_id` 倒序取前 8 条，不分页。查看全部记录请用「更多」进入 Datas/Perfs。

**问题：为什么看不到精度测试记录？**
测试记录面板只列性能记录：`kind = eval` 的记录被前端过滤；Eval Records 面板与 Datas 的 Evals Tab 当前隐藏，精度任务与结果请在 Accuracy 页面管理。

**问题：状态为什么显示「运行中」？**
状态枚举为 `pending` / `running` / `done` / `stopped` / `error`，前端将 `pending` 与 `running` 都显示为「运行中」；`done` / `error` / `stopped` 分别显示为已完成 / 出错 / 已停止。

**问题：有按模型名搜索的输入框吗？**
当前版本未渲染：`zh.js` 的 `searchModel` 键（占位符 `搜索模型...`）为预留项。请点「更多」进入 Datas/Perfs，按 Model 列人工定位目标模型。

**问题：结果文件在哪里下载？**
Dashboard 面板本身没有下载按钮；「详情」跳转 Datas/Perfs 后，在「Logs 信息」盒点击摘要或日志文件的下载图标，或用头部「备份」按钮打包下载全部文件。