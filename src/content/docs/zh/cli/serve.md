---
title: "serve 命令"
---

# serve 命令

启动 Web 服务，默认在 `http://127.0.0.1:8080` 打开完整平台。

```bash
benchscope serve [--host HOST] [--port PORT] [--no-browser] [--debug]
```

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--host` | `0.0.0.0` | 监听地址 |
| `--port` | `8080` | 监听端口 |
| `--no-browser` | 关闭 | 启动时不自动打开浏览器 |
| `--debug` | 关闭 | 开启调试日志（输出更详细的运行日志便于排障） |

<div class="tip">

**tip**：

`--debug` 在排查任务启动、接口调用等问题时非常有用，会输出详细的 debug 级别日志。

</div>

<div class="info">

**info**：

**向后兼容行为**：当 `benchscope` 无参数、或首个参数是选项（如 `--port 8080`）时，会走向兼容的「启动服务」行为，等价于 `benchscope serve`。

</div>

示例：

```bash
benchscope serve --host 127.0.0.1 --port 9090 --no-browser
```

## 相关文档

- [CLI 概述](/zh/docs/cli/) — 子命令总览与快速上手
- [perf 命令](/zh/docs/cli/perf/) — 性能压测
- [eval 命令](/zh/docs/cli/eval/) — 精度评测
- [快速入门](/zh/docs/quickstart/) — 安装与启动
