# Deeper and Darker 1.4.1 — bounded NeoVitae candidate reproduction audit

Status: `BOUNDED REPACK FAMILY TESTED / 0 OF 57 EXACT PHYSICAL SHA-1 MATCHES / FIRST LOCAL SIZE REPRODUCED BY ONE NON-IDENTICAL CANDIDATE / V2 SIZE NOT REPRODUCED / PHYSICAL TRANSFORMATION STILL UNKNOWN / FAIL-CLOSED`

## Scope

This checkpoint records the evidence produced by NON-MERGE audit PR **#604**. It is limited to the base provider **Deeper and Darker** / `deeperdarker`.

It does not audit or modify the separate **Deeper and Darker: Spellbooks** / `darkermagic` addon.

The purpose was to test a bounded, reproducible hypothesis about the local 2026-08-18 Deeper ↔ NeoVitae compatibility work without committing or publishing any third-party JAR bytes.

## Fixed identities

Official public Deeper and Darker 1.4.1:

- filename: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- size: **3,906,057 bytes**;
- SHA-1: `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`;
- SHA-256: `eee3f51222b0bcc714def002ff089ac9e131d3cae4575b542fd0a7dd101fe0af`.

Current physical pack authority:

- filename: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- mod id: `deeperdarker`;
- runtime: `1.4.1`;
- physical SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`.

Retained generated local artifact sizes:

- first compatibility JAR: **3,906,052 bytes**;
- `v2` compatibility JAR: **3,906,044 bytes**.

## Exact source hypothesis tested

Exact upstream `v1.4.1` source lists both redirect mixins in `deeperdarker.mixins.json`:

- `PlayerMixin`;
- `ServerPlayerMixin`.

Those mixins redirect `AbstractContainerMenu.stillValid(...)`, the same compatibility seam implicated by retained NeoVitae conflict logs.

The audit therefore tested only three bounded semantic transforms of the official release mixin config:

1. remove `PlayerMixin` only;
2. remove `ServerPlayerMixin` only;
3. remove both `PlayerMixin` and `ServerPlayerMixin`.

No other class, resource, manifest or archive entry was intentionally modified by the surgical candidate family.

## Repack families

For each of the three semantic transforms, the audit generated:

### Python `zipfile` rewrite

- default compression behavior;
- DEFLATE levels **1–9**.

Total: **10 candidates per semantic transform**.

### Surgical single-entry replacement

The audit preserved all other archive bytes and central/local entry metadata while replacing only `deeperdarker.mixins.json`, at DEFLATE levels **1–9**.

Total: **9 candidates per semantic transform**.

Overall bounded matrix:

- 3 semantic transforms;
- 19 archive variants per transform;
- **57 candidates total**.

## Execution evidence

NON-MERGE PR: **#604**

Successful reproduction run:

- workflow run: **37238826068**;
- audit HEAD: `2d5623112face63356b7e64baac924e6b800a753`;
- text evidence artifact: **11316632886**;
- artifact digest: `sha256:4a1e20380caba07e25cef8487135c6ff693e0638e47c86b32fc6189d31b38006`.

The uploaded artifact contains only JSON/Markdown hashes and sizes. No official or generated candidate JAR bytes were uploaded.

## Result

### Exact physical SHA-1

Candidates equal to physical SHA-1 `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`:

**0 / 57**

Disposition:

`NO_EXACT_PHYSICAL_MATCH_IN_BOUNDED_CANDIDATE_FAMILY`

Therefore none of the tested “remove Player / remove ServerPlayer / remove both” repacks, under the enumerated archive strategies and compression levels, reproduces the physical pack artifact.

### First local compatibility-JAR size

Retained first local size:

**3,906,052 bytes**

Exactly one tested candidate reproduced that size:

- semantic transform: remove `ServerPlayerMixin`;
- archive strategy: surgical single-entry replacement;
- DEFLATE level: **4**;
- candidate size: **3,906,052 bytes**;
- candidate SHA-1: `304eebbbf9c36e04003158903ba619513dddad72`.

That SHA-1 does **not** equal the physical pack SHA-1.

The size equality is therefore only a bounded structural clue. It is not byte identity and does not prove that the retained first generated compatibility JAR used this transform.

### V2 local compatibility-JAR size

Retained `v2` size:

**3,906,044 bytes**

Candidates reproducing that size:

**0 / 57**

The bounded matrix therefore does not reproduce even the retained v2 artifact size.

## Interpretation

The audit materially narrows what the physical artifact is **not**.

It rules out the tested candidate family as an exact reconstruction of physical SHA-1 `83f7edd0...`.

It also weakens the simple hypothesis that the retained `v2` JAR was produced only by deleting both conflicting redirect mixin names from the official `deeperdarker.mixins.json` under one of the tested common repack strategies.

It does **not** establish:

- the actual entry-level delta of either retained generated compatibility JAR;
- that the first local JAR removed only `ServerPlayerMixin`;
- that either generated compatibility JAR was deployed under the canonical filename;
- which additional class/resource/archive metadata changes may have occurred;
- that the physical `83f7...` JAR is semantically identical to the official release.

A candidate size match is not a hash/content match.

## Catalog consequence

No semantic or structural promotion follows.

Current state remains:

- public/source supernatural baseline: **3 roots**;
- exact-current physical roots: **UNKNOWN**;
- strict semantic contribution: **+0**;
- provider state: **⚠️ partial / conditioned**.

The established public/source roots remain:

1. Otherside Portal Activation;
2. Sonorous Staff Sonic Boom;
3. Soul Elytra Boost.

## Remaining closure requirement

Promotion to `✅ Catalogado` still requires an exact bridge to the installed bytes, such as:

- authorized raw-byte inspection of the physical `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- raw-byte inspection/hash of the retained generated compatibility JARs followed by an exact comparison;
- or another exact artifact whose SHA-1/content is proven identical to physical `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`.

Until then, Black Arcana remains fail-closed and does not project the three public/source roots into the strict exact-current numerator.
