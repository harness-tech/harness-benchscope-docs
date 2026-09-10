---
title: "Built-in Skills"
description: "The 3 built-in skills shipped with BenchScope: bs-perfs-concurrency / bs-perfs-threshold / bs-engine-create, and how to view and download them in Settings → Skills."
---

# Built-in Skills

BenchScope ships 3 **built-in skills** (located in `benchscope/skills/` within the package), providing structured operational guidance for Agents (such as Harness or Claude): how to write a performance stress-test configuration, how to configure threshold probing, and how to create a custom engine. All built-in skills can be viewed in the **Settings → Skills** panel, with packaged downloads supported.

## Skill List

| Skill | ID | Purpose |
| --- | --- | --- |
| Concurrency stress-test configuration | `bs-perfs-concurrency` | Guides the Agent to write concurrency stress-test task configurations (concurrency list / input-output lengths / request counts, etc.), and provides configuration templates and a packaging script. |
| Threshold probing configuration | `bs-perfs-threshold` | Guides the Agent to write threshold-probing task configurations (TTFT / TPOT / output-throughput thresholds, decision statistic, search upper bound), and provides configuration templates and a packaging script. |
| Custom engine creation | `bs-engine-create` | Guides the Agent to create a custom engine per the engine integration contract (four parts: Input / Core / Output / Mock), and provides a validation script (`validate.sh`) and an import manifest. |

## Usage

### View in the Web UI

1. Open the **Settings → Skills** panel;
2. View the description cards of the 3 built-in skills (name / description / version);
3. Click **Download** to obtain the skill package (tar.gz) for installation in an Agent environment.

Corresponding APIs:

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/skills` | GET | Built-in skill list. |
| `/api/skills/{skill_id}/download` | GET | Download the specified skill package (tar.gz). |

### Install in an Agent environment

After extracting the skill package into the Agent's skill directory (such as `~/.dsh/skills/` or the Harness skills directory), the Agent can reference the corresponding skill when writing stress-test or threshold configurations or creating custom engines.

## Skill Package Structure

Each skill directory follows a unified structure:

```text
benchscope/skills/<skill-id>/
├── SKILL.md          # Skill instructions (the core the Agent reads)
├── README.md         # Human-readable description
├── templates/        # Configuration templates (e.g., bench-perfs-config.yaml)
└── scripts/          # Helper scripts (package.sh for packaging / validate.sh for validation)
```

<div class="info">

**Info**:

The `validate.sh` of the `bs-engine-create` skill validates engine definition files offline (`configs/benchs.yaml` and `configs/bench-params.yaml`); the validation items are consistent with the backend's import validation, so you can run this validation before creating a custom engine.

</div>

## FAQ

**Question: What is the difference between built-in skills and custom skills?**

Built-in skills are distributed with the pip package (always visible in Settings → Skills); custom skills are created by users and installed in an Agent environment; the two do not affect each other.

**Question: Why is the Skills counter on the Dashboard 3?**

The counter is the number of built-in skills (`bs-perfs-concurrency` / `bs-perfs-threshold` / `bs-engine-create`); see [Dashboard Overview](/en/docs/tools/dashboard/).

**Question: How do I create a custom engine based on bs-engine-create?**

After installing the skill, have the Agent follow the SKILL.md guidance to produce the engine definition (appended to `configs/benchs.yaml`) and the parameter definition (appended to `configs/bench-params.yaml`); then validate with `validate.sh` and import it via Settings → Bench Engines. See [Bench Engine](/en/docs/tools/bench-engine/) for details.

## Related docs

- [Bench Engine](/en/docs/tools/bench-engine/) — engine integration contract and custom engines
- [Settings](/en/docs/tools/settings/) — Skills panel and skill downloads
- [Dashboard Overview](/en/docs/tools/dashboard/) — Skills counter
- [API Overview](/en/docs/api/) — skill-related endpoints