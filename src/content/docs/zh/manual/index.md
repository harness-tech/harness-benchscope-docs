---
title: 使用手册
description: BenchScope 使用手册总览：按 Web 导航分组，覆盖仪表盘、性能测试、精度测试、会话、数据管理与设置六大模块的完整操作手册。
---

# 使用手册

本手册**按 BenchScope Web 导航的六个模块分组**，将每个功能拆分为独立文档，逐步讲解「**输入参数、字段限制、按钮操作、页面结构、执行步骤、后台执行逻辑**」，帮助你从零完成一次完整的性能压测与精度评测。

<div class="tip">
**阅读方式**：每个模块（第 1–6 章）先阅读「概览」了解页面结构与功能定位，再按编号顺序逐篇操作。所有文档均含**编号目录**，右侧 TOC 可快速定位章节。
</div>

## 目录

### 1. Dashboard 手册（仪表盘）
1.1 [Dashboard 手册概览](/zh/docs/manual/dashboard/) — 页面结构、统计卡片、环境信息、测试记录
1.2 [统计概览与环境信息](/zh/docs/manual/dashboard/overview/) — 六大统计指标、硬件/网络/框架环境探测逻辑
1.3 [测试记录](/zh/docs/manual/dashboard/records/) — 最新 8 条记录、模型搜索、请求详情与下载

### 2. Performance 手册（性能测试）
2.1 [Performance 手册概览](/zh/docs/manual/performance/) — 页面结构、任务列表、任务状态机
2.2 [创建压测任务](/zh/docs/manual/performance/create-task/) — 三步向导：性能条件 → 性能参数 → 启动测试
2.3 [并发模式与阈值模式](/zh/docs/manual/performance/modes/) — 两种模式的参数、限制与扫描逻辑
2.4 [实时监控与曲线](/zh/docs/manual/performance/live-metrics/) — Profile Progress、Real-Time Metrics、12 条实时曲线
2.5 [结果查看与导出](/zh/docs/manual/performance/results/) — 统计图、默认 13 列表格、Excel 导出

### 3. Accuracy 手册（精度测试）
3.1 [Accuracy 手册概览](/zh/docs/manual/accuracy/) — 页面结构、任务列表、评测状态机
3.2 [创建评测任务](/zh/docs/manual/accuracy/create-task/) — 三步向导：选择数据集 → 模式与模型 → 预览与启动
3.3 [数据集与模式](/zh/docs/manual/accuracy/datasets-modes/) — 9 个内置数据集、Serving/Native 双模式、判分器
3.4 [结果查看与溯源](/zh/docs/manual/accuracy/results/) — 核心指标、基线对标、分学科准确率、单样本溯源

### 4. Sessions 手册（会话）
4.1 [Sessions 手册概览](/zh/docs/manual/sessions/) — 页面结构、工作区、对话列表
4.2 [创建会话](/zh/docs/manual/sessions/create-session/) — 选择 Provider、模型、质量等级、思考开关
4.3 [流式对话](/zh/docs/manual/sessions/chat/) — SSE 流式输出、Token 统计、生成文件

### 5. Datas 手册（数据管理）
5.1 [Datas 手册概览](/zh/docs/manual/datas/) — 页面结构、Perfs/Analysis 标签页（Evals 已隐藏）
5.2 [性能记录管理](/zh/docs/manual/datas/perfs/) — 任务记录、详情面板、运行目录、日志文件
5.3 [数据分析](/zh/docs/manual/datas/analysis/) — 记录对比分析、联动、均值/中位数
5.4 [导入导出与备份](/zh/docs/manual/datas/import-export/) — 备份 zip、导入恢复、分享 PNG

### 6. Settings 手册（设置）
6.1 [Settings 手册概览](/zh/docs/manual/settings/) — 页面结构、七大面板
6.2 [通用设置](/zh/docs/manual/settings/general/) — 主题、语言、目录、推理服务 API、数据目录变更
6.3 [Provider 管理](/zh/docs/manual/settings/providers/) — 添加/管理 Provider、模型、测试连接
6.4 [模型与数据集管理](/zh/docs/manual/settings/models-datasets/) — 模型目录、厂商目录、内置数据集缓存
6.5 [引擎管理](/zh/docs/manual/settings/engines/) — 引擎类型、环境校验、Mock 开关、上传引擎
6.6 [技能与插件](/zh/docs/manual/settings/skills-plugins/) — 内置技能、下载、提示词复制、插件系统

## 与现有文档的关系

<div class="info">
**使用手册 vs 参考文档**：本手册是**操作导向**的逐步指南（「怎么点、怎么填、后台怎么跑」），而 [性能测试](/zh/docs/performance/)、[精度测试](/zh/docs/accuracy/)、[CLI](/zh/docs/cli/)、[API](/zh/docs/api/) 等参考文档是**概念导向**的说明（「是什么、有哪些指标」）。建议先用本手册跑通一次完整流程，再查阅参考文档深入理解指标与参数。
</div>

## 前置条件

<div class="warning">
**开始前请确认**：
1. 已通过 [`benchscope serve`](/zh/docs/cli/serve/) 启动 WebUI（默认 `http://localhost:8080`）。
2. 已在 [Provider 管理](/zh/docs/manual/settings/providers/) 中至少配置一个可用的推理服务（或启用 Mock 引擎）。
3. 已阅读 [快速开始](/zh/docs/quickstart/) 与 [安装指南](/zh/docs/install/)。
</div>

## 相关文档

- [快速开始](/zh/docs/quickstart/) — 从零启动 BenchScope
- [性能测试](/zh/docs/performance/) — 性能测试概念与指标
- [精度测试](/zh/docs/accuracy/) — 精度测试概念与指标
- [CLI 参考](/zh/docs/cli/) — 命令行完整参数
- [API 参考](/zh/docs/api/) — REST API 完整路由
- [发布说明](/zh/docs/releases/) — 版本变更记录