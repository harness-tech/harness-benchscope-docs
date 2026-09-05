# CHANGELOG

本站（BenchScope 官网 + 文档站）版本记录。**最新更新在文档最上面。**

> 版本号说明：`Site x.y.z` 为文档站 / 仓库自身的版本；括号内为对应的 BenchScope 产品版本。
> 文末附产品版本速查，完整产品更新说明见文档中心 `更新说明`（changelog）与 [docs/zh/docs/changelog](docs/zh/docs/changelog)。

---

## [Site 1.0.0] — 2026-09-05

### 里程碑：从 Sphinx 迁移到 VuePress 2

本站完成从旧 Sphinx（Python / Read the Docs）方案到 **VuePress 2 + Vue 3 + Vite** 的完整重写与迁移，`harness-benchscope-docs` 仓库初始化（首个正式版本）。

**新增 / 变更**

- **完全重写技术栈**：VuePress 2.0.0-rc.30（`@vuepress/bundler-vite` + `theme-default` + `plugin-search`），废除 Sphinx / Python / Read the Docs 构建链，不再需要 `requirements.txt`、`Makefile`、`conf.py`、`.rst` 源码。
- **单站中英切换**：`/zh/` ↔ `/en/`，同一域名一份部署；导航栏语言下拉切换。
- **自研金色主题**：新增 `DESIGN.md` 固化设计约定（品牌金 `#c8a24a` / 墨色 / 字体 / 布局 / 组件 / 响应式），统一 `styles/index.css` 变量与 `Landing.vue` 落地页。
- **官网落地页**（`Layout: Landing`）：多屏锚点导航（首页 / 功能 / 性能测试 / 精度测试 / 快速开始）+ 页脚 HarnessTek，深墨顶栏 + 金色光晕首屏。
- **文档页**：白色顶栏 + 金 LOGO + 左侧可折叠目录 + 右侧可隐藏「本页」导航 + 搜索。
- **内容迁移**：40 篇中英双语文档迁移并整理（快速入门 / 核心能力 / 教程 / 更新说明 / 开发指南），对应产品版本 v1.1.0 → v1.0.5。
- **工程化**：根目录版本文档体系（`README.md` / `CHANGELOG.md` / `DESIGN.md` / `AGENTS.md`）；`scripts/make_gold_logo.py` 生成透明背景金色 LOGO。
- **测试 / 校验**：新增 `npm run test:links` 校验站内链接与图片引用，构建后自动校验。

**修复 / 优化**

- 清理 Sphinx 遗留物（`source/`、`locales/`、`build/`、`.venv/`），仓库更轻量、仅保留 VuePress 一套源码。
- 所有组件、页面、配置按 `AGENTS.md` 规约组织，便于 agents 协作维护。

---

## 产品版本速查（Application Changelog）

以下为 BenchScope 产品（PyPI）版本更新速查，完整说明见文档中心「更新说明」。

### [v1.1.0] — 2026-09-05（已发布）

会话体验、性能实时面板、Dashboard 概览与环境信息增强；Sessions 采样参数 + Markdown 高亮 + 重命名落盘；Datas 导航收敛。详见 [v1-1-0](docs/zh/docs/changelog/v1-1-0.md)。

### [v1.0.8] — 2026-09-01（未推 PyPI）

独立精度测试模块（Accuracy）落地：Native 原生精度 + Serving 链路精度双模式评测闭环。详见 [v1-0-8](docs/zh/docs/changelog/v1-0-8.md)。

### [v1.0.7] — 2026-08-30（未推 PyPI）

性能测试核心引擎改造：引擎抽象与自研 bench。详见 [v1-0-7](docs/zh/docs/changelog/v1-0-7.md)。

### [v1.0.6] — 2026-08-28（PyPI `benchscope==1.0.6`）

Datas 主导航、内置数据集模块、缓存路径扩充（统一到 `~/.benchscope`）。详见 [v1-0-6](docs/zh/docs/changelog/v1-0-6.md)。

### [v1.0.5] —（迭代开发）

v2.0 UI 大改 + 性能页双模式增强，后续 UI 与交互基础。详见 [v1-0-5](docs/zh/docs/changelog/v1-0-5.md)。
