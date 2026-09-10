---
title: "Sessions"
description: "Sessions: SSE-streaming interactive chat with sampling parameters, Markdown rendering, reasoning parsing, and a performance bar."
---

# Sessions

Sessions provides a **session-based interactive experience**: configure sampling parameters, send messages and watch the **SSE streaming output** in real time, with Markdown rendering + code highlighting, reasoning parsing, and a performance bar, so you can talk to a large model directly, just like using a chat tool.

![BenchScope Sessions interface](/images/benchscope_sessions.png)

<div class="tip">

**Tip**:

Sessions is different from stress / evaluation runs — the former is **interactive conversation**, the latter is **batch load / batch evaluation**. You can first use sessions to validate a model's answer quality, then run the formal stress tests and evaluations.

</div>

## Main Capabilities

- **Sampling parameters**: start a session request after configuring generation parameters (`temperature` / `top_p` / `top_k` / `quality`, etc.).
- **Thinking switch**: `enable_thinking` controls the model's thinking process (passed via `chat_template_kwargs` for vLLM / SGLang).
- **Markdown rendering**: output supports Markdown rendering and code syntax highlighting (highlight.js + dark theme).
- **SSE streaming**: streaming output is presented in real time, including parsing of the thinking process (`reasoning_content` increments).
- **Session management**: session items in the sidebar, switch / rename, per-session log persistence, and a centered confirmation dialog for clearing.
- **Performance bar**: shows the performance information of the current request (e.g., elapsed time, Tokens, etc.).

<div class="info">

**Info**:

Session requests are **proxied** by the server to the currently active Provider (an OpenAI-compatible endpoint) — BenchScope itself does not expose `/v1/*` endpoints. The session feature therefore depends on the inference service configured in Settings → Providers being available; without a real service, you can use the mock OpenAI service in the [Mock Debug Environment](/en/docs/tools/mock/) for integration debugging.

</div>

## Usage Workflow

1. **Create a new session** on the **Sessions** page;
2. Configure the **sampling parameters** (`temperature` / `top_p`, etc.);
3. **Send a message**, watching the streaming output and thinking process in real time;
4. Sessions are **cached automatically**; they can be **renamed** or **exported** per session.

### Sampling Parameters

| Parameter | Description |
| --- | --- |
| `model` | Model name used by the session (falls back to the session's selected model by default) |
| `temperature` | Sampling temperature (0–2); higher = more random output; takes precedence over `quality` when set explicitly |
| `quality` | Quality tier: high (0.9) / medium (0.5) / low (0.2); mapped to a temperature value when `temperature` is not set explicitly |
| `top_k` | Top-K sampling; keeps only the top K candidate tokens by probability |
| `top_p` | Nucleus sampling probability; samples within the cumulative probability threshold |
| `enable_thinking` | Thinking switch; controls the model's thinking process (passed via `chat_template_kwargs` for vLLM / SGLang) |
| `provider_id` | The Provider the session request is proxied to (defaults to the active Provider) |

> `max_tokens` for a single reply is fixed at 4096 on the server side and is not exposed as a session parameter.

<div class="info">

**Info**:

The session's sampling parameters are aligned with the sampling parameters of `eval` in the [CLI](/en/docs/cli/) (`temperature` / `top_p` / `max-tokens`, etc.), making it easy to keep consistent generation settings across sessions, stress tests, and evaluations.

</div>

## UI Layout

**Sidebar**:

- Session list, supporting switching and **renaming**;
- Each session's log is **persisted independently**;
- The clear action comes with a **centered confirmation dialog** to prevent misoperation.

**Main area**:

- Streaming output area (SSE), with Markdown rendering and code highlighting;
- Parsing display of the thinking process (reasoning);
- A performance bar at the bottom shows the performance information of the current request.

## FAQ

**Question: The output is not scrolling live?**

Confirm the session uses SSE streaming output; if there is a proxy at the network layer, the SSE long-lived connection may be interrupted; check the server logs.

**Question: How do I export a session?**

Select the session in the sidebar and use the export / persist actions. Session caches are stored in the `sessions` subdirectory of the data root (default `~/.benchscope/sessions/`); see [Configuration](/en/docs/install/configuration/) (`sessions_dir`).

## Related docs

- [Configuration](/en/docs/install/configuration/) — session cache directory `sessions_dir`
- [Settings](/en/docs/tools/settings/) — Provider configuration driving session requests
- [Mock Debug Environment](/en/docs/tools/mock/) — debug the session feature without a real service
- [Performance Testing](/en/docs/performance/) — formal stress testing of a model
- [Accuracy Testing](/en/docs/accuracy/) — quantitative evaluation of a model