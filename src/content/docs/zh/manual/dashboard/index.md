---
title: "Dashboard 手册概览"
description: "BenchScope Dashboard（仪表盘）手册概览：只读总览页的页面结构、统计概览卡片、环境信息面板、测试记录（最新 8 条）与手册章节索引。"
---

# Dashboard 手册概览

Dashboard 是 BenchScope WebUI 的**首页**（导航名「仪表盘」，i18n 键 `dashboard`，路由 `/dashboard`，`/` 重定向至此）。它是**只读展示页**：汇总平台资源统计、运行环境与最新性能测试记录，不提供发起测试或修改配置的入口。

## 1. 功能说明

Dashboard 由三个板块组成：

| 板块 | i18n 键 | 卡片标题显示 | 内容 | 手册章节 |
| --- | --- | --- | --- | --- |
| 统计概览 | `overview` | 统计概览 | 六大统计指标（性能 / 精度 / 会话 / 技能 / 模型 / 数据集）+ Provider 数量与 Provider 模型 | [统计概览与环境信息](/zh/docs/manual/dashboard/overview/) |
| 环境信息 | `envInfo` | Envs info | 硬件环境、操作系统、网络环境、框架版本 | [统计概览与环境信息](/zh/docs/manual/dashboard/overview/) |
| 测试记录 | `perfTestRecords` | Perf Records | 最新 8 条性能测试记录、「详情」跳转 | [测试记录](/zh/docs/manual/dashboard/records/) |

<div class="tip">

**tip**：

Dashboard 是**只读**页面，可交互控件仅有测试记录面板的「刷新」「更多」「详情」按钮。发起性能 / 精度测试、配置 Provider 等操作请在对应功能页完成。

</div>

## 2. 页面结构

```
┌──────────────────────────────────────────────────────────────────┐
│ 统计概览（overview）                  │ 环境信息（envInfo）            │
│ 性能 │ 精度                         │ 硬件环境：主机/CPU/内存/GPU │
│ 会话 │ 技能（内置）                  │ 操作系统：OS/版本/内核      │
│ 模型 │ 数据集                        │ 网络环境：每网口 MAC/IP/子网/掩码 │
│ Provider 数量 │ Provider 模型        │ 框架版本：Python/Pytorch/vLLM/  │
│                                  │ SGLang/benchscope           │
├──────────────────────────────────────────────────────────────────┤
│ 测试记录（perfTestRecords）              [刷新] [更多]              │
│ Run ID │ Model │ Framework │ Status │ Time │ 详情               │
│ （最多 8 行，不分页，无搜索框）                              │
│                                              *仅显示最新 8 条记录  │
└──────────────────────────────────────────────────────────────────┘
```

- 第一行：统计概览与环境信息两张卡片左右并排，窄屏时上下堆叠（栅格 `xs=24 / lg=12`）。
- 第二行：测试记录卡片通栏，footer 显示 `*仅显示最新 8 条记录`。

## 3. 手册章节索引

| 编号 | 章节 | 内容 |
| --- | --- | --- |
| 1 | [统计概览与环境信息](/zh/docs/manual/dashboard/overview/) | 六大统计指标、Provider 计数、硬件/网络/框架环境探测逻辑、字段限制 |
| 2 | [测试记录](/zh/docs/manual/dashboard/records/) | 最新 8 条记录、列字段限制、详情/更多/刷新操作、Perf 请求详情与下载 |

## 4. 相关文档

- [Dashboard 概览（参考文档）](/zh/docs/tools/dashboard/) — 概念导向的页面说明
- [性能记录管理（Datas 手册）](/zh/docs/manual/datas/perfs/) — 完整记录列表、详情面板、文件下载
- [设置（参考文档）](/zh/docs/tools/settings/) — Provider、模型、数据集等配置入口

<div class="info">

**info**：

统计概览与环境信息卡片在页面打开时**自动加载**，无需点击按钮；各指标的后台取数流程见 [统计概览与环境信息 · 后台执行逻辑](/zh/docs/manual/dashboard/overview/)。

</div>