# Apothic Enchanting — 1.6.2

Status: `EXACT PHYSICAL + EXACT PUBLISHER + EXACT OFFICIAL 1.6.2 SOURCE / ENCHANTING AUTHORITY / 20 ENCHANTMENT KEYS / ETERNA+QUANTA+ARCANA / MAX_ETERNA / INFUSION / RAVEN PERSISTENCE / 4 PLAY PAYLOADS / 20 MIXINS / ENCHANTABILITY DISCREPANCY QA / BYTE+FULL-PACK FAIL-CLOSED`

## Installed identity

- JAR: `ApothicEnchanting-1.21.1-1.6.2.jar`
- mod id: `apothic_enchanting`
- version: `1.6.2`
- SHA-1: `2623af251d3ddeae1d8e710afa76afe753834bab`
- Minecraft 1.21.1 / NeoForge 21.1.248
- physical modlist: 595 top-level entries, SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- physical Placebo 9.9.2 / Apothic Attributes 2.10.1

Apothic Enchanting is an enchanting-system provider. Its enchantments, table statistics, infusion and persistent table state do not transfer Black Arcana casting authority and are not BA spells.

## Publisher and exact source

- CurseForge project/file: `1063926 / 8797650`, uploaded 2026-09-03 for NeoForge 1.21.1.
- official repository: `Shadows-of-Fire/Apothic-Enchanting`
- exact release commit: `00fbcf00a2f42701645daf8906e54f67ec65a5dc`, message `1.6.2`
- root tree: `cad9b01b8d366e770cb811552884848afb320b30`
- Java subtree: `7f20d16f0d3f0c49caa1c5ae4582f88b22e8bd42`, recursive inspection `truncated=false`

Exact generated metadata requires Minecraft 1.21.1+, NeoForge 21.1.187+, Placebo 9.9.0+ and Apothic Attributes 2.4.0+. The physical pack satisfies those minimum ranges; that is not proof of complete runtime interoperability or source/JAR equality.

## Magic identity and authority

No standalone provider spell, glyph or ritual registration surface and no provider mana/cast resource were observed in the exact source. Eterna, Quanta and Arcana are provider-owned enchanting statistics. In particular, provider `Arcana` is only a naming collision with Black Arcana and must not be mapped by name alone.

Apothic Enchanting owns enchanting-table computation, enchantment selection, its enchantment identities/effects, infusion, Raven state/networking, `max_eterna`, shelves/libraries/tomes and its extension surfaces. Black Arcana retains canonical server-authoritative casting, targeting, transactional costs, BA cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash and world safety. RPG Skill Tree remains progression-only through explicit contracts.

## Enchanting statistics and provider seams

`EnchantmentTableStats` carries Eterna, Quanta, Arcana, clues, blacklist, treasure permission and stability. `EnchantingStatRegistry` is the provider's data-backed `enchanting_stats` registry. `api.EnchantmentStatBlock` exposes block-side Eterna/Quanta/Arcana/clue/blacklist/treasure/stability behavior. `api.EnchantableItem` exposes deterministic post-selection adjustment against the provider-supplied random source.

The provider also exposes IMC method `set_ench_hard_cap` for an enchantment key plus positive integer hard cap. These are real exact-source compatibility seams; they do not authorize bypassing provider selection or coupling BA to internal mixin classes.

The provider registers synced attribute `apothic_enchanting:max_eterna` with default 100 and range 0..100. RPG progression must not directly rewrite provider roll algorithms or state without a bounded contract.

## Exact enchantment registry

The exact source defines 20 keys:

1. `berserkers_fury`
2. `boon_of_the_earth`
3. `chainsaw`
4. `chromatic`
5. `crescendo_of_bolts`
6. `endless_quiver`
7. `growth_serum`
8. `icy_thorns`
9. `infusion`
10. `knowledge_of_the_ages`
11. `life_mending`
12. `miners_fervor`
13. `natures_blessing`
14. `rebounding`
15. `reflective_defenses`
16. `scavenger`
17. `shield_bash`
18. `stable_footing`
19. `tempting`
20. `worker_exploitation`

`infusion` is bootstrapped with an empty item target set and zero enchanting costs. It belongs to the provider's infusion/table mechanism, not to Black Arcana's ritual/spell registry.

## Infusion

The provider registers `apothic_enchanting:infusion` and `apothic_enchanting:keep_nbt_infusion` serializers. `InfusionRecipe` evaluates input plus minimum Eterna/Quanta/Arcana and optional maximum requirements. This remains provider recipe authority rather than a BA ritual.

## Raven persistence and networking

`RavenTableStats` is a serialized attachment storing Eterna/Quanta/Arcana on the Raven enchanting table. The exact provider registers four PLAY payloads, all version `1`:

- `apothic_enchanting:clue` — CLIENTBOUND;
- `apothic_enchanting:stats` — CLIENTBOUND;
- `apothic_enchanting:enchantment_info` — CLIENTBOUND;
- `apothic_enchanting:set_raven_stats` — SERVERBOUND.

The serverbound message is processed only for `RavenEnchantmentMenu`. Server code clamps Eterna to the player's provider `MAX_ETERNA` and Quanta/Arcana to 0..100 before updating provider persistence and resynchronizing stats. This is server-authoritative table state, not C2S cast intent.

## Mixins

The exact required mixin manifest contains 17 common and 3 client mixins at Java 21 compatibility level. They are provider implementation details, not automatically stable integration APIs.

## Enchantability 1.6.1 / 1.6.2 distinction

The exact changelog places the Enchantability redesign in **1.6.1**: Enchantability no longer contributes Arcana and is described as a percentage chance to increase individual enchantment levels. Version 1.6.2 itself fixes duplicate level display on star-prefixed enchantments and adds JEI transfer for Raven-table infusion recipes.

The exact 1.6.2 `ApothEnchantmentHelper` computes an Enchantability-derived `chance`, while the observed +1-level branch tests `rand.nextFloat() >= chance`. The audit does not silently rewrite that expression to match changelog prose and does not call it a confirmed physical runtime bug. Source↔physical-JAR equality and runtime reproduction remain unproven, so the discrepancy is explicit fail-closed QA.

## Clean-room / licensing

Evidence remains layered: root source code and generated metadata indicate MIT; exact `LICENSE_ASSETS` says All Rights Reserved; the current CurseForge project surface is also labeled All Rights Reserved. Black Arcana uses this material read-only for factual interoperability/deduplication analysis and copies/adapts no provider code, assets, translations, models, sounds or text.

## Remaining fail-closed QA

- source↔physical-JAR byte reproducibility;
- direct physical-vs-publisher-file hash equality;
- full-modpack reload/event ordering;
- physical runtime reproduction of the Enchantability comparison;
- complete-pack behavior of the 20 mixins;
- optional JEI/Jade/Curios runtime paths;
- stability of implementation classes outside explicit extension surfaces;
- future provider-version changes.
