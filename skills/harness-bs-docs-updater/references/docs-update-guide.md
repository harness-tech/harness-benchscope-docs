# 文档站更新规范（Doc-Spec）

本文档是 benchscope-docs 文档站内容更新的**强制规范**，覆盖目录结构、话术、段落、指标表、准确性红线。所有新增 / 修改的文档**必须**遵循本规范。

## 目录结构

```
src/content/docs/{zh,en}/
├── README.md                  # 文档首页
├── quickstart/                # 快速开始（含 requirements、platform）
├── install/                   # 安装（含 configuration、update-uninstall）
├── accuracy/                  # 精度（含 modes、datasets、scoring、guide、metrics）
├── performance/               # 性能（含 concurrency、threshold、metrics）
├── data/                      # 数据
├── tools/                     # 工具（含 dashboard、sessions、settings、skills、mock、architecture、bench-engine）
├── cli/                       # CLI（含 serve、perf、eval）
├── api/                       # API
├── releases/                  # 发布（含 v1-x-y 版本页）
└── help/                      # 帮助（含 contributing）
```

> **指标口径页**：`performance/metrics.md`（性能核心指标）与 `accuracy/metrics.md`（精度核心指标）是指标含义的**权威来源**，其他页面引用指标时以这两个页面为准。

## 文件命名规范

- 文件名：`kebab-case`（如 `update-uninstall.md`）
- frontmatter：至少含 `title`（建议含 `description`）
- h1 标题与 frontmatter `title` **必须一致**

```markdown
---
title: "页面标题"
description: "可选的页面描述"
---

# 页面标题
```

## 双语同步规则

| 规则 | 说明 |
|---|---|
| 文件数一致 | zh 有多少文件，en 就有多少文件 |
| 结构一致 | 目录层级、子分组完全相同 |
| 链接一致 | zh 用 `/zh/docs/...`，en 用 `/en/docs/...` |
| 内容独立 | 不是逐句翻译，而是用目标语言自然表达 |
| 术语一致 | 技术标识符（指标键 / CLI 参数 / API 路由 / 枚举值 / 文件路径）zh/en **原样一致，不翻译** |

## 话术规范（Wording）

> **核心原则**：简洁、客观、面向用户；不堆砌内部术语；技术标识符原样保留。

1. **简洁客观**：每句话传递一个信息点；避免口语化、避免夸张（不用「强大」「极致」等营销词）。
2. **面向用户**：用用户能理解的表述解释功能，而非内部实现细节。
3. **技术标识符原样保留（不翻译）**：
   - 指标键：`ttft_mean`、`peakoutput_mean`、`single_user` 等
   - CLI 参数：`--ttft-threshold-ms`、`--max-concurrency-search` 等
   - API 路由：`/api/tasks/{task_id}/start`、`/api/accuracy/baselines` 等
   - 枚举值：`concurrency`/`threshold`、`serving`/`native`/`mock`、`S`/`A`/`B`/`C`
   - 文件路径：`~/.benchscope/perfs/`、`benchscope/configs/benchs.yaml`
   - 环境变量：`BENCHSCOPE_DATA_DIR`、`BENCHSCOPE_FAKE_BENCH`
4. **中英对照**：zh 用「**问题：xxx？**」，en 用 `**Question: xxx?**`。
5. **数值与单位**：指标必须带单位（ms / tok/s / req/s / % / tokens）；阈值、默认值必须与源码一致。
6. **避免歧义**：不确定的行为不要臆测；以功能快照（`feature-snapshot.json`）和验证用例为准。

## 段落与结构规范（Paragraphs）

> **核心原则**：每段聚焦一个主题；结构化数据用表格；提示用 div 块。

1. **单主题段落**：每个段落只讲一个主题；超过 3-4 句应拆分。
2. **结构化数据用表格**：指标、CLI 参数、API 路由、数据集、基线等**必须**用表格呈现，不用长段罗列。
3. **提示用 div 块**：补充说明用 `<div class="tip">`、注意事项用 `<div class="warning">`、背景信息用 `<div class="info">`。
4. **代码示例**：命令、配置、输出示例用 fenced code block，带语言标签（`bash` / `python` / `json` / `console`）。
5. **列表**：并列要点用无序列表；有序步骤用有序列表。
6. **首段引导**：页面首段（1-2 句）说明本页主题与适用场景，并指向相关页面。
7. **尾部导航**：页面末尾放「相关文档」，链接到关联页面（绝对路由）。

## 指标表规范（Metrics Tables）

> **核心原则**：每个核心指标必须给出**含义、单位、统计量/口径**，并在正文中解释业务意义。

指标表必须包含以下列（按适用情况）：

| 列 | 说明 | 示例 |
|---|---|---|
| 指标 | 指标名称（含技术键） | 首 token 延迟 `ttft_mean` |
| 键名 | 代码中的指标键（原样，不翻译） | `ttft_mean` |
| 单位 | 指标单位 | ms / tok/s / req/s / % / tokens |
| 统计量 | 统计口径（适用时） | mean / median / p99 |
| 含义 | 指标的业务含义 + 优化方向 | 从请求发出到收到第一个 token 的耗时，**越低越好** |

**指标口径页（`performance/metrics.md` / `accuracy/metrics.md`）必须覆盖**：
1. 每个核心指标的**含义、单位、统计量**（表格）。
2. 指标的**业务意义**与**优化方向**（越低越好 / 越高越好）。
3. **统计量说明**（mean / median / p99 各自含义与使用建议）。
4. **指标分组**（核心指标 / 请求统计 / 判分器专项 / Token 消耗 / 基线对标 / 结论）。
5. **判定规则**（如精度结论 `合格/精度下跌/异常` 的判定条件、档位 `S/A/B/C` 的规则）。
6. **产物文件**（task.json / result.json / samples.jsonl 等）。
7. **常见问题**（澄清易混淆的指标，如 TPOT vs ITL、accuracy vs pass_rate）。

## 核心指标清单（44 个，必须 100% 覆盖）

> 覆盖度由 `feature_snapshot.py coverage` 自动校验；以下 44 个指标必须在 zh/en 文档中**都出现**（含含义说明）。

### 性能指标（14 个）

| 键名 | 含义 | 单位 | 统计量 |
|---|---|---|---|
| `ttft_mean` / `ttft_median` / `ttft_p99` | 首 token 延迟（TTFT） | ms | mean / median / p99 |
| `tpot_mean` / `tpot_median` / `tpot_p99` | 每输出 token 延迟（TPOT） | ms | mean / median / p99 |
| `itl_mean` / `itl_median` / `itl_p99` | token 间隔延迟（ITL） | ms | mean / median / p99 |
| `output_mean` | 输出吞吐 | tok/s | mean |
| `peakoutput_mean` | 峰值输出吞吐（vLLM 口径） | tok/s | mean |
| `total_mean` | 总 token 吞吐 | tok/s | mean |
| `req_per_s` | 请求吞吐 | req/s | mean |
| `single_user` | 单用户吞吐（`1000/TPOT`） | tok/s | 推导 |

> 注：mean/median/p99 三种统计量按「指标组」计，TTFT/TPOT/ITL 各 3 个 = 9，加 output/peakoutput/total/req_per_s/single_user 5 个 = 14。

### 精度指标（30 个）

| 类别 | 键名 | 含义 |
|---|---|---|
| 核心 | `accuracy` | 正确率（核心主指标） |
| 核心 | `pass_rate` | 通过率（有效可解析样本占比） |
| 样本 | `total_samples` / `correct_samples` / `wrong_samples` / `invalid_samples` | 总 / 正确 / 错误 / 无效样本数 |
| 分析 | `subjects` | 分学科正确率 |
| 分析 | `error_tag_summary` | 错因标签分布 |
| math | `exact_match` / `math_accuracy` / `answer_parse_rate` | 精确匹配率 / 数学正确率 / 答案解析率 |
| code | `pass_at_1` / `compile_rate` / `case_pass_rate` | pass@1 / 编译通过率 / 用例通过率 |
| judge | `mt_bench_score` / `first_turn_score` / `second_turn_score` | MT-Bench 总分 / 首轮得分 / 二轮得分 |
| judge | `dim_helpfulness` / `dim_truthfulness` / `dim_harmlessness` | 有用性 / 真实性 / 无害性维度分 |
| Token | `prompt_tokens_total` / `completion_tokens_total` / `total_tokens` | 输入 / 输出 / 总 token 量 |
| Token | `avg_prompt_tokens_per_sample` / `avg_completion_tokens_per_sample` | 单样本平均输入 / 输出 token |
| 基线 | `baseline_used` / `diff_pp` / `grade` | 对标基线 / 基线差值 / 档位评级（S/A/B/C） |
| 结论 | `conclusion` | 最终结论（合格 / 精度下跌 / 异常） |

## 准确性红线（Accuracy Red Lines）

> **以下错误绝不允许出现在文档中**（历史文档曾犯，已在本次重构中修复）：

1. **`benchscope --version` 不存在**：CLI 未提供 `--version` 选项；查版本用 `pip show benchscope` 或 `/api/version`。
2. **分析目录名是 `analysys`**（内置默认目录名），不是 `analysis`。
3. **API 不暴露 OpenAI 兼容 `/v1/*` 推理端点**：BenchScope 自身不提供 `/v1/models`、`/v1/chat/completions`；会话请求**代理转发**到激活的 Provider。
4. **精度最终结论枚举是 `合格/精度下跌/异常`**（en: Pass/Accuracy Drop/Anomaly），不是「持平/优于基线等」。
5. **Datas 子导航是 Perfs + Analysis**：Evals Tab 已隐藏（路由重定向到 Perfs），精度产物在 **Accuracy 页面**管理。
6. **数据集共 12 个**：9 个精度（mmlu/cmmlu/c-eval/gsm8k/math/humaneval/mbpp/mt-bench/gaokao-bench）+ 3 个性能（sharegpt/alpaca/dolly）。
7. **会话 `max_tokens` 固定 4096**：不在会话参数中开放配置；会话参数含 `quality`/`top_k`/`enable_thinking`/`provider_id`。
8. **版本号一致**：站点版本（package.json / footer / DESIGN.md / CHANGELOG）必须一致；产品版本（releases 页）与站点版本分开。

## 文档结构模板

### 分区落地页（index.md）

```markdown
---
title: "概述"
description: "本分区的简要描述"
---

# 概述

1-2 段概述本分区内容。

## 本页内容

- [子页面1](/zh/docs/xxx/sub1/) — 简要说明
- [子页面2](/zh/docs/xxx/sub2/) — 简要说明

## 核心概念

表格或列表形式介绍核心概念。

## 常见问题

**问题：xxx？**
回答内容。

## 相关文档

- [相关页面1](/zh/docs/xxx/) — 简要说明
- [相关页面2](/zh/docs/xxx/) — 简要说明
```

### 功能页（非 index.md）

```markdown
---
title: "功能名称"
description: "功能的简要描述"
---

# 功能名称

1-2 段功能说明。

## 前置条件

- 条件1
- 条件2

## 操作步骤

### 步骤 1：xxx

说明 + 代码示例。

## 常见问题

**问题：xxx？**
回答内容。

## 相关文档

- [相关页面](/zh/docs/xxx/) — 简要说明
```

### 指标口径页（metrics.md）

```markdown
---
title: "性能核心指标"
description: "性能测试的全部核心指标与关键指标，含指标含义、单位与统计口径。"
---

# 性能核心指标

本页是性能测试指标的**完整口径说明**：覆盖……阅读其他性能文档时遇到指标名，可在此页查找含义。

## 核心指标（每个并发点一组）

| 指标 | 键名 | 单位 | 统计量 | 含义 |
| --- | --- | --- | --- | --- |
| 首 token 延迟 TTFT | `ttft_mean` / `ttft_median` / `ttft_p99` | ms | mean / median / p99 | ……**越低越好**。 |

## 请求统计（每次运行一组）

| 指标 | 键名 | 单位 | 含义 |
| --- | --- | --- | --- |

## 图表与导出

### Excel 导出（benchmark-*.xlsx）

| 列 | 含义 |
| --- | --- |

## 常见问题

**问题：xxx？**
回答内容。

## 相关文档

- [性能测试概述](/zh/docs/performance/) — 双模式总览
```

## 排版规范

| 元素 | 规范 |
|---|---|
| 段落间距 | `margin: 0 0 0.85rem` |
| 列表项间距 | `margin: 0.25rem 0` |
| 代码块 | fenced code block，带语言标签 |
| 行内代码 | 用反引号包裹 |
| 图片 | `max-width: 66.666%`，居中显示 |
| 表格 | 13px 字号，表头加粗 |
| 提示块 | `<div class="tip/warning/info">` HTML 语法 |

## FAQ 格式统一

```markdown
## 常见问题

**问题：xxx？**
回答内容。

**问题：yyy？**
回答内容。
```

禁止使用 `**Q：**\n\nA：` 格式。

## 提示块格式

```html
<div class="tip">

**tip**：

提示内容。

</div>

<div class="warning">

**warning**：

警告内容。

</div>

<div class="info">

**info**：

信息内容。

</div>
```

> en 文档用英文标签：`**Tip**:` / `**Warning**:` / `**Info**:`。

## 内链格式

- ✅ `[链接文字](/zh/docs/quickstart/)` — 绝对路由
- ✅ `[链接文字](/en/docs/cli/perf/)` — 绝对路由
- ❌ `[链接文字](./quickstart.md)` — 相对链接
- ❌ `[链接文字](../install/)` — 相对链接

## 版本发布文档

新增版本时，创建 `src/content/docs/{zh,en}/releases/vX-Y-Z.md`：

```markdown
---
title: "vX.Y.Z 发布说明"
description: "本版本的简要亮点。"
---

# vX.Y.Z 发布说明

**发布日期**：YYYY-MM-DD
**变更类型**：patch / minor / major

## 版本概述

简要说明本版本定位与亮点。

## 更新内容

### 修复 / 特性：xxx

说明 + 验证要点。

## 升级提示

- 从 vA.B.C 升级：……

## 相关文档

- [vX.Y.Z-1 发布说明](/zh/docs/releases/vX-Y-Z-1/) — 上一版本
```

## 内容长度指引

| 页面类型 | 建议行数 |
|---|---|
| 分区落地页（index.md） | 40-80 行 |
| 功能页 | 80-150 行 |
| 参考页（CLI/API） | 100-200 行 |
| 指标口径页（metrics.md） | 150-250 行 |
| 版本发布页 | 50-100 行 |

超过 150 行的功能页应考虑拆分为子页。