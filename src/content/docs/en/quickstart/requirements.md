---
title: "Requirements"
description: "Python version, target inference service, network/browser, and optional GPU prerequisites for running BenchScope."
---

# Requirements

This page lists the environment prerequisites for running BenchScope. Once you meet them, follow the [Quick Install](/en/docs/quickstart/) to install and start the platform.

## Python and pip

- **Python**: 3.10 or later recommended (3.9 / 3.11 / 3.12 also supported). The package is pure Python.
- **pip** — keep it reasonably recent so dependencies resolve correctly (`pip install --upgrade pip`).

## The Inference Service Under Test

BenchScope does not host models itself — you need an inference service to test:

- a local **vLLM / SGLang** server (for example at `http://127.0.0.1:8000`), or
- any **OpenAI-compatible** remote endpoint (Base URL + API Key).

<div class="info">

**Info:**

BenchScope's Web frontend is fully bundled inside the Python package, so you do not need to install Node.js or any frontend dependencies — a single command starts the whole platform.

</div>

## Network and Browser

- **Network** — access to PyPI during installation, and to your inference service under test when stress-testing.
- **Browser** — a modern browser such as Chrome / Edge / Firefox (Chrome recommended).

## GPU (optional)

A GPU is only required if you plan to use **Native accuracy** evaluation (offline evaluation with local weights). BenchScope itself does **not** need a local GPU.

<div class="tip">

**Tip:**

If you plan to use **Native accuracy** evaluation, install the optional extra: `pip install benchscope[accuracy-native]`.

</div>

## FAQ

**Question: Can I run BenchScope without a GPU?**
Yes. BenchScope only sends requests and collects results; a GPU is needed only by the inference service under test, or for Native accuracy evaluation.

**Question: Do I need to install vLLM / SGLang myself?**
No. You deploy the inference service under test yourself (locally or remotely); BenchScope only runs the stress tests and evaluations against it.

**Question: Do I need Node.js or frontend dependencies?**
No. The Web frontend is fully embedded in the Python package.

## Related Docs

- [Quick Start](/en/docs/quickstart/) — feature overview and installation
- [Starting the Platform](/en/docs/quickstart/platform/) — launch the Web platform with one command
- [Install](/en/docs/install/) — installation and startup details
- [Configuration](/en/docs/install/configuration/) — data root directory and settings.json
