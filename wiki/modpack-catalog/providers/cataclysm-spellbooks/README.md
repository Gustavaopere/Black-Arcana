# Cataclysm: Spellbooks

Status: `CURRENT 1.1.13 BETA PINNED / PUBLIC CURRENT SCALE VERIFIED / 1.1.11 SOURCE BASELINE CATALOGED / EXACT 1.1.13 REGISTRY PENDING`

## Current installed identity

- Current JAR: `cataclysm_spellbooks-1.1.13-1.21.jar`
- Mod id: `cataclysm_spellbooks`
- Runtime version: `1.1.13-1.21`
- Minecraft / loader: `1.21.1` / NeoForge
- Current installed channel: **Beta**
- CurseForge project ID: `1099461`
- Exact current CurseForge file ID: `8792628`
- Uploaded: `2026-09-02`
- Provider class: `SPELL PROVIDER / CONTENT ADDON`
- Primary dependencies: Iron's Spells 'n Spellbooks + L_Ender's Cataclysm

The physical Black Arcana modlist is authority for presence and installed identity. The current CurseForge file page independently agrees with the exact filename, NeoForge 1.21.1, Beta channel and File ID.

## Current publisher-visible surface

The current project page states that Cataclysm: Spellbooks adds **65 new spells** and exposes Abyssal and Technomancy as provider schools. It also describes the addon as Cataclysm↔Iron's content rather than a replacement magic engine.

The exact 1.1.13 file changelog confirms only a coarse delta:

- updated art;
- more spells ported;
- bug fixes;
- a new boss;
- publisher warning that the beta is broadly playable but may still contain bugs.

These publisher claims are current enough for provider-level cataloging, but they do not expose the complete 65-entry registry, individual values or the identity of every change from 1.1.11.

## Source-version boundary

The project-linked official GitHub repository does **not** match the installed beta.

At public commit `82a0af71f051058fe515c8b1cb9168e7f972f41c`:

- `gradle.properties` declares `mod_version=1.1.11-1.21`;
- Minecraft is `1.21.1`;
- NeoForge baseline is `21.1.219`;
- Iron's baseline is `1.21-3.8.0`;
- `SpellRegistries.java` contains **34 concrete registrations**;
- `CSSchoolRegistry.java` registers Abyssal, Technomancy and a provider-owned Sand sub-school.

That source snapshot is cataloged in [`SOURCE-1.1.11-BASELINE.md`](SOURCE-1.1.11-BASELINE.md). It is useful for semantic/deduplication history but is **not** promoted to exact 1.1.13 runtime authority.

The numerical difference between the current public claim of 65 spells and the 34 registered entries in the old source snapshot is 31. It is not valid to infer that the installed beta simply adds 31 unchanged IDs: intermediate releases may add, remove, rename, port or rework content.

## Exact current spell table status

Current evidence supports:

- installed 1.1.13 artifact identity — `VERIFIED`;
- current provider-level 65-spell claim — `VERIFIED PUBLISHER CLAIM`;
- Abyssal and Technomancy current provider-school presence — `VERIFIED PUBLISHER CLAIM`;
- 1.1.11-labelled public-source baseline — `PINNED`, 34 concrete registrations;
- exact 1.1.13 65-spell names/registry IDs — `PENDING CURRENT ARTIFACT OR MATCHING SOURCE`;
- exact 1.1.13 mana/cooldown/damage/range/cast/acquisition values — `PENDING`;
- exact 1.1.13 boss/entity/item registry delta — `PENDING`.

No WIP comment from the older source is treated as a current spell.

## Provider-native authority

Iron's remains authority for the canonical addon-facing casting substrate used by these spells: standard spell registration/cast lifecycle, mana, school framework and spell-power plumbing where the provider delegates to Iron's.

Cataclysm: Spellbooks owns:

- its registered spells;
- its provider-owned schools/sub-school and provider attributes/damage types where present;
- its spellbooks, weapons, armor, entities, effects and provider-local state;
- Cataclysm-derived acquisition/progression rules introduced by this addon;
- its own boss/content additions.

L_Ender's Cataclysm remains authority for Cataclysm's original mobs, bosses, materials and mechanics. Theme provenance does not transfer runtime ownership of a Cataclysm: Spellbooks spell back to the base Cataclysm mod.

Black Arcana must not:

- charge a second mana/resource for a normal provider cast;
- replay provider damage/healing/summon settlement;
- duplicate provider cooldowns;
- convert provider-local state into Black Arcana authority;
- treat spectacular Cataclysm presentation as proof of a semantic gap;
- invent compatibility hooks against the beta without an exact supported seam.

## Current deduplication impact

### Infernal / Black Flame / Fire

The 1.1.11-labelled baseline already contains nine concrete Fire/Ignis registrations, including Incineration, Infernal Strike, Hellish Blade, Bone Storm, Bone Pierce, Ashen Breath and Tectonic Tremble. These are enough to block naive reskins in Black Arcana even before the exact 1.1.13 table is available.

Infernal remains a candidate school only after comparison against:

- Iron's Fire;
- Cataclysm: Spellbooks current Fire/Ignis content;
- Black Arcana Black Flame;
- Ignis Soulfires and Ignis Soulfires: Spellbooks;
- Soul Fire'd and other soul-fire providers;
- Somake's infernal/soul-fire ritual surface.

### Order / Technomancy

The current publisher explicitly exposes Technomancy. The old 1.1.11-labelled source registers the Technomancy school but no concrete Technomancy spells, proving that the source snapshot cannot stand in for the current provider.

Order candidates involving controlled beams, projectiles, constructs, battlefield systems, mechanical suppression or deterministic machine-like magic must be compared against the exact current Technomancy set when it becomes available.

### Chaos / boss-derived magic

Cataclysm boss-derived attacks can visually resemble high-tier chaos/reality magic. Presentation alone is not a semantic gap. Chaos candidates remain blocked until their mechanics are compared against the current 65-spell set.

### Space / gravity / displacement

The old source baseline already includes Void Rune, Void Bulwark, Gravity Storm and Gravitational Pull. Black Arcana Space/Displacement content must preserve its own approved domain contracts and avoid duplicating these provider-owned capabilities merely with different VFX.

### Summons / familiars

The baseline includes multiple Cataclysm-derived summons. These do not automatically become Black Arcana familiars; provider summons retain provider authority. Any future overlap with Familiars & Divination is semantic and must be resolved by role, persistence, control model and acquisition, not by creature appearance.

## World-effect safety

Provider spells remain provider-owned. Black Arcana must not intercept and reapply their block/entity effects as if they originated from the Black Arcana canonical pipeline.

For any independently implemented Black Arcana spell with destructive terrain effects, Black Arcana's own `WorldEffectPolicy` remains mandatory. A provider's willingness to destroy blocks is not permission to bypass Black Arcana safety policy.

## Provenance / license posture

Current CurseForge metadata labels the project **PolyForm Shield License 1.0.0**. The public source snapshot contains `TEMPLATE_LICENSE.txt` with PolyForm Shield 1.0.0, but its `gradle.properties` simultaneously declares `mod_license=All Rights Reserved`.

Because those source-level declarations are not internally uniform and PolyForm Shield includes a noncompete restriction, Black Arcana treats the source strictly as `REFERENCE_ONLY / COMPATIBILITY_TARGET` for factual clean-room cataloging. No source code or assets are copied/adapted.

## Remaining hard blocker

**PENDÊNCIA — REQUER ARTEFATO EXATO / NAVEGAÇÃO EXTERNA CAPAZ DE ENTREGAR O BINÁRIO**

The official CurseForge download flow exposed the 1.1.13 file page and download countdown but did not expose the JAR bytes to the permitted inspection tools in this session. Therefore exact current registry extraction remains fail-closed.

Phase 2M may advance the provider from a generic pending row to a rigorously bounded partial catalog, but it does **not** close the exact-current per-spell inventory gate.