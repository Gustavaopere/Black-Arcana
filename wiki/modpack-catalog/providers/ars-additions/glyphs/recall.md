# Ars Additions — Recall

Status: `SOURCE-PINNED 21.3.0 / SEMANTICS AUDITED / TARGET-VALIDATION QA PENDING`

- Provider: Ars Additions
- Type: Form / `AbstractCastMethod`
- Registry path: provider-generated `glyph_recall`
- Display name: Recall
- Default tier: III
- Default mana cost: 50
- Compatible augments: none
- Invalid combination: Mark
- Source class: `MethodRecall`

## Provider-native behavior

All cast entry points delegate to `cast(context, caster, resolver)`. Recall:

1. obtains a provider `UnstableReliquary` from the cast context/caster;
2. fails when the Reliquary is absent;
3. requires server-side execution;
4. reads the provider `MARK_DATA` component;
5. fails when no mark exists;
6. delegates the actual remote resolution to that `MarkData` implementation.

`ArsNouveauRegistry` also registers an explicit Spell Turret behavior for Recall, so turret resolution is provider-native rather than a Black Arcana automation hook.

## Configured reference costs

The 21.3.0 server config exposes default Reliquary costs of:

- player target: 1000 durability units;
- entity target: 250;
- location target: 50.

These are source defaults, not proof of the effective modpack config.

## Black Arcana boundary

Recall is a provider-owned remote target resolver. Black Arcana must not re-resolve the same mark, duplicate Reliquary cost, or treat stored provider references as authoritative Black Arcana target admission.

Cross-dimension/unloaded/removed-target behavior remains a runtime QA surface and must fail closed for any future integration that cannot prove a safe provider seam.

Source checkpoint: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4` (`MethodRecall`, `ArsNouveauRegistry`, `ServerConfig`).
