# Deeper and Darker 1.4.1 — physical hash row-boundary correction

Status: `PHYSICAL HASH ATTRIBUTION CORRECTED / LAST DIRECT ROW-BOUND SHA-1 783123AE... / 83F7EDD... REASSIGNED TO DELIGHTFUL BACKPORT / LOCAL PATCH LINEAGE PLAUSIBLE BUT UNPROVEN / FAIL-CLOSED`

## Purpose

This checkpoint corrects a row-boundary attribution error in the Deeper and Darker catalog.

The current sibling dossier still lists SHA-1 `83f7edd0a8516b2767c2cda7a3b2402f9e290d88` for physical row #215. Direct Project Library physical inventories show that value belongs to the following mod, **Delightful Backport**, not to Deeper and Darker.

The correction changes physical provenance only. It does not promote the provider, does not infer semantic equality, and does not claim that any retained local compatibility artifact is the deployed JAR.

## Correct physical row association

Multiple retained physical modlists captured between **2026-09-07** and **2026-09-16** independently preserve the same Deeper and Darker association:

- SHA-1: `783123ae86c91c01527c10f338679caaef42eb42`;
- fingerprint column: `1828555691`;
- filename: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- mod id: `deeperdarker`;
- runtime: `1.4.1`.

The adjacent physical row is independently preserved as:

- SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`;
- fingerprint column: `1917446721`;
- filename: `Delightful-Backport-1.0-1.21.1-neoforge.jar`;
- mod id: `delightfulbackport`;
- runtime: `1.0`.

Therefore `83f7edd0...` must not be used as Deeper and Darker evidence.

## Current sibling boundary

Current sibling authority at `neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a` still confirms row #215, filename, mod id and runtime for Deeper and Darker. Its certified dossier blob `9fd80b33b22af89c0bd141625c82eec6001476da` still embeds the misattributed `83f7edd0...` SHA.

Black Arcana therefore treats:

- sibling row/filename/version presence as current physical-presence authority;
- the retained direct physical modlists as the hash-row authority;
- the sibling dossier SHA field as **superseded for this provider until that upstream dossier is corrected**.

No newer correctly row-bound raw hash capture was found in the available evidence. Accordingly, `783123ae...` is the **latest directly supported Deeper and Darker SHA-1 in retained physical inventories**, not a claim that no same-name replacement could have occurred after the last captured dump.

## Publisher comparison

Official Deeper and Darker 1.4.1 distribution paths remain byte-identical at:

- SHA-1 `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`;
- SHA-256 `eee3f51222b0bcc714def002ff089ac9e131d3cae4575b542fd0a7dd101fe0af`;
- size `3,906,057` bytes.

The corrected retained physical SHA-1 `783123ae...` still differs from the official publisher SHA-1. The physical disposition therefore remains `OTHER_VERIFIED` at the last direct hash checkpoint.

## Local compatibility artifacts retained in Project Library

Project Library also retains a bounded local compatibility-work sequence from **2026-08-18**:

- original non-generated `deeperdarker-neoforge-1.21.1-1.4.1.jar` — **3,906,057 bytes**;
- generated `deeperdarker-neoforge-1.21.1-1.4.1-neovitae-compat.jar` — **3,906,052 bytes**;
- generated `deeperdarker-neoforge-1.21.1-1.4.1-neovitae-compat-v2.jar` — **3,906,044 bytes**;
- paired generated patch bundles and NeoVitae compatibility JARs are also retained.

The retained CurseForge instance snapshot from earlier on 2026-08-18 records project/file `659011 / 8201775`, publisher SHA-1 `b6094add...`, and `isModified=false`.

Local logs from the compatibility-work window document Deeper and Darker / NeoVitae `stillValid(...)` mixin interaction, including a `ServerPlayerMixin` redirect conflict and runs exposing Deeper and Darker `ContainerMenuMixin` injections.

This is strong provenance context for a local compatibility modification. It does **not** prove that either retained generated compatibility JAR has SHA-1 `783123ae...`.

## Raw-byte limitation

The retained JAR records are visible in Project Library metadata, but raw-byte materialization is not authorized in the current environment. A direct hash comparison of the generated compatibility JARs therefore has **not** been performed.

Do not infer any of the following:

- `783123ae...` == first generated compatibility JAR;
- `783123ae...` == v2 generated compatibility JAR;
- the compatibility patch is the only entry-level physical delta;
- the three public/source supernatural roots are byte-identical in the deployed artifact.

## Catalog consequence

The prior conclusion “physical bytes differ from the official publisher artifact” remains valid after correcting the SHA, but all references to `83f7edd0...` as Deeper and Darker evidence are invalid.

Current disposition remains:

- public/source supernatural baseline: **3 roots**;
- exact-current physical root denominator: **UNKNOWN**;
- strict semantic contribution: **+0**;
- provider state: **⚠️ partial/conditioned**.

Closure still requires direct inspection of the physical bytes corresponding to `783123ae...`, or an exact artifact/provenance bridge that establishes its entry-level delta and semantic equivalence.
