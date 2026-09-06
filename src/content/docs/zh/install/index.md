---
title: "概述"
description: "安装 BenchScope、启动 Web 平台并完成基础配置。"
---

# 概述

本文介绍如何安装 BenchScope、启动平台并完成基础配置。完整的环境与数据目录说明见 [配置说明](/zh/docs/install/configuration/)，升级 / 卸载见 [更新与卸载](/zh/docs/install/update-uninstall/)。

## 环境要求

- **Python**：推荐 3.10 及以上（同时支持 3.9 / 3.11 / 3.12）。
- **pip**：建议使用较新的 pip（`pip install --upgrade pip`）。
- **网络**：安装时需要访问 PyPI；压测时需要能访问被测推理服务。
- **浏览器**：Chrome / Edge / Firefox 等现代浏览器（推荐 Chrome）。

<div class="tip">

**tip**：

建议使用**虚拟环境**（如 `python -m venv` / `conda`）安装 BenchScope，避免与系统其他 Python 包相互干扰，也便于版本升级与卸载。

</div>

## 安装

从 PyPI 安装 BenchScope：

```bash
pip install benchscope
```

安装完成后验证版本与可用命令：

```console
$ benchscope --version
benchscope 1.1.0
$ benchscope --help
usage: benchscope [-h] [--version] {serve,perf,eval} ...
```

> 如需**原生精度评测（Native）**能力（本地加载 transformers 权重离线评测，无需外部推理服务），请安装额外可选依赖：`pip install benchscope[accuracy-native]`。若不确定是否需要，可先按基础安装，之后按需补充。

<div class="info">

**info**：

BenchScope 的 Web 前端完全内嵌在 Python 包中，安装后**无需**额外安装 Node.js 或前端依赖，也无需单独启动前后端服务。

</div>

## 启动平台

一条命令即可启动整个 Web 平台：

```bash
benchscope
```

常用选项：

```bash
benchscope --port 8080 --no-browser
```

| 选项 | 默认值 | 说明 |
| --- | --- | --- |
| `--host` | `0.0.0.0` | 监听地址，默认监听所有网卡，便于局域网访问 |
| `--port` | `8080` | 监听端口 |
| `--no-browser` | 关闭 | 启动时不自动打开浏览器 |
| `--debug` | 关闭 | 开启调试日志 |

启动后控制台会打印访问地址，浏览器访问 http://127.0.0.1:8080 即可进入平台：

```console
INFO  BenchScope server started
INFO  Web UI: http://127.0.0.1:8080
```

<div class="warning">

**warning**：

默认监听 `0.0.0.0`，意味着**局域网内其他机器也能访问**该平台。若仅在本地使用，建议加上 `--host 127.0.0.1`；首次启动会在 `~/.benchscope` 下创建数据根目录（见 [配置说明](/zh/docs/install/configuration/)）。

</div>

## 下一步

启动成功后：

1. 在 **Settings → Providers** 配置你的推理服务（Base URL 与 API Key）；
2. 进入 **性能测试** 页做并发压测或阈值探测；
3. 进入 **精度测试** 页做量化评测；
4. 进入 **Sessions** 页与模型交互式对话。

## 常见问题

**问题：端口被占用怎么办？**
使用 `--port` 指定其他端口，例如 `benchscope --port 9090`，然后访问对应地址。

**问题：启动后没有自动打开浏览器？**
加 `--host` / `--port` 等显式参数时不会自动打开浏览器；也可使用 `--no-browser` 关闭自动打开，再手动访问控制台打印的地址。

**问题：安装后 `benchscope` 命令找不到？**
多为虚拟环境未激活或未将 `Scripts` / `bin` 目录加入 PATH，请检查当前环境后重试。

## 相关文档

- [快速开始](/zh/docs/quickstart/) — 功能总览与上手
- [配置说明](/zh/docs/install/configuration/) — 数据根目录、settings.json 与内置配置清单
- [更新与卸载](/zh/docs/install/update-uninstall/) — 升级、卸载与数据清理
- [CLI](/zh/docs/cli/) — `serve` / `perf` / `eval` 子命令与参数
