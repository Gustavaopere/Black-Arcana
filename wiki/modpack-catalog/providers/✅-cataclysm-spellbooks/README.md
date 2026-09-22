# Cataclysm: Spellbooks

Status: `✅ CURRENT PHYSICAL VERSION 1.1.14 BETA / EXACT PUBLISHER FILE 8847070 / 59/59 RELEASE-BOUNDED CURRENT SPELL REGISTRATIONS / REGISTRY BYTE-IDENTICAL TO HASH-MATCHED 1.1.13 CONTROL / 10 TRANSLATION-ONLY ROOT KEYS EXCLUDED / PHYSICAL 1.1.14 BYTE-EQUALITY NOT INDEPENDENTLY RECAPTURED / RUNTIME+BALANCE QA SEPARATE`

## Current installed identity

- Current JAR: `cataclysm_spellbooks-1.1.14-1.21.jar`
- Mod id: `cataclysm_spellbooks`
- Runtime version: `1.1.14-1.21`
- Minecraft / loader: `1.21.1` / NeoForge
- Current installed channel: **Beta**
- CurseForge project ID: `1099461`
- Exact current publisher CurseForge file ID: `8847070`
- Exact publisher-release SHA-1: `568d798862a61a374ab1e55dcddf5b2e3326b8b5`
- Exact publisher-release SHA-256: `a5a0dcad537954f488c862b3409831e0d12b4dfdc50bbfade298cb3d05dff2cf`
- Physical 1.1.14 SHA-1 independently captured in Black Arcana authority material: **no**
- Uploaded: `2026-09-09`
- Provider class: `SPELL PROVIDER / CONTENT ADDON`
- Primary dependencies: Iron's Spells 'n Spellbooks + L_Ender's Cataclysm

The current sibling physical authority identifies the installed filename/version as 1.1.14. The exact publisher File `8847070` was independently materialized and fingerprinted, then compared against the previously hash-matched 1.1.13 physical control. Because the repository does not preserve a second independent physical SHA-1 for the installed 1.1.14 JAR, current evidence is `COUNTED_RELEASE_BOUNDED`, not physical-byte `COUNTED_EXACT`. See [`EXACT-1.1.14-RELEASE-REVALIDATION.md`](EXACT-1.1.14-RELEASE-REVALIDATION.md); the older [`EXACT-1.1.13-ARTIFACT-AUDIT.md`](EXACT-1.1.13-ARTIFACT-AUDIT.md) remains the exact hash-matched control.

## Exact current spell inventory — 59

The exact publisher 1.1.14 JAR contains a `SpellRegistries.class` byte-for-byte identical to the hash-matched 1.1.13 control. Therefore the current release closes at the same **59 provider-owned `AbstractSpell` registrations**:

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

The 1.1.14 registry class has SHA-256 `8c4f8570d832a2a178e2d35244729eacd3208ccb4e9df582a16a01976a4881c7`, exactly matching 1.1.13. The bounded spell-related class set is also unchanged at 225 paths, and the root spell-localization set is unchanged at 69 keys. The prior exact registry audit established 59 `Supplier<AbstractSpell>` fields, 59 `registerSpell(...)` calls, 59 spell-class instantiations and 0 conditional branches; identical registry bytes carry those facts to publisher release 1.1.14.

The complete current 59-row field/class/resource-ID table is [`EXACT-1.1.14-SPELL-INVENTORY.md`](EXACT-1.1.14-SPELL-INVENTORY.md). This closes current **release identity/count**, not numerical mechanics.

## Translation-only identities excluded

The exact 1.1.14 `en_us` language resource contains the same 69 root spell keys as 1.1.13. Ten do not reconcile to a registered current spell identity and therefore contribute zero to the 1.1.14 semantic count:

`conjure_abyssal_gnawer`, `conjure_clawdian`, `conjure_coral_golem`, `conjure_coralssus`, `cryopiercer`, `final_rend`, `hemorrhaging_impact`, `parting_shot`, `quick_strike`, `scorched_earth`.

Localization/WIP residue is not promoted to a spell merely because a root translation exists.

## Publisher-scale mismatch recorded

The generic/current CurseForge project description advertises **65 new spells**, but the exact 1.1.14 publisher artifact still carries the same registry bytes as the exact 1.1.13 control. The current catalog therefore remains **59 registered spell identities**; the project-page `65` is not promoted to a registry fact.

The 1.1.14 changelog adds a Strange Disc acquisition path and manuscript brewing into 500 mB of Timeless Slurry. It does not announce a spell-registry change. The stronger binary comparison independently confirms no registry-class delta.

## Public source-version boundary

The project-linked public source checkpoint `AceTheEldritchKing/Cataclysm_Spellbooks_1.21.1@82a0af71f051058fe515c8b1cb9168e7f972f41c` still declares `1.1.11-1.21` and contains 34 concrete registrations. It remains a historical semantic/deduplication baseline, not current runtime authority. See [`SOURCE-1.1.11-BASELINE.md`](SOURCE-1.1.11-BASELINE.md).

The old source result is not extrapolated numerically. The current 59-row table is carried to 1.1.14 only because the exact 1.1.14 publisher registry class is byte-identical to the already-audited 1.1.13 registry class.

## Semantic-magic result

Under [`../../meta/SEMANTIC-MAGIC-COVERAGE.md`](../../meta/SEMANTIC-MAGIC-COVERAGE.md):

- provider-owned standalone spells: **59**;
- evidence state: `COUNTED_RELEASE_BOUNDED` for current 1.1.14 spell identity/count; physical 1.1.14 byte-equality remains unasserted;
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

These gates do not reopen the **59-spell current release-bounded identity inventory**.

## Provenance / license posture

Current CurseForge metadata labels the project PolyForm Shield License 1.0.0, while the public source checkpoint also contains conflicting `All Rights Reserved` project metadata. Black Arcana therefore keeps the provider `REFERENCE_ONLY / COMPATIBILITY_TARGET / LICENSE REVIEW REQUIRED` and makes no derivation claim.

Phase 2BE established the hash-matched 1.1.13 control. The 1.1.14 revalidation retains only cryptographic digests, archive/class paths, exact registry-class byte equality, bounded class-path sets and localization root-key sets. No implementation body, reconstructed source, assets, models, sounds or upstream prose are copied/adapted.
