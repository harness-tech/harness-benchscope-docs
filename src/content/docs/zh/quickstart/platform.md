---
title: "启动平台"
description: "一条命令启动 BenchScope Web 平台，了解常用选项与首个 Dashboard 总览。"
---

# 启动平台

确认满足[环境要求](/zh/docs/quickstart/requirements/)并完成[安装](/zh/docs/quickstart/)后，用一条命令启动整个 Web 平台。

## 启动命令

```bash
benchscope
```

数秒后平台会在默认浏览器中打开 `http://127.0.0.1:8080`。如果浏览器不可用（例如无界面的服务器），可加上 `--no-browser` 不自动打开：

```bash
benchscope --port 8080 --no-browser
```

### 常用选项

| 选项 | 默认值 | 说明 |
| --- | --- | --- |
| `--host` | `0.0.0.0` | 监听地址，默认监听所有网卡便于局域网访问；可用 `127.0.0.1` 限制为本机 |
| `--port` | `8080` | 监听端口 |
| `--no-browser` | 关闭 | 启动时不自动打开浏览器 |
| `--debug` | 关闭 | 开启调试日志 |

也可通过显式的 `serve` 子命令传入相同选项：

```bash
benchscope serve --host 127.0.0.1 --port 8080 --no-browser
```

启动后控制台会打印访问地址与日志，例如：

```console
INFO  BenchScope server started
INFO  Web UI: http://127.0.0.1:8080
INFO  Browsing http://127.0.0.1:8080 ...
```

<div class="warning">

**warning**：

- 默认监听 `0.0.0.0`，表示局域网内其他机器也可访问。若仅在本地使用，建议加上 `--host 127.0.0.1`。
- 首次启动会在 `~/.benchscope` 下创建数据根目录，具体见 [配置说明](/zh/docs/install/configuration/)。

</div>

## 首次启动：总览 Dashboard

浏览器访问 `http://127.0.0.1:8080`，首先看到的是**总览 Dashboard**：

![BenchScope Dashboard 总览](/images/benchscope-dashboard.png)

Dashboard 会展示：

- **计数面板** — 性能 / 精度 / Sessions / Skills / Models / Datasets / Providers 的快捷数量。
- **环境信息** — 网络接口（MAC / IP / 子网 / 掩码）、框架版本、硬件与操作系统详情。
- **最近记录** — 最近的性能与精度运行，带各页面的快捷入口。

使用顶部导航栏可在 **Dashboard · Performance · Accuracy · Sessions · Datas · Settings** 之间切换。

## 常见问题

**问题：启动后浏览器未自动打开？**
确认未使用 `--no-browser`；也可手动在浏览器访问控制台打印的地址。

**问题：访问 http://127.0.0.1:8080 无响应？**
确认服务进程仍在运行，且端口未被占用（可换 `--port` 试其他端口）。

**问题：如何限制只在本机访问？**
启动时加上 `--host 127.0.0.1`。

## 相关文档

- [快速开始](/zh/docs/quickstart/) — 功能总览与安装
- [环境要求](/zh/docs/quickstart/requirements/) — 运行前置条件
- [安装](/zh/docs/install/) — 安装与启动细节
- [配置说明](/zh/docs/install/configuration/) — 数据根目录与 settings.json
