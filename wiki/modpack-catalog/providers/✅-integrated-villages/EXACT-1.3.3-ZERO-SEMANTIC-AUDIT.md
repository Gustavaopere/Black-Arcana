# Integrated Villages 1.3.3+1.21.1-neoforge — exact semantic-boundary audit

Status: `EXACT PHYSICAL=PUBLISHER / WORLDGEN INTEGRATION / ZERO SEMANTIC ACTIONS`

## Provenance

- audit branch: `audit/mowzies-cataclysm-pickable-orbs-zero-semantic-2026-09-27`;
- audit HEAD: `220b1b1df04e5509f86c84b7297dc36d573c47fc`;
- workflow run: `36291915300` — GREEN;
- CurseForge project/file: `661376 / 8161672`;
- physical/publisher SHA-1: `4ba7360abf671b1f0f40c43c590977da2048490e`;
- exact artifact SHA-256: `b53a485828da352b1a6a24cd2796aacf5d8360632b98c7dfba295f235d41ec00`;
- text-only evidence artifact: `10922387584`;
- evidence-artifact digest: `sha256:42fa420f94c3d462b5217781dcf5eda1b3f2302ce2aeff27c11a7b580d0d5bf1`.

The workflow hard-gates publisher bytes against the physical pack SHA-1 before retaining only metadata, path/class identities, counts and narrow reference facts.

## Exact facts

- provider resources: 1441 = 1 asset + 1440 data files;
- data buckets: `advancement:13,integrated_structure_spawners:1,integrated_villages_pool_additions:4,loot_table:153,structure:754,tags:64,worldgen:451`;
- semantic-action-like paths: 0;
- semantic-action-like classes: 0;
- item/entity/registry class-name matches: 0;
- bounded gameplay-data paths: 681.

## Conclusion

The exact installed provider is worldgen/structure/loot/integration data, not a player spell/ritual/ability provider. Strict semantic delta: **+0**.
