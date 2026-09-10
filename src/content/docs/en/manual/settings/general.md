---
title: General Settings
description: 'Manual for the Settings "General" panel: language switch, theme notes, cache path (Root Dir) editing and data directory change confirmation, and backend execution logic.'
---

# General Settings

The **General** panel (menu key `general`) provides two settings: **Language** (interface language switch) and **Cache Paths** (Root Dir and its 8 subdirectories). All changes are persisted immediately to `~/.benchscope/settings.json` — no restart required.

## 1. Features

- **Language**: pick one of Chinese (`zh`) / English (`en`); the change applies immediately and is saved.
- **Cache Paths**: lists 9 directories; only **Root Dir** (`data_dir`) is editable — the remaining 8 subdirectories are displayed read-only (they reset automatically when the Root Dir changes).
- **Theme (`theme`)**: the platform supports three levels — `light` / `dark` / `system` (rendered by `App.vue` from the config); the Settings page currently **provides no theme control** — the `theme` field is set via `POST /api/config` or by directly editing `~/.benchscope/settings.json`.
- **Inference service API (`api`)**: the four fields Base URL / Endpoint / API Key / Extra Headers are managed in the [Providers panel](/en/docs/manual/settings/providers/); the active Provider is synced automatically to the config `api` field (`base_url` / `endpoint` / `api_key` / `extra_headers`).
- **bench commands (`bench_commands`)**: `vllm` → `vllm bench serve`, `sglang` → `python -m sglang.bench_serving`, used by the native engines; the Settings page does not expose controls for them — modify them via `POST /api/config`.

## 2. Page Structure

```
+------------------------------------------+
| Language                                 |
| [English / 中文 v]                         |
+------------------------------------------+
| Cache Paths                              |
| Root Dir    ~/.benchscope      [editable]|
| Perf       ~/.benchscope/perfs           |
| Eval       ~/.benchscope/evals           |
| Analysis   ~/.benchscope/analysys        |
| Logs       ~/.benchscope/logs            |
| Sessions   ~/.benchscope/sessions        |
| Models     ~/.benchscope/models          |
| Datasets   ~/.benchscope/datasets        |
| Plugins    ~/.benchscope/plugins         |
+------------------------------------------+
```

| Area | Control | Description |
| --- | --- | --- |
| Language card | `a-select` dropdown | Options: English (`en`) / Chinese (`zh`), default `en` |
| Cache Paths card | 9 directory rows (label + description + path value) | Only the Root Dir row is clickable to edit; the other 8 rows are read-only gray text |
| Root Dir edit state | Input box + Save button | Entered by clicking the Root Dir path value; Enter or Save triggers the confirmation dialog |
| Change confirmation dialog | OK / Cancel | Title `rootDirChangeTitle` ("Change data storage path"), body `rootDirChangeContent` |

## 3. Input Parameters

### 3.1 Language

| Field | Type | Constraint | Default | Description |
| --- | --- | --- | --- | --- |
| `locale` | enum | required; only `en` / `zh` | `en` | Interface language; dropdown options are English / 中文 |

### 3.2 Cache Paths

| Field (key) | Editable | Default | Description |
| --- | --- | --- | --- |
| `data_dir` | Yes | `~/.benchscope` | Data root directory (Root Dir); takes effect immediately on change, no restart required |
| `perfs_dir` | No | `~/.benchscope/perfs` | Performance test task directory |
| `evals_dir` | No | `~/.benchscope/evals` | Accuracy test task directory |
| `analysis_dir` | No | `~/.benchscope/analysys` | Data analysis directory (the directory name is `analysys`, linked to the Datas cache) |
| `logs_dir` | No | `~/.benchscope/logs` | Log directory (runtime logs + task terminal output) |
| `sessions_dir` | No | `~/.benchscope/sessions` | Session cache directory |
| `models_dir` | No | `~/.benchscope/models` | Model download directory (linked to Settings/Models) |
| `datasets_dir` | No | `~/.benchscope/datasets` | Dataset download directory (linked to Settings/Datasets) |
| `plugins_dir` | No | `~/.benchscope/plugins` | Plugin installation & loading directory |

## 4. Operation Steps

### 4.1 Switch Language

1. Click **General** in the left menu.
2. In the **Language** card dropdown, select `中文` or `English`.
3. No need to click Save: the change applies to the whole page immediately and is persisted automatically.

### 4.2 Change Root Dir

1. Click **General** in the left menu, then go to the **Cache Paths** card.
2. Click the current path value on the right of the Root Dir row (read-only style → input box + Save button).
3. Enter the new path in the input box (`~` supported), then press **Enter** or click **Save**.
4. The "Change data storage path" confirmation dialog appears, with the text: "Clicking OK creates a new blank data storage path from the new Root Dir. Existing data will NOT be migrated. Continue?"
5. Click **OK** to save the new path; or **Cancel** to discard the edit and restore the original value display.

Note: the Root Dir value must not be empty after trimming — an empty value is not saved and the original value is restored; a value identical to the current one does not trigger a save.

<div class="warning">

**Warning:** After a Root Dir change, a **brand-new blank directory tree** is created and existing data is **NOT migrated**; all 8 subdirectories (`perfs` / `evals` / `analysys` / `logs` / `sessions` / `models` / `datasets` / `plugins`) are reset to the default directories under the new root. Back up or export important data before making the change.

</div>

### 5.1 Page Load

`GET /api/config/dirs` → the backend iterates over `CACHE_DIR_INFO` (9 items) and returns `value` (current config value, falling back to `DEFAULT_CONFIG` when absent), `default`, `exists` (whether the directory exists), and `readonly` (only `data_dir` is `false`).

### 5.2 Switch Language

Frontend `onLocaleChange`: `setLocale(locale)` replaces the interface copy immediately → `config.save({ locale })` → `POST /api/config` (body `{"locale": "zh"}`) → the backend `ConfigManager.update` merges the patch and writes `~/.benchscope/settings.json`.

### 5.3 Save Root Dir

`POST /api/config/dirs` (body `{"data_dir": "<new path>"}`):

1. The backend checks running tasks: if `state.tasks.running_count > 0` and the patch contains `perfs_dir` / `evals_dir`, it returns **409** (the current UI submits only `data_dir`, so this is never triggered).
2. `ConfigManager.update`: a `data_dir` change → all 8 subdirectories are reset to `<new root>/default subdir` (`perfs` / `evals` / `analysys` / `logs` / `sessions` / `models` / `datasets` / `plugins`).
3. The environment variable `BENCHSCOPE_DATA_DIR` is synced to the new root (passed through to child processes, no service restart needed).
4. `save()` persists settings.json; `ensure_dirs()` creates all directories recursively.
5. Returns `{"ok": true, "requires_restart": false, "changed": {...}}`; the frontend re-runs `loadDirs()` to refresh the list.

## 5. Backend Execution Logic

### 6.1 Related APIs (not called by the current UI, available via API)

| API | Method | Description |
| --- | --- | --- |
| `/api/config` | `POST` | General config patch (fields such as `theme` / `locale` / `api` / `bench_commands`) |
| `/api/config/restart` | `POST` | body `{"migrate": bool}`: optionally migrates data and restarts the service (`os.execv` restarts the process) |

## 6. FAQ

**Question: Can the old data still be used after changing the Root Dir?**

Not directly. The new Root Dir is a blank directory tree; the old data stays at the original path. To relocate it, copy it manually first, or call `POST /api/config/restart` (`migrate: true`) to run the migration flow. See [Configuration](/en/docs/install/configuration/) for details.

**Question: Why are the subdirectories shown in gray and not editable?**

The 8 subdirectories are derived from the Root Dir (`<root>/perfs`, `<root>/analysys`, etc.) and displayed read-only; to change their location, change the Root Dir. The analysis directory is named `analysys` (not `analysis`).

**Question: Where do I switch the theme?**

The Settings page currently has no theme control; the theme comes from the `theme` config field (`light` / `dark` / `system`, default `light`). You can modify it via `POST /api/config`; the change takes effect after a page refresh.