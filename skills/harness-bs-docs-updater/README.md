# harness-bs-docs-updater

以 BenchScope 源码为唯一事实来源，通过**功能快照（feature snapshot）**驱动 benchscope-docs 官网与文档站的全覆盖、可校验更新。

## 版本

当前版本：`2.0.0`

## 核心理念

1. **功能快照优先**：任何文档更新都从一份功能快照（`feature-snapshot.json`）出发，快照是文档的**唯一事实来源**。
2. **全覆盖可校验**：文档覆盖度由工具自动校验，44 个核心指标必须 100% 出现在 zh/en 文档中。
3. **文档规范强制**：所有文档必须遵循 `references/docs-update-guide.md`（话术 / 段落 / 指标表规范）。
4. **每次全量重模拟**：每次迭代都重新跑全量用例生成新快照，不做增量-only。
5. **快照存放硬规则**：功能快照存于**技能目录**，**绝不放入 `archives/` 归档目录**。

## 功能

1. **功能快照生成**：模拟跑全量用例 + 解析源码，生成 `feature-snapshot.json`
2. **覆盖分析**：按快照核对现有文档覆盖度，产出偏差 / 缺口报告
3. **文档更新**：按快照修复偏差、补全缺口、撰写 zh/en 双语文档（遵循文档规范）
4. **覆盖校验**：重跑覆盖度检查，确认核心指标与全部功能点 100% 覆盖
5. **版本归档**：旧文档按版本归档到 `archives/vX.Y.Z/`（功能快照不归档）
6. **官网更新**：落地页（Screen\*.astro）内容与截图规划
7. **发布闭环**：构建验证 → Git 提交 → Netlify 部署

## 安装

将 `skills/harness-bs-docs-updater/` 目录复制到项目的 `skills/` 目录下即可。

技能已内置在本项目中，无需额外安装。

## 使用

### 触发方式

在与 AI Agent 交互时，使用以下话术触发：

**中文触发**：
- "BenchScope 发布了 v1.2.0，帮我更新文档站"
- "核对文档和功能的偏差，补全核心指标"
- "模拟跑全量用例，生成功能快照"
- "同步 benchscope 最新版本到 docs"
- "更新文档，源码路径是 /path/to/benchscope"

**英文触发**：
- "BenchScope released v1.2.0, update the docs"
- "Verify docs against features, complete the core metrics"
- "Run all cases, generate the feature snapshot"
- "Sync benchscope latest version to docs"

### 使用流程（feature-snapshot-first）

1. **提供更新源**：告诉 Agent 源码本地路径或 GitHub URL
2. **确认版本号**：Agent 会自动提取或询问目标版本
3. **Phase 0 — 准备**：隔离测试端口（`BS_TEST_PORT` / `BS_MOCK_PORT`），确认测试环境
4. **Phase 1 — 功能快照**：模拟跑全量用例（`tests/run_tests.sh`）+ CLI 模拟运行（perf / eval），生成 `feature-snapshot.json`
5. **Phase 2 — 覆盖分析**：`feature_snapshot.py coverage` 核对覆盖度，产出偏差 / 缺口报告
6. **Phase 3 — 文档更新**：按快照 + 偏差报告修复偏差、补全缺口（遵循 `references/docs-update-guide.md`）
7. **Phase 4 — 覆盖校验**：重跑 coverage，确认 44 个核心指标 100% 覆盖
8. **Phase 5 — 版本归档**：`archive.py` 归档旧文档（功能快照不归档）
9. **Phase 6 — 官网更新**：落地页内容与截图
10. **Phase 7 — 截图处理**：Playwright 自动截图
11. **Phase 8 — 构建发布**：`pnpm test:links` + `pnpm build` → Git 提交 → Netlify 部署

### 功能快照工具

```bash
# 生成功能快照（模拟跑用例 + 解析源码）
python3 skills/harness-bs-docs-updater/scripts/feature_snapshot.py generate \
  --source /path/to/benchscope \
  --cases /path/to/cases.json \
  --output skills/harness-bs-docs-updater/feature-snapshot.json

# 覆盖度检查（有缺口时 exit 2）
python3 skills/harness-bs-docs-updater/scripts/feature_snapshot.py coverage \
  --snapshot skills/harness-bs-docs-updater/feature-snapshot.json \
  --docs src/content/docs \
  --output /tmp/coverage_report.json

# 校验快照存放位置（拒绝 archives/）
python3 skills/harness-bs-docs-updater/scripts/feature_snapshot.py validate \
  --path skills/harness-bs-docs-updater/feature-snapshot.json
```

### 源码快照工具（自动发现）

```bash
# 从真实源码树自动发现 modules（修复陈旧 manifest）
python3 skills/harness-bs-docs-updater/scripts/snapshot.py generate \
  --source /path/to/benchscope \
  --output skills/harness-bs-docs-updater/source-snapshot.json

# 对比快照与源码差异（增量更新）
python3 skills/harness-bs-docs-updater/scripts/snapshot.py diff \
  --source /path/to/benchscope \
  --snapshot skills/harness-bs-docs-updater/source-snapshot.json --json
```

### 自动截图

需要 Playwright 支持：

```bash
pip install playwright
playwright install chromium
```

截图命令：
```bash
# 单页截图
python skills/harness-bs-docs-updater/scripts/screenshot.py \
  --url http://localhost:4321/zh/ \
  --output public/images/landing-zh.png

# 全页截图
python skills/harness-bs-docs-updater/scripts/screenshot.py \
  --all --output-dir public/images/
```

### 手动归档

```bash
# 归档当前版本文档（自动打包为 tar.gz）
python skills/harness-bs-docs-updater/scripts/archive.py --version 1.1.0

# 仅创建元数据（不复制文档）
python skills/harness-bs-docs-updater/scripts/archive.py --version 1.1.0 --skip-docs

# 仅打包已有归档目录为 tar.gz
python skills/harness-bs-docs-updater/scripts/archive.py --version 1.1.0 --pack-only
```

归档产物：
```
archives/
├── v1.1.0/           # 归档目录（docs 快照 + META.md）
└── v1.1.0.tar.gz     # 归档压缩包（可上传仓库）
```

> **硬规则**：功能快照（`feature-snapshot.json`）**绝不归档**，只归档旧版本文档。

## 目录结构

```
skills/harness-bs-docs-updater/       # 技能目录
├── SKILL.md                          # 技能核心指令（v2.0.0 feature-snapshot-first）
├── README.md                         # 本文件
├── feature-snapshot.json             # 功能快照（文档唯一事实来源，不放 archives/）
├── source-snapshot.json              # 源码快照（模块/文件指纹，自动发现生成）
├── references/                       # 参考文档
│   ├── docs-update-guide.md          # 文档规范（话术/段落/指标表，强制）
│   └── landing-update-guide.md       # 官网更新指南
├── scripts/                          # 自动化脚本
│   ├── feature_snapshot.py           # 功能快照工具（generate/coverage/validate）
│   ├── snapshot.py                   # 源码快照工具（generate/diff/bump，自动发现）
│   ├── screenshot.py                 # 自动截图
│   └── archive.py                    # 文档归档
└── templates/                        # 模板文件
    ├── release-notes.md              # Release Notes 模板
    └── archive-meta.md               # 归档元数据模板

archives/                             # 旧版本文档归档（项目根目录，由技能维护）
├── v1.1.0/                           # 示例归档目录（docs 快照 + META.md）
└── v1.1.0.tar.gz                     # 示例归档压缩包
```

## 版本管理

本技能使用语义化版本号 `x.y.z`：

| 变动 | 说明 |
|---|---|
| `z` (patch) | 修复模板错误、更新指引措辞 |
| `y` (minor) | 新增参考文档、新增脚本功能 |
| `x` (major) | 重大流程变更、不兼容更新（如 v2.0.0 feature-snapshot-first） |

版本号记录在 `SKILL.md` 的 YAML front matter 中。

## 依赖

| 依赖 | 用途 | 必需 |
|---|---|---|
| Python 3.9+ | 运行脚本 | ✅ |
| Git | 源码克隆、版本管理 | ✅ |
| pnpm | 构建验证 | ✅ |
| playwright | 自动截图 | 可选 |

## 环境变量

| 变量 | 来源 | 用途 |
|---|---|---|
| `NETLIFY_AUTH_TOKEN` | `~/.env.netlify` | Netlify 部署 |
| `GITHUB_TOKEN` | `~/.env.github` | GitHub Release |
| `BS_TEST_PORT` | （运行时） | 模拟跑用例的被测服务端口（隔离） |
| `BS_MOCK_PORT` | （运行时） | 模拟跑用例的 mock OpenAI 端口（隔离） |