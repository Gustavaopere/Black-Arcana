# Capability Matrix Delta — Apothic Enchanting

Phase 2AU candidate provider: `apothic_enchanting` 1.6.2.

## Evidence layers

- Physical artifact: `ApothicEnchanting-1.21.1-1.6.2.jar`, mod ID `apothic_enchanting`, SHA-1 `2623af251d3ddeae1d8e710afa76afe753834bab`.
- Physical modlist: 595 top-level entries, SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`, NeoForge 21.1.248.
- Exact publisher release: CurseForge project/file `1063926 / 8797650`, uploaded 2026-09-03 for NeoForge Minecraft 1.21.1.
- Exact official source release commit: `Shadows-of-Fire/Apothic-Enchanting@00fbcf00a2f42701645daf8906e54f67ec65a5dc`, message `1.6.2`.
- Exact release tree: `cad9b01b8d366e770cb811552884848afb320b30`; exact Java subtree `7f20d16f0d3f0c49caa1c5ae4582f88b22e8bd42`, recursively inspected with `truncated=false`.
- Source metadata: Minecraft 1.21.1, Java 21, NeoForge 21.1.187+, Placebo 9.9.0+, Apothic Attributes 2.4.0+.

No source↔physical-JAR byte equivalence is asserted.

## Capability delta

| Capability family | Provider surface | Black Arcana action |
|---|---|---|
| standalone spells / glyphs / rituals | no provider spell, glyph or ritual registration surface observed | do not turn enchantments, shelves, infusion recipes or Raven controls into BA spell identities |
| cast resource | none observed | Eterna, Quanta and Arcana are enchanting statistics, not BA mana/cast resources |
| enchanting statistics | Eterna, Quanta, Arcana, clues, blacklist, treasure permission and stability | provider owns table-stat computation; no duplicate BA/RPG roll engine |
| personal Eterna cap | synced `apothic_enchanting:max_eterna`, default/range 100 / 0..100 | provider owns cap semantics; RPG progression may only interact through an explicit bounded contract |
| block extension seam | `EnchantmentStatBlock` plus data-backed `EnchantingStatRegistry` | preferred provider-native shelf/stat boundary when an integration is actually needed |
| item extension seam | `EnchantableItem#selectEnchantments(...)`, deterministic relative to seeded random | preferred item-selection seam; do not bypass provider selection with a second enchantment pipeline |
| enchantment hard-cap seam | IMC method `set_ench_hard_cap` carrying enchantment key + positive integer | real compatibility surface; use only if a concrete BA requirement needs it |
| enchantment registry | 20 provider enchantment keys | provider owns identities/effects; no BA spell/Mastery duplication by thematic similarity |
| infusion | recipe serializers `infusion` and `keep_nbt_infusion`; Eterna/Quanta/Arcana min/max requirements | provider recipe authority; not a BA ritual |
| Raven table control | one serverbound PLAY payload `apothic_enchanting:set_raven_stats`, version `1`; server clamps values before persistence | provider UI/state authority; not C2S cast intent |
| table synchronization | clientbound PLAY payloads `clue`, `stats`, `enchantment_info`, version `1` | provider presentation/sync only |
| Raven persistence | serialized `RavenTableStats` attachment for Eterna/Quanta/Arcana | do not mirror provider table state in BA persistence |
| mixin/runtime interception | 17 common + 3 client mixins | implementation detail, not a stable generic BA integration API |
| provider enchantment effects | equipment, combat, loot, durability, projectile and utility effects are registered/settled by provider runtime | no duplicate proc/effect settlement; BA Backlash must not replay provider enchantment effects |
| optional compat | Curios/JEI/Jade and source-specific mixins/hooks exist | compatibility does not transfer authority; exact target contracts remain separate |
| source/runtime parity | exact source release pinned; physical bytes not compared | behavior that depends on source/JAR equivalence remains QA/fail-closed |

## Exact enchantment registry keys

The exact 1.6.2 source defines 20 `apothic_enchanting` enchantment keys:

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

`infusion` has an empty item target set and zero enchanting costs in the exact provider bootstrap. It belongs to the provider's infusion/table mechanism and is not promoted to a Black Arcana spell or ritual.

## Enchantability 1.6.1 → 1.6.2 evidence boundary

The exact changelog states that the Enchantability redesign entered **1.6.1**: it stopped contributing Arcana and was described as a percentage chance to boost individual enchantment levels by one. Version 1.6.2 fixes star-prefixed display and adds a JEI transfer handler for Raven-table infusion recipes.

The exact 1.6.2 `ApothEnchantmentHelper` source computes an Enchantability-derived `chance`, but the observed branch increments a selected enchantment when `rand.nextFloat() >= chance`. That comparison is not silently normalized to the changelog wording. Without source↔physical-JAR byte equivalence or runtime reproduction, Black Arcana records this as a source-intent/source-implementation discrepancy and keeps the physical runtime interpretation fail-closed.

## Network and authority rule

The provider registers four PLAY payloads:

- clientbound `apothic_enchanting:clue`, version `1`;
- clientbound `apothic_enchanting:stats`, version `1`;
- clientbound `apothic_enchanting:enchantment_info`, version `1`;
- serverbound `apothic_enchanting:set_raven_stats`, version `1`.

`set_raven_stats` is accepted only while the player has a `RavenEnchantmentMenu`; the server clamps Eterna to the player's provider-owned `MAX_ETERNA` and Quanta/Arcana to 0..100 before updating persistent Raven state and recomputing synchronized stats.

Therefore this is a server-validated provider UI/state path, not a cast-intent pipeline. Black Arcana retains its single canonical server-authoritative casting pipeline.

## Naming collision: Arcana

`Arcana` inside Apothic Enchanting is a provider-owned enchanting statistic affecting enchantment selection/weighting. Its name does not create ownership over Black Arcana's runtime, nor does Black Arcana gain authority over the provider statistic.

Any future adapter must preserve namespace, semantic identity and causality rather than mapping one concept to the other solely because both use the word “Arcana”.

## Authority boundary

- Apothic Enchanting owns enchanting tables, Eterna/Quanta/Arcana/clue computation, `max_eterna`, its 20 enchantment identities/effects, infusion recipes, Raven table state, libraries/tomes/shelves and provider synchronization.
- Placebo owns the shared dynamic-registry/network/config infrastructure consumed by the provider.
- Apothic Attributes owns the attribute infrastructure it supplies; the provider owns its registered `max_eterna` attribute semantics.
- Black Arcana retains canonical casting, targeting, transactional costs, BA cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash causality and world safety.
- RPG Skill Tree remains progression-only and may not directly rewrite provider roll algorithms, table state, enchantment effects or Eterna/Quanta/Arcana without an explicit contract.

## Fail-closed boundaries

- source/JAR byte reproducibility;
- direct publisher-file hash equality with the physical artifact;
- full-modpack datapack/reload/event ordering;
- runtime reproduction of the Enchantability comparison discrepancy;
- binary/API stability of non-`api` implementation classes;
- cross-mod behavior of the 20 mixins in the complete pack;
- optional JEI/Jade/Curios compatibility in the physical pack;
- future provider-version changes.
