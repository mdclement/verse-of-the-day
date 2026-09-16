---
name: ponytail-debt
description: >
  Harvest every `ponytail:` comment in the codebase into a debt ledger, so
  deliberate shortcuts and deferrals get tracked instead of rotting into later
  means never. Use for ponytail debt, shortcut lists, or /ponytail-debt. One-shot report; changes nothing.
---

Every deliberate ponytail shortcut is marked with a `ponytail:` comment naming its ceiling and upgrade path. Collect these so a deferral cannot quietly become permanent.

## Scan

Search the repo for comment markers, skipping `node_modules`, `.git`, and build output. Use the comment prefix appropriate to the language, for example:

`grep -rnE '(#|//) ?ponytail:' .`

Each hit is one ledger row. The comment prefix keeps prose that merely mentions the convention out of the ledger.

## Output

One row per marker, grouped by file:

`<file>:<line>, <what was simplified>. ceiling: <the limit named>. upgrade: <the trigger to revisit>.`

Flag any marker with no upgrade path as `no-trigger`. End with `<N> markers, <M> with no trigger.` Nothing found: `No ponytail: debt. Clean ledger.`

## Boundaries

Reads and reports only; changes nothing. To persist it, ask and write a ledger such as `PONYTAIL-DEBT.md`. One-shot. "stop ponytail-debt" or "normal mode" to revert.