---
title: "设置（Settings）"
description: "Settings 页七个面板集中管理全局配置：General / Providers / Models / Datasets / Bench Engines / Skills / Plugins，修改自动持久化到 settings.json。"
---

# 设置（Settings）

Settings 页集中管理平台全局配置，分为**七个面板**：General / Providers / Models / Datasets / Bench Engines / Skills / Plugins（1.0.7 起面板化，并新增每引擎 Mock 开关）。

![BenchScope Settings 默认界面](/images/benchscope-settings_default.png)

<div class="tip">

**tip**：

Settings 中的所有修改都会**自动持久化**到 `~/.benchscope/settings.json`，无需手工编辑配置文件。见 [配置说明](/zh/docs/install/configuration/)。

</div>

## General（通用）

- **数据根目录与 Cache Paths**：Root Dir **即时生效（无需重启）**，各子目录默认只读展示（由平台管理）。

| 配置 | 说明 |
| --- | --- |
| Root Dir | 数据根目录（默认 `~/.benchscope`），修改即时生效 |
| perfs / evals / logs / sessions / datasets / models / plugins / ... | 各子目录映射（只读展示） |

<div class="info">

**info**：

Cache Paths 视图会列出数据根目录下的每个子目录（`perfs`、`evals`、`logs`、`sessions`、`datasets`、`models`、`plugins` 等），让你清楚每种数据存于何处、新数据将写入哪里。

</div>

## Providers（服务提供方）

- 配置 OpenAI 兼容 / vLLM / SGLang 等推理服务提供方的 **Base URL** 与 **API Key**。
- 每个 Provider 卡片展示：名称、Base URL、API Key、**模型可用状态**与**探测到的模型列表**。
- 服务**可用状态**在顶栏与 Dashboard 展示。
- 精度 Serving 模式**缺省使用全局 Provider 配置**（无需每次重复填写地址）；会话请求同样代理到激活的 Provider。

一个 Provider 即一个推理服务端点，例如：

```json
{
  "id": "provider_my-vllm",
  "name": "my-vllm",
  "base_url": "http://127.0.0.1:8000",
  "api_key": ""
}
```

<div class="info">

**info**：

历史配置中缺少 `id` 的 Provider（如旧版「Default」）会在配置加载时**自动回填稳定 id**（由名称 slug 生成，冲突时追加数字后缀），无需手工补全。

</div>

<div class="tip">

**tip**：

在这里**一次性添加** vLLM / SGLang 或 OpenAI 兼容端点后，它即可作为目标用于性能测试、会话与精度（Serving 模式）。

</div>

## Models（模型）

- 维护**内置模型清单**；
- Provider 模型以**绿色标签**展示，便于区分「内置清单」与「Provider 动态模型」。

## Datasets（数据集）

- **内置数据集**管理与下载目录（`datasets_dir`）；
- 数据集由 `datasets.yaml` 定义（当前 **12 个**：9 个精度评测数据集 + 3 个性能压测数据集，见[评测数据集](/zh/docs/accuracy/datasets/)），可从 **modelscope** 或 **url 源**下载，并缓存到数据根目录的 `datasets/{id}/`（默认 `~/.benchscope/datasets/{id}/`）。

## Bench Engines（引擎）

- **引擎注册与配置**；卡片按**来源标色**（内置蓝 / 用户上传紫），每引擎可开 **Mock 开关**。
- 内置自研引擎 **`benchscope`**，另支持 vLLM / SGLang 上游引擎及自定义引擎。

| 引擎 | 说明 |
| --- | --- |
| `benchscope`（自研） | 内置自研引擎，无需本地框架环境；同时支持 Serving 链路精度评测 |
| `vllm-0.23` | vLLM 官方 bench 引擎（需 torch >= 2.0 + vllm >= 0.23, < 0.24） |
| `sglang-0.5.10` | SGLang 官方 bench 引擎（需 torch + sglang >= 0.5.10, < 0.6） |
| `native-hf` | 本地权重精度评测引擎（需 torch + transformers，可选 LoRA） |
| `mock` | Mock 精度评测引擎（可控正确率，联调用） |
| 自定义引擎 | 通过 Upload Engine / 导入注册（可用 `bs-engine-create` 技能辅助创建） |

<div class="info">

**info**：

引擎的完整设计见 [Bench 引擎](/zh/docs/tools/bench-engine/)。环境校验约定：原生引擎（vllm / sglang）必须校验 torch 与对应框架版本，不满足则禁止进入下一步。

</div>

## Skills / Plugins（技能与插件）

- **技能包**与**插件**的安装与加载目录（`plugins_dir`）；
- Skills 面板展示 **3 个内置技能**（`bs-perfs-concurrency` / `bs-perfs-threshold` / `bs-engine-create`），支持打包下载，详见[内置技能](/zh/docs/tools/skills/)；
- 例如通过 `bs-engine-create` 技能创建自定义引擎。

## 相关文档

- [配置说明](/zh/docs/install/configuration/) — 数据目录与 settings.json
- [Dashboard 概览](/zh/docs/tools/dashboard/) — 资源计数与 Provider 模型数
- [内置技能](/zh/docs/tools/skills/) — 3 个内置技能的查看与下载
- [Bench 引擎](/zh/docs/tools/bench-engine/) — 引擎架构与自定义
- [性能测试](/zh/docs/performance/) — 使用 Bench Engines 压测
- [概述](/zh/docs/accuracy/) — 数据集 / 基线在评测中的使用