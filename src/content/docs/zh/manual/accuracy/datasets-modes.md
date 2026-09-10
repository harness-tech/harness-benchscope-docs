---
title: "数据集与模式"
description: "Accuracy 模块 9 个内置评测数据集、Serving/Native 双模式与 4 类判分器详解，含输入参数、字段限制与后台逻辑。"
---

# 数据集与模式

精度评测的「数据集」决定评什么，「模式」决定怎么推理，「判分器」决定怎么判对错。三者均在创建向导的 **Step 1（选择数据集）** 与 **Step 2（模式与模型）** 配置。

<div class="info">
**内置数据集共 9 个**（均带 `eval` 元数据）；另有 3 个性能数据集（sharegpt / alpaca / dolly）仅供性能测试，不出现在精度向导。
</div>

## 1. 页面结构

- **Step 1 数据集面板**：数据集来源（内置 / 本地 JSONL）→ 数据集下拉 → 元信息（类别 accDatasetCat / 判分器 accDatasetScorer / 样本量 accDatasetSize / 下载状态）→ 预览数据集（accPreviewBtn）→ 样本抽样上限（accLimit）。
- **Step 2 模式面板**：测试模式（accModes，Serving 链路 accModeServing / Native 原生 accModeNative）→ 评测引擎（accEngine）→（Serving）推理服务 Provider（accProvider）。

## 2. 输入参数

| 字段 | 标识 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- | --- |
| 数据集来源 | `accDatasetSource` | 单选 `builtin`/`path` | `builtin` | 内置评测数据集 / 本地路径 JSONL |
| 评测数据集 | `datasetId` | 下拉（可搜索） | — | 内置时必填，候选为 9 个内置 + 已导入自定义 |
| 本地 JSONL 路径 | `datasetPath` | 输入框 | — | 本地时必填，须为存在的合法 JSONL |
| 样本抽样上限 | `limit` | 数字 | `0` | 0 = 全量；固定种子抽样可复现 |
| 测试模式 | `mode` | 单选 `serving`/`native` | `serving` | Serving 链路 / Native 原生 |
| 评测引擎 | `engineId` | 下拉 | `benchscope` | 具备 `eval` 能力：benchscope / native-hf / mock |
| 推理服务 Provider | `providerId` | 下拉 | 激活项 | 仅 `serving` 显示 |

## 3. 字段限制

| 字段 | 必填 | 约束 / 枚举 |
| --- | --- | --- |
| `datasetId` | 内置来源必填 | 9 个内置 id 或已导入自定义 id |
| `datasetPath` | 本地来源必填 | 存在的合法 JSONL；标准字段 `question`/`answer`（可选 `choices`/`subject`，代码类 `prompt`/`test`/`entry_point`，对话类 `turns`） |
| `limit` | 可选 | 整数 ≥ 0，0 = 全量 |
| `mode` | 必填 | 枚举 `serving` / `native` |
| `engineId` | 必填 | 具备 `eval` 能力的引擎；环境校验 FAIL 时禁用 |

<div class="warning">
**MT-Bench（`mt-bench`）判分器为 `judge`**：评审模型须经 Serving 链路调用，故该数据集**仅支持 Serving 模式**，Native 模式会报「Native 模式暂不支持 judge 数据集」。
</div>

## 4. 内置数据集（9 个）

| id | 名称 | 类别 | 判分器 | 主指标 | 样本量 |
| --- | --- | --- | --- | --- | --- |
| `mmlu` | MMLU | 知识 | `choice` | `accuracy` | 14079 |
| `cmmlu` | CMMLU | 知识 | `choice` | `accuracy` | 11960 |
| `c-eval` | C-Eval | 知识 | `choice` | `accuracy` | 13480 |
| `gsm8k` | GSM8K | 数学 | `math` | `exact_match` | 7473 |
| `math` | MATH | 数学 | `math` | `exact_match` | 5000 |
| `humaneval` | HumanEval | 代码 | `code` | `pass@1` | 164 |
| `mbpp` | MBPP | 代码 | `code` | `pass@1` | 974 |
| `mt-bench` | MT-Bench | 对话 | `judge` | `mt_bench` | 80 |
| `gaokao-bench` | GAOKAO-Bench | 综合 | `choice` | `accuracy` | 2000 |

## 5. Serving / Native 双模式

| 维度 | Serving 链路 | Native 原生 |
| --- | --- | --- |
| `mode` 值 | `serving` | `native` |
| 典型引擎 | `benchscope` / `mock` | `native-hf` |
| 推理方式 | 调用推理服务 API（OpenAI 兼容）真实链路 | 本地加载模型权重离线推理（transformers） |
| 环境依赖 | 无（仅需可达的 Provider） | `torch` + `transformers`（+ CUDA），`pip install 'benchscope[accuracy-native]'` |
| Token 统计 | 有（逐条采集 usage，缺失按 chars/4 近似） | 无（能力边界） |
| Token 预估 | 有（启动前强提醒） | 恒为 0 |
| LoRA | `loraName` 请求服务端已注册 adapter | `loraPath` 经 peft 合并加载 |
| 适用 | 线上服务 / 远程模型验收 | 本地权重 / 无服务端场景 |

## 6. 判分器（4 类）

| 判分器 | 适用数据集 | 判分逻辑 | 结果状态 |
| --- | --- | --- | --- |
| `choice` | mmlu / cmmlu / c-eval / gaokao-bench | 多策略抽取选项字母（A–H）与标准答案比对 | correct / wrong（知识错误）/ invalid（格式错误） |
| `math` | gsm8k / math | 抽取最终答案（`\boxed{}` / 显式标记 / 末行数值），规范化后等价比较 | correct / wrong（推理错误）/ invalid（格式错误） |
| `code` | humaneval / mbpp | 抽取代码，受限子进程沙箱执行（`-I` isolated，10s 超时），全部用例通过 | correct / wrong（执行错误）/ invalid（格式错误） |
| `judge` | mt-bench | LLM-as-judge 对每轮打分（1–10 + helpfulness/truthfulness/harmlessness），均值 ≥ 6 判对 | correct / wrong / invalid（评审失败） |

## 7. 操作步骤（按钮操作）

1. 进入创建向导 Step 1，选择「数据集来源」（默认内置）。
2. 内置：从下拉选择 9 个内置数据集之一，核对类别 / 判分器 / 样本量 / 下载状态；未下载时显示「启动评测时自动下载」。
3. 本地：填写 JSONL 路径（须存在于服务端可访问路径）。
4. （可选）点「预览数据集」查看前 5 条样本，确认字段映射正确。
5. 设置「样本抽样上限」（大样本量建议抽样，如 `limit=200`）。
6. Step 2 选择「测试模式」与「评测引擎」；（Serving）选择 Provider。
7. 点「下一步」进入预览与启动。

## 8. 后台执行逻辑

- **数据集清单**：`GET /api/accuracy/datasets` 读取 `configs/datasets.yaml` 中所有带 `eval` 段的条目 + `datasets_dir/eval_custom/` 下已导入自定义数据集，并标记 `downloaded` 状态。
- **数据集预览**：`POST /api/accuracy/datasets/preview` 解析引用 → 标准化样本（`standardize_samples`）→ 过滤可评测样本（`filter_samples`）→ 构建 Prompt，返回前 5 条。
- **引擎环境校验**：`GET /api/accuracy/engines/{id}/env-check` 校验引擎 `requires` 依赖；`native` 追加 `torch.cuda.is_available()` 检测。
- **下载缓存**：内置数据集首次评测时按 `source`（modelscope / url）下载到 `datasets_dir/<id>/`，`.json` 自动转 `.jsonl`，并校验产物可解析（防错误页当数据集）。
- **判分路由**：`run_eval` 按数据集 `eval.scorer` 从判分器注册表取对应判分器，未知名称回退 `math`。

## 9. 常见问题

**问题：如何新增一个自定义数据集？**
两种途径：① 直接引用本地 JSONL 路径（`datasetPath`）；② 经 `POST /api/accuracy/datasets/import` 上传导入，落盘 `datasets_dir/eval_custom/`。标准字段 `question`/`answer`，可选 `choices`/`subject`。

**问题：数据集未下载会怎样？**
首次评测时后台自动下载（ModelScope 优先），下载中显示「启动评测时自动下载」标签；下载失败任务会置为 `error`。

**问题：Serving 与 Native 结果能直接对比吗？**
两者推理链路不同（在线 API vs 本地权重），指标口径一致但数值可能有差异，建议在同一模型、同一模式下对比，或用「Native vs Serving 一致性」对比能力核对。

**问题：判分器是怎么确定的？**
由数据集 `eval.scorer` 绑定（内置数据集已固化）；自定义数据集按样本字段自动探测（choices→choice / test→code / turns→judge / 默认 math）。