---
title: 引擎管理
description: Settings「Bench 引擎」面板操作手册：引擎类型、环境校验、Mock 开关、Create Engine 四步制作、Upload Engine 上传、引擎对比与后台执行逻辑。
---

# 引擎管理

「Bench 引擎」面板（菜单 key `benchesTab`）管理 BenchScope 的**内置测试引擎**：展示引擎列表（名称 / 类型 / 版本 / 环境状态 / 特点）、环境要求与校验结果、Mock 开关，并提供右上角三个操作：**Create Engine**（制作指引）、**Upload Engine**（上传引擎包）、**Engine Comparison**（引擎对比）。

## 1. 功能说明

- **内置测试引擎**：Bench CLI（自研引擎，无需本地框架环境）；vLLM / SGLang 原生引擎需校验本地安装版本；另有 Native（本地权重精度评测）与 Mock（可控伪输出）引擎。
- **环境校验**：原生 / Native 引擎逐个校验 `requires` 中的依赖（包版本 + 命令行可用性）；自研与 Mock 引擎无依赖，恒通过。
- **Mock 开关（`engineMock`）**：每个引擎一个开关，开启后该引擎使用**仿真数据与运行环境**（跳过真实框架依赖校验），卡片标记 Mock；关闭则恢复 Real。
- **Create Engine**：四步制作指引（确认目标版本 → 拉取上游源码核实参数 → 复制提示词给 AI 生成定义 → 用 Upload Engine 导入）+ 上游参考链接 + 可复制 AI 提示词。
- **Upload Engine / Engine Comparison**：上传 `.yaml` 引擎定义或 `.tar.gz` 技能包，校验通过后合并进引擎列表（1.0.7 起提供）；Engine Comparison 从 6 个维度横向对比全部引擎。

## 2. 页面结构

```
┌────────────────────────────────────────────────────────────────┐
│ Bench 引擎（benchesTab）        [Create Engine] [Upload Engine]  │
│ 内置测试引擎：Bench CLI 为自研引擎...（benchesDesc）[Engine Comparison] │
├────────────────────────────────────────────────────────────────┤
│ 引擎卡片（每个引擎一张，整页滚动）                                  │
│  Bench CLI  [默认引擎][builtin][Real][环境满足]   版本 stable      │
│  描述 + 特点（双语，按界面语言显示）                                 │
│  ────────────────────────────────────────────────────────────── │
│  环境要求（无依赖时显示：无框架环境依赖，安装即用）                    │
│  torch        要求版本 >=2.0   已安装 2.1.0   [OK]                │
│  vllm         要求版本 >=0.23,<0.24   已安装 未安装   [FAIL]       │
│  安装提示: pip install 'vllm>=0.23,<0.24'                        │
│  Mock 环境与数据  [开关]                                           │
└────────────────────────────────────────────────────────────────┘
```

| 区域 | 控件 / 标签 | 说明 |
| --- | --- | --- |
| 顶部操作栏 | Create Engine / Upload Engine / Engine Comparison（文字按钮，右上角） | 分别打开制作指引 / 上传 / 对比弹窗 |
| 卡片头部 | 名称 + 标签：默认引擎（`benchDefault`）、引擎类型（`benchKind`，`kind` 原值）、Mock / Real（`engineMockTag` / `engineRealTag`）、环境状态（环境满足 / 环境不满足）、版本（`benchVersion` v{version}） | 环境状态绿色 = 满足（`benchEnvReady`），红色 = 不满足（`benchEnvMissing`） |
| 卡片中部 | 描述 + 特点（`benchHighlights`）列表 | 按界面语言取 `*_zh` / 英文字段 |
| 卡片底部 | 环境要求表（`benchRequires`：名称 / 要求版本 / 已安装 / OK / FAIL + 安装提示）+ Mock 开关（`engineMock`） | 无依赖引擎显示 `benchNoRequires`「无框架环境依赖，安装即用」 |

## 3. 输入参数

引擎面板**无表单输入**，输入为 Mock 开关与上传文件两类：

| 参数 | 类型 | 限制 / 约束 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| Mock 开关（`engineMock`） | 布尔 | 每个引擎一个；取值 `true` / `false` | `false`（Real） | 开启后该引擎用仿真数据与运行环境 |
| 上传文件（Upload Engine） | 文件 | 扩展名仅 `.yaml` / `.yml` / `.tar.gz` / `.tgz`；**单个文件不超过 20MB**；非空 | 无 | `.yaml` / `.yml` 为引擎定义；`.tar.gz` / `.tgz` 为技能包（由 bench-engine-authoring 打包） |

**引擎类型（`kind`）枚举**：`builtin`（自研，无依赖）/ `vllm`（vLLM 原生）/ `sglang`（SGLang 原生）/ `native`（本地权重精度）/ `mock`（可控伪输出）；`vllm` 与 `sglang` 需校验框架版本 + 命令行可用，`native` 需校验 torch + transformers 版本。

**当前内置引擎**（`benchscope/configs/benchs.yaml`，共 5 个）：

| id | 名称 | kind | 版本 | 环境要求（requires） |
| --- | --- | --- | --- | --- |
| `benchscope` | Bench CLI | `builtin` | stable | 无（`requires: []`，默认引擎） |
| `vllm-0.23` | vLLM 0.23 | `vllm` | 0.23 | `torch >=2.0`；`vllm >=0.23,<0.24` |
| `sglang-0.5.10` | SGLang 0.5.10 | `sglang` | 0.5.10 | `torch >=2.0`；`sglang >=0.5.10,<0.6` |
| `native-hf` | Native HF | `native` | stable | `torch >=2.0`；`transformers >=4.40` |
| `mock` | Mock | `mock` | stable | 无（`requires: []`） |

**环境校验字段**（`env.checks[]`）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `name` | 字符串 | 依赖名称（如 `torch`、`vllm`、`sglang`、`vllm-cli`） |
| `required` | 字符串 | 要求版本（`benchRequiredVersion`，如 `>=0.23,<0.24`） |
| `installed` | 字符串 | 已安装版本（`benchInstalled`）；未安装显示 `benchNotInstalled`「未安装」 |
| `ok` | 布尔 | 单项校验是否通过（OK / FAIL 标签） |
| `hint` | 字符串 | 安装提示（`benchInstallHint`，如 `pip install 'vllm>=0.23,<0.24'`） |

## 4. 操作步骤

### 4.1 查看引擎与环境状态

1. 左侧菜单点击「Bench 引擎」。
2. 查看引擎卡片头部标签：默认引擎 / 引擎类型 / Mock / Real / 环境满足 / 环境不满足 / 版本。
3. 查看卡片底部「环境要求」表：逐项核对 要求版本 / 已安装 / OK / FAIL，FAIL 项下方显示安装提示（如 `pip install 'vllm>=0.23,<0.24'`）；按提示安装依赖后刷新页面重新校验。

### 4.2 切换 Mock 开关

1. 在目标引擎卡片底部找到「Mock 环境与数据」开关（默认关闭 = Real）。
2. 点击开关切换：开启后提示「已开启该引擎的 Mock——使用仿真数据与运行环境」，卡片标签变为 Mock、环境状态显示 环境满足（mock-environment 通过）；再次点击关闭，提示「已关闭该引擎的 Mock」，恢复真实环境校验。

<div class="warning">
**warning**：Mock 模式输出的是**仿真数据与运行环境**，结果不代表真实性能；仅用于无 GPU / 无真实推理服务场景的全链路联调与演示（见 [Mock](/zh/docs/tools/mock/)）。
</div>

### 4.3 Create Engine（制作自定义引擎）

1. 点击面板右上角 **Create Engine**，打开制作指引弹窗，阅读「制作步骤」四步：
   1. 确认目标框架与确切版本（如 vllm 0.24），不要猜测版本。
   2. 打开该版本 tag 的上游 bench 入口文件，读取真实参数（禁止跨版本复制参数）。
   3. 复制下方提示词给 AI，替换框架与版本，生成引擎定义与参数描述。
   4. 用 Upload Engine 上传生成的 `.yaml` 或技能包 `.tar.gz`，校验通过后即生效。
2. 查看「上游参考（按版本 tag 固定）」：vLLM（`https://github.com/vllm-project/vllm`，入口 `vllm/benchmarks/serve.py`，命令 `vllm bench serve`）与 SGLang（`https://github.com/sgl-project/sglang`，入口 `python/sglang/bench_serving.py`，命令 `python -m sglang.bench_serving`）；把链接中的版本替换为目标版本。
3. 复制「AI 提示词」（`<FRAMEWORK>` / `<VERSION>` 占位符自行替换）发送给 AI 生成引擎包，关闭弹窗后用 **Upload Engine** 导入。

### 4.4 Upload Engine（上传引擎包）

1. 点击面板右上角 **Upload Engine**，打开上传弹窗（提示「上传 .yaml 引擎定义或 .tar.gz 技能包，校验通过后才会写入」）。
2. 在拖拽区点击或拖入文件（前端先校验扩展名：仅 `.yaml` / `.yml` / `.tar.gz` / `.tgz`，否则提示「仅支持 .yaml / .yml / .tar.gz / .tgz 文件」；单个文件不超过 20MB）。
3. 选择后弹窗显示「待导入文件」与文件名（可点击取消清除），点击底部 **校验并导入**（未选文件时禁用）。
4. 导入完成后查看结果：新增引擎（`added`）/ 更新引擎（`updated`）/ 各项校验（`checks`，OK / FAIL 标签）；引擎列表自动刷新。

### 4.5 Engine Comparison（引擎对比）

1. 点击面板右上角 **Engine Comparison**，打开对比表弹窗。
2. 按 6 个维度横向对比全部引擎：Engine Type（引擎类型）、Environment（环境依赖）、Test Target（测试对象）、Execution（执行方式）、Metric Basis（指标口径）、Install Size（安装体积）；关闭弹窗返回引擎列表。

## 5. 后台执行逻辑

### 5.1 加载引擎列表

`GET /api/benchs` → 后端 `list_engines(with_env=True)`：解析 `benchs.yaml` 的 `engines` 段，逐引擎生成摘要（`id` / `kind` / `origin` / `framework` / `version` / `name(_zh)` / `description(_zh)` / `highlights(_zh)` / `requires` / `eval`），执行 `check_env` 附 `env: {ok, checks[]}`，再按 `engine_mocks` 映射注入 `mock` / `mock_state`（**Mock 开启时 env 被覆盖**为 `{ok: true, mock: true, checks: [mock-environment]}`）；返回 `{"engines": [...], "comparison": [...], "default_engine_id": "..."}`（`default_engine_id` 取第一个 `kind=builtin` 的引擎，当前为 `benchscope`）。前端随后调用 `GET /api/benchs/authoring` 拉取制作指引（上游链接 + AI 提示词模板）。对比表数据随 `comparison` 字段返回（来自 `benchs.yaml` 的 `comparison` 段，6 个维度 × N 个引擎，含 `*_zh` 中文值），前端按界面语言渲染。

### 5.2 环境校验（check_env）

1. 遍历引擎 `requires` 数组：`_installed_version(name)` 读取本机包版本，`_match_spec(installed, spec)` 比对版本区间（`>=2.0`、`>=0.23,<0.24` 等），生成单项 `checks`。
2. 原生引擎（`kind` 为 `vllm` / `sglang`）且依赖全部通过时，**追加 CLI 可用性检查**：`vllm-cli`（`vllm` 可执行文件）/ `sglang-cli`（`sglang` python 模块）。
3. 任一项失败 → `env.ok = false`（卡片显示「环境不满足」，失败项 `hint` 显示安装提示）；`requires: []` 的引擎恒 `ok = true`；单引擎可另经 `GET /api/benchs/{engine_id}/env-check` 单独校验（创建任务页使用），Mock 开启时同样返回 mock-environment 通过结果。

### 5.3 Mock 开关

`POST /api/benchs/{engine_id}/mock`（body `{"enabled": bool}`）：未知 `engine_id` 返回 **404**；`enabled=true` → `engine_mocks[engine_id] = true`，`enabled=false` → 移除该 key（用**整体替换** `config.set` 而非递归合并，确保删除生效）；落盘 `~/.benchscope/settings.json`（`engine_mocks` 字段），返回该引擎最新摘要（含注入后的 `mock` / `env`）。

### 5.4 上传引擎包

`POST /api/benchs/upload`（FormData `file`，前端超时 120 秒）：

1. 空文件返回 **400**；超过 **20MB** 返回 **400**（「引擎包过大（上限 20MB）」）；扩展名仅 `.yaml` / `.yml` / `.tar.gz` / `.tgz`（`import_engine_package`），否则 400。
2. `.tar.gz` / `.tgz`：安全解压到临时目录收集 yaml —— 含 `engines` 段的是引擎定义（可含 `comparison`），`bench-params.yaml` / `params.yaml` 为参数说明段；`.yaml` / `.yml` 直接解析，必须含非空 `engines` 段。
3. 包内自检：每个引擎必须含非空 `id` 且包内唯一；`kind` 必须为 `builtin` / `vllm` / `sglang` / `native` / `mock`。
4. 与现有 `benchs.yaml` 按 `id` 合并：新 `id` 记入 `added`，同 `id` 覆盖记入 `updated`；写入 `configs/benchs.yaml` 与 `configs/bench-params.yaml`；返回 `{"ok": true, "checks": [...], "added": [...], "updated": [...], "engines": [...]}`，前端刷新引擎列表。

## 6. 常见问题

**问题：环境状态显示「环境不满足」怎么办？**

查看卡片底部「环境要求」表中 FAIL 行的安装提示（`hint`，如 `pip install 'vllm>=0.23,<0.24'`），安装后刷新页面重新校验。原生引擎除包版本外还要求**命令行可用**（`vllm` 可执行文件 / `sglang` python 模块）。若暂时无真实环境，可开启该引擎的 **Mock 开关**用仿真数据联调（见 [Mock](/zh/docs/tools/mock/)）。

**问题：Mock 开关开启后测试结果是真实数据吗？**

不是。Mock 模式使用**仿真数据与运行环境**（跳过真实框架依赖校验），适合无 GPU / 无真实推理服务场景的全链路联调与演示；结果不代表真实性能。详见 [Mock](/zh/docs/tools/mock/) 与 [Bench 引擎](/zh/docs/tools/bench-engine/)。

**问题：上传引擎包失败怎么排查？**

依次确认：扩展名为 `.yaml` / `.yml` / `.tar.gz` / `.tgz`；大小 ≤ 20MB；yaml 含非空 `engines` 段；每个引擎 `id` 非空且包内唯一（同 `id` 会**覆盖更新**，记入 `updated`；不同 `id` 才新增，记入 `added`；`name` 仅用于展示，不参与去重）；`kind` 在 `builtin` / `vllm` / `sglang` / `native` / `mock` 之内。上传弹窗的 `checks` 区会逐项显示 OK / FAIL 与原因。