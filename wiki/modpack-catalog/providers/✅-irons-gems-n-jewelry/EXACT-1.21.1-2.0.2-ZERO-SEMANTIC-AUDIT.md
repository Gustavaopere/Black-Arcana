# Iron's Gems 'n Jewelry 1.21.1-2.0.2 — exact semantic-boundary audit

Status: `EXACT PHYSICAL=PUBLISHER / EQUIPMENT PROC FRAMEWORK / ZERO INDEPENDENT SEMANTIC ACTIONS`

## Provenance

- audit branch: `audit/mowzies-cataclysm-pickable-orbs-zero-semantic-2026-09-27`;
- audit HEAD: `220b1b1df04e5509f86c84b7297dc36d573c47fc`;
- workflow run: `36291915300` — GREEN;
- CurseForge project/file: `1101111 / 8365016`;
- physical/publisher SHA-1: `2f8d934d04111037dcf3fe7b04c96aec892da744`;
- exact artifact SHA-256: `7413dd081598337133e55dd7c42ac3adff5213bceb56f10da6cfb5b52d57958e`;
- text-only evidence artifact: `10922940536`;
- evidence-artifact digest: `sha256:bf1fb3644328d1adb554b06051e2d81a29e90bd3c729b1b265732ff91abda642`.

The workflow hard-gates publisher bytes against the physical pack SHA-1 before retaining only metadata, path/class identities, counts and narrow reference facts.

## Exact facts

- provider resources: 248 = 122 assets + 126 data files;
- data buckets: `curios:3,irons_jewelry:63,loot_modifiers:11,loot_table:19,recipe:3,structure:5,tags:22`;
- semantic-action-like spell/ritual/rite/ability paths: 0;
- semantic-action-like spell/ritual/rite/ability classes: 0;
- bounded item/entity/registry class-name matches: 49;
- bounded gameplay-data paths: 44.

## Source corroboration of the internal action framework

Public 1.21.1 source pin `bd3fae5579376472c04d9090e42a7a932d604333` declares version `1.21.1-2.0.2`. Its `ActionRegistry` registers eight `IAction` codecs. `ActionParameter` wraps an `IAction` as bonus data, and `JewelryBonusEvents` calls `handleAction` from equipment event callbacks. The generated material/pattern definitions assign those actions to jewelry bonuses.

This proves the action registry is a proc/effect primitive layer, not evidence of eight player-facing spells.

## Conclusion

Strict semantic delta: **+0**. Runtime proc/cooldown/stacking behavior remains separate QA.

