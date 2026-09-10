---
title: Skills and Plugins
description: 'Operations manual for the Settings "Skills" and "Plugins" panels: 3 built-in skills, skill package downloads, prompt copying, the plugin-system placeholder, and backend execution logic.'
---

# Skills and Plugins

The **Skills** panel (menu key `skills`) displays BenchScope's **built-in skill list** (AI skill packages for the Bench engine authoring and benchmarking workflow), supporting viewing feature highlights / usage instructions / prompts, and allows **downloading skill packages** or **copying prompts**; the **Plugins** panel (menu key `plugins`) is a placeholder for the plugin system (coming soon).

## 1. Feature Overview

- **Built-in skill list**: AI skill packages for the Bench engine authoring and benchmarking workflow; download and install them, or copy the prompt, to start using them (each skill lives at `benchscope/skills/<skill-id>/SKILL.md` and is distributed with the package).
- **Feature highlights / Usage instructions / Prompt**: Each skill card shows feature highlights (unordered list), usage instructions (ordered list), and the full prompt (monospace text block), all displayed in Chinese and English according to the UI language.
- **Download skill**: Downloads the skill version package (`.tar.gz`); the backend preferentially returns the already-released local artifact, and packages one on the fly when no release exists.
- **Copy prompt**: Writes the skill prompt text to the clipboard; send it to an AI assistant to execute the workflow.
- **Plugin system**: Coming soon; the panel currently shows only placeholder copy (`pluginsDesc` "The plugin system is coming soon."); the plugin installation directory `plugins_dir` (default `~/.benchscope/plugins`) is already reserved in the directory scheme.

<div class="info">
**Info:** The Skills panel has no form inputs and only three operations: "view / copy prompt / download skill"; the skill list is generated dynamically by the backend scanning the `benchscope/skills/` directory. See [Skills](/en/docs/tools/skills/).
</div>

## 2. Page Structure

```
[Skills panel]                                    [Plugins panel]
+-----------------------------------------------+  +------------------------------+
| Skills (skills)                               |  | Plugins (plugins)            |
| Built-in skill list: for Bench engine         |  | The plugin system is         |
| authoring and...                              |  | coming soon.                 |
+-----------------------------------------------+  | (Empty state: no data)       |
| Skill cards (one per skill, full-page scroll) |  +------------------------------+
| bs-engine-create  [bs-engine-create]  v1.2.0  |
| Create a custom Bench Engine package...       |
| Feature highlights:                           |
|  - Define custom bench engines via yaml...    |
| Usage instructions:                           |
|  1. Download skill: download the package      |
|     (.tar.gz)...                              |
|  2. Copy prompt: send the prompt below to an  |
|     AI...                                     |
| Prompt:                                       |
| +-------------------------------------------+  |
| | You are using the bs-engine-create skill..|  |
| +-------------------------------------------+  |
| [Download skill]    [Copy prompt]              |
+-----------------------------------------------+
```

| Area | Control / Content | Description |
| --- | --- | --- |
| Card header | Name + id tag (purple) + version (`v{version}`) | Version is taken from the `version` field of the `SKILL.md` frontmatter |
| Card body | Description, feature highlights (`skillFeatures`, unordered list), usage instructions (`skillUsage`, ordered list), prompt (`skillPrompt`, monospace text block) | Reads the `*_zh` / English fields according to the UI language |
| Card footer | **Download skill** (`skillDownload`) / **Copy prompt** (`skillCopyPrompt`) buttons | Text buttons (link style) |
| Plugins panel | Title + placeholder copy + empty state | No controls, no data |

## 3. Input Parameters

The Skills panel has **no form inputs**; the only input is the skill id of the download API:

| Endpoint | Parameter | Type | Constraint | Description |
| --- | --- | --- | --- | --- |
| `GET /api/skills` | None | — | — | Returns the built-in skill list `{skills: [...]}` |
| `GET /api/skills/{skill_id}/download` | `skill_id` (path parameter) | String | Required; enum of the current built-in skill ids (see table below) | Downloads the skill version package (`.tar.gz`); on failure the frontend falls back to downloading the `SKILL.md` text |

**Built-in skills** (`benchscope/skills/`, 3 in total):

| id | Name | Version | Purpose |
| --- | --- | --- | --- |
| `bs-engine-create` | bs-engine-create | 1.2.0 | Create a custom Bench Engine (vLLM / SGLang, etc.) package: import-time validation + Mock data verification + dynamic feature registration |
| `bs-perfs-concurrency` | bs-perfs-concurrency | 1.0.0 | Concurrency load testing with `benchscope perf`: built-in form + saving tasks / logs + generating a package importable into Datas/perfs |
| `bs-perfs-threshold` | bs-perfs-threshold | 1.0.0 | Threshold-search load testing with `benchscope perf --mode threshold`: built-in form + saving tasks / logs + generating a package importable into Datas/perfs |

Skill object fields: `id` / `name` / `version` / `description(_zh)` / `features(_zh)` / `usage(_zh)` / `prompt(_zh)` / `download` (`SKILL.md` path) / `download_url` (`/api/skills/<id>/download`) / `package` (`<id>-<version>.tar.gz`).

## 4. Operating Steps

### 4.1 Viewing Skills

1. Click **Skills** in the left menu.
2. Browse the skill cards: name + id tag + version (header); description, feature highlights, usage instructions, prompt (body).
3. When the UI language is switched to Chinese, each text block automatically shows the Chinese content (`*_zh` fields).

### 4.2 Copying a Prompt

1. At the bottom of the target skill card, click the **Copy prompt** button.
2. The skill prompt text is written to the clipboard (toast: "Prompt copied"; when the clipboard is unavailable: "Copy failed, please select and copy manually").
3. Paste the prompt into any AI assistant and follow its workflow (e.g. have the AI ask for the framework and version, then generate the engine package).

### 4.3 Downloading a Skill

1. At the bottom of the target skill card, click the **Download skill** button.
2. The browser downloads the skill version package `.tar.gz` (file name like `bs-engine-create-1.2.0.tar.gz`), toast: "Skill package downloaded".
3. Import the skill package into any agents platform that supports skills to use it.

## 5. Backend Execution Logic

### 5.1 Loading the Skill List

`GET /api/skills` -> the backend runs `_collect_skills()`:

1. Scans the subdirectories of `benchscope/skills/` (sorted by directory name), skipping directories without a `SKILL.md`.
2. Parses the YAML frontmatter of each `SKILL.md` (`---` delimited): reads `name`, `description`, `version` (default `1.0.0`).
3. Merges built-in supplementary metadata `_SKILL_EXTRA` (bilingual `description_zh` / `features(_zh)` / `prompt(_zh)`; when there is no supplement, the full `SKILL.md` text is used as the prompt).
4. Produces the `download` (`SKILL.md` path), `download_url` (`/api/skills/<id>/download`), and `package` (`<id>-<version>.tar.gz`) fields, and returns `{"skills": [...]}`.

### 5.2 Downloading a Skill Package

`GET /api/skills/{skill_id}/download`:

| Step | Logic |
| --- | --- |
| 1. Locate the skill directory | `benchscope/skills/<skill_id>/` does not exist or has no `SKILL.md` -> returns **404** |
| 2. Read the version number | Parses `version` from the `SKILL.md` frontmatter |
| 3. Prefer the released artifact | `skills/<skill_id>/dist/<skill_id>-<version>.tar.gz` exists -> returned directly via `FileResponse` (`application/gzip`) |
| 4. Package on the fly when unreleased | Runs `skills/<skill_id>/scripts/package.sh` (subprocess, **120-second timeout**) to package into a temp directory and returns the generated `.tar.gz`; no package script -> **404**; packaging failure -> **500** |

Frontend `downloadSkill`: requests `download_url` (`responseType: 'blob'`) -> triggers a browser download with `package.name` (e.g. `bs-engine-create-1.2.0.tar.gz`); **on request failure, it falls back** to packaging the skill prompt text into a `.md` file for download.

### 5.3 Copying a Prompt

Frontend `copySkillPrompt`: `navigator.clipboard.writeText(s.prompt)` writes to the clipboard (what is copied is the skill's **default English prompt** text, independent of the UI language); success toast "Prompt copied", error toast "Copy failed, please select and copy manually".

### 5.4 Plugins Panel

The **Plugins** panel is a static placeholder: it renders only the title (`plugins`) + copy (`pluginsDesc` "The plugin system is coming soon.") + empty state, with **no data loading and no API calls**; the plugin installation directory `plugins_dir` (default `~/.benchscope/plugins`) is already reserved in the directory scheme (see [General Settings](/en/docs/manual/settings/general/)).

## 6. Frequently Asked Questions

**Question: How do I use a skill after downloading the package?**

What you download is a `.tar.gz` skill package (e.g. `bs-engine-create-1.2.0.tar.gz`), which can be imported into any agents platform that supports skills (see [Skills](/en/docs/tools/skills/) for the skill list); alternatively, just click "Copy prompt" and send the prompt to an AI assistant to execute the workflow — no installation required.

**Question: Is the copied prompt the same as the one displayed on the card?**

The interface displays the localized prompt (the Chinese UI shows `prompt_zh`); the **Copy prompt** button copies the skill's **default English prompt** (the `prompt` field). The two have the same content in different languages.

**Question: Is the skill list fixed?**

Currently 3 skills are built in (`bs-engine-create`, `bs-perfs-concurrency`, `bs-perfs-threshold`), driven by the `SKILL.md` files under the `benchscope/skills/` directory; the backend scans that directory to generate the list dynamically, so a newly added skill directory appears in the list after the service is restarted.

**Question: When will the Plugins panel be available?**

The plugin system is coming soon; the panel is currently only a placeholder ("The plugin system is coming soon.") with no usable features; the plugin installation directory `plugins_dir` (default `~/.benchscope/plugins`) is already reserved in the directory scheme.