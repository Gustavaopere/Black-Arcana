# Phase 2AS — Apothic Compats checkpoint

## Scope

Phase 2AS audits `apothic_compats` 0.2.4.2 against the current physical modpack and exact official source. It is a catalog/deduplication phase only; no Black Arcana runtime implementation is added.

## Branch base / concurrency

- canonical base at branch creation: `main@ac4df420158616d2fb993fb5fbf6b8325c207c27`
- that main already contains Phase 2AR / PR #154, Backported Spellbooks, as component #46;
- no equivalent `apothic_compats` branch or open PR was found before branch creation;
- branch: `docs/magic-catalog-phase2as-apothic-compats-0.2.4.2`.

## Physical anchor

- Minecraft: 1.21.1
- NeoForge: `21.1.248`
- physical modlist: 595 top-level entries
- modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- physical artifact: `apothic_compats-0.2.4.2.jar`
- physical mod ID: `apothic_compats`
- physical version: `0.2.4.2`
- physical JAR SHA-1: `46d3699a4af63531fe84c69fdd2623fbe71fbc75`

Relevant physical providers include Ars Nouveau 5.13.1, Malum 1.8.2, Apotheosis 8.8.0, Placebo 9.9.2, Curios 9.5.1+1.21.1 and Apothic Enchanting 1.6.2. No exact mod ID `ae2` or Ancient Reforging identifier is present in the current physical inventory.

## Exact source anchor

- repository: `ianm1647/apothic-compats`
- exact commit: `0b9c900344dc536e4748e3ad0f3f18e03f2c3ba4`
- root tree: `76e2e650732584a315b3faa3ab94ff8953e6caad`
- Java tree: `2129a1dcffe47cff7f28647b781078f938407f2d`, recursively inspected with `truncated=false`
- resources tree: `a9682560521c5c9323681f0fdf89241580da3e11`
- source metadata: version 0.2.4.2, Minecraft 1.21.1, NeoForge development baseline 21.1.242, MIT metadata
- development Apotheosis baseline: 8.6.0; physical pack: 8.8.0

## Semantic closure

At the exact source ceiling:

- standalone spells: **0**
- glyphs: **0**
- rituals: **0**
- provider-owned mana/cast resource: **0**
- provider cast controller: **0 observed**
- provider packet/payload surface: **0 observed**
- provider SavedData-style magic persistence subsystem: **0 observed**
- required mixins: **3**

Magic-adjacent compatibility is nevertheless substantial and closed sufficiently for deduplication:

### Ars Nouveau

- one provider Apotheosis gem, `apothic_compats:ars_nouveau/mana`;
- Ars max-mana, mana-regen, spell-damage, warding and mob-effect bonuses;
- conditional Ars affixes;
- 14 Ars affix-loot equipment entries;
- 3 Ars gear sets;
- 3 regular Wilden invaders;
- Ancient variants are source-defined but condition-unsatisfied in the current physical pack.

### Malum

- 3 provider gems: soul_stained, thief, etheric;
- Malum/Lodestone/Apothic attribute and effect integration;
- extra gem bonuses for Malum scythe/staff categories;
- armor/scythe/staff affix definitions;
- 4 conditional custom affix codecs: scythe/staff Cleaving + Thunderstruck;
- Cleaving can issue additional normal attacks;
- Thunderstruck can apply nearby lightning-tagged bypass-armor damage.

### Apothic Enchanting / runtime glue

- 3 mixins adapting Supplementaries/Amendments blocks to `EnchantmentStatBlock` Arcana/Quanta stats;
- server-side projectile spawn pass scaling projectile velocity by Apothic `ARROW_VELOCITY`, with `apothic_compats.proj.done` persistent-data dedup marker;
- high-priority invulnerability-check event delegation for provider Aether/Create affix helpers;
- optional 11-item Curios registry when Curios is loaded and config enables it.

## Authority/deduplication decision

- Apothic Compats is not a spell provider despite integrating magic providers.
- Ars Nouveau keeps authority over Ars mana/spells/effects/entities.
- Malum/Lodestone keeps authority over Malum magic attributes/effects/charge/Soul Ward/item behavior.
- Apotheosis/Apothic keeps affix/gem/loot/category/invader semantics.
- Apothic Enchanting keeps its Arcana/Quanta enchanting-stat semantics; those do not map automatically to Black Arcana `Arcane Danger`.
- Black Arcana keeps canonical server-authoritative casting, transactional costs, targeting, BA cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash causality and `WorldEffectPolicy`.
- BA must not duplicate the projectile velocity pass or reinterpret Cleaving/Thunderstruck as BA spell/Backlash proc chains.
- RPG Skill Tree receives no runtime authority.

## Static QA / unresolved boundaries

- source↔physical-JAR byte reproducibility is not proven;
- source development target Apotheosis 8.6.0 differs from physical 8.8.0;
- full-pack datapack reload/duplicate-key behavior remains runtime QA;
- event ordering for projectile velocity scaling remains runtime QA;
- offensive affix interaction with other attack/damage listeners remains runtime QA;
- dormant AE2/Ancient Reforging paths are not promoted to current active behavior;
- dedicated-server/full-pack behavior remains to CI/runtime validation where applicable.

## License / clean-room

Source metadata and publisher evidence label the project MIT. The repository root has `TEMPLATE_LICENSE.txt`, whose own wording applies to NeoForged MDK template files; it is not treated as a standalone whole-project license file. Inspection is factual/read-only and no third-party implementation or assets are copied.

## Coverage decision

Phase 2AR / Backported Spellbooks is already canonical as component **#46** at `main@ac4df420158616d2fb993fb5fbf6b8325c207c27`.

`apothic_compats` is eligible to become component **#47** because the provider's current semantic surface is closed at a defensible exact-source evidence ceiling, including the exact result that its standalone spell/glyph/ritual inventory is zero while its cross-domain affix/gem/proc boundaries are explicitly cataloged.

Until latest-main reconciliation, CI GREEN on the reconciled HEAD, merge and post-merge main confirmation, canonical coverage remains **46/100 = 46%** and Phase 2AS represents **47/100 = 47% candidate**.

Phase 3 remains blocked.
