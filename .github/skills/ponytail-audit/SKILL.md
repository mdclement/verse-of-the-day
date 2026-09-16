---
name: ponytail-audit
description: >
  Whole-repo audit for over-engineering. Like ponytail-review, but scans the
  entire codebase instead of a diff: a ranked list of what to delete, simplify,
  or replace with stdlib/native equivalents. Use for repo-wide bloat audits,
  deletion opportunities, or /ponytail-audit. One-shot report; does not apply fixes.
---

ponytail-review, repo-wide. Scan the whole tree instead of a diff. Rank findings biggest cut first.

## Tags

- `delete:` dead code or unused flexibility. Replacement: nothing.
- `stdlib:` hand-rolled thing the standard library ships. Name the function.
- `native:` dependency or code doing what the platform already does. Name the feature.
- `yagni:` abstraction with one implementation, config nobody sets, or layer with one caller.
- `shrink:` same logic, fewer lines. Show the shorter form.

## Hunt

Look for dependencies the stdlib or platform already ships, single-implementation interfaces, factories with one product, wrappers that only delegate, files exporting one thing, dead flags and config, and hand-rolled stdlib.

## Output

One line per finding, ranked: `<tag> <what to cut>. <replacement>. [path]`.
End with `net: -<N> lines, -<M> deps possible.` Nothing to cut: `Lean already. Ship.`

## Boundaries

Scope is over-engineering and complexity only. Correctness bugs, security holes, and performance are out of scope. Lists findings and applies nothing. One-shot. "stop ponytail-audit" or "normal mode" to revert.