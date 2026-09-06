---
title: "环境要求"
description: "运行 BenchScope 所需的 Python 版本、被测试推理服务、网络 / 浏览器以及可选的 GPU 条件。"
---

# 环境要求

本页介绍运行 BenchScope 所需的环境前提条件。确认满足条件后，即可按[快速安装](/zh/docs/quickstart/)安装并启动平台。

## Python 与 pip

- **Python**：推荐 3.10 及以上版本（同时支持 3.9 / 3.11 / 3.12），纯 Python 实现。
- **pip**：建议使用较新的 pip 以正确解析依赖（`pip install --upgrade pip`）。

## 被测试推理服务

BenchScope 本身不托管模型，你需要一个待测试的推理服务：

- 本地 **vLLM / SGLang** 服务（例如 `http://127.0.0.1:8000`），或
- 任意 **OpenAI 兼容**的远程端点（Base URL + API Key）。

<div class="info">

**info**：

BenchScope 的 Web 前端完全内嵌在 Python 包中，安装后无需额外安装 Node.js 或前端依赖，一条命令即可启动完整平台。

</div>

## 网络与浏览器

- **网络**：安装时需访问 PyPI；压测时需能访问被测试推理服务。
- **浏览器**：Chrome / Edge / Firefox 等现代浏览器（推荐 Chrome）。

## GPU（可选）

仅当计划使用**原生精度评测（Native）**（本地加载权重离线评测）时才需要 GPU；BenchScope 本身**不需要**本地 GPU。

<div class="tip">

**tip**：

如需使用**原生精度评测**能力，请一并安装可选依赖：`pip install benchscope[accuracy-native]`。

</div>

## 常见问题

**问题：没有 GPU 能运行 BenchScope 吗？**
可以。BenchScope 只发起请求并收集结果，GPU 仅由被测试的推理服务使用，或用于原生精度评测。

**问题：需要自行安装 vLLM / SGLang 吗？**
不需要。被测试的推理服务由你自行部署（本地或远程均可），BenchScope 只负责压测与评测。

**问题：需要安装 Node.js 或前端依赖吗？**
不需要。Web 前端完全内嵌在 Python 包中。

## 相关文档

- [快速开始](/zh/docs/quickstart/) — 功能总览与安装
- [启动平台](/zh/docs/quickstart/platform/) — 一条命令启动 Web 平台
- [安装](/zh/docs/install/) — 安装与启动细节
- [配置说明](/zh/docs/install/configuration/) — 数据根目录与 settings.json
