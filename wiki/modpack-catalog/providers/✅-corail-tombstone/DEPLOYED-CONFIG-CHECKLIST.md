# Corail Tombstone 9.5.6 — deployed config closure checklist

Status: `10 STRICT COUNTED_EXACT ACTIONS CLOSED / PHYSICAL=PUBLISHER HASH CLOSED / 12 CASTABLE FAMILIES EXACTLY DEDUPED / DEPLOYED ALLOW FLAGS REQUIRED`

## Already closed — do not redo

- current filename/runtime line: `tombstone-neoforge-1.21.1-9.5.6.jar`;
- exact publisher File `8842741` SHA-1: `d830d16caa20b0d23a44ed6b1d339bc22afc2460`;
- Project Library physical modlist snapshot `modlist(1).txt` (2026-09-16) records the installed Tombstone JAR with the same SHA-1; physical↔publisher equality is closed;
- 6 prayer + 4 Ritual Flute semantic actions strict-counted as `COUNTED_EXACT`;
- 12 remaining castable magic-item action families exactly deduplicated one-to-one to provider `allow_*` gates;
- scroll-buff/effect/enchantment/document wrappers excluded by the semantic metric.

Do not re-enumerate the action surface unless the physical version changes.

## Required deployed evidence

Run the bounded collector on the exact current assembled instance/world.

Required report evidence:

1. exactly one `mods.corail_tombstone` row for `tombstone-neoforge-1.21.1-9.5.6.jar`;
2. `release_9_5_6_equality = true` should still be re-observed when collecting the eventual current-instance config report as a drift guard; canonical catalog identity is already closed by the physical modlist snapshot;
3. effective deployed values for these 12 keys:

- `allow_tablet_of_assistance`;
- `allow_tablet_of_cupidity`;
- `allow_tablet_of_guard`;
- `allow_tablet_of_home`;
- `allow_tablet_of_recall`;
- `allow_gemstone_of_familiar`;
- `allow_gemstone_of_guardian`;
- `allow_gemstone_of_merchant`;
- `allow_grave_key`;
- `allow_lost_tablet`;
- `allow_magic_scroll`;
- `allow_scroll_of_knowledge`.

The collector reads only bounded config roots and only those keys. `defaultconfigs` is template evidence; actual world/server config precedence must be resolved from the deployed environment.

## Acceptance per action family

For each of the 12 exact rows in `EXACT-9.5.6-CONDITIONAL-CASTABLE-MATRIX.md`:

- effective `allow_*=true` + matching current-instance 9.5.6 fingerprint → eligible for strict promotion according to the already-closed one-to-one semantic mapping;
- effective `allow_*=false` + matching physical fingerprint → close as deployed-disabled, **+0** for that row;
- missing/ambiguous value or non-matching physical artifact → keep that row conditional.

Do not multiply internal modes/effects into additional identities.

## Files to update after closure

- `EXACT-9.5.6-CONDITIONAL-CASTABLE-MATRIX.md`;
- provider README/action cards for rows actually resolved;
- semantic/global ledgers only by the number of newly enabled strict action families;
- folder prefix ⚠️ → ✅ only when all 12 gates are resolved for the current physical artifact.

Runtime resource/Soul settlement, multiplayer behavior, grave recovery and external inventory integration remain separate QA.

## Authority rule

Tombstone owns Souls, magic-item use, prayers, rites and Knowledge of Death. Black Arcana records catalog identity/availability only and must not duplicate provider settlement.
