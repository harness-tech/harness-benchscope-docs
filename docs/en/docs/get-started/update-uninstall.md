# Update & Uninstall

This page explains how to upgrade BenchScope to the latest version, how to remove it, and what happens to your data.

## Update

BenchScope is distributed on PyPI. Upgrade to the latest version with pip:

```bash
pip install --upgrade benchscope
```

After the upgrade completes, **restart the service** for the new version to take effect:

```bash
# stop the running benchscope process first, then:
benchscope
```

::: tip
If you installed BenchScope inside a virtual environment, remember to activate that environment before running the upgrade command.
:::

To verify the installed version:

```bash
pip show benchscope
```

(or `benchscope --version` if available in your installed version).

## Uninstall

Remove the package with pip:

```bash
pip uninstall benchscope
```

If you also want to clean up the runtime data directory:

```bash
rm -rf ~/.benchscope
```

::: warning
`~/.benchscope` stores performance artifacts, accuracy evaluations, logs, downloaded datasets, and cached models. Before removing it, decide whether you need to **back it up** — for example by copying it to another location or archiving it with `tar`. There is no way to recover it afterwards.
:::

If you overrode the data root with `BENCHSCOPE_DATA_DIR`, remove that directory instead (and unset the environment variable):

```bash
rm -rf "$BENCHSCOPE_DATA_DIR"
```

## Version Compatibility

BenchScope keeps backward compatibility with data produced by earlier versions:

- The legacy `~/.benchscope/config.json` is **automatically migrated to `settings.json`** at startup — no manual step required.
- `~/.benchscope/settings.json` carries over your providers, models, and platform configuration across upgrades.
- Task records created by older versions remain readable in **Datas → Perfs / Evals**.

::: info
Details of what changed between versions can be found in the [Release Notes](../changelog/v1-1-0.md). If you plan to skip several versions, review the intermediate changelogs for any breaking changes.
:::

## Upgrade Checklist

1. Back up `~/.benchscope` (or your custom data root).
2. Stop the running `benchscope` process.
3. Run `pip install --upgrade benchscope`.
4. Restart the service and confirm the Dashboard loads.
5. Spot-check your recent records in **Datas** to confirm the migration succeeded.

## Related

- [Quick Start](quickstart.md) — installing and launching
- [Configuration](configuration.md) — data root directory and settings
- [Release Notes](../changelog/v1-1-0.md) — what’s new in each version
