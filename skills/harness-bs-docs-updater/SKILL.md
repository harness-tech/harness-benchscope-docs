---
name: harness-bs-docs-updater
version: "2.0.0"
author: "HarnessAI / 模力有方"
description: >
  以「功能快照」为唯一事实来源，驱动 benchscope-docs 官网（落地页）与文档站（docs）的全覆盖更新。
  先模拟跑全量用例生成功能快照，再按快照核对文档覆盖、修复偏差、校验核心指标齐全，最后归档、更新官网并构建发布。
  触发词：更新文档、发布新版本、更新官网、同步文档、docs update、release docs。
  不适用：非 BenchScope 项目的文档维护、一次性文案润色、纯翻译任务。
tags:
  - docs
  - benchscope
  - release
  - astro
  - maintenance
  - feature-snapshot
---

# Harness BS Docs Updater

以 BenchScope 源码为唯一事实来源，通过**功能快照（feature snapshot）**驱动 benchscope-docs 官网与文档站的全覆盖、可校验更新。

## 核心理念

1. **功能快照优先（snapshot-first）**：任何文档更新都从一份**功能快照**（`feature-snapshot.json`）出发。快照由「模拟跑全量用例 + 源码分析」生成，是文档的**唯一事实来源**。
2. **全覆盖可校验（coverage-verified）**：文档覆盖度由工具自动校验（`feature_snapshot.py coverage`），核心指标（44 个）必须 100% 出现在 zh/en 文档中，否则不通过。
3. **文档规范强制（spec-mandatory）**：所有新增 / 修改的文档必须遵循 `references/docs-update-guide.md`（话术 / 段落约定 + 指标表规范）。
4. **每次全量重模拟（full re-simulation）**：每次迭代都重新跑全量用例生成新快照，**不做增量-only 模式**，保证文档始终对齐当前功能。
5. **快照存放硬规则（placement rule）**：功能快照存于**技能目录** `skills/harness-bs-docs-updater/feature-snapshot.json`，**绝不放入 `archives/` 归档目录**（归档目录只放旧版本文档）。

## 目标

根据 BenchScope 源码的功能现状，自动完成：
1. **功能快照**：模拟跑全量用例 + 解析源码，生成功能快照
2. **覆盖分析**：按快照核对现有文档覆盖度，产出偏差 / 缺口报告
3. **文档更新**：按快照修复偏差、补全缺口、撰写 zh/en 双语文档（遵循文档规范）
4. **覆盖校验**：重跑覆盖度检查，确认核心指标与全部功能点 100% 覆盖
5. **版本归档**：旧文档按版本归档到 `archives/vX.Y.Z/`
6. **官网更新**：落地页（Screen\*.astro）内容与截图规划
7. **发布闭环**：构建验证 → Git 提交 → Netlify 部署

## 使用边界

| 场景 | 是否适用 |
|---|---|
| BenchScope 新版本发布，需更新官网 + 文档 | ✅ 适用 |
| 文档与功能出现偏差，需核对并修复 | ✅ 适用 |
| 仅更新官网某屏文案或截图 | ✅ 适用 |
| 仅更新某篇文档内容 | ✅ 适用 |
| 非 BenchScope 项目的文档维护 | ❌ 不适用 |
| 一次性文案润色、不涉及版本管理 | ❌ 不适用 |
| 纯翻译任务（无功能变更） | ❌ 不适用 |

## 输入检查

开始前确认以下输入（缺失时提示用户补充）：

| 输入 | 必需 | 说明 |
|---|---|---|
| 源码路径或 GitHub URL | ✅ | 本地路径如 `/path/to/benchscope`，或 GitHub `https://github.com/LABELNET/benchscope` |
| 目标版本号 | ✅ | 如 `v1.2.0`；若未指定，从源码 `pyproject.toml` 自动提取 |
| 更新范围 | 可选 | `all`（默认）/ `landing`（仅官网）/ `docs`（仅文档）/ `both`（官网+文档） |
| 截图文件 | 可选 | 若未提供，标记为 `<!-- TODO: screenshot -->` 占位 |
| 测试端口 | 可选 | 模拟跑用例时隔离端口，避免与运行中的服务冲突（如 `BS_TEST_PORT` / `BS_MOCK_PORT`） |

## 关键文件

| 文件 | 路径 | 说明 |
|---|---|---|
| **功能快照** | `skills/harness-bs-docs-updater/feature-snapshot.json` | 文档唯一事实来源（**不放 archives/**） |
| 功能快照工具 | `scripts/feature_snapshot.py` | `generate` / `coverage` / `validate` 三个子命令 |
| 源码快照 | `source-snapshot.json` | 源码文件指纹（增量对比用，自动发现生成） |
| 源码快照工具 | `scripts/snapshot.py` | `generate` / `diff` / `bump` |
| 文档规范 | `references/docs-update-guide.md` | 话术 / 段落约定 + 指标表规范（强制） |
| 官网规范 | `references/landing-update-guide.md` | 落地页文案与截图规范 |
| 归档工具 | `scripts/archive.py` | 旧文档归档到 `archives/vX.Y.Z/` |
| 截图工具 | `scripts/screenshot.py` | Playwright 自动截图 |

## 工作流

### Phase 0 — 准备（端口隔离 + 环境检查）

> 模拟跑全量用例前，必须隔离端口并确认测试环境，避免与运行中的服务 / 旧进程冲突。

1. **隔离测试端口**：
   ```bash
   # 用独立端口跑用例，避免 8080 / 8001 等被运行中的服务占用
   export BS_TEST_PORT=18091   # 被测 benchscope 服务端口
   export BS_MOCK_PORT=8011    # mock OpenAI 服务端口
   ```
2. **确认测试环境**：
   - 使用系统 `python3`（含依赖），而非 benchscope 自带的 `.venv`（可能缺依赖）。
   - 确认 `tests/run_tests.sh` 可用（mock OpenAI + 临时数据目录 + `BENCHSCOPE_FAKE_BENCH=1`）。
   - 用临时 `BENCHSCOPE_DATA_DIR` 隔离测试数据，避免污染 `~/.benchscope`。
3. **确认端口未被占用**：
   ```bash
   # 若端口被占用，改用其他端口，不要 kill 未知进程
   lsof -i :$BS_TEST_PORT || true
   ```

### Phase 1 — 功能快照生成（snapshot-first）

> **核心步骤**：模拟跑全量用例 + 解析源码，生成功能快照 `feature-snapshot.json`。这是文档的**唯一事实来源**。

1. **模拟跑全量用例**（生成验证数据）：
   ```bash
   # 全量功能用例：API + WebUI（mock OpenAI + FAKE bench + 临时数据目录）
   BS_TEST_PORT=$BS_TEST_PORT BS_MOCK_PORT=$BS_MOCK_PORT \
     ./tests/run_tests.sh
   # 记录：API 通过/失败数、WebUI 通过/失败数、失败用例及原因
   ```
   > 失败用例需**归因**（环境问题 / 代码缺陷 / 过期用例 / 状态污染），写入快照的 `cli_runs` / `test_suite` 字段，作为偏差报告的一部分。

2. **CLI 模拟运行**（perf / eval 真实 mock 跑）：
   ```bash
   # 并发模式：对 mock OpenAI 服务压测（真实压测链路、仿真服务端）
   python3 -m benchscope.cli perf --model mock-model --base-url http://127.0.0.1:$BS_MOCK_PORT \
     --concurrency 4 --num-prompts 8 --input-len 64 --output-len 32
   # 阈值模式：自动搜索最佳并发
   python3 -m benchscope.cli perf --model mock-model --base-url http://127.0.0.1:$BS_MOCK_PORT \
     --mode threshold --ttft-threshold-ms 500 --tpot-threshold-ms 100 --max-concurrency-search 8 --num-prompts 4
   # 精度评测：mock 引擎 + 本地 JSONL 数据集（全链路）
   python3 -m benchscope.cli eval --engine mock --model mock-model \
     --dataset /path/to/samples.jsonl --limit 20 --mock-correct-rate 0.7
   ```
   > 记录每次运行的关键输出（指标值、best_concurrency、accuracy、conclusion 等），写入快照。

3. **整理验证用例清单**（cases.json）：
   - 汇总 `test_suite`（API / WebUI 通过失败数 + 失败归因）与 `cli_runs`（perf / eval 关键输出）。
   - 这是 `feature_snapshot.py generate --cases` 的输入。

4. **生成功能快照**：
   ```bash
   python3 skills/harness-bs-docs-updater/scripts/feature_snapshot.py generate \
     --source /path/to/benchscope \
     --cases /path/to/cases.json \
     --output skills/harness-bs-docs-updater/feature-snapshot.json
   ```
   快照包含：版本、CLI 参数、引擎、数据集、基线、API 路由、WebUI 页面、指标定义、环境、内置技能、功能开关、mock 环境、验证用例。

5. **校验快照存放位置**：
   ```bash
   # 确认快照在技能目录，绝不在 archives/
   python3 skills/harness-bs-docs-updater/scripts/feature_snapshot.py validate \
     --path skills/harness-bs-docs-updater/feature-snapshot.json
   ```

6. **核对快照准确性**：
   - 抽查 CLI 参数、引擎、数据集、API 分组、WebUI 页面是否与源码一致。
   - 若解析异常（正则未命中），修正 `feature_snapshot.py` 的解析器后重新 generate。

### Phase 2 — 覆盖分析（coverage）

> **核心步骤**：按快照核对现有文档覆盖度，产出偏差 / 缺口报告。

1. **运行覆盖度检查**：
   ```bash
   python3 skills/harness-bs-docs-updater/scripts/feature_snapshot.py coverage \
     --snapshot skills/harness-bs-docs-updater/feature-snapshot.json \
     --docs src/content/docs \
     --output /tmp/coverage_report.json
   # 有缺口时 exit 2，并列出所有缺口（按 zh/en 分语言、按类别）
   ```
2. **解读缺口报告**：
   - `metric` 缺口：核心指标未在文档出现（**最高优先级**，44 个指标必须 100% 覆盖）
   - `cli-arg` / `engine` / `dataset` / `webui-page` / `api-group` 缺口：功能点未覆盖
   - 区分 zh / en 两语言的缺口
3. **人工核对偏差**（工具无法自动发现的）：
   - 文档中的**错误描述**（如错误的结论枚举、错误的端点声明、错误的目录名）
   - 文档中的**过期内容**（如已隐藏的功能、已改名的字段）
   - 与验证用例的**行为偏差**（如 CLI 实际输出与文档不符）
4. **产出偏差报告**：
   ```
   ## 偏差报告
   ### 覆盖缺口（工具检测）
   - [metric] peakoutput / req_per_s / single_user ...（19 个）
   - [dataset] sharegpt / alpaca / dolly（3 个）
   - [api-group] /api/test / /api/benchs / /api/skills（3 个）
   ### 描述错误（人工核对）
   - CLI --version 选项不存在（文档错误声明）
   - 分析目录名为 analysys（文档误写为 analysis）
   - API 不暴露 /v1/* 推理端点（文档误称 OpenAI 兼容）
   - 精度结论枚举为 合格/精度下跌/异常（文档误写为 持平/优于基线等）
   ### 行为偏差（验证用例）
   - 阈值模式上限为 2 的幂时的边界行为
   ```

### Phase 3 — 文档更新（spec-mandatory）

> **核心步骤**：按快照 + 偏差报告修复偏差、补全缺口、撰写文档。**所有文档必须遵循 `references/docs-update-guide.md`**。

1. **确定文档影响面**：
   - 用覆盖缺口 + 偏差报告确定需要新增 / 修改的文档页（zh/en）。
   - 核心指标缺口 → 新增 / 补全指标口径页（如 `performance/metrics.md`、`accuracy/metrics.md`）。
   - 功能页缺口 → 新增 / 补全对应功能页（如 `tools/dashboard.md`、`tools/mock.md`、`tools/skills.md`）。
   - 描述错误 → 修正对应文档页。
2. **遵循文档规范**（`references/docs-update-guide.md`，强制）：
   - **话术**：简洁、客观、面向用户；避免内部术语堆砌；技术标识符（指标键 / CLI 参数 / API 路由 / 枚举值 / 文件路径）**原样保留，不翻译**。
   - **段落**：每段聚焦一个主题；表格用于结构化数据（指标 / 参数 / 路由）；`<div class="tip/info/warning">` 用于提示。
   - **指标表规范**：每个核心指标必须给出**含义、单位、统计量 / 口径**，并在正文中解释其业务意义。
   - **双语同步**：zh/en 必须同时更新，结构一致。
   - **绝对路由**：链接使用 `/zh/docs/...` 或 `/en/docs/...`。
   - **FAQ 格式**：`**问题：xxx？**`（zh）/ `**Question: xxx?**`（en）。
   - **命名规范**：文件名 `kebab-case`，frontmatter 至少含 `title`，H1 与 `title` 一致。
3. **指标全覆盖**（44 个核心指标）：
   - 性能 14 个：`ttft_mean/median/p99`、`tpot_mean/median/p99`、`itl_mean/median/p99`、`output_mean`、`peakoutput_mean`、`total_mean`、`req_per_s`、`single_user`。
   - 精度 30 个：`accuracy`、`pass_rate`、`total_samples`、`correct_samples`、`wrong_samples`、`invalid_samples`、`subjects`、`error_tag_summary`、判分器专项（`exact_match`/`math_accuracy`/`answer_parse_rate`、`pass_at_1`/`compile_rate`/`case_pass_rate`、`mt_bench_score`/`first_turn_score`/`second_turn_score`/`dim_helpfulness`/`dim_truthfulness`/`dim_harmlessness`）、Token（`prompt_tokens_total`/`completion_tokens_total`/`total_tokens`/`avg_*`）、基线（`baseline_used`/`diff_pp`/`grade`/`conclusion`）。
   - 每个指标必须在 zh 和 en 文档中**都出现**（含含义说明）。
4. **版本记录更新**：
   - 更新 `src/content/docs/{zh,en}/releases/` 新增版本页。
   - 更新 `releases/index.md` 版本表（最新在上）+ 当前版本号。
5. **站点版本号一致性**（若站点版本变化）：
   - 同步 `package.json`、`SiteFooter.astro`、`Landing.astro`、`DESIGN.md`、`CHANGELOG.md` 的版本号。

### Phase 4 — 覆盖校验（coverage-verified）

> **核心步骤**：重跑覆盖度检查，确认全部缺口已消除、核心指标 100% 覆盖。

1. **重跑覆盖度检查**：
   ```bash
   python3 skills/harness-bs-docs-updater/scripts/feature_snapshot.py coverage \
     --snapshot skills/harness-bs-docs-updater/feature-snapshot.json \
     --docs src/content/docs \
     --output /tmp/coverage_after.json
   # 必须 exit 0（无缺口）才通过
   ```
2. **确认核心指标 100% 覆盖**：
   - 44 个核心指标在 zh/en 文档中全部出现。
   - CLI 参数、引擎、数据集、API 分组、WebUI 页面全部覆盖。
3. **交叉核对**：
   - 抽查文档中的关键描述（结论枚举、端点声明、目录名、版本号）是否与快照一致。
   - 确认无残留的错误描述 / 过期内容。
4. **未通过则回到 Phase 3**：仍有缺口时继续补全，直到覆盖度 100%。

### Phase 5 — 版本归档（archive）

> 归档目录位于**项目根目录** `archives/`（非技能目录下），由技能负责维护。归档后自动打包为 `tar.gz`。
> **硬规则**：功能快照（`feature-snapshot.json`）**绝不归档**，只归档旧版本文档。

1. **运行归档脚本**：
   ```bash
   python skills/harness-bs-docs-updater/scripts/archive.py --version <当前版本>
   ```
2. **归档内容**：
   - 当前 `src/content/docs/zh/` 全量快照
   - 当前 `src/content/docs/en/` 全量快照
3. **自动生成**：
   - `archives/vX.Y.Z/META.md` — 归档元数据
   - `archives/vX.Y.Z.tar.gz` — 归档压缩包
4. **确认快照未被归档**：
   - `feature-snapshot.json` 仍在 `skills/harness-bs-docs-updater/`，**不在** `archives/`。

> **归档规则**：仅在版本号发生变化时归档；同一版本的多次修改不重复归档。

### Phase 6 — 官网更新（Landing Page）

> 参考 `references/landing-update-guide.md` 和 `DESIGN.md`

1. **识别变更屏幕**：根据功能变更，确定需要更新的 `Screen*.astro` 文件
2. **规划更新内容**：
   - 新增功能 → 更新对应屏幕的功能描述
   - UI 变更 → 更新截图占位 + 描述文字
   - 新模块 → 评估是否需要新增屏幕或扩展现有屏幕
3. **Mock 数据填充**：
   - 表格类数据：使用真实格式 + mock 数值
   - 截图占位：`<!-- TODO: replace with screenshot at /images/xxx.png -->`
4. **文案要求**：
   - 中英双语同步（`isEn` 条件）
   - 简洁有力，每项功能 ≤ 2 行描述
   - 符合 DESIGN.md 规定的字体、颜色、间距
5. **官网版本号一致性**：
   - 若站点版本变化，同步 `SiteFooter.astro` / `Landing.astro` / `DESIGN.md` 的版本号。

### Phase 7 — 截图处理

1. **自动截图**（需 Playwright）：
   ```bash
   python scripts/screenshot.py --url http://localhost:4321/zh/ --output public/images/xxx.png
   ```
2. **手动截图**：提示用户将截图放入 `public/images/` 并告知文件名
3. **占位标记**：未获取到截图时，在文档中插入：
   ```markdown
   <!-- TODO: replace with screenshot at /images/benchscope-xxx.png -->
   ```

### Phase 8 — 构建验证与发布

1. **构建验证**（必须通过）：
   ```bash
   pnpm test:links   # 链接校验
   pnpm build         # 完整构建
   ```
2. **更新 CHANGELOG**：
   - 在 `CHANGELOG.md` **顶部**新增版本记录（新版在最上）。
   - 记录文档重构、核心指标补全、偏差修复、技能优化等要点。
3. **Git 提交**（按 AGENTS.md §7 规范，**需维护者明确指示**）：
   ```bash
   git add -A
   git commit -m "docs(site): update for vX.Y.Z - <简短英文描述>"
   ```
   > **绝不自动 commit / push**，必须由维护者明确指示后才执行。
4. **Netlify 部署**（需维护者明确指示）：
   ```bash
   export NETLIFY_AUTH_TOKEN=$(cut -d= -f2 ~/.env.netlify)
   pnpm build
   python3 scripts/deploy-netlify.py --site-id 2fb005db-4cd4-4dd4-b2e3-f21de81b6f00 --prod
   ```
5. **GitHub Release**（需维护者明确指示）：
   ```bash
   export GITHUB_TOKEN=$(cut -d= -f2 ~/.env.github)
   # 使用 API 创建 Release，body 读取 releases/vX.Y.Z.md
   ```

## 输出契约

每次执行完成后交付：

| 产出 | 路径 | 说明 |
|---|---|---|
| **功能快照** | `skills/harness-bs-docs-updater/feature-snapshot.json` | 文档唯一事实来源（**不放 archives/**） |
| 覆盖度报告 | `/tmp/coverage_report.json` + `/tmp/coverage_after.json` | 更新前 / 更新后的覆盖度 |
| 偏差报告 | （输出到反馈） | 覆盖缺口 + 描述错误 + 行为偏差 |
| 归档文档 | `archives/vX.Y.Z/docs/{zh,en}/`（项目根目录） | 旧版本文档快照 |
| 归档压缩包 | `archives/vX.Y.Z.tar.gz`（项目根目录） | 归档目录的 tar.gz 压缩包 |
| 归档元数据 | `archives/vX.Y.Z/META.md`（项目根目录） | 归档时间、版本、变更摘要 |
| Release Notes | `releases/vX.Y.Z.md` | 中英双语发布说明 |
| 更新后的官网组件 | `src/components/Screen*.astro` | 涉及变更的屏幕 |
| 更新后的文档 | `src/content/docs/{zh,en}/` | 新增或修改的文档页 |
| 更新后的 CHANGELOG | `CHANGELOG.md` | 顶部新增版本记录 |

## 质量门禁

- [ ] 功能快照已生成且经 `validate` 确认**不在 archives/**
- [ ] 覆盖度检查 `exit 0`（无缺口）
- [ ] 44 个核心指标在 zh/en 文档中 100% 出现
- [ ] CLI 参数 / 引擎 / 数据集 / API 分组 / WebUI 页面全覆盖
- [ ] 所有文档遵循 `references/docs-update-guide.md`（话术 / 段落 / 指标表）
- [ ] YAML front matter 存在且可解析，H1 与 title 一致
- [ ] zh/en 文档文件数一致
- [ ] 所有内链为绝对路由
- [ ] FAQ 格式统一
- [ ] 提示块使用 HTML div 语法
- [ ] 站点版本号一致（package.json / footer / DESIGN.md / CHANGELOG）
- [ ] `pnpm test:links` 通过
- [ ] `pnpm build` 通过
- [ ] Release Notes 中英双语齐全
- [ ] 归档目录结构完整，功能快照未被归档
- [ ] Git commit message 为英文且 ≤ 72 字符（且经维护者指示）

## 异常处理

| 异常 | 处理方式 |
|---|---|
| 源码路径不存在 | 提示用户确认路径，或使用 GitHub URL 克隆 |
| 测试端口被占用 | 改用其他端口（`BS_TEST_PORT` / `BS_MOCK_PORT`），不 kill 未知进程 |
| `.venv` 缺依赖 | 用系统 `python3`（含依赖），而非 benchscope 自带 `.venv` |
| mock 引擎缺数据集文件 | 本地构造 JSONL 数据集（choice 格式：question/choices/answer/subject），`--dataset` 指向本地文件 |
| 用例失败 | 归因（环境 / 代码缺陷 / 过期用例 / 状态污染），写入快照 + 偏差报告，**不修改产品代码**（除非用户要求） |
| 快照解析异常（正则未命中） | 修正 `feature_snapshot.py` 解析器后重新 generate |
| 覆盖度未通过（exit 2） | 回到 Phase 3 补全缺口，直到 100% 覆盖 |
| 快照被误放 archives/ | 运行 `validate` 检测，移回技能目录 |
| 截图获取失败 | 插入 TODO 占位，提示用户后续补充 |
| 构建失败 | 读取错误输出，定位问题文件，修复后重试 |
| 部署失败 | 检查 Netlify token，重试或提示手动部署 |
| GitHub Release 创建失败 | 保存 release notes 到文件，提示手动创建 |

## 资源索引

| 何时读取 | 路径 |
|---|---|
| **功能快照（文档唯一事实来源）** | `feature-snapshot.json` |
| **功能快照工具（generate/coverage/validate）** | `scripts/feature_snapshot.py` |
| 源码快照（模块/文件/指纹） | `source-snapshot.json` |
| 源码快照工具（生成/对比/更新） | `scripts/snapshot.py` |
| **文档规范（话术/段落/指标表，强制）** | `references/docs-update-guide.md` |
| 官网更新规范 | `references/landing-update-guide.md` |
| 截图自动化 | `scripts/screenshot.py` |
| 归档工具 | `scripts/archive.py` |
| 归档模板 | `templates/archive-meta.md` |
| Release Notes 模板 | `templates/release-notes.md` |
| 项目设计规范 | `DESIGN.md`（项目根目录） |
| 提交规范 | `AGENTS.md`（项目根目录） |

## 触发测试

**应触发**：
- "BenchScope 发布了 v1.2.0，帮我更新文档站"
- "核对文档和功能的偏差，补全核心指标"
- "模拟跑全量用例，生成功能快照"
- "同步 benchscope 最新版本到 docs"
- "根据这个 PRD 更新官网功能介绍"

**不应触发**：
- "帮我写一篇博客"（非 BenchScope 文档）
- "翻译这篇文档"（纯翻译，无功能变更）
- "修改这个 Astro 组件的样式"（无版本关联的单次修改）