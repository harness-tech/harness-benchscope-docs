---
title: "Dashboard Overview"
description: "Dashboard page: statistics overview (performance / accuracy / sessions / built-in skills / models / datasets / Provider counts), environment info (hardware / operating system / network / framework versions), and the latest performance records."
---

# Dashboard Overview

The Dashboard is the **home page** of BenchScope (route `/dashboard`, with `/` redirecting here by default), presenting the platform's running status in one place: resource counts, environment information, and the latest performance records. This is the page you land on after starting `benchscope`.

![BenchScope Dashboard overview](/images/benchscope-dashboard.png)

## Statistics Overview

The first-row left card shows the resource counts of each platform module:

| Counter | Meaning |
| --- | --- |
| Performance | Number of completed performance stress-test runs. |
| Accuracy | Number of completed accuracy evaluation runs. |
| Sessions | Current number of sessions. |
| Skills (built-in) | Number of built-in skills (currently 3, see [Built-in Skills](/en/docs/tools/skills/)). |
| Models | Number of model download records (not yet implemented, defaults to 0). |
| Datasets | Number of dataset download records (not yet implemented, defaults to 0). |

At the bottom of the card is the **Providers full-width row**: number of Providers + number of Provider models (the total number of models probed across all Providers).

## Environment Info

The first-row right card shows the runtime environment along four dimensions:

| Dimension | Fields |
| --- | --- |
| Hardware environment | Hostname (Host), CPU, memory (Memory), GPU. |
| Operating system | System name (OS), system version (OS Version), kernel (Kernel). |
| Network environment | Listed per network interface: MAC address (IPv4), IP address, subnet (Subnet), mask (Mask). |
| Framework versions | Versions of Python, PyTorch, vLLM, SGLang, benchscope (showing — when not installed). |

<div class="info">

**Info**:

Environment info is especially useful when **comparing stress-test results across different machines** — mismatched hardware / framework versions make throughput and latency not directly comparable.

</div>

## Performance Test Records

The second-row card shows the **latest 8** performance stress-test records (no pagination):

| Column | Meaning |
| --- | --- |
| Run ID | Run number. |
| Model | Model under test. |
| Framework | Inference framework (vLLM / SGLang, etc.). |
| Status | Status (done / running / stopped / error). |
| Time | Start time. |
| Detail | Click to jump to **Datas → Perfs** and select the corresponding record. |

> The accuracy records panel (Eval Records) is currently hidden (coming soon); manage accuracy evaluation artifacts on the [Accuracy page](/en/docs/accuracy/).

## FAQ

**Question: The Dashboard counters don't match the record counts in Datas?**

The Dashboard counters count **completed runs**; Datas → Perfs lists all records (including in-progress / failed). Different scopes are normal.

**Question: Why are the Models / Datasets counters always 0?**

Model / dataset download counters are not yet implemented and default to displaying 0; download management is done in [Settings → Models / Datasets](/en/docs/tools/settings/).

**Question: What does the GPU field in the environment info show?**

It shows the GPU models and counts detected by the system (e.g., cards visible in nvidia-smi); environments without a GPU show —.

## Related docs

- [Starting the Platform](/en/docs/quickstart/platform/) — first launch and first look at the Dashboard
- [Data & Statistics (Datas)](/en/docs/data/) — full history record management
- [Settings](/en/docs/tools/settings/) — Provider / model / dataset management
- [Built-in Skills](/en/docs/tools/skills/) — source of the Skills counter