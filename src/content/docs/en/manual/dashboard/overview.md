---
title: "Statistics Overview & Environment Info"
description: "Dashboard statistics overview panel: the six statistics (performance / accuracy / sessions / skills / models / datasets) and Provider counts, plus environment info panel fields (hardware / operating system / network / framework versions), with field constraints and backend probing logic."
---

# Statistics Overview & Environment Info

The first row of the Dashboard holds two read-only cards side by side: **Statistics Overview** on the left (`overview`, six statistics + Provider block) and **Environment Info** on the right (`envInfo`, title displayed as "Envs info"). Both load automatically when the page opens; the cards themselves have no refresh button (the test records panel's **Refresh** re-fetches the statistics in sync).

## 1. Feature Description

- **Statistics Overview**: aggregates the counts of various records / resources across the platform — performance records, accuracy records, sessions, built-in skills, models, datasets, plus the Provider count and total Provider models.
- **Environment Info**: shows the host hardware, operating system, network interfaces, and relevant framework versions, used to document the test environment before and after benchmark runs.

Tip: before comparing benchmark results across different machines, check the hardware and framework versions in this panel first — when GPU or vLLM / SGLang versions differ, throughput and latency results are not directly comparable.

## 2. Page Structure

```
┌──────────────────────────────────────│──────────────────────────────────────┐
│ Statistics Overview (overview)       │ Environment Info (envInfo)           │
│  ┌────────────┬────────────┐         │  ┌────────────────┬────────────────┐ │
│  │ Performance│  Accuracy  │         │  │ Hardware       │ OS             │ │
│  │ Sessions   │ Skills     │         │  │ host/CPU/memory│ OS/system ver/ │ │
│  │ (built-in) │            │         │  │ GPU            │ kernel version │ │
│  ├────────────┼────────────┤         │  ├────────────────┼────────────────┤ │
│  │ Models     │ Datasets   │         │  │ Network        │ Frameworks     │ │
│  └────────────┴────────────┘         │  │ per iface: MAC │ Python/Pytorch/│ │
│  ┌────────────┬────────────┐         │  │ IP/subnet/mask │ vLLM/SGLang/   │ │
│  │ Providers  │ Provider   │         │  │                │ benchscope     │ │
│  │ count      │ Models     │         │  └────────────────┴────────────────┘ │
│  └────────────┴────────────┘         │                                      │
└──────────────────────────────────────│──────────────────────────────────────┘
```

- Statistics Overview: a 2×3 main grid (the six statistics) + a Provider block at the bottom (Providers / Provider Models in two small cells side by side).
- Environment Info: a 2×2 set of four boxes: Hardware / OS / Network / Frameworks.

## 3. Metrics and Field Constraints

Both cards are **pure display** with **no input parameters** (read-only panels; all data loads automatically when the page opens). The input parameter table below documents this explicitly; field constraints follow in 3.1–3.3.

**Input Parameters**

| Field | i18n key | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| — | — | — | — | — | No input fields: both cards are read-only display panels; every value is fetched automatically on page load. |

### 3.1 Statistics Overview Metrics

| Metric | i18n key | Data source (API) | Returned field | Description |
| --- | --- | --- | --- | --- |
| Performance | `perfCount` | `GET /api/dashboard/stats` | `total_runs` | Number of performance test records (`kind != eval`, excluding accuracy records) |
| Accuracy | `accCount` | `GET /api/dashboard/stats` | `total_acc_runs` | Number of accuracy test records (`kind = eval`); displays 0 when missing |
| Sessions | `sessions` | `GET /api/sessions` | `sessions.length` | Current number of sessions |
| Skills (built-in) | `skills` + `builtin` | `GET /api/skills` | `skills.length` | Number of built-in skills |
| Models / Datasets | `modelsTab` / `datasetsTab` | — | — | Number of model / dataset download records; not yet implemented, defaults to 0 |
| Provider count | `providerCount` | `GET /api/config/providers` | `providers.length` | Number of configured inference Providers |
| Provider models | `providerModelCount` | `POST /api/config/test-connection` | Σ `models.length` | The backend probes each Provider's `{base_url}/v1/models` in parallel and sums the results; Providers that fail probing count as 0 |

<div class="warning">

**Warning:**

BenchScope itself does **not expose** an OpenAI-compatible `/v1/*` inference endpoint. The Provider model count is a read-only probe of an external **Provider's** model-list API `{base_url}/v1/models` (not an inference request).

</div>

<div class="tip">

**Tip:**

`en.js` still retains the legacy metric keys `totalPerfsRecords` (Total Perf Records), `totalAccRecords` (Total Acc Records), `maxPerfRecords` (Max Perf Records), `maxAccRecords` (Max Acc Records), `runningTasks` (Running Tasks), and `envStatusLabel` (Test Env Status). The current page **no longer displays** these metrics.

</div>

### 3.2 Environment Info Fields

| Box | Field (display name) | i18n key | Returned field | Collection method |
| --- | --- | --- | --- | --- |
| Hardware | Host | `host` | `hardware.host` | `platform.node()` (hostname) |
| Hardware | CPU | — | `hardware.cpu` | Linux reads `model name` from `/proc/cpuinfo`; macOS uses `sysctl`; core count appended |
| Hardware | Memory | `memory` | `hardware.memory` | Linux reads `MemTotal` from `/proc/meminfo`; macOS uses `sysconf`; converted to GB |
| Hardware | GPU | — | `hardware.gpu` | Probed by `detect_gpu()`, format `model × count` |
| OS | OS | `os` | `os.name` | `platform.system()` |
| OS | System version | `osVersion` | `os.version` | Linux reads `PRETTY_NAME` from `/etc/os-release`; macOS uses `mac_ver` |
| OS | Kernel version | `kernel` | `os.kernel` | `platform.release()` |
| Network | Interface name | — | `network[].iface` | Enumerates non-virtual interfaces (see constraints in 3.3) |
| Network | MAC | `netUuid` | `network[].mac` | Linux runs `ip -o link show`; macOS parses `ether` from `ifconfig` |
| Network | IP | `netIp` | `network[].ip` | Linux runs `ip -o -4 addr show` (IPv4 only); macOS parses `inet` from `ifconfig` |
| Network | Subnet | `netSubnet` | `network[].subnet` | Computes the network address from IP + mask |
| Network | Mask | `netMask` | `network[].mask` | Converts a CIDR prefix (Linux) or hex mask (macOS) to dotted decimal |
| Frameworks | Python | — | `versions.python` | `sys.version` |
| Frameworks | Pytorch / vLLM / SGLang / benchscope | — | `versions.pytorch` / `versions.vllm` / `versions.sglang` / `versions.benchscope` | Reads the `torch` / `vllm` / `sglang` / `benchscope` package versions via `importlib.metadata` |

### 3.3 Field Constraints

| Constraint | Rule |
| --- | --- |
| Read-only | All fields are read-only; changes must be made on the Settings page or from the command line. |
| Missing display | Any field that fails to collect returns `None`; the frontend displays `—` uniformly. |
| Interface filtering | Virtual interfaces prefixed `docker` / `veth` / `br-` / `virbr` / `cni` / `flannel` / `lo` / `tun` / `utun` are not displayed. |
| Interface count | One block per interface (MAC / IP / Subnet / Mask); if all are filtered out, the Network box shows a single `—` row. |
| Metric refresh | Neither card has an independent refresh button; clicking **Refresh** on the test records panel re-fetches `/api/dashboard/stats` in sync. |

## 4. Operation Steps

1. Start the BenchScope service and open the WebUI (route `/dashboard`; `/` redirects automatically).
2. The page finishes loading automatically (fetch order in Section 5); no clicks are required.
3. On the **Statistics Overview** card, review the six statistics and the Provider block.
4. On the **Environment Info** card, review the Hardware / OS / Network / Frameworks boxes.
5. (Optional) Click **Refresh** in the top-right of the test records panel to re-fetch `/api/dashboard/stats` in sync and update the performance / accuracy counters. The same panel's **More** button opens the full record list under Datas → Perfs, and the per-row **Detail** button selects a task there; see [Test Records](/en/docs/manual/dashboard/records/).
6. (Optional) Verify the platform version: use `pip show benchscope` or `GET /api/version`. The `benchscope` version in the Frameworks box comes from `importlib.metadata`.

## 5. Backend Execution Logic

### 5.1 Page Load Order (frontend `onMounted`)

| Order | Frontend function | API calls | Purpose |
| --- | --- | --- | --- |
| 1 | `loadRuns()` | `GET /api/logs/runs` | Fetch all run records (shared by the test records panel) |
| 2 | `loadStats()` / `loadAccRuns()` | `GET /api/dashboard/stats` + `GET /api/logs/runs` | Fetch performance / accuracy counters (the accuracy records panel is currently hidden, reserved) |
| 3 | `loadEnv()` | `GET /api/dashboard/env` | Fetch environment info |
| 4 | `config.refreshStatus()` | `GET /api/config/status` | Refresh service status (top bar) |
| 5 | `loadOverviewCounts()` | `GET /api/sessions` + `GET /api/skills` + `GET /api/config/providers` (`Promise.allSettled` in parallel), then `POST /api/config/test-connection` for each Provider | Sessions / skills / Provider counts + total Provider models |

The `POST /api/config/test-connection` in step 5 is triggered after the Provider list returns: for each Provider, send `{base_url, endpoint, api_key, extra_headers}`; the backend performs `GET {base_url}/v1/models` (6-second timeout, with `Authorization: Bearer <api_key>` and the extra headers) and returns `models` (a list of model ids); the frontend accumulates `length` for each successful result, and failed Providers count as 0.

### 5.2 `GET /api/dashboard/stats` Aggregation Logic

1. Iterate over the record directories `~/.benchscope/perfs` and `~/.benchscope/evals` (legacy subdirectories under `~/.benchscope/logs` are included as well when they contain a `run.json`).
2. Read each subdirectory's `run.json` (skipping the `tasks` directory); `kind == "eval"` counts as an accuracy record.
3. Return `total_runs` (performance record count = total − accuracy count), `total_acc_runs`, `best_acc` (max `summary.accuracy` across accuracy records), `running_tasks` (number of performance + accuracy tasks running in memory), and `avg_tpot` with `best_model` (aggregated from performance records' `rows[].metrics.tpot_mean`).

### 5.3 `GET /api/dashboard/env` Probing Logic

The backend calls `collect_env_info()`; all four categories of collection are fault-tolerant (missing items are `None`):

- **Hardware**: `platform.node()`; CPU model + core count; total memory; `detect_gpu()`.
- **OS**: `platform.system()` / `platform.release()` + `/etc/os-release` (Linux) or `mac_ver` (macOS).
- **Network**: Linux runs `ip -o -4 addr show` and `ip -o link show`; macOS runs `ifconfig`. After filtering out virtual interfaces, converts CIDR prefixes to dotted-decimal masks, then computes the subnet address from IP + mask.
- **Frameworks**: `sys.version` and the `torch` / `vllm` / `sglang` / `benchscope` package versions read via `importlib.metadata`.

## 6. FAQ

**Question: Why are the Models / Datasets counters always 0?**

The model / dataset download record counts are not yet implemented; the frontend defaults to 0. Dataset download management is done on the Settings page.

**Question: Why does the Environment Info show `—` for the GPU or a framework version?**

The corresponding probe failed or the package is not installed (e.g. `vllm` / `sglang` not installed). This is normal and does not affect platform operation.

**Question: Where did the legacy "Test Env Status" and "Running Tasks" metrics go?**

These metrics (i18n keys `envStatusLabel`, `runningTasks`, etc.) are no longer displayed after the page redesign; the service status is now shown in the top bar.

**Question: How do I verify the BenchScope version?**

The Frameworks box shows the `benchscope` package version read via `importlib.metadata`. You can also use `pip show benchscope` or `GET /api/version`.