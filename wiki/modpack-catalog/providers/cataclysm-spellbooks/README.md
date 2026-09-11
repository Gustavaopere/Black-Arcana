# Cataclysm: Spellbooks

Status: `EXACT PHYSICAL 1.1.13 BETA / EXACT FILE 8792628 / EXACT JAR HASH-MATCHED / 59/59 CURRENT SPELL REGISTRATIONS / 10 TRANSLATION-ONLY ROOT KEYS EXCLUDED / PUBLISHER 65-SPELL SCALE NOT USED AS INSTALLED REGISTRY / RUNTIME+BALANCE QA SEPARATE`

## Current installed identity

- Current JAR: `cataclysm_spellbooks-1.1.13-1.21.jar`
- Mod id: `cataclysm_spellbooks`
- Runtime version: `1.1.13-1.21`
- Minecraft / loader: `1.21.1` / NeoForge
- Current installed channel: **Beta**
- CurseForge project ID: `1099461`
- Exact installed CurseForge file ID: `8792628`
- Physical SHA-1: `4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2`
- Uploaded: `2026-09-02`
- Provider class: `SPELL PROVIDER / CONTENT ADDON`
- Primary dependencies: Iron's Spells 'n Spellbooks + L_Ender's Cataclysm

The physical Black Arcana modlist is authority for presence/version. Phase 2BE independently materialized File ID `8792628` through Curse Maven and required byte-identity by SHA-1 before factual registry inspection. See [`EXACT-1.1.13-ARTIFACT-AUDIT.md`](EXACT-1.1.13-ARTIFACT-AUDIT.md).

## Exact current spell inventory — 59

The exact hash-matched 1.1.13 JAR closes the installed spell registry at **59 provider-owned `AbstractSpell` registrations**:

| Provider package group | Count |
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

`SpellRegistries` exposes 59 `Supplier<AbstractSpell>` spell fields; its exact static initializer performs 59 `registerSpell(...)` calls, instantiates 59 spell classes and has 0 conditional branch instructions in the narrow registration audit.

The complete 59-row field/class/resource-ID table is [`EXACT-1.1.13-SPELL-INVENTORY.md`](EXACT-1.1.13-SPELL-INVENTORY.md). This closes current **identity/count**, not numerical mechanics.

## Translation-only identities excluded

The exact `en_us` language resource contains 69 root spell keys. Ten do not reconcile to a current registry field/call/class ID and therefore contribute zero to the installed 1.1.13 semantic count:

`conjure_abyssal_gnawer`, `conjure_clawdian`, `conjure_coral_golem`, `conjure_coralssus`, `cryopiercer`, `final_rend`, `hemorrhaging_impact`, `parting_shot`, `quick_strike`, `scorched_earth`.

Localization/WIP residue is not promoted to a spell merely because a root translation exists.

## Publisher-scale mismatch recorded

The generic/current CurseForge project description advertises **65 new spells**, but that surface is not version-bounded to the physical 1.1.13 registry and the project now has a newer 1.1.14 beta release. Exact installed 1.1.13 evidence therefore controls this snapshot: **59 registered spell identities**.

The exact 1.1.13 file changelog remains useful for its coarse release delta — updated art, more spells ported, bug fixes and a new boss — but it does not override the exact registry count.

## Public source-version boundary

The project-linked public source checkpoint `AceTheEldritchKing/Cataclysm_Spellbooks_1.21.1@82a0af71f051058fe515c8b1cb9168e7f972f41c` still declares `1.1.11-1.21` and contains 34 concrete registrations. It remains a historical semantic/deduplication baseline, not current runtime authority. See [`SOURCE-1.1.11-BASELINE.md`](SOURCE-1.1.11-BASELINE.md).

The exact 1.1.13 result is not described as “34 + 25 unchanged spells”; intermediate releases can rename, move, remove or rework identities. Only the exact 59-current table is canonical for this pack snapshot.

## Semantic-magic result

Under [`../../meta/SEMANTIC-MAGIC-COVERAGE.md`](../../meta/SEMANTIC-MAGIC-COVERAGE.md):

- provider-owned standalone spells: **59**;
- evidence state: `COUNTED_EXACT` for current spell identity/count;
- translation-only/WIP root keys above: **0**;
- exact mana/cooldown/rarity/levels/formulas/acquisition: `NÃO VERIFICADO` unless separately cataloged.

## Provider-native authority

Iron's remains authority for the generic addon-facing spell substrate it exposes. Cataclysm: Spellbooks owns its 59 provider spell identities/content registrations and provider-local state. L_Ender's Cataclysm remains authority for the original Cataclysm mobs, bosses, materials and mechanics consumed by the addon.

Black Arcana must not:

- charge a second mana/resource for a provider cast;
- replay provider damage/healing/summon settlement;
- duplicate provider cooldowns;
- convert provider-local state into Black Arcana authority;
- infer a compatibility hook merely from a matching theme/class name;
- treat spectacular Cataclysm presentation as proof of a Black Arcana semantic gap.

No Black Arcana runtime adapter is created by this catalog closure.

## Current deduplication impact

### Infernal / Black Flame / Fire

The exact current artifact now closes **11** Fire-package registrations. Infernal remains a candidate only after comparison against Iron's Fire, these Cataclysm spells, Black Arcana Black Flame, Ignis Soulfires/Spellbooks, Soul Fire'd and Somake's infernal/soul-fire surfaces.

### Order / Technomancy

The exact current artifact closes **22** Technomancy-package spell registrations. Order candidates involving beams, projectiles, constructs, machine-like suppression/control, system manipulation or deterministic mechanical magic must be compared against this exact current set rather than the old source snapshot that had zero concrete Technomancy registrations.

### Chaos / boss-derived magic

Cataclysm-derived effects can visually resemble chaos/reality magic. Presentation alone is not a gap. Capability-level comparison remains required before Black Arcana implements a semantic duplicate.

### Space / gravity / displacement

Current registered identities still include provider Void/gravity content such as Void Rune, Void Bulwark, Gravity Storm and Gravitational Pull. Black Arcana Space/Displacement work must preserve its approved domain contracts and avoid duplicate ownership/settlement.

### Summons / familiars

Provider summon spells remain provider-owned spells; they do not automatically become Black Arcana familiars. Any overlap with Familiars & Divination is resolved by role, persistence, control model, acquisition and real ownership seams.

## World-effect safety

Provider spells remain provider-owned; Black Arcana must not intercept and reapply their block/entity effects as if they originated from the Black Arcana canonical pipeline. Independently implemented destructive Black Arcana effects still pass through `WorldEffectPolicy`.

## Remaining gates outside identity/count closure

1. exact current numerical spell mechanics where capability-level comparison requires them;
2. current acquisition/loot/crafting rules where progression deduplication requires them;
3. provider runtime/full-pack QA before compatibility assertions;
4. any stable provider-native integration seam required by a future adapter.

These gates do not reopen the exact **59-spell current identity inventory**.

## Provenance / license posture

Current CurseForge metadata labels the project PolyForm Shield License 1.0.0, while the public source checkpoint also contains conflicting `All Rights Reserved` project metadata. Black Arcana therefore keeps the provider `REFERENCE_ONLY / COMPATIBILITY_TARGET / LICENSE REVIEW REQUIRED` and makes no derivation claim.

Phase 2BE exact binary inspection retained only factual cryptographic identity, archive/resource paths, localization IDs, class/member signatures, filtered root-ID literals and narrow registry/constructor facts. No implementation body, reconstructed source, assets, models, sounds or upstream prose are copied/adapted.
