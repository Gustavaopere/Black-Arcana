# Alshanex's Familiars 4.0.3 — exact artifact catalog

## Status

`EXACT PHYSICAL 4.0.3 / EXACT PUBLISHER FILE 8675568 / EXACT JAR HASH-MATCHED / 7/7 PROVIDER SPELL REGISTRATIONS / 11/11 PACKAGED RITUAL_RECIPE IDENTITIES / SOUND OWNERSHIP MIGRATED TO TUNES / 18 COUNTED SEMANTIC MAGICS / RUNTIME QA + ADAPTER SEAM PENDING`

## Installed authority

- provider: **Alshanex's Familiars**
- mod id: `alshanex_familiars`
- installed JAR: `alshanex_familiars-1.21.1_v4.0.3.jar`
- runtime version: `1.21.1_v4.0.3`
- Minecraft / loader: NeoForge 1.21.1
- physical SHA-1: `e5051c2385a426d05bf203ba8081a23d891f6686`
- CurseForge project / exact file: `1171602 / 8675568`
- exact file published: `2026-08-18`, Release
- declared license: **All Rights Reserved**
- required ecosystem: Iron's Spells 'n Spellbooks + FamiliarsLib infrastructure

The physical modlist remains authority for installed identity. Phase 2BD independently materialized Curse Maven File ID `8675568` in an isolated GitHub Actions audit and verified byte identity against the physical SHA-1 before inspecting factual archive/registry metadata. See [`EXACT-4.0.3-ARTIFACT-AUDIT.md`](EXACT-4.0.3-ARTIFACT-AUDIT.md).

## Exact provider-owned spell inventory — 7

The exact JAR contains one `DeferredRegister<AbstractSpell>` surface in `PetSpellRegistry`. Its static initializer assigns seven spell fields through seven `registerSpell` calls with no conditional branch in that initializer. Class literals and the provider's own translation keys converge on these seven current IDs:

| Registry field | Provider class | Exact spell ID | Catalog |
|---|---|---|---|
| `SUMMON_SHADOW` | `ShadowSummonSpell` | `alshanex_familiars:summon_shadows` | [Summon Shadows](spells/summon-shadows.md) |
| `ICE_AGE` | `IceAgeSpell` | `alshanex_familiars:ice_age` | [Ice Age](spells/ice-age.md) |
| `ICE_CHAMBER` | `IceChamberSpell` | `alshanex_familiars:ice_chamber` | [Ice Chamber](spells/ice-chamber.md) |
| `MEGIDO` | `MegidoSpell` | `alshanex_familiars:megido` | [Megido](spells/megido.md) |
| `HIKEN` | `HikenSpell` | `alshanex_familiars:fire_fist` | [Fire Fist](spells/fire-fist.md) |
| `MAYHEM` | `EndMayhemSpell` | `alshanex_familiars:end_mayhem` | [End Mayhem](spells/end-mayhem.md) |
| `FAMILIAR_SWAP` | `SwitcherooSpell` | `alshanex_familiars:switcheroo` | [Switcheroo](spells/switcheroo.md) |

This closes the **current identity inventory**, not every numerical mechanic. Mana, cooldown, level scaling, damage formula, exact targeting details and acquisition remain provider-owned and are `NÃO VERIFICADO` in the individual pages unless supported by separate current evidence.

## Exact packaged ritual inventory — 11

The exact JAR packages eleven JSON resources whose type is precisely `alshanex_familiars:ritual_recipe`. They are discrete provider ritual identities under the semantic-magic ledger, not ordinary crafting recipes:

| Ritual recipe ID | Result ID | Catalog |
|---|---|---|
| `archmage_shard` | `alshanex_familiars:archmage_shard` | [Archmage Shard](rituals/archmage-shard.md) |
| `druid_shard` | `alshanex_familiars:druid_shard` | [Druid Shard](rituals/druid-shard.md) |
| `frostling_shard` | `alshanex_familiars:frostling_shard` | [Frostling Shard](rituals/frostling-shard.md) |
| `hunter_shard` | `alshanex_familiars:hunter_shard` | [Hunter Shard](rituals/hunter-shard.md) |
| `lightning_mage_shard` | `alshanex_familiars:lightning_mage_shard` | [Lightning Mage Shard](rituals/lightning-mage-shard.md) |
| `magic_power_tier_2` | `alshanex_familiars:magic_power_tier_2` | [Magic Power Tier 2](rituals/magic-power-tier-2.md) |
| `magic_power_tier_3` | `alshanex_familiars:magic_power_tier_3` | [Magic Power Tier 3](rituals/magic-power-tier-3.md) |
| `magic_resist_tier_2` | `alshanex_familiars:magic_resist_tier_2` | [Magic Resist Tier 2](rituals/magic-resist-tier-2.md) |
| `magic_resist_tier_3` | `alshanex_familiars:magic_resist_tier_3` | [Magic Resist Tier 3](rituals/magic-resist-tier-3.md) |
| `summoner_shard` | `alshanex_familiars:summoner_shard` | [Summoner Shard](rituals/summoner-shard.md) |
| `truth_mirror` | `alshanex_familiars:truth_mirror` | [Truth Mirror](rituals/truth-mirror.md) |

The provider Wiki independently documents the custom ritual subsystem and shard acquisition through rituals. Exact ingredient quantities, altar conditions, timing, multiplayer ownership and runtime settlement are intentionally not inferred from identity alone.

## Semantic-magic result

Under [`../../meta/SEMANTIC-MAGIC-COVERAGE.md`](../../meta/SEMANTIC-MAGIC-COVERAGE.md):

- provider-owned standalone spells: **7**;
- provider-owned custom ritual identities: **11**;
- Alshanex semantic contribution: **18**;
- evidence state: `COUNTED_EXACT` for current identity/count inventory.

Familiar AI abilities, passives, lifecycle actions and casts of external Iron's spells remain excluded. They do not mint duplicate spell identities.

## 4.0 ownership migration — Sound remains Tunes-owned

The version-specific 4.0 release moved Sound-school content out of Alshanex's Familiars and into Tunes n' Tomes. Generic/stale Bard/Sound prose is therefore historical context only. The current pack contains Tunes n' Tomes `1.1.0-HOTFIX`; its 16 counted Melodic spells remain owned and counted there exactly once.

## Authority and integration boundary

- **FamiliarsLib** owns its familiar framework/lifecycle surfaces.
- **Alshanex's Familiars** owns these seven provider spell identities, eleven provider ritual identities, familiar content and provider-local progression/items.
- **Tunes n' Tomes** owns the migrated Sound/Melodic spell content.
- **Iron's Spells** owns the generic spellcasting substrate and any external Iron's spells selected/cast by familiars.
- **Black Arcana** owns its own casting, spell domains, hazards, rituals, persistence, costs, cooldowns, targeting, Corruption, Strain, Arcane Danger, Backlash and `WorldEffectPolicy`.

No Black Arcana runtime adapter is created by this catalog closure. Stage 07.07 familiar ownership remains fail-closed until a stable provider-native ownership/lifecycle seam is verified and server-side revalidation is designed against the exact provider stack.

## Remaining gates outside catalog identity/count closure

1. dedicated runtime QA for Alshanex 4.0.3 + FamiliarsLib 1.7.1 + Tunes n' Tomes 1.1.0-HOTFIX + Iron's 3.16.3;
2. exact numerical spell mechanics where required for later capability deduplication;
3. exact ritual ingredient/condition/settlement details where required for integration or balance;
4. stable provider-native ownership/lifecycle seam before any Black Arcana familiar adapter.

These do not reopen the exact current **7-spell + 11-ritual identity inventory**.

## Provenance / clean-room

Alshanex's Familiars is All Rights Reserved. Phase 2BD used the exact binary only for read-only factual interoperability/catalog evidence: cryptographic identity, archive/resource paths, structured ritual type/result IDs, class/member signatures, filtered spell-ID literals and a narrow count/branch check of the registry static initializer. No spell implementation body, source code, assets, models, sounds or upstream prose are copied/adapted into Black Arcana.

## Sources

- physical modlist: current Black Arcana `modlist.txt`, SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- exact 4.0.3 file: `https://www.curseforge.com/minecraft/mc-mods/alshanexs-familiars/files/8675568`
- 4.0 migration release: `https://www.curseforge.com/minecraft/mc-mods/alshanexs-familiars/files/7920260`
- publisher Wiki: `https://wiki.pixeldreamstudios.net/mods/alshanex-familiars`
- Phase 2BD isolated exact-artifact audit: GitHub Actions run `34649305941`, job `103427464735`, text-only evidence artifact `10283338450`
