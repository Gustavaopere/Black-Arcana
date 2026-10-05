# Traveloptics Gate 2 — preserved-log search boundary (2026-10-05)

Status: `INDEXED PRESERVED-LOG SEARCH EXHAUSTED / HISTORICAL FAILURE POSITIVE / POST-REPAIR DISTINCT-SERIALIZER OBSERVATION NOT FOUND / PHYSICAL PROBE STILL REQUIRED`

## Purpose

This checkpoint records the result of a bounded search across the Project Library's preserved runtime logs for direct evidence of the two Traveloptics global-loot-modifier serializer registrations required by Gate 2.

It exists to prevent repeated generic log searching from being mistaken for progress or for absence evidence.

## Target evidence

The canonical Black Arcana QA probe expects bounded runtime rows for:

- `traveloptics:key_loot`;
- `traveloptics:universal_loot`;
- pair result `distinct_codec_instances=true`.

Canonical runbook: `docs/qa/provider-catalog-runtime-registry-probe.md`.

## Preserved-log search result

A bounded Project Library indexed search on 2026-10-05 was performed for:

- exact serializer IDs `traveloptics:key_loot` and `traveloptics:universal_loot`;
- `key_loot` / `universal_loot` paired with Traveloptics/registry context;
- `KeyLootModifier` / `UniversalLootModifier`;
- expected probe marker `distinct_codec_instances=true`.

What surfaced:

- multiple 2026-08-16 / early-2026-08-17 assembled logs and crash reports reproducing Traveloptics `RegisterEvent` failure with duplicate `KeyLootModifier` codec registration;
- post-repair/current-line logs that reach Traveloptics config/resource/runtime initialization;
- **no indexed preserved-log hit that directly records both serializer IDs as observed registry values**;
- **no indexed preserved-log hit for `distinct_codec_instances=true`**;
- **no indexed preserved-log hit identifying a post-repair `UniversalLootModifier` serializer object**.

## Evidence boundary

This result is **not** proof that the target rows never existed in any raw log.

The Project Library search layer is indexed/retrieval-based and some retained runtime files are not fully readable/exportable as raw bytes in the current project context. Search misses therefore remain non-absence evidence.

Likewise, successful post-repair startup does not prove the two registered serializer values are distinct objects.

## Gate consequence

Gate 2 remains:

`HISTORICAL DUPLICATE-CODEC FAILURE REPRODUCED / CONTEMPORANEOUS CURRENT-LINE INIT OBSERVED / DIRECT DISTINCT-SERIALIZER OBSERVATION STILL OPEN`.

Further generic Project Library keyword searching is no longer a productive closure path.

The next authoritative step is the existing physical-pack QA probe, paired with the deployed Traveloptics artifact disposition:

1. run the canonical provider-catalog registry probe in the assembled pack;
2. retain the two serializer-ID rows;
3. retain the pair result;
4. pair that run with the physical Traveloptics hash/disposition;
5. require `status=OBSERVED` for both IDs and `distinct_codec_instances=true` before treating the serializer-pair observation as closed.

This checkpoint changes no semantic count, provider status, Blackout acquisition conclusion, or physical provenance disposition.
