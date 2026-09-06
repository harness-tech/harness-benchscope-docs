<p align="center">
  <img src="public/images/logo-gold.png" alt="BenchScope" width="96" height="96" />
</p>

<h1 align="center">BenchScope Docs</h1>

<p align="center">
  BenchScope —— 大模型推理平台的<strong>官方文档</strong>。
</p>

---

## 项目说明

**BenchScope Docs** 是 BenchScope 大模型推理测试平台的官方文档，涵盖快速入门、核心能力、实战教程、更新说明与开发指南，支持**中英双语**（`/zh/` ↔ `/en/`）。基于 **Astro** 构建的纯静态站点，OpenClaw 风格（近黑 + 金色主题）。

关于 BenchScope 本身（安装与使用）：

```bash
pip install benchscope
```

- [![GitHub](https://img.shields.io/badge/GitHub-LABELNET%2Fbenchscope-181717?logo=github&logoColor=white&style=flat)](https://github.com/LABELNET/benchscope)
- [![PyPI](https://img.shields.io/badge/PyPI-benchscope-3775a9?logo=pypi&logoColor=white&style=flat)](https://pypi.org/project/benchscope)

## 目录结构

```
harness-benchscope-docs/
├── astro.config.mjs         # Astro 配置
├── public/                  # 静态资源（images / search-index.json）
├── src/
│   ├── content.config.ts    # Content Collections 配置
│   ├── content/docs/        # 文档内容（zh / en）
│   ├── components/          # Landing / Search / Typewriter / DocsIndex
│   ├── layouts/             # Base / DocLayout
│   ├── lib/sidebar.ts       # 侧边栏与前/后文逻辑
│   ├── pages/               # /zh /en /zh/docs /en/docs 路由
│   └── styles/global.css    # OpenClaw 风格全局样式（金主题）
├── scripts/                 # 链接校验 / 搜索索引 / 文档转换
├── AGENTS.md                # Harness 与 agents 协作规约
├── CHANGELOG.md             # 版本更新日志（最新在顶部）
├── DESIGN.md                # UI 设计约定
├── package.json             # 依赖与脚本
└── README.md
```

## 快速开始

```bash
# 1. 安装依赖（pnpm）
pnpm install

# 2. 本地开发预览
pnpm dev

# 3. 构建静态站（自动生成搜索索引 + 链接校验）
pnpm build

# 4. 单独校验链接
pnpm test:links
```

## 部署

```bash
pnpm build
```

把 `dist/` 下的内容部署到任意静态托管（nginx / GitHub Pages / 对象存储 / CDN）即可。默认 site 见 `astro.config.mjs`，按需修改 `site` 后重新构建。

## 开发 / 内容维护

- **修改文档**：直接编辑 `src/content/docs/{zh,en}/**/*.md`（中英双语需同步）。
- **新增页面/样式**：遵循 [DESIGN.md](./DESIGN.md) 与 [AGENTS.md](./AGENTS.md)。
- **导入旧内容**：`::: tip` 容器与相对 `.md` 链接可用 `pnpm convert:docs` 转换。
- **版本与发布**：当前版本 **`1.0.0.dev`**，约定 `x.y.z`。发布用 `pnpm release <patch|minor|major>`；patch 只打 tag + 推送，minor/major 加 release notes + 发布（待定义）。详见 [AGENTS.md](./AGENTS.md) 第 8 节。
- **版本日志**：按 [CHANGELOG.md](./CHANGELOG.md) 顶部新增版本记录。

## 开源信息

- **开源协议**：[Apache License 2.0](./LICENSE)
- **源码仓库**：https://github.com/LABELNET/benchscope
- **PyPI 下载**：https://pypi.org/project/benchscope
- **版权**：© HarnessTek（https://www.harness-tech.com）
