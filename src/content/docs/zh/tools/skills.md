---
title: "内置技能"
description: "BenchScope 随包分发的 3 个内置技能：bs-perfs-concurrency / bs-perfs-threshold / bs-engine-create，及其在 Settings → Skills 中的查看与下载方式。"
---

# 内置技能

BenchScope 随包分发 3 个**内置技能**（位于包内 `benchscope/skills/`），为 Agent（如 Harness、Claude）提供结构化的操作指引：如何编写性能压测配置、如何配置阈值探测、如何创建自定义引擎。在 **Settings → Skills** 面板可查看全部内置技能，并支持打包下载。

## 技能清单

| 技能 | ID | 用途 |
| --- | --- | --- |
| 并发压测配置 | `bs-perfs-concurrency` | 指导 Agent 编写并发压测任务配置（并发列表 / 输入输出长度 / 请求数等），并提供配置模板与打包脚本。 |
| 阈值探测配置 | `bs-perfs-threshold` | 指导 Agent 编写阈值探测任务配置（TTFT / TPOT / 输出吞吐阈值、判定统计量、搜索上限），并提供配置模板与打包脚本。 |
| 自定义引擎创建 | `bs-engine-create` | 指导 Agent 按引擎接入契约创建自定义引擎（Input / Core / Output / Mock 四部分），并提供校验脚本（`validate.sh`）与导入清单。 |

## 使用方式

### 在 Web 界面查看

1. 进入 **Settings → Skills** 面板；
2. 查看 3 个内置技能的说明卡片（名称 / 描述 / 版本）；
3. 点击**下载**可获取技能包（tar.gz），供 Agent 环境安装使用。

对应 API：

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| `/api/skills` | GET | 内置技能清单。 |
| `/api/skills/{skill_id}/download` | GET | 下载指定技能包（tar.gz）。 |

### 在 Agent 环境安装

将技能包解压到 Agent 的技能目录（如 `~/.dsh/skills/` 或 Harness 技能目录）后，Agent 即可在编写压测配置 / 阈值配置、创建自定义引擎时引用对应技能。

## 技能包结构

每个技能目录遵循统一结构：

```text
benchscope/skills/<skill-id>/
├── SKILL.md          # 技能指令（Agent 阅读的核心）
├── README.md         # 人类可读说明
├── templates/        # 配置模板（如 bench-perfs-config.yaml）
└── scripts/          # 辅助脚本（package.sh 打包 / validate.sh 校验）
```

<div class="info">

**info**：

`bs-engine-create` 技能的 `validate.sh` 会离线校验引擎定义文件（`configs/benchs.yaml` 与 `configs/bench-params.yaml`），校验项与后端导入校验保持一致，创建自定义引擎前可先运行该校验。

</div>

## 常见问题

**问题：内置技能和自定义技能有什么区别？**
内置技能随 pip 包分发（Settings → Skills 中始终可见）；自定义技能由用户自行创建并安装到 Agent 环境，两者互不影响。

**问题：为什么 Dashboard 的 Skills 计数是 3？**
计数即内置技能数（`bs-perfs-concurrency` / `bs-perfs-threshold` / `bs-engine-create`），见 [Dashboard 概览](/zh/docs/tools/dashboard/)。

**问题：如何基于 bs-engine-create 创建自定义引擎？**
安装技能后，让 Agent 按 SKILL.md 指引产出引擎定义（追加到 `configs/benchs.yaml`）与参数定义（追加到 `configs/bench-params.yaml`），运行 `validate.sh` 校验后通过 Settings → Bench Engines 导入，详见 [Bench 引擎](/zh/docs/tools/bench-engine/)。

## 相关文档

- [Bench 引擎](/zh/docs/tools/bench-engine/) — 引擎接入契约与自定义引擎
- [设置（Settings）](/zh/docs/tools/settings/) — Skills 面板与技能下载
- [Dashboard 概览](/zh/docs/tools/dashboard/) — Skills 计数
- [API 概述](/zh/docs/api/) — 技能相关接口