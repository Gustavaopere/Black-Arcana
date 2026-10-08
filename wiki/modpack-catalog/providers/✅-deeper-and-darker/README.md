# Deeper and Darker — 1.4.1

**Current physical-JAR intake override (2026-10-08):** direct inspection of the exact `83f7edd0...` JAR closes the **3-root physical semantic inventory** with **2 `COUNTED_EXACT` actions + 1 Soul Elytra config-conditional**. Deeper and Darker now contributes **+2 strict**. Its old raw-JAR-unavailable premise below is historical; the deployed `soulElytraCooldown` remains unknown, so the provider folder remains ⚠️. See [`PHYSICAL-JAR-DIRECT-AUDIT-2026-10-08.md`](PHYSICAL-JAR-DIRECT-AUDIT-2026-10-08.md).

Status: `⚠️ PARTIAL / EXACT PHYSICAL JAR VERIFIED / 3 CURRENT ACTION ROOTS / 2 COUNTED_EXACT + 1 SOUL ELYTRA CONFIG-CONDITIONAL / STRICT +2 / RUNTIME QA PENDING`

## Current physical identity

Current sibling physical authority records:

- row: **#215**;
- JAR: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- mod id: `deeperdarker`;
- runtime: `1.4.1`;
- physical SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`.

The mod is cross-domain: its sibling category is dimension/worldgen/mobs rather than `Magic`, but its player-facing surface includes supernatural portal, staff and Soul Elytra actions.

This folder is only for the base provider **Deeper and Darker**. The separate `darkermagic` / **Deeper and Darker: Spellbooks** addon has its own provider folder and is not folded into this denominator.

## Publisher origin and local post-install modification — historical provenance gap

NON-MERGE PR **#517** tested every relevant official 1.4.1 distribution path:

- GitHub release `v1.4.1`;
- Modrinth version `TuD0Zvi3`;
- CurseForge File `8201775`.

All three official paths resolve to the same public artifact:

- SHA-1: `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`;
- SHA-256: `eee3f51222b0bcc714def002ff089ac9e131d3cae4575b542fd0a7dd101fe0af`;
- bytes: `3,906,057`.

That artifact does **not** equal the physical pack fingerprint `83f7edd0...`; the pack JAR remains `OTHER_VERIFIED` relative to the publisher release. Before the 2026-10-08 direct physical-JAR intake, this mismatch blocked exact-current semantic accounting. It still blocks claims of publisher-byte identity or patch provenance, but no longer blocks the three-root *directly inspected* current physical inventory.

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

The later physical modlist records the **same filename, mod id and runtime**, and measures SHA-1 `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`. That physical table has no JAR-size column, so no same-byte-length claim is made for the later snapshot.

This closes an important provenance question: the current physical fingerprint is **not evidence of a second official 1.4.1 release**. The retained installation history points to the official File 8201775 as the original installed artifact, followed by a local byte-level change/repack before the later physical hash snapshot.

The installation provenance does **not** identify which archive entries changed. That historical evidence alone cannot project the official three-root denominator onto the physical JAR; the three roots were subsequently established independently by direct inspection of the matching current physical bytes.

### Known local compatibility signal

Logs from the local compatibility-work window record Deeper and Darker `PlayerMixin` / `ServerPlayerMixin` redirect conflicts with NeoVitae around container `stillValid(...)` handling. Project Library metadata also retains two generated Deeper and Darker compatibility JARs from 2026-08-18: a first variant at **3,906,052 bytes** and a `v2` variant at **3,906,044 bytes**.

The retained boot after the first generated set still records the Deeper/NeoVitae `ServerPlayerMixin` redirect conflict. A later boot captured after the `v2` generation loads both mods under their **canonical JAR filenames**, advances beyond that earlier redirect-conflict failure point, and eventually crashes for an unrelated Photon config lifecycle error. It also records Deeper and Darker `ContainerMenuMixin` activity; because retained pre-v2 logs already expose `ContainerMenuMixin`, that surface is not treated as a v2 deployment fingerprint or as proof that v2 caused a runtime transition.

This historical chronology does **not** identify whether either generated compatibility JAR became the deployed artifact: the *generated candidate* JARs remain unavailable for byte-level comparison. Separately, the 2026-10-08 uploaded current physical JAR now matches `83f7edd0...` and has been inspected directly. That does not establish the `v2` candidate's deployment, the full archive-level delta or byte identity of the semantic classes with the official publisher artifact.

A retained physical inventory from **2026-08-22** now directly binds the canonical `deeperdarker-neoforge-1.21.1-1.4.1.jar` row to SHA-1 `83f7edd0a8516b2767c2cda7a3b2402f9e290d88` / fingerprint `1917446721`. The current physical artifact was therefore present in the canonical pack slot no later than 2026-08-22, roughly four days after the 2026-08-18 compatibility-work window. This narrows chronology only; it does not prove that either generated compatibility JAR became those bytes.

See [`LOCAL-NEOVITAE-COMPAT-LINEAGE.md`](LOCAL-NEOVITAE-COMPAT-LINEAGE.md) and [`PHYSICAL-83F7-AUG22-CHECKPOINT.md`](PHYSICAL-83F7-AUG22-CHECKPOINT.md).

A bounded reproduction audit in NON-MERGE PR **#604** first tested **57** candidate repacks by removing `PlayerMixin`, `ServerPlayerMixin`, or both from the official mixin config under common and surgical archive strategies. **0/57** candidates matched physical SHA-1 `83f7edd0...`; that initial matrix reproduced the first local JAR's size once but did not reproduce the retained `v2` size.

The expanded NON-MERGE audit **#622** then tested **80** candidates, validated the CurseForge fingerprint implementation against the official artifact, and found a coherent serialization/repack family that reproduces **both retained local sizes**. Even so, **0/80** candidates matched physical SHA-1 `83f7edd0...` or physical fingerprint `1917446721`. The size chronology is therefore structurally plausible, but the deployed physical transformation remains unidentified.

NON-MERGE audit **#632** separately tested the narrower hypothesis that the physical JAR is only a full repack/recompression of the publisher **effective extracted file tree**, with no extracted file-content changes. The successful run validated the publisher fingerprint and measured **61** effective-content-identical Info-ZIP/JDK rebuilds; **0/61** matched physical SHA-1 `83f7edd0...` or fingerprint `1917446721`. This rules out the bounded no-op full-repack family tested there, but it does not prove that every archive serializer/metadata layout has been excluded or that semantic file content necessarily changed.

Follow-up NON-MERGE audit **#635** re-downloaded the verified publisher artifact and inspected its central-directory/local-header/span structure directly. It found **2,900 unique entries**, **0** duplicate names, **0** duplicate local-header offsets, **0** CPython-style overlap-span violations, **0** full-entry `zipfile` read errors, `ZipFile.testzip() == NONE`, and **0** local-vs-central metadata mismatches. That result supersedes only the earlier explanatory note that publisher ZIP overlap forced #632's extraction boundary; the measured **0/61** #632 no-match remains valid.

NON-MERGE audit **#640** then filled the Python-`zipfile` gap left by #632. It measured **22** content-identical full rewrites across two `ZipInfo` strategies and default/0–9 DEFLATE settings. **0/22** matched physical SHA-1 `83f7edd0...` or fingerprint `1917446721`; **0/22** matched either retained local compatibility-JAR size. Four candidates reproduced the publisher total size exactly, but collapsed to SHA-1 `eb6f9fbc5adfc4e12de9e6b2462370da74572acc` / fingerprint **824150764**, so size equality did not establish identity.

See [`NEOVITAE-CANDIDATE-REPRO-AUDIT.md`](NEOVITAE-CANDIDATE-REPRO-AUDIT.md), [`NEOVITAE-PATCH-REPRO-AUDIT.md`](NEOVITAE-PATCH-REPRO-AUDIT.md), [`CONTENT-IDENTICAL-REPACK-AUDIT.md`](CONTENT-IDENTICAL-REPACK-AUDIT.md), [`PUBLISHER-ZIP-STRUCTURE-AUDIT.md`](PUBLISHER-ZIP-STRUCTURE-AUDIT.md), and [`PYTHON-ZIPFILE-REPACK-AUDIT.md`](PYTHON-ZIPFILE-REPACK-AUDIT.md).

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

## Public/source 1.4.1 supernatural baseline — corroborated by the physical JAR

The official public artifact and exact upstream source pin corroborate three discrete player-owned supernatural actions:

1. **Otherside Portal Activation** — Heart of the Deep used on a valid reinforced-deepslate portal frame invokes provider portal creation;
2. **Sonorous Staff Sonic Boom** — deliberate charged staff release emits the provider sonic-boom damage/knockback action;
3. **Soul Elytra Boost** — dedicated client BOOST keybind sends `soul_elytra_boost` to the server; when eligible, the provider supplies a firework-style flight boost and applies its cooldown.

Detailed cards:

- aggregate baseline: [`actions/PUBLIC-BASELINE-ACTIONS.md`](actions/PUBLIC-BASELINE-ACTIONS.md);
- [Otherside Portal Activation](actions/otherside-portal-activation.md);
- [Sonorous Staff Sonic Boom](actions/sonorous-staff-sonic-boom.md);
- [Soul Elytra Boost](actions/soul-elytra-boost.md).

Individual-card materialization checkpoint: [`INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md`](INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md).

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
- Soul Elytra is provider equipment; the exact physical JAR contains its recipe. Eligibility to *activate the boost* remains contingent on the current deployed COMMON `soulElytraCooldown` value.

## Soul Elytra config condition

The exact 1.4.1 source registers a NeoForge `COMMON` config and defines `soulElytraCooldown` with a default of **600 ticks**, valid range **-1..12000**, with `-1` disabling Soul Elytra Boost.

Retained runtime logs positively show the deployed instance tracking, loading and watching `config/deeperdarker-common.toml` across multiple boots. This closes the deployed config **path**, but not the effective value: the standalone TOML bytes are not retained in the current Project Library and the logs do not print `soulElytraCooldown`.

Therefore Black Arcana does not infer `600` from the source default or from successful config loading. Soul Elytra Boost remains independently conditioned on deployed-config evidence even after any future physical-JAR closure.

See [`DEPLOYED-CONFIG-CHECKPOINT.md`](DEPLOYED-CONFIG-CHECKPOINT.md).


## Deployed evidence collector support

The canonical read-only collector at `docs/qa/provider-catalog-deployed-evidence-collector.py` now has a bounded Deeper and Darker surface:

- hashes only `mods/deeperdarker-neoforge-1.21.1-1.4.1.jar` for this provider and reports whether it equals current physical SHA-1 `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`;
- reads only `config/deeperdarker-common.toml` for the exact key `soulElytraCooldown`;
- accepts only an observed integer in the provider range `-1..12000`; missing, malformed, ambiguous, wrong-type or out-of-range evidence stays fail-closed;
- does not copy the surrounding TOML or substitute the source default.

An authoritative current-instance collector report can close the remaining deployed-config subgate independently. Exact-current semantic inventory is already closed by the 2026-10-08 direct JAR inspection, so no additional raw-byte acquisition or publisher-match search is required. The config report alone is not a live-modpack gameplay PASS.

## Current strict accounting — 2026-10-08

- exact physical semantic-action roots: **3**, independently observed in the matching current JAR;
- `COUNTED_EXACT`: **2** — Otherside Portal Activation and Sonorous Staff Sonic Boom, with physical triggering/acquisition evidence;
- `CONDITIONAL`: **1** — Soul Elytra Boost, with a physical recipe/packet but missing deployed `soulElytraCooldown`;
- current provider strict contribution: **+2**;
- global strict minimum after PR #697: **1851**;
- provider folder: **⚠️ partial/conditioned**, not ✅ runtime-qualified.

## Remaining closure requirements

1. Capture the effective `config/deeperdarker-common.toml -> soulElytraCooldown` from the authoritative current assembled instance using the bounded collector. The source default `600` is not an observed deployed value; `-1` disables the boost.
2. Reconcile enabled/disabled Soul Elytra eligibility and strict accounting from that *observed* value without manufacturing a survival or runtime claim.
3. Perform provider-native/current-modpack runtime acceptance (including NeoVitae coexistence and the Soul Elytra boost path when enabled). A six-entry active mixin configuration and static packet analysis are not runtime acceptance.

Direct physical-byte inspection is already complete. Publisher hash mismatch remains a provenance limitation, **not** an outstanding raw-JAR semantic-inventory gate. See [`PHYSICAL-JAR-DIRECT-AUDIT-2026-10-08.md`](PHYSICAL-JAR-DIRECT-AUDIT-2026-10-08.md).
