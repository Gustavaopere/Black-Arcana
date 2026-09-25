# T.O Magic n' Extras 4.4.0.1-1.21.1 — Closure Checklist

Status: `33 REGISTERED SPELL IDS CATALOGED / STRICT PROMOTION BLOCKED / RUNTIME FAIL-CLOSED`

## Purpose

The current Traveloptics dossier already closes the exact publisher-release registry inventory at **33 registered spell identities** and excludes **32 residual localization-only spell IDs**. The remaining work is not another spell enumeration. It is a finite set of evidence gates required before strict semantic/runtime promotion can be considered.

This checklist does not promote the provider, does not treat a third-party patch as upstream authority, and does not infer survival acquisition or assembled-pack runtime from publisher marketing language.

## Gate 1 — Physical artifact identity / patch deployment

Current physical evidence establishes the installed version line and filename:

- observed installed filename: `traveloptics-4.4.0.1-1.21.1.jar`;
- latest sibling dossier rechecked at `neoforge-rpg-skilltree@4d9710dc0c9bf17e1fdaef29e48d843de80288d0`: `PROJECT-INSTRUCTIONS/modlist/to-magic-n-extras.md` still marks that filename/version as physically installed; the dossier carries no physical cryptographic hash;
- physical version line: `4.4.0.1-1.21.1`;
- exact publisher file: CurseForge project/file `1046916 / 6342780`;
- exact publisher-release SHA-1: `3808493ce45cdfeb6408e85578adecf13df698e8`;
- exact publisher-release SHA-256: `0372b4b8593288726fb0d6e8cdb86202a87677d0c2dafeb96cab50bf057ec298`.

Project Library physical modlist checkpoint `modlist(1).txt` dated 2026-09-16 preserves SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4` for `traveloptics-4.4.0.1-1.21.1.jar`. It is neither the original publisher SHA-1 nor the known patch SHA-1. Gate 1 therefore advances from unknown hash to a verified third-artifact disposition.

A third-party compatibility project published after the original audit exposes patched file `1690333 / 8861368`, filename `traveloptics-4.4.0.1.1-1.21.1-patched.jar`. Exact clean-room binary-diff evidence now fingerprints that candidate at SHA-1 `680fa679d8ea2419a79571f455436367222f6f9d` / SHA-256 `05f588202900c691fb70389435c9997d090f81a699f7df7cdebcbec552298cc2`. Compared with original File `6342780`, both JARs contain 1339 entries, with zero additions/removals and exactly one changed entry: `com/gametechbc/traveloptics/loot/TOLootModifiers.class`; zero non-class resources differ. The patch publisher attributes that one-class delta to correcting the `universal_loot` codec wiring. This establishes an exact comparison target, **not** deployment. Current sibling evidence still does not prove which byte sequence is physically installed. See [`PATCH-8861368-BINARY-DIFF.md`](PATCH-8861368-BINARY-DIFF.md).

Required authoritative result:

| Question | Required evidence | Current state |
|---|---|---|
| Is the physical JAR byte-identical to original File `6342780`? | compare physical SHA-1 with `3808493ce45cdfeb6408e85578adecf13df698e8` | `NÃO` — physical is `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4` |
| Is the known patch File `8861368` physically installed? | compare physical SHA-1 with `680fa679d8ea2419a79571f455436367222f6f9d` | `NÃO` |
| If another replacement exists, what is it? | exact physical hash + provenance/content audit | `PARCIAL` — `OTHER_VERIFIED` hash known; provenance/content delta not yet materialized |

Physical disposition is now **`OTHER_VERIFIED`**. Do not infer its implementation from the unchanged nominal filename/version. The next gate is to materialize/audit the exact `7b74816e...` bytes or obtain equivalent authoritative provenance.

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

The exact patch candidate is now cryptographically fingerprinted and independently proven to differ from the original in only `TOLootModifiers.class`. The patch publisher states that this class delta corrects the universal codec registration. That still does not prove the user's pack deploys SHA-1 `680fa679d8ea2419a79571f455436367222f6f9d`, nor that the assembled modpack completes registry initialization with the actual deployed artifact.

Current state: `RUNTIME INITIALIZATION UNVERIFIED / FAIL-CLOSED`.

### Bounded runtime observation now available

The isolated `black_arcana_catalog_qa` companion can observe the public NeoForge `GLOBAL_LOOT_MODIFIER_SERIALIZERS` registry on `ServerStartedEvent` without loading or reflecting Traveloptics implementation classes.

For the exact assembled pack it emits only the bounded targets:

- `traveloptics:key_loot`;
- `traveloptics:universal_loot`;
- whether both resolved values are distinct object instances.

Canonical runbook: [`docs/qa/provider-catalog-runtime-registry-probe.md`](../../../../docs/qa/provider-catalog-runtime-registry-probe.md).

This does not create a PASS by itself. Gate 2 evidence must still pair the runtime rows with the deployed artifact hash/disposition from Gate 1.

For an exact patched/replacement artifact, a strong closure packet for this gate is:

1. physical hash classified as `PATCHED_EXACT` or another explicitly verified replacement;
2. assembled dedicated server reaches `ServerStartedEvent` with that exact artifact;
3. both serializer IDs emit `status=OBSERVED`;
4. the pair emits `status=OBSERVED distinct_codec_instances=true`.

For `ORIGINAL_EXACT`, successful startup and observed serializer rows are evidence to retain, but any result that conflicts with the already-audited duplicate-codec structure must be investigated rather than silently reclassified as fixed. The probe does not identify codec classes and does not prove loot-modifier behavior or Blackout acquisition.

## Gate 3 — `traveloptics:blackout` survival reachability

`traveloptics:blackout` is an exact registered spell identity in the audited publisher artifact and inherits `AbstractUniqueSpell.allowCrafting() = false`.

Unlike the other nine non-craftable Unique spells, the exact artifact audit found:

- no direct structured loot reference for `blackout`;
- no provider-owned reference to `TOSpells.BLACKOUT_SPELL` outside `TOSpells` itself.

The publisher's generic 1.21.1 statement that ported spells are obtainable in survival is not object-level evidence for this spell.

The current broad project page documents a Dead King → Blackout acquisition loop, and official 1.20.1 File `6010839` introduced `Blackout`, `Call Forth The Dead King` and the `Enraged Dead King` together. That is real publisher evidence for the full project/1.20.1 feature line, but not for the installed deprecated 1.21.1 alpha.

Exact File `6342780` evidence instead shows:

- `call_forth_the_dead_king` is residual localization-only content and absent from the exact 33-spell registry;
- the exact artifact's 41 loot/loot-modifier JSON resources expose no Enraged Dead King loot route;
- `blackout` remains registered, but no object-level structured acquisition route is present in the audited artifact.

See [`BLACKOUT-VERSIONED-ACQUISITION-BOUNDARY.md`](BLACKOUT-VERSIONED-ACQUISITION-BOUNDARY.md).

Therefore the broader Dead King route must not be projected into the installed alpha. This does not prove impossibility; it preserves the requirement for File-6342780-specific or actual-pack evidence.

Required closure evidence must establish an actual current-pack player path, such as an authoritative 1.21.1 provider/host route, progression grant, item/scroll source, scripted acquisition or runtime-observed survival mechanism that resolves specifically to `traveloptics:blackout`.

| Required field | Current state |
|---|---|
| exact acquisition mechanism | `NÃO VERIFICADO` |
| authoritative source/runtime evidence | `NÃO VERIFICADO` |
| prerequisite entity/structure/item/config | `NÃO VERIFICADO` |
| actual pack/world checkpoint | `NÃO VERIFICADO` |

Creative access, commands, registry presence, translation keys, generic publisher language, or the 1.20.1 Dead King acquisition loop do not close this 1.21.1 gate.

## Gate 4 — Somake Aqua ↔ T.O Aqua coexistence

The physical pack contains both:

- Somake Spells `1.0.9`;
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
