# 快速入门

BenchScope 是一个开源的大模型推理测试平台，基于 Harness Coding 开发。它面向大语言模型的**性能与精度**提供可视化测试能力，支持基于 vLLM / SGLang 的模型推理，以及所有兼容 OpenAI 协议的接口。

在几分钟内，你就可以通过一条命令启动完整的 Web 测试平台，对已部署的推理服务进行并发压测、阈值探测与精度评测。

![BenchScope 性能测试主界面](/images/benchscope-performance_default.png)

::: tip
BenchScope 本身**不需要本地 GPU 或推理框架**。被测试的是你已部署的推理服务（vLLM / SGLang 等，位于 `http://127.0.0.1:8000`），BenchScope 负责发起压测与评测请求并收集、可视化结果。
:::

## 环境要求

- **Python**：推荐 3.10 及以上版本（同时支持 3.9 / 3.11 / 3.12）。
- **pip**：建议使用较新的 pip 以正确解析依赖（`pip install --upgrade pip`）。
- **网络**：安装时需访问 PyPI；压测时需能访问被测推理服务。
- **浏览器**：Chrome / Edge / Firefox 等现代浏览器（推荐 Chrome）。

::: info
BenchScope 的 Web 前端完全内嵌在 Python 包中，安装后无需额外安装 Node.js 或前端依赖，一条命令即可启动完整平台。
:::

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

::: tip
如果希望使用**原生精度评测（Native）**能力（本地加载 transformers 权重离线评测），请安装额外可选依赖：

```bash
pip install benchscope[accuracy-native]
```
:::

## 启动平台

一条命令启动整个 Web 平台：

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

启动后控制台会打印访问地址与日志，例如：

```console
INFO  BenchScope server started
INFO  Web UI: http://127.0.0.1:8080
INFO  Browsing http://127.0.0.1:8080 ...
```

浏览器访问 http://127.0.0.1:8080 即可进入平台，首先看到的是**总览 Dashboard**：

![BenchScope Dashboard 总览](/images/benchscope-dashboard.png)

::: warning
- 默认监听 `0.0.0.0`，表示局域网内其他机器也可访问。若仅在本地使用，建议加上 `--host 127.0.0.1`。
- 首次启动会在 `~/.benchscope` 下创建数据根目录，具体见 [配置说明](./configuration.md)。
:::

## 下一步

启动成功后，你可以：

1. 在 **Settings → Providers** 配置你的推理服务（Base URL 与 API Key）；
2. 进入 **性能测试** 页对服务做并发压测或阈值探测；
3. 进入 **精度测试** 页对模型输出做量化评测；
4. 进入 **Sessions** 页直接与模型交互式对话。

## 常见问题

**问题：启动后浏览器未自动打开？**
确认未使用 `--no-browser`；也可手动在浏览器访问控制台打印的地址。

**问题：访问 http://127.0.0.1:8080 无响应？**
确认服务进程仍在运行，且端口未被占用（可换 `--port` 试端口）。

**问题：如何更新到最新版本 / 卸载？**
见 [更新与卸载](./update-uninstall.md)。

## 相关文档

- [CLI 参考](./cli.md) — `serve` / `perf` / `eval` 三个子命令完整参数
- [配置说明](./configuration.md) — 数据根目录、settings.json 与内置配置清单
- [性能测试](../core/performance.md) — 并发压测与阈值探测双模式
- [精度测试](../core/accuracy.md) — 原生 / 服务双模式评测
- [更新与卸载](./update-uninstall.md) — 升级、卸载与数据清理
