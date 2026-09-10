---
title: Sessions Manual Overview
description: "Overview of the Sessions (chats) module manual: features, page structure, document navigation, module labels (i18n), and related docs."
---

# Sessions Manual Overview

Sessions (navigation name "Sessions") is BenchScope's **interactive chat module**: pick a configured inference Provider and model, then hold an **SSE streaming conversation** with the model, watching its output, reasoning process (`reasoning_content` increments), and Token statistics in real time.

<div class="info">
**Info:** BenchScope does **not** expose an OpenAI-compatible `/v1/*` inference endpoint. Chat requests are **proxied** by the server to the active Provider (an OpenAI-compatible endpoint), so a usable inference service must be configured and activated under Settings → Providers before using the Sessions feature.
</div>

## 1. Features

- **Multi-session management**: create, switch, rename, delete, and clear sessions; sessions are persisted automatically and restored after the service restarts.
- **Streaming chat**: SSE streaming output (`token` / `thinking` increments), Markdown rendering + code highlighting.
- **Sampling parameters**: `temperature` (0-2), `top_k` (1-200), `top_p` (0-1), plus the quality preset `quality` (high/medium/low) and the thinking switch `enable_thinking`.
- **Token statistics**: metrics such as TTFT, tok/s, TPOT, and ITL are displayed live in the session header performance bar.
- **Session persistence**: session state is stored under `~/.benchscope/sessions/*.json`; chat logs are stored under `~/.benchscope/logs/sessions/*.log`.

## 2. Page Structure

```
+----------------------------------+----------------------------------------------+
| Left sidebar (260px, session     | Main content area                            |
| workspace)                       |                                              |
| +------------------------------+ | +-------------------------------------------+|
| |[ + New Session ]             | | |Perf turns/steps | LLM | TTFT | TPOT | ITL ||
| +------------------------------+ | |+ top_k [10]  temp [0.5]  top_p [1.0]      ||
| | Chats          [ Clear ]     | | +-------------------------------------------+|
| +------------------------------+ | |Messages (Markdown + code highlight +      ||
| | - Session A  09-09 21:00 [..]| | |collapsed thinking block)                  ||
| | - Session B  09-09 20:30 [..]| | | U user bubble (right)                     ||
| +------------------------------+ | |AI assistant bubble (left)  [Thinking v]   ||
|                                  | +-------------------------------------------+|
|                                  | |Input box (Enter to send / Shift+Enter     ||
|                                  | |for a new line)                            ||
|                                  | |Provider v  Select Model v  Quality v      ||
|                                  | |Thinking [x]  (->)                         ||
+----------------------------------+----------------------------------------------+
```

- **Left sidebar (workspace)**: a **New Session** button at the top; a **Clear** button next to the **Chats** list title; each session item has an icon, a title, a modified time, and a three-dot menu (Rename session / Delete).
- **Main content area**: a performance bar (with sampling parameter configuration), a message area, and a bottom input bar (Provider, model, quality, thinking switch, send button).
- **When no session is selected**: the main content area shows the empty state "Select or create a session".

## 3. Document Navigation

| No. | Document | Content |
| --- | --- | --- |
| 4.2 | [Create Session](/en/docs/manual/sessions/create-session/) | Choosing the Provider, model, quality preset, and thinking switch |
| 4.3 | [Streaming Chat](/en/docs/manual/sessions/chat/) | SSE streaming output, Token statistics, generated files |

## 4. Module Labels (i18n)

| i18n key | English label | Description |
| --- | --- | --- |
| `sessions` | Sessions | Top navigation name |
| `workspaces` / `chats` | Workspaces / Chats | Left workspace and conversation list |
| `newSession` | New Session | Button at the top-left |
| `clearSessions` | Clear All | One-click clear of all sessions |
| `sessionRename` | Rename session | Three-dot menu item on a session |
| `selectModelForChat` | Select Model | Placeholder of the model dropdown in the input bar |
| `inputPlaceholder` / `messagePlaceholder` | Type a message... / Message the agent | Input box placeholder |
| `send` / `newline` | Send / New line | Send (Enter) and newline (Shift+Enter) |
| `qualityHigh` / `qualityMedium` / `qualityLow` | High / Medium / Low | Quality preset enum |
| `thinking` / `thinkingInProgress` | Thinking / Thinking... | Thinking switch and streaming thinking block |
| `fullAccess` | Full access | Reserved permission display label in the module |
| `produced` | Produced | Reserved label for session artifacts in the module |
| `systemPrompt` | System Prompt | `system_prompt` parameter for session creation |

## 5. Related Docs

- [Manual Overview](/en/docs/manual/) — index of the six module manuals
- [Sessions Reference](/en/docs/tools/sessions/) — concepts and parameter reference
- [Mock Debug Environment](/en/docs/tools/mock/) — joint debugging of Sessions without a real inference service