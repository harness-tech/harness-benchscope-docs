# Contributing

You are welcome to contribute to BenchScope as **open source** through Issues / PRs. This page describes how the project is organized and how to contribute cleanly.

## Related Links

- **Source repository**: <https://github.com/LABELNET/benchscope>
- **Download / releases**: <https://pypi.org/project/benchscope>
- **License**: Apache License 2.0

## Local Development Environment

Read the root documentation before you start — it explains how the project is structured and maintained:

- `docs/Readme.md` — documentation structure
- `agents/Readme.md` — project-level maintenance conventions

While developing, please follow these conventions:

- **Documentation sync** — developing or updating a feature must be accompanied by updating the corresponding documentation (`docs/prds/`, `docs/versions/`, `docs/rules/`, and so on).
- **Testing** — run the `tests/` test suite before committing.
- **Minimal changes** — keep changes focused, and follow the repository’s **naming** and **i18n** conventions.

## Testing

Run the test suite before you commit:

```bash
pytest
```

Make sure any changes you make come with tests where appropriate, and that the full suite still passes.

::: tip
Because the project tracks Chinese / English documentation with i18n conventions, keep your user-facing strings and docs bilingual-friendly when adding new UI text.
:::

## Contribution Workflow

1. **Fork the repository** and create a feature branch.
2. **Write / adjust features**, and add tests and documentation for them.
3. **Run the tests** to confirm they pass.
4. **Submit a PR** describing the changes and the test results.

## See Also

- [Architecture](architecture.md) — understand the codebase before you start
- [Bench Engine](bench-engine.md) — how engines are integrated (a common extension point)
