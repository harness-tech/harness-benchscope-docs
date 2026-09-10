---
title: "Contributing"
description: "Contributing to BenchScope: local development setup, how to run tests, the contribution workflow, and a pre-submit checklist."
---

# Contributing

You are welcome to contribute to the open-source BenchScope project via **Issues / PRs** — whether it is fixing bugs, adding features, improving documentation, or extending tests.

## Related Links

- **Source repository**: https://github.com/LABELNET/benchscope
- **Download / releases**: https://pypi.org/project/benchscope
- **License**: Apache License 2.0

<div class="info">

**Info:**

Before you submit, read the root documentation — it explains how the project is structured and maintained.

</div>

## Local Development Environment

The repository root is organized as follows:

| File | Description |
| --- | --- |
| `docs/Readme.md` | Documentation structure and planning |
| `agents/Readme.md` | Project-level maintenance conventions |

While developing, please follow these conventions:

- **Documentation sync** — developing or updating a feature must be accompanied by updating the corresponding documentation (`docs/prds/`, `docs/versions/`, `docs/rules/`, and so on).
- **Testing** — run the `tests/` test suite before committing.
- **Minimal changes** — keep changes focused, and follow the repository’s naming and i18n conventions.

## Testing

Run the test suite before you commit:

```bash
pytest
```

<div class="tip">

**Tip:**

Make sure all related tests pass before submitting a PR, and add test cases when you introduce new functionality.

</div>

## Contribution Workflow

1. **Fork the repository** and create a feature branch.
2. **Write / adjust features**, and add tests and documentation for them.
3. **Run the tests** to confirm they pass.
4. **Submit a PR** describing the changes and the test results.

### Checklist

- [ ] Code style and naming follow the repository conventions
- [ ] New / changed functionality is documented
- [ ] Related tests cover the changes and pass (`pytest`)
- [ ] i18n strings are updated

## See Also

- [Architecture](/en/docs/tools/architecture/) — understand the code structure
- [Bench Engine](/en/docs/tools/bench-engine/) — engine abstraction and customization
- [Quick Start](/en/docs/quickstart/) — installation and usage
