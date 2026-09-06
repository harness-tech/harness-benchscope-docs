---
title: "参与贡献"
---

# 参与贡献

欢迎通过 **Issue / PR** 参与 BenchScope 开源贡献。无论是修复 Bug、新增功能、完善文档，还是补充测试，都非常欢迎。

## 相关链接

- 源码仓库：https://github.com/LABELNET/benchscope
- 下载 / 发布：https://pypi.org/project/benchscope
- 许可证：Apache License 2.0

<div class="info">

**info**：

在提交前请先阅读仓库根目录的说明文档：`docs/Readme.md`（文档体系）与 `agents/Readme.md`（项目级维护约定）。

</div>

## 本地开发环境

仓库根目录说明如下：

| 文件 | 说明 |
| --- | --- |
| `docs/Readme.md` | 文档体系与规划 |
| `agents/Readme.md` | 项目级维护约定 |

开发时请遵循以下规则：

- **文档同步**：开发 / 更新功能必须**同步更新对应文档**（`docs/prds/`、`docs/versions/`、`docs/rules/` 等）；
- **测试**：提交前运行 `tests/` 测试套件；
- **最小改动**：保持改动聚焦，遵循仓库命名与 i18n 约定。

## 测试

运行测试套件：

```bash
pytest
```

<div class="tip">

**tip**：

提交 PR 前请确保相关测试全部通过，并在有新增功能时补充相应测试用例。

</div>

## 贡献流程

1. **Fork** 仓库并创建特性分支；
2. 编写 / 调整功能，并**补充测试与文档**；
3. 运行测试确认通过；
4. 提交 **PR**，说明变更与测试结果。

### 检查清单

- [ ] 代码风格与命名符合仓库约定
- [ ] 新增 / 修改功能已同步文档
- [ ] 相关测试覆盖并通过（`pytest`）
- [ ] 国际化（i18n）文案已更新

## 相关文档

- [架构介绍](/zh/docs/tools/architecture/) — 了解代码结构
- [Bench 引擎](/zh/docs/tools/bench-engine/) — 引擎抽象与自定义
- [快速入门](/zh/docs/quickstart/) — 安装使用
