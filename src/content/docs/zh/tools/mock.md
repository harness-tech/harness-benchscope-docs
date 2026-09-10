---
title: "模拟调试环境（Mock）"
description: "无真实 vLLM / SGLang / GPU 时的完整联调环境：mock OpenAI 服务、FAKE bench 后端、mock bench CLI 与全量功能用例的模拟运行方法。"
---

# 模拟调试环境（Mock）

没有真实 vLLM / SGLang 服务或 GPU 时，BenchScope 提供一套**模拟调试环境**，可以完整跑通性能压测、精度评测与全部功能用例。本目录（`mocks/`）是唯一的 mock 来源，`tests/` 不包含 mock 代码。

## 环境组成

| 组件 | 文件 | 作用 |
| --- | --- | --- |
| mock OpenAI 推理服务 | `mocks/openai_server.py` | 模拟 OpenAI 兼容接口：`GET /v1/models`（4 个 mock 模型）+ `POST /v1/chat/completions`（支持 SSE 流式，先发 `reasoning_content` 思考增量再发正文）。 |
| 独立 mock bench CLI | `mocks/cli.py` | 冒充 `vllm bench serve` / `sglang.bench_serving`，打印与解析正则严格对齐的仿真输出。 |
| 仿真结果生成器 | `mocks/bench_outputs.py` | vLLM / SGLang 两种风格的 bench 结果仿真生成器。 |
| 一键启动脚本 | `mocks/run_mock.sh` | 启动 mock OpenAI 服务（默认 :8001）+ FAKE bench 后端（默认 :8080）。 |

mock OpenAI 服务提供的模型：`/data/disk3/DeepSeek-V4-Flash-0731-W8A8`、`Qwen2.5-72B-Instruct`、`mock-vllm-model`、`mock-sglang-model`。

## 环境变量

| 变量 | 作用 |
| --- | --- |
| `BENCHSCOPE_FAKE_BENCH` | 置 `1` 时，性能引擎不依赖真实 bench CLI，改用 `mocks/bench_outputs.py` 生成仿真输出（`mocks` 包不可导入时自动回退到内置简化仿真生成器，行为一致）。 |
| `BENCHSCOPE_DATA_DIR` | 覆盖数据根目录（默认 `~/.benchscope`），用于测试隔离，避免污染真实数据。 |

<div class="warning">

**warning**：

`BENCHSCOPE_FAKE_BENCH=1` 产生的指标是**仿真值**，仅用于链路联调与功能验证，**不能**作为真实性能数据引用。

</div>

## 一键启动联调环境

```bash
./mocks/run_mock.sh
# mock OpenAI server: http://127.0.0.1:8001
# benchscope 后端:    http://127.0.0.1:8080 （BENCHSCOPE_FAKE_BENCH=1）

# 另开终端启动前端（开发模式）
cd web && npm run dev   # http://127.0.0.1:5173
```

启动后：

1. **Settings → Providers**：Base URL 填 `http://127.0.0.1:8001`，点「测试连接」。
2. **Performance**：新建任务（vLLM 或 SGLang 引擎均可），FAKE 模式生成对应框架风格的仿真输出，实时表格与曲线照常更新。
3. **Sessions**：新建会话即可用 SSE 流式对话（先模拟一段「思考」增量再出正文）。

端口可通过环境变量覆盖：`OPENAI_PORT=9001 PORT=9000 ./mocks/run_mock.sh`；不需要对话功能时 `NO_OPENAI=1 ./mocks/run_mock.sh` 只启动后端。

## 独立使用各组件

### 1. mock OpenAI 推理服务

```bash
python -m mocks.openai_server --port 8001
```

### 2. 模拟 bench 输出

```bash
# vLLM 风格（参数与真实 vllm bench serve 相同）
python -m mocks.cli vllm bench serve --max-concurrency 32 --num-prompts 32 \
    --model Qwen2.5-72B-Instruct --random-input-len 3072 --random-output-len 1024

# SGLang 风格
python -m mocks.cli python -m sglang.bench_serving --max-concurrency 16 \
    --model Qwen2.5-72B-Instruct --random-input-len 1024 --random-output-len 1024

# 固定随机种子，结果可复现；保存到文件
python -m mocks.cli --framework sglang --max-concurrency 8 --seed 42 --save /tmp/mock_sglang.txt
```

### 3. 只跑 FAKE bench 后端

```bash
BENCHSCOPE_FAKE_BENCH=1 python -m benchscope.cli --port 8080 --no-browser
```

## CLI 模拟运行（perf / eval）

`benchscope perf` 的自研引擎直接对 **OpenAI 兼容端点**发起真实 HTTP 请求，因此可以指向 mock OpenAI 服务获得真实的延迟 / 吞吐指标（仿真服务端、真实压测链路）：

```bash
# 并发模式：对 mock 服务压测
python -m benchscope.cli perf --model mock-model --base-url http://127.0.0.1:8001 \
  --concurrency 4 --num-prompts 8 --input-len 64 --output-len 32

# 阈值模式：自动搜索最佳并发
python -m benchscope.cli perf --model mock-model --base-url http://127.0.0.1:8001 \
  --mode threshold --ttft-threshold-ms 500 --tpot-threshold-ms 100 \
  --max-concurrency-search 8 --num-prompts 4
```

精度评测可直接使用 `mock` 引擎（无需任何服务端），配合本地 JSONL 数据集即可跑通全链路：

```bash
python -m benchscope.cli eval --engine mock --model mock-model \
  --dataset /path/to/samples.jsonl --limit 20 --mock-correct-rate 0.7
```

## 模拟运行全量功能用例

`tests/run_tests.sh` 是一键入口：自动启动 mock OpenAI 服务 + 以「临时数据目录 + FAKE bench」启动被测服务，然后执行全部功能用例（API 180 项 + WebUI 51 项），结束后自动清理：

```bash
./tests/run_tests.sh              # 全量：API + WebUI
./tests/run_tests.sh --api-only   # 仅 API
./tests/run_tests.sh --ui-only    # 仅 WebUI（需 Playwright Chromium）
```

可覆盖端口与环境：`BS_TEST_PORT`（默认 18081）、`BS_MOCK_PORT`（默认 8001）、`BS_CHROMIUM_PATH`（Chromium 可执行文件路径）。

<div class="tip">

**tip**：

模拟运行全量用例是**文档与功能对齐**的常规手段：跑完 `tests/run_tests.sh` 与 CLI 模拟运行后，按实际输出核对文档中的参数、指标与行为描述，确保文档不落后于功能迭代。

</div>

## 常见问题

**问题：FAKE 模式的性能数据能用于报告吗？**
不能。FAKE 模式指标是仿真值，仅用于链路联调与功能验证；正式报告请使用真实服务压测数据。

**问题：mocks 包不可导入时会怎样？**
`BENCHSCOPE_FAKE_BENCH=1` 时自动回退到内置的简化仿真生成器，行为一致，不影响 pip 安装的独立环境。

**问题：为什么测试脚本要用临时数据目录？**
`BENCHSCOPE_DATA_DIR` 指向临时目录可避免测试污染 `~/.benchscope` 中的真实任务与会话数据。

## 相关文档

- [参与贡献](/zh/docs/help/contributing/) — 本地开发与测试
- [配置说明](/zh/docs/install/configuration/) — 数据目录与环境变量
- [内置技能](/zh/docs/tools/skills/) — 随包分发的维护技能
- [API 概述](/zh/docs/api/) — mock 服务提供的 OpenAI 兼容接口