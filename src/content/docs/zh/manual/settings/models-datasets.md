---
title: 模型与数据集管理
description: Settings「模型」与「数据集」面板操作手册：模型厂商目录浏览、内置数据集下载缓存、输入参数与后台执行逻辑。
---

# 模型与数据集管理

「模型」面板（菜单 key `modelsTab`）提供**模型厂商目录**（国内 / 国外分组，只读浏览）；「数据集」面板（菜单 key `datasetsTab`）提供**内置数据集缓存**（共 12 个：9 个精度 + 3 个性能，可一键下载到本地缓存目录）。

## 1. 功能说明

- **模型厂商目录**：浏览 vLLM 支持的模型厂商（国内 / 国外），点击厂商查看其模型卡片（描述 / 精度 / 链接 / 下载命令）。数据来自后端 `GET /api/config/model-catalog`（`benchscope/configs/models.yaml`）。
- **模型卡片详情**：前端按模型名匹配内置模型目录（`web/src/data/modelCatalog.js`，6 个常用模型），展示介绍、支持的数据精度、访问链接与下载命令；未收录的模型显示「该模型暂无目录详情」。
- **内置数据集缓存**：点击下载内置数据集，缓存到 `~/.benchscope/datasets` 目录（`datasets_dir`，可在 [通用设置](/zh/docs/manual/settings/general/) 中查看）。
- **缓存状态**：每个数据集卡片显示 已缓存（`datasetCached`，绿色）/ 未缓存（`datasetNotCached`）标签。

<div class="info">
**info**：两个面板均为**只读浏览 + 单按钮操作**，不提供表单输入；模型目录数据来自 `benchscope/configs/models.yaml`，数据集缓存目录为 `datasets_dir`（默认 `~/.benchscope/datasets`，可在 [通用设置](/zh/docs/manual/settings/general/) 查看）。
</div>

## 2. 页面结构

```
【模型面板】                              【数据集面板】
┌────────────────────────────────┐  ┌────────────────────────────────┐
│ 模型厂商目录（builtinModels）    │  │ 内置数据集（builtinDatasets）    │
│ 浏览 vLLM 支持的模型厂商...       │  │ 点击下载内置数据集...（datasetsHint）│
│ [国内] [国外]（分组）             │  │ [全部] [对话] [指令微调] [数学推理] │
│  (厂商 chip，选中高亮)            │  │ [精度·知识] [精度·数学] ...        │
├────────────────────────────────┤  ├────────────────────────────────┤
│ 厂商标题（如 DeepSeek）          │  │ 数据集卡片（每个一张，整页滚动）    │
│ ┌ 模型卡片（每个模型一张）┐       │  │ ┌ MMLU        [已缓存/未缓存]     │
│ │ DeepSeek-V3      [详情] │      │  │ │ [下载]                             │
│ │ 介绍...               │       │  │ │ 描述...                            │
│ │ 支持的数据精度 [BF16]...│      │  │ │ 访问链接  https://modelscope...    │
│ │ 访问链接  https://...  │       │  │ │ 下载命令  modelscope download ...  │
│ │ 下载命令  huggingface...│      │  │ └────────────────────────────────┘ │
│ └────────────────────────┘       │  └────────────────────────────────┘ │
└────────────────────────────────┘  └────────────────────────────────┘
```

| 区域 | 控件 | 说明 |
| --- | --- | --- |
| 模型 - 分类栏 | 分组标题（国内 / 国外）+ 厂商 chip | 点击厂商 chip 切换下方模型列表（默认选中第一个厂商） |
| 模型 - 模型卡片 | 名称、详情链接、介绍、精度 tag、访问链接、下载命令（可复制） | 无匹配目录时显示 muted 提示 |
| 数据集 - 分类栏 | 「全部」+ 8 个分类 chip（带数量） | 点击 chip 过滤下方数据集卡片 |
| 数据集 - 数据集卡片 | 名称、已缓存/未缓存 tag、下载按钮、描述、访问链接、下载命令（可复制） | 下载按钮进入 loading，完成后刷新状态 |

## 3. 输入参数

两个面板均为**只读浏览 + 单按钮操作**，无表单输入；唯一显式参数是下载 API 的数据集 id：

| 接口 | 参数 | 类型 | 限制 / 约束 | 说明 |
| --- | --- | --- | --- | --- |
| `GET /api/config/model-catalog` | 无 | — | — | 返回模型厂商目录 `groups` |
| `GET /api/config/datasets` | 无 | — | — | 返回 `categories` + `datasets`（含缓存状态） |
| `POST /api/config/datasets/download` | `id` | 字符串 | 必填；枚举为 12 个内置数据集 id（见下表） | 下载指定数据集到 `datasets_dir/<id>/` |

**12 个内置数据集**（9 个精度 + 3 个性能）：

| id | 名称 | 分类 | 类型 | 下载源 |
| --- | --- | --- | --- | --- |
| `mmlu` | MMLU | `accuracy-knowledge` | 精度 | ModelScope（`opencompass/mmlu`） |
| `cmmlu` | CMMLU | `accuracy-knowledge` | 精度 | ModelScope（`opencompass/cmmlu`） |
| `c-eval` | C-Eval | `accuracy-knowledge` | 精度 | ModelScope（`opencompass/ceval-exam`） |
| `gsm8k` | GSM8K | `accuracy-math` | 精度 | HuggingFace URL（`openai/gsm8k`） |
| `math` | MATH | `accuracy-math` | 精度 | ModelScope（`opencompass/math`） |
| `humaneval` | HumanEval | `accuracy-code` | 精度 | ModelScope（`opencompass/humaneval`） |
| `mbpp` | MBPP | `accuracy-code` | 精度 | ModelScope（`opencompass/mbpp`） |
| `mt-bench` | MT-Bench | `accuracy-chat` | 精度 | ModelScope（`opencompass/mt_bench`） |
| `gaokao-bench` | GAOKAO-Bench | `accuracy-mix` | 精度 | ModelScope（`opencompass/gaokao-bench`） |
| `sharegpt` | ShareGPT | `chat` | 性能 | ModelScope（`gliang1001/ShareGPT_V3_unfiltered_cleaned_split`） |
| `alpaca` | Alpaca | `instruction` | 性能 | HuggingFace URL（`tatsu-lab/alpaca`） |
| `dolly` | Dolly | `instruction` | 性能 | HuggingFace URL（`databricks/databricks-dolly-15k`） |

分类 chip 共 8 个：`chat`（对话）、`instruction`（指令微调）、`math`（数学推理）、`accuracy-knowledge`（精度·知识）、`accuracy-math`（精度·数学）、`accuracy-code`（精度·代码）、`accuracy-chat`（精度·对话）、`accuracy-mix`（精度·综合）。

## 4. 操作步骤

### 4.1 浏览模型厂商目录

1. 左侧菜单点击「模型」。
2. 在分类栏选择分组（国内 / 国外）并点击厂商 chip（如 DeepSeek、Qwen、OpenAI）。
3. 查看该厂商下的模型卡片：点击 **详情** 跳转模型主页（新标签页）；点击「下载命令」旁的复制图标复制 `huggingface-cli download ...` 命令；访问链接同样可点击打开。
4. 切换厂商 chip 重新加载对应模型列表。

### 4.2 下载内置数据集

1. 左侧菜单点击「数据集」。
2. 在分类栏选择「全部」或具体分类 chip 过滤列表。
3. 在目标数据集卡片右上角点击 **下载** 按钮（按钮进入 loading 状态）。
4. 下载完成后卡片标签由「未缓存」变为「已缓存」（绿色），可再次点击下载覆盖刷新。
5. 需要离线导入时，复制卡片底部的「下载命令」（如 `modelscope download --dataset opencompass/mmlu --local_dir ./mmlu`）在服务器终端执行。

## 5. 后台执行逻辑

### 5.1 加载厂商目录

`GET /api/config/model-catalog` → 后端 `yaml.safe_load` 读取 `benchscope/configs/models.yaml` → 返回 `{"groups": [{key: "cn"|"intl", name_zh, name_en, providers: [{key, name, homepage, models: [...]}]}]}`；文件不存在返回 404，解析失败返回 500。前端默认选中第一个厂商。

### 5.2 加载数据集与缓存状态

`GET /api/config/datasets` → 后端：

1. `load_builtin_datasets()` 解析 `benchscope/configs/datasets.yaml`（12 个数据集定义 + 8 个分类）。
2. 对每个数据集调用 `dataset_status(ds, cache_root)`：检查 `datasets_dir/<id>/` 是否存在 → 生成 `status: {cached: bool}`。
3. 返回 `{"categories": [...], "datasets": [{id, name, category, description, url, download, status: {cached}}]}`。

### 5.3 下载数据集

`POST /api/config/datasets/download`（body `{"id": "mmlu"}`）→ 后端 `download_builtin_dataset(ds, state.config.datasets_dir)`：

| 源类型（`source.type`） | 处理方式 |
| --- | --- |
| `modelscope` | 从 ModelScope 下载 `source.dataset_id` 到 `datasets_dir/<id>/` |
| `url` | 从 `source.url` 拉取文件到 `datasets_dir/<id>/` |

- 未知 `id` 返回 **404**；下载异常返回 **502**（detail 含原因）。
- 成功后前端重新 `loadDatasets()` 刷新缓存状态。

## 6. 常见问题

**问题：数据集缓存到哪里？**

`datasets_dir`，默认 `~/.benchscope/datasets`，每个数据集占一个子目录（`datasets_dir/<id>/`）。目录可在 [通用设置](/zh/docs/manual/settings/general/) 的缓存路径面板查看（只读，跟随 Root Dir）。

**问题：模型面板能添加或删除模型吗？**

不能。模型面板是**只读厂商目录**（数据来自 `benchscope/configs/models.yaml`），无添加 / 删除入口；要新增模型明细需修改该 yaml 文件。模型的实际使用（压测 / 精度评测）在新建任务页选择，详见 [性能测试](/zh/docs/performance/) 与 [精度测试](/zh/docs/accuracy/)。

**问题：数据集显示「未缓存」但下载命令可以复制，二者是什么关系？**

「已缓存 / 未缓存」只反映本地 `datasets_dir/<id>/` 是否存在；「下载命令」供在服务器终端手动下载（如内网无法走 WebUI 时）。WebUI 点击 **下载** 与执行下载命令效果一致，都落到 `datasets_dir/<id>/`。