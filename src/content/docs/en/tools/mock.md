---
title: "Mock Debug Environment"
description: "A complete integration-debugging environment without a real vLLM / SGLang / GPU: mock OpenAI service, FAKE bench backend, mock bench CLI, and how to run the full feature test cases in simulation."
---

# Mock Debug Environment

Without a real vLLM / SGLang service or GPU, BenchScope provides a **mock debugging environment** in which performance stress tests, accuracy evaluations, and all feature test cases run end to end. This directory (`mocks/`) is the only source of mocks; `tests/` contains no mock code.

## Environment Composition

| Component | File | Role |
| --- | --- | --- |
| mock OpenAI inference service | `mocks/openai_server.py` | Simulates the OpenAI-compatible API: `GET /v1/models` (4 mock models) + `POST /v1/chat/completions` (supports SSE streaming; sends `reasoning_content` thinking increments before the body). |
| Standalone mock bench CLI | `mocks/cli.py` | Impersonates `vllm bench serve` / `sglang.bench_serving`, printing simulated output strictly aligned with the parsing regexes. |
| Simulated result generator | `mocks/bench_outputs.py` | Bench result simulation generators in the two styles of vLLM / SGLang. |
| One-click startup script | `mocks/run_mock.sh` | Starts the mock OpenAI service (default :8001) + FAKE bench backend (default :8080). |

Models provided by the mock OpenAI service: `/data/disk3/DeepSeek-V4-Flash-0731-W8A8`, `Qwen2.5-72B-Instruct`, `mock-vllm-model`, `mock-sglang-model`.

## Environment Variables

| Variable | Role |
| --- | --- |
| `BENCHSCOPE_FAKE_BENCH` | When set to `1`, the performance engine no longer depends on a real bench CLI and instead uses `mocks/bench_outputs.py` to generate simulated output (automatically falls back to a built-in simplified simulation generator when the `mocks` package is not importable, with identical behavior). |
| `BENCHSCOPE_DATA_DIR` | Overrides the data root directory (default `~/.benchscope`), for test isolation to avoid polluting real data. |

<div class="warning">

**Warning**:

Metrics produced by `BENCHSCOPE_FAKE_BENCH=1` are **simulated values**, used only for pipeline integration debugging and feature validation; they **must not** be cited as real performance data.

</div>

## One-Click Startup of the Integration-Debugging Environment

```bash
./mocks/run_mock.sh
# mock OpenAI server: http://127.0.0.1:8001
# benchscope backend:    http://127.0.0.1:8080 (BENCHSCOPE_FAKE_BENCH=1)

# In another terminal, start the frontend (dev mode)
cd web && npm run dev   # http://127.0.0.1:5173
```

After startup:

1. **Settings → Providers**: fill in `http://127.0.0.1:8001` as the Base URL and click "Test Connection".
2. **Performance**: create a new task (either the vLLM or the SGLang engine works); FAKE mode generates simulated output in the corresponding framework's style, and the real-time tables and curves update as usual.
3. **Sessions**: create a new session to have an SSE-streaming conversation (it first simulates a stretch of "thinking" increments before the body appears).

Ports can be overridden via environment variables: `OPENAI_PORT=9001 PORT=9000 ./mocks/run_mock.sh`; when the conversation feature is not needed, `NO_OPENAI=1 ./mocks/run_mock.sh` starts only the backend.

## Using Components Individually

### 1. mock OpenAI inference service

```bash
python -m mocks.openai_server --port 8001
```

### 2. Simulated bench output

```bash
# vLLM style (same arguments as the real vllm bench serve)
python -m mocks.cli vllm bench serve --max-concurrency 32 --num-prompts 32 \
    --model Qwen2.5-72B-Instruct --random-input-len 3072 --random-output-len 1024

# SGLang style
python -m mocks.cli python -m sglang.bench_serving --max-concurrency 16 \
    --model Qwen2.5-72B-Instruct --random-input-len 1024 --random-output-len 1024

# Fixed random seed for reproducible results; save to a file
python -m mocks.cli --framework sglang --max-concurrency 8 --seed 42 --save /tmp/mock_sglang.txt
```

### 3. Run only the FAKE bench backend

```bash
BENCHSCOPE_FAKE_BENCH=1 python -m benchscope.cli --port 8080 --no-browser
```

## CLI Simulation Runs (perf / eval)

The self-developed engine of `benchscope perf` sends real HTTP requests directly to **OpenAI-compatible endpoints**, so pointing it at the mock OpenAI service still yields real latency / throughput metrics (simulated server side, real stress-test pipeline):

```bash
# Concurrency mode: stress-test the mock service
python -m benchscope.cli perf --model mock-model --base-url http://127.0.0.1:8001 \
  --concurrency 4 --num-prompts 8 --input-len 64 --output-len 32

# Threshold mode: automatically search for the best concurrency
python -m benchscope.cli perf --model mock-model --base-url http://127.0.0.1:8001 \
  --mode threshold --ttft-threshold-ms 500 --tpot-threshold-ms 100 \
  --max-concurrency-search 8 --num-prompts 4
```

For accuracy evaluation, the `mock` engine works directly (no server side required); combined with a local JSONL dataset, it runs the full pipeline:

```bash
python -m benchscope.cli eval --engine mock --model mock-model \
  --dataset /path/to/samples.jsonl --limit 20 --mock-correct-rate 0.7
```

## Running the Full Feature Test Cases in Simulation

`tests/run_tests.sh` is the one-click entry point: it automatically starts the mock OpenAI service, launches the service under test with a "temporary data directory + FAKE bench", runs all feature test cases (180 API items + 51 WebUI items), and cleans up automatically afterward:

```bash
./tests/run_tests.sh              # Full: API + WebUI
./tests/run_tests.sh --api-only   # API only
./tests/run_tests.sh --ui-only    # WebUI only (requires Playwright Chromium)
```

Ports and environment can be overridden: `BS_TEST_PORT` (default 18081), `BS_MOCK_PORT` (default 8001), `BS_CHROMIUM_PATH` (path to the Chromium executable).

<div class="tip">

**Tip**:

Running the full test cases in simulation is a routine means of **keeping docs aligned with features**: after running `tests/run_tests.sh` and the CLI simulation runs, cross-check the parameters, metrics, and behavior descriptions in the docs against the actual output, ensuring the docs do not lag behind feature iterations.

</div>

## FAQ

**Question: Can the performance data from FAKE mode be used in reports?**

No. FAKE-mode metrics are simulated values, used only for pipeline integration debugging and feature validation; use real-service stress-test data for formal reports.

**Question: What happens when the mocks package is not importable?**

When `BENCHSCOPE_FAKE_BENCH=1`, it automatically falls back to the built-in simplified simulation generator with identical behavior, without affecting standalone environments installed via pip.

**Question: Why do the test scripts use a temporary data directory?**

Pointing `BENCHSCOPE_DATA_DIR` at a temporary directory avoids tests polluting the real task and session data in `~/.benchscope`.

## Related docs

- [Contributing](/en/docs/help/contributing/) — local development and testing
- [Configuration](/en/docs/install/configuration/) — data directories and environment variables
- [Built-in Skills](/en/docs/tools/skills/) — maintenance skills shipped with the package
- [API Overview](/en/docs/api/) — the OpenAI-compatible endpoints provided by the mock service