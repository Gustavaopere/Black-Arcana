# Ars Sophisticated Compatibility — runtime QA gate

Status: `RUNTIME QA REQUIRED / FAIL-CLOSED`

## Why runtime QA remains open

The installed artifact `arssophisticatedcompat-0.3.0.jar` is not byte-identical to the accessible official NeoForge 1.21.1 publication `arssophisticatedstoragecompat-0.3.0.jar`.

The current physical host stack also includes Sophisticated Core 1.5.1, while the Notion dossier was written against 1.5.0. No exact installed-binary source/API contract has been established.

Therefore nominal version `0.3.0` and documented product-family behavior are insufficient to certify runtime compatibility.

## Required physical-binary inspection

Before any code-level BA adapter is approved, establish from the installed artifact or exact matching source:

1. exact metadata/dependency ranges;
2. registered item/upgrade/resource IDs;
3. capability/API entry points;
4. config values/defaults;
5. payloads/network direction and server validation;
6. mixins if any;
7. lifecycle/tick entry points;
8. Source storage/conversion/repair semantics;
9. recipe/acquisition definitions;
10. physical-artifact license/provenance.

## Required runtime matrix

On the actual modpack stack, validate at minimum:

- place/remove every supported upgrade;
- Source insert/extract and full-capacity behavior;
- Stack Upgrade increase/decrease while Source/duration is stored;
- Source Link conversion under player and automated inventory mutation;
- chunk unload/reload and full server restart;
- storage break/re-place/move paths supported by provider;
- Potion Jar effect expiration/removal/reconnect without ghost refresh;
- Enchanter repair with insufficient/exact/excess Source;
- two concurrent users/automation actors touching the same storage;
- dedicated-server startup/classloading;
- interaction with Sophisticated Storage Create Integration where applicable.

## Acceptance rule

Only directly observed or exact-source-backed behavior may move from `UNKNOWN` to `CONFIRMED`.

A failed or unavailable provider hook disables the dependent BA feature. It must not trigger a generic fallback that invents Source, repairs, potion duration or storage state.