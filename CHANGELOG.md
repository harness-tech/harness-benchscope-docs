# CHANGELOG

本站（BenchScope 官网 + 文档站）版本记录。**最新更新在文档最上面。**

> **当前版本定位：`1.0.0.dev`**（`package.json`）—— 版本号约定 **`x.y.z`**。
> - **z（patch）**：只打 tag + 推送代码。
> - **x.y（minor / major）**：打 tag + 推送 release + 总结 release notes + 发布（发布流程**暂未定义**）。
> - 发布命令：`pnpm release <patch|minor|major>`，详见 [AGENTS.md](./AGENTS.md) 第 8 节。
>
> 版本号说明：`Site x.y.z` 为文档站 / 仓库自身的版本；括号内为对应的 BenchScope 产品版本。
> 文末附产品版本速查，完整产品更新说明见文档中心「更新说明」与 [/zh/docs/changelog/](/zh/docs/changelog/v1-1-0/)。

---

## [Unreleased] — 官网分屏改版 v2（金色 · 双主题 · 全面优化）

### 全局

- **平滑滚动**：移除 `scroll-snap`，改为 `html { scroll-behavior: smooth }` 自然滚动。
- **屏间分界**：每屏之间增加 `border-top: 1px solid var(--line-strong)` 明确分界线。
- **内容面板**：第 2~7 屏内容统一包裹在 `.sec-panel` 容器内（`var(--bg-surface)` 背景 + 边框），视觉更清晰。

### 导航

- **扁平 SVG 图标**：替换所有 emoji 为统一金色调的 stroke 风格 SVG 图标（`home` / `sparkles` / `bolt` / `target` / `folder` / `puzzle` / `book` / `github`），颜色统一 `var(--gold)`。

### 第 1 屏（介绍）

- **流光特效**：`Mesh` 组件升级为 Canvas 渲染，金色流光沿格子线流动（水平/垂直方向，随机生成 5~12 条，带发光尾迹）。
- **打字效果**：`Typewriter` 组件改为「BenchScope · _打字后缀_」结构，品牌名保持不动，只有后缀词（Performance / 精度 / …）打字切换。

### 第 2~7 屏（图标）

- **统一扁平 SVG 图标**：功能、性能、精度、高级、快速开始所有 emoji 替换为 SVG 图标，统一 `var(--gold-text)` 颜色 + `drop-shadow` 发光。

### 第 5 屏（数据）

- **4 个 Tab 切换**：`REALTIME METRICS` / `STATISTICS` / `PERF DATAS` / `LOGS`，全部大写字母、mono 字体，点击切换显示。
- **REALTIME METRICS**：改为表格数据（10 行指标：Output TPS / TTFT / TPOT / ITL / ISL / OSL / Completed / Errors / Req/s / Duration），带绿色脉冲点 + 实时标签。
- **STATISTICS**：改为 SVG 折线图（2 张：吞吐随并发增长曲线 + TTFT 随并发增长曲线），带面积渐变填充、数据点标注。
- **PERF DATAS**：表格展示 8 级并发（c1~c128）的性能数据，数据来源 `.dev-data2/perfs` 真实测试结果。
- **LOGS**：独立 Tab，左侧日志预览 + 右侧文件列表（带查看/下载按钮）。

### 第 6 屏（高级）

- **箭头位置**：跳转箭头从左上角移至**右上角**（`top: 12px; right: 12px`）。

### 第 7 屏（快速开始）

- 左右面板均在 `.sec-panel` 容器内，保持视觉一致性。

### Footer

- **布局**：2 行，比例 4:1；第 1 行 4 列（Logo+介绍 / 超链接 / 版本 / 语言），第 2 行版权右对齐。
- **介绍列**：金色 Logo + BenchScope + 一句话介绍。
- **超链接列**：HarnessTek / BenchScope / BenchScope Docs，上下排列左对齐，图标统一 SVG。
- **版本列**：右对齐，2 行文字（BenchScope v1.1.1 / BenchScope Docs v1.0.0.dev）。
- **语言列**：下拉选框，默认简体中文，含国旗 emoji。
- **版权**：第 2 行最右侧，`© 2026 HarnessTek. All rights reserved.`

### 基础设施

- 新增 `Icons.astro` 组件（统一 SVG 图标集，支持按名称调用）。
- 重写 `Mesh.astro`（Canvas 渲染流光，沿格子线流动）。
- 重写 `Typewriter.astro`（BenchScope 静态 + 后缀打字）。
- 重写 `SiteFooter.astro`（4 列布局 + SVG 图标）。
- 重写 `Landing.astro`（全量改版，面板化 + SVG 图标 + Tab 切换 + 折线图 + 真实数据）。
- 更新 `global.css`（移除 scroll-snap，保留所有主题变量）。

---

## [Unreleased] — 文档站信息架构重构

### 文档布局（双主题 · 银色 / 黑色）

- **文档侧两级别导航**：主导航（毛玻璃、LOGO + BenchScope + DOCS 徽标、居中搜索、GitHub + 主题切换）+ 副导航十个分区（快速开始 / 安装 / 精度 / 性能 / 数据 / 工具（高级）/ CLI / API / 发布 / 帮助），hover / active 金色下划线。
- **全文栅格**：导航高亮、侧边栏点击态、面包屑、创建 / 更新时间、页脚均改用主题语义变量（`--bg*` / `--text*` / `--line` / `--gold*`）。
- **Docs 正文增强**：文章标题上方新增「面包屑 + 当前文档标题」；正文底部新增创建 / 更新时间（金色图标）；页脚渲染 `SiteFooter`。
- **章节索引路由**：各分区 `index.md` 折叠为目录根路由（如 `/zh/docs/performance/`），子导航 / 侧边栏 / 搜索索引一致指向新路由。

### 内容组织（10 个顶层分区，中英双语同步）

- 快速开始 `quickstart` / 安装 `install`（配置 + 更新与卸载）/ 精度 `accuracy`（核心 + 教程）/ 性能 `performance`（核心 + 并发 / 阈值教程）/ 数据 `data` / 工具（高级）`tools`（会话 + 设置 + 架构 + Bench 引擎）/ CLI / API / 发布 `releases`（原 changelog）/ 帮助 `help`（排障 + 贡献）。
- 新增章节落地页：`cli/index`、`api/index`（OpenAI 兼容 HTTP API + REST + WebSocket）、`releases/index`、`help/index`、`install/index`、`tools/index`。
- 全部文档文件补齐 `title` frontmatter；站内链接统一为绝对路由并指向新路径。

---

## [Site 2.0.0] — 2026-09-05

### 里程碑：迁移到 Astro + 官网分屏改版

本站完整体迁移到 **Astro 7** 静态站，全站重写（官网 + 文档），OpenClaw 设计风格，**主题色保持金色不变**。

**技术栈**

- **构建框架**：**Astro 7**（Content Collections + glob loader + Shiki 高亮 + MiniSearch 搜索 + sitemap）。
- **包管理**：**pnpm**。
- **目录**：`src/`（content / components / layouts / lib / pages / styles）+ `public/`。
- **路由**：`/zh/`、`/en/` 官网 + `/zh/docs/**`、`/en/docs/**` 文档（`[...slug]` 动态路由）。
- **内容**：40 篇中英文档入 `src/content/docs/{zh,en}`；`::: tip` 容器与相对 `.md` 链接经 `scripts/convert-docs.mjs` 转为绝对路由。
- **搜索**：MiniSearch（预生成 `search-index.json`，前端模糊+前缀搜索 modal）。
- **脚本**：`check-links`（内链/图片/路由校验，postbuild 自动跑）、`build-search-index`（prebuild）、`convert-docs`。

**官网（OpenClaw 风格，金色主题）**

- **分屏整屏滚动**：`scroll-snap` 逐屏定格；每屏左标题右内容分块布局。
- **全直角 + 图片灰色蒙版**：图片默认灰度，hover 显原图；内容块全部直角。
- **纯文字导航 + 大 LOGO**：顶栏移除色块按钮，纯文字导航；品牌 LOGO 增大至 38px。
- Hero：近黑渐变 + mono eyebrow + 细体大标题 + 衬线斜体金词 + 打字机 + 纯文字按钮。
- 板块：Hero → 功能 → 工作流程 → 测试模式 → 实时反馈 → CLI → 快速开始。

**文档页（docs.openclaw.ai 风格）**

- 近黑主题：左侧按目录自动生成的侧边栏 + 中正文 + 右侧 TOC + 上一页/下一页。
- 深色代码块（Shiki github-dark）、深色表格 / 引用 / 提示容器、金链接。

**其它**

- 根 `/` 跳转 `/zh`；站点 tab 统一 **BenchScope Docs**。
- 移除旧文档目录。`.gitignore` 适配 Astro（`dist` / `.astro` / `node_modules` / `search-index.json`）。

---

## [Site 1.1.0] — 2026-09-05

### 官网 + 文档 UI 全站改版（OpenClaw 风格）

借鉴 **openclaw.ai** 与 **docs.openclaw.ai** 的设计语言，官网与文档页全面改版，**主题色保持金色不变**（近黑背景 + 金色强调）。

**官网（新增/改版）**

- **Hero**：近黑渐变 + mono eyebrow + 大白标题 + **衬线斜体金词** + **打字机副标题** + ownership 声明 + 双按钮。
- **Topbar**：近黑毛玻璃吸顶导航（品牌 + 锚点 + GitHub + 按钮 + 中英切换）。
- **板块**：统计带 → 功能卡（6）→ 工作流程（三步）→ 测试模式（性能/精度左右分栏 + 多维度指标）→ 实时反馈（会话 + Datas）→ CLI 命令卡 + 数据集 pill → 快速开始 → 近黑页脚。
- **交互**：平滑滚动、滚动渐入、锚点高亮、返回顶部、打字机。

**文档页（改版）**

- 改为 **深色文档主题**：近黑背景 + 半透明卡片 + 金链接 + 深色代码块 + 深色表格/引用/提示。
- 顶栏近黑玻璃、侧栏近黑；右侧「本页」导航深色化。

**其它**

- 保留金色品牌（`#c8a24a` / 亮金 `#e8c76a` / 深金 `#b08a34`）。
- 站点 tab 标题统一为 **BenchScope Docs**。
- 生成 `logo-white.png`（透明底白色版，已备用未引用）。
- 根路径 `/` 跳转 `/zh/`（修复 404）。
- docs 页不显示 Apache License 2.0 字样；页脚仅版权且靠右。

---

## 产品版本速查（Application Changelog）

以下为 BenchScope 产品（PyPI）版本更新速查，完整说明见文档中心「更新说明」。

### [v1.1.0] — 2026-09-05（已发布）

会话体验、性能实时面板、Dashboard 概览与环境信息增强；Sessions 采样参数 + Markdown 高亮 + 重命名落盘；Datas 导航收敛。详见 [/zh/docs/changelog/v1-1-0/](/zh/docs/changelog/v1-1-0/)。

### [v1.0.8] — 2026-09-01（未推 PyPI）

独立精度测试模块（Accuracy）落地：Native 原生精度 + Serving 链路精度双模式评测闭环。详见 [/zh/docs/changelog/v1-0-8/](/zh/docs/changelog/v1-0-8/)。

### [v1.0.7] — 2026-08-30（未推 PyPI）

性能测试核心引擎改造：引擎抽象与自研 bench。详见 [/zh/docs/changelog/v1-0-7/](/zh/docs/changelog/v1-0-7/)。

### [v1.0.6] — 2026-08-28（PyPI `benchscope==1.0.6`）

Datas 主导航、内置数据集模块、缓存路径扩充（统一到 `~/.benchscope`）。详见 [/zh/docs/changelog/v1-0-6/](/zh/docs/changelog/v1-0-6/)。

### [v1.0.5] —（迭代开发）

v2.0 UI 大改 + 性能页双模式增强，后续 UI 与交互基础。详见 [/zh/docs/changelog/v1-0-5/](/zh/docs/changelog/v1-0-5/)。
