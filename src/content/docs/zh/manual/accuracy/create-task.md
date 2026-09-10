---
title: "创建评测任务"
description: "Accuracy 三步创建向导逐步讲解：选择数据集 → 模式与模型 → 预览与启动，含输入参数、字段限制、按钮操作与后台执行逻辑。"
---

# 创建评测任务

在精度页右上角点击「创建精度任务（accCreateTask）」按钮（介绍页上为主按钮）即可创建任务。进入 `/accuracy/create` 后是一个**三步向导**（`AccuracyCreateView.vue`），按「选择数据集 → 模式与模型 → 预览与启动」依次填写。

<div class="info">
**步骤条**：页面顶部为 `a-steps` 三步条（accStepDataset / accStepModel / accStepPreview），底部操作栏随步骤显示「上一步 / 下一步 / 启动精度评测任务」。
</div>

## 1. 页面结构

```
┌──────────────────────────────────────────────────────────┐
│ [创建精度任务]                          [返回]             │
│  ① 选择数据集 ──── ② 模式与模型 ──── ③ 预览与启动          │
├──────────────────────────────────────────────────────────┤
│  Step 1：数据集来源(内置/本地JSONL) + 数据集选择            │
│          + 元信息(类别/判分器/样本量/下载状态) + 抽样上限    │
│  Step 2：测试模式 + 评测引擎 + Provider + 模型 + LoRA       │
│          + seed/温度/top_p/maxTokens/并发 + 评审模型        │
│  Step 3：参数汇总 + 等效CLI命令 + Token消耗预估提醒         │
├──────────────────────────────────────────────────────────┤
│                                  [上一步] [下一步/启动]    │
└──────────────────────────────────────────────────────────┘
```

## 2. 输入参数

### 2.1 Step 1 — 选择数据集（accStepDataset）

| 字段 | 标识 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- | --- |
| 数据集来源 | `accDatasetSource` | 单选 `builtin`/`path` | `builtin` | 内置评测数据集（accDatasetBuiltin）/ 本地路径 JSONL（accDatasetPath） |
| 评测数据集 | `datasetId` | 下拉（可搜索） | — | 来源为内置时必填，候选来自 `GET /api/accuracy/datasets` |
| 类别 / 判分器 / 样本量 | `accDatasetCat`/`accDatasetScorer`/`accDatasetSize` | 只读 | — | 选中后展示 `category_name` / `eval.scorer` / `total_samples` |
| 下载状态 | `accDatasetReady`/`accDatasetNeedDownload` | 只读标签 | — | 已下载缓存（绿）/ 启动评测时自动下载（橙） |
| 本地 JSONL 路径 | `datasetPath` | 输入框 | — | 来源为本地时必填，须为存在的合法 JSONL |
| 样本抽样上限 | `limit` | 数字 | `0` | 0 = 全量；按固定种子抽样，可复现 |

选中数据集后可点击「预览数据集（accPreviewBtn）」预览前 5 条样本（题干 accDatasetQuestion / Prompt accPromptCol / 标准答案 accAnswerCol）。

### 2.2 Step 2 — 模式与模型（accStepModel）

| 字段 | 标识 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- | --- |
| 测试模式 | `mode` | 单选 `serving`/`native` | `serving` | Serving 链路（accModeServing）/ Native 原生（accModeNative） |
| 评测引擎 | `engineId` | 下拉 | `benchscope` | 仅列出具备 `eval` 能力的引擎（benchscope / native-hf / mock） |
| 推理服务 Provider | `providerId` | 下拉 | 激活项 | 仅 `serving` 显示，候选来自 `GET /api/providers` |
| 被测模型 | `model` | 下拉/输入 | — | 厂商目录（accModelCatalog）或自定义（accModelCustom），必填 |
| LoRA 增量模型路径 | `loraPath` | 输入框 | — | 可选；Native 经 peft 合并，Serving 请求服务端 adapter |
| LoRA 服务端注册名 | `loraName` | 输入框 | — | 可选，仅 `serving`；服务端注册 adapter 的请求名 |
| 种子 | `seed` | 数字 | `1234` | 抽样与生成的随机种子 |
| 温度 | `temperature` | 数字 | `0.0` | 采样温度 |
| top_p | `topP` | 数字 | `1.0` | 核采样概率 |
| 最大输出 Token | `maxTokens` | 数字 | `512` | 单样本最大输出 token |
| 并发推理数 | `concurrency` | 数字 | `4` | 仅 `serving` 显示 |
| 评审模型 | `judgeModel` | 输入框 | — | 所选数据集判分器为 `judge`（MT-Bench）时显示 |

### 2.3 Step 3 — 预览与启动（accStepPreview）

只读汇总 + 两个提示块：

- **参数汇总**：数据集 / 模式 / 引擎 / 模型 / LoRA / `seed · temp · top_p · max`。
- **等效 CLI 命令（accCmdHint）**：可复制的 `benchscope eval --engine <id> --model <m> --dataset <ds> [--lora-path] [--lora-name] [--limit] [--seed] [--judge-model]`。
- **Token 消耗预估提醒（accEstimateTitle，仅 serving）**：当前选择数据集（accEstimateDataset）、预估本次评测消耗总 Token（accEstimateTotal）、输入（accEstimateIn）/ 输出（accEstimateOut）、样本数与口径（accEstimateSamples）。

## 3. 字段限制

| 字段 | 必填 | 约束 / 枚举 | 默认 |
| --- | --- | --- | --- |
| `datasetId` | 内置来源必填 | 枚举：内置或已导入自定义数据集 id | — |
| `datasetPath` | 本地来源必填 | 须存在且为合法 JSONL | — |
| `limit` | 可选 | 整数 ≥ 0 | 0 |
| `mode` | 必填 | 枚举 `serving` / `native` | serving |
| `engineId` | 必填 | 具备 `eval` 能力的引擎；环境校验 FAIL 时禁用 | benchscope |
| `providerId` | serving 必填 | 已存在的 Provider | 激活项 |
| `model` | 必填 | 非空字符串 | — |
| `loraPath` / `loraName` | 可选 | 路径 / 名称（loraName 仅 serving） | — |
| `seed` | 可选 | 整数 | 1234 |
| `temperature` | 可选 | 0 – 2，步进 0.1 | 0.0 |
| `topP` | 可选 | 0 – 1，步进 0.1 | 1.0 |
| `maxTokens` | 必填 | 整数 ≥ 1 | 512 |
| `concurrency` | serving 可选 | 整数 ≥ 1 | 4 |
| `judgeModel` | 条件必填 | scorer=`judge` 且 serving 时必填 | — |

## 4. 操作步骤

**进入向导**
1. 精度页点击「创建精度任务」按钮，进入 `/accuracy/create`。

**Step 1 — 选择数据集**
2. 选择「数据集来源」：默认「内置评测数据集」；本地数据切换「本地路径 JSONL」。
3. 内置时选择「评测数据集」，核对类别 / 判分器 / 样本量 / 下载状态；本地时填写 JSONL 路径。
4. （可选）点「预览数据集」查看前 5 条样本。
5. 填写「样本抽样上限」（0 = 全量）。
6. 点「下一步」（未选数据集时按钮禁用）。

**Step 2 — 模式与模型**
7. 选择「测试模式」：Serving 链路（默认）/ Native 原生。
8. 选择「评测引擎」（切换即触发环境校验）。
9. （Serving）选择「推理服务 Provider」。
10. 选择「被测模型」（厂商目录 / 自定义）。
11. （可选）填写 LoRA 路径；（Serving 可选）填写 LoRA 服务端注册名。
12. 设置种子 / 温度 / top_p / 最大输出 Token；（Serving）设置并发推理数。
13. （MT-Bench）填写「评审模型」。
14. 点「下一步」。

**Step 3 — 预览与启动**
15. 核对参数汇总与「等效 CLI 命令」（可复制执行）。
16. （Serving）查看「Token 消耗预估提醒」。
17. 点「启动精度评测任务」；（Serving 且预估 > 0）在弹窗点「确认启动（accReminderConfirm）」。
18. 启动成功后自动返回精度任务列表页，任务进入运行中。

## 5. 后台执行逻辑

**页面加载（onMounted）**：并行发起 4 个请求 —— `GET /api/accuracy/datasets`（数据集）、`GET /api/accuracy/engines`（引擎，按 `eval` 过滤）、`GET /api/providers`（Provider）、`GET /api/model-catalog`（厂商模型目录）。

**交互触发**：

| 动作 | API |
| --- | --- |
| 预览数据集 | `POST /api/accuracy/datasets/preview`（`{id}` 或 `{path}`） |
| 切换引擎 | `GET /api/accuracy/engines/{engine_id}/env-check` |
| 进入 Step 3（serving） | `GET /api/accuracy/estimate`（`dataset_id`/`path`/`limit`/`mode`/`max_tokens`） |

**启动（`POST /api/accuracy/tasks`）**：
1. 参数校验：`model` 非空；`dataset.id` 或 `dataset.path` 必填。
2. 数据集校验：`path` 须存在；`id` 须已注册（内置或已导入）。
3. `create_task()`：生成 `task_id`（`eval-MMDD-HHMMSS`），按引擎能力定模式（native-hf→native，否则→serving），落盘 `task.json` + `run.json`。
4. `start_task()`：置 `running`；（serving）先做 Token 预估；启动守护线程。
5. 线程内 `run_eval()`：加载样本 → 构建 Prompt → 批量推理（serving 走 aiohttp 并发 / native 走 transformers）→ 判分 → 汇总指标 → 基线对标 → 结论。
6. 实时经 WebSocket 推送 `eval_task_log` / `eval_task_progress` / `eval_task_result`。
7. 完成后落盘 `result.json` / `samples.jsonl` 并置状态。

## 6. 常见问题

**问题：为什么「下一步」按钮是灰色的？**
Step 1 未选数据集、或 Step 2 未填模型（Serving 下 MT-Bench 还需填评审模型）时禁用；引擎环境校验 FAIL 时该引擎也会被禁用。

**问题：Native 模式提示环境校验不通过怎么办？**
Native 引擎需 `torch` + `transformers`（并检测 CUDA）。安装 `pip install 'benchscope[accuracy-native]'` 后重新进入向导，或改用 Serving 模式。

**问题：等效 CLI 命令有什么用？**
Step 3 生成的 `benchscope eval` 命令与 Web 任务共用同一评测核心，可复制后在终端直接执行，便于脚本化与复现。

**问题：Token 预估提醒在 Native 模式会出现吗？**
不会。Native 模式无线上链路消耗，预估恒为 0，启动时不弹确认框。