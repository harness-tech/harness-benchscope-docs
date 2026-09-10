---
title: Engine Management
description: 'Operations manual for the Settings "Bench Engines" panel: engine types, environment validation, Mock toggles, the four-step Create Engine flow, Upload Engine, engine comparison, and backend execution logic.'
---

# Engine Management

The **Bench Engines** panel (menu key `benchesTab`) manages BenchScope's **built-in testing engines**. It displays the engine list (name / type / version / environment status / highlights), environment requirements and validation results, and Mock toggles, and provides three actions in the top-right corner: **Create Engine** (authoring guide), **Upload Engine** (upload an engine package), and **Engine Comparison**.

## 1. Feature Overview

- **Built-in testing engines**: Bench CLI (in-house engine, no local framework environment required); the vLLM / SGLang native engines require validation of the locally installed version; there are also Native (accuracy evaluation with local weights) and Mock (controllable pseudo-output) engines.
- **Environment validation**: The vLLM / SGLang and Native engines validate each dependency in `requires` one by one (package version + command-line availability); the in-house and Mock engines have no dependencies and always pass.
- **Mock toggle (`engineMock`)**: One toggle per engine; when enabled, the engine uses **simulated data and a simulated runtime** (skipping real framework dependency checks) and the card is marked Mock; when disabled it reverts to Real.
- **Create Engine**: A four-step authoring guide (confirm the target version → pull the upstream source and verify parameters → copy the prompt to an AI to generate the definition → import with Upload Engine) + upstream reference links + a copyable AI prompt.
- **Upload Engine / Engine Comparison**: Upload a `.yaml` engine definition or a `.tar.gz` skill package; once validation passes it is merged into the engine list (available since 1.0.7); Engine Comparison compares all engines across 6 dimensions.

## 2. Page Structure

```
+--------------------------------------------------------------+
| Bench Engines (benchesTab)      [Create Engine] [Upload Engine]|
| Built-in testing engines: Bench CLI is the in-house engine... |
| (benchesDesc)                          [Engine Comparison]    |
+--------------------------------------------------------------+
| Engine cards (one per engine, full-page scroll)               |
| Bench CLI  [Default][builtin][Real][Env OK]   Version stable  |
| Description + highlights (bilingual, shown per UI language)   |
| ------------------------------------------------------------ |
| Environment requirements (when no deps: no framework          |
| requirements, ready out of the box)                           |
| torch        required >=2.0        installed 2.1.0   [OK]     |
| vllm         required >=0.23,<0.24 installed -       [FAIL]   |
| Install hint: pip install 'vllm>=0.23,<0.24'                  |
| Mock environment & data      [toggle]                         |
+--------------------------------------------------------------+
```

| Area | Control / Label | Description |
| --- | --- | --- |
| Top action bar | Create Engine / Upload Engine / Engine Comparison (text buttons, top-right) | Open the authoring guide / upload / comparison dialogs respectively |
| Card header | Name + tags: Default engine (`benchDefault`), engine type (`benchKind`, raw `kind` value), Mock / Real (`engineMockTag` / `engineRealTag`), environment status (Env OK / Env missing), version (`benchVersion` v{version}) | Environment status green = satisfied (`benchEnvReady`), red = not satisfied (`benchEnvMissing`) |
| Card body | Description + highlights (`benchHighlights`) list | Reads the `*_zh` / English fields according to the UI language |
| Card footer | Environment requirements table (`benchRequires`: name / required version / installed / OK / FAIL + install hint) + Mock toggle (`engineMock`) | Engines without dependencies show `benchNoRequires` "no framework environment requirements, ready out of the box" |

## 3. Input Parameters

The engine panel has **no form inputs**; the inputs are the Mock toggle and uploaded files:

| Parameter | Type | Constraint | Default | Description |
| --- | --- | --- | --- | --- |
| Mock toggle (`engineMock`) | Boolean | One per engine; value `true` / `false` | `false` (Real) | When enabled, the engine uses simulated data and a simulated runtime |
| Uploaded file (Upload Engine) | File | Extension only `.yaml` / `.yml` / `.tar.gz` / `.tgz`; **single file no larger than 20MB**; non-empty | None | `.yaml` / `.yml` is an engine definition; `.tar.gz` / `.tgz` is a skill package (packaged by bench-engine-authoring) |

**Engine type (`kind`) enum**: `builtin` (in-house, no dependencies) / `vllm` (vLLM native) / `sglang` (SGLang native) / `native` (accuracy with local weights) / `mock` (controllable pseudo-output); `vllm` and `sglang` require framework version + CLI availability checks, and `native` requires torch + transformers version checks.

**Current built-in engines** (`benchscope/configs/benchs.yaml`, 5 in total):

| id | Name | kind | Version | Environment requirements (`requires`) |
| --- | --- | --- | --- | --- |
| `benchscope` | Bench CLI | `builtin` | stable | None (`requires: []`, default engine) |
| `vllm-0.23` | vLLM 0.23 | `vllm` | 0.23 | `torch >=2.0`; `vllm >=0.23,<0.24` |
| `sglang-0.5.10` | SGLang 0.5.10 | `sglang` | 0.5.10 | `torch >=2.0`; `sglang >=0.5.10,<0.6` |
| `native-hf` | Native HF | `native` | stable | `torch >=2.0`; `transformers >=4.40` |
| `mock` | Mock | `mock` | stable | None (`requires: []`) |

**Environment check fields** (`env.checks[]`):

| Field | Type | Description |
| --- | --- | --- |
| `name` | String | Dependency name (e.g. `torch`, `vllm`, `sglang`, `vllm-cli`) |
| `required` | String | Required version (`benchRequiredVersion`, e.g. `>=0.23,<0.24`) |
| `installed` | String | Installed version (`benchInstalled`); shows `benchNotInstalled` "not installed" when absent |
| `ok` | Boolean | Whether the individual check passed (OK / FAIL label) |
| `hint` | String | Install hint (`benchInstallHint`, e.g. `pip install 'vllm>=0.23,<0.24'`) |

## 4. Operating Steps

### 4.1 Viewing Engines and Environment Status

1. Click **Bench Engines** in the left menu.
2. Review the card header tags: Default engine / engine type / Mock / Real / Env OK / Env missing / version.
3. Review the environment requirements table at the bottom of the card: check required version / installed / OK / FAIL for each row; a FAIL row shows an install hint below it (e.g. `pip install 'vllm>=0.23,<0.24'`). Install the dependency as hinted, then refresh the page to re-validate.

### 4.2 Switching the Mock Toggle

1. At the bottom of the target engine card, find the **Mock environment & data** toggle (off by default = Real).
2. Click the toggle: when enabled, a toast reads "Mock enabled for this engine — using simulated data and a simulated runtime"; the card tag becomes Mock and the environment status shows Env OK (mock-environment passed). Click again to disable, and a toast reads "Mock disabled for this engine", restoring real environment validation.

<div class="warning">
**Warning:** Mock mode outputs **simulated data and a simulated runtime**; results do not represent real performance. Use it only for full-pipeline integration and demos in scenarios without a GPU / real inference service (see [Mock](/en/docs/tools/mock/)).
</div>

### 4.3 Create Engine (Authoring a Custom Engine)

1. Click **Create Engine** in the top-right of the panel to open the authoring guide dialog and read the four steps under "Authoring steps":
   1. Confirm the target framework and exact version (e.g. vllm 0.24); do not guess versions.
   2. Open the upstream bench entry file at that version tag and read the real parameters (never copy parameters across versions).
   3. Copy the prompt below to an AI, replace the framework and version, and generate the engine definition and parameter descriptions.
   4. Upload the generated `.yaml` or skill package `.tar.gz` via Upload Engine; it takes effect once validation passes.
2. Review "Upstream references (fixed per version tag)": vLLM (`https://github.com/vllm-project/vllm`, entry `vllm/benchmarks/serve.py`, command `vllm bench serve`) and SGLang (`https://github.com/sgl-project/sglang`, entry `python/sglang/bench_serving.py`, command `python -m sglang.bench_serving`); replace the version in the links with your target version.
3. Copy the "AI prompt" (replace the `<FRAMEWORK>` / `<VERSION>` placeholders yourself) and send it to an AI to generate the engine package, then close the dialog and import it with **Upload Engine**.

### 4.4 Upload Engine (Uploading an Engine Package)

1. Click **Upload Engine** in the top-right of the panel to open the upload dialog (hint: "Upload a .yaml engine definition or a .tar.gz skill package; it is only written after validation passes").
2. In the drop zone, click or drag in a file (the frontend checks the extension first: only `.yaml` / `.yml` / `.tar.gz` / `.tgz`, otherwise it shows "Only .yaml / .yml / .tar.gz / .tgz files are supported"; a single file must not exceed 20MB).
3. After selection, the dialog shows "File to import" and the file name (click to cancel and clear), then click **Validate & Import** at the bottom (disabled when no file is selected).
4. When the import finishes, review the result: added engine (`added`) / updated engine (`updated`) / individual checks (`checks`, OK / FAIL labels); the engine list refreshes automatically.

### 4.5 Engine Comparison

1. Click **Engine Comparison** in the top-right of the panel to open the comparison table dialog.
2. Compare all engines side by side across 6 dimensions: Engine Type, Environment, Test Target, Execution, Metric Basis, Install Size; close the dialog to return to the engine list.

## 5. Backend Execution Logic

### 5.1 Loading the Engine List

`GET /api/benchs` → the backend runs `list_engines(with_env=True)`: it parses the `engines` section of `benchs.yaml`, generates a summary per engine (`id` / `kind` / `origin` / `framework` / `version` / `name(_zh)` / `description(_zh)` / `highlights(_zh)` / `requires` / `eval`), runs `check_env` to attach `env: {ok, checks[]}`, then injects `mock` / `mock_state` per the `engine_mocks` mapping (**when Mock is enabled, env is overridden** with `{ok: true, mock: true, checks: [mock-environment]}`); it returns `{"engines": [...], "comparison": [...], "default_engine_id": "..."}` (`default_engine_id` is the first `kind=builtin` engine, currently `benchscope`). The frontend then calls `GET /api/benchs/authoring` to fetch the authoring guide (upstream links + AI prompt template). Comparison table data is returned with the `comparison` field (from the `comparison` section of `benchs.yaml`, 6 dimensions × N engines, including `*_zh` Chinese values), rendered by the frontend according to the UI language.

### 5.2 Environment Validation (`check_env`)

1. Iterates the engine's `requires` array: `_installed_version(name)` reads the local package version, and `_match_spec(installed, spec)` compares the version range (`>=2.0`, `>=0.23,<0.24`, etc.), producing one `checks` entry per item.
2. For native engines (`kind` is `vllm` / `sglang`) whose dependencies all pass, an **additional CLI availability check** is appended: `vllm-cli` (the `vllm` executable) / `sglang-cli` (the `sglang` python module).
3. Any failure → `env.ok = false` (the card shows "Env missing", and the failing item's `hint` shows the install hint); engines with `requires: []` always have `ok = true`; a single engine can also be checked via `GET /api/benchs/{engine_id}/env-check` (used by the create-task page); with Mock enabled, it likewise returns the mock-environment pass result.

### 5.3 Mock Toggle

`POST /api/benchs/{engine_id}/mock` (body `{"enabled": bool}`): an unknown `engine_id` returns **404**; `enabled=true` → `engine_mocks[engine_id] = true`, `enabled=false` → the key is removed (using a **whole-object replace** `config.set` rather than a recursive merge, to guarantee the removal takes effect); it is persisted to `~/.benchscope/settings.json` (the `engine_mocks` field), and the latest summary for that engine is returned (including the injected `mock` / `env`).

### 5.4 Uploading an Engine Package

`POST /api/benchs/upload` (FormData `file`, frontend timeout 120 seconds):

1. An empty file returns **400**; a file over **20MB** returns **400** ("Engine package too large (20MB limit)"); extensions are limited to `.yaml` / `.yml` / `.tar.gz` / `.tgz` (`import_engine_package`), otherwise 400.
2. `.tar.gz` / `.tgz`: safely extracted into a temp directory to collect yaml — a file containing an `engines` section is the engine definition (may include `comparison`), and `bench-params.yaml` / `params.yaml` are the parameter-description sections; `.yaml` / `.yml` is parsed directly and must contain a non-empty `engines` section.
3. In-package self-check: every engine must have a non-empty `id` that is unique within the package; `kind` must be one of `builtin` / `vllm` / `sglang` / `native` / `mock`.
4. Merged with the existing `benchs.yaml` by `id`: new `id`s are recorded in `added`, same `id` overwrites are recorded in `updated`; written to `configs/benchs.yaml` and `configs/bench-params.yaml`; returns `{"ok": true, "checks": [...], "added": [...], "updated": [...], "engines": [...]}`, and the frontend refreshes the engine list.

## 6. Frequently Asked Questions

**Question: The environment status shows "Env missing" — what should I do?**

Check the install hint (`hint`, e.g. `pip install 'vllm>=0.23,<0.24'`) on the FAIL rows of the environment requirements table at the bottom of the card, install it, and refresh the page to re-validate. Native engines require not only the package version but also **command-line availability** (the `vllm` executable / the `sglang` python module). If no real environment is available, enable the engine's **Mock toggle** to run full-pipeline integration with simulated data (see [Mock](/en/docs/tools/mock/)).

**Question: With the Mock toggle enabled, are test results real data?**

No. Mock mode uses **simulated data and a simulated runtime** (skipping real framework dependency checks), suited for full-pipeline integration and demos without a GPU / real inference service; results do not represent real performance. See [Mock](/en/docs/tools/mock/) and [Bench Engines](/en/docs/tools/bench-engine/).

**Question: How do I troubleshoot a failed engine package upload?**

Check in order: the extension is `.yaml` / `.yml` / `.tar.gz` / `.tgz`; the size is ≤ 20MB; the yaml contains a non-empty `engines` section; every engine `id` is non-empty and unique within the package (the same `id` **overwrites and updates**, recorded in `updated`; a different `id` adds a new entry, recorded in `added`; `name` is display-only and not used for deduplication); `kind` is within `builtin` / `vllm` / `sglang` / `native` / `mock`. The `checks` area of the upload dialog shows OK / FAIL and the reason for each item.