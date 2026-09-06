# BenchScope Docs · UI 设计约定 (DESIGN)

本文档是本站（**Astro 静态站**）**唯一的 UI 设计约定**，覆盖品牌色、字体、布局、组件与交互。所有页面与样式必须遵循本约定；新增组件前先在此补充约定，避免样式漂移。

> 核心技术栈：**Astro 7** + Content Collections + Shiki（代码高亮）+ MiniSearch（搜索）。
> 设计语言参照 **OpenClaw**（openclaw.ai / docs.openclaw.ai）：近黑背景 + 半透明卡片 + mono eyebrow + 衬线斜体强调，**主题色保持金色不变**。
> 样式入口：`src/styles/global.css`（全局）· `src/components/Landing.astro`（落地页入口）· 各 `Screen*.astro`（分屏组件）· `src/layouts/Base.astro` / `DocLayout.astro`（页面骨架）。

---

## 文件对应关系

落地页按屏拆分为独立组件，修改某屏时只需编辑对应文件：

| 文件 | 屏 | 内容 |
| --- | --- | --- |
| `src/components/Landing.astro` | 入口 | 导航 + 导入各屏 + Footer + 翻书/滚动 JS + 全局 CSS |
| `src/components/ScreenIntro.astro` | 第 1 屏 | 介绍（Mesh + Typewriter + CTA 按钮） |
| `src/components/ScreenFeatures.astro` | 第 2 屏 | 功能 8 宫格 |
| `src/components/ScreenPerf.astro` | 第 3 屏 | 性能 4 子面板（form/cases/rt/stat 预览） |
| `src/components/ScreenAccuracy.astro` | 第 4 屏 | 精度 + 数据集 Tags |
| `src/components/ScreenData.astro` | 第 5 屏 | 4 Tab（RT 表格 / Statistics 折线图 / PERF DATAS / LOGS） |
| `src/components/ScreenAdvanced.astro` | 第 6 屏 | 高级 6 宫格 |
| `src/components/ScreenQuickStart.astro` | 第 7 屏 | Prompt/Install/Start/Web/CLI 五步引导 |
| `src/components/ScreenNav.astro` | — | 导航栏（独立组件） |
| `src/components/SiteFooter.astro` | — | Footer |
| `src/components/Mesh.astro` | — | Canvas 网格背景 + 流光 + 鼠标变形 |
| `src/components/Typewriter.astro` | — | 打字效果 |
| `src/components/ThemeToggle.astro` | — | 主题切换按钮 |
| `src/lib/icons.ts` | — | 共享 SVG 图标模块（`ico()` 函数） |
| `src/styles/global.css` | — | 全局主题变量 + 基础样式 |

> **修改约定**：修改第 N 屏内容/样式时，编辑对应的 `Screen*.astro` 文件，不要在 `Landing.astro` 中直接修改该屏的 HTML/CSS。各屏 CSS 隔离在各自的 `<style>` 块中。

---

## 1. 品牌（LOGO 与名称）

| 项 | 值 |
| --- | --- |
| 站点名 | **BenchScope**（品牌大小写，勿写成 Benchscope / benchscope） |
| 标语 | LLM 性能与精度可视化测试平台 |
| LOGO | `public/images/logo-gold.png`（透明底金色） |
| 辅助 LOGO | `logo-blue.png` / `logo-black.png` / `logo-white.png`（备用场景） |
| 圆角 | LOGO 统一 `border-radius: 6px`（导航）/ `8px`（落地页） |

生成金 LOGO：`python scripts/make_gold_logo.py <src.png> <dst.png> --gold c8a24a`。

### Footer 小图标 Logo

Footer 超链接中 HarnessTek 使用网站 Logo 小图标（13×12px，无内边距），由 Python 脚本从 `logo-white.png` 裁剪透明边缘 + 缩放 + 染色生成：

```
public/images/logo-ht-dark.png   # 黑色主题（#8c8c96）
public/images/logo-ht-light.png  # 银色主题（#6e6e76）
public/images/logo-ht-gold.png   # hover 金色（#ecd07a）
```

生成方式：参考 `scripts/make_gold_logo.py`，用 Pillow 裁剪透明边距 → 等比缩放到 13px 内容区 → 逐像素染色。CSS 通过 `content: url()` 按主题 + hover 状态切换。

---

## 2. 色彩体系（双主题 × 金色）

全站支持**黑色主题**（默认）与**银色主题**切换。**所有颜色必须取自 CSS 变量**，禁止硬编码近似色。

### 黑色主题（`global.css :root`）

| 变量 | 值 | 用途 |
| --- | --- | --- |
| `--bs-gold` | `#d6b15a` | 主品牌亮金 |
| `--bs-gold-light` | `#e8c876` | hover 高亮亮金 |
| `--bs-gold-dark` | `#b8933f` | 激活 / 深金 |
| `--bs-gold-text` | `#ecd07a` | 亮金文字：链接、eyebrow |
| `--bg` | `#0b0b0d` | 页面背景 |
| `--bg-surface` | `#141417` | 表面 / 卡片 / 面板 |
| `--bg-float` | `#1b1b1f` | 浮层 / 强调 |
| `--bg-inset` | `#101013` | 内嵌 / 表格 |
| `--text-1` | `#ededed` | 主文字 / 标题 |
| `--text-2` | `#bcbcc4` | 正文次级 |
| `--text-3` | `#9a9aa2` | 次要文字 / 标签 |
| `--ft-text` | `#8c8c96` | Footer 专用（比 text-3 更暗） |
| `--nav-text` | `#c7c7cf` | 导航文字 |
| `--line` | `#ededed1f` | 边框 / 分隔线 |
| `--line-strong` | `#ededed33` | 强边框 |

### 银色主题（`global.css :root[data-theme='silver']`）

| 变量 | 值 | 用途 |
| --- | --- | --- |
| `--bs-gold` | `#9a7b2e` | 主品牌暗金 |
| `--bs-gold-text` | `#8b6914` | 黑金色文字 |
| `--bg` | `#ecebf0` | 页面背景 |
| `--bg-surface` | `#f7f7fa` | 表面 / 卡片 |
| `--text-1` | `#2b2b32` | 主文字 |
| `--text-2` | `#4c4c55` | 正文次级 |
| `--text-3` | `#6d6d76` | 次要文字 |
| `--ft-text` | `#6e6e76` | Footer 专用（比 text-3 更暗） |
| `--nav-text` | `#4c4c55` | 导航文字 |

### 语义映射

```css
--gold / --gold-light / --gold-dark / --gold-text / --bs-gold-soft / --gold-line  /* 金色语义别名 */
--bg / --bg-surface / --bg-float / --bg-inset   /* 背景分层 */
--text-1 / --text-2 / --text-3 / --ft-text / --nav-text  /* 文字层级 */
--line / --line-strong   /* 边框 */
```

### 语义

- **金色 = 品牌 / 可行 / 激活 / 链接 / hover**。
- **背景分层**：`--bg`（页面底）→ `--bg-surface`（卡片/面板）→ `--bg-float`（浮层）→ `--bg-inset`（内嵌/表格）。
- **文字层级**：`--text-1`（标题/主文字）→ `--text-2`（正文）→ `--text-3`（次要）→ `--ft-text`（Footer 专用，最暗）→ `--nav-text`（导航）。

---

## 3. 字体

统一中英文字体栈，禁止引入外部字体（保持纯静态、无外部请求）。**西文字体优先，中文字体衬底**，保证英文用西文形、中文不受污染。

```css
/* 正文 / 标题（OpenClaw Switzer 近似） */
font-family: "Inter", "Segoe UI", -apple-system, BlinkMacSystemFont,
  "PingFang SC", "Microsoft YaHei", "Noto Sans SC", "Source Han Sans SC", sans-serif;
```

::: tip 字体栈顺序说明
- **西文在前**：`Inter` / `Segoe UI`（近似 Switzer，OpenClaw 同款风格）。
- **中文在后**：`PingFang SC` / `Microsoft YaHei` / `Noto Sans SC`。
- **衬线斜体**（hero `<em>` 强调词）：`Georgia, "Times New Roman", "Songti SC", "STSong", serif`（近似 Sentient italic）。
- **等宽 mono**（eyebrow / 命令 / 代码）：`ui-monospace, "SF Mono", "JetBrains Mono", Menlo, Consolas, monospace`。
:::

- 正文启用：`-webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; text-rendering: optimizeLegibility;`
- 标题 `letter-spacing: -.01em`；mono eyebrow `letter-spacing: .09em + uppercase`。

---

## 4. 布局

本站是「**单站中英切换**」：`/zh/` ↔ `/en/`，同一域名、一份部署。

### 4.1 导航（`Landing.astro` 内 `.land-nav`）

- **容器**：`position: fixed; top: 0; height: 52px; z-index: 120`。毛玻璃背景（`bg-float 82% + blur(14px)`），底部 `1px var(--line)` 边框 + 阴影。
- **内容**：`max-width: 76rem; margin: 0 auto; padding: 0 24px`，flex 布局，垂直居中。
- **品牌**（左侧）：`logo-gold.png`（34×34px，`border-radius: 6px`）+ `BenchScope`（16px, 750 字重，`var(--gold-text)`）。
- **导航链接**（右侧）：flex 布局 `gap: 2px`。每个链接为 `inline-flex`，SVG 图标（14px）+ 文字（13.5px），颜色 `var(--nav-text)`。图标颜色跟随文字色。hover 时图标 + 文字均变为 `var(--gold-text)`。
- **主题切换按钮**（最右）：`34px × 34px`，`border: none`，`background: transparent`，`color: var(--nav-text)`。hover 时 `color: var(--gold-text); background: var(--bs-gold-soft)`。黑色主题显示太阳图标，银色主题显示月亮图标，通过 CSS `display: none/block` 切换。
- **导航图标列表**：`home` / `sparkles` / `bolt` / `target` / `folder` / `terminal` + `book`（文档）+ `github`。均为 SVG stroke 风格（`stroke-width: 1.8`），统一 `currentColor`。
- **响应式**：`≤720px` 隐藏链接文字，只保留图标。

### 4.2 介绍屏（第 1 屏，`#home`）

- **容器**：`.screen`（`height: 100vh`），`.intro-in`（居中布局 `text-align: center; justify-content: center`）。
- **内容顺序**（自上而下）：
  1. **Logo**：`logo-gold.png`，80×80px，`margin-bottom: 16px`。
  2. **开源标签**：`.eyebrow`（mono 12px, 700, `letter-spacing: .09em`, `text-transform: uppercase`, `var(--gold)`），内容 `Open Source · Harness Coding`。
  3. **品牌名 + 打字效果**：`<h1>` 内使用 `Typewriter` 组件。
     - `BenchScope`（品牌名）：固定不动，`var(--gold-text)`，850 字重。
     - 换行后为打字内容：`0.55em`（相对 h1），`var(--gold-light)`，600 字重，`letter-spacing: .06em`。英文内容全部大写。
     - 打字速度：打字 65ms / 删除 35ms / 停顿 1500ms。通过 `textNode.data` 直接操作文本节点（非 `textContent`），保证流畅。
     - 光标：`2px` 宽，`1em` 高（相对打字容器），`var(--gold-light)`，`vertical-align: text-bottom`，闪烁动画 `1s steps(2)`。
  4. **简介**：`var(--text-2)`，`13~15px`（clamp），`max-width: 52ch`，居中。
  5. **按钮行**：flex 居中 `gap: 16px`。
     - **Get Started**（primary）：`var(--gold)` 底色 + `#2b200a` 深字。银色主题改为 `#2b2b32` 深底 + `#f0e6c8` 暖白字。
     - **Read the Docs**（ghost）：`var(--gold)` 描边 + `var(--gold-text)` 金色字。银色主题改为 `#2b2b32` 描边 + 深灰字。

- **背景 Mesh 组件**（`Mesh.astro`）：
  - 全部用 Canvas 绘制（无 DOM 格子），`position: absolute; inset: 0`。
  - **网格线**：固定 34px 间距，`rgba(214,177,90, 0.08)` 淡金色，`lineWidth: 1`。
  - **鼠标变形**：鼠标附近网格线做正弦波起伏（`sin((x+y)*0.04 + elapsed*3)`），沿鼠标方向弯曲偏移，最大 6px。衰减半径 = 格子尺寸 × 6，二次衰减（`falloff²`）。鼠标区域网格线自动变亮（`0.08 → 0.26`）。
  - **流光**：沿网格线流动，每帧应用同样的变形函数，流光路径跟随变形后的网格线弯曲。5~10 条，随机方向（水平/垂直），带发光尾迹。
  - **事件监听**：`mousemove` 监听在 `.screen`（section）级别，避免被 `intro-in` 的 `z-index: 1` 遮挡。

### 4.3 落地页全局布局（`Landing.astro`）

- **滚动切换**：`.landing` 容器 `scroll-snap-type: y mandatory; overflow-y: scroll; height: 100vh`，每个 `.screen` 加 `scroll-snap-align: start; scroll-snap-stop: always`，滚轮操作自动锁定到下一/上一屏。
- **翻书特效**：已隐藏（JS 代码已移除），保留 CSS 以备后续启用。
- **滚动指示器**：固定右侧垂直居中，椭圆条形状（`width: 6px; height: 20px; border-radius: 3px`）。当前屏高亮（`height: 32px` + 金色背景），非当前屏灰色。
- **面板尺寸**：`.sec-panel` 设 `min-height: 540px; max-height: 810px; min-width: 900px; max-width: 1440px`（最小适配 720P，最大适配 1080P），居中显示。屏幕拉伸时背景 Mesh 跟着拉伸，面板不拉伸。
- **Footer 作为 snap 的一部分**：Footer 区域（`.footer-screen`）加 `scroll-snap-align: start`，在 Quick Start 屏向下滑动 → snap 到 footer → footer 显示；向上滑动 → snap 回 Quick Start → footer 隐藏。
- **回到顶部按钮**：固定位置（`bottom: 32px`，`right` 与面板右边缘对齐），默认隐藏。非首屏且非 footer 可见时显示。footer 出现时隐藏。点击回到介绍屏。
  - 黑色主题：金色按钮 `var(--gold)` + 深色字 `#2b200a`。
  - 银色主题：银色按钮 `#b0b0b8` + 白字，hover `#c8c8d0`。
- **全直角**：所有卡片、图片包裹、指标块、命令块一律 `border-radius: 0`。
- **图片**：默认**灰色蒙版**（`filter: grayscale(1) brightness(.75)`），**hover 显示原图**。
- **第 2~7 屏**：内容统一包裹在 `.sec-panel` 容器内（`var(--bg-surface)` 背景 + 边框）。所有小图标为 SVG stroke 风格，默认 `var(--text-2)`（文字色），hover 面板时变为 `var(--gold-text)` 金色。
- **第 3 屏（性能）子面板**：
  - 4 列横排（`grid-template-columns: repeat(4, 1fr); grid-auto-rows: 1fr`），面板背景透明（`background: transparent`），禁用 `flowcell` 的 `conic-gradient`。
  - 头部区域固定高度（head 28px + 描述 32px），预览区 `flex: 1` 填满剩余空间，4 个面板内容高度一致。
  - 内容颜色统一 `var(--text-2)`，hover 面板时数值/表格右对齐列变金色。银色主题 hover 用 `var(--bs-gold-text)`。
  - Tags 行：每个面板 2 个标签 + `···` 省略标签，`flex-shrink: 0`。
- **第 4 屏（精度）**：
  - 左侧主面板（`acol-main`）：3 列布局 `2fr 1fr 1fr`。主面板包含 Mesh 背景 + 标题 + 描述 + 数据集 Tags 行。
  - **数据集 Tags**：`MMLU` / `GSM8K` / `C-Eval` / `HumanEval` / `MATH` / `BBH` / `ARC` / `HellaSwag`，`10px mono` 字体，`var(--bg-inset)` 背景，hover 主面板时 tags 边框变金色 + 文字变金色。
  - 右侧 2 列各 2 个子面板（共 4 个），图标尺寸 28px（`.ficon-lg`）。
  - 主面板无 `overflow: hidden`，`.row-lead-in` z-index: 2 确保内容浮在 Mesh 之上。
- **第 5 屏（数据）**：
  - 4 个 Tab 全大写 mono 字体（`REALTIME METRICS` / `STATISTICS` / `PERF DATAS` / `LOGS`），点击切换显示。`.dpanel` flex column 布局，`.dbody` `flex: 1; overflow: auto; min-height: 0`。
  - **提示文字**：`* Reference data...` 放在 tab 栏右侧（`.dtab-foot`，`9.5px mono`，`opacity: .7`）。
  - **REALTIME METRICS**：紧凑表格（th `9px` / td `10.5px` mono），8 列（Metric / avg / min / max / p99 / p90 / p50 / std），11 行数据。hover 单元格变金色，hover 行微弱金色背景。
  - **STATISTICS**：2×3 grid 直接 6 块折线图，无分组标题，无 X 轴标签。SVG 折线 + 圆点标记 + 面积填充，默认灰色 `var(--text-3)`，hover 图表时折线/数据点/面积变金色。`preserveAspectRatio="none"`，曲线完全填充格子。
  - **PERF DATAS**：紧凑表格（th `9px` / td `10.5px` mono），8 列（Requests / Output TPS / Peak TPS / Total TPS / TTFT / TPOT / ITL / Detail），9 行数据。`table-layout: fixed`。hover 值变金色，hover 行微弱金色背景。Output TPS 列默认金色加粗。
  - **LOGS**：左右两栏（`1fr 1fr`），高度充满一致。左侧日志预览（`.logview`，`10px/1.6 mono`，`overflow-y: auto` 内部滚动条，`pre-wrap`）。右侧文件列表（6 个文件，th `8.5px` / td `9.5px`，Size 列右对齐，颜色统一 `var(--text-2)` 不高亮）。
- **第 6 屏（高级）**：跳转箭头 `↗` 在卡片**右上角**（`top: 12px; right: 12px`）。
- **右侧滚动提示器**：固定右侧垂直居中，圆点指示当前屏。
- 落地页内容由各 `Screen*.astro` 组件独立定义文案（`isEn` 条件），**中英双语必须同步**。

> **Astro Scoped CSS 注意**：Landing.astro 的 `<style>` 块会被 Astro 自动添加 `[data-astro-cid-xxx]` 属性限定。JS 动态创建的元素（如翻书 `.fx` / `.tile`）不带此属性，其样式必须使用 `:global()` 选择器（如 `:global(.fx)` / `:global(.fx .tile)`）。

### 4.4 第 7 屏 Quick Start（`ScreenQuickStart.astro`）

- **左侧按钮列表**：5 个步骤按钮，无数字序号，纯图标 + 大写标签：`PROMPT` / `INSTALL` / `START` / `WEB` / `CLI`。
- **右侧内容区**（`.qcontent`）：Mesh 背景网格，各 pane 通过 `data-step` 切换。
  - **PROMPT**：居中布局（`flex + justify-content: center`），无小图标，提示词文本框（`var(--bg-inset)` 背景 + 边框），hover 时流光转圈效果（`conic-gradient` + `@property --pf` 动画）。Copy Prompt 按钮 hover 金色。
  - **INSTALL**：标题 + 描述 + 命令块。PyPI 链接有独立边框，Python 版本列表右对齐显示。
  - **START**：标题 + 描述 + 命令块 + 参数表格。
  - **WEB**：标题 + 描述 + 浏览器外壳模拟（圆点按钮 + 地址栏 + 缩小版截图，hover 显示原图）。
  - **CLI**：Perf / Eval 两个子 Tab 切换，各显示命令 + 参数说明表。

### 4.5 Footer（`SiteFooter.astro`）

- **高度**：固定 `208px`（导航 52px × 4）。
- **布局**：2 行 flex，比例 4:1。Row1 占 4 份，Row2 占 1 份。
- **Row1（4 列）**：
  - **Col 1**（左）：金色 Logo + BenchScope + 介绍文字，上下居中。
  - **Col 2**（左）：超链接（HarnessTek / BenchScope / BenchScope Docs），上下居中 + 左对齐。HarnessTek 用网站 Logo 小图标（`logo-ht-dark.png` / `logo-ht-light.png`，13px，无内边距），BenchScope / Docs 用 GitHub SVG 图标。图标颜色 = 文字颜色（`var(--ft-text)`），hover 时图标 + 文字均变为金色。
  - **Col 3**：弹性空白（`flex: 1`），撑开左右间距。
  - **Col 4**（右）：自上而下——语言下拉选框（默认简体中文，含国旗 emoji）→ 空白间距（8px）→ `BenchScope v1.1.1` → `BenchScope Docs v1.0.0.dev`。版本文字更小（`10.5px`），右对齐。
- **Row2**：版权 `© 2026 HarnessTek. All rights reserved.` 靠右 + 上下居中。
- **颜色**：Footer 所有文字使用 `var(--ft-text)`（比页面文字更暗，与导航/内容区区分）。hover 统一金色 `var(--gold-text)`。
- **响应式**：`≤880px` 隐藏 Col3 空白列，Col4 左对齐；`≤560px` 单列。

### 4.6 文档页（默认主题）

> 参照 **docs.openclaw.ai**：**近黑文档主题 + 金色强调**（阅读区深色，非白底）。

- **顶栏**：近黑玻璃（`#19191c` + blur）+ 金 LOGO + 搜索 + 中英切换。
- **左侧可折叠目录 + 右侧可隐藏「本页」导航**（`bs-right-toc-*`）。
- **阅读区**：深背景 `#101012`、正文 `#bcbcc4`、大标题 `#ededed`；正文链接金 `#e8c76a`；表格/引用/提示块统一深色 `#19191c` + 金强调。
- **代码块**：近黑 `#131316` + `1px #ededed1f` 边框；mono 字体；关键字金、字符串绿、注释灰。
- 内容区 `max-width: 860px`（宽屏右侧目录时右移留白）。
- 字体：文档正文 `Inter/Segoe UI/PingFang`；代码 `SF Mono / JetBrains Mono`。

### 4.7 右侧「本页」导航（TOC）

由 `src/layouts/DocLayout.astro` 的内联 `<script>` 构建（扫描 `.prose` 内 h2/h3，映射锚点链接）：

- 固定右侧（`position: sticky; top: 60px`），仅当文档页存在多级标题时渲染。
- 二级标题 `lv1`（600 字重）、三级标题 `lv2`（缩进 14px）。
- 左侧金竖线引导，hover 金色。响应式：`≤1000px` 隐藏。

---

## 5. 组件与交互状态

| 状态 | 约定 |
| --- | --- |
| 导航链接 | 点击 / 访问后**不变色**（覆盖 `:visited` 为 `color: inherit`） |
| hover | 亮金 `--bs-gold-light` 或深金，视底色而定 |
| 激活态（active） | 深金 `--bs-gold-dark` 加粗 |
| 按钮 primary | 金底 `#c8a24a`、深色字 `#4a3a12`、圆角 999px；hover 深金底 + 白字 |
| 按钮 ghost | 金描边 + 金字；hover 金淡底 |
| 卡片 | 白底、`--bs-line` 边框、圆角 14px、柔和金阴影；hover 上浮 4px + 金边 |
| 侧边栏 | 分组标题墨色 600，open/hover 深金 |

---

## 6. 响应式

- 断点：功能网格 `repeat(auto-fit, minmax(250px,1fr))`；性能/精度双列 `≤880px` 降为单列；顶栏导航 `≤880px` 隐藏。
- 文档页：`≤1000px` 隐藏右侧 TOC；`≤760px` 隐藏左侧侧边栏（内容单列）。

---

## 7. 国际化（i18n）文案约定

- **官网**：文案资源分散在各 `Screen*.astro` 组件内（每个组件独立定义 `isEn` 条件文案），由 `lang` prop 选择；landing 页面按 `/zh/`、`/en/` 分别生成。**中英双语必须同步**。
- **文档**：内容按 `src/content/docs/zh` 与 `en` 分别维护；页面路由 `/zh/docs/**`、`/en/docs/**`。
- 新增导航 / 分区 / 特性时，务必同时补 `en` 与 `zh` 两组文案，保持双语文案对齐。顶栏语言切换在 `Base.astro`（`/zh/` ↔ `/en/`）。

---

## 8. 构建与校验

```bash
pnpm install                 # 安装依赖
pnpm dev                     # 开发预览（http://localhost:4321）
pnpm build                   # 构建静态站到 dist/（自动生成搜索索引 + 链接校验）
pnpm test:links              # 检查文档内链 / 图片 / 路由是否失效
pnpm convert:docs            # 将旧式 ::: 容器与相对 .md 链接转为 Astro 绝对路由
pnpm release <patch|minor|major>   # 版本发布（patch=打tag+推代码；minor/major=tag+notes+发布待定义）
```

---

*（本文件为设计约定，非实现代码；具体样式以 `src/styles/global.css` 与各 `Screen*.astro` 组件为准。修改某屏时请参考顶部「文件对应关系」表。）*
