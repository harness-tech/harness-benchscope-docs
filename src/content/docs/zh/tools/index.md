---
title: "概述"
---

# 概述

工具区收录 BenchScope 的**进阶使用与平台级能力**：会话式交互、全局设置，以及面向开发者的架构与引擎抽象。它由四个子页组成，覆盖从「在浏览器里与模型对话」到「扩展平台本身」的完整链路。

## 子页面导览

- **[会话（Sessions）](/zh/docs/tools/sessions/)** — 基于 SSE 流式的交互式对话：配置 `temperature` / `top_p` 等采样参数、发送消息并实时查看流式输出，支持 Markdown 渲染 + 代码高亮、思考（reasoning）解析与性能栏。
- **[设置（Settings）](/zh/docs/tools/settings/)** — 七个面板集中管理全局配置：General / Providers / Models / Datasets / Bench Engines / Skills / Plugins；所有修改自动持久化到 `settings.json`。
- **[架构介绍](/zh/docs/tools/architecture/)** — 后端 Python（FastAPI）+ 前端 Vue 的单体架构：核心模块、API 面、性能与精度模块解耦设计及数据流。
- **[Bench 引擎](/zh/docs/tools/bench-engine/)** — 引擎抽象与自定义：自研 `benchscope` / vLLM / SGLang / 自定义引擎的统一接入契约（环境校验 / 参数描述 / 指标可得性）。

## 我应该从哪里开始

| 你的目标 | 前往 |
| --- | --- |
| 在浏览器里与模型**交互式对话** | [会话（Sessions）](/zh/docs/tools/sessions/) |
| 配置推理服务、模型清单、数据集与引擎 | [设置（Settings）](/zh/docs/tools/settings/) |
| 理解 BenchScope 内部如何运转 | [架构](/zh/docs/tools/architecture/) |
| 接入新的压测后端 / 自研引擎 | [Bench 引擎](/zh/docs/tools/bench-engine/) |
| 把模型跑起来做一次压测或评测 | [快速开始](/zh/docs/quickstart/) 与 [CLI](/zh/docs/cli/) |

<div class="tip">

**tip**：

工具区聚焦**平台内的交互与全局配置**，以及**二次开发**。如果你只是想把模型跑起来做一次压测或评测，从 [快速开始](/zh/docs/quickstart/) 与 [CLI](/zh/docs/cli/) 开始即可。

</div>

## 常见问题

**问题：工具区和命令行 / API 是什么关系？**

工具区是 Web 界面中的交互、配置与平台能力；[CLI](/zh/docs/cli/) 与 [API](/zh/docs/api/) 提供等价或脚本化的入口，产物与数据完全一致。

**问题：改了 Settings 需要重启吗？**

数据根目录（Root Dir）**即时生效**、无需重启；其余修改自动持久化到 `~/.benchscope/settings.json`，见 [配置说明](/zh/docs/install/configuration/)。

**问题：会话和压测 / 评测有什么区别？**

会话（Sessions）是**交互式对话**，用于快速验证回答质量；压测 / 评测是**批量施压 / 批量评测**，用于得到可复现的指标。两者在 [CLI](/zh/docs/cli/) 中也使用一致的采样参数。

## 相关文档

- [CLI](/zh/docs/cli/) — 命令行等价能力
- [API](/zh/docs/api/) — HTTP 接口
- [配置说明](/zh/docs/install/configuration/) — 数据目录与 settings.json
- [参与贡献](/zh/docs/help/contributing/) — 本地开发与提交 PR
