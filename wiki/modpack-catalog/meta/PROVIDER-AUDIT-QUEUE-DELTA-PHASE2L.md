# Provider Audit Queue — Phase 2L delta

Date: `2026-09-07`

This is a narrow status overlay over `PROVIDER-AUDIT-QUEUE.md`. It prevails for `apprenticecodex` until the next integral regeneration of the current magic-provider queue. Earlier deltas remain authoritative for their own named rows.

## Current row

| Mod ID | Installed identity | Current effective audit state |
|---|---|---|
| `apprenticecodex` | `apprentice_codex-0.9.7.1+mc1.21.1.jar` / runtime `0.9.7.1` | `EXACT INSTALLED ARTIFACT / EXACT VERSION SOURCE PIN 305ea6a / MIT CODE + CC0 ORIGINAL ASSETS / 83/83 SPELL REGISTRY IDS + PER-SPELL SOURCE CATALOG COMPLETE / 9 IRON'S SCHOOLS / SCHOOL AFFINITY + BLOCK/EFFECT/ATTRIBUTE + EQUIPMENT/CASTING-SURFACE FAMILIES + ACQUISITION + OPTIONAL COMPAT AUDITED / CORE IRON'S 3.16.3 BASELINE MATCHES PACK / FULL 612-MOD RUNTIME QA PENDING` |

## Evidence

Installed artifact from the current physical modlist:

- JAR `apprentice_codex-0.9.7.1+mc1.21.1.jar`;
- mod id `apprenticecodex`;
- runtime `0.9.7.1`;
- mixin `mixins.apprenticecodex.json`;
- SHA-1 `b514315add32b93b0049c8673075627d7ef812e0`;
- package fingerprint `702285225`.

Exact source checkpoint:

`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

The exact source metadata declares Apprentice's Codex `0.9.7.1`, Minecraft 1.21.1, NeoForge source baseline 21.1.228, Iron's `1.21.1-3.16.3`, Iron's Lib `1.21.1-2.1.0`, Curios `9.5.1+1.21.1` and GeckoLib `4.8.3`. The physical pack runs NeoForge `21.1.248`; source build baseline and installed loader are intentionally kept distinct.

## Exact spell inventory

The 0.9.7.1 `SpellRegistry` contains **83 spells**:

- Blood 3;
- Ender 15;
- Evocation 17;
- Fire 5;
- Holy 11;
- Ice 3;
- Lightning 10;
- Nature 12;
- Eldritch 7.

Every registry entry now has a source-pinned page under `wiki/modpack-catalog/providers/apprentice-codex/<school>/`.

## Provider-wide coverage completed

Phase 2L additionally closes source-level catalog coverage for:

- School Affinity: 9 fixed Iron's school slots + up to 16 extra eligible schools, with exact temporary spell-power modifiers/potion variants;
- provider blocks;
- 20 static mob effects plus dynamic affinity effects;
- provider synced `max_enchantment_table_level` attribute;
- item/equipment/casting-surface families;
- spellcaster rounds/ammunition and crafting-support families;
- brooms/Curios/provider infrastructure;
- recipes, loot modifier, Errand Mage trades and spell acquisition eligibility rules;
- optional compatibility package inventory reconciled against the current physical pack.

## Compatibility posture

Core dependency alignment is strong:

- Iron's Spells `3.16.3` — exact source baseline;
- Iron's Lib `2.1.0` — exact minimum;
- Curios `9.5.1+1.21.1` — exact minimum;
- Create `6.0.10` — exact optional source baseline;
- Epic Fight `21.17.3.1` — exact optional source baseline;
- Iron's Jewelry `2.0.2`, Atlas API `1.2.0`, Malum `1.8.2`, Lodestone `1.8.2`, Patchouli `93` — exact source baselines where declared.

Several optional providers are newer than the development baseline and are version-eligible but still need runtime QA. Better Combat and Botania are absent. The exact `sodiumdynamiclights` mod id used by the provider's Sodium Dynamic Lights compatibility class is absent, so that specific surface remains inactive even though Sodium/LambDynamicLights exist in the pack.

## Authority consequence

Apprentice's Codex owns its 83 spell implementations, custom state/entities/blocks/items, alternative casting equipment, School Affinity and provider-local compatibility behavior. Iron's owns the underlying spell registry/schools/mana/standard cast lifecycle.

Black Arcana retains authority over its own canonical cast pipeline, spell domains, hazards, rituals, Corruption, Strain, Arcane Danger, persistence and world-safety policy.

RPG Skill Tree remains progression/mastery authority only through real boundaries; it does not become the cast/state authority for Apprentice's Codex.

## Deduplication consequence

The provider substantially occupies generic:

- magical firearms/blades/barrages;
- barriers/guard;
- mobility/flight/evasion;
- remote sight/sensing/divination;
- pet storage and companions;
- temporary bound equipment;
- block placement/excavation/harvesting/processing;
- mana/healing support.

Black Arcana Phase 3 content must demonstrate a material domain-specific delta rather than re-skin these capabilities.

## Runtime QA still open

Source/catalog completeness is not runtime proof. Remaining QA includes, where relevant:

- full 612-mod client/server load compatibility;
- final pack config/datapack overrides;
- delegated manager/entity constants marked pending in individual pages;
- optional compat activation in the actual pack;
- acquisition/economy behavior after pack overrides;
- server/client behavior for high-risk world-changing or movement spells.

These QA flags do not erase the exact source-derived catalog; they prevent overclaiming runtime validation.

## Next provider checkpoint

Phase 2L does **not** automatically choose the next provider by theme. After merge, the next checkpoint must be selected from the then-current queue/modlist after fresh reconciliation, preserving any newer parallel catalog work already merged into `main`.