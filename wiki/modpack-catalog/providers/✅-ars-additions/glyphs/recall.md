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

## Engenharia para perks — execução exata 21.3.0

- **Classe pinada:** [`MethodRecall.java`](https://github.com/Jarva/Ars-Additions/blob/91f102a90dc058cf40e4eac5a67a881e48b856b4/src/main/java/com/github/jarva/arsadditions/common/glyph/MethodRecall.java); commit `91f102a90dc058cf40e4eac5a67a881e48b856b4`, versão de source 21.3.0.
- **All cast entrypoints:** `onCast`, `onCastOnBlock(UseOnContext)`, `onCastOnBlock(BlockHitResult)` and `onCastOnEntity` delegate to `cast(context,caster,resolver)`. The `UseOnContext` branch fails if `context.getPlayer()==null`.
- **Exact failure gates:** `cast` returns `CastResolveType.FAILURE` if no Reliquary, if caster world is not `ServerLevel`, or if `reliquary.get(MARK_DATA)` is null. Otherwise returns `mark.cast(context,reliquary,serverLevel,caster,resolver)`; that **downstream** implementation owns target lookup, durability debit and actual resolution.
- **Spell grammar:** `addDefaultInvalidCombos` adds `EffectMark.INSTANCE.getRegistryName()`; default mana 50 and no augments. **Perks:** do not substitute a Black Arcana target lookup, or treat `SUCCESS` and actual hit/damage as equivalent. Config defaults Reliquary player/entity/location 1000/250/50 are separate from spell mana and require downstream proof.
- **Estado:** ✅ classe versionada e entrada source-audited; ⚠️ diferença host Ars 5.13.1 versus build baseline 5.11.2, config instalada, helpers/callback, runtime e Survival ainda não aprovados; ⛔ nenhuma perk RPG/adaptador Black Arcana foi implementado ou testado. Não duplicar mana, Source, inventário ou resolução do provider.
