---
title: Provider Management
description: 'Manual for the Settings "Providers" panel: adding / editing / deleting inference service providers, testing connections, probing models, and backend execution logic.'
---

# Provider Management

The **Providers** panel (menu key `environment`) configures **multiple inference service providers (OpenAI-compatible API)**: one card per Provider, each of which can be added, edited, deleted, and connection-tested. The active Provider is synced to the config `api` field and becomes the forwarding target for task execution and session requests.

<div class="info">

**Info:** The BenchScope API does **not expose** an OpenAI-compatible `/v1/*` inference endpoint; session requests are proxied by the backend to the active Provider. See [Architecture](/en/docs/tools/architecture/) and [Sessions](/en/docs/tools/sessions/).

</div>

## 1. Features

- **Multiple providers coexist**: several inference services can be configured at the same time (e.g. Local vLLM, Remote SGLang); each page picks the service to use via the Provider selection.
- **Online status probing**: every Provider card shows its live Online / Offline status and the probed **model list** (model tags can be copied with one click).
- **Activation & sync**: the first Provider added is activated automatically; the active entry's `base_url` / `endpoint` / `api_key` / `extra_headers` are synced into the config `api` field (task execution and session proxying both read `api`).
- **Endpoint convention**: a Provider's `endpoint` defaults to `/v1/chat/completions` (model probing hits `{base_url}/v1/models` on the backend).

## 2. Page Structure

```
+-------------------------------------------------+
|Providers                       [Add Provider]   |
|Configure multiple inference providers ...       |
+-------------------------------------------------+
|Provider card (one per Provider)                 |
|Local vLLM    * Online                  [Delete] |
|------------------------------------------------ |
|Provider Name  [______________________________]  |
|Base URL       [http://127.0.0.1:8000]           |
|API Key        [sk-... (password box)]           |
|Model Status   * Online / o Offline              |
|Models         [model-a] [model-b] (tags, copy)  |
|------------------------------------------------ |
|[Edit / Save]  [Test Connection]                 |
+-------------------------------------------------+
(When the list is empty: "No providers yet — click
 Add Provider in the top-right to add one")
```

## 3. Input Parameters

### 3.1 Add Provider Dialog

| Field | Type | Constraint | Default | Description |
| --- | --- | --- | --- | --- |
| `name` (Provider Name) | string | **required**, non-empty after trim | empty | Provider name, e.g. Local vLLM / Remote SGLang |
| `base_url` (Base URL) | string | optional; OpenAI-compatible service address | empty (placeholder `http://127.0.0.1:8000`) | Inference service Base URL; a trailing `/` is stripped automatically by the backend |
| `api_key` (API Key) | string | optional (password box) | empty (placeholder `sk-... (optional)`) | API Key; when non-empty, probe requests carry `Authorization: Bearer <key>` |
| `endpoint` | string | no page input, backend default | `/v1/chat/completions` | Session request path |
| `extra_headers` | object | no page input, backend default | `{}` | Extra request headers |

### 3.2 Provider Card Edit Fields

| Field | Type | Constraint | Description |
| --- | --- | --- | --- |
| `name` (Provider Name) | string | required, non-empty after trim | read-only outside edit mode; click **Edit** to unlock |
| `base_url` (Base URL) | string | optional | same as above |
| `api_key` (API Key) | string | optional (password box) | same as above |

## 4. Operation Steps

### 4.1 Add Provider

1. Click **Providers** in the left menu.
2. Click the **Add Provider** button in the top-right of the panel to open the add dialog (title "Add Provider", hint "Add an inference provider (OpenAI-compatible API)").
3. Fill in **Provider Name** (required), **Base URL**, and **API Key** (optional).
4. Click the **Save** button at the bottom of the dialog (disabled while `name` is empty); or **Cancel** to close the dialog.
5. After a successful add, the card list refreshes and the new Provider's online status and models are probed automatically.

### 4.2 Edit & Save Provider

1. Click **Edit** at the bottom of the target Provider card (the card's fields unlock).
2. Modify Provider Name / Base URL / API Key.
3. Click **Save**: on success, the Provider's status is re-probed automatically.

### 4.3 Test Connection

1. Click the **Test Connection** button at the bottom of the Provider card (the button enters a loading state).
2. Probe succeeds: a "Connected" toast is shown, and the card displays Online + the model tag list.
3. Probe fails: a "Connection Failed" toast is shown, and the card displays Offline with an empty model list.

Note: the model list is read-only display data obtained by probing, not a configurable parameter.

### 4.4 Copy / Delete Provider

1. Copy a model: click the copy icon on a model tag; the model name is written to the clipboard.
2. Delete: click the **Delete** (red) button in the top-right of the card; after deletion the list refreshes and probing is re-run.

### 5.1 Page Load & Probing

1. `GET /api/config/providers` → returns `{providers: [...], active_provider: "..."}`.
2. The frontend calls `POST /api/config/test-connection` **in parallel for each Provider**, body `{base_url, endpoint, api_key, extra_headers}`.
3. Backend `test_connection`: `requests.get("{base_url}/v1/models")` — an `Authorization: Bearer <key>` header is attached when `api_key` is non-empty, `extra_headers` are merged in, **timeout 6 seconds**; on success it returns `{"ok": true, "models": [...]}` (list of model ids), and on exception it returns `{"ok": false, "error": "..."}` (error truncated to 300 characters).

### 5.2 Add / Edit / Delete / Activate

| Operation | API | Backend logic |
| --- | --- | --- |
| Add | `POST /api/config/providers` | validates `name` is non-empty (400 otherwise); generates id `provider_<millisecond timestamp>`; **the first Provider is auto-activated**; `_sync_api_from_active` writes the active entry into the config `api` field; persists to settings.json |
| Edit | `PUT /api/config/providers/{id}` | unknown id returns 404; empty `name` returns 400; if the edited entry is the active one, the `api` field is re-synced |
| Delete | `DELETE /api/config/providers/{id}` | unknown id returns 404; if the deleted entry is the active one, **the first remaining Provider is auto-activated** and the `api` field is synced |
| Activate | `/activate` sub-route of `POST /api/config/providers/{id}` | switches `active_provider` and syncs the `api` field (no button in the current Settings page; available via the API) |

## 5. Backend Execution Logic

### 6.1 Configuration Sync Chain

```
active Provider --sync--> config api field (base_url/endpoint/api_key/extra_headers)
                                    |
                    +---------------+---------------+
                    v                               v
        performance / accuracy task execution   session request proxy forwarding
```

The configuration is persisted in `~/.benchscope/settings.json` (`providers` array + `active_provider` + `api` field). The `api` field is read by both the task execution chain and the session proxy — BenchScope itself never serves the requests; it forwards them to the active Provider.

## 6. FAQ

**Question: Among multiple Providers, which one takes effect?**

The Provider that `active_provider` points to takes effect: its `base_url` / `endpoint` / `api_key` / `extra_headers` are synced into the config `api` field, and both task execution and session requests are forwarded to it. In the current version the **first** Provider added is auto-activated, and when the active entry is deleted the first remaining one automatically takes over.

**Question: How do I troubleshoot a failed connection test (shown as Offline)?**

Check in order: the Base URL is reachable (`{base_url}/v1/models` returns 200); the API Key is correct (a Bearer header is attached when non-empty); the network is reachable (the backend probe timeout is 6 seconds). Verify on the server side with `curl {base_url}/v1/models`.

**Question: Where does a Provider's model list come from?**

From the probe: the backend requests `{base_url}/v1/models` and displays the response's `data[].id` as the model list on the card; the list does not represent a BenchScope whitelist — it only reflects the models currently available on that service.