---
name: ponytail-review
description: >
  Code review focused exclusively on over-engineering. Finds what to delete:
  reinvented standard library, unneeded dependencies, speculative abstractions,
  and dead flexibility. Use for simplify reviews or /ponytail-review. One line per finding.
---

Review diffs for unnecessary complexity. One line per finding: location, what to cut, and what replaces it. The diff's best outcome is getting shorter.

## Format

`L<line>: <tag> <what>. <replacement>.`, or `<file>:L<line>: ...` for multi-file diffs.

Tags:

- `delete:` dead code, unused flexibility, or speculative feature. Replacement: nothing.
- `stdlib:` hand-rolled thing the standard library ships. Name the function.
- `native:` dependency or code doing what the platform already does. Name the feature.
- `yagni:` abstraction with one implementation, config nobody sets, or layer with one caller.
- `shrink:` same logic, fewer lines. Show the shorter form.

## Scoring

End with the only metric that matters: `net: -<N> lines possible.` If there is nothing to cut, say `Lean already. Ship.` and stop.

## Boundaries

Scope is over-engineering and complexity only. Correctness bugs, security holes, and performance are out of scope. A single smoke test or assert-based self-check is the ponytail minimum, not bloat. Does not apply fixes; only lists them. "stop ponytail-review" or "normal mode" reverts to verbose review style.