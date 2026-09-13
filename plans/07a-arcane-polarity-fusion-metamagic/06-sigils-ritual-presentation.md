# 07A.06 — Sigil/Ritual Presentation Runtime Boundary

## State

`PLANNED / NOT IMPLEMENTED`

The actual sigil visual grammar, glyph/art rules, animation/palette/telegraph design and accessibility requirements are owned by `plans/visual-production/07a-arcane-polarity-fusion-metamagic/06-sigils-ritual-presentation.md`.

## Server/client authority

The server owns ritual, cast and session state. The client may render only bounded presentation snapshots/events derived from that state.

Client presentation cannot complete a ritual, choose cost/result, create an unlock, classify polarity, change target legality, bypass world safety or author arbitrary remote assets.

## Payload/schema safety

Any data-driven sigil presentation schema is declarative and bounded. It must reject commands, scripts, remote code, arbitrary paths, gameplay effects and arbitrary remote URL assets. Unknown/oversized presentation ids or definitions fail safely.

## Provider boundary

Optional Eidolon/Iron's/Ars presentation coordination requires an exact safe supported seam. Provider presentation never transfers Black Arcana ritual/cast authority, and Black Arcana must not replace provider-owned rendering merely because a provider is installed.

## Ritual materials

Material/offering placement is server-validated through canonical Stage 06 ritual transactions. Visual placement is never proof of payment, reservation or completion.

## Engineering tests

Cover malformed/oversized presentation definition rejection, unknown ids, client inability to complete/alter authoritative ritual state, reduced-presentation settings not changing server timing, exactly-once offering reservation/completion and absence of arbitrary remote URL asset references.

## Acceptance

Runtime acceptance is limited to bounded non-authoritative presentation transport and provider/server authority safety. Final art/readability/provenance acceptance is delegated to visual production.
