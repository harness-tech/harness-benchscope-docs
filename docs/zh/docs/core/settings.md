# 设置（Settings）

Settings 页集中管理平台全局配置，共**七个面板**：General / Providers / Models / Datasets / Bench Engines / Skills / Plugins（1.0.7 起面板化，并新增每引擎 Mock 开关）。

![BenchScope Settings 默认界面](/images/benchscope-settings_default.png)

::: tip
Settings 中的所有修改都会**自动持久化**到 `~/.benchscope/settings.json`，无需手工编辑配置文件。见 [配置说明](../get-started/configuration.md)。
:::

## General（通用）

- **数据根目录与 Cache Paths**：Root Dir **即时生效（无需重启）**，各子目录默认只读展示。
- **运行参数**等全局配置项。

| 配置 | 说明 |
| --- | --- |
| Root Dir | 数据根目录，修改即时生效 |
| perfs / evals / logs / ... | 各子目录映射（只读展示） |

## Providers（服务提供方）

- 配置 OpenAI 兼容 / vLLM / SGLang 等推理服务提供方的 **Base URL** 与 **API Key**。
- 服务**可用状态**在顶栏与 Dashboard 展示。
- 精度 Serving 模式**缺省使用全局 Provider 配置**（无需每次重复填写地址）。

```json
{
  "name": "my-vllm",
  "type": "vllm",
  "base_url": "http://127.0.0.1:8000",
  "api_key": ""
}
```

## Models（模型）

- 维护**内置模型清单**；
- Provider 模型以**绿色标签**展示，便于区分「内置清单」与「Provider 动态模型」。

## Datasets（数据集）

- **内置数据集**管理与下载目录（`datasets_dir`）；
- 数据集由 `datasets.yaml` 定义，可通过 modelscope 或 url 源下载，并缓存到 `~/.benchscope/datasets/{id}/`。

## Bench Engines（引擎）

- **引擎注册与配置**；卡片按**来源标色**，每引擎可开 **Mock 开关**。
- 内置自研引擎 **`benchscope`**，另支持 vLLM / SGLang 上游引擎及自定义引擎。

| 引擎 | 说明 |
| --- | --- |
| `benchscope`（自研） | 内置自研引擎，无需本地框架环境 |
| `vllm-<版本>` | vLLM 官方 bench 引擎 |
| `sglang-<版本>` | SGLang 官方 bench 引擎 |
| 自定义引擎 | 通过技能 / 插件注册 |

::: info
引擎的完整设计见 [Bench 引擎](../development/bench-engine.md)。环境校验约定：原生引擎（vllm / sglang）必须校验 torch 与对应框架版本，不满足则禁止进入下一步。
:::

## Skills / Plugins（技能与插件）

- **技能包**与**插件**的安装、加载目录（`plugins_dir`）；
- 例如通过 `bs-engine-create` 技能创建自定义引擎。

## 相关文档

- [配置说明](../get-started/configuration.md) — 数据目录与 settings.json
- [性能测试](./performance.md) — 使用 Bench Engines 压测
- [Bench 引擎](../development/bench-engine.md) — 引擎架构与自定义
