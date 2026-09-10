---
title: Datas 手册概览
description: Datas（数据管理）模块手册概览：页面结构、Perfs/Analysis 子导航、Evals 标签页隐藏说明、数据目录与本章索引，是查看历史性能/精度测试记录的统一入口。
---

# Datas 手册概览

**Datas（数据管理）** 是 BenchScope 的「档案馆」：集中展示所有历史测试的落盘产物，支持查看、导入恢复、备份与分享。性能压测与精度评测完成后，记录都会在此登记，可跨会话、跨服务重启持久访问。

<div class="info">

**info**：

Datas 页面只读展示**已落盘的运行记录**（run），不管理运行中的任务。创建 / 启动 / 停止任务请在 [性能测试](/zh/docs/performance/) 与 [精度测试](/zh/docs/manual/accuracy/) 页面进行。

</div>

## 1. 页面结构

Datas 页由**副导航 + 子路由内容**两部分组成，副导航提供两个标签页：

```
┌────────────────────────────────────────────┐
│  Datas 副导航    [ Perfs ]   [ Analysis ]    │
├────────────────────────────────────────────┤
│     （子路由内容区，随标签切换）              │
└────────────────────────────────────────────┘
```

| 标签页 | 路由 | 状态 | 说明 |
| --- | --- | --- | --- |
| Perfs | `/datas/perfs` | 可用 | 性能测试记录：列表 + 详情面板（数据表 + 统计图） |
| Analysis | `/datas/analysis` | 敬请期待 | 数据分析占位页，功能规划中 |

<div class="warning">

**warning**：

早期版本曾有 **Evals（精度评测记录）** 标签页，现已**隐藏**——路由 `/datas/evals` 会重定向到 `/datas/perfs`，副导航中也不再显示。精度评测产物与结果请在 **Accuracy 页面**（[精度测试](/zh/docs/manual/accuracy/)）管理。

</div>

## 2. 路由与入口

| 路由 | 行为 |
| --- | --- |
| `/datas` | 重定向到 `/datas/perfs`（默认进入 Perfs 页） |
| `/datas/perfs` | 性能记录管理页 |
| `/datas/evals` | 重定向到 `/datas/perfs`（Evals 已隐藏） |
| `/datas/analysis` | 数据分析占位页 |
| `/datas/perfs?run_id=<id>` | 打开并自动选中指定记录（Dashboard「详情」跳转入口） |

## 3. 数据来源

所有 Datas 记录来自本地数据根目录（默认 `~/.benchscope/`）的落盘产物：

| 来源 | 目录 | 内容 |
| --- | --- | --- |
| 性能压测记录 | `perfs/<run_id>/` | `run.json` + `live/*.json` + 汇总 / 日志文件 |
| 精度评测记录 | `evals/<run_id>/` | 精度任务产物（在 Accuracy 页管理） |
| 终端输出日志 | `logs/perf_<run_id>_*.log` | 任务运行时的终端日志 |
| 数据分析 | `analysys/` | 数据分析目录（Analysis 功能规划中） |

<div class="tip">

**tip**：

数据分析目录的默认名是 **`analysys`**，这是内置默认值，请勿误写为 `analysis`。

</div>

## 4. 本章目录

- [性能记录管理](/zh/docs/manual/datas/perfs/) — 任务记录、详情面板、运行目录、日志文件
- [数据分析](/zh/docs/manual/datas/analysis/) — 记录对比分析、联动、均值 / 中位数
- [导入导出与备份](/zh/docs/manual/datas/import-export/) — 备份 zip、导入恢复、分享 PNG

## 5. 相关文档

- [Datas 概述（参考）](/zh/docs/data/) — Datas 模块概念与指标口径；[性能测试](/zh/docs/performance/) — 产生 Perfs 记录
