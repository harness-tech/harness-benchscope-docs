---
title: "帮助"
---

# 帮助

遇到问题或想参与贡献？从下面的入口开始。

## 常见问题 / 排障

- **启动后浏览器未自动打开**：确认未使用 `--no-browser`，或手动访问控制台打印的地址。
- **访问 http://127.0.0.1:8080 无响应**：确认服务进程仍在运行、端口未被占用（可换 `--port` 重试）。
- **压测请求大量失败**：检查 `--base-url`、API Key、`--timeout` 与并发设置，确认被测服务可达。
- **Native 模式启动被阻断**：执行 `pip install benchscope[accuracy-native]` 安装可选依赖后重试。
- **找不到某次历史任务**：确认数据根目录未被清理 / 未切换 `BENCHSCOPE_DATA_DIR`，或通过导入备份恢复。

更多问题排查请参考对应功能的「常见问题」小节，以及 [数据与统计（Datas）](/zh/docs/data/) 的备份 / 导入。

## 反馈 Bug / 提需求

欢迎到 GitHub 提交 **Issue**（Bug 报告、功能建议）与 **Pull Request**：

- 源码仓库：https://github.com/LABELNET/benchscope
- 文档仓库：https://github.com/harness-tech/harness-benchscope-docs
- 下载 / 发布：https://pypi.org/project/benchscope

## 参与贡献

了解本地开发环境、测试与贡献流程，见 [参与贡献](/zh/docs/help/contributing/)。

## 相关文档

- [快速开始](/zh/docs/quickstart/) — 从这里上手
- [安装](/zh/docs/install/) — 环境要求、更新与卸载
- [发布](/zh/docs/releases/) — 版本更新记录
