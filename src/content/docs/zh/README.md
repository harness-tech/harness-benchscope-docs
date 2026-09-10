---
title: "文档"
description: "BenchScope 文档中心：按「快速开始 → 测试 → 平台 → 参考 → 社区」五个分组组织，覆盖性能压测与精度评测的使用与参考内容。"
---

# 文档

欢迎使用 **BenchScope** —— 一个用于模型（及 OpenAI 兼容推理服务）**性能压测**与**精度评测**的开源平台。本手册按「**快速开始 → 测试 → 平台 → 参考 → 社区**」五个分组组织，覆盖从初次使用到深入调优的全部内容，便于快速定位。

## 快速开始

- [快速开始](/zh/docs/quickstart/) — 了解 BenchScope 是什么、能做什么，从这里开始
- [安装](/zh/docs/install/) — 环境要求、启动、配置、更新与卸载

## 测试

- [性能测试](/zh/docs/performance/) — 性能测试与压测（并发 / 阈值双模式），含[性能核心指标](/zh/docs/performance/metrics/)
- [精度测试](/zh/docs/accuracy/) — 精度测试与评测（Native / Serving / Mock 三模式），含[精度核心指标](/zh/docs/accuracy/metrics/)

## 平台

- [Dashboard 概览](/zh/docs/tools/dashboard/) — 资源计数、环境信息与最新性能记录
- [数据与统计](/zh/docs/data/) — 历史测试产物、统计、备份与导入
- [会话（Sessions）](/zh/docs/tools/sessions/) — SSE 流式交互式对话
- [设置（Settings）](/zh/docs/tools/settings/) — 全局配置（Provider / 模型 / 数据集 / 引擎 / 技能 / 插件）
- [内置技能](/zh/docs/tools/skills/) — 随包分发的 3 个 Agent 技能
- [模拟调试环境](/zh/docs/tools/mock/) — 无真实服务 / GPU 时的完整联调环境
- [架构介绍](/zh/docs/tools/architecture/) — 模块划分、API 面与数据流
- [Bench 引擎](/zh/docs/tools/bench-engine/) — 引擎抽象、对比与自定义

## 参考

- [CLI](/zh/docs/cli/) — 命令行工具（serve / perf / eval）
- [API](/zh/docs/api/) — HTTP 接口全量清单
- [性能核心指标](/zh/docs/performance/metrics/) — 性能指标完整口径
- [精度核心指标](/zh/docs/accuracy/metrics/) — 精度指标完整口径

## 社区

- [发布](/zh/docs/releases/) — 版本更新记录
- [帮助](/zh/docs/help/) — 常见问题排障与贡献

<div class="tip">

**tip**：

本站所有页面均遵循「简洁 + FAQ + 相关文档」的组织方式；指标类问题优先查阅[性能核心指标](/zh/docs/performance/metrics/)与[精度核心指标](/zh/docs/accuracy/metrics/)两个口径页。

</div>

## 常用入口

想快速上手？从下面几个页面开始。

- [快速开始](/zh/docs/quickstart/) — 第一次使用从这里开始
- [性能测试](/zh/docs/performance/) — 并发压测与阈值探测
- [精度测试](/zh/docs/accuracy/) — 精度评测与判分

## 需要帮助？

遇到问题时，请先查阅 [帮助 → 常见问题与排障](/zh/docs/help/)，或在 [GitHub Issues](https://github.com/LABELNET/benchscope/issues) 提交反馈。