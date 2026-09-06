---
title: "更新与卸载"
description: "更新、卸载 BenchScope 以及运行时数据的备份与清理。"
---

# 更新与卸载

本文介绍 BenchScope 的版本升级、卸载以及运行时数据的管理（备份与清理）。

## 更新

使用 pip 升级到最新版本：

```bash
pip install --upgrade benchscope
```

升级完成后**重启服务**即可生效：

```bash
# 停止当前运行的 benchscope（Ctrl+C 或结束进程），然后重新启动：
benchscope
```

<div class="tip">

**tip**：

升级前建议先查看[更新日志](/zh/docs/releases/v1-1-0/)，了解新版本的特性与可能的破坏性变更，尤其关注数据目录与配置结构是否有迁移。若跳过多版本升级，请逐个查看中间版本说明。

</div>

### 验证升级

升级后可确认版本号：

```console
$ benchscope --version
benchscope 1.1.0
```

## 卸载

卸载 BenchScope：

```bash
pip uninstall benchscope
```

如需同时清理运行时数据：

```bash
rm -rf ~/.benchscope
```

若使用 `BENCHSCOPE_DATA_DIR` 覆盖了数据根目录，请删除该目录并取消环境变量：

```bash
rm -rf "$BENCHSCOPE_DATA_DIR"
unset BENCHSCOPE_DATA_DIR
```

<div class="warning">

**warning**：

`~/.benchscope` 存放性能产物、精度评测、日志、数据集、模型缓存等数据。**卸载前请确认是否需要备份**，一旦删除无法恢复。

</div>

## 数据备份（卸载前）

如果需要保留历史测试产物，建议在卸载前将数据根目录打包备份：

```bash
# 备份整个数据根目录
tar -czf benchscope-data-backup.tar.gz -C ~ .benchscope

# 或仅备份需要的子目录（例如性能与精度产物）
tar -czf benchscope-results.tar.gz -C ~/.benchscope perfs evals
```

备份后可通过网页 **Datas → Perfs / Evals → 导入备份** 将打包产物恢复到新环境（见 [数据与统计（Datas）](/zh/docs/data/)）。

## 版本兼容

- 旧版 `~/.benchscope/config.json` 会在启动时**自动迁移**为 `settings.json`，无需手动处理。
- 各版本更新内容见[更新日志](/zh/docs/releases/v1-1-0/)及各历史版本页面。

### 数据目录兼容

| 项目 | 说明 |
| --- | --- |
| 配置迁移 | `config.json` → `settings.json` 自动迁移，旧文件可安全删除 |
| 数据根目录 | 默认 `~/.benchscope`，可用 `BENCHSCOPE_DATA_DIR` 覆盖（见[配置说明](/zh/docs/install/configuration/)） |
| 产物格式 | 性能 `run.json` / 精度 `evals/eval-<时间>/` 跨版本基本稳定，可导入新版本 |

<div class="info">

**info**：

若卸载后重新安装，且保留了旧的 `~/.benchscope` 数据目录，则新安装会自动读取原有数据与配置，历史产物仍然可见。

</div>

## 升级 / 卸载清单

**升级：**
1. 备份 `~/.benchscope`（或自定义数据根目录）；
2. 停止正在运行的 `benchscope` 进程；
3. 执行 `pip install --upgrade benchscope`；
4. 重启服务并确认 Dashboard 正常加载；
5. 在 **Datas** 中抽查近期记录，确认数据迁移成功。

**卸载：**
1. 确认是否需要备份数据根目录；
2. 执行 `pip uninstall benchscope`；
3. （可选）删除数据根目录以完全清理。

## 常见问题

**问题：升级后启动报错？**
先确认版本号；再查看是否出现配置迁移相关提示。确认 Python 与依赖环境没有被系统其他工具改动。

**问题：如何完全重置平台？**
停止服务、备份需要的数据、删除 `~/.benchscope` 后重新启动即得到全新环境。

**问题：`pip uninstall` 后数据还在吗？**
还在。卸载只移除 Python 包，不会删除 `~/.benchscope` 数据目录，需手动 `rm -rf` 才会删除。

## 相关文档

- [安装](/zh/docs/install/) — 环境要求与启动
- [配置说明](/zh/docs/install/configuration/) — 数据目录与配置迁移
- [数据与统计（Datas）](/zh/docs/data/) — 产物落盘与导入备份
- [更新日志](/zh/docs/releases/v1-1-0/) — 各版本变更
