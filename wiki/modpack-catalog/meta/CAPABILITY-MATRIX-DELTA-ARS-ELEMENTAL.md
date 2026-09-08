# Capability Matrix Delta — Ars Elemental 0.7.10.1

Status: `SOURCE-PINNED PROVIDER DELTA / RUNTIME QA PENDING`

| Capability | Provider-native authority | Black Arcana boundary |
|---|---|---|
| Modular spell parts | Ars Nouveau GlyphRegistry + Ars Elemental spell parts | observe/dedup provider cast; no parallel cast pipeline |
| Projectile forms/propagation | Ars spell context/resolver + provider projectile entities | child projectiles/propagators remain one causal provider cast |
| Target filtering | Ars `AbstractFilter` / SpellContext cancellation | filters do not establish Order-law authority |
| Player mana | Ars Nouveau mana capability, modified by foci/armor/familiars | never create or debit a second provider mana pool |
| Source | Ars Nouveau Source capability and provider Source infrastructure | never convert into Black Arcana-owned Source |
| Familiar modifiers | Ars FamiliarRegistry + SpellModifier/SpellCost events | no duplicate school damage or cost reduction |
| Perks/threads | Ars PerkRegistry + provider perk events/attributes | no duplicate poison/shock/summon attributes |
| Armor perk slots | Ars PerkRegistry provider contract on 48 items | RPG Skill Tree does not become owner of Ars armor threads |
| Ritual lifecycle | Ars RitualRegistry and Ars ritual base classes | observe provider lifecycle; no parallel ritual settlement |
| Biome/world mutation | provider rituals/worldgen/mixins | provider effects stay provider-owned; Black Arcana effects use WorldEffectPolicy |
| Lightning | provider ritual/entity/chunk hook | do not replay lightning or derive a second offensive proc chain |
| Charm/domination | provider Charm path | not sufficient Black Arcana Chaos/Witchcraft identity |
| Life Link | provider Life Link glyph | Black Arcana Vincular requires typed persistent infrastructure delta |
| Spell-school mutation | provider post-init changes Ars core school sets | bridge reads final provider classification, not stale duplicated map |
| Network intent | NeoForge payload + server CurioHolder revalidation | client request never inventory authority |
| Discharge VFX | server-origin visual payload rendered client-side | VFX never gameplay authority |
| Provider config | NeoForge STARTUP/COMMON/CLIENT specs | source defaults are not assumed equal to installed config |

## Deduplication consequences

- provider mana/Source costs settle once through Ars;
- familiar and perk callbacks are modifiers of the same provider cast, not new casts;
- propagated/projectile spell contexts retain provider causality;
- provider world mutation is not mirrored through Black Arcana;
- Black Arcana hazards/danger can only consume safe provider observations/contracts without claiming ownership of provider mechanics.