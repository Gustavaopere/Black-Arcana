# `efiscompat` 3.1.0 — evidence and provenance

## Physical pack authority

Current physical artifact:

- `efiscompat-3.1.0.jar`
- mod id `efiscompat`
- runtime `3.1.0`
- display name `Epic Fight & Iron's Spellbook animation compat`
- SHA-1 `4250e1c65732d70d1091cc50b84a91b6ed5b2b3f`
- Minecraft 1.21.1 / NeoForge pack baseline `21.1.248`

The physical modlist/JAR metadata is authority for installed presence/version/hash.

## Publisher release pin

Official CurseForge project:

`https://www.curseforge.com/minecraft/mc-mods/epic-fight-x-irons-spells-enhanced-animations`

Current exact 1.21.1 release page identifies:

- project ID `1109064`;
- file ID `8372294`;
- release `3.1.0`;
- public listing filename `efiscompat-3.1.0-neoforge.jar`;
- file-detail `File name efiscompat-3.1.0.jar`;
- NeoForge / Minecraft 1.21.1;
- upload date `2026-07-05`;
- client + server environment;
- release note: fixed a crash when casting certain spells on dedicated server.

Publisher description states that the mod supplies Epic Fight-style casting animations for Iron's, supports staff variants, data-driven spell animation customization and cancellation when Epic Fight skills such as guard/roll occur.

## Exact official source version pin

Official source repository linked by the publisher:

`domanhthang2110/efiscompat`

The repository default branch is not used as the 1.21.1 version authority because its history diverged/reverted later. The dedicated `1.21.1` branch is pinned at:

`b4b58aff86e707420fac8a7c29fe647d7f5aaac4`

At that immutable revision:

- commit date is `2026-07-05`;
- commit message is `Fixed dedicated server crash`;
- `gradle.properties` declares:
  - `minecraft_version=1.21.1`;
  - `neo_version=21.1.219`;
  - `neo_version_range=[21.1,)`;
  - `irons_spells_version=1.21.1-3.15.6`;
  - `mod_id=efiscompat`;
  - `mod_name=Epic Fight & Iron's Spellbook animation compat`;
  - `mod_version=3.1.0`;
  - `mod_license=GNU GPLv3`;
  - `mod_authors=Yukami`;
- Java toolchain is 21;
- the 3.1.0 commit itself changes `mod_version` from `3.0.0` to `3.1.0` while applying the dedicated-server compatibility fix.

This is strong evidence that the source revision belongs to the exact released 3.1.0 line. It is **not** a cryptographic/source-reproducibility proof that the physical JAR was built byte-for-byte from that tree.

## Dependency evidence

Exact generated NeoForge metadata declares mandatory BOTH-side dependencies:

- NeoForge `[21.1,)`;
- Minecraft `[1.21.1,1.21.2)`;
- Epic Fight `[21,)`;
- Iron's Spells `[1.21.1-3.15.0,)`.

Exact upstream build baseline directly compiles against:

- NeoForge `21.1.219`;
- Iron's `1.21.1-3.15.6`;
- Iron's Lib;
- Placebo;
- an exact Curse Maven Epic Fight file.

It also places several providers in local runtime for development, including ESS Requiem, Ace's Spell Utils, Apothic Attributes, GeckoLib, Caelus, Player Animator, Curios and Shoulder Surfing Reloaded.

Development-runtime presence in `build.gradle` is not promoted to mandatory semantic dependency unless runtime metadata/code actually requires it.

Physical Black Arcana pack currently uses:

- NeoForge `21.1.248`;
- Epic Fight `21.17.3.1`;
- Iron's `1.21.1-3.16.3`;
- Iron's Lib `1.21.1-2.1.0`;
- ESS Requiem `0.1.7`;
- Ace's Spell Utils `1.2.7.2-1.21.1`;
- Apothic Attributes `2.10.1`;
- Curios `9.5.1+1.21.1`;
- Player Animator `2.0.4+1.21.1`.

Declared host ranges are satisfied, but exact mixin target/API/event-order compatibility on the newer physical host stack remains runtime QA.

## Source-derived catalog facts

At the exact source revision:

- 28 Java source files;
- 35 provider animation accessor declarations;
- 12 required mixins:
  - 6 client;
  - 6 common;
- 6 common config keys;
- data reload through `SpellAnimationLoader` rooted at `spell_animations`;
- a 9-role spell animation mapping schema;
- provider default mapping plus mappings for Iron's and selected addon spells;
- `SpellPreCastEvent` gate from Epic Fight stunned/recent-action state;
- server-side cancellation via Iron's `Utils.serverSideCancelCast(...)` for skill/guard/dodge interactions;
- cast-complete/cancel hooks that clean Epic Fight animation layers;
- 0 standalone provider spell registrations;
- 0 provider-owned mana/resource system;
- no Black Arcana runtime state.

## Mixin target uncertainty preserved

`MixinComboBasicAttack` targets the string class:

`com.p1nero.invincible.skill.ComboBasicAttack`

The exact source does not annotate that mixin as `@Pseudo`, and `neoforge.mods.toml` does not declare a dependency corresponding to the `com.p1nero.invincible` namespace.

The current top-level physical modlist does not expose an obvious `invincible` or Nightfall provider row. That does not prove the target class cannot be present through another artifact or internal packaging. Consequently:

- the source intent is cataloged;
- target ownership/presence in the physical pack remains `NÃO VERIFICADO`;
- no Black Arcana integration may bind to that target;
- full physical startup/mixin QA remains required.

## License / notice conflict

Two publisher/source surfaces disagree:

- CurseForge project/file metadata currently labels the project **MIT License**;
- exact source `gradle.properties` declares `mod_license=GNU GPLv3`;
- exact generated `neoforge.mods.toml` uses that source `mod_license` value;
- no root `LICENSE` file was present in the exact source tree inspected through the GitHub tree API.

Therefore this audit records **LICENSE METADATA CONFLICT** rather than choosing one license as resolved authority for code/assets.

Black Arcana treatment:

- source/data inspection is read-only for factual interoperability/cataloging;
- no provider implementation or animation assets are copied/adapted;
- any future code/asset reuse is blocked pending independent license/notice reconciliation;
- clean-room architectural design remains mandatory regardless of eventual license resolution.

## Clean-room / authority boundary

The audit uses provider source only to establish factual identities, event/mixin behavior and interop boundaries.

Black Arcana does not adopt:

- `MagicData` as BA casting state;
- Iron's event lifecycle as BA's canonical cast lifecycle;
- `serverSideCancelCast` as BA cancellation implementation;
- provider animation classes/assets/data as BA animation content;
- provider config as BA gameplay configuration.

BA retains one canonical server-authoritative casting pipeline and its own Corruption, Strain, Arcane Danger, ritual/hazard and world-effect authorities.

## Runtime QA still required

Catalog closure does not assert:

- source↔physical-JAR byte identity;
- successful application of all 12 required mixins in the full physical modpack;
- physical ownership/presence of the `com.p1nero.invincible.skill.ComboBasicAttack` target;
- event/mixin ordering with other Epic Fight/Iron's compatibility mods;
- correctness of every bundled animation mapping against physical addon versions;
- successful dedicated-server/client multiplayer smoke for this exact modpack composition;
- a stable public Epic Fight hook suitable for future BA-native casting integration.

These remain fail-closed QA/integration questions, not reasons to leave the provider's semantic inventory open.

## Closure rationale

`efiscompat` can be catalog-closed because its exact current source-version surface is bounded and its ownership is clear: **0 spells, animation registration/data mapping plus Iron's↔Epic Fight casting-interaction reconciliation**.

The component therefore contributes one provider-catalog closure point while keeping every physical-runtime interoperability claim that was not directly tested explicitly fail-closed.