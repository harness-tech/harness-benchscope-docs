---
title: "Bench 引擎"
---

# Bench 引擎

引擎抽象（Bench Engine）统一了不同压测后端的接入方式，支持**自研引擎、vLLM / SGLang 上游引擎**及**自定义引擎**，全部遵循同一套契约。

## 引擎类型

| 引擎 | 说明 |
| --- | --- |
| `benchscope`（自研） | 内置自研引擎，流式时间线采集，指标口径对齐 vLLM |
| `vllm-<ver>` | vLLM 官方 bench 引擎（如 `vllm-0.23`） |
| `sglang-<ver>` | SGLang 官方 bench 引擎（如 `sglang-0.5.10`） |
| 自定义引擎 | 通过技能 / 插件注册的自定义引擎（`bs-engine-create`） |

自研的 `benchscope` 引擎是 `benchscope perf` 的默认引擎——**无需本地框架环境**，可直接压测**远程 OpenAI 兼容服务**。

## 组成

每个引擎都由以下三部分组成，平台据此统一接入、无需特判：

### 环境校验

- 启动前**校验引擎依赖与运行环境**；
- 原生引擎（vllm / sglang）强制校验 torch 与框架版本，不满足则阻断。

### 参数描述

- 每个引擎声明其参数（**集群 / 生成 / 请求参数**）；
- 参数可在 Settings → Bench Engines 中**下拉选择并查看描述**。

### 指标可得性

- 可得 → 值（蓝）；不可得 → N/A（灰黑）；缺失 → 灰横线；
- **固定 11 指标快照契约**，保证跨引擎结构一致。

## 指标口径

自研引擎的吞吐 / TTFT / TPOT / ITL 指标口径与 **vLLM 对齐**，保证跨引擎可比——用自研引擎测出的结果与 vLLM bench 测出的结果含义一致：

| 指标 | 口径 |
| --- | --- |
| 吞吐（output_mean / total_mean） | 输出 / 总吞吐（tok/s） |
| TTFT（ttft_mean） | 首 token 延迟（ms） |
| TPOT（tpot_mean） | 每输出 token 延迟（ms） |
| ITL（itl_mean） | 令牌间隔延迟（ms） |

## 自定义引擎（进阶）

通过 **`bs-engine-create`** 技能创建自定义引擎，需遵循实现契约，由四部分组成：

- **Input** — 引擎如何接收任务的参数；
- **Core** — 压测负载在何处执行；
- **Output** — 指标 / 进度如何输出；
- **Mock** — 用于流水线集成测试的 Mock 实现。

通过**导入校验**后即可在 Settings → Bench Engines 启用。每个引擎（含自定义引擎）都有 **Mock 开关**用于集成测试。

<div class="tip">

**tip**：

如需接入尚未官方支持的压测后端（例如自研推理框架、网关代理等），自定义引擎是最灵活的路径。请先参考技能模板与[参与贡献](/zh/docs/help/contributing/)了解实现约定。

</div>

## 常见问题

**问题：为什么选择引擎后无法进入下一步？**

原生引擎会做环境校验，若本机未安装匹配的 torch / 框架版本则被阻断。改用自研 `benchscope` 引擎即可在本机直接测远程 API。

**问题：第三方引擎某些指标显示 N/A？**

该引擎不支持对应指标，指标可得性已显式化（N/A / 灰横线）。如需完整指标请用自研引擎。

## 相关文档

- [设置（Settings）→ Bench Engines](/zh/docs/tools/settings/) — 在界面中配置引擎
- [架构介绍](/zh/docs/tools/architecture/) — 模块划分
- [v1.0.7 更新日志](/zh/docs/releases/v1-0-7/) — 引擎改造背景
