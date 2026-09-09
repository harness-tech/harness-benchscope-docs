---
title: "概述"
---

# 概述

**Datas** 记录并组织历史测试产物与结果，支持导入恢复、查看与分析，是所有性能压测与精度评测结果的「档案馆」。

![BenchScope Datas 性能记录详情](/images/benchscope-datas-perfs_detail.png)

<div class="tip">

**tip**：

Datas 是你所有历史测试的持久化视图：在网页或 [CLI](/zh/docs/cli/) 产生的性能 / 精度产物，都会在这里登记，可查看、可导入、可导出。

</div>

## 记录面板

Datas 按类型提供多个记录面板，每个面板对应一类测试产物：

### Perfs（性能测试记录）

- 分页记录表 + **最佳测试记录高亮**（性能最佳，金色 **Best** 标记）；
- **Perf Datas**：性能数据详情——Output / TTFT / TPOT / ITL 的 **mean / median / p99** 三元组；
- **Perf-Cases-Logs 高视图**：按用例组织查看；
- **分析面板**：多选记录**对比分析**；
- 操作：删除 / 备份 / 分享 / **导入恢复**。

### Evals（精度评测记录）

- 查看精度评测产物与结果；
- 支持打包导入。

### Analysis（数据分析）

- 数据分析面板（部分版本为占位）。

## 导入备份

Datas 支持从打包备份中恢复历史记录：

- **性能**：打包为**扁平 zip**（含 `run.json` + 日志 + 可选 `metrics.json`），在 **Datas → Perfs → 导入备份** 导入。
- **精度**：导入 `evals` 产物目录打包文件。

```bash
# 性能任务产物打包示例（手动打包后导入）
cd ~/.benchscope/perfs/<run_id>
zip -r perf-backup.zip run.json perf_<run_id>_*.log metrics.json
```

<div class="info">

**info**：

CLI 命令 `benchscope perf` / `benchscope eval` 落盘的产物与 Web UI 完全一致。因此你可以在无界面的机器上跑测试、打包 zip，再导入到本机 BenchScope 实例以图形方式查看。

</div>

<div class="warning">

**warning**：

导入备份用于在不同机器 / 环境间迁移历史记录。导入的是产物包，而不是整个数据目录。

</div>

## 记录详情

每条记录都支持深入查看：

- **单请求实时快照**可回看（性能页第二行实时面板 + Datas / Perfs 详情弹窗）。
- **日志**在线预览与下载。
- **Excel 导出**：按 mean / P99 汇总导出（含分组标题行与 Best / BestPerf 标记）。

性能记录详情页：

![BenchScope Datas 性能记录统计](/images/benchscope-datas-perfs_statistics.png)

### 性能统计示例

| 指标 | mean | median | p99 |
| --- | --- | --- | --- |
| Output (tok/s) | 112.4 | 110.8 | 96.5 |
| TTFT (ms) | 92.5 | 71.3 | 205.1 |
| TPOT (ms) | 34.2 | 33.1 | 58.7 |
| ITL (ms) | 33.9 | 32.7 | 58.6 |

## 数据来源

所有 Datas 记录都来自本地数据根目录的产物落盘（见[配置说明](/zh/docs/install/configuration/)）：

| 来源 | 数据目录 |
| --- | --- |
| 性能压测 | `~/.benchscope/perfs/`（`run.json` + 日志） |
| 精度评测 | `~/.benchscope/evals/eval-<时间>/`（task / result / samples） |
| 数据分析 | `~/.benchscope/analysis/` |

## 常见问题

**问题：找不到某次历史任务？**
确认数据根目录未被清理 / 未切换 `BENCHSCOPE_DATA_DIR`；也可通过导入备份恢复。

**问题：导入后结构异常？**
确认 zip 为平坦结构（根目录直接含 `run.json` / 日志等），嵌套目录可能导致导入失败。

## 相关文档

- [性能测试](/zh/docs/performance/) — 产生 Perfs 记录
- [概述](/zh/docs/accuracy/) — 产生 Evals 记录
- [配置说明](/zh/docs/install/configuration/) — 产物落盘目录
- [设置（Settings）](/zh/docs/tools/settings/) — 数据目录与 Cache Paths
