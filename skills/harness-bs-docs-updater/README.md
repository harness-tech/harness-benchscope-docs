# harness-bs-docs-updater

从 BenchScope 源码分析版本变更，自动维护 benchscope-docs 官网与文档站。

## 版本

当前版本：`1.0.0`

## 功能

1. **源码功能分析**：从本地源码仓库或 GitHub 仓库分析版本变更
2. **官网更新**：落地页内容规划、简洁说明、截图补充、Mock 数据填充
3. **文档更新**：zh/en 双语文档规范撰写，符合项目目录和措辞要求
4. **版本归档**：旧文档按版本归档到 `archives/vX.Y.Z/`，可上传代码仓库
5. **发布闭环**：构建验证 → Git 提交 → Netlify 部署 → GitHub Release

## 安装

将 `skills/harness-bs-docs-updater/` 目录复制到项目的 `skills/` 目录下即可。

技能已内置在本项目中，无需额外安装。

## 使用

### 触发方式

在与 AI Agent 交互时，使用以下话术触发：

**中文触发**：
- "BenchScope 发布了 v1.2.0，帮我更新文档站"
- "根据源码更新官网功能介绍"
- "同步 benchscope 最新版本到 docs"
- "更新文档，源码路径是 /path/to/benchscope"

**英文触发**：
- "BenchScope released v1.2.0, update the docs"
- "Update landing page based on source code"
- "Sync benchscope latest version to docs"

### 使用流程

1. **提供更新源**：告诉 Agent 源码本地路径或 GitHub URL
2. **确认版本号**：Agent 会自动提取或询问目标版本
3. **确认更新范围**：`all`（默认）/ `landing` / `docs` / `both`
4. **提供截图**（可选）：将截图放入 `public/images/` 或让 Agent 自动截图
5. **Agent 执行**：分析 → 归档 → 更新 → 验证 → 发布

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
# 归档当前版本文档
python skills/harness-bs-docs-updater/scripts/archive.py --version 1.1.0

# 仅创建元数据（不复制文档）
python skills/harness-bs-docs-updater/scripts/archive.py --version 1.1.0 --skip-docs
```

## 目录结构

```
skills/harness-bs-docs-updater/
├── SKILL.md                    # 技能核心指令
├── README.md                   # 本文件
├── references/                 # 参考文档
│   ├── landing-update-guide.md # 官网更新指南
│   └── docs-update-guide.md    # 文档更新指南
├── scripts/                    # 自动化脚本
│   ├── screenshot.py           # 自动截图
│   └── archive.py              # 文档归档
├── templates/                  # 模板文件
│   ├── release-notes.md        # Release Notes 模板
│   └── archive-meta.md         # 归档元数据模板
└── archives/                   # 版本归档目录
    └── v1.1.0/                 # 示例归档
```

## 版本管理

本技能使用语义化版本号 `x.y.z`：

| 变动 | 说明 |
|---|---|
| `z` (patch) | 修复模板错误、更新指引措辞 |
| `y` (minor) | 新增参考文档、新增脚本功能 |
| `x` (major) | 重大流程变更、不兼容更新 |

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
