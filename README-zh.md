<p align="center">
  <img src="public/images/logo-gold.png" alt="BenchScope" width="120" height="120" />
</p>

<h1 align="center">BenchScope Docs · 简体中文</h1>

<p align="center">
  <a href="README.md"><b>English</b></a> · <b>简体中文</b>
</p>

<p align="center">
  <b>BenchScope</b> —— 面向 <b>LLM 性能与精度</b> 的可视化测试平台的官方文档。
</p>

---

## BenchScope 是什么？

**BenchScope** 是一个用于测试大语言模型及 OpenAI 兼容推理服务的开源平台，将**性能压测**与**精度评测**带入可视化 Web 界面。

本仓库（**BenchScope Docs**）承载其官方文档站点 —— 一个快速、静态、中英双语（`/zh` ↔ `/en`）的文档站。

## 核心能力

- **性能测试** —— 并发压测与阈值探测双模式，对已部署的推理服务进行压测，实时可视化吞吐、延迟与进度。
- **精度评测** —— 原生（本地权重）与服务（已部署服务）两种模式，内置数据集与判分器，支持基线对标。
- **数据分析** —— 记录、汇总、备份与导入历史测试产物。
- **交互式会话** —— SSE 流式对话，支持采样参数控制。
- **CLI 与 API** —— 完整的命令行工具与 OpenAI 兼容 HTTP 接口。

## 快速开始

BenchScope 本体通过 PyPI 安装：

```bash
pip install benchscope
```

阅读文档：

- [📖 阅读文档](https://benchscope.harness-tech.com/zh/docs/)

## 文档主题

- **快速开始** —— 环境要求、安装与启动
- **性能测试** —— 并发与阈值压测
- **精度测试** —— 原生与服务评测
- **数据分析** —— 记录、统计、备份与导入
- **高级工具** —— 会话、设置、架构与引擎
- **CLI 与 API** —— 命令行与 HTTP 接口
- **发布与帮助** —— 版本说明与支持

## 维护技能

本项目内置维护技能，用于自动化官网与文档站更新。

### harness-bs-docs-updater

从 BenchScope 源码分析版本变更，自动维护官网（落地页）与文档站。

**安装技能** —— 对 AI Agent 说：

> 从本项目的 `skills/harness-bs-docs-updater/` 目录安装 harness-bs-docs-updater 技能。

**使用技能** —— 对 AI Agent 说：

> - "BenchScope 发布了 vX.Y.Z，帮我更新文档站"
> - "根据源码路径 /path/to/benchscope 更新官网"
> - "同步 benchscope 最新版本到 docs"

**工作流程**：源码分析 → 旧文档归档 → 官网更新 → 文档更新 → 截图 → 构建验证 → 发布

详细说明见 [`skills/harness-bs-docs-updater/README.md`](skills/harness-bs-docs-updater/README.md)

## 项目信息

- **源码仓库**：[LABELNET/benchscope](https://github.com/LABELNET/benchscope)
- **PyPI**：[benchscope](https://pypi.org/project/benchscope)
- **开源协议**：[Apache License 2.0](./LICENSE)
- **版权**：© 模力有方（https://www.harness-tech.com）
