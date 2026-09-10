---
title: "Update & Uninstall"
description: "Update and uninstall BenchScope, and back up / clean up runtime data."
---

# Update & Uninstall

This page covers BenchScope version upgrades, uninstallation, and the management of runtime data (backup and cleanup).

## Update

Upgrade to the latest version with pip:

```bash
pip install --upgrade benchscope
```

After the upgrade completes, **restart the service** to make it take effect:

```bash
# Stop the currently running benchscope (Ctrl+C or kill the process), then start it again:
benchscope
```

<div class="tip">

**Tip**:

Before upgrading, review the [Release Notes](/en/docs/releases/v1-1-0/) for the new version's features and possible breaking changes, paying particular attention to any data-directory or configuration-structure migrations. If you skip across multiple versions, review the intermediate version notes one by one.

</div>

### Verify the Upgrade

After upgrading, you can confirm the version number (the CLI does not provide a `--version` option):

```console
$ pip show benchscope
Name: benchscope
Version: 1.1.1
```

> The version can also be viewed via `/api/version` in the Web interface, or on the Settings page.

## Uninstall

Uninstall BenchScope:

```bash
pip uninstall benchscope
```

If you also need to clean up the runtime data:

```bash
rm -rf ~/.benchscope
```

If you used `BENCHSCOPE_DATA_DIR` to override the data root directory, delete that directory and unset the environment variable:

```bash
rm -rf "$BENCHSCOPE_DATA_DIR"
unset BENCHSCOPE_DATA_DIR
```

<div class="warning">

**Warning**:

`~/.benchscope` stores performance artifacts, accuracy evaluations, logs, datasets, model caches, and other data. **Please confirm whether a backup is needed before uninstalling** — once deleted, it cannot be recovered.

</div>

## Data Backup (Before Uninstall)

If you need to keep historical test artifacts, archive the data root directory before uninstalling:

```bash
# Back up the entire data root directory
tar -czf benchscope-data-backup.tar.gz -C ~ .benchscope

# Or back up only the needed subdirectories (e.g. performance and accuracy artifacts)
tar -czf benchscope-results.tar.gz -C ~/.benchscope perfs evals
```

After backing up, you can restore the archived artifacts to a new environment via the web **Datas → Perfs / Evals → Import Backup** (see [Data & Statistics (Datas)](/en/docs/data/)).

## Version Compatibility

- The legacy `~/.benchscope/config.json` is **automatically migrated** to `settings.json` on startup; no manual handling is needed.
- See the [Release Notes](/en/docs/releases/v1-1-0/) and each historical version page for what changed in each version.

### Data Directory Compatibility

| Item | Description |
| --- | --- |
| Config migration | `config.json` → `settings.json` automatic migration; the old file can be safely deleted |
| Data root directory | Default `~/.benchscope`, overridable with `BENCHSCOPE_DATA_DIR` (see [Configuration](/en/docs/install/configuration/)) |
| Artifact format | Performance `run.json` / accuracy `evals/eval-<time>/` are largely stable across versions and can be imported into newer versions |

<div class="info">

**Info**:

If you reinstall after uninstalling and keep the old `~/.benchscope` data directory, the new installation will automatically read the original data and configuration, and historical artifacts will remain visible.

</div>

## Upgrade / Uninstall Checklist

**Upgrade:**
1. Back up `~/.benchscope` (or your custom data root directory);
2. Stop the running `benchscope` process;
3. Run `pip install --upgrade benchscope`;
4. Restart the service and confirm the Dashboard loads properly;
5. Spot-check recent records in **Datas** to confirm the data migration succeeded.

**Uninstall:**
1. Confirm whether the data root directory needs to be backed up;
2. Run `pip uninstall benchscope`;
3. (Optional) Delete the data root directory for a complete cleanup.

## FAQ

**Question: Startup errors after upgrading?**
First confirm the version number, then check for any configuration-migration-related notices. Make sure Python and the dependency environment have not been modified by other system tools.

**Question: How do I fully reset the platform?**
Stop the service, back up the data you need, delete `~/.benchscope`, then start again to get a fresh environment.

**Question: Is the data still there after `pip uninstall`?**
Yes, it is. Uninstalling only removes the Python package; it does not delete the `~/.benchscope` data directory. You must `rm -rf` it manually.

## Related Docs

- [Install](/en/docs/install/) — environment requirements and startup
- [Configuration](/en/docs/install/configuration/) — data directories and config migration
- [Data & Statistics (Datas)](/en/docs/data/) — artifact persistence and backup import
- [Release Notes](/en/docs/releases/v1-1-0/) — changes in each version