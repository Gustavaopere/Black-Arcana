# Provider Audit Queue Delta — Phase 2V Ars Technica 2.7.6

Status: `SOURCE CATALOG CLOSED / INSTALLED CONFIG + RUNTIME QA OPEN`

This narrow overlay prevails only for `ars_technica` until the full shared provider queue is regenerated safely.

## Canonical row delta

| Mod ID | Nome atual | JAR atual | Versão atual | Estado da auditoria | Delta |
|---|---|---|---|---|---|
| `ars_technica` | Ars Technica | `ars_technica-1.21.1-2.7.6.jar` | `2.7.6` | `SOURCE-PINNED 2.7.6 / 11 SPELL PARTS 11/11 + ACQUISITION 11/11 + 3 BLOCKS + 3 BEs + 8 ENTITIES + 12 ARMORS + PRESSURE PERK + SOURCE MOTOR/TURRET/RELAY + 18 MIXINS + 5 PAYLOADS CATALOGADOS / RUNTIME+CONFIG QA PENDENTES` | preliminary feature-only page replaced by exact source catalog |

## Closed — source catalog

- physical JAR/version/mod id/SHA-1;
- exact Ars Technica 2.7.6 source pin;
- exact Ars 5.11.0.1267 inherited Tier-I source seam needed by Insert;
- 11/11 production spell-part registrations;
- 11/11 generated glyph-learning recipes;
- tier, mana, school, compatible augments and provider-specific limits/processing behavior for all 11;
- major Enchanting Apparatus acquisition surfaces;
- 3 blocks and 3 block entities;
- 8 misc entity types;
- current item/equipment registry surface and old Runic Spanner alias/migration;
- 12/12 Technomancy armor pieces and Ars perk-provider layout;
- Pressure Thread reserve/backtank implementation;
- Transmutation Focus spell/processing modifications;
- Source Motor Source-cost formula and Create stress/RPM boundary;
- Precise Relay and Ars Rune cadence customization;
- Transmutation Turret Source/caster transaction;
- Fuse/Whirl/item-fluid processing boundaries and provider world output;
- 18/18 declared mixins;
- 5/5 registered payload types across both network registration paths;
- COMMON source-default interoperability configs;
- Ars/Create/provider authority and deduplication consequences;
- clean-room provenance and license metadata discrepancy.

## Open — installed config/runtime

1. Compare actual generated/installed COMMON config against source defaults.
2. Verify 11 glyph registrations/recipes in the installed JAR/datapack/runtime.
3. Validate every concrete mixin against installed Ars Nouveau 5.13.1 and Create 6.0.10.
4. Source Motor: Source debit, redstone, RPM ±256, stress ratio, save/reload, chunk unload/reload and kinetic reconnect.
5. Pressure/backtank: perk level selection, equip/unequip, refill/depletion, death, logout and dimension change.
6. Transmutation Focus: Fortune injection and eligible output doubling without duplicate settlement from other addons.
7. Transmutation Turret: exact-once Source charge and cast execution, fake-player/caster behavior and reload safety.
8. Fuse/Whirl/Press/Polish/Apply/Insert/Telefeast: current Create recipe/capability interop and conservation of items/fluids.
9. Rune/Relay client→server packets: range, distance, permission and malicious-value behavior in multiplayer.
10. Source Motor Create-native configuration packet: inherited host validation under installed Create version.
11. Schematicannon: cadence/material conservation, player-query performance and client sync.
12. Dedicated-server/client/full-pack interoperability.

## Open — provenance

Resolve the `neoforge.mods.toml` LGPLv3 vs root `LICENSE` GPLv3 discrepancy before any future source copying, derivative implementation or asset reuse. Phase 2V itself remains read-only clean-room and copies no upstream implementation/assets.

## Merge gate

Before merge: fetch current `main`, reconcile semantically if it advanced, review the exact final diff, require fresh CI on the reconciled HEAD and keep review threads clear. Runtime/config items above may remain explicitly deferred because this PR closes factual source catalog coverage; they must not be reported as runtime PASS.