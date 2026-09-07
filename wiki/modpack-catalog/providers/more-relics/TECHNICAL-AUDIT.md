# More Relics 1.7.7 — technical/provenance/compatibility audit

## Scope

This audit is deliberately artifact/public-documentation based. It does not decompile the installed More Relics JAR and does not treat unsupported-version behavior as known merely because both JARs are present.

## 1. Exact installed identities

Current physical modlist:

### More Relics

- `morerelics-1.7.7-1.21.1.jar`;
- mod id `morerelics`;
- runtime name `More Relics`;
- runtime version `1.7.7`;
- SHA-1 `ba0c920bc7712d1ff85012327b26e1a808c648f6`;
- package/Curse fingerprint `1163810056`.

### Relics

- `relics-1.21.1-0.12.8.jar`;
- mod id `relics`;
- runtime `0.12.8`;
- SHA-1 `1fe7d57ebfa56ebd0aeecfed01075f8b55b94ef7`;
- package/Curse fingerprint `2050122937`.

### Curios

- `curios-neoforge-9.5.1+1.21.1.jar`;
- mod id `curios`;
- runtime `9.5.1+1.21.1`.

## 2. Exact More Relics release

Publisher evidence for installed release:

- project ID `1269280`;
- exact CurseForge file ID `8685815`;
- `morerelics-1.7.7-1.21.1.jar`;
- Minecraft 1.21.1;
- NeoForge;
- uploaded `2026-08-19`;
- Release channel;
- Client & Server;
- project license **All Rights Reserved**.

Modrinth independently lists More Relics 1.7.7 for Minecraft 1.21.1/NeoForge, Client & Server, ARR.

No official public exact-source repository was located during this checkpoint.

## 3. Required provider stack

Current publisher relations/documentation establish dependencies on:

- Relics;
- Curios API;
- ShatterLib / OctoLib;
- Architectury API.

This is an addon/provider stack, not an independent relic engine.

The physical modlist must remain authority for exact installed dependency versions; public dependency pages frequently use broad/“any compatible” relation metadata and therefore are not sufficient to prove exact binary compatibility.

## 4. Hard support mismatch: Relics 0.12.8

The More Relics publisher states, specifically for NeoForge:

- Relics 0.11 and 0.12 are beta releases;
- they are not yet supported;
- Minecraft 1.21.1 users should use Relics `0.10.7.8` instead;
- the warning will be removed when those versions are supported.

Exact More Relics 1.7.7 additionally says the **next** update may be a mini beta for Relics `0.12.8` due to demand, may not include all content and would only receive bug fixes.

This establishes that More Relics 1.7.7 itself is **not the promised 0.12.8-support build**.

## 5. Host Relics status

Exact installed Relics `0.12.8` is published as:

- Minecraft 1.21.1;
- NeoForge;
- Client & Server;
- **Beta**;
- uploaded `2026-05-28`.

Its publisher changelog includes major data/cache/progression-facing changes such as relic experience statistics and data-cache optimization, reinforcing why addon compatibility cannot be assumed across the 0.10→0.12 host transition.

Black Arcana does not infer which internal breaking change affects More Relics. The upstream support warning is sufficient to classify the pair as unsupported.

## 6. Curatorial decision versus engineering status

The current modpack guide records **More Relics 1.7.7 = Manter / risco aceito**.

That remains the curatorial decision.

Engineering state is separately:

`INSTALLED + KEPT ≠ SUPPORTED`

For provider-specific Black Arcana work:

`FAIL-CLOSED`

For final modpack compatibility:

`REAL RUNTIME QA REQUIRED`

If the pair actually fails to load or corrupts provider state, that finding would escalate from “unsupported” to a concrete pack blocker. This audit does not claim that failure without execution evidence.

## 7. Current public content surface

Publisher description:

- `25+` relics;
- 29 named entries visible in the current loot/evolution list;
- several evolved forms;
- explicit location categories for 1.21.1.

Exact/recent changelogs document current provider behavior involving:

- Moodworm;
- Twin Fangs;
- Eject Button;
- Bionic Eye;
- Cyberpsychosis;
- Mass Gauntlet;
- Swiftedge;
- Runic Plate;
- Made in Heaven;
- Wonder of U.

These facts support semantic deduplication. They do not establish a stable external API.

## 8. 1.7.0 persistent-config migration hazard

The More Relics 1.7.0 publisher changelog documents a specific upgrade failure mode:

- Made in Heaven was completely reworked;
- with Relics `enabledExtendedConfigs: true`, stale old ability values can produce a `data is null` crash;
- provider-recommended mitigation is disabling extended configs if unused or deleting/regenerating the Made in Heaven config;
- servers may require cleanup on both server and client.

QA consequences:

- a fresh instance is not automatically affected;
- an upgraded persistent profile/world may be affected;
- Black Arcana must not patch provider config ownership itself;
- release validation should inspect the actual instance configuration/history if the modpack evolved through pre-1.7.0 More Relics.

## 9. Current-line slot/UI behavior

Publisher changelogs establish:

- Eject Button can be equipped in charm/ring slots in 1.7.6;
- selected relic statuses/effects render icons above the food bar;
- 1.7.7 allows individual client-side indicator disabling.

Client indicators are presentation only. Any server progression/hazard integration based on icons would violate Black Arcana's server-authoritative rules.

## 10. Static QA risk matrix

| Risk | Evidence | Engineering response |
|---|---|---|
| More Relics 1.7.7 + Relics 0.12.8 unsupported | explicit More Relics publisher notice + 1.7.7 future-plan note | provider-specific fail-closed; runtime-test exact pair |
| Relics 0.12.8 is Beta | official Relics release metadata | do not infer API stability |
| Made in Heaven stale extended config | official More Relics 1.7.0 changelog | inspect actual config/history; provider-directed regeneration if needed |
| More Relics code/source unavailable for exact audit | no official source pin located; ARR project | no decompilation/private-contract inference |
| Relic progression/evolution host changed across versions | unsupported host transition + Relics beta evolution | validate persistence/evolution empirically before consuming state |
| Curios slot/passive duplication | addon uses Curios + current-line slot changes | provider-native effect settlement once |
| client icons mistaken for server state | 1.7.6/1.7.7 presentation features | never use visual indicator as authority |

## 11. Required runtime matrix

### Load and dependency gate

- launch client with exact current pack;
- launch dedicated server with exact current pack;
- verify no missing-method/class/mixin/load error involving More Relics/Relics/OctoLib/Curios/Architectury;
- verify handshake/join.

### Relic data/progression

- obtain a fresh More Relics item;
- equip/unequip through supported Curios slots;
- gain provider-owned relic XP where applicable;
- save/reload;
- reconnect;
- die/respawn;
- dimension change;
- verify no data reset/corruption/null failure.

### Evolution

At minimum validate one documented evolution chain end-to-end under current Relics 0.12.8, preserving provider ownership and persistent state.

### Current 1.7.7 features

Validate representative behavior for:

- Moodworm status/config;
- Twin Fangs repeated-hit safety;
- Eject Button threshold/config and slots;
- Bionic Eye Vulnerability behavior;
- Mass Gauntlet cooldown;
- evolved relic state after reload.

### Migration

If the instance predates More Relics 1.7.0, inspect Made in Heaven extended-config state and execute the publisher-documented remediation only when relevant.

## 12. API/integration gate

Even if runtime smoke is green, provider-specific Black Arcana integration still requires a supported external boundary. Unsupported host compatibility plus private/ARR implementation makes reflection/mixin coupling especially high risk.

Allowed without provider-specific API:

- semantic catalog/deduplication;
- provider-neutral Curios/equipment observations only where a canonical supported boundary already provides them;
- normal gameplay with provider ownership preserved if the pack proves stable.

Not approved:

- direct relic data mutation;
- direct relic XP/evolution mutation;
- private ability-state reads;
- client-icon-triggered server rewards;
- copying/decompiling provider code.

## 13. Current disposition

`CONTENT CATALOG ADVANCED`

`CURRENT PACK HOST COMBINATION = EXPLICITLY UNSUPPORTED BY ADDON PUBLISHER`

`RUNTIME RESULT = NOT YET ESTABLISHED BY THIS AUDIT`

`PROVIDER-SPECIFIC BLACK ARCANA/RPG INTEGRATION = FAIL-CLOSED`