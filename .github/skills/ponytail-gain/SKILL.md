---
name: ponytail-gain
description: >
  Show ponytail's measured impact as a compact scoreboard: less code, less
  cost, more speed, from benchmark medians. One-shot display, not persistent
  and not a per-repo number. Trigger with /ponytail-gain or ponytail gain.
---

# Ponytail Gain

Display this scoreboard when invoked. One-shot: do not change mode, write flag files, or persist anything.

The figures are published benchmark medians across five everyday tasks and three models. They are measured, not computed from the current repo. Source: `benchmarks/` and the Ponytail README.

## Scoreboard

```text
  ponytail gain                 benchmark median

  Lines of code   no-skill  100%
                  ponytail  6-20%       down 80-94%
  Cost            no-skill  100%
                  ponytail  23-53%      down 47-77%
  Speed           ponytail  3-6x faster

  This repo: /ponytail-debt  shortcuts you deferred
             /ponytail-audit what's still cuttable
```

## Honesty boundary

These are benchmark medians, not this repo. Never print a per-repo savings number: the unbuilt version was never written, so there is no real baseline to subtract from a live repo. Per-repo figures come from `/ponytail-debt`.

## Boundaries

One-shot display. Edits nothing and changes no mode. "stop ponytail" or "normal mode" to revert.