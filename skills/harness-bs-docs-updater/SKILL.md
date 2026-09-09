---
name: harness-bs-docs-updater
version: "1.0.0"
author: "HarnessAI / 模力有方"
description: >
  从 BenchScope 源码仓库（本地路径或 GitHub）分析版本更新内容，
  自动维护 benchscope-docs 官网（落地页）和文档站（docs）。
  触发词：更新文档、发布新版本、更新官网、同步文档、docs update、release docs。
  不适用：非 BenchScope 项目的文档维护、一次性文案润色、纯翻译任务。
tags:
  - docs
  - benchscope
  - release
  - astro
  - maintenance
---

# Harness BS Docs Updater

从 BenchScope 源码分析版本变更，驱动 benchscope-docs 官网与文档站的规范更新。

## 目标

根据 BenchScope 源码仓库的版本变更，自动完成：
1. **功能分析**：从源码 / GitHub Release 提取变更点
2. **官网更新**：落地页（Screen\*.astro）内容与截图规划
3. **文档更新**：zh/en 双语文档的规范撰写
4. **版本归档**：旧文档按版本归档到 `archives/vX.Y.Z/`
5. **发布闭环**：构建验证 → Git 提交 → Netlify 部署

## 使用边界

| 场景 | 是否适用 |
|---|---|
| BenchScope 新版本发布，需更新官网 + 文档 | ✅ 适用 |
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
| 目标版本号 | ✅ | 如 `v1.2.0`；若未指定，从源码 `setup.py` / `pyproject.toml` / `__init__.py` 自动提取 |
| 更新范围 | 可选 | `all`（默认）/ `landing`（仅官网）/ `docs`（仅文档）/ `both`（官网+文档） |
| 截图文件 | 可选 | 若未提供，标记为 `<!-- TODO: screenshot -->` 占位 |

## 工作流

### Phase 1 — 源码分析（快照对比模式）

> **核心优化**：不全量读取源码，而是通过 `source-snapshot.json` 快照对比差异，只读取变更文件。

1. **加载快照**：读取 `skills/harness-bs-docs-updater/source-snapshot.json`
   - 快照记录了 benchscope 源码的模块结构、文件指纹（SHA256）、功能映射和文档路径

2. **对比差异**（运行快照工具）：
   ```bash
   # 本地源码对比
   python skills/harness-bs-docs-updater/scripts/snapshot.py diff \
     --source /path/to/benchscope --json

   # 或 GitHub 对比
   python skills/harness-bs-docs-updater/scripts/snapshot.py diff \
     --github https://github.com/LABELNET/benchscope --tag v1.2.0 --json
   ```

3. **解读差异报告**：
   - `modules_changed`：变更的模块列表，每个变更包含 module、file、old_hash、new_hash
   - `docs_to_update`：需要更新的文档路径（zh/en）
   - `changelog_changed`：CHANGELOG 是否有变化
   - `configs_changed`：配置文件是否有变化
   - 若 `needs_update = false`，说明无变更，跳过更新

4. **只读取变更文件**：
   - 根据 `modules_changed` 中的文件列表，只读取这些文件的 diff 或内容
   - 读取 `CHANGELOG.md` 的新增条目（只读最新版本部分）
   - **不读取**未变更的模块代码

5. **输出变更摘要**：
   ```
   ## 变更摘要 (vX.Y.Z)
   ### 变更模块
   - performance: perf/runner.py, perf/metrics.py 变更
   - accuracy: accuracy/scorer.py 变更
   ### 需要更新的文档
   - zh: performance/index.md, accuracy/scoring.md
   - en: performance/index.md, accuracy/scoring.md
   ### 配置变更
   - 是/否
   ```

6. **更新快照**：变更处理完成后，更新快照文件：
   ```bash
   python skills/harness-bs-docs-updater/scripts/snapshot.py bump --version 1.2.0
   ```
   或重新生成（首次 / 结构大改时）：
   ```bash
   python skills/harness-bs-docs-updater/scripts/snapshot.py generate \
     --source /path/to/benchscope --tag v1.2.0
   ```

### Phase 2 — 归档旧文档

1. **创建归档目录**：`archives/v<当前版本>/`
2. **归档内容**：
   - 当前 `src/content/docs/zh/` 全量快照
   - 当前 `src/content/docs/en/` 全量快照
   - 当前 `src/components/` 中涉及变更的组件快照
3. **记录归档元数据**：`archives/v<当前版本>/META.md`（归档时间、版本、变更摘要）

> **归档规则**：仅在版本号发生变化时归档；同一版本的多次修改不重复归档。

### Phase 3 — 官网更新（Landing Page）

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

### Phase 4 — 文档更新（Docs）

> 参考 `references/docs-update-guide.md` 和 `DESIGN.md §4.6`

1. **确定文档影响面**（直接使用快照报告的 `docs_to_update`）：
   - 快照 diff 已输出需要更新的文档路径列表
   - 只读取和更新这些文档，不触碰未变更的文档
   - 若有新模块（快照中不存在），需新增文档页并同步更新快照

2. **文档撰写规范**：
   - **双语同步**：zh/en 必须同时更新，结构一致
   - **绝对路由**：链接使用 `/zh/docs/...` 或 `/en/docs/...`
   - **标题层级**：h1（页面标题）→ h2（主要章节）→ h3（子章节）
   - **FAQ 格式**：`**问题：xxx？**\n回答内容`
   - **提示块**：使用 `<div class="tip/warning/info">` HTML 语法
   - **代码块**：带语言标签的 fenced code block
   - **命名规范**：文件名 `kebab-case`，frontmatter 至少含 `title`

3. **文档结构模板**（每个功能页）：
   ```markdown
   ---
   title: "功能名称"
   ---
   # 功能名称
   简要说明（1-2 段）
   ## 前置条件
   ## 操作步骤
   ## 常见问题
   ## 相关文档
   ```

4. **版本记录更新**：
   - 更新 `src/content/docs/{zh,en}/releases/` 新增版本页
   - 更新 `releases/index.md` 版本表（最新在上）

### Phase 5 — 截图处理

1. **自动截图**（需 Playwright）：
   ```bash
   python scripts/screenshot.py --url http://localhost:4321/zh/ --output public/images/xxx.png
   ```
2. **手动截图**：提示用户将截图放入 `public/images/` 并告知文件名
3. **占位标记**：未获取到截图时，在文档中插入：
   ```markdown
   <!-- TODO: replace with screenshot at /images/benchscope-xxx.png -->
   ```

### Phase 6 — 构建验证与发布

1. **构建验证**：
   ```bash
   pnpm test:links   # 链接校验
   pnpm build         # 完整构建
   ```

2. **Git 提交**（按 AGENTS.md §7 规范）：
   ```bash
   git add -A
   git commit -m "docs(site): update for vX.Y.Z - <简短英文描述>"
   git tag -a v<X.Y.Z> -m "BenchScope Docs v<X.Y.Z>"
   git push origin main
   git push origin v<X.Y.Z>
   ```

3. **Netlify 部署**：
   ```bash
   export NETLIFY_AUTH_TOKEN=$(cut -d= -f2 ~/.env.netlify)
   pnpm build
   python3 scripts/deploy-netlify.py --site-id 2fb005db-4cd4-4dd4-b2e3-f21de81b6f00 --prod
   ```

4. **GitHub Release**：
   ```bash
   export GITHUB_TOKEN=$(cut -d= -f2 ~/.env.github)
   # 使用 API 创建 Release，body 读取 releases/vX.Y.Z.md
   ```

## 输出契约

每次执行完成后交付：

| 产出 | 路径 | 说明 |
|---|---|---|
| 变更分析报告 | `archives/vX.Y.Z/ANALYSIS.md` | 源码变更摘要 |
| 归档文档 | `archives/vX.Y.Z/docs/{zh,en}/` | 旧版本文档快照 |
| 归档元数据 | `archives/vX.Y.Z/META.md` | 归档时间、版本、变更摘要 |
| Release Notes | `releases/vX.Y.Z.md` | 中英双语发布说明 |
| 更新后的官网组件 | `src/components/Screen*.astro` | 涉及变更的屏幕 |
| 更新后的文档 | `src/content/docs/{zh,en}/` | 新增或修改的文档页 |
| 更新后的 CHANGELOG | `CHANGELOG.md` | 顶部新增版本记录 |

## 质量门禁

- [ ] YAML front matter 存在且可解析
- [ ] zh/en 文档文件数一致
- [ ] 所有内链为绝对路由
- [ ] FAQ 格式统一
- [ ] 提示块使用 HTML div 语法
- [ ] `pnpm test:links` 通过
- [ ] `pnpm build` 通过
- [ ] Release Notes 中英双语齐全
- [ ] 归档目录结构完整
- [ ] Git commit message 为英文且 ≤ 72 字符

## 异常处理

| 异常 | 处理方式 |
|---|---|
| 源码路径不存在 | 提示用户确认路径，或使用 GitHub URL 克隆 |
| 版本无变化（快照 diff 无变更） | 跳过源码分析，询问是否做文档维护 |
| 快照文件不存在 | 运行 `snapshot.py generate` 生成初始快照 |
| 快照中缺少新模块 | 手动补充模块信息到快照，或重新 generate |
| 截图获取失败 | 插入 TODO 占位，提示用户后续补充 |
| 构建失败 | 读取错误输出，定位问题文件，修复后重试 |
| 部署失败 | 检查 Netlify token，重试或提示手动部署 |
| GitHub Release 创建失败 | 保存 release notes 到文件，提示手动创建 |

## 资源索引

| 何时读取 | 路径 |
|---|---|
| 源码快照（模块/文件/指纹） | `source-snapshot.json` |
| 快照工具（生成/对比/更新） | `scripts/snapshot.py` |
| 官网更新规范 | `references/landing-update-guide.md` |
| 文档更新规范 | `references/docs-update-guide.md` |
| 截图自动化 | `scripts/screenshot.py` |
| 归档工具 | `scripts/archive.py` |
| 归档模板 | `templates/archive-meta.md` |
| Release Notes 模板 | `templates/release-notes.md` |
| 项目设计规范 | `DESIGN.md`（项目根目录） |
| 提交规范 | `AGENTS.md`（项目根目录） |

## 触发测试

**应触发**：
- "BenchScope 发布了 v1.2.0，帮我更新文档站"
- "根据这个 PRD 更新官网功能介绍"
- "同步 benchscope 最新版本到 docs"

**不应触发**：
- "帮我写一篇博客"（非 BenchScope 文档）
- "翻译这篇文档"（纯翻译，无功能变更）
- "修改这个 Astro 组件的样式"（无版本关联的单次修改）
