# T.O Magic n' Extras — 2026-08-17 post-repair canonical-slot runtime correlation

Status: `HISTORICAL POST-REPAIR CANONICAL-SLOT BOOT OBSERVED / FIXED-KEYLOOT CANDIDATE PRECEDES BOOT / PROCESS HASH UNBOUND / CURRENT 7b74816e IDENTITY UNPROVEN`

## Purpose

This checkpoint narrows the retained August repair chronology for T.O Magic n' Extras 4.4.0.1-1.21.1.

The Project Library preserves a failing assembled-pack process, two local JAR records, and the immediately following assembled boot. The following boot discovers Traveloptics under the **canonical filename** in the real CurseForge instance `mods` folder and progresses beyond the earlier fatal Traveloptics `RegisterEvent` stage into provider initialization and resource reload.

This is stronger historical repair-lineage evidence than coexistence of the retained JAR records alone. It is **not** a cryptographic bridge to current physical SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`.

## Retained sequence

### 1. Last retained pre-repair failure

Project Library record:

- `crash-2026-08-16_23.51.05-fml.txt`;
- retained at approximately `2026-08-17T02:51:57Z`.

The crash report identifies:

- mod file path ending in `mods/traveloptics-4.4.0.1-1.21.1.jar`;
- mod id `traveloptics`;
- runtime `4.4.0.1-1.21.1`;
- failure while dispatching NeoForge `RegisterEvent`;
- `IllegalStateException: Adding duplicate value ... to registry`;
- duplicated value rooted at `com.gametechbc.traveloptics.loot.KeyLootModifier`.

This is the same historical duplicate-codec failure already cataloged in [`RUNTIME-2026-08-16-LOOT-CODEC-CRASH.md`](RUNTIME-2026-08-16-LOOT-CODEC-CRASH.md).

### 2. Local JAR records retained minutes later

Project Library metadata retains:

- `traveloptics-4.4.0.1-1.21.1.jar` — 18,393,445 bytes — retained at approximately `2026-08-17T02:54:20Z`;
- `traveloptics-4.4.0.1-1.21.1-fixed-keyloot.jar` — 18,393,641 bytes — retained at approximately `2026-08-17T02:56:14Z`.

The second filename is evidence that a local `fixed-keyloot` repair candidate existed at that point. Its bytes are not currently materializable through the available Project Library path, so its SHA-1/content delta is not established here.

### 3. Canonical filename discovered in the following assembled boot

The retained `stdout-logs(20260817-032725).txt` contains a NeoForge `ModDiscoverer` event with timestamp `1786935446675`, corresponding to `2026-08-17T02:57:26.675Z`:

- `Found mod file "traveloptics-4.4.0.1-1.21.1.jar"`;
- locator: `mods folder locator at C:\\Users\\gusta\\curseforge\\minecraft\\Instances\\Mods\\mods`;
- reader: `mod manifest`.

The discovery event is approximately **73 seconds after** the retained Library timestamp for the separately named `fixed-keyloot.jar`.

The same retained boot surface does not establish that the canonical file bytes equal the separately retained candidate. It proves only that the next assembled process discovered the **canonical slot/name** rather than requiring the `fixed-keyloot` name as the active mod filename.

## Runtime progression after discovery

The paired `debug(20260817-032729).log` / `latest(20260817-032726).log` subsequently record Traveloptics progressing through initialization:

- both Traveloptics TOML configs are loaded/watched;
- `TravelopticsMod$ClientModEvents` is scanned/subscribed;
- `TOEntityAttributes`, `TOCreativeTabs`, `ModClientEvents`, `MobEffectsServerEvent`, `FrozenSightClientHandler`, `CastingClientHandler`, `SpellsConfig` and `CommonConfig` are reached in event-subscriber/config initialization;
- the process then reaches client resource reload and resolves Traveloptics sprites, models and `traveloptics:animations/casting_animations.json`.

The pre-repair processes terminated during Traveloptics registry registration with the duplicate `KeyLootModifier` codec. Reaching provider resource reload in the next canonical-slot process therefore establishes that this boot progressed **past that earlier fatal stage**.

This checkpoint does not infer the exact repaired serializer wiring from the successful progression.

## What this establishes

- a `fixed-keyloot` candidate existed before the following preserved assembled boot — **YES**;
- the following boot discovered `traveloptics-4.4.0.1-1.21.1.jar` from the actual instance `mods` directory — **YES**;
- that process progressed past the earlier fatal Traveloptics `RegisterEvent` failure into resource reload — **YES**;
- the post-candidate canonical-slot process does not terminate at the formerly fatal Traveloptics registration point and reaches provider resource reload — **YES**.

## What this does not establish

- the `fixed-keyloot.jar` bytes were copied/renamed into the canonical slot — **NOT PROVEN**;
- the canonical JAR in this boot has the same bytes as the separately retained `fixed-keyloot.jar` — **NOT PROVEN**;
- the boot's canonical JAR SHA-1 is `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4` — **NOT PROVEN**;
- the exact current physical registry equals the 33-ID publisher registry — **NOT PROVEN BY THIS CHECKPOINT**;
- `traveloptics:key_loot` and `traveloptics:universal_loot` resolve to distinct codec instances in current physical runtime — **NOT PROVEN**;
- `traveloptics:blackout` has a current-pack survival acquisition route — **NOT PROVEN**.

## Gate consequences

### Gate 1 — provenance/content delta

Narrowed, not closed.

The August local-modification window now has a bounded operational sequence:

`duplicate-codec canonical-slot failure -> retained canonical + fixed-keyloot candidate -> canonical-slot boot progressing past the failure -> launcher isModified=true -> 33-ID historical runtime -> first direct 7b74816e capture`.

The missing bridge is still raw-byte/checksum/content evidence tying one of the Aug-17 artifacts or the post-repair boot to the Aug-22/current `7b74816e...` bytes.

### Gate 2 — registry initialization

Historical evidence is strengthened from a broad later-runtime observation to an **immediate post-repair canonical-slot process** that passes the former fatal registration stage.

Current physical closure remains fail-closed because the process does not embed the JAR SHA-1 and does not directly observe the two target serializer instances.

## Catalog consequence

No provider status, semantic count, spell identity, mechanics row or strict numerator changes.

Traveloptics remains:

`⚠️ partial / conditioned / OTHER_VERIFIED / strict +0`.

The next useful evidence remains exact-current bytes/checksums/provenance or an equivalent hash-bound runtime/content attestation.
