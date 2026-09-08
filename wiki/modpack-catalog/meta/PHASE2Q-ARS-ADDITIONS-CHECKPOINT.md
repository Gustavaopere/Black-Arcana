# Phase 2Q — Ars Additions 21.3.0 checkpoint

State: `SOURCE CATALOG COMPLETE / FINAL BRANCH QA + MERGE GATE PENDING`

## Current synchronized base

Phase 2Q originally started from the Phase 2P Ars Nouveau merge `main@f9c3854bc7e5b2f1bd051434080f13ae3c7d5e5d`.

During Phase 2Q, `main` advanced with concurrent Stage 07.07 Borrowed Sight work to `4053c060bb7e4c3f57ca06f49295868277a6eb57`. The catalog branch also received concurrent Phase 2Q documentation through `903e2c1f9251d154a7c912f30f74089f6d7b0c55`. Both streams were preserved by synchronization PR #96, merged into the catalog branch as `9b748a1cc49944c211a3ad0e5fe35bc00bfb51f2` with two-parent ancestry. No rebase/force-push was used.

Canonical Phase 2Q PR: **#94**, branch `docs/magic-catalog-phase2q-ars-additions`.

## Exact installed provider

- JAR: `ars_additions-1.21.1-21.3.0.jar`;
- mod id: `ars_additions`;
- runtime metadata: `1.21.1-21.3.0`;
- physical SHA-1: `ce2440b606acb20b79a42bf7c6c24d163c93241f`;
- CurseForge project/file: `974408` / `7646325`.

## Source/provenance checkpoint

Factual source audit is pinned to `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`, whose `version` file is exactly `21.3.0`. Root `LICENSE` is GNU LGPL v3. No upstream code or assets are copied/adapted into Black Arcana.

The provider source baseline references Ars Nouveau `5.11.2.1298`, while the installed pack uses Ars Nouveau `5.13.1`; runtime compatibility remains a separate fail-closed QA gate.

## Closed source surfaces

- 3/3 glyphs;
- 2/2 rituals;
- 1/1 perk;
- 1/1 registered mob effect;
- 12/12 charms;
- 35 blocks + 35 block items;
- 26 direct items = 14 non-charm direct items + 12 charms;
- 61 total items when block items are included;
- 5 block entities and 0 custom EntityTypes;
- 11 data components and 4 attachments;
- 5 recipe serializers + 5 recipe types;
- 15 built-in Locate Structure recipes;
- Warp/Source/storage/target-reference/state-transfer/automation systems audited;
- Spellweave, Enchanting Wixie, Bulk Scribing and Ars-base mixin modifications audited;
- Arcane Library, Nexus Tower and Ruined Warp Portal worldgen/config/loot surfaces audited;
- local-weather infrastructure classified as dormant/not active in the audited production path.

## Preserved gaps and divergences

- Retaliate's public description says the last attacker within five seconds, while the inspected executable class uses `caster.getKillCredit()` without an explicit age check in that class. Runtime behavior remains QA-required.
- Memory Crystal has confirmed registry/state/runtime behavior, but a normal default acquisition path was not proven in the audited source pass; no acquisition is invented.
- Lost and Ancient Codex Entry variants are registered and executable but explicitly unobtainable by default in the release-line documentation; only Tier I Codex Entry is injected into normal basic loot by `AddonSetup`.
- Exact physical-JAR↔source-commit byte equivalence is not claimed.

## Remaining Phase 2Q work

1. run final diff/provenance consistency review;
2. update PR #94 body to this source-complete state;
3. run CI on the current synchronized HEAD;
4. fetch `main` again immediately before merge and reconcile if it advanced;
5. re-run CI after any final synchronization;
6. only after a green reconciled HEAD, mark PR ready and merge;
7. confirm post-merge `main` SHA and post-merge CI.

No Black Arcana runtime Stage is changed by this checkpoint.
