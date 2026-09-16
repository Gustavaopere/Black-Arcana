# Cataclysm: Spellbooks — technical audit

## State

`EXTERNAL PROVIDER / INSTALLED 1.1.13 BETA / EXACT JAR HASH-MATCHED / 59 CURRENT SPELL REGISTRATIONS CLOSED / PUBLIC 1.1.11 SOURCE BASELINE RETAINED / NUMERICAL+RUNTIME CONTRACTS SEPARATE`

## Evidence ladder

### Authority 1 — physical pack

The current Black Arcana modlist contains:

- JAR: `cataclysm_spellbooks-1.1.13-1.21.jar`
- mod id: `cataclysm_spellbooks`
- runtime version: `1.1.13-1.21`
- SHA-1: `4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2`

This remains the authority for installed identity.

### Authority 2 — exact installed artifact audit

Temporary non-merge PR #188 materialized CurseForge File ID `8792628` through Curse Maven and required the downloaded SHA-1 to equal the physical hash before inspection.

Primary run/artifact: `34656614109 / 10285687158`.

Constructor-ID disambiguation run/artifact: `34656814496 / 10285756485`.

The exact 1.1.13 JAR proves:

- runtime metadata `cataclysm_spellbooks` / `1.1.13-1.21`;
- one `SpellRegistries` current registry surface;
- 59 `Supplier<AbstractSpell>` spell fields;
- 59 `registerSpell(...)` calls in `<clinit>`;
- 59 provider spell-class instantiations;
- 59 spell-field assignments after registry bootstrap;
- zero conditional branches in the narrow registration initializer audit;
- 59 unique registered root spell identities after field/class/literal reconciliation.

The exact table is [`EXACT-1.1.13-SPELL-INVENTORY.md`](EXACT-1.1.13-SPELL-INVENTORY.md); audit boundary/details are [`EXACT-1.1.13-ARTIFACT-AUDIT.md`](EXACT-1.1.13-ARTIFACT-AUDIT.md).

### Authority 3 — version-bounded publisher file metadata

CurseForge File ID `8792628` confirms the installed filename, NeoForge/Minecraft 1.21.1, Beta channel, upload date `2026-09-02` and a coarse changelog covering updated art, more ported spells, bug fixes and a new boss.

The generic/current project description advertises **65 new spells**. That statement is not version-bounded tightly enough to override the exact installed 1.1.13 registry, especially because a newer 1.1.14 beta now exists. For the physical pack snapshot, exact 1.1.13 binary evidence controls: **59 registered spells**.

### Authority 4 — public 1.1.11 source baseline only

Official repository checkpoint: `AceTheEldritchKing/Cataclysm_Spellbooks_1.21.1@82a0af71f051058fe515c8b1cb9168e7f972f41c`.

At that commit:

- `gradle.properties` declares `mod_version=1.1.11-1.21`;
- `SpellRegistries.java` contains 34 concrete registrations;
- `CSSchoolRegistry.java` registers Abyssal, Technomancy and Sand;
- Technomancy has zero concrete spell registrations in that historical registry.

This source remains semantic/history evidence only and is documented in [`SOURCE-1.1.11-BASELINE.md`](SOURCE-1.1.11-BASELINE.md). It is not used to infer current 1.1.13 values or implementation.

## Exact current identity result

Current exact package distribution:

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

This grouping reflects exact class namespaces. It does not by itself prove the exact school object returned by every spell or any balance value.

## Localization residue is not registry authority

The exact English language file contains 69 root `spell.cataclysm_spellbooks.*` keys. Ten have no current registered field/call/class-ID mapping in the exact 1.1.13 artifact:

`conjure_abyssal_gnawer`, `conjure_clawdian`, `conjure_coral_golem`, `conjure_coralssus`, `cryopiercer`, `final_rend`, `hemorrhaging_impact`, `parting_shot`, `quick_strike`, `scorched_earth`.

They are classified `EXCLUDED / TRANSLATION_ONLY` for the current semantic count. Localization residue/WIP presentation cannot mint a spell identity without registration.

`DesertWindsSpell` and `PharaohsWrathSpell` each also reference `sandstorm` in their class bytes. Constructor-only filtered facts close their own resource IDs as `desert_winds` and `pharaohs_wrath`, respectively; no cast/effect implementation body was retained.

## What exact artifact identity closure establishes

It establishes:

- exact current spell registry size and identities: 59;
- exact registration field/class mapping;
- unconditional static registration topology for those 59 entries;
- the installed-vs-publisher-count discrepancy;
- the fact that ten localization roots are not current registry entries.

It does **not** establish:

- exact 1.1.13 rarity/levels/cooldowns;
- mana/cast/range/damage/healing formulas;
- current acquisition/loot/crafting rules;
- supported addon API hooks or stable Black Arcana adapter seams;
- full current item/entity/effect registry semantics;
- runtime compatibility in the user's complete pack.

Those remain `NÃO VERIFICADO`/fail-closed until separately required and evidenced.

## Historical balance examples remain historical

The old source's Void Beam and Sandstorm numerical values remain useful only as 1.1.11-labelled comparison evidence. They are not promoted to 1.1.13 balance by the binary identity audit.

## Architecture / authority consequence

- Iron's owns the standard addon-facing spell substrate it exposes.
- Cataclysm: Spellbooks owns its 59 exact current spell/content registrations and provider-local state.
- L_Ender's Cataclysm owns original Cataclysm entities/materials/mechanics.
- Black Arcana owns only Black Arcana casting/runtime and may observe/integrate through a real verified boundary.

No Cataclysm: Spellbooks cast may be double-settled by Black Arcana. No second mana charge, duplicate cooldown, duplicate damage/heal, duplicate summon or duplicate world effect is allowed because Black Arcana tracks Arcane Danger or semantic overlap.

## Deduplication consequences

- **Infernal:** exact current Fire package closes 11 provider spell identities that must be compared against Iron's Fire, Black Flame, Ignis/Soul Fire and Somake surfaces.
- **Order:** exact current Technomancy package closes 22 spell identities; the historical zero-Technomancy-registration source snapshot is superseded for current identity.
- **Chaos:** boss-derived spectacle is not a gap by appearance; capability-level comparison remains required.
- **Space / displacement:** current exact registry retains Void/gravity identities; BA domain candidates must preserve a real semantic delta.
- **Summons / familiars:** provider summon spells remain provider-owned spells and do not become BA familiars by theme.

## License / clean-room finding

Current CurseForge metadata labels the project PolyForm Shield License 1.0.0, while the public source checkpoint has conflicting All Rights Reserved project metadata. This repository therefore continues to treat the provider as `REFERENCE_ONLY / COMPATIBILITY_TARGET / LICENSE REVIEW REQUIRED`.

Exact binary inspection retained only hash/metadata, archive/resource identities, localization IDs, class/member signatures, filtered root-ID literals, and narrow registry/constructor facts. No implementation body, source reconstruction, asset, model, sound or upstream prose is copied/adapted.

## Current closure state

The former exact-artifact/navigation blocker is **closed for spell identity/count**. The exact current spell inventory is 59/59 and may enter the semantic ledger as `COUNTED_EXACT`.

Runtime QA, numerical mechanics, acquisition details and any future integration seam remain separate gates. Identity closure is not a claim of full provider compatibility validation.
