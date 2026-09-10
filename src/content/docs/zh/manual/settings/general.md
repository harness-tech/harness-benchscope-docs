---
title: 通用设置
description: Settings「通用」面板操作手册：语言切换、主题说明、缓存路径（Root Dir）修改与数据目录变更确认、后台执行逻辑。
---

# 通用设置

「通用」面板（菜单 key `general`）提供两项设置：**语言**（界面语言切换）与**缓存路径**（Root Dir 与 8 个子目录）。修改均即时持久化到 `~/.benchscope/settings.json`，无需重启。

## 1. 功能说明

- **语言**：中文（`zh`）/ English（`en`）二选一，切换后立即生效并保存。
- **缓存路径**：列出 9 个目录；仅 **Root Dir**（`data_dir`）可编辑，其余 8 个子目录只读展示（跟随 Root Dir 自动重置）。
- **主题（`theme`）**：平台支持 `light` / `dark` / `system` 三档（`App.vue` 读取配置渲染），当前版本 Settings 页**未提供主题控件**，需通过 `POST /api/config` 写入 `theme` 字段或直接编辑 `~/.benchscope/settings.json`。
- **推理服务 API（`api`）**：Base URL / Endpoint / API Key / 额外请求头四项由 [Providers 面板](/zh/docs/manual/settings/providers/)统一管理，激活的 Provider 自动同步到配置 `api` 字段（`base_url` / `endpoint` / `api_key` / `extra_headers`）。
- **bench 命令（`bench_commands`）**：`vllm` → `vllm bench serve`、`sglang` → `python -m sglang.bench_serving`，供原生引擎调用；Settings 页不暴露控件，可经 `POST /api/config` 修改。

## 2. 页面结构

```
┌──────────────────────────────────────────────┐
│ 语言                                         │
│  [English / 中文 ▾]                          │
├──────────────────────────────────────────────┤
│ 缓存路径                                      │
│  根目录 (Root Dir)   ~/.benchscope   [可编辑] │
│  性能 (Perf)         ~/.benchscope/perfs      │
│  精度 (Eval)         ~/.benchscope/evals      │
│  分析 (Analysis)     ~/.benchscope/analysys   │
│  日志 (Logs)         ~/.benchscope/logs       │
│  会话 (Sessions)     ~/.benchscope/sessions   │
│  模型 (Models)       ~/.benchscope/models     │
│  数据集 (Datasets)   ~/.benchscope/datasets   │
│  插件 (Plugins)      ~/.benchscope/plugins    │
└──────────────────────────────────────────────┘
```

| 区域 | 控件 | 说明 |
| --- | --- | --- |
| 语言卡片 | `a-select` 下拉框 | 选项：English（`en`）/ 中文（`zh`），默认 `en` |
| 缓存路径卡片 | 9 行目录（标签 + 描述 + 路径值） | 仅 Root Dir 行可点击编辑，其余 8 行为只读灰色文字 |
| Root Dir 编辑态 | 输入框 + Save 按钮 | 点击 Root Dir 路径值进入；回车或 Save 触发确认弹窗 |
| 变更确认弹窗 | 确定 / 取消 | 标题 `rootDirChangeTitle`「更改数据存储路径」，正文 `rootDirChangeContent` |

## 3. 输入参数

### 3.1 语言

| 字段 | 类型 | 限制 / 约束 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `locale` | 枚举 | 必填；仅 `en` / `zh` | `en` | 界面语言；下拉选项为 English / 中文 |

### 3.2 缓存路径

| 字段（key） | 可编辑 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `data_dir` | 是 | `~/.benchscope` | 数据根目录（Root Dir）；修改后即时生效、无需重启 |
| `perfs_dir` | 否 | `~/.benchscope/perfs` | 性能测试任务目录 |
| `evals_dir` | 否 | `~/.benchscope/evals` | 精度测试任务目录 |
| `analysis_dir` | 否 | `~/.benchscope/analysys` | 数据分析目录（目录名是 `analysys`，联动 Datas 缓存） |
| `logs_dir` | 否 | `~/.benchscope/logs` | 日志目录（runtime 日志 + 任务终端输出） |
| `sessions_dir` | 否 | `~/.benchscope/sessions` | 会话缓存目录 |
| `models_dir` | 否 | `~/.benchscope/models` | 模型下载目录（联动 Settings/Models） |
| `datasets_dir` | 否 | `~/.benchscope/datasets` | 数据集下载目录（联动 Settings/Datasets） |
| `plugins_dir` | 否 | `~/.benchscope/plugins` | 插件安装加载目录 |

字段限制：Root Dir 输入值 **trim 后不能为空**（空值不保存、直接还原）；与当前值相同则不触发保存；路径支持 `~` 展开。

## 4. 操作步骤

### 4.1 切换语言

1. 左侧菜单点击「通用」。
2. 「语言」卡片下拉框中选择 `中文` 或 `English`。
3. 无需点击保存：切换后立即全页生效并自动持久化。

### 4.2 修改 Root Dir

1. 左侧菜单点击「通用」，进入「缓存路径」卡片。
2. 点击 Root Dir 行右侧的当前路径值（只读样式 → 变为输入框 + Save 按钮）。
3. 在输入框中填入新路径（支持 `~`），按 **Enter** 或点击 **Save**。
4. 弹出「更改数据存储路径」确认框：文案为「点击确定将根据新的 Root Dir 创建新的空白数据存储路径，原有数据不会迁移。是否继续？」。
5. 点击 **确定**：保存新路径；或 **取消**：丢弃编辑、恢复原值显示。

<div class="warning">

**warning**：Root Dir 变更后创建的是**全新空白目录树**，原有数据**不会迁移**；8 个子目录（`perfs` / `evals` / `analysys` / `logs` / `sessions` / `models` / `datasets` / `plugins`）全部重置为新根下的默认目录。变更前请先备份或导出重要数据。

</div>

## 5. 后台执行逻辑

### 5.1 页面加载

`GET /api/config/dirs` → 后端遍历 `CACHE_DIR_INFO`（9 项）返回 `value`（当前配置值，缺省取 `DEFAULT_CONFIG`）、`default`、`exists`（目录是否存在）、`readonly`（仅 `data_dir` 为 `false`）。

### 5.2 切换语言

前端 `onLocaleChange`：`setLocale(locale)` 立即替换界面文案 → `config.save({ locale })` → `POST /api/config`（body `{"locale": "zh"}`）→ 后端 `ConfigManager.update` 合并并写入 `~/.benchscope/settings.json`。

### 5.3 保存 Root Dir

`POST /api/config/dirs`（body `{"data_dir": "<新路径>"}`）：

1. 后端检查运行中任务：`state.tasks.running_count > 0` 且补丁含 `perfs_dir` / `evals_dir` 时返回 **409**（当前 UI 只提交 `data_dir`，不会触发）。
2. `ConfigManager.update`：`data_dir` 变化 → 8 个子目录全部重置为 `<新根>/默认子目录`（`perfs` / `evals` / `analysys` / `logs` / `sessions` / `models` / `datasets` / `plugins`）。
3. 同步环境变量 `BENCHSCOPE_DATA_DIR` 为新根（子进程透传，无需重启服务）。
4. `save()` 落盘 settings.json，`ensure_dirs()` 递归创建全部目录。
5. 返回 `{"ok": true, "requires_restart": false, "changed": {...}}`，前端重新 `loadDirs()` 刷新列表。

### 5.4 相关接口（当前 UI 未调用，供 API 使用）

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| `/api/config` | `POST` | 通用配置补丁（`theme` / `locale` / `api` / `bench_commands` 等字段） |
| `/api/config/restart` | `POST` | body `{"migrate": bool}`：可选迁移数据并重启服务（`os.execv` 重启进程） |

## 6. 常见问题

**问题：修改 Root Dir 后旧数据还能用吗？**

不能直接沿用。新 Root Dir 是空白目录树，旧数据保留在原路径；如需搬迁，可先手动拷贝，或调用 `POST /api/config/restart`（`migrate: true`）走迁移流程。详见 [配置说明](/zh/docs/install/configuration/)。

**问题：为什么子目录显示为灰色不可编辑？**

8 个子目录由 Root Dir 派生（`<根>/perfs`、`<根>/analysys` 等），只读展示；要改位置请修改 Root Dir。注意分析目录名是 `analysys`（不是 `analysis`）。

**问题：主题在哪里切换？**

当前版本 Settings 页没有主题控件；主题取自配置 `theme` 字段（`light` / `dark` / `system`，默认 `light`），可经 `POST /api/config` 修改后刷新页面生效。