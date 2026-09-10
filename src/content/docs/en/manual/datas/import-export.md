---
title: "Import, Export, and Backup"
description: "Datas import / export / backup manual: button operations, input parameters, and backend execution logic (including zip-slip / path-traversal protection) plus FAQs for backup zip, import / recovery, and share PNG."
---

# Import, Export, and Backup

Datas supports **backup** (export to zip), **import** (restore from zip), and **share** (export as PNG image) for performance records, so you can migrate historical records between different machines / environments, or share results as images.

## 1. Feature Overview

| Feature | Entry point | Artifact / behavior | Direction |
| --- | --- | --- | --- |
| Backup | **Backup** button on row 1 of the detail | Downloads `{run_id}.zip` (run directory + terminal logs) | Export |
| Import | **Import** button on the left list → drawer | Restores one record from a zip to local | Restore |
| Share | **Share** button on row 1 of the detail | Downloads `{run_id}.png` (full-page screenshot of the detail) | Export |

<div class="info">

**Info:**

Backup / import targets **performance records** (`kind=perf`); the artifact is a flat zip. Accuracy evaluation artifacts (`evals/`) are migrated together with the entire data directory and are not imported / exported here.

</div>

## 2. Page Structure

```
Left list title bar:  [Import (upload icon)]  [Refresh (circular icon)]

Detail row-1 title bar:  <run_id>   [Delete] [Backup] [Share]

Import drawer (right side, 360px):
┌──────────────────────────────┐
│  Import record               │
│  Import hint (importTip)     │
│  [Upload zip archive]        │
│  Progress bar (uploading)    │
│  Result: success / exists / failed │
│  [Cancel]                    │
└──────────────────────────────┘
```

## 3. Input Parameters and Field Constraints

| Field | Type | Constraints | Default | Description |
| --- | --- | --- | --- | --- |
| `file` (import) | file | Required, `.zip` only; `multipart/form-data`, field name `file` | — | The backup zip; non-zip uploads are rejected outright |
| zip contents | — | Must be **flat** files (no subdirectories, to prevent zip-slip) | — | Must contain at least `run.json` |
| `run.json` | json | Required; contains `run_id`, `kind` (perf / eval) | — | Used to identify the task ID and type |
| `run_id` | string | Single-level name; must not contain `/` `\` `..` (path-traversal protection) | Inferred from the zip | Target record directory name |
| Share target | — | The currently selected record | — | Pure frontend screenshot; no upload involved |

## 4. Button Operations

1. **Backup**: click **Backup** in the detail → confirmation dialog (backup confirm) → confirm → the browser downloads `{run_id}.zip`, with a "Backup complete" toast.
2. **Import**: click **Import** on the left → the drawer opens → click **Upload zip archive** to select a `.zip` → upload (with progress) → the result is shown:
   - **Import succeeded**: the record is restored and the list is refreshed.
   - **Already exists**: a record with the same `run_id` already exists; it is not overwritten.
   - **Import failed**: the error reason is shown (non-zip / missing `run.json` / unrecognizable `run_id`, etc.).
   - Click **Cancel** to reset the drawer.
3. **Share**: click **Share** in the detail → confirmation dialog (share confirm) → confirm → the browser downloads `{run_id}.png`, with a "Share complete" toast.

## 5. Execution Steps (Backup → Migrate → Import)

1. Select the source record on the Perfs page, click **Backup** and confirm, and obtain `{run_id}.zip`.
2. Copy the zip to the target machine (independent of the target machine's current `~/.benchscope/` directory contents).
3. On the target machine's Perfs page, click **Import** and choose the file via **Upload zip archive**.
4. Once "Import succeeded" appears, the record shows up in the list; click it to view.

## 6. Backend Execution Logic

| Operation | API | Processing logic |
| --- | --- | --- |
| Backup | `GET /api/logs/runs/{run_id}/backup` | Collects all files in the run directory + terminal logs `logs/{kind}_{run_id}_*.log`, dedupes, packages them into a flat zip (`application/zip`), and returns it |
| Import | `POST /api/logs/runs/import` | See the flow below |
| Share | None (pure frontend) | `html2canvas` renders the full detail page to PNG (`scale=1.5`, temporarily expanding the scroll container to keep long pages complete), then triggers the download after `toDataURL` |

**Import flow (`POST /api/logs/runs/import`)**:

1. Read the uploaded bytes; empty content → 400.
2. Extract into a temporary directory, with **zip-slip protection**: only flat file names are accepted (entries containing `/` `\` `..` are skipped).
3. `run.json` must exist, otherwise 400 (task unidentifiable).
4. Parse `kind` (`perf` / `eval`, defaulting to `perf`); infer `run_id`: prefer `run.json.run_id`, otherwise extract it from the terminal log file name using the regex `^(perf|eval)_(.+)_\d{6}\d*\.log$`; if still none → 400.
5. If the target directory `perfs/<run_id>` (or `evals/<run_id>`) already exists → return `exists` (no overwrite).
6. Migrate the files: terminal logs (`.log` with the `perf_*` / `eval_*` prefix) go to `logs/`; all other files go to the run directory.
7. Return `ok`; the frontend refreshes the list.

<div class="warning">

**Warning:**

Import does **not** overwrite an existing `run_id` (it returns "exists"). To replace a record, first **delete** it on the Perfs page, then import. All paths are validated against traversal, and out-of-bounds files are rejected.

</div>

## 7. FAQ

**Question: Import says "already exists"?**
The target machine already has a record with the same `run_id`. **Delete** the old record first, then import, or use a different record.

**Question: Import fails with "not a valid zip archive"?**
Make sure you uploaded the **zip exported by Backup** (flat structure, containing `run.json`), not a compressed directory or a corrupted file.

**Question: What files are inside the backup zip?**
All files in the run directory (`run.json`, `live/*.json`, summary / logs, etc.) + the corresponding terminal logs `logs/{kind}_{run_id}_*.log`, all stored flat.

**Question: The shared image is incomplete (truncated)?**
The frontend temporarily expands the scroll container before taking the screenshot; if it is still incomplete, lower the browser zoom level and retry, or use **Backup** instead to preserve the complete data.

## 8. Related Docs

- [Performance Record Management](/en/docs/manual/datas/perfs/) — the page hosting the backup / share entry points
- [Datas Manual Overview](/en/docs/manual/datas/) — entry to the module
- [Datas Overview (Reference)](/en/docs/data/) — backup / import concepts
- [API Reference](/en/docs/api/) — `/api/logs/runs/{id}/backup`, `/api/logs/runs/import`