---
title: "Dashboard 概览"
description: "Dashboard 页面：统计概览（性能 / 精度 / 会话 / 内置技能 / 模型 / 数据集 / Provider 计数）、环境信息（硬件 / 操作系统 / 网络 / 框架版本）与最新性能记录。"
---

# Dashboard 概览

Dashboard 是 BenchScope 的**首页**（路由 `/dashboard`，`/` 默认重定向至此），集中展示平台运行状态：资源计数、环境信息与最新性能记录。启动 `benchscope` 后打开的即是该页面。

![BenchScope Dashboard 总览](/images/benchscope-dashboard.png)

## 统计概览（Overview）

第一行左侧卡片，展示平台各模块的资源计数：

| 计数项 | 含义 |
| --- | --- |
| Performance | 已完成的性能压测运行数。 |
| Accuracy | 已完成的精度评测运行数。 |
| Sessions | 当前会话数。 |
| Skills (built-in) | 内置技能数（当前 3 个，见[内置技能](/zh/docs/tools/skills/)）。 |
| Models | 模型下载记录数（暂未实现，默认 0）。 |
| Datasets | 数据集下载记录数（暂未实现，默认 0）。 |

卡片底部为 **Providers 整行**：Provider 数量 + Provider 模型数（各 Provider 探测到的模型总数）。

## 环境信息（Envs info）

第一行右侧卡片，按四个维度展示运行环境：

| 维度 | 字段 |
| --- | --- |
| 硬件环境 | 主机名（Host）、CPU、内存（Memory）、GPU。 |
| 操作系统 | 系统名（OS）、系统版本（OS Version）、内核（Kernel）。 |
| 网络环境 | 按网口列出：MAC 地址（IPv4）、IP 地址、子网（Subnet）、掩码（Mask）。 |
| 框架版本 | Python、PyTorch、vLLM、SGLang、benchscope 的版本号（未安装的显示 —）。 |

<div class="info">

**info**：

环境信息在**对比不同机器上的压测结果**时尤其有用——硬件 / 框架版本不一致会导致吞吐与延迟不可直接比较。

</div>

## 性能测试记录（Perf Test Records）

第二行卡片，展示**最新 8 条**性能压测记录（不分页）：

| 列 | 含义 |
| --- | --- |
| Run ID | 运行编号。 |
| Model | 被测模型。 |
| Framework | 推理框架（vLLM / SGLang 等）。 |
| Status | 状态（done / running / stopped / error）。 |
| Time | 开始时间。 |
| Detail | 点击跳转 **Datas → Perfs** 并选中对应记录。 |

> 精度记录面板（Eval Records）当前隐藏（敬请期待），精度评测产物请在 [Accuracy 页面](/zh/docs/accuracy/) 管理。

## 常见问题

**问题：Dashboard 的计数和 Datas 里的记录数对不上？**
Dashboard 计数统计的是**已完成运行**；Datas → Perfs 列出的是全部记录（含进行中 / 失败）。口径不同属正常现象。

**问题：为什么 Models / Datasets 计数一直是 0？**
模型 / 数据集下载计数暂未实现，默认显示 0；下载管理在 [Settings → Models / Datasets](/zh/docs/tools/settings/) 中进行。

**问题：环境信息里的 GPU 显示什么？**
展示系统检测到的 GPU 型号与数量（如 nvidia-smi 可见的卡）；无 GPU 环境显示 —。

## 相关文档

- [启动平台](/zh/docs/quickstart/platform/) — 首次启动与 Dashboard 初见
- [数据与统计（Datas）](/zh/docs/data/) — 完整历史记录管理
- [设置（Settings）](/zh/docs/tools/settings/) — Provider / 模型 / 数据集管理
- [内置技能](/zh/docs/tools/skills/) — Skills 计数来源