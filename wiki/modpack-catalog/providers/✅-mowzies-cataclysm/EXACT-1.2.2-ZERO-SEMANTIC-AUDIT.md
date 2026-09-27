# Mowzie's Cataclysm 1.2.2 — exact semantic-boundary audit

Status: `EXACT PHYSICAL=PUBLISHER / ZERO SEMANTIC ACTIONS`

## Provenance

- audit branch: `audit/mowzies-cataclysm-pickable-orbs-zero-semantic-2026-09-27`;
- audit HEAD: `220b1b1df04e5509f86c84b7297dc36d573c47fc`;
- workflow run: `36291915300` — GREEN;
- CurseForge project/file: `1128348 / 8196282`;
- physical/publisher SHA-1: `0dff3e849155ca343d1a500f5b9ca2b54ffa692d`;
- exact artifact SHA-256: `afbef1775a869eb65dbd5eb2fe75b37edd1b2d08b014b24d2049867b7ef768b0`;
- text-only evidence artifact: `10922422417`;
- evidence-artifact digest: `sha256:6d0dede14852266a3586d22aa7cca1e17e59e0550b9379d2d644fc14103aeb0b`.

The workflow hard-gates publisher bytes against the physical pack SHA-1 before retaining only metadata, path/class identities, counts and narrow reference facts.

## Exact facts

- provider resources: 19 = 11 assets + 8 data files;
- data buckets: `recipe:4,tags:4`;
- semantic-action-like paths: 0;
- semantic-action-like classes: 0;
- item/entity/registry class-name matches: 7;
- gameplay-data paths: 8.

The eight data files are four Eye recipes and four worldgen structure tags. The exact four item classes and four English Eye localization roots align one-to-one with the published locator role.

## Conclusion

The exact installed provider adds locator content, not a spell/ritual/ability catalog. Strict semantic delta: **+0**.
