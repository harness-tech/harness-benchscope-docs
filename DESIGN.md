# BenchScope 文档站 · UI 设计约定 (DESIGN)

本文档是本站（VuePress 2 静态站）**唯一的 UI 设计约定**，覆盖品牌色、字体、布局、组件与交互。所有页面与样式必须遵循本约定；新增组件前先在此补充约定，避免样式漂移。

> 核心技术栈：VuePress 2.0-rc + Vue 3 + Vite；自定义主题继承 `@vuepress/theme-default`，并注册官网落地页布局 `Landing`。
> 样式入口：`docs/.vuepress/styles/index.css`（全局覆盖）与 `docs/.vuepress/theme/layouts/Landing.vue`（落地页）。

---

## 1. 品牌（LOGO 与名称）

| 项 | 值 |
| --- | --- |
| 站点名 | **BenchScope**（品牌大小写，勿写成 Benchscope / benchscope） |
| 标语 | LLM 性能与精度可视化测试平台 |
| LOGO | `docs/.vuepress/public/images/logo-gold.png`（透明底金色） |
| 辅助 LOGO | `logo-blue.png` / `logo-black.png` / `logo-white.png`（备用场景） |
| 圆角 | LOGO 统一 `border-radius: 6px`（导航）/ `8px`（落地页） |

生成金 LOGO：`python scripts/make_gold_logo.py <src.png> <dst.png> --gold c8a24a`。

---

## 2. 色彩体系（金色主题）

「金 + 墨」双主色，背景以白 / 深墨分区。**所有颜色必须取自下表变量**，禁止硬编码近似色。

### 金色品牌系（`styles/index.css :root`）

| 变量 | 值 | 用途 |
| --- | --- | --- |
| `--bs-gold` | `#c8a24a` | 主品牌金：强调、按钮、主链接 |
| `--bs-gold-light` | `#d9bb70` | 高亮 / hover 亮金 |
| `--bs-gold-dark` | `#b08a34` | 深金：激活态、正文链接 |
| `--bs-gold-soft` | `#f6edd9` | 浅金底：卡片图标、代码背景 |

### 墨色 / 中性（同表）

| 变量 | 值 | 用途 |
| --- | --- | --- |
| `--bs-ink` | `#23201a` | 主文字 / 标题 |
| `--bs-ink-2` | `#5a564d` | 次要文字 / 标签 |
| `--bs-line` | `#e8e2d3` | 边框 / 分隔线 |
| `--bs-header-bg` | `#16130d` | 深色顶栏（落地页导航 / 页脚） |

### defaultTheme 变量覆盖

```css
--c-brand: var(--bs-gold);
--c-brand-light: var(--bs-gold-light);
--c-brand-dark: var(--bs-gold-dark);
--c-bg: #ffffff;
--c-bg-navbar: #ffffff;
--c-text: #23201a;
```

### 语义

- **金色 = 品牌 / 可行 / 激活**；**墨色 = 内容**；**深墨 = 醒目背景**。
- 代码关键字高亮金：`.token.keyword { color: var(--bs-gold-light) }`。

---

## 3. 字体

统一中英文字体栈，禁止引入外部字体（保持纯静态、无外部请求）。

```css
font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei",
  "Noto Sans SC", "Source Han Sans SC", system-ui, -apple-system, sans-serif;
```

- 正文启用：`-webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility;`
- 代码 / 命令行：`"SF Mono", "JetBrains Mono", Menlo, Consolas, monospace`（字号 13.5px）。
- 标题继承字体，`letter-spacing: .2px`。

---

## 4. 布局

本站是「**单站中英切换**」：`/zh/` ↔ `/en/`，同一域名、一份部署。

### 4.1 官网落地页（`layout: Landing`）

- **深色导航**`#16130d`（sticky top，高 62px）：品牌左、锚点导航（首页/功能/性能测试/精度测试/快速开始）、右侧 GitHub 图标 + 文档按钮 + 中英切换。
- **首屏**：径向金色光晕 + 深墨渐变背景，白色大标题（品牌金副标题）、副文案、CTA、特性标签、大图。
- **分区**：功能网格（卡片 hover 上浮 + 金边）、性能双模式（并发/阈值）、精度双模式（原生/服务）、快速开始（深色代码块含金注释 `#c8a24a` / 绿命令 `#9ecb7b`）。
- **页脚**：深墨 `#16130d`，底部导航同主导航一致，版权 `© 2026 HarnessTek · Apache License 2.0`。
- 落地页隐藏默认 navbar/footer（frontmatter：`navbar: false, footer: false`）。

### 4.2 文档页（默认主题）

- **白色顶栏** + 金 LOGO（点击回官网）+ 左侧可折叠目录 + 右侧可隐藏「本页」导航 + 搜索。
- 内容区 `max-width: 860px`（宽屏右侧目录时 `880px` 并右移留白）。
- 文档正文链接用深金 `--bs-gold-dark`。

### 4.3 右侧「本页」导航（可隐藏）⭐

由 `docs/.vuepress/client.ts` 注入（`router.afterEach` → `buildRightToc()`）：

- 固定右上（top 96px, right 18px, 宽 190px），仅 `≥1140px` 显示。
- 头部含「本页」标题 + `×` 隐藏按钮（点击添加 `.hidden` 类）。
- 二级标题 `lv1`、三级标题 `lv2`（缩进 10px），hover 左侧金竖线。
- 进入 `/docs/` 路径才注入；离开移除。仅浏览器端（SSR 跳过 `document`）。

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

- 断点：网格 `repeat(auto-fit, minmax(240px,1fr))`；性能/精度双列 `≤860px` 降为单列；落地页导航 `≤860px` 隐藏。
- 右侧「本页」目录：`≥1140px` 显示，`<1140px` 隐藏；内容区宽屏时右移留白。

---

## 7. 国际化（i18n）文案约定

- 文案资源集中在 `Landing.vue` 的 `t` 对象（`en` / `zh`），用 `route.path.startsWith('/en/')` 判断语言。
- 落地页中英一份；文档内容按 `zh/` 与 `en/` 目录分别维护。
- 新增导航 / 分区 / 特性时，务必同时补 `en` 与 `zh` 两组文案，保持双语文案对齐。

---

## 8. 构建与校验

```bash
npm install --legacy-peer-deps   # 已用 overrides 将 @vuepress/* 锁到 2.0.0-rc.30
npm run dev                      # http://localhost:8080
npm run build                    # 输出 docs/.vuepress/dist/
npm run test:links               # 检查 markdown 内链/图片引用是否失效
```

---

*（本文件为设计约定，非实现代码；具体样式以 `styles/index.css` 与 `Landing.vue` 为准。）*
