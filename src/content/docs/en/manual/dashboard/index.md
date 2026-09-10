---
title: "Dashboard Manual Overview"
description: "BenchScope Dashboard manual overview: page structure of the read-only home page, statistics overview cards, environment info panel, test records (latest 8), and the manual chapter index."
---

# Dashboard Manual Overview

The Dashboard is the **home page** of the BenchScope WebUI (nav label "Dashboard", i18n key `dashboard`, route `/dashboard`, `/` redirects here). It is a **read-only display page**: it aggregates platform resource statistics, the runtime environment, and the latest performance test records, and provides no entry point for launching tests or modifying configuration.

## 1. Feature Description

The Dashboard consists of three panels:

| Panel | i18n key | Card title display | Content | Manual chapter |
| --- | --- | --- | --- | --- |
| Statistics Overview | `overview` | Overview | Six statistics (performance / accuracy / sessions / skills / models / datasets) + Provider count and Provider models | [Statistics Overview & Environment Info](/en/docs/manual/dashboard/overview/) |
| Environment Info | `envInfo` | Envs info | Hardware environment, operating system, network environment, framework versions | [Statistics Overview & Environment Info](/en/docs/manual/dashboard/overview/) |
| Test Records | `perfTestRecords` | Perf Records | Latest 8 performance test records, "Detail" navigation | [Test Records](/en/docs/manual/dashboard/records/) |

<div class="tip">

**Tip:**

The Dashboard is a **read-only** page; the only interactive controls are the **Refresh**, **More**, and **Detail** buttons on the test records panel. Launch performance / accuracy tests and configure Providers on the corresponding feature pages.

</div>

## 2. Page Structure

```
┌─────────────────────────────────│──────────────────────────────────┐
│ Statistics Overview (overview)  │ Environment Info (envInfo)       │
│ Performance │ Accuracy          │ Hardware: host/CPU/memory/GPU    │
│ Sessions │ Skills (built-in)    │ OS: OS/version/kernel            │
│ Models │ Datasets               │ Network: MAC/IP/subnet/mask      │
│ Providers │ Provider Models     │ Frameworks: Python/Pytorch/      │
│                                 │ vLLM/SGLang/benchscope           │
├─────────────────────────────────│──────────────────────────────────┤
│ Test Records (perfTestRecords)      [Refresh] [More]               │
│ Run ID │ Model │ Framework │ Status │ Time │ Detail                │
│ (max 8 rows, no pagination, no search box)                         │
│                               *Only the latest 8 records are shown │
└────────────────────────────────────────────────────────────────────┘
```

- Row 1: the Statistics Overview and Environment Info cards sit side by side (grid `xs=24 / lg=12`), stacking vertically on narrow screens.
- Row 2: the Test Records card spans the full width; the footer shows `*Only the latest 8 records are shown`.

## 3. Manual Chapter Index

| No. | Chapter | Content |
| --- | --- | --- |
| 1 | [Statistics Overview & Environment Info](/en/docs/manual/dashboard/overview/) | The six statistics, Provider counts, hardware / network / framework environment probing logic, field constraints |
| 2 | [Test Records](/en/docs/manual/dashboard/records/) | The latest 8 records, column field constraints, Detail / More / Refresh operations, Perf request details and downloads |

## 4. Related Docs

- [Dashboard Overview (reference docs)](/en/docs/tools/dashboard/) — concept-oriented page description
- [Performance Record Management (Datas manual)](/en/docs/manual/datas/perfs/) — full record list, detail panel, file downloads
- [Settings (reference docs)](/en/docs/tools/settings/) — configuration entry for Providers, models, datasets, etc.

<div class="info">

**Info:**

The Statistics Overview and Environment Info cards **load automatically** when the page opens, with no button click required; see [Statistics Overview & Environment Info · Backend Execution Logic](/en/docs/manual/dashboard/overview/) for the backend data-fetching flow of each metric.

</div>