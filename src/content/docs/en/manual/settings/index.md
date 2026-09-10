---
title: Settings Manual Overview
description: "Overview of the BenchScope Settings page manual: page structure, the seven panels, backend loading logic when the page opens, and navigation through the manual chapters."
---

# Settings Manual Overview

The Settings page (navigation name "Settings", i18n key `settings`) is the **global configuration hub** of the BenchScope WebUI, centrally managing **language and data directories, inference service Providers, the model catalog, dataset caches, Bench engines, and built-in skills**. This manual walks through each panel one by one: how to click, what to fill in, and how the backend executes.

## 1. Features

- **Left menu + right content** layout: the 7 menu items on the left correspond to 7 panels; the right content area switches along with the menu selection.
- All setting changes are **persisted immediately** to `~/.benchscope/settings.json` (the backend `ConfigManager` writes to disk); no service restart is required (Root Dir changes also take effect immediately). All panel data comes from the backend REST API (FastAPI, routes mounted at `/api/*`) and is fetched in parallel when the page opens.

## 2. Page Structure

```
+------------------+--------------------------------------------------+
| Settings (title) | Right content area (switches with the left menu) |
+------------------+--------------------------------------------------+
| > General        | +----------------------------------------------+ |
| > Providers      | | Panel cards (language / cache paths /         |
| > Models         | | Provider / models / datasets / engines /      |
| > Datasets       | | skills cards)                                 |
| > Bench Engines  | +----------------------------------------------+ |
| > Skills         | The Bench Engines / Models / Datasets / Skills  |
| > Plugins        | panels use a "fill height + inner scroll"       |
|                  | layout (content-fill)                           |
+------------------+--------------------------------------------------+
```

**Seven panels** (menu order matches `menuItems` in `SettingsView.vue`):

| # | Menu (i18n key) | Panel content | Manual |
| --- | --- | --- | --- |
| 1 | General (`general`) | Language switch, cache paths (Root Dir + 8 subdirectories) | [General Settings](/en/docs/manual/settings/general/) |
| 2 | Providers (`environment`) | Multiple inference providers: add / edit / delete / test connection | [Provider Management](/en/docs/manual/settings/providers/) |
| 3 | Models (`modelsTab`) | Model vendor catalog (Domestic / International groups, read-only browsing) | [Models & Datasets](/en/docs/manual/settings/models-datasets/) |
| 4 | Datasets (`datasetsTab`) | Built-in dataset cache (12 total, downloadable) | [Models & Datasets](/en/docs/manual/settings/models-datasets/) |
| 5 | Bench Engines (`benchesTab`) | Engine list (5 built-in: `benchscope` / `vllm` / `sglang` / `native-hf` / `mock`), environment validation, Mock toggle, create / upload engines, engine comparison | [Engine Management](/en/docs/manual/settings/engines/) |
| 6 | Skills (`skills`) | Built-in skill list: skill pack download, prompt copy | [Skills & Plugins](/en/docs/manual/settings/skills-plugins/) |
| 7 | Plugins (`plugins`) | Plugin system placeholder (coming soon) | [Skills & Plugins](/en/docs/manual/settings/skills-plugins/) |

## 3. Backend Execution Logic

`onMounted` in `SettingsView.vue` loads in the following order (step 1 is internally parallel; the remaining panel loads follow immediately after, fired in parallel):

| Step | Frontend action | Backend API | Notes |
| --- | --- | --- | --- |
| 1 | `config.load()` | `GET /api/config`, `GET /api/config/status`, `GET /api/config/gpu` (parallel) | config snapshot, service status, GPU info |
| 2 | `loadDirs()` | `GET /api/config/dirs` | cache directory list (General panel) |
| 3 | `loadDatasets()` | `GET /api/config/datasets` | built-in datasets + categories + cache status |
| 4 | `loadModelCatalog()` | `GET /api/config/model-catalog` | model vendor catalog (Domestic / International groups) |
| 5 | `loadBenches()` | `GET /api/benchs` → `GET /api/benchs/authoring` | engine list (with environment validation + Mock status), engine authoring guide |
| 6 | `loadProviders()` | `GET /api/config/providers` → per-provider `POST /api/config/test-connection` (parallel) | provider list + per-provider online status and model probe |
| 7 | `loadSkills()` | `GET /api/skills` | built-in skill list |

<div class="info">
**Info:** Write operations in any panel (language switch, directory change, save provider, download dataset, Mock toggle, engine upload) all go through `POST/PUT` APIs that persist to `~/.benchscope/settings.json` or the corresponding yaml file; the frontend then refreshes the affected list. See [Settings](/en/docs/tools/settings/) and [Architecture](/en/docs/tools/architecture/).
</div>

## 4. Document Navigation

1. [General Settings](/en/docs/manual/settings/general/) — language, theme, cache paths, Root Dir change confirmation
2. [Provider Management](/en/docs/manual/settings/providers/) — add / edit / delete providers, test connection, model probe
3. [Models & Datasets](/en/docs/manual/settings/models-datasets/) — vendor catalog browsing, download & cache for the 12 built-in datasets
4. [Engine Management](/en/docs/manual/settings/engines/) — engine types, environment validation, Mock toggle, Create / Upload Engine, engine comparison
5. [Skills & Plugins](/en/docs/manual/settings/skills-plugins/) — the 3 built-in skills, skill pack download, prompt copy, plugin placeholder

## 5. FAQ

**Question: Do I need to restart the service after changing Settings?**

No. All settings (including Root Dir changes) take effect immediately and are written to `~/.benchscope/settings.json`; after a Root Dir change the backend rebuilds the subdirectories under the new root (existing data is not migrated).

**Question: Which languages does the Settings page support?**

Chinese (`zh`) and English (`en`); switch via the **Language** dropdown in the General panel — the change applies to the whole page immediately and is persisted.

**Question: Which command checks the BenchScope version?**

`benchscope --version` does not exist; check the version with `pip show benchscope` or call `GET /api/version`.