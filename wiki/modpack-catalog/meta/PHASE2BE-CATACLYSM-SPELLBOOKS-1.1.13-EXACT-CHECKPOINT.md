# Phase 2BE — Cataclysm: Spellbooks 1.1.13 exact catalog closure

## Scope

Close the installed Cataclysm: Spellbooks 1.1.13 spell **identity/count inventory** against the exact physical artifact, without treating stale 1.1.11 source or the generic/current 65-spell publisher claim as installed-registry authority.

## Synchronization anchor

- audited base: `main@c5a46a622351b6d9157b4620ca5386889c7bd5f3`
- base validation: Black Arcana CI **#2467 GREEN** on that exact `main` SHA
- physical modlist: **595 top-level entries**
- NeoForge: `21.1.248`
- modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- durable closure PR: `#189`
- isolated non-merge evidence PR: `#188`

## Exact artifact evidence

- JAR: `cataclysm_spellbooks-1.1.13-1.21.jar`
- mod id / runtime version: `cataclysm_spellbooks` / `1.1.13-1.21`
- CurseForge project/file: `1099461 / 8792628`
- physical SHA-1: `4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2`
- primary exact-artifact audit run/artifact: `34656614109 / 10285687158`
- constructor-ID disambiguation run/artifact: `34656814496 / 10285756485`
- both audit paths required exact SHA-1 equality before factual inspection

## Closure result

The exact 1.1.13 `SpellRegistries` surface closes:

- **59** `Supplier<AbstractSpell>` spell fields;
- **59** `registerSpell(...)` calls in the static initializer;
- **59** provider spell-class instantiations;
- **59** spell-field assignments after registry bootstrap;
- **0** conditional branch instructions in the narrow registration audit;
- **59 unique current spell IDs** after field/class/literal reconciliation.

Exact implementation-package distribution:

- Abyssal: **7**;
- Ender: **4**;
- Evocation: **1**;
- Holy: **5**;
- Fire: **11**;
- Ice: **5**;
- Nature: **4**;
- Technomancy: **22**;
- total: `7 + 4 + 1 + 5 + 11 + 5 + 4 + 22 = 59`.

The exact English localization contains 69 root spell keys. Ten are not current registered spell identities and remain excluded as translation-only/WIP-or-residual evidence:

`conjure_abyssal_gnawer`, `conjure_clawdian`, `conjure_coral_golem`, `conjure_coralssus`, `cryopiercer`, `final_rend`, `hemorrhaging_impact`, `parting_shot`, `quick_strike`, `scorched_earth`.

Two classes with an additional `sandstorm` literal were separately disambiguated from constructor-only root-ID facts:

- `DesertWindsSpell -> desert_winds`;
- `PharaohsWrathSpell -> pharaohs_wrath`.

## Semantic/catalog delta proposed by PR #189

- Cataclysm: Spellbooks current semantic contribution: **+59** `COUNTED_EXACT` spells;
- strict semantic minimum: **815 → 874**;
- Iron ecosystem subtotal: **468 → 527**;
- provider component: candidate **#55** on this PR, becoming canonical only after latest-main reconciliation, merge and exact post-merge validation;
- structural component coverage candidate: **55/100 = 55%**.

The global semantic denominator remains incomplete; **874 is a strict counted minimum, not a semantic percentage**.

## Publisher/source mismatch disposition

The generic/current CurseForge project description advertises 65 spells, while the hash-matched installed 1.1.13 registry closes 59. A newer 1.1.14 beta exists after the installed file. The physical installed artifact controls this pack snapshot; the project-scale 65 claim is not backported into 1.1.13 by assumption.

The public source checkpoint `AceTheEldritchKing/Cataclysm_Spellbooks_1.21.1@82a0af71f051058fe515c8b1cb9168e7f972f41c` remains a 1.1.11-labelled 34-registration historical baseline only.

## Remaining non-catalog gates

The following remain separate and fail-closed where not independently evidenced:

1. exact current mana/cooldown/rarity/level/cast/range/damage/healing formulas;
2. current acquisition, loot and crafting rules;
3. exact supported provider API/integration seams;
4. dedicated/full-pack runtime compatibility QA for any future integration assertion;
5. broader item/entity/effect registry semantics not required for this spell-identity closure.

These gates do not reopen the exact **59-spell identity/count inventory**.

## Authority / clean-room

Iron's retains authority for its generic spell substrate. Cataclysm: Spellbooks owns its provider spell registrations/content. L_Ender's Cataclysm owns original Cataclysm entities/materials/mechanics. Black Arcana retains authority over its own canonical casting, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash and world-safety policy.

Cataclysm: Spellbooks remains `REFERENCE_ONLY / COMPATIBILITY_TARGET / LICENSE REVIEW REQUIRED`. Exact binary inspection retained only cryptographic identity, archive/resource/localization IDs, class/member signatures, filtered root-ID literals and narrow registry/constructor facts. No upstream implementation body, reconstructed source, assets, models, sounds or publisher prose are copied/adapted.
