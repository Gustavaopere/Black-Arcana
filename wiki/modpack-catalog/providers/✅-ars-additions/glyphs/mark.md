# Ars Additions — Mark

Status: `SOURCE-PINNED 21.3.0 / SEMANTICS AUDITED / RUNTIME QA PENDING`

- Provider: Ars Additions
- Type: Effect / `AbstractEffect`
- Registry path: provider-generated `glyph_mark`
- Display name: Mark
- Default tier: III
- Default mana cost: 25
- Compatible augments: none
- Per-spell occurrence limit: exactly 1
- Source class: `EffectMark`

## Provider-native behavior

Mark first obtains an `UnstableReliquary` from the caster/spell context. Without a valid Reliquary it resolves no stored mark.

For a block hit it stores `LocationMarkData` containing a `GlobalPos` with the current dimension and block position in the Reliquary's `MARK_DATA` component.

For an entity hit it stores `EntityMarkData` containing the entity UUID, entity type holder and optional display name for players. When the marked entity is a player, Ars Additions also applies its `marked` mob effect for a server-configured duration.

Source default for player Marked duration is **300 seconds**, configurable from 0 to 900 seconds.

## Black Arcana boundary

The Reliquary data component is the provider's persistent targeting reference. Black Arcana must not mirror it into a second hidden mark store or infer that a stored UUID/location remains valid, loaded, reachable or protection-authorized.

Any Black Arcana remote targeting continues to require its own server-authoritative validation. Provider Mark state is not a bypass for loaded-chunk, dimension, protection or world-effect policy.

Source checkpoint: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4` (`EffectMark`, `ServerConfig`).

## Engenharia para perks — execução exata 21.3.0

- **Classe pinada:** [`EffectMark.java`](https://github.com/Jarva/Ars-Additions/blob/91f102a90dc058cf40e4eac5a67a881e48b856b4/src/main/java/com/github/jarva/arsadditions/common/glyph/EffectMark.java); commit `91f102a90dc058cf40e4eac5a67a881e48b856b4`, versão de source 21.3.0.
- **Target/settlement:** `onResolveBlock` uses `UnstableReliquary.getReliquaryFromCaster(context,shooter)` and, only when non-null, stores `new LocationMarkData(new GlobalPos(world.dimension(),hitBlockPos))` under `AddonDataComponentRegistry.MARK_DATA`. This is reference-data mutation, not a placed world block.
- **Entity path:** with a valid Reliquary, stores `EntityMarkData(entity.getUUID(), entity.getType().builtInRegistryHolder(), optionalName)`. If target is a `Player`, also applies `MARKED_EFFECT` for `ServerConfig.SERVER.reliquary_effect_duration.get()*20` ticks (default 300 s declared elsewhere). The `MARK_DATA` write happens independently of whether the Marked potion later persists.
- **Spell restrictions:** fixed provider `PER_SPELL_LIMIT` config defined with min=max=1; no compatible augments; default mana 25. **Perks:** stateful reference and player effect must not become two Mastery awards; no generic RPG hook to extend remote target storage is proven.
- **Estado:** ✅ classe versionada e entrada source-audited; ⚠️ diferença host Ars 5.13.1 versus build baseline 5.11.2, config instalada, helpers/callback, runtime e Survival ainda não aprovados; ⛔ nenhuma perk RPG/adaptador Black Arcana foi implementado ou testado. Não duplicar mana, Source, inventário ou resolução do provider.
