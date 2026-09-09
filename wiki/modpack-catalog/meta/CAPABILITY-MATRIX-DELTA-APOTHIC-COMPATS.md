# Capability Matrix Delta — Apothic Compats

Phase 2AS candidate provider: `apothic_compats` 0.2.4.2.

## Evidence layers

- Physical artifact: `apothic_compats-0.2.4.2.jar`, SHA-1 `46d3699a4af63531fe84c69fdd2623fbe71fbc75`.
- Physical modlist: 595 top-level entries, SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`, NeoForge 21.1.248.
- Exact official source: `ianm1647/apothic-compats@0b9c900344dc536e4748e3ad0f3f18e03f2c3ba4`.
- Exact source root tree: `76e2e650732584a315b3faa3ab94ff8953e6caad`.
- Exact source metadata: Minecraft 1.21.1, mod version 0.2.4.2, NeoForge development baseline 21.1.242, MIT metadata.
- Publisher release: CurseForge project/file `1188699 / 8483936`, NeoForge 1.21.1, released 2026-07-22.

No source↔physical-JAR byte equivalence is asserted.

## Capability delta

| Capability family | Provider surface | Black Arcana action |
|---|---|---|
| standalone spells | 0 observed in complete exact Java/resource source tree | component closure can record zero; do not invent semantic spells from magic-themed affixes |
| glyphs / rituals | 0 / 0 observed | no BA registry identities or automatic domain/Mastery mappings |
| cast resource | no provider-owned mana/cast resource; Ars/Malum attributes are consumed through compatibility definitions | Ars/Malum remain authority over their own resources/attributes; no second BA settlement path |
| casting/network | no provider cast controller or packet/payload surface observed | no casting bridge inferred; fail closed if future versions add one |
| persistence | no provider SavedData magic subsystem observed; one projectile persistent-data dedup marker exists | marker is local event deduplication, not a BA persistence seam |
| Ars Nouveau gem | `apothic_compats:ars_nouveau/mana` modifies Ars max mana, regen, spell damage, warding/effect surfaces | treat as Apotheosis↔Ars compatibility; never reinterpret as BA mana |
| Ars loot/gear | 14 affix-loot entries + 3 gear sets | provider/Apotheosis ownership; no spell-count inflation |
| Ars invaders | 3 regular Wilden invaders; Ancient variants additionally condition on Ancient Reforging | provider-owned world/loot combat content; no BA casting authority |
| Malum gems | 3 provider gems: soul_stained, thief, etheric | preserve Malum/Lodestone attribute/effect authority |
| Malum affixes | armor/scythe/staff definitions plus extra gem bonuses | provider-owned; avoid duplicate datapack/affix classification |
| Malum custom procs | 4 codecs: scythe/staff Cleaving + Thunderstruck | preserve provider causality; do not route BA Backlash/casts into duplicate offensive proc chains |
| projectile attribute pass | server-side projectile spawn scaling by Apothic `ARROW_VELOCITY`, guarded by `apothic_compats.proj.done` | do not apply a second equivalent velocity multiplier in BA adapters |
| Apothic Enchanting block stats | 3 mixins adapt Supplementaries/Amendments blocks to Arcana/Quanta stats | `Arcana` here is provider terminology; no mapping to BA Arcane Danger |
| optional Curios content | 11 provider items when Curios loaded + config enabled | equipment provider-owned; no runtime authority transfer to RPG Skill Tree |
| other datapack compat | affix loot, gear sets, invaders, tags, categories, data maps, recipes across third-party mods | do not duplicate provider data injection; absent provider => fail closed |

## Magic-adjacent identity result

The component has **zero standalone magic identities** in Black Arcana's spell/glyph/ritual sense. Its relevant magic surface is cross-domain compatibility:

- Apotheosis/Apothic ↔ Ars Nouveau attributes/effects/equipment/entities;
- Apotheosis/Apothic ↔ Malum/Lodestone attributes/effects/scythe/staff behavior;
- Apothic Enchanting ↔ Amendments/Supplementaries block-stat adapters.

Those relationships justify cataloging the component but do not create a second spell runtime.

## Offensive causality result

`ScytheCleavingAffix` and `StaffCleavingAffix` can execute additional normal player attacks against nearby eligible entities. `ScytheThunderstruckAffix` and `StaffThunderstruckAffix` can apply nearby lightning-tagged, bypass-armor damage after a sufficiently charged attack.

Black Arcana must preserve those as provider-affix causes. In particular:

- BA Backlash must not be deliberately surfaced as a normal attack/cast trigger for these procs;
- a BA adapter must not repeat already-applied Cleaving/Thunderstruck damage;
- deduplication must follow real provider hooks rather than thematic matching.

## Authority boundary

- Apotheosis/Apothic: affix, gem, loot, category, invader and generic attribute/proc semantics.
- Ars Nouveau: Ars spell/mana/effect/entity/equipment runtime.
- Malum/Lodestone: Malum magic attributes/effects/charge/Soul Ward/item semantics.
- Apothic Enchanting: enchanting stats including Eterna/Quanta/Arcana.
- Apothic Compats: compatibility definitions, custom affix codecs, conditional Curios content, exact observed event/mixin glue.
- Black Arcana: canonical BA casting, targeting, transactional costs, BA cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash causality and `WorldEffectPolicy`.
- RPG Skill Tree: progression only through explicit contracts; no provider magic-runtime authority.

## Fail-closed boundaries

- source baseline Apotheosis 8.6.0 versus physical Apotheosis 8.8.0;
- source↔physical-JAR reproducibility not proven;
- complete-pack datapack reload/duplicate-key behavior not runtime-tested here;
- projectile event ordering versus BA/provider projectile initialization not runtime-tested;
- interaction of offensive affixes with other damage/attack listeners not runtime-tested;
- Ancient Reforging and AE2 source support is dormant because those mod IDs are absent from the current physical inventory;
- exact future compatibility must be re-audited after provider/modlist updates.
