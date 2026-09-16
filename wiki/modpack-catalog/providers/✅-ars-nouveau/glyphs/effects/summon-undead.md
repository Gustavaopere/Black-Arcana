# Ars Nouveau — Summon Undead

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_summon_undead`
- Display name: Summon Undead
- School: Conjuration
- Default tier: 3
- Default mana cost: 150
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`), Amplify, Split, Pierce
- Source default duration: 15 s
- Source default Extend Time increment: 10 s
- Base summon count: 3 + Split count

## Provider-native behavior

Summons temporary allied `SummonSkeleton` entities. Pierce switches them to bows; Amplify upgrades weapon quality, including stronger swords/axes or bow Power enchantment depending on amplification. Split adds additional skeletons. The caster receives Summoning Sickness for the summon lifetime.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:conjuration_essence` + `minecraft:bone` + `minecraft:wither_skeleton_skull`.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns these temporary undead summons, their loadout scaling, ownership/lifetime and Summoning Sickness. Black Arcana Souls & Death content must not reinterpret them as Black Arcana souls/minions or double-settle their attacks.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectSummonUndead`).
