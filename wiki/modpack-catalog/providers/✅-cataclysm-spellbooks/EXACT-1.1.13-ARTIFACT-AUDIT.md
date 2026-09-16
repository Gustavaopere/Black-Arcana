# Cataclysm: Spellbooks 1.1.13 — exact artifact audit

## Purpose

Close the installed 1.1.13 **spell identity inventory** against the exact physical artifact without promoting stale 1.1.11 source or the publisher's generic/current 65-spell project claim into an installed-registry fact.

## Artifact identity

- physical JAR: `cataclysm_spellbooks-1.1.13-1.21.jar`
- mod id: `cataclysm_spellbooks`
- runtime version: `1.1.13-1.21`
- CurseForge project/file: `1099461 / 8792628`
- physical SHA-1: `4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2`
- primary audit run: `34656614109`
- primary text-only artifact: `10285687158`
- constructor-ID disambiguation run: `34656814496`
- disambiguation text-only artifact: `10285756485`

Both audit paths materialized the exact Curse Maven artifact and required SHA-1 equality with the physical modlist before factual inspection.

## Exact registry closure

The exact JAR contains `net.acetheeldritchking.cataclysm_spellbooks.registries.SpellRegistries` with:

- one `DeferredRegister<AbstractSpell>` registry field;
- **59** `Supplier<AbstractSpell>` spell fields;
- **59** `registerSpell(...)` calls in the static initializer;
- **59** provider spell-class instantiations in that initializer;
- **59** spell-field assignments after the registry bootstrap field;
- **0** conditional branch instructions in the narrow static-registration audit.

The registered class/field sequence and filtered root-ID literals reconcile to **59 unique current spell identities**. The complete table is versioned in [`EXACT-1.1.13-SPELL-INVENTORY.md`](EXACT-1.1.13-SPELL-INVENTORY.md).

### Exact package distribution

| Provider package group | Registered spells |
|---|---:|
| Abyssal | 7 |
| Ender | 4 |
| Evocation | 1 |
| Holy | 5 |
| Fire | 11 |
| Ice | 5 |
| Nature | 4 |
| Technomancy | 22 |
| **Total** | **59** |

Package grouping is a factual implementation namespace observation, not a claim that every group is a distinct provider-owned school. Exact school/balance mechanics remain separate where not otherwise proven.

## Translation-key reconciliation

The exact `en_us` resource contains **69** root keys of the form `spell.cataclysm_spellbooks.<id>`, but only **59** reconcile to the exact registered spell classes/IDs.

The following ten root translation identities are **not registered spells in the installed 1.1.13 artifact**:

- `conjure_abyssal_gnawer`
- `conjure_clawdian`
- `conjure_coral_golem`
- `conjure_coralssus`
- `cryopiercer`
- `final_rend`
- `hemorrhaging_impact`
- `parting_shot`
- `quick_strike`
- `scorched_earth`

They are retained as translation-only/WIP-or-residual evidence and contribute **0** to the exact current semantic spell count. Their presence in localization does not manufacture a registry identity.

## Two literal ambiguities closed separately

Raw class-literal scanning showed that `DesertWindsSpell` and `PharaohsWrathSpell` also reference `sandstorm` outside their own identity literal. A separate constructor-only factual check retained only root-ID String constants from the no-arg constructors and closed:

- `DesertWindsSpell` -> `desert_winds`
- `PharaohsWrathSpell` -> `pharaohs_wrath`

No cast/effect implementation body was retained.

## Publisher 65-spell claim

The current generic CurseForge project description advertises **65 new spells**. That claim is useful provider-scale evidence, but it is not substituted for the physically installed 1.1.13 registry. The exact hash-matched 1.1.13 binary closes **59 registered spell identities**.

The project also has a newer 1.1.14 beta release after the installed 1.1.13 file. The physical modlist remains authority for this pack snapshot, so later project-page scale must not be backported into 1.1.13 by assumption.

## Relation to the public 1.1.11 source baseline

The public source checkpoint `AceTheEldritchKing/Cataclysm_Spellbooks_1.21.1@82a0af71f051058fe515c8b1cb9168e7f972f41c` still declares 1.1.11 and contains 34 concrete registrations. It remains useful historical/deduplication evidence only.

The exact 1.1.13 result is not represented as a simple `34 + 25` release diff: registrations may have moved package group, been renamed, removed, or reworked. Only the exact 59-current table is promoted.

## Semantic result

Under the repository semantic-magic definition, the exact 59 `AbstractSpell` registrations are standalone provider-owned spell identities and are admitted as `COUNTED_EXACT`.

This identity closure does **not** establish exact 1.1.13 mana costs, cooldowns, rarity/level ranges, cast times, damage/healing formulas, acquisition, loot/crafting rules, or Black Arcana integration hooks. Those remain provider-owned and `NÃO VERIFICADO` unless separately evidenced.

## Authority / deduplication

- Iron's Spells owns its generic spellcasting substrate.
- Cataclysm: Spellbooks owns these provider spell identities/content registrations.
- L_Ender's Cataclysm owns the original Cataclysm entities/materials/mechanics consumed by the addon.
- Black Arcana retains authority over Black Arcana casting, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash and world-safety policy.

Black Arcana must not replay provider casts, double-charge mana, duplicate cooldown settlement, duplicate summons or duplicate world effects. Semantic overlap informs deduplication; it does not transfer ownership.

## Clean-room / license boundary

The project remains `REFERENCE_ONLY / COMPATIBILITY_TARGET / LICENSE REVIEW REQUIRED`. Current publisher/source licensing surfaces are not treated as a derivation grant. Exact binary inspection was restricted to cryptographic identity, archive/resource paths, localization IDs, class/member signatures, filtered spell-ID literals, and a narrow registry static-initializer count/branch audit.

No upstream implementation body, reconstructed source, assets, models, sounds or prose are copied/adapted into Black Arcana.
