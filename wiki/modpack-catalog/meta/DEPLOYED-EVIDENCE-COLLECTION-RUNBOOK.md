# Black Arcana — Deployed Provider Evidence Collection Runbook

Checkpoint: 2026-09-17

Status: `FIVE CONDITIONAL PROVIDERS / REGISTRY WORK NOT TO BE REDONE / ACTUAL PACK EVIDENCE REQUIRED`

## Purpose

The remaining conditional catalog blockers are no longer broad discovery tasks. They are bounded deployed-state questions that require evidence from the **actual modpack instance/world/server**.

This runbook defines the smallest acceptable evidence package for:

- Asterism Arcanum `1.21.1-0.1.0`;
- Gaze `1.1.7.1`;
- Not Enough Glyphs `4.6.1`;
- Somake Spells `1.0.9`;
- T.O Magic n' Extras / Traveloptics `4.4.0.1-1.21.1`.

Do not regenerate provider registries already closed by the provider-specific dossiers. Do not substitute source defaults, fresh-generated configs, creative/command access or a different Minecraft instance for deployed evidence.

## Evidence provenance header

Every collection must record:

- collection timestamp;
- Minecraft instance/server identifier sufficient to distinguish it from a fresh test instance;
- world/serverconfig source when a world-specific config is involved;
- filenames of the five provider JARs actually present;
- SHA-1 and SHA-256 of every provider JAR used for a closure decision;
- whether the evidence comes from client instance, dedicated server, integrated server/world, or authoritative exported config set;
- any datapack/KubeJS/script layer that can alter acquisition/config behavior.

Absolute personal filesystem prefixes do not need to be committed. Preserve enough relative path information to prove which deployed file was read.

## Hash checkpoints already known

These hashes are comparison targets, not assumptions about the deployed bytes.

| Provider/artifact | Known exact SHA-1 | Meaning |
|---|---|---|
| Gaze 1.1.7.1 physical/exact artifact | `a8cb3190bde157f78160ce65c202ce2d47fb2041` | exact installed-artifact identity previously closed |
| Not Enough Glyphs 4.6.1 physical JAR | `e5fd04b7c40d6d5a9aea5d6356f3eb628941fca4` | physical JAR fingerprint already cataloged |
| Somake 1.0.9 publisher release File 8867079 | `171841ac9f802be9309ecc166c1d972ac6d404c0` | release artifact; deployed equality still open |
| Traveloptics original File 6342780 | `3808493ce45cdfeb6408e85578adecf13df698e8` | exact original publisher artifact |
| Traveloptics patch File 8861368 | `680fa679d8ea2419a79571f455436367222f6f9d` | exact one-class patch candidate |

Asterism must still have its deployed JAR hash captured with the same evidence package.

## Provider 1 — Asterism Arcanum

Canonical blocker: effective survival reachability of `asterismarcanum:astral_gateway`.

Collect either or both:

1. deployed Asterism/Iron's config or datapack evidence that deterministically includes/excludes `asterismarcanum:astral_gateway` from enabled/craftable/loot selection;
2. deterministic provider-native runtime observation on the assembled pack.

Required runtime notes when used:

- acquisition mechanism exercised;
- Astromancer/random Astral-scroll path if relevant;
- whether commands/creative were excluded;
- deployed config/datapack checkpoint used;
- enough repetitions or deterministic state to avoid treating a small negative random sample as exclusion proof.

Do not promote Astral Gateway from publisher intent alone. Its 0.1.0 source/static host defaults remain in tension with the creative-only/unfinished release wording.

Canonical checklist: `providers/⚠️-asterism-arcanum/SURVIVAL-CLOSURE-CHECKLIST.md`.

## Provider 2 — Gaze

Canonical blocker: effective deployed COMMON boolean `disableGazeRites`.

Preferred evidence:

- the actual deployed Gaze COMMON config containing `disableGazeRites`, including relative path, file hash and resolved value.

Alternative evidence:

- authoritative assembled-pack/provider observation proving whether the Gaze Rite registry initializes under the deployed configuration.

Acceptance:

- `disableGazeRites=false` may release all 26 exact Rite identities from the common config gate, subject only to any newly discovered deployed gate;
- `disableGazeRites=true` keeps those 26 out of the active current-pack semantic count.

Do not infer `false` from the provider default.

Canonical checklist: `providers/⚠️-gaze/DEPLOYED-CONFIG-CHECKLIST.md`.

## Provider 3 — Not Enough Glyphs

Canonical blocker: effective NeoForge/Ars SERVER `[general].enabled` for the 39 source-enabled candidate glyphs.

Primary authoritative location is the actual world/server configuration, including `<world>/serverconfig` overrides.

For every candidate row in the canonical checklist, retain:

- registry identity;
- relative config path;
- file present/absent;
- SHA-256 of the deployed file when present;
- resolved `[general].enabled` value;
- provenance of the world/serverconfig set.

If a config file is absent, do not call the glyph enabled solely because the source default is `true`. The effective fallback must be demonstrated from the deployed environment/runtime.

`not_enough_glyphs:momentum` remains source-disabled regardless of an observed enabled config value and is not one of the 39 candidates.

Canonical checklist: `providers/⚠️-not-enough-glyphs/DEPLOYED-CONFIG-CHECKLIST.md`.

## Provider 4 — Somake Spells 1.0.9

Current physical filename authority: `somakespells-1.0.9-1.21.1.jar`.

First collect the installed JAR hash:

- if SHA-1 = `171841ac9f802be9309ecc166c1d972ac6d404c0`, publisher-release byte equality is closed;
- any other SHA-1 must be recorded as a different deployed artifact and must not inherit the exact release audit.

Then collect deployed reachability gates:

- any actual Somake config entry corresponding to `enableSpellLockSystem` if the key still exists in 1.0.9;
- effective Iron's spell `enabled` / `allow_crafting` overrides affecting Somake IDs;
- school-focus/acquisition state sufficient to prove player reachability;
- provider-specific progression prerequisites that actually gate use.

The historical 1.0.8-fix 67-ID audit must not be used as a current 1.0.9 registry.

Canonical checklist: `providers/⚠️-somake-spells/CURRENT-1.0.9-REVALIDATION-CHECKLIST.md`.

## Provider 5 — Traveloptics

Current sibling dossier still records physical filename `traveloptics-4.4.0.1-1.21.1.jar`.

### Gate 1 — classify deployed bytes

Hash the actual installed JAR and record exactly one result:

- `ORIGINAL_EXACT` if SHA-1 = `3808493ce45cdfeb6408e85578adecf13df698e8`;
- `PATCHED_EXACT` if SHA-1 = `680fa679d8ea2419a79571f455436367222f6f9d`;
- `OTHER_VERIFIED` for any other reproducibly captured hash.

Filename alone is insufficient because the patch retains the same internal mod/version metadata and could be renamed.

### Gate 2 — registry initialization

With the exact deployed hash recorded, retain authoritative assembled-pack startup evidence showing whether the relevant loot-modifier registry initialization completes.

A Black Arcana standalone CI/server smoke without the physical Traveloptics stack is not evidence for this gate.

### Gate 3 — Blackout

Retain an object-specific current-1.21.1 acquisition route for `traveloptics:blackout`.

General project-page language and creative/command access are insufficient. If the route depends on a boss/entity/item, prove that prerequisite exists in this exact 1.21.1 alpha/runtime.

### Gate 4 — Aqua coexistence

Retain assembled-pack evidence for Somake + Traveloptics loaded together:

- actual school/registry identities visible in the deployed stack;
- any suppression/alias/delegation;
- acquisition/focus behavior;
- duplicate/conflicting authority if observed.

Known exact alpha fact: Traveloptics 4.4.0.1 has zero Aqua spells among its 33 registered spells, but retains Aqua residual/support surfaces such as `AQUA_SCROLL_DUMMY` and `data/traveloptics/tags/item/aqua_focus.json`. This does not by itself close coexistence.

Canonical checklist: `providers/⚠️-traveloptics/CLOSURE-CHECKLIST.md`.

## Minimal evidence package

A sufficient handoff bundle should contain only what is needed for catalog closure:

```text
provider-evidence/
  provenance.txt
  jar-hashes.txt
  gaze-config-evidence.txt
  neg-serverconfig-evidence.txt
  somake-config-host-evidence.txt
  asterism-gateway-evidence.txt
  traveloptics-runtime-evidence.txt
```

Where practical, each evidence text should include:

- relative source path;
- SHA-256 of the source file;
- only the relevant config key/value or bounded log lines;
- command/runtime action used to produce the observation;
- PASS/FAIL/UNRESOLVED disposition without interpretation beyond the observed fact.

Do not include unrelated credentials, account data, personal paths, complete proprietary JAR contents, full protected localization/asset payloads, or private server secrets.

## Hash commands

### Bash / Linux

```bash
sha1sum mods/<provider>.jar
sha256sum mods/<provider>.jar
```

### PowerShell / Windows

```powershell
Get-FileHash -Algorithm SHA1 .\mods\<provider>.jar
Get-FileHash -Algorithm SHA256 .\mods\<provider>.jar
```

## Closure discipline

After evidence is collected:

1. verify the provider/version against the latest sibling modlist;
2. compare hashes against exact known artifacts where available;
3. update only the affected checklist rows;
4. change strict semantic count only for objects whose current active/reachable state is proven under the global counting rule;
5. change provider folder/status only when the provider's declared catalog scope is fully closed;
6. keep runtime/API compatibility QA separate from catalog closure where the checklist permits;
7. rerun canonical Black Arcana CI after synchronization with latest `main`.

This runbook is an evidence-collection contract. It does not promote any provider by itself.
