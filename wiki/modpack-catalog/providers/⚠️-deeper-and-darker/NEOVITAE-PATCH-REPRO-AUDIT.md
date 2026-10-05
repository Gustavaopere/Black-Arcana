# Deeper and Darker 1.4.1 — extended NeoVitae patch reproduction audit

Status: `80 CANDIDATES TESTED / CURSEFORGE FINGERPRINT IMPLEMENTATION VALIDATED / BOTH RETAINED LOCAL SIZES REPRODUCED BY A COHERENT SERIALIZATION FAMILY / 0 PHYSICAL SHA-1 OR FINGERPRINT MATCHES / PHYSICAL TRANSFORMATION STILL UNKNOWN / FAIL-CLOSED`

## Scope

This checkpoint records the result of NON-MERGE audit PR **#622** for the base provider **Deeper and Darker** / `deeperdarker`.

It extends the earlier bounded candidate audit (#604) with:

- a validated CurseForge fingerprint implementation;
- additional JSON serialization forms;
- Info-ZIP replacement strategies with and without `-X`;
- multiple DEFLATE levels;
- explicit comparison against both the physical SHA-1 and physical CurseForge-style fingerprint.

It does not audit or modify the separate **Deeper and Darker: Spellbooks** / `darkermagic` addon.

## Fixed identities

Official Deeper and Darker 1.4.1:

- filename: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- SHA-1: `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`;
- SHA-256: `eee3f51222b0bcc714def002ff089ac9e131d3cae4575b542fd0a7dd101fe0af`;
- size: **3,906,057 bytes**;
- official CurseForge fingerprint: **1323964125**.

Current physical pack authority:

- filename: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- mod id: `deeperdarker`;
- runtime: `1.4.1`;
- physical SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`;
- physical CurseForge-style fingerprint: **1917446721**.

Retained generated local artifact sizes:

- first compatibility JAR: **3,906,052 bytes**;
- `v2` compatibility JAR: **3,906,044 bytes**.

## Hypothesis under test

The exact 1.4.1 source registers the conflicting player redirect mixins in `deeperdarker.mixins.json`.

The audit tested the two-stage local-repair hypothesis suggested by retained chronology:

1. stage 1 — remove `PlayerMixin`;
2. stage 2 — remove `PlayerMixin` and `ServerPlayerMixin`.

The test remained deliberately bounded to mixin-config rewriting and archive serialization/repacking. No claim was made that the real local patch changed only those entries.

## Fingerprint implementation validation

Before comparing candidate fingerprints to the physical target, the audit computed the CurseForge-style fingerprint for the official publisher JAR.

Measured:

- computed publisher fingerprint: **1323964125**;
- expected publisher fingerprint: **1323964125**.

Result:

`CURSEFORGE_FINGERPRINT_IMPLEMENTATION_VALIDATED`

This permits the same implementation to be used as a bounded comparison signal for generated candidates.

## Execution evidence

NON-MERGE PR: **#622**

Successful audit:

- workflow run: **37250559305**;
- audit HEAD: `0906cde960603dec3ac5b98338103da44e060a3a`;
- job: `candidate-reproduction` — **SUCCESS**.

The workflow emitted text-only evidence and did not commit or publish third-party JAR bytes.

## Candidate matrix

The successful run measured:

- candidates tested: **80**;
- candidates matching at least one retained local byte size: **14**;
- candidates matching physical SHA-1 or physical fingerprint: **0**.

Disposition:

`NO_PHYSICAL_HASH_OR_FINGERPRINT_MATCH_IN_80-CANDIDATE_MATRIX`

## Coherent two-stage size reproduction

A single serialization/repack family reproduces **both** retained local JAR sizes under the same recipe:

- JSON serialization with indentation plus final newline;
- Info-ZIP archive update with `-X`;
- DEFLATE levels **5, 6, or 7**.

For those levels the resulting bytes are identical within each stage.

### Stage 1 — remove PlayerMixin

Measured candidate:

- size: **3,906,052 bytes**;
- SHA-1: `286581c0a2dcaf0bfd9de457b3bc720723b899f2`;
- CurseForge-style fingerprint: **2334698443**.

This exactly reproduces the retained **size** of the first generated local compatibility JAR.

It does **not** match the physical target:

- physical SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`;
- physical fingerprint: **1917446721**.

### Stage 2 — remove PlayerMixin + ServerPlayerMixin

Measured candidate:

- size: **3,906,044 bytes**;
- SHA-1: `f59297201d7510cd45005451fed9ed7f539b5db5`;
- CurseForge-style fingerprint: **3888303024**.

This exactly reproduces the retained **size** of the generated `v2` compatibility JAR.

It also does **not** match the physical target.

## Additional size matches

The run found **14** candidates whose total byte size equals one of the two retained local JAR sizes.

Examples include alternate JSON/newline and compression-level combinations. Size equality alone is not treated as identity.

The important negative result is independent of those collisions:

- physical SHA-1/fingerprint matches: **0 / 80**.

## Interpretation

The extended audit strengthens two different conclusions.

### What became more plausible

The retained first/v2 byte sizes can both be produced by a coherent two-stage mixin-JSON rewrite family.

This makes the simple chronology structurally plausible:

- stage 1 removes `PlayerMixin`;
- stage 2 additionally removes `ServerPlayerMixin`;
- `ContainerMenuMixin` remains registered.

### What did not close

The candidate bytes do not reproduce the installed physical artifact.

Therefore the audit does **not** prove:

- that either coherent-size candidate is byte-identical to the retained generated local JAR;
- that either retained generated JAR was deployed under the canonical filename;
- that physical SHA-1 `83f7edd0...` came from only those mixin-config removals;
- that archive metadata/serialization was the only additional change;
- that the physical JAR is semantically identical to the public/source artifact.

The retained generated JARs themselves remain non-materializable as raw bytes in the current environment, so their own SHA-1/fingerprint values are still unknown.

## Relationship to the earlier #604 audit

Earlier NON-MERGE PR #604 tested **57** candidates and found:

- **0/57** exact physical SHA-1 matches;
- one first-size-only match;
- no v2-size match.

This #622 audit expands the serialization/repack space to **80** candidates and additionally validates the fingerprint implementation.

It reproduces both retained sizes under one coherent family but still finds:

- **0** physical SHA-1 matches;
- **0** physical fingerprint matches.

The newer result supersedes #604 only for the expanded candidate-space conclusion. It does not invalidate the earlier negative result.

## Catalog consequence

No semantic promotion follows.

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

- authorized raw-byte inspection of the physical canonical JAR;
- raw-byte hash/fingerprint of either retained generated compatibility JAR followed by exact comparison;
- or another exact artifact proven identical to physical SHA-1 `83f7edd0a8516b2767c2cda7a3b2402f9e290d88` / fingerprint **1917446721**.

Until then, Black Arcana remains fail-closed and must not project the public/source three-root denominator into the strict exact-current numerator.
