---
title: "Update & Uninstall"
description: "Upgrade, uninstall, and manage (backup/cleanup) BenchScope runtime data."
---

# Update & Uninstall

This page explains how to upgrade BenchScope to the latest version, how to remove it, and how to manage (back up and clean up) your runtime data.

## Update

BenchScope is distributed on PyPI. Upgrade to the latest version with pip:

```bash
pip install --upgrade benchscope
```

After the upgrade completes, **restart the service** for the new version to take effect:

```bash
# stop the running benchscope process first (Ctrl+C or kill it), then:
benchscope
```

<div class="tip">

**tip**：

Before upgrading, review the [Release Notes](/en/docs/releases/v1-1-0/) to learn about new features and any breaking changes — especially data-directory or config-structure migrations. If you skip several versions, check the intermediate changelogs too.

</div>

### Verify the upgrade

Confirm the installed version:

```console
$ benchscope --version
benchscope 1.1.0
```

## Uninstall

Remove the package with pip:

```bash
pip uninstall benchscope
```

If you also want to clean up the runtime data directory:

```bash
rm -rf ~/.benchscope
```

If you overrode the data root with `BENCHSCOPE_DATA_DIR`, remove that directory and unset the variable instead:

```bash
rm -rf "$BENCHSCOPE_DATA_DIR"
unset BENCHSCOPE_DATA_DIR
```

<div class="warning">

**warning**：

`~/.benchscope` stores performance artifacts, accuracy evaluations, logs, downloaded datasets, and cached models. Before removing it, decide whether you need to **back it up** — there is no way to recover it afterwards.

</div>

## Backing Up Data (before uninstall)

If you want to keep historical test artifacts, archive the data root before uninstalling:

```bash
# archive the whole data root
tar -czf benchscope-data-backup.tar.gz -C ~ .benchscope

# or archive only the subdirectories you need (e.g. perf + eval artifacts)
tar -czf benchscope-results.tar.gz -C ~/.benchscope perfs evals
```

After backing up, you can restore the archived artifacts into a new environment via **Datas → Perfs / Evals → Import Backup** in the web UI (see [Data & Statistics (Datas)](/en/docs/data/)).

## Version Compatibility

- The legacy `~/.benchscope/config.json` is **automatically migrated to `settings.json`** at startup — no manual step required.
- What changed between versions is described in the [Release Notes](/en/docs/releases/v1-1-0/) and the individual version pages.

### Data Directory Compatibility

| Item | Description |
| --- | --- |
| Config migration | `config.json` → `settings.json` is automatic; the old file can be safely deleted |
| Data root | Defaults to `~/.benchscope`, overridable via `BENCHSCOPE_DATA_DIR` (see [Configuration](/en/docs/install/configuration/)) |
| Artifact format | Performance `run.json` / accuracy `evals/eval-<time>/` are broadly stable across versions and can be imported into newer versions |

<div class="info">

**info**：

If you reinstall later and keep the old `~/.benchscope` data directory, the new install automatically picks up your existing data and configuration, so historical artifacts remain visible.

</div>

## Upgrade / Uninstall Checklist

**Upgrade:**
1. Back up `~/.benchscope` (or your custom data root).
2. Stop the running `benchscope` process.
3. Run `pip install --upgrade benchscope`.
4. Restart the service and confirm the Dashboard loads.
5. Spot-check recent records in **Datas** to confirm the migration succeeded.

**Uninstall:**
1. Decide whether you need to back up the data root.
2. Run `pip uninstall benchscope`.
3. (Optional) Remove the data root for a complete cleanup.

## FAQ

**Q: Startup errors after upgrading?**
First check the version; then look for any config-migration notices. Make sure your Python and dependency environment were not altered by other system tools.

**Q: How do I fully reset the platform?**
Stop the service, back up any data you need, delete `~/.benchscope`, then start again to get a fresh environment.

**Q: Does `pip uninstall` remove my data?**
No. Uninstall only removes the Python package; it does not delete the `~/.benchscope` data directory. You must `rm -rf` it manually.

## Related

- [Install](/en/docs/install/) — requirements and launching
- [Configuration](/en/docs/install/configuration/) — data root directory and config migration
- [Data & Statistics (Datas)](/en/docs/data/) — artifact persistence and importing backups
- [Release Notes](/en/docs/releases/v1-1-0/) — what’s new in each version
