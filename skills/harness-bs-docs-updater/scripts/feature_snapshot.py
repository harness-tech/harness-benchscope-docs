#!/usr/bin/env python3
"""
功能快照工具 — 生成/校验 benchscope 功能级快照（feature-snapshot.json）。

与 source-snapshot.json（文件指纹级）不同，功能快照记录项目**实际功能**：
  - CLI 命令与全部参数（含默认值，解析自 argparse）
  - 引擎（性能引擎 / 精度引擎，解析自 configs/benchs.yaml）
  - 数据集（解析自 configs/datasets.yaml，含判分器绑定与样本量）
  - 基线库（解析自 configs/baselines.yaml）
  - API 路由（解析自 benchscope/server/api_*.py）
  - WebUI 页面与路由（解析自 web/src/router/index.js）
  - 核心指标（性能 / 精度，指标定义来自 references/metrics-reference.md 口径）
  - 环境变量 / 数据目录 / mock 调试环境
  - 内置技能（benchscope/skills/*）
  - 已验证用例（模拟跑全部 case：pytest 套件 + CLI 模拟运行，结果经 --cases 注入）

用法：
  # 生成功能快照（可附验证用例结果）
  python scripts/feature_snapshot.py generate \
    --source /path/to/benchscope \
    --cases /tmp/cases.json \
    --output feature-snapshot.json

  # 覆盖度分析（功能快照 vs 文档站，输出未覆盖 / 部分覆盖清单）
  python scripts/feature_snapshot.py coverage \
    --snapshot feature-snapshot.json \
    --docs /path/to/docs-repo/src/content/docs

  # 校验快照落位（禁止落入项目归档目录 archives/）
  python scripts/feature_snapshot.py validate --path feature-snapshot.json

cases.json 结构（可选）：
  {
    "test_suite": {"total": 212, "passed": 211, "failed": 1, "failed_tests": ["tests/api/...::test_x"],
                    "environment": "...", "finished_at": "..."},
    "cli_runs": [
      {"name": "perf concurrency", "command": "benchscope perf ...", "status": "ok",
       "key_output": {"successful_requests": 8, "output_mean": 252.49, ...}}
    ]
  }
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
SNAPSHOT_PATH = SKILL_DIR / "feature-snapshot.json"

# ---------------------------------------------------------------------------
# 指标口径（定义与 references/metrics-reference.md 保持一致，单一事实来源）
# ---------------------------------------------------------------------------

PERF_METRIC_DEFS = {
    # 核心指标（每个并发点一组）
    "ttft": {
        "name_zh": "首 token 延迟 TTFT",
        "name_en": "Time To First Token (TTFT)",
        "unit": "ms",
        "stats": ["mean", "median", "p99"],
        "def_zh": "从请求发出到收到第一个生成 token 的耗时，反映用户感知的首字响应速度，越低越好。",
        "def_en": "Time from request send to the first generated token; reflects perceived first-token responsiveness, lower is better.",
    },
    "tpot": {
        "name_zh": "每输出 token 延迟 TPOT",
        "name_en": "Time Per Output Token (TPOT)",
        "unit": "ms",
        "stats": ["mean", "median", "p99"],
        "def_zh": "生成每个输出 token 的平均耗时，决定流式输出的持续流畅度，越低越好。",
        "def_en": "Average time to generate each output token; determines sustained streaming smoothness, lower is better.",
    },
    "itl": {
        "name_zh": "token 间隔延迟 ITL",
        "name_en": "Inter-Token Latency (ITL)",
        "unit": "ms",
        "stats": ["mean", "median", "p99"],
        "def_zh": "相邻两个输出 token 之间的间隔耗时，刻画流式输出的抖动与卡顿，越低越好。",
        "def_en": "Gap between consecutive output tokens; characterizes streaming jitter/stutter, lower is better.",
    },
    "output": {
        "name_zh": "输出吞吐",
        "name_en": "Output Throughput",
        "unit": "tok/s",
        "stats": ["mean"],
        "def_zh": "服务端生成的输出 token 速率（总输出 token 数 / 压测时长），越高越好。",
        "def_en": "Rate of generated output tokens (total output tokens / duration), higher is better.",
    },
    "peakoutput": {
        "name_zh": "峰值输出吞吐",
        "name_en": "Peak Output Throughput",
        "unit": "tok/s",
        "stats": ["mean"],
        "def_zh": "压测窗口内观察到的输出 token 速率峰值（vLLM 口径提供；SGLang 原生输出无此项时记 N/A）。",
        "def_en": "Peak output token rate observed in the window (vLLM provides it; recorded as N/A when the engine does not).",
    },
    "total": {
        "name_zh": "总 token 吞吐",
        "name_en": "Total Token Throughput",
        "unit": "tok/s",
        "stats": ["mean"],
        "def_zh": "输入 + 输出 token 的总处理速率（总 token 数 / 压测时长），衡量服务整体处理容量，越高越好。",
        "def_en": "Combined input + output token processing rate (total tokens / duration), measures overall capacity, higher is better.",
    },
    "req_per_s": {
        "name_zh": "请求吞吐",
        "name_en": "Request Throughput",
        "unit": "req/s",
        "stats": ["mean"],
        "def_zh": "每秒完成的请求数（成功请求数 / 压测时长），衡量服务承载的请求速率，越高越好。",
        "def_en": "Completed requests per second (successful requests / duration), higher is better.",
    },
    "single_user": {
        "name_zh": "单用户吞吐",
        "name_en": "Single-User Throughput",
        "unit": "tok/s",
        "stats": ["derived"],
        "def_zh": "单个用户可获得的生成速率，按 1000 / TPOT(mean) 推导，近似单人连续生成速度。",
        "def_en": "Generation rate available to a single user, derived as 1000 / TPOT(mean), approximating single-user speed.",
    },
    # 请求统计（每次运行一组）
    "successful_requests": {
        "name_zh": "成功请求数",
        "name_en": "Successful Requests",
        "unit": "count",
        "stats": ["scalar"],
        "def_zh": "压测中成功完成的请求数（收到完整响应）。",
        "def_en": "Requests that completed successfully with a full response.",
    },
    "failed_requests": {
        "name_zh": "失败请求数",
        "name_en": "Failed Requests",
        "unit": "count",
        "stats": ["scalar"],
        "def_zh": "压测中失败的请求数（超时 / 错误 / 未完成），健康压测中应为 0。",
        "def_en": "Requests that failed (timeout / error / incomplete); should be 0 in a healthy run.",
    },
    "benchmark_duration": {
        "name_zh": "压测时长",
        "name_en": "Benchmark Duration",
        "unit": "s",
        "stats": ["scalar"],
        "def_zh": "整轮压测的墙钟时长（从首个请求发出到全部请求结束）。",
        "def_en": "Wall-clock duration of the whole run (first request sent to last request finished).",
    },
    "total_input_tokens": {
        "name_zh": "总输入 token 数",
        "name_en": "Total Input Tokens",
        "unit": "tokens",
        "stats": ["scalar"],
        "def_zh": "本轮压测发送的全部输入 token 总量。",
        "def_en": "Total input tokens sent in this run.",
    },
    "total_generated_tokens": {
        "name_zh": "总输出 token 数",
        "name_en": "Total Generated Tokens",
        "unit": "tokens",
        "stats": ["scalar"],
        "def_zh": "本轮压测服务端生成的全部输出 token 总量。",
        "def_en": "Total output tokens generated by the service in this run.",
    },
    "peak_concurrent": {
        "name_zh": "峰值并发",
        "name_en": "Peak Concurrent Requests",
        "unit": "count",
        "stats": ["scalar"],
        "def_zh": "压测过程中同时在途的请求数峰值。",
        "def_en": "Peak number of in-flight requests during the run.",
    },
    # 阈值模式
    "best_concurrency": {
        "name_zh": "最佳并发",
        "name_en": "Best Concurrency",
        "unit": "count",
        "stats": ["derived"],
        "def_zh": "阈值模式下满足全部阈值条件（TTFT / TPOT / 输出吞吐）的最大并发；达到搜索上限仍满足时取上限。",
        "def_en": "In threshold mode, the maximum concurrency satisfying all thresholds (TTFT / TPOT / output throughput); the search cap is used when it still satisfies.",
    },
}

ACC_METRIC_DEFS = {
    "accuracy": {
        "name_zh": "正确率（核心主指标）",
        "name_en": "Accuracy (core metric)",
        "unit": "%",
        "stats": ["derived"],
        "def_zh": "正确样本数 / 总样本数，精度评测的核心主指标。",
        "def_en": "Correct samples / total samples; the core accuracy metric.",
    },
    "pass_rate": {
        "name_zh": "通过率",
        "name_en": "Pass Rate",
        "unit": "%",
        "stats": ["derived"],
        "def_zh": "有效可解析样本占比 =（总样本 - 无效样本）/ 总样本，衡量回答可被判分的比例。",
        "def_en": "Share of parseable samples = (total - invalid) / total; measures how many answers can be scored.",
    },
    "total_samples": {
        "name_zh": "总样本数",
        "name_en": "Total Samples",
        "unit": "count",
        "stats": ["scalar"],
        "def_zh": "本轮评测实际执行的样本总数。",
        "def_en": "Total samples actually evaluated.",
    },
    "correct_samples": {
        "name_zh": "正确样本数",
        "name_en": "Correct Samples",
        "unit": "count",
        "stats": ["scalar"],
        "def_zh": "判分结果为正确的样本数。",
        "def_en": "Samples judged correct.",
    },
    "wrong_samples": {
        "name_zh": "错误样本数",
        "name_en": "Wrong Samples",
        "unit": "count",
        "stats": ["scalar"],
        "def_zh": "可判分但结果错误的样本数。",
        "def_en": "Scorable samples judged wrong.",
    },
    "invalid_samples": {
        "name_zh": "无效样本数",
        "name_en": "Invalid Samples",
        "unit": "count",
        "stats": ["scalar"],
        "def_zh": "无法解析 / 无法判分的样本数（格式错误、未作答等）。",
        "def_en": "Samples that could not be parsed or scored.",
    },
    "subjects": {
        "name_zh": "分学科正确率",
        "name_en": "Per-Subject Accuracy",
        "unit": "%",
        "stats": ["per_subject"],
        "def_zh": "按数据集 subject 字段分组的逐学科正确率（subject 为空的样本不参与）。",
        "def_en": "Per-subject accuracy grouped by the dataset's subject field (samples without subject are excluded).",
    },
    "error_tag_summary": {
        "name_zh": "错因标签分布",
        "name_en": "Error-Tag Distribution",
        "unit": "count",
        "stats": ["per_tag"],
        "def_zh": "错误样本的归因标签计数（如「知识错误」），用于定位薄弱能力。",
        "def_en": "Counts of error-attribution tags on wrong samples (e.g. \"knowledge error\"), used to locate weak abilities.",
    },
    # 数学判分器
    "exact_match": {
        "name_zh": "精确匹配率",
        "name_en": "Exact Match",
        "unit": "%",
        "stats": ["derived"],
        "def_zh": "数学题最终答案与标准答案精确匹配的样本占比（math 判分器）。",
        "def_en": "Share of math samples whose final answer exactly matches the reference (math scorer).",
    },
    "math_accuracy": {
        "name_zh": "数学正确率",
        "name_en": "Math Accuracy",
        "unit": "%",
        "stats": ["derived"],
        "def_zh": "数学类数据集主指标，与 exact_match 同口径。",
        "def_en": "Primary metric for math datasets; same basis as exact_match.",
    },
    "answer_parse_rate": {
        "name_zh": "答案解析率",
        "name_en": "Answer Parse Rate",
        "unit": "%",
        "stats": ["derived"],
        "def_zh": "能从模型回答中提取出可判分答案的样本占比（math 判分器）。",
        "def_en": "Share of samples whose answer could be extracted for scoring (math scorer).",
    },
    # 代码判分器
    "pass_at_1": {
        "name_zh": "pass@1",
        "name_en": "pass@1",
        "unit": "%",
        "stats": ["derived"],
        "def_zh": "单次生成即通过全部测试用例的样本占比（code 判分器主指标）。",
        "def_en": "Share of samples whose single generation passes all test cases (code scorer primary metric).",
    },
    "compile_rate": {
        "name_zh": "编译通过率",
        "name_en": "Compile Rate",
        "unit": "%",
        "stats": ["derived"],
        "def_zh": "生成代码可成功编译 / 执行的样本占比（code 判分器）。",
        "def_en": "Share of generated code that compiles / executes (code scorer).",
    },
    "case_pass_rate": {
        "name_zh": "用例通过率",
        "name_en": "Case Pass Rate",
        "unit": "%",
        "stats": ["derived"],
        "def_zh": "全部样本的测试用例总体通过率（通过用例数 / 总用例数，code 判分器）。",
        "def_en": "Overall test-case pass rate across samples (passed cases / total cases, code scorer).",
    },
    # 评审判分器（MT-Bench）
    "mt_bench_score": {
        "name_zh": "MT-Bench 总分",
        "name_en": "MT-Bench Score",
        "unit": "0-10",
        "stats": ["derived"],
        "def_zh": "LLM 评审的两轮对话平均分（首轮均分 × 0.5 + 二轮均分 × 0.5，judge 判分器主指标）。",
        "def_en": "Average LLM-judge score over two dialogue turns (first × 0.5 + second × 0.5, judge scorer primary metric).",
    },
    "first_turn_score": {
        "name_zh": "首轮得分",
        "name_en": "First-Turn Score",
        "unit": "0-10",
        "stats": ["derived"],
        "def_zh": "MT-Bench 第一轮对话的评审平均分。",
        "def_en": "Average judge score for the first dialogue turn.",
    },
    "second_turn_score": {
        "name_zh": "二轮得分",
        "name_en": "Second-Turn Score",
        "unit": "0-10",
        "stats": ["derived"],
        "def_zh": "MT-Bench 第二轮对话的评审平均分（考察对首轮上下文的继承）。",
        "def_en": "Average judge score for the second turn (tests context inheritance from the first turn).",
    },
    "dim_helpfulness": {
        "name_zh": "有用性维度分",
        "name_en": "Helpfulness Dimension",
        "unit": "0-10",
        "stats": ["derived"],
        "def_zh": "评审的有用性（helpfulness）维度平均分。",
        "def_en": "Average judge score on the helpfulness dimension.",
    },
    "dim_truthfulness": {
        "name_zh": "真实性维度分",
        "name_en": "Truthfulness Dimension",
        "unit": "0-10",
        "stats": ["derived"],
        "def_zh": "评审的真实性（truthfulness）维度平均分。",
        "def_en": "Average judge score on the truthfulness dimension.",
    },
    "dim_harmlessness": {
        "name_zh": "无害性维度分",
        "name_en": "Harmlessness Dimension",
        "unit": "0-10",
        "stats": ["derived"],
        "def_zh": "评审的无害性（harmlessness）维度平均分。",
        "def_en": "Average judge score on the harmlessness dimension.",
    },
    # Token 统计（Serving 模式）
    "prompt_tokens_total": {
        "name_zh": "输入 token 总量",
        "name_en": "Prompt Tokens Total",
        "unit": "tokens",
        "stats": ["scalar"],
        "def_zh": "本轮评测全部请求的输入（prompt）token 总量（Serving 模式）。",
        "def_en": "Total prompt tokens across all requests (serving mode).",
    },
    "completion_tokens_total": {
        "name_zh": "输出 token 总量",
        "name_en": "Completion Tokens Total",
        "unit": "tokens",
        "stats": ["scalar"],
        "def_zh": "本轮评测全部响应的输出（completion）token 总量（Serving 模式）。",
        "def_en": "Total completion tokens across all responses (serving mode).",
    },
    "total_tokens": {
        "name_zh": "token 总量",
        "name_en": "Total Tokens",
        "unit": "tokens",
        "stats": ["derived"],
        "def_zh": "输入 + 输出 token 总量，用于成本核算。",
        "def_en": "Prompt + completion tokens; used for cost accounting.",
    },
    "avg_prompt_tokens_per_sample": {
        "name_zh": "单样本平均输入 token",
        "name_en": "Avg Prompt Tokens / Sample",
        "unit": "tokens",
        "stats": ["derived"],
        "def_zh": "输入 token 总量 / 总样本数。",
        "def_en": "Prompt tokens total / total samples.",
    },
    "avg_completion_tokens_per_sample": {
        "name_zh": "单样本平均输出 token",
        "name_en": "Avg Completion Tokens / Sample",
        "unit": "tokens",
        "stats": ["derived"],
        "def_zh": "输出 token 总量 / 总样本数。",
        "def_en": "Completion tokens total / total samples.",
    },
    # 基线对标
    "baseline_used": {
        "name_zh": "对标基线",
        "name_en": "Baseline Used",
        "unit": "-",
        "stats": ["field"],
        "def_zh": "参与对标的开源基线模型名（基线库中同尺寸段最优 / 指定模型）。",
        "def_en": "Open-source baseline model name used for comparison (best in the same size segment, or specified).",
    },
    "diff_pp": {
        "name_zh": "基线差值",
        "name_en": "Baseline Diff (pp)",
        "unit": "pp",
        "stats": ["derived"],
        "def_zh": "本次主指标得分与基线得分的差值（百分点），正数表示优于基线。",
        "def_en": "Difference between the primary score and the baseline (percentage points); positive means above baseline.",
    },
    "grade": {
        "name_zh": "档位评级",
        "name_en": "Grade",
        "unit": "S/A/B/C",
        "stats": ["derived"],
        "def_zh": "按与同尺寸段最优基线的差值评级：S ≥ 0；A ≥ -5；B ≥ -15；其余为 C。",
        "def_en": "Grade by diff vs the best same-size baseline: S ≥ 0; A ≥ -5; B ≥ -15; otherwise C.",
    },
    "conclusion": {
        "name_zh": "评测结论",
        "name_en": "Conclusion",
        "unit": "合格 / 精度下跌 / 异常",
        "stats": ["derived"],
        "def_zh": "最终结论三选一：总样本为 0 或无效占比 > 20% → 异常；主指标较基线下降 > 5pp → 精度下跌；否则 → 合格。",
        "def_en": "One of three: total = 0 or invalid ratio > 20% → abnormal; primary metric drops > 5pp vs baseline → accuracy drop; otherwise → pass.",
    },
    "estimate": {
        "name_zh": "Token 消耗预估",
        "name_en": "Token Estimate",
        "unit": "-",
        "stats": ["field"],
        "def_zh": "评测前的消耗预估：prompt/completion/total tokens、预计耗时 est_seconds、估算来源 source（内置样本均值 / 字符估算）。Native 模式恒为 0（无线上链路消耗）。",
        "def_en": "Pre-run cost estimate: prompt/completion/total tokens, est_seconds, source (builtin sample means / char heuristic). Native mode is always 0 (no serving link).",
    },
}

# ---------------------------------------------------------------------------
# 解析器
# ---------------------------------------------------------------------------


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _yaml_load(text: str) -> dict:
    try:
        import yaml
        data = yaml.safe_load(text)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def parse_version(source: Path) -> str:
    text = _read(source / "pyproject.toml")
    m = re.search(r'^version\s*=\s*"([^"]+)"', text, re.M)
    if m:
        return m.group(1)
    m = re.search(r"__version__\s*=\s*\"([^\"]+)\"", _read(source / "benchscope" / "__init__.py"))
    return m.group(1) if m else "unknown"


def parse_cli(source: Path) -> dict:
    """解析 benchscope/cli.py 的 argparse 定义（命令 + 参数 + 默认值）。"""
    text = _read(source / "benchscope" / "cli.py")
    commands: dict = {}

    # serve 参数（主 parser + serve 子 parser 共用 _add_serve_args）
    def extract_args_block(name: str) -> list:
        """提取 _add_<name>_args 函数内的 add_argument 调用。"""
        m = re.search(rf"def _add_{name}_args\(p: argparse\.ArgumentParser\)[^:]*:\n(.*?)(?=\n\ndef |\nmain\()", text, re.S)
        block = m.group(1) if m else ""
        args = []
        for am in re.finditer(r'p\.add_argument\(\s*((?:[^()]*|\([^()]*\))*)\)', block):
            raw = am.group(1)
            flags = re.findall(r'"--([a-z0-9-]+)"', raw)
            default = re.search(r'default\s*=\s*("([^"]*)"|\'([^\']*)\'|[\w.]+|None|true|false)', raw)
            has_default = "default=" in raw
            choices = re.search(r'choices\s*=\s*\[([^\]]*)\]', raw)
            req = "required=True" in raw
            action_flag = "action=" in raw
            dtype = re.search(r'type\s*=\s*(\w+)', raw)
            args.append({
                "flags": ["--" + f for f in flags],
                "default": (default.group(2) if default and default.group(2) is not None
                             else default.group(3) if default and default.group(3) is not None
                             else (default.group(0).split("=")[1].strip() if default else None)) if has_default else None,
                "choices": [c.strip().strip("\"'") for c in choices.group(1).split(",")] if choices else None,
                "required": req,
                "flag": action_flag,
                "type": dtype.group(1) if dtype else None,
            })
        return args

    serve_args = extract_args_block("serve")
    for a in serve_args:
        a["default"] = "0.0.0.0" if a["flags"] == ["--host"] else a["default"]
    commands["serve"] = {
        "usage": "benchscope serve [--host HOST] [--port PORT] [--no-browser] [--debug]",
        "args": serve_args + [
            {"flags": ["--debug"], "default": None, "choices": None, "required": False, "flag": True, "type": None},
        ],
        "behavior_zh": "启动 Web 服务（FastAPI + WebUI 统一入口）；无参数或首参为选项时同样进入 serve（向后兼容 benchscope --port 8080）。",
        "behavior_en": "Starts the web service (FastAPI + WebUI unified entry); also entered when no args or the first arg is an option (backward-compatible `benchscope --port 8080`).",
    }
    commands["perf"] = {
        "usage": "benchscope perf --model MODEL [options]",
        "args": extract_args_block("perf"),
        "behavior_zh": "执行一次自研引擎压测：concurrency（单并发）/ threshold（阈值搜索找最佳并发）；落盘 run.json + 终端日志。",
        "behavior_en": "Runs one built-in-engine benchmark: concurrency (single level) / threshold (search best concurrency); writes run.json + terminal log.",
    }
    commands["eval"] = {
        "usage": "benchscope eval --model MODEL --dataset DATASET [options]",
        "args": extract_args_block("eval"),
        "behavior_zh": "执行一次精度评测：serving / native 模式，引擎可选 benchscope / native-hf / mock；落盘 task.json / result.json / samples.jsonl。",
        "behavior_en": "Runs one accuracy evaluation: serving / native mode with engines benchscope / native-hf / mock; writes task.json / result.json / samples.jsonl.",
    }
    return {
        "entry": "benchscope",
        "compat_zh": "无参数或首参为选项（如 --port 8080）时等价于 benchscope serve。",
        "compat_en": "No args, or first arg is an option (e.g. --port 8080), is equivalent to `benchscope serve`.",
        "note_zh": "CLI 未提供 --version 选项；版本可经 Web 端 /api/version、Settings 页或 pip show benchscope 查看。",
        "note_en": "The CLI has no --version option; check the version via /api/version, the Settings page, or `pip show benchscope`.",
        "commands": commands,
    }


def parse_engines(source: Path) -> dict:
    data = _yaml_load(_read(source / "benchscope" / "configs" / "benchs.yaml"))
    engines = data.get("engines") or []
    comparison = data.get("comparison") or []
    perf, acc = [], []
    for e in engines:
        item = {
            "id": e.get("id"), "kind": e.get("kind"), "framework": e.get("framework"),
            "version": e.get("version"), "name": e.get("name"),
            "description_zh": e.get("description_zh"), "description_en": e.get("description"),
            "eval": e.get("eval"),
            "requires": e.get("requires") or [],
        }
        if e.get("kind") in ("vllm", "sglang", "builtin"):
            perf.append(item)
        else:
            acc.append(item)
    return {
        "performance": perf,
        "accuracy": acc,
        "comparison_dimensions": [
            {"dimension": c.get("dimension"), "dimension_zh": c.get("dimension_zh"), "values": c.get("values") or {}}
            for c in comparison
        ],
    }


def parse_datasets(source: Path) -> dict:
    data = _yaml_load(_read(source / "benchscope" / "configs" / "datasets.yaml"))
    items = []
    for d in data.get("datasets") or []:
        items.append({
            "id": d.get("id"), "name": d.get("name"), "category": d.get("category"),
            "description": d.get("description"),
            "eval": d.get("eval"),  # 含 scorer / metrics / total_samples（无 eval 表示性能数据集）
            "source": (d.get("source") or {}).get("type"),
        })
    return {
        "categories": data.get("categories") or [],
        "items": items,
        "perf_datasets": [i["id"] for i in items if not i.get("eval")],
        "eval_datasets": [i["id"] for i in items if i.get("eval")],
    }


def parse_baselines(source: Path) -> dict:
    data = _yaml_load(_read(source / "benchscope" / "configs" / "baselines.yaml"))
    return {
        "version": data.get("version"),
        "models": data.get("models") or [],
    }


def parse_api(source: Path) -> dict:
    """解析 server/api_*.py 的路由（含前缀）。"""
    groups: dict = {}
    api_dir = source / "benchscope" / "server"
    prefix_map = {
        "api_config": "/api/config", "api_tasks": "/api/tasks", "api_logs": "/api/logs",
        "api_dashboard": "/api/dashboard", "api_sessions": "/api/sessions",
        "api_test": "/api/test", "api_accuracy": "/api/accuracy",
        "api_benchs": "/api/benchs", "api_skills": "/api/skills",
    }
    for fname, prefix in prefix_map.items():
        text = _read(api_dir / f"{fname}.py")
        routes = []
        for m in re.finditer(r'@router\.(get|post|put|delete|patch)\(\s*"([^"]*)"', text):
            method, path = m.group(1).upper(), m.group(2)
            routes.append({"method": method, "path": prefix + path})
        groups[fname] = routes
    groups["_app"] = [
        {"method": "GET", "path": "/api/version"},
        {"method": "WS", "path": "/ws"},
    ]
    groups["_note_zh"] = ("BenchScope 本身不暴露 OpenAI 兼容的 /v1/* 端点；/v1/models 与 /v1/chat/completions "
                          "是被测服务（或 mocks/openai_server.py）的端点。会话 /api/sessions/{id}/chat 由服务端代理转发到激活的 Provider。")
    groups["_note_en"] = ("BenchScope itself does not expose OpenAI-compatible /v1/* endpoints; /v1/models and "
                          "/v1/chat/completions belong to the target service (or mocks/openai_server.py). "
                          "Session chat /api/sessions/{id}/chat is proxied server-side to the active provider.")
    return groups


def parse_webui(source: Path) -> dict:
    text = _read(source / "web" / "src" / "router" / "index.js")
    routes = []
    for m in re.finditer(r'\{\s*path:\s*"([^"]+)"[^}]*?(?:name:\s*"([^"]+)")?[^}]*', text):
        path = m.group(1)
        name = m.group(2) or ""
        routes.append({"path": path, "name": name})
    return {
        "routes": routes,
        "pages": [
            {"route": "/dashboard", "panels_zh": ["统计概览（性能/精度/会话/内置技能/模型/数据集计数 + Provider 整行）", "环境信息（硬件/操作系统/网络/框架版本）", "性能测试记录（最新 8 条）"],
             "notes_zh": "Eval Records（精度记录）面板当前隐藏（敬请期待）；Models/Datasets 下载计数暂未实现（默认 0）。"},
            {"route": "/performance", "panels_zh": ["任务列表 + 任务详情（指标表 + 4 组 12 图曲线 + 实时面板）", "创建任务三步表单（条件 / 参数 / 命令预览）"],
             "notes_zh": "曲线 4 组：吞吐（Output/Peak Output/Total）、TTFT（mean/median/p99）、TPOT（mean/median/p99）、ITL（mean/median/p99）。"},
            {"route": "/accuracy", "panels_zh": ["无任务时介绍页 + 创建入口", "任务列表 + 详情（指标 / 分学科 / 基线对标 / 样本）"],
             "notes_zh": "创建三步表单：数据集 / 模式与引擎 / 预览与 Token 强提醒确认。"},
            {"route": "/sessions", "panels_zh": ["会话列表 + SSE 流式对话（Markdown 渲染 + 代码高亮 + 思考解析 + 性能栏）"],
             "notes_zh": "会话请求由服务端代理到激活 Provider；支持 model / quality / enable_thinking / top_k / temperature / top_p。"},
            {"route": "/datas", "panels_zh": ["Perfs（性能记录：列表 + 详情 + 导入/备份/导出）", "Analysis（数据分析）"],
             "notes_zh": "Evals 子 Tab 已隐藏（路由 /datas/evals 重定向到 /datas/perfs）；精度评测产物仍在 Accuracy 页管理。"},
            {"route": "/settings", "panels_zh": ["General（Root Dir + Cache Paths）", "Providers（Provider 管理 + GPU 信息）", "Models", "Datasets", "Bench Engines（上传/导入/参数 YAML）", "Skills", "Plugins"],
             "notes_zh": "全部修改自动持久化到 ~/.benchscope/settings.json；Root Dir 即时生效无需重启。"},
        ],
    }


def parse_environment(source: Path) -> dict:
    const = _read(source / "benchscope" / "constants.py")
    config = _read(source / "benchscope" / "config.py")
    env_vars = sorted(set(re.findall(r"BENCHSCOPE_[A-Z_]+", const + config + _read(source / "benchscope" / "benches" / "runner.py") + _read(source / "benchscope" / "benches" / "builtin_bench.py"))))
    dirs = re.findall(r'"(\w+_dir)":\s*"(~/.benchscope[^"]*)"', const)
    return {
        "env_vars": env_vars,
        "env_var_notes": {
            "BENCHSCOPE_DATA_DIR": "数据根目录覆盖（默认 ~/.benchscope），用于测试隔离",
            "BENCHSCOPE_FAKE_BENCH": "置 1 时性能引擎使用仿真输出（mocks/bench_outputs.py，缺失时回退内置简化仿真），无需真实 bench CLI",
        },
        "data_dirs": dict(dirs),
        "data_root": "~/.benchscope",
        "config_file": "~/.benchscope/settings.json",
    }


def parse_builtin_skills(source: Path) -> list:
    skills_dir = source / "benchscope" / "skills"
    out = []
    if not skills_dir.is_dir():
        return out
    for d in sorted(skills_dir.iterdir()):
        if d.is_dir() and (d / "SKILL.md").exists():
            text = _read(d / "SKILL.md")
            m = re.search(r"^name:\s*(\S+)", text, re.M)
            desc = re.search(r"^description:?\s*(.+)$", text, re.M)
            out.append({"id": d.name, "name": m.group(1) if m else d.name,
                        "description": desc.group(1).strip() if desc else ""})
    return out


def parse_feature_flags(source: Path) -> list:
    """代码中显式隐藏的 UI 功能（隐藏 / 占位 / 未实现），文档必须如实标注。"""
    return [
        {"feature_zh": "Datas → Evals 子 Tab", "feature_en": "Datas → Evals sub-tab", "status": "hidden",
         "note_zh": "路由 /datas/evals 重定向到 /datas/perfs；精度评测产物在 Accuracy 页管理。", "note_en": "/datas/evals redirects to /datas/perfs; accuracy artifacts are managed on the Accuracy page."},
        {"feature_zh": "Dashboard → Eval Records（精度记录）面板", "feature_en": "Dashboard → Eval Records panel", "status": "hidden",
         "note_zh": "面板隐藏（敬请期待），前端保留数据接口。", "note_en": "Panel hidden (coming soon); data endpoints retained."},
        {"feature_zh": "Dashboard Models / Datasets 下载计数", "feature_en": "Dashboard Models / Datasets download counts", "status": "not_implemented",
         "note_zh": "计数恒为 0（暂未实现下载统计）。", "note_en": "Counts are always 0 (download stats not implemented yet)."},
    ]


def build_snapshot(source: Path, cases: dict | None) -> dict:
    source = source.resolve()
    if not (source / "benchscope").is_dir():
        print(f"Error: {source} does not look like a benchscope source tree", file=sys.stderr)
        sys.exit(1)
    perf_metrics = {
        "core_per_concurrency": ["ttft", "tpot", "itl", "output", "peakoutput", "total"],
        "request_stats": ["successful_requests", "failed_requests", "benchmark_duration",
                          "total_input_tokens", "total_generated_tokens", "peak_concurrent"],
        "request_throughput": ["req_per_s"],
        "derived": ["single_user"],
        "threshold": ["best_concurrency"],
        "definitions": PERF_METRIC_DEFS,
        "export": {
            "xlsx_columns": ["GPU", "模型", "精度", "推理框架", "输入长度", "输出长度", "并发数",
                             "Output", "Peak Output", "Total", "TTFT", "ITL", "TPOT", "单用户"],
            "xlsx_sheets": ["均值 Mean", "P99"],
            "csv_note_zh": "汇总 CSV 按用例分组，含「测试条件」标题行与 并发数/Output/Peak Output/Total/TTFT/TPOT/ITL 列（mean 或 P99 两套）。",
            "csv_note_en": "Summary CSV is grouped by case with a condition header row and columns concurrency/Output/Peak Output/Total/TTFT/TPOT/ITL (mean or P99 sets).",
        },
        "charts_layout": {
            "groups": [
                {"group_zh": "吞吐 Throughput", "unit": "tok/s", "cells": ["output_mean", "peakoutput_mean", "total_mean"]},
                {"group_zh": "TTFT", "unit": "ms", "cells": ["ttft_mean", "ttft_median", "ttft_p99"]},
                {"group_zh": "TPOT", "unit": "ms", "cells": ["tpot_mean", "tpot_median", "tpot_p99"]},
                {"group_zh": "ITL", "unit": "ms", "cells": ["itl_mean", "itl_median", "itl_p99"]},
            ],
        },
    }
    acc_metrics = {
        "core": ["accuracy", "pass_rate", "total_samples", "correct_samples", "wrong_samples", "invalid_samples"],
        "per_subject": ["subjects"],
        "attribution": ["error_tag_summary"],
        "per_scorer": {
            "choice": [],
            "math": ["exact_match", "math_accuracy", "answer_parse_rate"],
            "code": ["pass_at_1", "compile_rate", "case_pass_rate"],
            "judge": ["mt_bench_score", "first_turn_score", "second_turn_score",
                      "dim_helpfulness", "dim_truthfulness", "dim_harmlessness"],
        },
        "tokens_serving": ["prompt_tokens_total", "completion_tokens_total", "total_tokens",
                           "avg_prompt_tokens_per_sample", "avg_completion_tokens_per_sample"],
        "baseline": ["baseline_used", "diff_pp", "grade", "conclusion"],
        "grade_rules": [{"grade": "S", "diff_pp": ">= 0"}, {"grade": "A", "diff_pp": ">= -5"},
                        {"grade": "B", "diff_pp": ">= -15"}, {"grade": "C", "diff_pp": "< -15"}],
        "conclusion_rules": [
            {"value_zh": "异常", "value_en": "abnormal", "rule_zh": "总样本 = 0 或无效样本占比 > 20%", "rule_en": "total = 0 or invalid ratio > 20%"},
            {"value_zh": "精度下跌", "value_en": "accuracy drop", "rule_zh": "主指标较基线下降 > 5pp", "rule_en": "primary metric drops > 5pp vs baseline"},
            {"value_zh": "合格", "value_en": "pass", "rule_zh": "其余情况", "rule_en": "otherwise"},
        ],
        "radar_dimensions": ["知识", "数学", "代码", "对话", "综合"],
        "estimate": ["estimate"],
        "definitions": ACC_METRIC_DEFS,
        "artifacts": ["task.json", "result.json", "samples.jsonl"],
    }
    snap = {
        "snapshot_version": "2.0",
        "kind": "feature-snapshot",
        "project": "benchscope",
        "version": parse_version(source),
        "source_path": str(source),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "placement_rule_zh": "功能快照存放于技能目录 skills/harness-bs-docs-updater/，禁止放入项目归档目录 archives/。",
        "placement_rule_en": "Feature snapshots live under skills/harness-bs-docs-updater/; they must NOT be placed in the project archive directory archives/.",
        "verified_cases": cases or {},
        "cli": parse_cli(source),
        "engines": parse_engines(source),
        "datasets": parse_datasets(source),
        "baselines": parse_baselines(source),
        "api": parse_api(source),
        "webui": parse_webui(source),
        "metrics": {"performance": perf_metrics, "accuracy": acc_metrics},
        "environment": parse_environment(source),
        "built_in_skills": parse_builtin_skills(source),
        "feature_flags": parse_feature_flags(source),
        "mock_environment": {
            "components": {
                "mocks/openai_server.py": "mock OpenAI 兼容推理服务（/v1/models + /v1/chat/completions，SSE 流式含 reasoning 增量）",
                "mocks/cli.py": "独立 mock bench CLI（冒充 vllm bench serve / sglang.bench_serving，输出与 parser 正则对齐）",
                "mocks/bench_outputs.py": "vLLM / SGLang 两种 bench 结果的仿真生成器",
                "mocks/run_mock.sh": "一键启动 mock 调试环境（mock OpenAI :8001 + FAKE bench 后端 :8080）",
            },
            "models": ["/data/disk3/DeepSeek-V4-Flash-0731-W8A8", "Qwen2.5-72B-Instruct",
                       "mock-vllm-model", "mock-sglang-model"],
            "usage_zh": "无真实 vLLM/SGLang/GPU 时：./mocks/run_mock.sh 启动联调环境；或 BENCHSCOPE_FAKE_BENCH=1 benchscope serve；全量功能用例：./tests/run_tests.sh（mock OpenAI + 临时数据目录 + FAKE bench，API 212 项 + WebUI 用例）。",
            "usage_en": "Without real vLLM/SGLang/GPU: run ./mocks/run_mock.sh for a debug env; or BENCHSCOPE_FAKE_BENCH=1 benchscope serve; full feature cases: ./tests/run_tests.sh (mock OpenAI + temp data dir + FAKE bench; 212 API + WebUI cases).",
        },
    }
    return snap


# ---------------------------------------------------------------------------
# 覆盖度分析
# ---------------------------------------------------------------------------


def collect_doc_text(docs_root: Path) -> dict:
    langs = {}
    for lang in ("zh", "en"):
        parts = []
        lang_dir = docs_root / lang
        if lang_dir.is_dir():
            for f in sorted(lang_dir.rglob("*.md")):
                parts.append(f.read_text(encoding="utf-8"))
        langs[lang] = "\n".join(parts)
    return langs


def coverage_report(snap: dict, docs_root: Path) -> dict:
    docs = collect_doc_text(docs_root)
    gaps = {"zh": [], "en": []}
    checks_per_lang = {"zh": 0, "en": 0}

    def check(token: str, label: str, category: str):
        for lang in ("zh", "en"):
            checks_per_lang[lang] += 1
            if token not in docs[lang]:
                gaps[lang].append({"token": token, "label": label, "category": category})

    # 指标（核心指标必须 100% 覆盖：指标 key 出现在文档中）
    for scope, mdefs in (("performance", PERF_METRIC_DEFS), ("accuracy", ACC_METRIC_DEFS)):
        for key, d in mdefs.items():
            check(key, f"{scope}:{d.get('name_zh', key)}", "metric")
    # CLI 参数
    for cmd, info in (snap.get("cli", {}).get("commands") or {}).items():
        for a in info.get("args") or []:
            for fl in a.get("flags") or []:
                check(fl, f"cli:{cmd}:{fl}", "cli-arg")
    # 引擎
    for e in (snap.get("engines", {}).get("performance") or []) + (snap.get("engines", {}).get("accuracy") or []):
        check(e["id"], f"engine:{e.get('name', e['id'])}", "engine")
    # 数据集
    for d in snap.get("datasets", {}).get("items") or []:
        check(d["id"], f"dataset:{d.get('name', d['id'])}", "dataset")
    # WebUI 页面
    for p in snap.get("webui", {}).get("pages") or []:
        check(p["route"], f"page:{p['route']}", "webui-page")
    # API 分组（按前缀覆盖即可，逐路由过严）
    for group in snap.get("api", {}):
        if group.startswith("_"):
            continue
        check(f"/api/{group.replace('api_', '')}", f"api-group:{group}", "api-group")

    total = sum(len(v) for v in gaps.values())
    cov_zh = 1.0 - len(gaps["zh"]) / max(1, checks_per_lang["zh"])
    cov_en = 1.0 - len(gaps["en"]) / max(1, checks_per_lang["en"])
    return {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "docs_root": str(docs_root),
        "checks": checks_per_lang,
        "gaps": gaps,
        "total_gaps": total,
        "coverage_zh": round(cov_zh, 4),
        "coverage_en": round(cov_en, 4),
        "pass": total == 0,
    }


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="BenchScope feature snapshot tool")
    sub = parser.add_subparsers(dest="command")

    gen = sub.add_parser("generate", help="Generate feature snapshot")
    gen.add_argument("--source", required=True, help="Local benchscope source path")
    gen.add_argument("--cases", help="Optional JSON with verified case results (test suite + CLI runs)")
    gen.add_argument("--output", default=str(SNAPSHOT_PATH), help="Output snapshot path")

    cov = sub.add_parser("coverage", help="Coverage report: feature snapshot vs docs")
    cov.add_argument("--snapshot", default=str(SNAPSHOT_PATH), help="Feature snapshot path")
    cov.add_argument("--docs", required=True, help="Docs content root (contains zh/ and en/)")
    cov.add_argument("--output", help="Optional JSON output path")

    val = sub.add_parser("validate", help="Validate snapshot placement (not under archives/)")
    val.add_argument("--path", required=True, help="Snapshot file path")

    args = parser.parse_args()

    if args.command == "generate":
        source = Path(args.source)
        cases = None
        if args.cases and Path(args.cases).exists():
            cases = json.loads(Path(args.cases).read_text(encoding="utf-8"))
        snap = build_snapshot(source, cases)
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(snap, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"✅ Feature snapshot saved: {out}")
        print(f"   version={snap['version']} engines={len(snap['engines']['performance']) + len(snap['engines']['accuracy'])} "
              f"datasets={len(snap['datasets']['items'])} api_groups={len([g for g in snap['api'] if not g.startswith('_')])}")

    elif args.command == "coverage":
        snap = json.loads(Path(args.snapshot).read_text(encoding="utf-8"))
        report = coverage_report(snap, Path(args.docs))
        text = json.dumps(report, indent=2, ensure_ascii=False)
        if args.output:
            Path(args.output).write_text(text, encoding="utf-8")
            print(f"✅ Coverage report saved: {args.output}")
        print(text)
        if not report["pass"]:
            print(f"\n⚠️  {report['total_gaps']} gaps (zh={len(report['gaps']['zh'])}, en={len(report['gaps']['en'])})")
            sys.exit(2)

    elif args.command == "validate":
        p = Path(args.path).resolve()
        if "archives" in p.parts:
            print(f"❌ Snapshot must NOT be placed under archives/: {p}")
            sys.exit(1)
        print(f"✅ Placement OK: {p}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()