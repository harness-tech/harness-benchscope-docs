---
title: User Manual
description: "BenchScope User Manual overview: grouped by the Web navigation, covering the Dashboard, Performance, Accuracy, Sessions, Data and Settings modules with step-by-step operation guides."
---

# User Manual

This manual is **grouped by the six modules of the BenchScope Web navigation**. Each feature is split into a standalone document that walks through the **input parameters, field constraints, button actions, page structure, execution steps and backend logic**, so you can run a complete performance benchmark and accuracy evaluation from scratch.

<div class="tip">

**How to read:** For each module (Chapters 1–6), read the "Overview" first to understand the page structure and feature scope, then work through the numbered docs in order. Every document includes a **numbered table of contents** — use the TOC on the right to jump to a section.

</div>

## Table of Contents

### 1. Dashboard Manual
1.1 [Dashboard Overview](/en/docs/manual/dashboard/) — page structure, stat cards, environment info, test records
1.2 [Stat Overview & Environment](/en/docs/manual/dashboard/overview/) — six stat metrics, hardware/network/framework detection logic
1.3 [Test Records](/en/docs/manual/dashboard/records/) — latest 8 records, model search, request detail & download

### 2. Performance Manual
2.1 [Performance Overview](/en/docs/manual/performance/) — page structure, task list, task state machine
2.2 [Create a Benchmark Task](/en/docs/manual/performance/create-task/) — three-step wizard: performance conditions → parameters → start
2.3 [Concurrency & Threshold Modes](/en/docs/manual/performance/modes/) — parameters, constraints and scan logic for both modes
2.4 [Live Monitoring & Curves](/en/docs/manual/performance/live-metrics/) — Profile Progress, Real-Time Metrics, 12 live curves
2.5 [View & Export Results](/en/docs/manual/performance/results/) — stat charts, 13-column default table, Excel export

### 3. Accuracy Manual
3.1 [Accuracy Overview](/en/docs/manual/accuracy/) — page structure, task list, evaluation state machine
3.2 [Create an Evaluation Task](/en/docs/manual/accuracy/create-task/) — three-step wizard: pick dataset → mode & model → preview & start
3.3 [Datasets & Modes](/en/docs/manual/accuracy/datasets-modes/) — 9 built-in datasets, Serving/Native dual modes, scorers
3.4 [View & Trace Results](/en/docs/manual/accuracy/results/) — core metrics, baseline comparison, per-subject accuracy, single-sample trace

### 4. Sessions Manual
4.1 [Sessions Overview](/en/docs/manual/sessions/) — page structure, workspace, conversation list
4.2 [Create a Session](/en/docs/manual/sessions/create-session/) — pick Provider, model, quality level, thinking toggle
4.3 [Streaming Chat](/en/docs/manual/sessions/chat/) — SSE streaming output, token stats, generated files

### 5. Data Manual
5.1 [Data Overview](/en/docs/manual/datas/) — page structure, Perfs/Analysis tabs (Evals hidden)
5.2 [Performance Record Management](/en/docs/manual/datas/perfs/) — task records, detail panel, run directory, log files
5.3 [Data Analysis](/en/docs/manual/datas/analysis/) — record comparison, chart linkage, mean/median
5.4 [Import, Export & Backup](/en/docs/manual/datas/import-export/) — backup zip, import/restore, share PNG

### 6. Settings Manual
6.1 [Settings Overview](/en/docs/manual/settings/) — page structure, seven panels
6.2 [General Settings](/en/docs/manual/settings/general/) — theme, language, directories, inference API, data-dir change
6.3 [Provider Management](/en/docs/manual/settings/providers/) — add/manage Providers, models, test connection
6.4 [Model & Dataset Management](/en/docs/manual/settings/models-datasets/) — model catalog, vendor catalog, built-in dataset cache
6.5 [Engine Management](/en/docs/manual/settings/engines/) — engine types, env validation, Mock toggle, upload engine
6.6 [Skills & Plugins](/en/docs/manual/settings/skills-plugins/) — built-in skills, download, prompt copy, plugin system

## Relationship to the Reference Docs

<div class="info">

**User Manual vs Reference Docs:** This manual is an **operation-oriented** step-by-step guide ("how to click, how to fill, how it runs in the backend"), while the reference docs such as [Performance](/en/docs/performance/), [Accuracy](/en/docs/accuracy/), [CLI](/en/docs/cli/) and [API](/en/docs/api/) are **concept-oriented** explanations ("what it is, what metrics exist"). Run a full flow with this manual first, then consult the reference docs to deepen your understanding of the metrics and parameters.

</div>

## Prerequisites

<div class="warning">

**Before you start, make sure:**
1. The WebUI is started with [`benchscope serve`](/en/docs/cli/serve/) (default `http://localhost:8080`).
2. At least one working inference service is configured in [Provider Management](/en/docs/manual/settings/providers/) (or the Mock engine is enabled).
3. You have read [Quick Start](/en/docs/quickstart/) and [Installation](/en/docs/install/).

</div>

## Related Docs

- [Quick Start](/en/docs/quickstart/) — start BenchScope from scratch
- [Performance](/en/docs/performance/) — performance concepts and metrics
- [Accuracy](/en/docs/accuracy/) — accuracy concepts and metrics
- [CLI Reference](/en/docs/cli/) — full command-line parameters
- [API Reference](/en/docs/api/) — full REST API routes
- [Release Notes](/en/docs/releases/) — version change history