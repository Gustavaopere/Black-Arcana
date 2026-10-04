# T.O Magic n' Extras 4.4.0.1 — 2026-09-08 physical/runtime correlation

Status: `STRONG CONTEMPORANEOUS PHYSICAL-RUNTIME EVIDENCE / REGISTRY-CRASH PATH NO LONGER OBSERVED / PROCESS HASH NOT EMBEDDED / SPELL DENOMINATOR STILL OPEN`

## Purpose

This checkpoint narrows Traveloptics Gate 2 using two Project Library artifacts from the same assembled CurseForge instance on 2026-09-08. It does **not** promote the provider to exact-current and does not project the publisher 33-ID registry onto the current physical bytes.

## Physical checkpoint immediately before runtime

Project Library file `modlist 08.09.2026.txt` was captured at approximately 12:05 UTC and records, on the Traveloptics row:

- filename: `traveloptics-4.4.0.1-1.21.1.jar`;
- mod id: `traveloptics`;
- runtime: `4.4.0.1-1.21.1`;
- SHA-1: `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`;
- fingerprint column: `4254006126`.

The next/previous-row boundary was rechecked explicitly: `fb37ae0a35e8bb9340e61007275121f02cf7a8bc` belongs to the neighboring Transmog row and is not Traveloptics evidence.

## Contemporaneous assembled runtime

Project Library `debug(9).log` belongs to the same `C:\Users\gusta\curseforge\minecraft\Instances\Mods` instance and begins the relevant client initialization at about 09:19 local time (~12:19 UTC), minutes after the physical dump.

The log proves that this assembled runtime:

- creates the FML container for `com.gametechbc.traveloptics.TravelopticsMod`;
- loads and watches `config\traveloptics\traveloptics-spells.toml`;
- loads and watches `config\traveloptics\traveloptics-common.toml`;
- scans/subscribes multiple Traveloptics event-handler classes, including weapon/effect handlers;
- advances through mod registration/initialization without emitting the earlier Traveloptics duplicate-registry exception.

Bounded search of the complete 33,748-line log finds **zero** occurrences of:

- `Mod loading issue for:`;
- `Adding duplicate value`.

This differs materially from the 2026-08-16 logs, where the same nominal provider failed during `RegisterEvent` with `IllegalStateException: Adding duplicate value ... KeyLootModifier`.

## Later crash is unrelated to Traveloptics registration

The 2026-09-08 boot eventually crashes during client game initialization with `MixinTransformerError`.

The root cause in the captured stack is:

`InjectionError: Critical injection failure ... in shine.mixins.json:ProgramMixin from mod shine`

on Minecraft shader initialization. The failure is not attributed to Traveloptics and occurs after Traveloptics container/config/event-handler setup has advanced past the earlier duplicate-codec crash point.

## What this proves

This is strong contemporaneous evidence that the **September physical line carrying SHA-1 `7b74816e...`** was being used in an assembled boot that no longer hit the original Traveloptics duplicate-codec registration failure.

It therefore narrows Gate 2 from `no current physical runtime evidence` to:

`CONTEMPORANEOUS PHYSICAL-RUNTIME INITIALIZATION OBSERVED / ORIGINAL DUPLICATE-REGISTRY FAILURE NOT OBSERVED`.

## What this does not prove

The runtime process itself does not print the JAR SHA-1. The physical dump and runtime are separated by minutes, so this is a strong temporal/instance correlation rather than a process-embedded cryptographic attestation. It must not be upgraded to `PATCHED_EXACT` or used to identify the provenance of `7b74816e...`.

The log also does not enumerate the Traveloptics spell registry. It therefore does not close:

- exact-current equality to the 33-ID publisher baseline;
- the provenance/content delta of `7b74816e...`;
- `traveloptics:blackout` survival acquisition;
- Somake Aqua ↔ T.O Aqua authority/deduplication;
- exact serializer object identity (`key_loot` vs `universal_loot`) inside the current runtime.

## Catalog consequence

Traveloptics remains **⚠️ partial/conditioned** and contributes **+0 strict** until the current 33-ID denominator or equivalent exact-content evidence is closed.

However, future work must no longer describe the current physical line as having *no* runtime initialization evidence. The 2026-09-08 physical/runtime pair is now canonical bounded evidence that the historical duplicate-registry crash path was not reproduced in a contemporaneous assembled boot.
