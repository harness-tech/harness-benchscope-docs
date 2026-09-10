---
title: Streaming Chat
description: "Guide to streaming chat in the Sessions module: SSE streaming output, Token statistics, and generated files, including the backend proxying logic and the SSE event protocol."
---

# Streaming Chat

This page explains how to send a message on the Sessions page, watch the **SSE streaming output**, track Token metrics, and see the files produced by a running session, and describes the backend proxying and data flow that happen after you click **Send**.

## 1. Features

- Type a message in the input box and press Enter or click the send button; the model reply is rendered **token by token over SSE**, with **Markdown rendering** and code highlighting (code blocks carry a language tag and a Copy button).
- The model's reasoning is shown in a **Thinking** collapsible block (`reasoning_content` increments or think-tag parsing).
- The performance bar in the session header tracks **Token metrics** in real time (TTFT, tok/s, TPOT, ITL, etc.).
- Shift+Enter inserts a newline; during streaming you can click the stop button to abort (content already generated is kept).

## 2. Page Structure

The streaming chat UI consists of the **message area** and the **bottom input bar**:

```
+----------------------------------------------------------------------+
| Perf bar turns/steps | LLM | TTFT | TPOT | ITL + top_k/temp/top_p    |
+----------------------------------------------------------------------+
| Message area: U user bubble (right) / AI assistant bubble (left)     |
|   [Thinking v] thinking block (collapsed by default,                 |
|    rolling dots while streaming)                                     |
|   Reply body (Markdown + code highlight + Copy) +                    |
|    blinking caret on the streaming line                              |
+----------------------------------------------------------------------+
| Input box (Enter to send / Shift+Enter for new line,                 |
|  disabled while streaming)                                           |
| Provider v  Select Model v  Quality v  Thinking [x]  (send/stop)     |
+----------------------------------------------------------------------+
```

- **Message area**: user messages on the right (avatar `U`), assistant messages on the left (avatar is the blue logo); the thinking block can be clicked to expand/collapse.
- **Input bar**: the input box is disabled while streaming; the send button becomes a **stop** square — click it to abort the current stream.

## 3. Input Parameters

Request body fields of the send-message API (`POST /api/sessions/{session_id}/chat`):

| Field | Type | Constraint | Default | Description |
| --- | --- | --- | --- | --- |
| `message` | string | non-empty | — | The user message for this turn |
| `model` | string | within the Provider's model list | the session's selected model | Inference model name |
| `quality` | string | enum: `high` / `medium` / `low` | the session's saved value | Quality preset, mapping to temperature 0.9 / 0.5 / 0.2 |
| `enable_thinking` | boolean | true / false | true | Thinking switch |
| `provider_id` | string | valid Provider id | the session's saved value | Target Provider to proxy to |
| `top_k` | int | 1 - 200 | 10 | Top-K sampling |
| `temperature` | number | 0 - 2 | 0.5 | Sampling temperature; takes precedence over `quality` when passed explicitly |
| `top_p` | float | 0 - 1 | 1.0 | Nucleus sampling threshold |

<div class="warning">
**Warning:** `max_tokens` is **fixed at 4096** and is not exposed as a session parameter. The server always writes `"max_tokens": 4096` into the proxied payload.
</div>

## 4. Field Constraints

| Field | Required | Type | Min | Max | Enum | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `message` | Yes | string | 1 | — | — | Empty messages cannot be sent from the frontend |
| `model` | No | string | — | — | Provider model list | Falls back to the session's selected model, then to `default` |
| `quality` | No | string | — | — | high / medium / low | The mapping only takes effect when `temperature` is missing |
| `enable_thinking` | No | boolean | — | — | true / false | Passed via `chat_template_kwargs` |
| `provider_id` | No | string | — | — | configured Provider ids | Falls back to the active Provider's global `api` config when missing or unknown |
| `top_k` | No | int | 1 | 200 | — | Not written into the proxied payload when ≤ 0 |
| `temperature` | No | number | 0 | 2 | — | Overrides the `quality` mapping when passed explicitly |
| `top_p` | No | float | 0 | 1 | — | Not written into the proxied payload when missing |
| `max_tokens` | — | int | — | — | — | Fixed at 4096, not configurable |

## 5. Execution Steps (Button Operations)

1. Click a session in the **Chats** list (or create one first, see [Create Session](/en/docs/manual/sessions/create-session/)).
2. In the bottom input bar, confirm that **Provider**, **Select Model**, **Quality**, and the **Thinking** switch are as expected.
3. Click the input box and type a message; press **Shift+Enter** to insert a newline (i18n `newline`).
4. Press **Enter** (i18n `send`) or click the **send** button on the right to start the streaming chat.
5. While streaming:
    - the **Thinking** collapsible block shows the reasoning content live (click to expand);
    - the reply body is appended token by token; when a code block completes, its language tag and Copy button appear;
    - the session item icon in the left sidebar becomes a **rolling-dots** animation and the performance bar refreshes in real time.
6. To abort: click the **stop** square (the send button's streaming state); the partially generated content is kept in the session.
7. After sending completes, the performance bar records this turn's metrics and the session is persisted automatically.

## 6. Backend Execution Logic

After you click send, the following flow happens in the backend (data flow: browser → BenchScope server → active Provider):

1. The frontend `fetch`es `POST /api/sessions/{session_id}/chat` (body in section 3) and reads the SSE stream as `text/event-stream`.
2. The server's `api_sessions.chat()` validates that the session exists (returns 404 "Session not found" if not) and enters `SessionManager.stream_chat()`:
    - resolve the model: `model` → the session's selected model → `default`;
    - persist the config: the session's `model` / `provider_id` / `quality` / `enable_thinking`;
    - write the user message (`add_message`), refreshing `~/.benchscope/sessions/<session_id>.json` and the session log; the first message triggers the automatic session-title update.
3. Resolve the Provider API config: fetch `base_url` / `endpoint` / `api_key` / `extra_headers` from the Provider list by `provider_id`; **when missing or unknown, fall back to the global `api` config (i.e., the active Provider)**.
4. Assemble the proxied payload: `model`, `messages` (`system_prompt` prepended + all history), `stream: true`, **`max_tokens: 4096`** (fixed), `temperature` (explicit value or the `quality` mapping: high=0.9 / medium=0.5 / low=0.2), `top_k` (when > 0), `top_p`, `chat_template_kwargs: {enable_thinking}`.
5. The server issues a `POST` to `{base_url}{endpoint}` (default `/v1/chat/completions`) (`Authorization: Bearer <api_key>`, timeout 120s) and **streams the Provider's SSE response through as a proxy**.
6. Parse the Provider SSE line by line (`data: {...}`): `choices[0].delta.content` → `token` event; `delta.reasoning_content` or the think-tag parse result → `thinking` event; end on `data: [DONE]`; when finished, persist the assistant reply and emit a `done` event.

SSE event protocol (all JSON after `data:`):

| Event | Example | Description |
| --- | --- | --- |
| `token` | `data: {"token": "hi"}` | Reply body increment |
| `thinking` | `data: {"thinking": "let me think..."}` | Reasoning increment |
| `error` | `data: {"error": "API error: 500 ..."}` | Error message (non-200 or request exception) |
| `done` | `data: {"done": true}` | This generation finished |

<div class="info">
**Info:** BenchScope does **not** expose an OpenAI-compatible `/v1/*` inference endpoint. Chat requests are **proxied** by the server to the active Provider (an OpenAI-compatible endpoint): when `provider_id` is missing or unknown, the global `api` config (synced from the active Provider) is used; otherwise the request is forwarded to the specified Provider's `base_url + endpoint`.
</div>

## 7. Token Statistics

The performance bar metrics are computed by the **frontend client** while receiving the SSE stream (live values during streaming) and persisted to the session via `PATCH /api/sessions/{session_id}/perf` after sending completes; they are restored when the session is reopened:

| Metric | Meaning | How it's computed |
| --- | --- | --- |
| `turns` | Conversation turns | Number of user messages |
| `steps` | Message steps | Total user + assistant messages |
| `llmTime` | Total time for this request | completion time − send time |
| `ttft` | Time to first token | first `token` event time − send time |
| `tokPerSec` | Decode rate | token count ÷ (completion time − first token time) |
| `tpot` | Average time per token | (completion time − first token time) ÷ token count |
| `itl` | Average token interval | Σ(inter-token time deltas) ÷ (token count − 1) |

## 8. Generated Files

A running session produces the following files (the Sessions module marks session artifacts with the `produced` label):

| File | Path | Description |
| --- | --- | --- |
| Session state | `~/.benchscope/sessions/<session_id>.json` | Complete session data (messages, config, perf), refreshed on every message change |
| Session log | `~/.benchscope/logs/sessions/<session_id>.log` | Human-readable chat log (with `# Session` / `# ID` / `# Model` / `# Provider` headers and `[timestamp] role` message bodies; thinking content carries a `[thinking]` line) |
| Code blocks in replies | Inline in the message area | Code blocks in model replies are rendered as Markdown, with a language tag and a Copy button |

The session log is plain text and can be viewed or kept directly; when a session is deleted or cleared, the corresponding `.json` and `.log` are removed as well.

## 9. FAQ

**Question: There is no output at all after sending a message — what should I check?**
First confirm the page header border is green (the Provider is online); then check the `base_url` / `endpoint` / `api_key` config. When the server connection fails, an `error` event is returned (e.g., `Request failed: ...`) and the page shows an error toast.

**Question: Why is the thinking block empty?**
The model did not output any reasoning (no `reasoning_content` and no think tags in the reply), or the **Thinking** switch was off when sending; the switch state is saved with the session.

## Related Docs

- [Sessions Manual Overview](/en/docs/manual/sessions/)
- [Create Session](/en/docs/manual/sessions/create-session/)
- [Sessions Reference](/en/docs/tools/sessions/)
- [Mock Debug Environment](/en/docs/tools/mock/)