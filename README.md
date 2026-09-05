<p align="center">
  <img src="docs/.vuepress/public/images/logo-gold.png" alt="BenchScope" width="96" height="96" />
</p>

<h1 align="center">BenchScope 官网 + 文档站</h1>

<p align="center">
  <strong>LLM 性能与精度可视化测试平台</strong> 的官方文档站 —— 官网落地页 + 中英双语文档，
  基于 <b>VuePress 2</b>（Vue 3）的纯静态站点，自研<b>金色主题</b>。
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/vuepress" target="_blank"><img src="https://img.shields.io/badge/VuePress-2.0.0--rc.30-c8a24a" alt="VuePress"></a>
  <a href="https://vuejs.org/" target="_blank"><img src="https://img.shields.io/badge/Vue-3.x-42b883" alt="Vue 3"></a>
  <a href="https://github.com/LABELNET/benchscope" target="_blank"><img src="https://img.shields.io/badge/License-Apache--2.0-blue" alt="License"></a>
</p>

---

## 项目说明

**BenchScope 官网 + 文档站** 是 BenchScope 大模型推理测试平台的官方站点，包含两部分：

- **官网落地页**：品牌首页，多屏锚点导航（首页 / 功能 / 性能测试 / 精度测试 / 快速开始）+ 页脚 HarnessTek，纯静态、无后端。
- **文档中心**：中英**单站切换**（`/zh/` ↔ `/en/`），覆盖快速入门、核心能力（性能 / 精度 / 会话 / 数据 / 设置）、实战教程、更新说明与开发指南。

本站已从旧的 Sphinx 方案 **完全迁移到 VuePress 2**，不再依赖任何 Sphinx / Python 文档构建链（旧源码不纳入本仓库）。部署产物为纯静态 HTML，可部署到任意静态托管。

## 站点要点

- **单站中英切换**：`/zh/` ↔ `/en/`，导航栏语言下拉切换，一份部署。
- **官网**：金色 LOGO + 锚点导航 + 文档入口 + 页脚 HarnessTek；底部链接与主导航一致。
- **文档**：白色顶栏 + 金 LOGO（点击回官网）+ 左侧可折叠目录 + 右侧可隐藏「本页」导航 + 搜索。
- **统一字体**、导航链接点击不变色、自研金色主题。
- 设计约定详见 [DESIGN.md](./DESIGN.md)。

## 目录结构

```
harness-benchscope-docs/
├── docs/                        # VuePress 站点源码
│   ├── .vuepress/
│   │   ├── config.ts           # i18n(zh/en) + 主题 + 侧边栏 + 搜索
│   │   ├── client.ts           # 全局样式 + Landing 布局注册 + 右侧「本页」导航
│   │   ├── styles/index.css    # 金色主题变量 / 字体 / 导航不染色
│   │   ├── theme/
│   │   │   ├── index.ts        # 自定义主题（继承 defaultTheme）
│   │   │   └── layouts/Landing.vue  # 官网多屏落地页
│   │   └── public/images/      # 金色 LOGO + 截图
│   ├── zh/                     # 中文
│   │   ├── README.md           # 官网（layout: Landing）
│   │   └── docs/**             # 中文文档（/zh/docs/）
│   └── en/                     # 英文
│       ├── README.md
│       └── docs/**             # 英文文档（/en/docs/）
├── scripts/
│   └── make_gold_logo.py       # 把任意单色 LOGO 染成金色（保留透明）
├── AGENTS.md                   # Harness 与 agents 协作规约
├── CHANGELOG.md                # 版本更新日志（最新在顶部）
├── DESIGN.md                   # UI 设计约定（金色主题）
├── package.json                # 依赖与脚本
└── README.md
```

## 快速开始

```bash
# 1. 安装依赖（已用 overrides 将 @vuepress/* 锁到 2.0.0-rc.30）
npm install --legacy-peer-deps

# 2. 本地开发预览（http://localhost:8080）
npm run dev

# 3. 构建静态站到 docs/.vuepress/dist/
npm run build

# 4. 校验文档链接 / 图片引用是否失效
npm run test:links
```

## 部署

```bash
npm run build && npm run test:links
```

把 `docs/.vuepress/dist/` 下的内容部署到任意静态托管（nginx / GitHub Pages / 对象存储 / CDN）即可。默认 `base: '/'`，如需部署到子路径，在 `docs/.vuepress/config.ts` 修改 `base` 后重新构建。

## 贡献 / 开发

- 新增 / 修改页面：遵循 [DESIGN.md](./DESIGN.md) 的设计约定与 [AGENTS.md](./AGENTS.md) 的协作规约。
- 修改文档内容：直接在 `docs/zh/docs/**` 与 `docs/en/docs/**` 对应文件编辑；新增入口记得同步更新 `docs/.vuepress/config.ts` 的侧边栏与 `docs/{zh,en}/docs/README.md`。
- 版本迭代：按 [CHANGELOG.md](./CHANGELOG.md) 顶部新增版本记录。

## 更多命令

| 命令 | 说明 |
| --- | --- |
| `npm run dev` | 启动开发服务器（HMR） |
| `npm run build` | 构建生产静态站 |
| `npm run test:links` | 校验站内链接与图片引用 |
| `python scripts/make_gold_logo.py <src> <dst>` | 生成金色 LOGO |

## 开源信息

- **开源协议**：本项目文档站按 [Apache License 2.0](./LICENSE) 开源（与 BenchScope 主项目一致）。
- **源码仓库**：https://github.com/LABELNET/benchscope
- **PyPI 下载**：https://pypi.org/project/benchscope
- **版权**：© HarnessTek（https://www.harness-tech.com）

---

<p align="center">Made with ❤️ by HarnessTek · Built with VuePress</p>
