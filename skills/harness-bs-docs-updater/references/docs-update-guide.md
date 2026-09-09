# 文档站更新指南

本文档指导如何更新 benchscope-docs 文档站内容。

## 目录结构

```
src/content/docs/{zh,en}/
├── README.md                  # 文档首页
├── quickstart/                # 快速开始（含 requirements、platform）
├── install/                   # 安装（含 configuration、update-uninstall）
├── accuracy/                  # 精度（含 modes、datasets、scoring、guide）
├── performance/               # 性能（含 concurrency、threshold）
├── data/                      # 数据
├── tools/                     # 工具（含 sessions、settings、architecture、bench-engine）
├── cli/                       # CLI（含 serve、perf、eval）
├── api/                       # API
├── releases/                  # 发布（含 v1-x-y 版本页）
└── help/                      # 帮助（含 contributing）
```

## 文件命名规范

- 文件名：`kebab-case`（如 `update-uninstall.md`）
- frontmatter：至少含 `title`
- h1 标题与 frontmatter `title` 一致

```markdown
---
title: "页面标题"
description: "可选的页面描述"
---

# 页面标题
```

## 双语同步规则

| 规则 | 说明 |
|---|---|
| 文件数一致 | zh 有多少文件，en 就有多少文件 |
| 结构一致 | 目录层级、子分组完全相同 |
| 链接一致 | zh 用 `/zh/docs/...`，en 用 `/en/docs/...` |
| 内容独立 | 不是逐句翻译，而是用目标语言自然表达 |

## 文档结构模板

### 分区落地页（index.md）

```markdown
---
title: "概述"
---

# 概述

1-2 段概述本分区内容。

## 本页内容

- [子页面1](/zh/docs/xxx/sub1/) — 简要说明
- [子页面2](/zh/docs/xxx/sub2/) — 简要说明

## 核心概念

表格或列表形式介绍核心概念。

## 常见问题

**问题：xxx？**
回答内容。

## 相关文档

- [相关页面1](/zh/docs/xxx/) — 简要说明
- [相关页面2](/zh/docs/xxx/) — 简要说明
```

### 功能页（非 index.md）

```markdown
---
title: "功能名称"
---

# 功能名称

1-2 段功能说明。

## 前置条件

- 条件1
- 条件2

## 操作步骤

### 步骤 1：xxx

说明 + 代码示例。

### 步骤 2：xxx

说明 + 代码示例。

## 常见问题

**问题：xxx？**
回答内容。

## 相关文档

- [相关页面](/zh/docs/xxx/) — 简要说明
```

## 排版规范

| 元素 | 规范 |
|---|---|
| 段落间距 | `margin: 0 0 0.85rem` |
| 列表项间距 | `margin: 0.25rem 0` |
| 代码块 | fenced code block，带语言标签 |
| 行内代码 | 用反引号包裹 |
| 图片 | `max-width: 66.666%`，居中显示 |
| 表格 | 13px 字号，表头加粗 |
| 提示块 | `<div class="tip/warning/info">` HTML 语法 |

## FAQ 格式统一

```markdown
## 常见问题

**问题：xxx？**
回答内容。

**问题：yyy？**
回答内容。
```

禁止使用 `**Q：**\n\nA：` 格式。

## 提示块格式

```html
<div class="tip">

**tip**：

提示内容。

</div>

<div class="warning">

**warning**：

警告内容。

</div>

<div class="info">

**info**：

信息内容。

</div>
```

## 内链格式

- ✅ `[链接文字](/zh/docs/quickstart/)` — 绝对路由
- ✅ `[链接文字](/en/docs/cli/perf/)` — 绝对路由
- ❌ `[链接文字](./quickstart.md)` — 相对链接
- ❌ `[链接文字](../install/)` — 相对链接

## 版本发布文档

新增版本时，创建 `src/content/docs/{zh,en}/releases/vX-Y-Z.md`：

```markdown
---
title: "vX.Y.Z"
---

# vX.Y.Z

## 发布信息

| 项目 | 内容 |
| --- | --- |
| 版本 | X.Y.Z |
| 状态 | 已发布（Released） |
| 发布日期 | YYYY-MM-DD |

简要说明本版本亮点。

## 特性亮点

### 功能1

说明 + 截图。

## 相关文档

- 历史版本：[vX.Y.Z-1](/zh/docs/releases/vX-Y-Z-1/)
```

## 内容长度指引

| 页面类型 | 建议行数 |
|---|---|
| 分区落地页（index.md） | 40-80 行 |
| 功能页 | 80-150 行 |
| 参考页（CLI/API） | 100-200 行 |
| 版本发布页 | 50-100 行 |

超过 150 行的功能页应考虑拆分为子页。
