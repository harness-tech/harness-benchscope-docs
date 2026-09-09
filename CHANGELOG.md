# CHANGELOG

本站（BenchScope 官网 + 文档站）版本记录。**最新更新在文档最上面。**

> **当前版本定位：`1.1.0`**（`package.json`）—— 版本号约定 **`x.y.z`**。
> - **z（patch）**：只打 tag + 推送代码。
> - **x.y（minor / major）**：打 tag + 推送 release + 总结 release notes + 发布（发布流程**暂未定义**）。
> - 发布命令：`pnpm release <patch|minor|major>`，详见 [AGENTS.md](./AGENTS.md) 第 8 节。
>
> 版本号说明：`Site x.y.z` 为文档站 / 仓库自身的版本；括号内为对应的 BenchScope 产品版本。
> 文末附产品版本速查，完整产品更新说明见文档中心「更新说明」与 [/zh/docs/changelog/](/zh/docs/changelog/v1-1-0/)。

---

## [1.1.0] — 2026-09-09

**UI/UX 美化与文档规范化（Site v1.1.0）。** 全面优化落地页交互、配色对比度、文档排版与键盘导航：

### 高优先级修复
- **版本号同步**：SiteFooter 版本号与 package.json 一致（v1.0.0 → v1.1.0）
- **链接修复**：CHANGELOG 产品版本速查链接从 `/changelog/` 修正为 `/releases/`
- **拼写修复**：配置说明中 `analysys` 修正为 `analysis`（zh/en 同步）
- **银色主题金色对比度**：`--bs-gold-text` 从 `#8b6914` 调整为 `#7a5e1a`（对比度≥4.5:1，符合 WCAG AA）

### UI/UX 美化
- **按钮样式统一**：落地页 + 文档主页按钮添加 `border-radius: 6px` + hover 微交互（`transform: scale(1.02)`）
- **功能卡片交互增强**：功能 8 宫格 + 高级 6 宫格 hover 添加阴影 + 微位移
- **代码块字号优化**：代码正文字号从 9px 提升至 10px，可读性增强
- **搜索框键盘导航**：支持 ↑/↓ 键导航 + Enter 选中 + Esc 关闭

### 文档规范化
- **FAQ 格式统一**：所有文档 FAQ 从 `**Q：**\n\nA：` 统一为 `**问题：**\n回答` 格式
- **双语同步验证**：zh/en 文档文件结构完全一致（34+34 文件）
- **内链格式验证**：运行 `convert:docs` 确认无相对 `.md` 链接

### 响应式优化
- **移动端导航**：落地页导航链接添加 `title` 属性（tooltip）
- **表格字号优化**：性能屏 + 数据屏表格字号从 8.5px 提升至 12px

### 基础设施
- **新增 favicon**：添加 `public/favicon.ico`（从 logo-gold.png 复制）

---

## [1.0.0] — 2026-09-06

**首个正式版发布（Site v1.0.0）。** 官网 + 文档站全量定稿，涵盖以下内容：

- **官网**：落地页分屏改版、Logo/导航对齐、关闭翻书滚动特效。
- **文档站**：信息架构重构——副导航分区（快速开始 / 性能测试 / 精度测试 / 数据分析 / 高级工具 / CLI / API / 发布 / 帮助）、安装并入快速开始、各分区「概述」首项、发布版本倒序、文档命名去「教程 / Tutorial」前缀。
- **渲染**：代码块（字号 / 行号 / 复制 / 分主题配色）、图标圆角化、侧栏分组样式、搜索（快捷键 + 金色可用态）、目录滚动高亮。
- 详见下方 [Unreleased] 各分节。

---

## [Unreleased] — 发布流程文档化 + Netlify 部署

- **发布流程记录到 AGENTS.md**：§8.4 新增「完整发布与部署流程」（更新版本号 → 构建校验 → 提交 → 打 tag → GitHub Release（先英文后中文）→ Netlify 部署）；§8.5 新增「凭据存储约定」（token 存本地 gitignore，不入库）。
- **Netlify 部署脚本**：新增 `scripts/deploy-netlify.py`（无 CLI，直接走 Netlify API：哈希 dist/ → 创建 deploy → 上传文件 → 提升生产）；正式站点 `https://benchscope-docs.netlify.app`。
- **.gitignore**：新增忽略 `.env.netlify` / `.netlify/`（凭据与部署缓存不入库）。

---

## [Unreleased] — 导航 / 图片 / README 整理

### 主导航布局

- **搜索框移至右侧**：文档副导航（`doc-nav`）改为 `1fr auto auto`，**搜索框显示在最右侧**，**GitHub 图标位于其左侧**（品牌在最左）。

### 文档图片

- **缩至 2/3 且居中**：`.prose img` 设为 `max-width: 66.666%` + `display:block; margin:1.2em auto`，所有文档图片缩小为原尺寸 2/3 并水平居中。

### 根 README 重构

- **中英双语，默认英文**：README 改为英文在前、可切换简体中文。
- **去除开发/维护信息**：移除目录结构、pnpm 开发/构建/部署、内容维护等开发向内容；改为**介绍项目是做什么的**（BenchScope 是什么、核心能力、快速开始、文档主题、项目信息）。
- **项目名下增加中英切换**：在项目名称下新增 `<b>English</b> · <a>简体中文</a>` 语言切换链接。
- **修正 README 中 Logo 显示**：Logo 引用 `public/images/logo-gold.png`（相对路径，正确解析）。

---

## [Unreleased] — 侧栏「概述」首项

- **分区侧栏以「概述」为首项**：单分组分区（如性能测试、精度测试、CLI、API 等）不再显示与副导航同名的分区大标题，左侧栏**首个文档即「概述 / Overview」**，其后为子文档。
- **多分组分区保留分组标题**：含子分组的分区（如快速开始的「安装」子分组）仍显示统一的组标题样式。

---

## [Unreleased] — 文档命名与结构整理

- **分区落地页改名「概述」**：各分区 `index.md`（原本与分区同名，如「性能测试」「精度测试」「数据分析」「高级工具」「CLI」「发布」「帮助」等）统一改为**「概述 / Overview」**，并作为该分区侧栏**第一个文档**。
- **组标题统一样式**：侧栏中分组与子分组（如快速开始下的「安装」子分组）标题统一为**金色色块**（`--bs-gold-soft` 底 + 金描边 + 金字），一致显示。
- **发布（releases）顺序**：落地页「概述」置顶，其后版本**倒序**（`v1.1.0 → v1.0.8 → … → v1.0.5`，最新在上）。
- **性能（performance）重构**：落地页改「概述」；`concurrency` →「并发压测 / Concurrency Testing」、`threshold` →「阈值压测 / Threshold Testing」，**移除「教程：/Tutorial:」前缀**，重组为清晰的分步结构；联动清理精度 `guide`（教程：精度评测 → 精度评测）。

---

## [Unreleased] — 代码块精细优化

- **字号缩至 9px**：代码正文 / 行号均降至 `9px`，行高 1.8，内边距收窄（`.7rem`）。
- **行号与行对齐**：行号 gutter 与代码行使用一致的行高（`9px × 1.8`），行号逐行高度对齐。
- **分主题配色**：**黑色主题 → 深色代码块**（`--code-bg:#0d0d10`，token 用 `--shiki-dark` 深色高亮）；**银色主题 → 亮色代码块**（`--code-bg:#f6f6f9`，token 用内联亮色值）。启用 Shiki 双主题（`github-light` / `github-dark`）。
- **修复代码块底色失效**：改为直接命中 `<pre class="astro-code">` 元素（此前误用后代选择器 `.astro-code pre` 未命中），并用 `!important` 覆盖 Shiki 内联 `background-color`，确保银色主题显示亮色、黑色主题显示深色（不再受 OS 深色模式影响）。

---

## [Unreleased] — 文档阅读体验细化

### 代码块

- **字号缩小 + 边距加大**：代码正文字号 12.5→12px，行高 1.6→1.7，内边距增大（`.9rem 1.1rem .9rem 1rem`），文字与代码块边缘更透气。
- **行号**：代码块左侧新增行号 gutter（mono 11px，主 内容区右侧分隔线），配合 Shiki 语法高亮。

### 图标

- **圆角且缩小**：主页功能卡片 / 分类入口图标改为小尺寸圆角色块（`34×34` / `30×30`，圆角 8–9px，金字金边淡底）；侧栏分组图标同样改为圆角金块。

### 搜索

- **改为内联输入框**：主导航搜索由「点击弹窗」改为**直接可输入的搜索框**，聚焦 / 输入时下拉展示结果（含标题 + 摘要片段）。**图标 idle 灰、有文字输入 / 聚焦时变金色**（可用状态）。

### 副导航对齐

- **对齐 BenchScope 名称**：副导航首个 tab 由「对齐 Logo 左缘」改为**对齐主导航 BenchScope 名称左缘**（`padding-left: 38px`）。

### 侧栏分组

- **色块区分**：各分区侧栏分组标题改为**金色色块**（`--bs-gold-soft` 底 + 金描边 + 金字 + 圆角图标块），与列表内的具体文档链接（普通字体）明显区分。

---

## [Unreleased] — 文档信息架构与导航重构

### 副导航（1 级 tab）

- **对齐 Logo**：副导航首个 tab 与主导航 Logo 左缘对齐（`padding-left: 0`）。
- **移除「概览」tab**：副导航不再有概览项，改为九个分区，顺序 `快速开始 → 性能测试 → 精度测试 → 数据分析 → 高级工具 → CLI → API → 发布 → 帮助`。
- **安装并入快速开始**：install 不再是 1 级分区，作为 quickstart 侧栏子分组（保留独立「安装」分组标签）展示。
- **分区更名**：`精度→精度测试`、`性能→性能测试`、`数据→数据分析`、`工具（高级）→高级工具`。

### 文档主页（/docs/）

- 新增 `DocsHome.astro` **文档主页**：BenchScope 介绍 + 功能概览卡片 + 文档分类入口 + 开始使用 CTA；左侧栏只显示「主页」自身。
- 官网「文档」入口与各页「返回文档」均进入主页。

### 发布顺序

- **版本倒序**：releases 分区子页按 `v1.1.0 → v1.0.8 → … → v1.0.5` 逆序展示（最新在上）。

### 搜索

- **主导航搜索完善**：`Search.astro` 支持 `/` 或 ⌘/Ctrl+K 快捷键唤出，结果展示标题 + 摘要片段，改用主题语义变量。

---

## [Unreleased] — 文档设计规范 + 内容重构

### 文档 DESIGN 规范（DESIGN.md §4.6）

- **输出文档站 DESIGN 规范**：新增 `4.6 文档站 DESIGN 规范`，明确目录结构（Content Collections 双语对齐、kebab-case、分区顺序）、三层页面骨架（左栏分区侧栏 / 正文 / 右栏本页 TOC）、两级别导航、标题层级字号表、代码块 / 引用 / 提示块 / 表格样式，以及长文档拆分原则（>150 行拆分）。

### 排版与布局优化

- **正文字体收敛**：`.prose` 正文基调降为 `14.5px`，H1–H4 层级收窄（1.7 / 1.3 / 1.12 / 1rem），行内代码、引用、提示块字体同步缩小。
- **代码块**：代码字号降至 `12.5px`，头部语言标签 + 复制按钮细化排版。
- **表格 / 引用 / 提示块**：字号降至 13–14.5px，间距收敛，更舒适。
- **导航清理**：文档顶栏高度 56→52px、副导航 42→40px，分区链接字号与间距收敛，滚动更规整。

### 内容重构（按副导航分区拆分子页）

- **CLI**：超大 `reference.md`（275 行）拆分为 `serve` / `perf` / `eval` 三个子命令页，`index.md` 改为 CLI 概览；全站 `/cli/reference/` 链接迁移至对应新路由。
- **精度 accuracy**：`index.md` 拆为概览页 + `modes`（评测模式）/ `datasets`（评测数据集）/ `scoring`（判分器与指标）。
- **快速开始 quickstart**：拆为概览页 + `requirements`（环境要求）/ `platform`（启动平台）。
- **落地页增强**：`tools/index`、`README`（文档首页）升级为带分组导航 + 常用入口 + FAQ 的规范落地页。

---

## [Unreleased] — 文档阅读体验优化

### 侧栏（左侧目录）

- **分区联动**：侧栏只显示**当前分区**的内容（随副导航高亮分区切换），不再堆叠全部 10 个分区；文档首页（README 概览）仍显示全部分区目录。
- **图标加持**：每个分区标题新增金色 SVG 图标；文档首页新增「文档概览」返回入口。
- **交互与高亮**：激活项金色背景 + 加粗，滚动条细化为主题色。

### 面包屑

- **移除「首页」**：文档正文上方导航不再显示首页，首个目录即为「文档」。

### 渲染（代码 / 字体 / 目录）

- **代码块增强**：代码块新增头部（语言标签 + 复制按钮），深色底主题化；`bash` / `console` / `json` 等代码高亮。
- **右侧 TOC 升级**：新增「本页目录」标题与「返回文档」入口；滚动时高亮当前章节（IntersectionObserver）；标题悬停显示 `#` 锚点，便于定位。
- **正文字体与排版**：正文行高 / 标题间距优化，行内代码底色主题化。

### 内容（中英双语全面优化）

- 全站 **27 zh + 27 en** 文档逐一重写 / 润色：信息架构更清晰、补充 FAQ / 相关文档、统一绝对路由内链、规范 HTML 提示块（`tip` / `info` / `warning` / `danger`），并保持中英结构对齐。

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

会话体验、性能实时面板、Dashboard 概览与环境信息增强；Sessions 采样参数 + Markdown 高亮 + 重命名落盘；Datas 导航收敛。详见 [/zh/docs/releases/v1-1-0/](/zh/docs/releases/v1-1-0/)。

### [v1.0.8] — 2026-09-01（未推 PyPI）

独立精度测试模块（Accuracy）落地：Native 原生精度 + Serving 链路精度双模式评测闭环。详见 [/zh/docs/releases/v1-0-8/](/zh/docs/releases/v1-0-8/)。

### [v1.0.7] — 2026-08-30（未推 PyPI）

性能测试核心引擎改造：引擎抽象与自研 bench。详见 [/zh/docs/releases/v1-0-7/](/zh/docs/releases/v1-0-7/)。

### [v1.0.6] — 2026-08-28（PyPI `benchscope==1.0.6`）

Datas 主导航、内置数据集模块、缓存路径扩充（统一到 `~/.benchscope`）。详见 [/zh/docs/releases/v1-0-6/](/zh/docs/releases/v1-0-6/)。

### [v1.0.5] —（迭代开发）

v2.0 UI 大改 + 性能页双模式增强，后续 UI 与交互基础。详见 [/zh/docs/releases/v1-0-5/](/zh/docs/releases/v1-0-5/)。
