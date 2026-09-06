---
title: "概述"
---

# 概述

精度测试模块对模型的输出做**量化评估**，支持**原生（Native）**与**服务（Serving）**双模式，内置多种评测数据集与判分器，并提供 Token 预估与开源基线对标能力。它回答「模型在给定任务上答得多准」。

![BenchScope 精度测试默认界面](/images/benchscope-accuracy_default.png)

<div class="tip">

**tip**：

精度测试专注于「模型输出是否正确」，与[性能测试](/zh/docs/performance/)互补：性能回答「跑得多快」，精度回答「答得多准」。

</div>

## 本页内容

- [评测模式（Modes）](/zh/docs/accuracy/modes/) — 原生 / 服务 / Mock 模式与 Token 预估
- [评测数据集（Datasets）](/zh/docs/accuracy/datasets/) — 内置数据集清单与选取
- [判分器与指标（Scoring）](/zh/docs/accuracy/scoring/) — 判分器、指标与基线对标
- [精度评测](/zh/docs/accuracy/guide/) — 分步操作

## 模式总览

| 模式 | 说明 | 依赖 |
| --- | --- | --- |
| 原生 Native | 直接加载本地模型权重（transformers / HF id）离线评测 | 可选依赖 `accuracy-native` |
| 服务 Serving | 通过 OpenAI 兼容链路评测已部署服务 | 无 |
| Mock（联调） | 无真实服务，验证链路正确性 | 无 |

<div class="info">

**info**：

如何选择模式？想离线评测本地权重（无需起服务）选 **Native**；想评测线上真实服务表现（含服务栈）选 **Serving**；想先打通链路用 **Mock**。

</div>

## 常见问题

**问题：Native 模式和 Serving 模式如何选择？**
离线评测本地权重（不开服务）用 Native；评测线上真实部署链路（含服务栈）用 Serving；只想验证链路用 Mock。

**问题：Native 模式启动被阻断？**
未检测到 torch / transformers / peft。执行 `pip install benchscope[accuracy-native]` 后重试。

**问题：评测结果中的 conclusion 是什么？**
`conclusion` 是对比基线的结论（合格 / 精度下跌 / 持平 / 优于基线等），由 `diff_pp`、`grade` 等共同判定。

**问题：如何定位个别错误样本？**
打开 `samples.jsonl`，按样本逐条查看输入、输出与判分结果，实现样本级溯源。

## 相关文档

- [eval 命令](/zh/docs/cli/eval/) — `eval` 命令完整参数
- [精度评测](/zh/docs/accuracy/guide/) — 分步操作
- [数据与统计（Datas）](/zh/docs/data/) — 结果查看与导入
- [设置（Settings）](/zh/docs/tools/settings/) — 配置 Provider、Datasets
