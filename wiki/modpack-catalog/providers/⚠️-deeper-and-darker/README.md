# Deeper and Darker — 1.4.1

Status: `⚠️ PARTIAL / PUBLIC 1.4.1 BASELINE + EXACT SOURCE TAG CORROBORATED / PHYSICAL JAR UNMATCHED / 3 SUPERNATURAL ACTION ROOTS IN PUBLIC+SOURCE BASELINE / +0 STRICT`

## Current physical identity

Current sibling physical authority records:

- row: **#215**;
- JAR: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- mod id: `deeperdarker`;
- runtime: `1.4.1`;
- physical SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`.

The mod is cross-domain: its sibling category is dimension/worldgen/mobs rather than `Magic`, but its player-facing surface includes supernatural portal, staff and Soul Elytra actions.

This folder is only for the base provider **Deeper and Darker**. The separate `darkermagic` / **Deeper and Darker: Spellbooks** addon has its own provider folder and is not folded into this denominator.

## Publisher origin and local post-install modification — blocker

NON-MERGE PR **#517** tested every relevant official 1.4.1 distribution path:

- GitHub release `v1.4.1`;
- Modrinth version `TuD0Zvi3`;
- CurseForge File `8201775`.

All three official paths resolve to the same public artifact:

- SHA-1: `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`;
- SHA-256: `eee3f51222b0bcc714def002ff089ac9e131d3cae4575b542fd0a7dd101fe0af`;
- bytes: `3,906,057`.

That artifact does **not** equal the physical pack fingerprint `83f7edd0...`. The pack JAR is therefore `OTHER_VERIFIED` relative to the official public release and cannot inherit the public semantic denominator as exact-current.

Publisher-baseline audit run `36959073485` completed successfully and produced evidence artifact `11206937200` with digest `sha256:b103afe2dd4b52780acf54682ddcca4b6df484df9ad9cf7accd218e443fb8b1f`.

See [`PUBLIC-1.4.1-BASELINE-AUDIT.md`](PUBLIC-1.4.1-BASELINE-AUDIT.md).

### Local installation provenance

A retained CurseForge instance-metadata snapshot narrows the origin of the current mismatch:

- project: **659011**;
- installed/latest File: **8201775**;
- original installed filename: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- original File SHA-1 recorded by CurseForge: `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`;
- original File length: **3,906,057 bytes**;
- the snapshot records `isModified=false`, `isWorkingCopy=false` and `isFuzzyMatch=false` at that capture point.

The later physical modlist records the **same filename, mod id, runtime and byte length lineage**, but measures SHA-1 `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`.

This closes an important provenance question: the current physical fingerprint is **not evidence of a second official 1.4.1 release**. The retained installation history points to the official File 8201775 as the original installed artifact, followed by a local byte-level change/repack before the later physical hash snapshot.

It does **not** identify which archive entries changed. Therefore it does not authorize projecting the official three-root denominator onto the physical JAR.

### Known local compatibility signal

Logs from the local compatibility-work window record Deeper and Darker `PlayerMixin` / `ServerPlayerMixin` redirect conflicts with NeoVitae around container `stillValid(...)` handling. Project Library metadata also retains two generated Deeper and Darker compatibility JARs from 2026-08-18: a first variant at **3,906,052 bytes** and a `v2` variant at **3,906,044 bytes**.

The retained boot after the first generated set still records the Deeper/NeoVitae `ServerPlayerMixin` redirect conflict. A later boot captured after the `v2` generation positively records Deeper and Darker applying `ContainerMenuMixin` `stillValid(...)` injections to vanilla container menus. However, retained pre-v2 logs also expose `ContainerMenuMixin`, so that surface is not treated as a v2 deployment fingerprint or as proof that v2 caused a runtime transition.

This narrows the local modification chronology but does **not** identify the deployed bytes. The generated JARs are not raw-byte accessible in the current audit, so their hashes cannot be compared to physical SHA-1 `83f7edd0...`. Black Arcana therefore does not infer that `v2` was renamed/deployed, that the mixin change is the only archive-level delta, or that every semantic action class is byte-identical to the official publisher artifact.

See [`LOCAL-NEOVITAE-COMPAT-LINEAGE.md`](LOCAL-NEOVITAE-COMPAT-LINEAGE.md).

A bounded reproduction audit in NON-MERGE PR **#604** then generated **57** candidate repacks by removing `PlayerMixin`, `ServerPlayerMixin`, or both from the official mixin config under common and surgical archive strategies. **0/57** candidates matched physical SHA-1 `83f7edd0...`. One candidate matched only the first local JAR's byte length (**3,906,052 bytes**) but had SHA-1 `304eebbb...`; no candidate reproduced the retained `v2` size (**3,906,044 bytes**). This rules out that bounded family as the physical reconstruction but still does not identify the real byte delta.

See [`NEOVITAE-CANDIDATE-REPRO-AUDIT.md`](NEOVITAE-CANDIDATE-REPRO-AUDIT.md).

## Exact source reproduction — corroboration, not closure

The official upstream tag `v1.4.1` resolves to `KyaniteMods/DeeperAndDarker@f7ba235d078411a1165a8cac184adfe0ccc8cebe`.

NON-MERGE PR **#573** rebuilt that exact source pin with Java 21:

- workflow run: `37201343546` — **SUCCESS**;
- evidence artifact: `11303191470`;
- evidence digest: `sha256:33ccbde9972a32b0272abdb9018254ef0bff00c39df6743eeecd57e2597e91ca`;
- rebuilt SHA-1: `23a498b9d80db87c6f81fe40584a0bc04bc80661`;
- rebuilt SHA-256: `8d9dd572306c2e3dc1d1a4508ed599547c423df65f6558915d42360fb76e2f29`;
- rebuilt bytes: `3,904,543`.

The rebuilt source artifact differs from both:

- physical pack SHA-1 `83f7edd0...`;
- official publisher SHA-1 `b6094add...`.

A normalized source-build↔publisher comparison has the same **2,668 file paths** in both artifacts, with **2,408 identical-content entries** and **260 changed-content entries**. The semantic-path filter over those differences finds only three Otherside portal asset resources and no source-only/publisher-only semantic path. This corroborates the public action-family inventory but does **not** reveal the unmatched physical JAR.

See [`SOURCE-1.4.1-REPRO-AUDIT.md`](SOURCE-1.4.1-REPRO-AUDIT.md).

## Public/source 1.4.1 supernatural baseline

The official public artifact and exact upstream source pin corroborate three discrete player-owned supernatural actions:

1. **Otherside Portal Activation** — Heart of the Deep used on a valid reinforced-deepslate portal frame invokes provider portal creation;
2. **Sonorous Staff Sonic Boom** — deliberate charged staff release emits the provider sonic-boom damage/knockback action;
3. **Soul Elytra Boost** — dedicated client BOOST keybind sends `soul_elytra_boost` to the server; when eligible, the provider supplies a firework-style flight boost and applies its cooldown.

Detailed cards: [`actions/PUBLIC-BASELINE-ACTIONS.md`](actions/PUBLIC-BASELINE-ACTIONS.md).

## Exclusions from the semantic baseline

The binary and source audits observe adjacent player-facing surfaces that do not create separate semantic magic identities under the Black Arcana ledger:

- Ancient Compass — structure locator state;
- Sculk Transmitter / transmit keybind — remote container/block interaction utility;
- Soul Elytra item tick — presentation/cooldown state, separate from the active boost packet;
- Warden Armor — passive blindness/darkness suppression;
- boats and Lily Flower — ordinary placement;
- portal traversal after portal creation — consequence of the portal action, not a second spell;
- `Catalysis` and `Sculk Smite` — enchantment effects/modifiers, not standalone semantic actions;
- `Volume` and `Reverberation` — modifiers of the same Sonorous Staff action, not separate actions.

## Acquisition baseline

Public 1.4.1 provider data closes baseline acquisition:

- `deeperdarker:heart_of_the_deep` is added to the vanilla Warden loot table by a provider loot modifier;
- `deeperdarker:sonorous_staff` has a provider shaped recipe using Heart of the Deep, Soul Crystal and Sculk Bone;
- Soul Elytra is provider equipment; exact current-pack acquisition is not projected from the public release because the physical JAR differs.

## Soul Elytra config condition

The exact 1.4.1 source registers a NeoForge `COMMON` config and defines `soulElytraCooldown` with a default of **600 ticks**, valid range **-1..12000**, with `-1` disabling Soul Elytra Boost.

Retained runtime logs positively show the deployed instance tracking, loading and watching `config/deeperdarker-common.toml` across multiple boots. This closes the deployed config **path**, but not the effective value: the standalone TOML bytes are not retained in the current Project Library and the logs do not print `soulElytraCooldown`.

Therefore Black Arcana does not infer `600` from the source default or from successful config loading. Soul Elytra Boost remains independently conditioned on deployed-config evidence even after any future physical-JAR closure.

See [`DEPLOYED-CONFIG-CHECKPOINT.md`](DEPLOYED-CONFIG-CHECKPOINT.md).

## Strict accounting

Because the physical JAR is not byte-equivalent to any official public 1.4.1 artifact, is not reproduced by a clean build of the official `v1.4.1` source pin, and its raw bytes are not currently available to this audit despite the retained Library/instance metadata:

- public/source baseline roots: **3**;
- exact-current physical roots: **UNKNOWN**;
- strict semantic contribution: **+0**;
- folder state: **⚠️ partial/conditioned**.

## Closure requirement

Promote this provider only after one of these evidence paths closes the installed bytes:

- direct raw-byte inspection of the physical `deeperdarker-neoforge-1.21.1-1.4.1.jar`; or
- a publisher/repository artifact whose SHA-1 exactly equals `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`.

The exact official source tag is now audited and is **not** a hash match, so version/source-label agreement alone is not sufficient.

Until physical closure exists, do not add the three public/source baseline actions to the strict global numerator and do not assume the installed JAR has exactly the same registrations/control flow.
