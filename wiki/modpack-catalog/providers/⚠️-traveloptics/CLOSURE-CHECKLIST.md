# T.O Magic n' Extras 4.4.0.1-1.21.1 — Closure Checklist

Status: `33 REGISTERED SPELL IDS CATALOGED / STRICT PROMOTION BLOCKED / RUNTIME FAIL-CLOSED`

## Purpose

The current Traveloptics dossier already closes the exact publisher-release registry inventory at **33 registered spell identities** and excludes **32 residual localization-only spell IDs**. The remaining work is not another spell enumeration. It is a finite set of evidence gates required before strict semantic/runtime promotion can be considered.

This checklist does not promote the provider, does not treat a third-party patch as upstream authority, and does not infer survival acquisition or assembled-pack runtime from publisher marketing language.

## Gate 1 — Physical artifact identity / patch deployment

Current physical evidence establishes the installed version line and filename:

- observed installed filename: `traveloptics-4.4.0.1-1.21.1.jar`;
- physical version line: `4.4.0.1-1.21.1`;
- exact publisher file: CurseForge project/file `1046916 / 6342780`;
- exact publisher-release SHA-1: `3808493ce45cdfeb6408e85578adecf13df698e8`;
- exact publisher-release SHA-256: `0372b4b8593288726fb0d6e8cdb86202a87677d0c2dafeb96cab50bf057ec298`.

The repository does **not** preserve an independent current physical SHA-1 for the installed JAR, so byte equality with File `6342780` remains unproven.

A third-party compatibility project published after the original audit now exposes a patched 1.21.1 artifact (CurseForge project/file `1690333 / 8861368`, filename `traveloptics-4.4.0.1.1-1.21.1-patched.jar`) and states that it changes the `universal_loot` codec wiring. This is a **non-authoritative external candidate only**. Current sibling repository search does not show that patched filename, but absence from indexed repository text is not proof of absence from the physical modpack.

Required authoritative result:

| Question | Required evidence | Current state |
|---|---|---|
| Is the physical JAR byte-identical to original File `6342780`? | SHA-1/SHA-256 from the actual installed JAR | `NÃO VERIFICADO` |
| Is a patched/replacement JAR physically installed instead? | exact installed filename + hash + provenance | `NÃO VERIFICADO` |
| If another replacement exists, what is it? | exact file identity/hash/provider source | `NÃO VERIFICADO` |

Record exactly one physical disposition: `ORIGINAL_EXACT`, `PATCHED_EXACT`, or `OTHER_VERIFIED`. Do not infer from nominal version strings.

## Gate 2 — Loot-modifier registry initialization

Exact clean-room structure of publisher File `6342780` established:

- `key_loot` registry name present;
- `universal_loot` registry name present;
- `KeyLootModifier.CODEC` referenced twice by the setup;
- `UniversalLootModifier.CODEC` referenced zero times by the setup.

That mismatch remains a structural risk until the **actual physical pack** proves one of these branches:

### Branch A — original artifact is installed

Required:

- assembled-pack dedicated-server or equivalent authoritative NeoForge runtime reaches and completes the relevant registry initialization with the actual installed JAR;
- evidence must identify the pack/JAR hash used;
- absence of a crash must be tied to that startup, not inferred from a standalone build or unrelated server smoke without Traveloptics.

### Branch B — verified patched/replacement artifact is installed

Required:

- exact patched/replacement physical filename and hash;
- provenance sufficient to identify what changed;
- authoritative assembled-pack startup completing registry initialization with that exact artifact.

A third-party project description that says the patch fixes startup is useful external evidence, but it does not prove the user's pack deploys that artifact or that the assembled modpack boots with it.

Current state: `RUNTIME INITIALIZATION UNVERIFIED / FAIL-CLOSED`.

## Gate 3 — `traveloptics:blackout` survival reachability

`traveloptics:blackout` is an exact registered spell identity in the audited publisher artifact and inherits `AbstractUniqueSpell.allowCrafting() = false`.

Unlike the other nine non-craftable Unique spells, the exact artifact audit found:

- no direct structured loot reference for `blackout`;
- no provider-owned reference to `TOSpells.BLACKOUT_SPELL` outside `TOSpells` itself.

The publisher's generic 1.21.1 statement that ported spells are obtainable in survival is not object-level evidence for this spell.

Required closure evidence must establish an actual current-pack player path, such as an authoritative provider/host loot route, progression grant, item/scroll source, scripted acquisition or runtime-observed survival mechanism that resolves specifically to `traveloptics:blackout`.

| Required field | Current state |
|---|---|
| exact acquisition mechanism | `NÃO VERIFICADO` |
| authoritative source/runtime evidence | `NÃO VERIFICADO` |
| prerequisite entity/structure/item/config | `NÃO VERIFICADO` |
| actual pack/world checkpoint | `NÃO VERIFICADO` |

Creative access, commands, registry presence, translation keys or generic publisher language do not close this gate.

## Gate 4 — Somake Aqua ↔ T.O Aqua coexistence

The physical pack contains both:

- Somake Spells 1.0.8-fix;
- T.O Magic n' Extras `4.4.0.1-1.21.1`.

Somake historical publisher text described Aqua as covering T.O's absence on 1.21.1 and discussed future migration if T.O returned. The installed T.O 1.21.1 line is a deprecated partial alpha. Those facts do **not** establish current authority migration or safe deduplication.

Required evidence before any Black Arcana integration chooses an Aqua authority:

- authoritative runtime/provider observation of both addons loaded together;
- exact school/registry identities that coexist or conflict;
- whether either provider suppresses, aliases, replaces or delegates Aqua content under this stack;
- no double registration/duplicate settlement assumptions;
- no Black Arcana-created fallback school/resource pipeline.

Current state: `COEXISTENCE / AUTHORITY UNVERIFIED`.

This gate is primarily an integration/authority blocker. It does not erase the 33 Traveloptics spell identities already structurally cataloged.

## Already closed — do not redo

The following work is already canonical and should not be repeated:

- 33 exact publisher-release registered spell identities enumerated;
- spell cards materialized under verified school membership;
- 32 residual localization-only IDs excluded;
- 10 `AbstractUniqueSpell` registrations identified;
- 2 `AbstractWeaponSpell` craftable registrations identified (`cursed_blast`, `gyro_slash`);
- nine non-craftable Unique spell structured loot routes identified;
- `blackout` isolated as the unresolved Unique reachability exception;
- structural `TOLootModifiers` codec mismatch recorded clean-room.

## Acceptance boundary

Traveloptics remains `⚠️ Parcial / condicionado` until the relevant evidence above is closed.

No future checkpoint may claim strict semantic promotion or runtime compatibility merely because:

- the 33 registry IDs are known;
- a third-party patch exists on the internet;
- the publisher says spells are generally survival-obtainable;
- a build without the actual provider stack is green;
- the version string matches the publisher release.

Any promotion must cite the exact physical artifact/runtime evidence and preserve Iron's/Traveloptics provider authority. Black Arcana must not silently repair the provider registry, invent a `blackout` acquisition route, or select an Aqua authority by assumption.
