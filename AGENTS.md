# AGENTS — Harness 与 Agents 协作规约

本文件是 **本站（BenchScope 官网 + 文档站）面向 agents（含大模型编程助手）与人工维护者的协作与开发规约**。任何在本仓库执行的 agent 应在动手前阅读本文件，并遵循下述规则。

> 术语：**Harness** 指运行本仓库任务的执行框架/环境（含 deepseek-harness，下称 DSH）；**Agent** 指在本仓库中执行任务的智能体。本文件统一定义两者在本仓库内的协作方式。

---

## 1. 共识与优先级

1. **仓库根文档是行为契约**：`README.md`（项目说明与快速开始）、`DESIGN.md`（UI 设计约定）、`CHANGELOG.md`（版本日志）、`AGENTS.md`（本文件）。四者互不冲突，以各自主题为最高优先级来源。
2. **DESIGN.md 优先于实现直觉**：凡涉及视觉、颜色、字体、布局、交互，一律以 `DESIGN.md` 为唯一口径，禁止引入未定义的近似色 / 第三方字体 / 外链样式。
3. **技术栈固定为 Astro**：本站由 Astro 构建。需要文档构建能力时，只改 Astro 相关文件（`.astro` / `src/`）。
4. **内容与展示分层**：文档内容（`src/content/docs/{zh,en}`）与样式/组件（`src/styles`、`src/components`、`src/layouts`）分离；内容改动不应侵入展示层，反之亦然。**本站完全基于 Astro**。

---

## 2. 任务执行范式（Plan → Todo → Feedback → Test）

本仓库要求 agent 按以下闭环范式工作，避免“一把梭”：

### 2.1 计划（Plan）
- 动手前先给出**简短计划**：目标、影响面（改哪些文件）、验证方式。
- 计划应显式声明涉及的技术栈（Astro / TypeScript）。

### 2.2 待办（Todo）
- 使用待办清单（如 `todo` 工具）将计划拆解为**可勾选步骤**。
- 每完成一步即更新状态；跨会话的任务保留待办以便续跑。

### 2.3 反馈（Feedback）
- 每个阶段性完成后，向维护者输出**简明反馈**：做了什么、结果如何、下一步。
- 遇到阻塞（依赖不可用、命令失败、路径缺失）需先排查，再如实上报，不得臆测或跳过。

### 2.4 测试（Test）
- 每个改动必须经过**构建/校验**验证，不提交未经验证的改动。
- 标准验证命令见第 5 节；任何 agent 在本仓库完成后应至少运行一次相关校验。

---

## 3. Harness 规约（本仓库内）

### 3.1 环境
- 工作区根：仓库根目录（`harness-benchscope-docs`）。
- DSH（deepseek-harness）安装路径仅供**检查/扩展 DSH 自身**使用；本仓库开发**不修改 DSH 安装**，也不以之为依赖。
- 本仓库自身是一个独立 Astro 项目，Node / pnpm 工具链独立管理。

### 3.2 命令与运行时（Harness 内执行）
- 在本仓库内执行命令时，工作目录一律指向仓库根（除非命令明确需要在子目录运行）。
- 长时间运行的命令（如 `pnpm install` / `pnpm build`）可后台运行并轮询结果，避免阻塞。
- 命令失败务必读取退出码与错误输出，不要忽略 `[exit code: N]`。

### 3.3 文件访问
- 使用读写/搜索工具（而非 `cat` / `grep`）检查文件内容，尊重文件观察策略。
- 修改既有文件前先读取；改动保持最小、可审查。
- 不提交构建产物与缓存（见 4.3）。

---

## 4. 目录与文件规约

### 4.1 目录结构（以 README.md 为准，此处重申关键点）

```
astro.config.mjs               # Astro 配置
public/images/                 # LOGO + 截图（gold / white / black / blue）
src/
├── content.config.ts          # Content Collections 配置
├── content/docs/{zh,en}/**    # 中文 / 英文文档（markdown）
├── components/                # Landing / Search / Typewriter / DocsIndex
├── layouts/                   # Base（骨架+顶栏）/ DocLayout（侧栏+正文+TOC）
├── lib/sidebar.ts             # 侧边栏与前/后文逻辑
├── pages/{zh,en}/             # 官网 + 文档路由
└── styles/global.css          # OpenClaw 风格全局样式（金主题，唯一视觉口径）
scripts/                       # check-links / build-search-index / convert-docs / make_gold_logo
AGENTS.md · CHANGELOG.md · DESIGN.md · README.md · package.json
```

### 4.2 内容改动约定
- **双语对齐**：凡改动 `src/content/docs/zh/**`，须同步改动 `src/content/docs/en/**` 对应文件；反之亦然。缺一不可。
- **链接形式**：文档内链接一律用**绝对路由**（`/zh/docs/...`、`/en/docs/...`）；不得引入相对 `.md` 链接或 `::: tip` 旧式容器（如从旧源导入，用 `pnpm convert:docs` 转换）。
- **入口同步**：新增文档页后，侧边栏由 `src/lib/sidebar.ts` 按目录自动生成（无需手工改菜单）。
- **版本日志**：任何面向用户的特性 / 修复，须在 `CHANGELOG.md` **顶部**新增版本记录（新版在最上）。
- **技术栈声明**：本站固定使用 Astro；禁止引入其他静态站框架的构建文件（`.rst`、`conf.py`、`Makefile`、`requirements.txt` 等）。

### 4.3 禁止提交的产物
- `node_modules/`
- `dist/`、`.astro/`
- `*.log`、`.DS_Store`
- （已由 `.gitignore` 覆盖，提交时复核）

---

## 5. 标准命令与校验（Agents 与维护者共用）

```bash
pnpm install            # 安装依赖
pnpm dev                # 本地开发预览（http://localhost:4321）
pnpm build              # 构建静态站到 dist/（自动生成搜索索引 + 链接校验）
pnpm test:links         # 校验站内链接 / 图片 / 路由（内容级测试）
pnpm convert:docs       # 将旧式 ::: 提示容器与相对 .md 链接转为 Astro 绝对路由
```

**测试职责划分**
- `test:links`：内容 / 链接级校验，每次内容改动后**必须**运行。
- `build`：编译 / 主题级校验，涉及 `src/` 或依赖改动后**必须**运行。
- 两者都为 pass 才算一次完成的改动闭环。

---

## 6. 工作流程（Recommended Agent Loop）

1. 读 `README.md` / `AGENTS.md` / `DESIGN.md` / `CHANGELOG.md`（按需）。
2. 制定 Plan + Todo。
3. 按 Todo 逐项实现，阶段性 Feedback。
4. 运行 `test:links` 与 `build` 校验。
5. 更新 `CHANGELOG.md`（若适用）与相关文档。
6. 提交 Git（信息含 type & scope）。

---

## 7. 提交（Commit）与推送（Push）规范

> **核心约定：绝不自动 commit / push，必须由维护者明确指示后才执行。**
> 维护者说「提交/commit」才 commit；说「推送/push」才 push。二者相互独立，互不默认连带。

- 完成某项工作后：**只保留工作区改动（不提交、不推送）**，向维护者反馈，等待明确指示。
- 只有在维护者明确要求时，才执行 `git add` + `git commit`（以及仅在明确要求时 `git push`）。
- 提交信息遵循 `<type>(<scope>): <subject>`，如 `docs(core): add performance tutorial`、`feat(theme): gold navbar`。
- type 常用：`feat` / `fix` / `docs` / `style` / `refactor` / `chore`。
- 提交前确认 `.gitignore` 生效、无构建产物入仓。

---

## 8. 版本与发布（Version & Release）规约

> **版本定位**：当前版本 **`1.0.0.dev`**。版本号约定 **`x.y.z`**（见 `package.json`）。

### 8.1 变动类型 → 发布动作

| 变动类型 | 版本变化 | 动作 |
| --- | --- | --- |
| **patch（z）** | `1.0.0 -> 1.0.1` | **只打 tag + 推送代码**（不发布 release） |
| **minor（x.y）** | `1.0 -> 1.1` | **打 tag + 推送 release + 总结 release notes + 发布**（发布流程**暂未定义**） |
| **major（x.y）** | `1.0 -> 2.0` | 同 minor：tag + release notes + 发布（待定义） |

### 8.2 发布命令

发布统一用 `scripts/release.mjs`（预览模式，不自动执行 git 命令）：

```bash
pnpm release patch     # z 变动：算出 v1.0.1，打印 patch 流程（打 tag + 推代码）
pnpm release minor     # x.y 变动：算出 v1.1.0，打印 release notes 草稿 + 发布(待定义) 提示
pnpm release major
```

- 脚本**只打印**待执行的 `git tag / git push` 命令与 release notes 草稿，**不自动执行**；由维护者确认后手动或加 `--push` 执行。
- `--no-tag`：仅预览，不写回 `package.json` 版本号。

### 8.3 约定补充

- **patch（z）**：只打 tag 并推送代码，不生成 release、不总结 notes。
- **minor / major（x.y）**：tag + 推送 release + 总结 release notes；其中「发布（publish）」动作**暂未定义**，留待后续确定渠道后补全。
- tag 命名：`v<x.y.z>`（如 `v1.1.0`）。
- release notes 草稿由脚本输出，维护者补充「变更要点」后发布。
- 版本号唯一来源 `package.json`；发布时同步更新。

---

## 9. 阻塞与上报

- 若某命令被沙箱拒绝 / 依赖缺失 / 构建报错，先按错误信息尝试修复；无法修复时如实上报**具体错误信息**，不臆测原因、不静默跳过。
- 沙箱策略变化（如 approval 策略）会影响命令执行，agent 应依据当前运行时上下文的策略行事。

---

*本文件是活文档，可随项目演进补充；修改需同步更新 README（若涉及结构）并在 CHANGELOG 记录。*
