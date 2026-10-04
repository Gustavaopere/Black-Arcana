# Deeper and Darker 1.4.1 — local NeoVitae compatibility lineage

Status: `LOCAL COMPATIBILITY WORK BOUNDED / GENERATED ARTIFACTS RETAINED / RUNTIME TRANSITION OBSERVED / NO HASH BRIDGE TO 83F7EDD0... / FAIL-CLOSED`

## Purpose

This checkpoint narrows the local post-install modification history behind the physical Deeper and Darker artifact without asserting byte identity that the retained evidence cannot prove.

It applies only to the base provider **Deeper and Darker** / `deeperdarker`. The separate **Deeper and Darker: Spellbooks** / `darkermagic` addon is out of scope.

## Fixed physical boundary

Current physical authority remains:

- JAR: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- mod id: `deeperdarker`;
- runtime: `1.4.1`;
- physical SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`.

The official CurseForge/GitHub/Modrinth 1.4.1 artifact remains:

- SHA-1: `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`;
- size: **3,906,057 bytes**.

The two are not byte-identical.

## Pre-patch installation state

Retained CurseForge instance metadata captured on 2026-08-18 records the canonical Deeper and Darker slot as:

- project/file: `659011 / 8201775`;
- filename: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- SHA-1 recorded by CurseForge: `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`;
- file length: **3,906,057 bytes**;
- `isModified=false`;
- `isWorkingCopy=false`;
- `isFuzzyMatch=false`.

A non-generated Project Library copy of that canonical filename is retained at **3,906,057 bytes**.

## Local compatibility artifacts retained

Project Library metadata records the following generated artifacts on 2026-08-18:

### First compatibility set

- `DeeperDarker_NeoVitae_compat_patch.zip`
  - created: **2026-08-18 11:53:07Z**;
  - size: **15,374,810 bytes**;
- `deeperdarker-neoforge-1.21.1-1.4.1-neovitae-compat.jar`
  - created: **2026-08-18 11:53:10Z**;
  - size: **3,906,052 bytes**;
- paired generated NeoVitae artifact:
  - `neovitae-1.21.1-1.1.10-deeperdarker-compat.jar`;
  - size: **13,143,869 bytes**.

### Second compatibility set

- `DeeperDarker_NeoVitae_compat_patch_v2.zip`
  - created: **2026-08-18 12:43:01Z**;
  - size: **15,374,798 bytes**;
- `deeperdarker-neoforge-1.21.1-1.4.1-neovitae-compat-v2.jar`
  - created: **2026-08-18 12:43:04Z**;
  - size: **3,906,044 bytes**;
- paired generated NeoVitae artifact:
  - `neovitae-1.21.1-1.1.10-deeperdarker-compat-v2.jar`;
  - size: **13,143,867 bytes**.

These metadata records prove that two distinct local compatibility rebuilds existed. They do **not** prove that either generated Deeper and Darker JAR was copied into the canonical mod slot.

## Runtime chronology

### Conflict still present after the first generated set

Retained `debug(20260818-123756).log` records a bootstrap failure with:

- Deeper and Darker `ServerPlayerMixin` redirecting `AbstractContainerMenu.stillValid(...)`;
- NeoVitae `ServerPlayerMixin` already redirecting the same call at the same priority;
- Mixin reporting an `@Redirect conflict` and skipping the Deeper and Darker redirect.

The corresponding stdout log records the same conflict immediately before the bootstrap crash.

This log was retained after the first compatibility artifact set had been generated. It therefore proves that the local compatibility work was **not yet operationally closed at that checkpoint**.

It does not identify which JAR bytes were loaded in that boot.

### ContainerMenuMixin observed after the v2 generation

Retained `debug(20260818-125153).log`, captured after the v2 artifact set was generated, positively records:

- `deeperdarker.mixins.json:ContainerMenuMixin` mixing into vanilla container menus;
- its `@Inject::stillValid(Player, CallbackInfoReturnable)` handler being applied.

Later retained logs on 2026-08-18/19 and 2026-09-08 also positively record the same Deeper and Darker `ContainerMenuMixin` `stillValid(...)` injection surface.

This establishes a real runtime transition in the local compatibility-work history.

It does **not** prove:

- that `deeperdarker-neoforge-1.21.1-1.4.1-neovitae-compat-v2.jar` was the artifact loaded by that boot;
- that the generated v2 JAR was renamed to the canonical filename;
- that the physical SHA-1 `83f7edd0...` equals either generated compatibility JAR;
- that the mixin change is the only archive-level delta in the physical artifact.

## Raw-byte limitation

The retained generated JARs are visible through Project Library metadata, but this audit does not have an authorized raw-byte materialization path for them. Their SHA-1/SHA-256 values could therefore not be computed here.

The only authoritative physical hash remains `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`.

## Provenance consequence

The evidence now supports a more specific bounded history:

1. official File `8201775` was the original unmodified installation;
2. a Deeper and Darker ↔ NeoVitae `stillValid(...)` mixin conflict was reproduced;
3. two local compatibility artifact sets were generated;
4. the first set did not correspond to an operationally closed state in the next retained bootstrap checkpoint;
5. after the v2 generation, retained runtime logs positively show the `ContainerMenuMixin` injection surface that remains visible in later boots;
6. a later physical inventory fingerprints the canonical Deeper and Darker JAR as `83f7edd0...`.

The missing step is still a **cryptographic or exact-content bridge** from one retained generated artifact to the deployed `83f7edd0...` bytes.

## Catalog consequence

No semantic promotion follows from this checkpoint.

- public/source supernatural baseline: **3 roots**;
- exact-current physical roots: **UNKNOWN**;
- strict contribution: **+0**;
- provider state: **⚠️ partial / conditioned**.

The three public/source actions remain:

1. Otherside Portal Activation;
2. Sonorous Staff Sonic Boom;
3. Soul Elytra Boost.

Promotion to `✅ Catalogado` still requires direct raw-byte inspection of the physical JAR or an exact artifact whose hash/content can be proven identical to `83f7edd0...`.
