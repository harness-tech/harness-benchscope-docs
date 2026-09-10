---
title: Settings 手册概览
description: BenchScope Settings（设置）页操作手册概览：页面结构、七大面板、打开页面时的后台加载逻辑与手册章节导航。
---

# Settings 手册概览

Settings 页（导航名「设置」，i18n key `settings`）是 BenchScope WebUI 的全局配置中心，集中管理**语言与数据目录、推理服务 Provider、模型目录、数据集缓存、Bench 引擎与内置技能**。本手册按面板逐篇讲解「怎么点、怎么填、后台怎么跑」。

## 1. 功能说明

- **左侧菜单 + 右侧内容**布局：左侧 7 个菜单项对应 7 个面板，右侧随菜单切换。
- 所有设置修改**即时持久化**到 `~/.benchscope/settings.json`（后端 `ConfigManager` 落盘），无需重启服务（Root Dir 变更也即时生效）；面板数据全部来自后端 REST API（FastAPI，路由挂载于 `/api/*`），页面打开时并发拉取。

## 2. 页面结构

```
┌──────────────┬──────────────────────────────────────────────┐
│ 设置（标题）   │  右侧内容区（随左侧菜单切换）                   │
├──────────────┤  ┌────────────────────────────────────────┐  │
│ ▸ 通用        │  │ 面板卡片（语言/缓存路径/Provider/模型/   │  │
│ ▸ Providers  │  │ 数据集/引擎/技能卡片）                   │  │
│ ▸ 模型        │  └────────────────────────────────────────┘  │
│ ▸ 数据集      │  Bench 引擎/模型/数据集/技能 四个面板为          │
│ ▸ Bench 引擎  │  「填满高度 + 内部滚动」布局（content-fill）    │
│ ▸ 技能        │                                              │
│ ▸ 插件        │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

**七大面板**（菜单顺序与 `SettingsView.vue` 的 `menuItems` 一致）：

| 序号 | 菜单（i18n key） | 面板内容 | 对应手册 |
| --- | --- | --- | --- |
| 1 | 通用（`general`） | 语言切换、缓存路径（Root Dir + 8 个子目录） | [通用设置](/zh/docs/manual/settings/general/) |
| 2 | Providers（`environment`） | 多个推理服务提供方：添加 / 编辑 / 删除 / 测试连接 | [Provider 管理](/zh/docs/manual/settings/providers/) |
| 3 | 模型（`modelsTab`） | 模型厂商目录（国内 / 国外分组，只读浏览） | [模型与数据集管理](/zh/docs/manual/settings/models-datasets/) |
| 4 | 数据集（`datasetsTab`） | 内置数据集缓存（共 12 个，可下载） | [模型与数据集管理](/zh/docs/manual/settings/models-datasets/) |
| 5 | Bench 引擎（`benchesTab`） | 引擎列表、环境校验、Mock 开关、创建 / 上传引擎、引擎对比 | [引擎管理](/zh/docs/manual/settings/engines/) |
| 6 | 技能（`skills`） | 内置技能清单：下载技能包、复制提示词 | [技能与插件](/zh/docs/manual/settings/skills-plugins/) |
| 7 | 插件（`plugins`） | 插件系统占位（即将推出） | [技能与插件](/zh/docs/manual/settings/skills-plugins/) |

## 3. 打开页面时的后台执行逻辑

`SettingsView.vue` 的 `onMounted` 按以下顺序加载（第 1 步内部并发，其后各面板数据紧随加载）：

| 步骤 | 前端动作 | 后台 API | 说明 |
| --- | --- | --- | --- |
| 1 | `config.load()` | `GET /api/config`、`GET /api/config/status`、`GET /api/config/gpu`（并发） | 读取配置快照、服务状态、GPU 信息 |
| 2 | `loadDirs()` | `GET /api/config/dirs` | 缓存目录列表（通用面板） |
| 3 | `loadDatasets()` | `GET /api/config/datasets` | 内置数据集 + 分类 + 缓存状态 |
| 4 | `loadModelCatalog()` | `GET /api/config/model-catalog` | 模型厂商目录（国内 / 国外分组） |
| 5 | `loadBenches()` | `GET /api/benchs` → `GET /api/benchs/authoring` | 引擎列表（含环境校验 + Mock 状态）、引擎制作指引 |
| 6 | `loadProviders()` | `GET /api/config/providers` → 每个 Provider 并发 `POST /api/config/test-connection` | Provider 列表 + 逐个探测在线状态与模型 |
| 7 | `loadSkills()` | `GET /api/skills` | 内置技能清单 |

<div class="info">
**info**：任意面板的写操作（切换语言、改目录、保存 Provider、下载数据集、切 Mock 开关、上传引擎）都通过 `POST/PUT` API 落盘到 `~/.benchscope/settings.json` 或对应 yaml 文件，前端随后刷新对应列表。参考 [设置（Settings）](/zh/docs/tools/settings/) 与 [架构](/zh/docs/tools/architecture/)。
</div>

## 4. 手册章节导航

1. [通用设置](/zh/docs/manual/settings/general/) — 语言、主题、缓存路径、Root Dir 变更确认
2. [Provider 管理](/zh/docs/manual/settings/providers/) — 添加 / 编辑 / 删除 Provider、测试连接、模型探测
3. [模型与数据集管理](/zh/docs/manual/settings/models-datasets/) — 厂商目录浏览、12 个内置数据集下载缓存
4. [引擎管理](/zh/docs/manual/settings/engines/) — 引擎类型、环境校验、Mock 开关、Create / Upload Engine、引擎对比
5. [技能与插件](/zh/docs/manual/settings/skills-plugins/) — 3 个内置技能、技能包下载、提示词复制、插件占位

## 5. 常见问题

**问题：修改 Settings 后需要重启服务吗？**

不需要。所有设置（含 Root Dir 变更）即时生效并写入 `~/.benchscope/settings.json`；Root Dir 变更后后端按新根目录重建子目录（原数据不迁移）。

**问题：Settings 页支持哪些语言？**

中文（`zh`）与 English（`en`），在「通用」面板的「语言」下拉框中切换，切换后立即全页生效并持久化。

**问题：查 BenchScope 版本用什么命令？**

`benchscope --version` 不存在；查版本用 `pip show benchscope` 或调用 `GET /api/version`。