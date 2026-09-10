---
title: "Overview"
description: "Help hub for BenchScope: troubleshooting common issues, reporting bugs and feature requests, and a guide to contributing."
---

# Overview

Running into a problem or want to contribute? Start here.

## FAQ / Troubleshooting

- **Browser did not open on startup**: make sure you are not using `--no-browser`, or visit the printed address manually.
- **`http://127.0.0.1:8080` does not respond**: confirm the service is still running and the port is not taken (try a different `--port`).
- **Many benchmark requests fail**: check `--base-url`, API key, `--timeout`, and concurrency settings; make sure the target service is reachable.
- **Native mode is blocked**: install the optional dependency with `pip install benchscope[accuracy-native]` and retry.
- **Cannot find a historical task**: make sure the data root directory was not cleaned / `BENCHSCOPE_DATA_DIR` was not changed, or restore it by importing a backup.

<div class="tip">

**Tip:**

For more specific issues, see the FAQ section of each feature page and the backup / import notes in [Datas](/en/docs/data/).

</div>

## Report a Bug / Request a Feature

Please open a GitHub **Issue** (bug report, feature request) or **Pull Request**:

- Source repo: https://github.com/LABELNET/benchscope
- Docs repo: https://github.com/harness-tech/harness-benchscope-docs
- Download / releases: https://pypi.org/project/benchscope

## Contributing

For the local development environment, tests, and the contribution flow, see [Contributing](/en/docs/help/contributing/).

## Related

- [Quick Start](/en/docs/quickstart/) — get started here
- [Install](/en/docs/install/) — requirements, updates and uninstall
- [Releases](/en/docs/releases/) — version release notes
