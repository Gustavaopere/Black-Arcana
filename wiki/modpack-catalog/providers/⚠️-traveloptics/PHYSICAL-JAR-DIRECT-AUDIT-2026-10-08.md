# Traveloptics 4.4.0.1-1.21.1 — direct current-physical JAR intake (2026-10-08)

Status: `CURRENT PHYSICAL SHA-1 MATCH / EXACT 33-ROOT SPELL REGISTRY VERIFIED / CODEC REFERENCES RESOLVED / BLACKOUT SURVIVAL + DEPLOYED RUNTIME OPEN / +0 STRICT`

## Exact uploaded physical authority

A user-supplied local modpack JAR was inspected read-only, without loading Minecraft or executing the mod.

- Name: `traveloptics-4.4.0.1-1.21.1.jar`;
- mod id/version from bundled NeoForge metadata: `traveloptics`, `4.4.0.1-1.21.1`;
- SHA-1: `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4` — matches the current sibling physical modlist;
- SHA-256: `e2522866f438a8c8ea5596c7d066347316b3463c30afb174d2491121d93e5eb9`;
- size: **18,393,641 bytes**; ZIP entries: **1,339**; class entries: **250**.

This directly eliminates the old **raw-current-JAR-unavailable** premise. It does not identify publisher or modification provenance. Its size coincides with the historically retained `fixed-keyloot.jar` candidate size, but size alone does not prove byte identity or deployment lineage.

## Exact-current spell registry

Bounded `javap -p -c` inspection of the physical `TOSpells` initializer and all concrete `spells/<school>/` classes observes:

- **33** `registerSpell` calls in the class initializer;
- **33** concrete and distinct spell class instantiations, with **zero conditional branch opcodes** in that initializer;
- **33** distinct provider-owned `traveloptics:<id>` resource identities;
- exact ID-set equality with all **33/33** previously cataloged publisher-baseline cards — **zero extra, zero missing**;
- the provider `registerSpell` symbol appears in the `TOSpells` class, not other classes in this archive, in a bounded class-byte token scan.

Therefore the **exact-current registered spell-ID denominator is 33**, not merely a historical publisher estimate. Spell metadata/effective behavior, server datapack overrides, survival eligibility and assembled runtime are separate evidence layers and are not inferred from this static initializer.

## Gate-2 loot serializer references and Blackout

The physical `TOLootModifiers` bytecode has:

- `key_loot` -> `KeyLootModifier.CODEC`;
- `universal_loot` -> `UniversalLootModifier.CODEC`.

These are distinct *referenced suppliers*. This supports the intended structural repair compared with the historical shared-serializer failure; it does **not** prove distinct constructed MapCodec instance identities or successful provider startup in the assembled pack. The schema-4 in-process probe is still required for that gate.

The exact JAR includes **20** provider global-loot JSON entries, all referenced by its NeoForge global-modifiers index. None directly names `traveloptics:blackout`. This is a bounded negative fact about the mod's own packaged modifier data, not a universal exclusion of generic host loot rules, third-party scripts, datapacks or command grants. The Blackout survival route remains **unverified**.

The current exact registered spell set contains no `traveloptics:aqua` spell ID. That does not independently resolve Somake Aqua integration/semantic ownership across the assembled pack.

## Accounting and remaining gates

- Exact-current provider spell identities: **33**; already individually cataloged **33/33**.
- Current strict addition: **+0**, pending authoritative current-pack reachability and runtime evidence.
- The global strict minimum is changed only by the independent Deeper and Darker audit, not by these 33 spell-ID findings.

Still required: current-instance Iron's settings/server/datapack acquisition context for Blackout and other conditional surfaces; provider-native schema-4 startup/registry/serializer observation; Aqua cross-provider deduplication; full-pack runtime QA.

## Method/clean-room

Read-only SHA-1/SHA-256; ZIP directory/resource parsing; Java 21 `javap -p -c` control-flow and identifier inspection; bounded class-byte symbol search. Local structural assertions passed. No provider binary, disassembly body, translation, implementation source or asset is committed. Static inspection is not a live-modpack test.
