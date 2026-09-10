---
title: Create Session
description: "Create a session on the Sessions page: input parameters, field constraints, button operations, and backend logic for choosing the Provider, model, quality preset, and thinking switch."
---

# Create Session

This page explains how to **create a session** on the Sessions page: choose the Provider, model, quality preset, and thinking switch, and describes the API calls and data flow that run in the backend when a session is created.

## 1. Features

- Click the **New Session** button in the left sidebar to create a session; it appears in the **Chats** list immediately and is activated.
- The default session name follows the pattern `会话 MM/DD HH:mm` (e.g., `会话 09/09 21:00`, i.e. "Session 09/09 21:00"); after the first message is sent, it is automatically replaced with the first 50 characters of the message (custom-named sessions keep their names).
- The session identifier **session_id** has the format `sess-MMDD-HHMMSS-<6-char hex>` (e.g., `sess-0909-210000-a1b2c3`).
- The Provider, model, quality preset, and thinking switch selections in the bottom input bar are saved with the session and used in the later [Streaming Chat](/en/docs/manual/sessions/chat/).

## 2. Page Structure

The session-creation controls are concentrated in the **left sidebar** and the **bottom input bar**:

```
+----------------------------------+----------------------------------------------+
| Left sidebar (260px)             | Main content area                            |
| +------------------------------+ | +-------------------------------------------+|
| |[ + New Session ]  <- entry   | | |Perf turns/steps | LLM | TTFT | TPOT | ITL ||
| +------------------------------+ | |+ top_k [10]  temp [0.5]  top_p [1.0]      ||
| | Chats          [ Clear ]     | | +-------------------------------------------+|
| +------------------------------+ | |Message area                               ||
| | - Session A  09-09 21:00 [..]| | +-------------------------------------------+|
| | - Session B  09-09 20:30 [..]| | |Input box: Message the agent               ||
| +------------------------------+ | |Provider v  Select Model v  Quality v      ||
|                                  | |Thinking [x]  (->)                         ||
+----------------------------------+----------------------------------------------+
```

| Control | Location | Description |
| --- | --- | --- |
| New Session | Top of the left sidebar | Create a new session (i18n `newSession`) |
| Provider dropdown | Bottom input bar | List comes from `GET /api/config/providers`; switching re-probes the model list (i18n `selectInferenceProvider`) |
| Select Model | Bottom input bar | List comes from the probe results of the selected Provider (i18n `selectModelForChat`) |
| Quality dropdown | Bottom input bar | `high`/`medium`/`low`, default `medium` |
| Thinking switch | Bottom input bar | `enable_thinking`, on by default |
| top_k / temp / top_p | Top performance bar | Sampling parameters, defaults 10 / 0.5 / 1 |

## 3. Input Parameters

| Field | Type | Constraint | Default | Description |
| --- | --- | --- | --- | --- |
| `provider_id` | string | valid Provider id | the active Provider | Target Provider to which chat requests are proxied |
| `model` | string | within the Provider's model list | first probed model | Inference model name |
| `temperature` | number | 0 - 2 | 0.5 | Sampling temperature; takes precedence over `quality` when passed explicitly |
| `quality` | string | enum: `high` / `medium` / `low` | `medium` | Quality preset, mapping to temperature 0.9 / 0.5 / 0.2 |
| `top_k` | int | 1 - 200 | 10 | Keep only the top-K candidate tokens by probability |
| `top_p` | float | 0 - 1 | 1.0 | Nucleus sampling cumulative probability threshold |
| `enable_thinking` | boolean | true / false | true | Thinking switch |

<div class="warning">
**Warning:** `max_tokens` is **fixed at 4096** and is not exposed as a session parameter. The server writes `"max_tokens": 4096` directly into the proxied payload.
</div>

Additional fields of the session creation API (`POST /api/sessions`):

| Field | Type | Constraint | Default | Description |
| --- | --- | --- | --- | --- |
| `title` | string | ≤ 60 characters (rename input limit) | auto-generated `会话 MM/DD HH:mm` | Session name |
| `model` | string | optional | empty | Initial model |
| `system_prompt` | string | optional | empty | System prompt (i18n `systemPrompt`); prepended as a `system` message in every conversation |

## 4. Field Constraints

| Field | Required | Type | Min | Max | Enum | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `provider_id` | No | string | — | — | configured Provider ids | Falls back to the active Provider's global `api` config when missing or unknown |
| `model` | No | string | — | — | Provider model list | Falls back to the session's selected model, then to `default` |
| `temperature` | No | number | 0 | 2 | — | Overrides the `quality` mapping when passed explicitly |
| `quality` | No | string | — | — | high / medium / low | The mapping only takes effect when `temperature` is missing |
| `top_k` | No | int | 1 | 200 | — | Not written into the proxied payload when ≤ 0 |
| `top_p` | No | float | 0 | 1 | — | Not written into the proxied payload when missing |
| `enable_thinking` | No | boolean | — | — | true / false | Passed via `chat_template_kwargs` |
| `max_tokens` | — | int | — | — | — | Fixed at 4096, not configurable |

## 5. Execution Steps (Button Operations)

1. Open the **Sessions** page from the top navigation (i18n `sessions`).
2. Confirm the page header border is **green** (the selected Provider is online); red means not configured or offline — configure it under Settings → Providers first, see [Settings](/en/docs/tools/settings/).
3. In the bottom input bar, open the **Provider** dropdown and select an inference provider.
4. Open the **Select Model** dropdown and choose a model (defaults to the first one once probing completes).
5. Open the **Quality** dropdown and choose `high` / `medium` / `low` (default `medium`).
6. Toggle the **Thinking** switch (on by default).
7. (Optional) Adjust `top_k` / `temp` / `top_p` in the top performance bar.
8. Click **New Session** at the top of the left sidebar.
9. The new session appears in the **Chats** list and is activated; you can now send a message in the input box, see [Streaming Chat](/en/docs/manual/sessions/chat/).

## 6. Backend Execution Logic

When the page loads and a session is created, the following flow happens in the backend:

1. Page load (`onMounted`): the frontend calls `GET /api/sessions` to load the session list and `GET /api/config/providers` to load the Provider list (returns `providers` and `active_provider`).
2. The frontend calls `POST /api/config/test-connection` for the selected Provider (submitting `base_url` / `endpoint` / `api_key` / `extra_headers`) to obtain the model list and online status; the header border turns green when online.
3. Clicking **New Session** → the frontend calls `POST /api/sessions` (e.g., body `{"model": "qwen3-8b"}`):
    - `SessionManager.create_session()` generates a `sess-...` id with the default title `会话 MM/DD HH:mm`;
    - the session is persisted immediately to `~/.benchscope/sessions/<session_id>.json` and logged to `~/.benchscope/logs/sessions/<session_id>.log`;
    - the API returns `{session: {...}}`.
4. The frontend refreshes the session list (`GET /api/sessions`, sorted by `updated_at` descending) and activates the new session (`GET /api/sessions/{session_id}`).

<div class="info">
**Info:** BenchScope does **not** expose an OpenAI-compatible `/v1/*` inference endpoint. When chatting, the server resolves `base_url` / `endpoint` / `api_key` from the Provider list by `provider_id` (falling back to the global `api` config, i.e., the **active Provider**, when missing or unknown) and **proxies** the request to the target Provider's `base_url + endpoint` (default `/v1/chat/completions`).
</div>

## 7. FAQ

**Question: Why is the Provider dropdown empty?**
No Provider has been configured yet. Configure and activate at least one inference service under Settings → Providers first, see [Settings](/en/docs/tools/settings/).

**Question: What is the difference between quality and temperature?**
`quality` (high/medium/low) maps to `temperature` 0.9 / 0.5 / 0.2; an explicitly passed `temperature` takes precedence. The WebUI always sends `temperature` by default, so the quality preset mainly takes effect when the API is called directly without passing `temperature`.

**Question: Can I configure the maximum reply length?**
No. The session `max_tokens` is fixed at 4096 and is not exposed as a session parameter.

**Question: Will sessions be lost after restarting the service?**
No. Session state is persisted under `~/.benchscope/sessions/*.json` and is restored automatically after the service restarts.

## Related Docs

- [Sessions Manual Overview](/en/docs/manual/sessions/)
- [Streaming Chat](/en/docs/manual/sessions/chat/)
- [Sessions Reference](/en/docs/tools/sessions/)
- [Settings](/en/docs/tools/settings/)