# Deeper and Darker 1.4.1 — exact source reproduction audit

Status: `SOURCE TAG REPRODUCED / SOURCE BUILD != PHYSICAL / SOURCE BUILD != PUBLISHER / PUBLIC 3-ROOT SEMANTIC BASELINE CORROBORATED / PHYSICAL DENOMINATOR OPEN`

## Scope

This audit is limited to the base provider **Deeper and Darker**. It does not audit or modify the separate addon **Deeper and Darker: Spellbooks** / `darkermagic`.

## Physical authority

Current sibling physical authority records:

- JAR: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- mod id: `deeperdarker`;
- runtime: `1.4.1`;
- physical SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`.

That fingerprint remains the installed-byte authority.

## Exact upstream source pin

Official upstream tag `v1.4.1` resolves to:

- repository: `KyaniteMods/DeeperAndDarker`;
- commit: `f7ba235d078411a1165a8cac184adfe0ccc8cebe`;
- Minecraft: `1.21.1`;
- NeoForge build dependency: `21.1.233`;
- Java toolchain: `21`;
- mod id: `deeperdarker`;
- mod version: `1.4.1`.

The official GitHub release asset for the same tag is the already-audited publisher artifact:

- SHA-1: `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`;
- SHA-256: `eee3f51222b0bcc714def002ff089ac9e131d3cae4575b542fd0a7dd101fe0af`;
- bytes: `3,906,057`.

## Reproduction evidence

NON-MERGE PR **#573** rebuilt the exact upstream commit with Java 21 and compared the produced JAR against both the physical fingerprint and official release asset.

Evidence:

- branch/head: `audit/deeper-and-darker-1.4.1-source-repro-2026-10-04@6919b34fd0186028f4618cc108bcc273e79e518f`;
- workflow run: `37201343546` — **SUCCESS**;
- evidence artifact: `11303191470`;
- evidence digest: `sha256:33ccbde9972a32b0272abdb9018254ef0bff00c39df6743eeecd57e2597e91ca`.

Rebuilt source artifact:

- SHA-1: `23a498b9d80db87c6f81fe40584a0bc04bc80661`;
- SHA-256: `8d9dd572306c2e3dc1d1a4508ed599547c423df65f6558915d42360fb76e2f29`;
- bytes: `3,904,543`.

Therefore:

- `source_build_sha1 != physical_sha1`;
- `source_build_sha1 != publisher_sha1`;
- the exact upstream source tag does **not** reproduce either the installed physical JAR or the official published JAR byte-for-byte under this clean rebuild.

No equivalence is inferred from equal version labels.

## Normalized source-build versus publisher comparison

Comparing file contents inside the rebuilt source JAR and official release JAR while excluding ZIP directory entries produced:

- source file entries: **2,668**;
- publisher file entries: **2,668**;
- same-content entries: **2,408**;
- changed-content entries: **260**;
- source-only entries: **0**;
- publisher-only entries: **0**.

The two artifacts therefore expose the same file-path set but are not content-identical.

The semantic-path filter over the 260 changed entries found only:

- `assets/deeperdarker/models/block/otherside_portal_ew.json`;
- `assets/deeperdarker/models/block/otherside_portal_ns.json`;
- `assets/deeperdarker/textures/block/otherside_portal.png.mcmeta`.

No source-only or publisher-only semantic path was found by that filter. This strengthens source↔publisher corroboration of the previously identified action families, but it still cannot establish the contents of the unmatched physical JAR.

## Exact source semantic corroboration

The pinned source directly corroborates the three public-baseline supernatural action roots.

### Otherside Portal Activation

`WardenHeartItem.useOn(...)` admits use only in Overworld/Otherside and calls the provider-owned Otherside portal block's `spawnPortal(...)`. Successful activation consumes the Heart for non-creative players.

Semantic disposition: one deliberate supernatural portal-creation action.

### Sonorous Staff Sonic Boom

`SonorousStaffItem.use(...)` begins charging and `releaseUsing(...)` performs the provider sonic attack, including range/damage calculation, sonic damage, knockback, durability and cooldown settlement.

`Volume` and `Reverberation` are read as modifiers of that same release action.

Semantic disposition: one deliberate supernatural staff attack.

### Soul Elytra Boost

The client exposes a dedicated BOOST keybind. `SoulElytraBoostPacket` is the provider payload for `deeperdarker:soul_elytra_boost`; the server-side handler checks configured enablement, fall-flying state, equipped Soul Elytra and cooldown, then creates the boost and applies cooldown.

The exact source default for `soulElytraCooldown` is **600 ticks** and `-1` disables the boost. The deployed pack value is not versioned in the sibling repository and is therefore not inferred.

Semantic disposition: one deliberate supernatural equipment/flight action in the public/source baseline, with an additional deployed-config condition.

## Explicit non-identities

The exact source also corroborates exclusions already made by the public binary audit:

- Sculk Transmitter — remote block/container interaction utility;
- Ancient Compass — structure locator;
- Soul Elytra ordinary item tick — presentation/state support rather than the boost action;
- Warden Armor passive behavior — passive state;
- portal collision/traversal after activation — downstream lifecycle;
- `Catalysis`, `Sculk Smite`, `Volume`, `Reverberation` — provider enchantments/modifiers, not standalone semantic magic actions under the Black Arcana ledger.

## Accounting

Evidence now supports:

- official publisher baseline roots: **3**;
- exact upstream source corroborated roots: **3**;
- exact-current physical roots: **UNKNOWN**;
- strict current contribution: **+0**;
- provider state: **⚠️ partial / physical denominator open**.

The source reproduction closes a provenance question, not the installed artifact.

## Remaining closure requirement

Promotion to `✅ Catalogado` requires direct evidence for the installed physical bytes, such as:

- direct inspection of the physical `deeperdarker-neoforge-1.21.1-1.4.1.jar`; or
- a repository/publisher artifact whose SHA-1 exactly equals `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`.

Until that occurs, Black Arcana must not project the public/source three-root denominator onto the physical pack.
