<p align="center">
  <img src="public/images/logo-gold.png" alt="BenchScope" width="120" height="120" />
</p>

<h1 align="center">BenchScope Docs</h1>

<p align="center">
  <b>English</b> · <a href="README-zh.md"><b>简体中文</b></a>
</p>

<p align="center">
  The official documentation for <b>BenchScope</b> — an open-source, visual testing platform for <b>LLM performance and accuracy</b>.
</p>

---

## What is BenchScope?

**BenchScope** is an open-source platform for testing large language models and OpenAI-compatible inference services. It brings **performance benchmarking** and **accuracy evaluation** into a visual, web-based interface.

This repository (**BenchScope Docs**) hosts the official documentation site — a fast, static, bilingual (`/en` ↔ `/zh`) documentation site.

## Key Capabilities

- **Performance testing** — Concurrency Mode and Threshold Mode for load testing deployed inference services, with real-time throughput, latency, and progress visualization.
- **Accuracy evaluation** — Native (offline weights) and Serving (deployed service) modes, built-in datasets and scorers, with baseline comparison.
- **Data analysis** — record, aggregate, back up, and import historical run artifacts.
- **Interactive sessions** — SSE streaming chat with sampling-parameter control.
- **CLI & API** — full command-line tooling and OpenAI-compatible HTTP interfaces.

## Quick Start

BenchScope itself is installed from PyPI:

```bash
pip install benchscope
```

Explore the docs:

- [📖 Read the documentation](https://benchscope.harness-tech.com/en/docs/)

## Documentation Topics

- **Quick Start** — requirements, install, and launch
- **Performance** — concurrency & threshold benchmarking
- **Accuracy** — native & serving evaluation
- **Data** — records, statistics, backup & import
- **Advanced Tools** — sessions, settings, architecture, engines
- **CLI & API** — command line and HTTP interfaces
- **Releases & Help** — version notes and support

## Skills

本项目内置维护技能，用于自动化官网与文档站更新：

### harness-bs-docs-updater

从 BenchScope 源码分析版本变更，自动维护官网（落地页）与文档站。

**使用方式**：在 AI Agent 交互中说：
- "BenchScope 发布了 vX.Y.Z，帮我更新文档站"
- "根据源码路径 /path/to/benchscope 更新官网"
- "Sync benchscope latest version to docs"

**功能**：源码功能分析 → 旧文档归档 → 官网更新 → 文档更新 → 截图 → 构建验证 → 发布

详细说明见 [`skills/harness-bs-docs-updater/README.md`](skills/harness-bs-docs-updater/README.md)

## Project Information

- **Source code**: [LABELNET/benchscope](https://github.com/LABELNET/benchscope)
- **PyPI**: [benchscope](https://pypi.org/project/benchscope)
- **License**: [Apache License 2.0](./LICENSE)
- **Copyright**: © HarnessAI (https://www.harness-tech.com)
