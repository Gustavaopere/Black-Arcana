# 03 — Integration Layer

Freeze real adapters to the magic/RPG ecosystem before content depends on them.

## Principle
Black Arcana owns interfaces; adapter packages own optional mod types. Capability probing must be safe and explicit.

## Tasks
- Iron's active-spell/mana integration.
- Ars resource/glyph-compatible integration where useful.
- Eidolon ritual/occult integration.
- Malum spirit/soul integration.
- RPG skill-tree progression/mastery integration.
- Optional dependency/fallback matrix.

## Exit criteria
Each installed-mod adapter passes contract tests and the mod still reaches a dedicated-server boot path when optional integrations are absent according to the decided dependency policy.
