# Epic Fight x Iron's Spells: Enhanced Animations 3.1.0 — provider catalog

Status: `EXACT PHYSICAL VERSION / EXACT OFFICIAL SOURCE VERSION PIN / CASTING-INTERACTION+ANIMATION COMPAT / 0 STANDALONE SPELLS / CATALOG CLOSED AT SOURCE EVIDENCE CEILING / BINARY+HOST QA FAIL-CLOSED`

## Installed identity

- physical JAR: `efiscompat-3.1.0.jar`
- mod id: `efiscompat`
- runtime: `3.1.0`
- display name from physical metadata: `Epic Fight & Iron's Spellbook animation compat`
- Minecraft / loader: `1.21.1` / NeoForge
- physical SHA-1: `4250e1c65732d70d1091cc50b84a91b6ed5b2b3f`
- CurseForge project/file: `1109064 / 8372294`
- public release filename: `efiscompat-3.1.0-neoforge.jar`
- public release date: `2026-07-05`
- environment: client + server
- provider class: `EPIC FIGHT ↔ IRON'S CASTING-INTERACTION + ANIMATION COMPAT`

Physical modlist/JAR metadata remains authority for the installed artifact. The CurseForge file page is useful release evidence even though it displays the uploaded file as `efiscompat-3.1.0-neoforge.jar` while its file-detail metadata also reports `File name efiscompat-3.1.0.jar`, matching the physical artifact name.

Official source is pinned at:

`domanhthang2110/efiscompat@b4b58aff86e707420fac8a7c29fe647d7f5aaac4`

on the dedicated `1.21.1` branch. That commit is dated `2026-07-05`, is titled `Fixed dedicated server crash`, and changes source metadata from `mod_version=3.0.0` to `mod_version=3.1.0`.

This is an exact **source-version pin**, not a byte-for-byte source↔physical-JAR reproducibility claim.

## What this component is

`efiscompat` makes Iron's Spells casting coexist with Epic Fight's animation/action state. It has two distinct responsibilities:

1. **presentation** — selecting and synchronizing Epic Fight animations for Iron's spell chant/cast/continuous phases, including staff-specific variants and data-driven spell mappings;
2. **casting interaction** — server-side gates/cancellation that reconcile Iron's casting with Epic Fight stun/recent-action/skill states.

It does **not** own Iron's spells, mana, spell effects, spell cooldown storage or targeting. It also does not define a Black Arcana cast path.

The complete current standalone spell inventory for this component is:

**0 registered standalone spells.**

The exact source tree contains no provider-owned spell registry. Its references to `SpellRegistry` resolve Iron's existing spell IDs for animation selection.

## Exact source surface

At the exact 3.1.0 source revision:

- 28 Java source files total;
- 35 provider Epic Fight animation accessors declared in `Animation`;
- 12 required mixins total:
  - 6 client mixins;
  - 6 common mixins;
- 5 common config values;
- 1 JSON reload listener rooted at `spell_animations`;
- 1 nine-field animation-set schema for chant/cast/continuous + left/right staff variants;
- built-in data-driven mappings for Iron's plus selected addon spells, with a default fallback mapping;
- 0 provider-owned standalone spell registrations;
- 0 provider-owned mana/resource registry;
- no Black Arcana state, Corruption, Strain or Arcane Danger surface.

See the dedicated documents for the exact casting/cancellation and presentation boundaries.

## Host dependency contract

Generated NeoForge metadata requires:

- Minecraft `[1.21.1,1.21.2)`;
- NeoForge `[21.1,)`;
- Epic Fight `[21,)`, `BOTH`;
- Iron's Spells `[1.21.1-3.15.0,)`, `BOTH`.

The exact source build baseline uses:

- Java 21;
- NeoForge `21.1.219`;
- Iron's `1.21.1-3.15.6`;
- the exact Epic Fight Curse Maven file pinned by the upstream build.

The physical pack currently has:

- NeoForge `21.1.248`;
- Epic Fight `21.17.3.1`;
- Iron's `1.21.1-3.16.3`;
- Iron's Lib `1.21.1-2.1.0`;
- ESS Requiem `0.1.7`;
- T.O Magic n' Extras / Traveloptics `4.4.0.1-1.21.1`;
- Ace's Spell Utils `1.2.7.2-1.21.1`;
- Player Animator `2.0.4+1.21.1` present both as top-level and jarjar metadata in the current inventory.

The declared dependency ranges are satisfied by the physical host versions, but that is not proof that every required mixin target and event-order interaction remains binary-compatible. Full-modpack runtime QA therefore remains fail-closed.

## Casting-interaction authority

The exact source consumes Iron's server-owned casting state through `MagicData` and Iron's own cast events/utilities.

Observed server-relevant behavior includes:

- `SpellPreCastEvent` can be canceled when Epic Fight reports the player stunned or still inside the configured post-action casting delay;
- Epic Fight skill execution can cancel an in-progress Iron's cast before allowing the skill to continue;
- successful guard can cancel an in-progress cast;
- dodge can cancel an in-progress cast when enabled by provider config;
- a targeted `ComboBasicAttack` compat path refuses that attack while the player is casting;
- Iron's own cast completion/cancellation paths are used as seams to clear Epic Fight animation layers.

These hooks make `efiscompat` a real interaction provider, not merely a cosmetic layer. They still **mediate Iron's cast state** rather than becoming a second casting authority.

## Data-driven animation boundary

`SpellAnimationLoader` reloads JSON resources from `spell_animations`, clears the prior map and builds per-spell animation sets. If a spell mapping is absent it falls back to `default`; if individual fields are null/invalid, those fields are merged from the default mapping.

A mapping can choose nine animation roles:

- chant;
- cast;
- continuous;
- staff chant right;
- staff cast right;
- staff chant left;
- staff cast left;
- staff continuous right;
- staff continuous left.

Animation lookup resolves provider animation fields, Epic Fight animation fields or explicit animation registry keys. These are presentation identities, not spell identities.

## Config surface

Exact common config values:

- `staffWeapon` — explicit staff-item ID list;
- `hideTwoHandedItems` — default `true`;
- `hideOffHandItems` — default `true`;
- `castingDelay` — default `0.0`;
- `EnableSkillCooldown` — default `true`;
- `EnableDodgeCancelling` — default `true`.

The Java class exposes five `ConfigValue` fields after grouping the two hide booleans and three casting-interaction controls plus the staff list; semantically the TOML surface contains the six keys above. Catalog consumers should preserve the actual keys rather than normalize them into Black Arcana settings.

## Black Arcana authority

Black Arcana must not:

- create a second Iron's↔Epic Fight cast-cancellation path;
- translate `efiscompat` animation readiness or pose state into Black Arcana cast authority;
- route Black Arcana casts through Iron's `MagicData` solely to reuse this compat;
- duplicate provider cooldown/cancel decisions for Iron's casts;
- count animation mapping JSONs as spells or spell domains;
- copy provider animation assets or implementation into Black Arcana;
- transfer Black Arcana runtime authority to RPG Skill Tree.

Black Arcana casting, targeting, costs, cooldowns, hazards, rituals, Corruption, Strain, Arcane Danger and `WorldEffectPolicy` remain Black Arcana-owned.

If Black Arcana later needs Epic Fight-aware BA-native casting presentation/action coordination, it requires a separate bounded adapter driven by Black Arcana's canonical server-authoritative cast state and verified Epic Fight hooks. It must not repurpose Iron's state as BA authority.

## Catalog files

- [CAST-INTERACTION-AND-CANCELLATION.md](CAST-INTERACTION-AND-CANCELLATION.md)
- [DATA-DRIVEN-ANIMATION-AND-PRESENTATION.md](DATA-DRIVEN-ANIMATION-AND-PRESENTATION.md)
- [EVIDENCE-AND-PROVENANCE.md](EVIDENCE-AND-PROVENANCE.md)

## Evidence ceiling

Closed for catalog/deduplication:

- installed identity/version/hash;
- exact publisher release and File ID;
- exact official source-version pin;
- zero standalone provider spells;
- source-level dependency metadata;
- complete 28-file Java source surface at the pinned revision;
- exact 12-mixin split;
- provider casting-interaction seams;
- provider animation registration/reload model;
- common config semantics;
- ownership/deduplication boundary.

Still fail-closed for runtime integration:

- independent source↔physical-JAR byte equivalence;
- exact mixin target success on physical Epic Fight `21.17.3.1` + Iron's `3.16.3`;
- combined event/mixin ordering with every other installed Epic Fight/Iron's compat;
- dedicated-server and multiplayer smoke of the physical 3.1.0 artifact inside the full pack;
- correctness of every bundled third-party spell animation mapping against the physical addon versions;
- any future Black Arcana↔Epic Fight adapter contract.