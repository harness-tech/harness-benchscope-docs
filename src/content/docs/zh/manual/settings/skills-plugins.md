---
title: 技能与插件
description: Settings「技能」与「插件」面板操作手册：3 个内置技能、技能包下载、提示词复制、插件系统占位与后台执行逻辑。
---

# 技能与插件

「技能」面板（菜单 key `skills`）展示 BenchScope 的**内置技能清单**（面向 Bench 引擎制作与基准测试流程的 AI 技能包），支持查看功能特性 / 使用说明 / 提示词，并可**下载技能包**或**复制提示词**；「插件」面板（菜单 key `plugins`）为插件系统占位（即将推出）。

## 1. 功能说明

- **内置技能清单**：面向 Bench 引擎制作与基准测试流程的 AI 技能包，下载安装或复制提示词后即可使用（技能本体位于 `benchscope/skills/<skill-id>/SKILL.md`，随包分发）。
- **功能特性 / 使用说明 / 提示词**：每张技能卡片展示 功能特性（无序列表）、使用说明（有序列表）与提示词全文（等宽文本块），均按界面语言显示中英双语。
- **下载技能**：下载技能版本包（`.tar.gz`）；后端优先返回已发版的本地产物，未发版时实时打包一次。
- **复制提示词**：将技能提示词文本写入剪贴板，发送给 AI 助手即可按流程执行。
- **插件系统**：即将推出，当前面板仅显示占位文案（`pluginsDesc`「插件系统即将推出。」）；插件安装目录 `plugins_dir`（默认 `~/.benchscope/plugins`）已随目录体系预留。

<div class="info">
**info**：技能面板无表单输入，操作仅「查看 / 复制提示词 / 下载技能」三种；技能清单由后端扫描 `benchscope/skills/` 目录动态生成，详见 [Skills](/zh/docs/tools/skills/)。
</div>

## 2. 页面结构

```
【技能面板】                                   【插件面板】
┌────────────────────────────────────────┐  ┌──────────────────────────────┐
│ 技能（skills）                          │  │ 插件（plugins）              │
│ 内置技能清单：面向 Bench 引擎制作与...    │  │ 插件系统即将推出。           │
├────────────────────────────────────────┤  │ （空状态：暂无数据）          │
│ 技能卡片（每个技能一张，整页滚动）        │  └──────────────────────────────┘
│  bs-engine-create  [bs-engine-create]  版本 v1.2.0
│  创建自定义 Bench Engine 压缩包...        │
│  功能特性：                               │
│   - 基于 yaml 定义自定义 bench 引擎...    │
│  使用说明：                               │
│   1. 下载技能：下载技能包（.tar.gz）...   │
│   2. 复制提示词：将下方提示词发送给 AI... │
│  提示词：                                 │
│  ┌──────────────────────────────────┐  │
│  │ 你正在使用 bs-engine-create 技能... │  │
│  └──────────────────────────────────┘  │
│  [下载技能]    [复制提示词]              │
└────────────────────────────────────────┘
```

| 区域 | 控件 / 内容 | 说明 |
| --- | --- | --- |
| 卡片头部 | 名称 + id 标签（紫色）+ 版本（`v{version}`） | 版本取自 `SKILL.md` frontmatter 的 `version` 字段 |
| 卡片中部 | 描述、功能特性（`skillFeatures`，无序列表）、使用说明（`skillUsage`，有序列表）、提示词（`skillPrompt`，等宽文本块） | 按界面语言取 `*_zh` / 英文字段 |
| 卡片底部 | **下载技能**（`skillDownload`）/ **复制提示词**（`skillCopyPrompt`）按钮 | 文字按钮（link 样式） |
| 插件面板 | 标题 + 占位文案 + 空状态 | 无控件、无数据 |

## 3. 输入参数

技能面板**无表单输入**，输入仅为下载 API 的技能 id：

| 接口 | 参数 | 类型 | 限制 / 约束 | 说明 |
| --- | --- | --- | --- | --- |
| `GET /api/skills` | 无 | — | — | 返回内置技能清单 `{skills: [...]}` |
| `GET /api/skills/{skill_id}/download` | `skill_id`（路径参数） | 字符串 | 必填；枚举为当前内置技能 id（见下表） | 下载技能版本包（`.tar.gz`），失败时前端回退下载 `SKILL.md` 文本 |

**内置技能**（`benchscope/skills/`，共 3 个）：

| id | 名称 | 版本 | 用途 |
| --- | --- | --- | --- |
| `bs-engine-create` | bs-engine-create | 1.2.0 | 创建自定义 Bench Engine（vLLM / SGLang 等）压缩包：导入时校验 + Mock 数据验证 + 功能动态注册 |
| `bs-perfs-concurrency` | bs-perfs-concurrency | 1.0.0 | 用 `benchscope perf` 进行并发（concurrency）压测：内置表单 + 保存任务 / 日志 + 生成可导入 Datas/perfs 的压缩包 |
| `bs-perfs-threshold` | bs-perfs-threshold | 1.0.0 | 用 `benchscope perf --mode threshold` 进行阈值搜索压测：内置表单 + 保存任务 / 日志 + 生成可导入 Datas/perfs 的压缩包 |

技能对象字段：`id` / `name` / `version` / `description(_zh)` / `features(_zh)` / `usage(_zh)` / `prompt(_zh)` / `download`（`SKILL.md` 路径）/ `download_url`（`/api/skills/<id>/download`）/ `package`（`<id>-<version>.tar.gz`）。

## 4. 操作步骤

### 4.1 查看技能

1. 左侧菜单点击「技能」。
2. 浏览技能卡片：名称 + id 标签 + 版本（头部）；描述、功能特性、使用说明、提示词（中部）。
3. 界面语言切换为中文时，各文案块自动显示中文（`*_zh` 字段）。

### 4.2 复制提示词

1. 在目标技能卡片底部点击 **复制提示词** 按钮。
2. 技能提示词文本写入剪贴板（提示「提示词已复制」；剪贴板不可用时提示「复制失败，请手动选择复制」）。
3. 将提示词粘贴给任意 AI 助手，按提示词流程执行（如让 AI 追问框架与版本、生成引擎包）。

### 4.3 下载技能

1. 在目标技能卡片底部点击 **下载技能** 按钮。
2. 浏览器下载技能版本包 `.tar.gz`（文件名形如 `bs-engine-create-1.2.0.tar.gz`），提示「技能包已下载」。
3. 将技能包导入任意支持 skills 的 agents 平台即可使用。

## 5. 后台执行逻辑

### 5.1 加载技能清单

`GET /api/skills` → 后端 `_collect_skills()`：

1. 扫描 `benchscope/skills/` 下的子目录（按目录名排序），跳过无 `SKILL.md` 的目录。
2. 解析每个 `SKILL.md` 的 YAML frontmatter（`---` 分隔）：读取 `name`、`description`、`version`（缺省 `1.0.0`）。
3. 合并内置补充元数据 `_SKILL_EXTRA`（中英双语的 `description_zh` / `features(_zh)` / `prompt(_zh)`；无补充项时回退 `SKILL.md` 全文作为提示词）。
4. 生成 `download`（`SKILL.md` 路径）、`download_url`（`/api/skills/<id>/download`）、`package`（`<id>-<version>.tar.gz`）字段，返回 `{"skills": [...]}`。

### 5.2 下载技能包

`GET /api/skills/{skill_id}/download`：

| 步骤 | 逻辑 |
| --- | --- |
| 1. 定位技能目录 | `benchscope/skills/<skill_id>/` 不存在或无 `SKILL.md` → 返回 **404** |
| 2. 读取版本号 | 从 `SKILL.md` frontmatter 解析 `version` |
| 3. 优先已发版产物 | `skills/<skill_id>/dist/<skill_id>-<version>.tar.gz` 存在 → 直接 `FileResponse`（`application/gzip`）返回 |
| 4. 未发版实时打包 | 执行 `skills/<skill_id>/scripts/package.sh`（子进程，**超时 120 秒**）在临时目录打包，返回生成的 `.tar.gz`；无打包脚本 → **404**；打包失败 → **500** |

前端 `downloadSkill`：请求 `download_url`（`responseType: 'blob'`）→ 以 `package.name`（如 `bs-engine-create-1.2.0.tar.gz`）触发浏览器下载；**请求失败时回退**为把技能提示词文本打包成 `.md` 文件下载。

### 5.3 复制提示词

前端 `copySkillPrompt`：`navigator.clipboard.writeText(s.prompt)` 写入剪贴板（复制的是技能**默认英文提示词**文本，与界面语言无关）；成功提示「提示词已复制」，异常提示「复制失败，请手动选择复制」。

### 5.4 插件面板

「插件」面板为静态占位：仅渲染标题（`plugins`）+ 文案（`pluginsDesc`「插件系统即将推出。」）+ 空状态，**无数据加载、无 API 调用**；插件安装目录 `plugins_dir`（默认 `~/.benchscope/plugins`）已随目录体系预留（见 [通用设置](/zh/docs/manual/settings/general/)）。

## 6. 常见问题

**问题：技能包下载后怎么用？**

下载的是 `.tar.gz` 技能包（如 `bs-engine-create-1.2.0.tar.gz`），可导入任意支持 skills 的 agents 平台（技能清单见 [Skills](/zh/docs/tools/skills/)）；也可以只点「复制提示词」，把提示词发给 AI 助手按流程执行，无需安装。

**问题：复制的提示词和卡片里显示的提示词一致吗？**

界面显示的是按语言本地化的提示词（中文界面显示 `prompt_zh`）；「复制提示词」按钮复制的是技能的**默认英文提示词**（`prompt` 字段）。两者内容一致、语言不同。

**问题：技能列表是固定的吗？**

当前内置 3 个技能（`bs-engine-create`、`bs-perfs-concurrency`、`bs-perfs-threshold`），由 `benchscope/skills/` 目录下的 `SKILL.md` 驱动；后端扫描该目录动态生成清单，新增技能目录后重启服务即可出现在列表中。

**问题：插件面板什么时候能用？**

插件系统即将推出，当前面板仅为占位（「插件系统即将推出。」），无可用功能；插件安装目录 `plugins_dir`（默认 `~/.benchscope/plugins`）已随目录体系预留。