# IronSable X Wind's Spellbooks 1.0.0 — exact semantic-boundary audit

Status: `EXACT PHYSICAL=PUBLISHER / EXISTING-SPELL PHYSICS BRIDGE / ZERO NEW IDENTITIES`

## Provenance

- audit branch: `audit/mowzies-cataclysm-pickable-orbs-zero-semantic-2026-09-27`;
- audit HEAD: `220b1b1df04e5509f86c84b7297dc36d573c47fc`;
- workflow run: `36291915300` — GREEN;
- CurseForge project/file: `1643762 / 8598265`;
- physical/publisher SHA-1: `c09c73a83deaf6439f2d33652898eb610dbfa4f3`;
- exact artifact SHA-256: `8f2a885bd21ee614c56b28c4558fc240290dd2fb64e6ccb1e799c5165ab67e2d`;
- text-only evidence artifact: `10922686707`;
- evidence-artifact digest: `sha256:d3d1ca6b1f60a3358feb72d1ecde130b20c86e55bb25cc2ecc6a9caf18556543`.

The workflow hard-gates publisher bytes against the physical pack SHA-1 before retaining only metadata, path/class identities, counts and narrow reference facts.

## Exact facts

- provider resources/assets/data: 0 / 0 / 0;
- semantic-action-like paths/classes: 0 / 0;
- exact class count: 14;
- gameplay-data paths: 0.

Exact classes include dedicated physics handlers for Aeropic, Almighty Push, Tornado and Wind Blade. Narrow constant/reference inspection confirms all four Wind spell names plus `wind_spellbooks`, `ironsable` and `sable` are referenced by the exact artifact.

## Deduplication

Wind's Spellbooks already owns `wind_spellbooks:tornado`, `wind_spellbooks:almighty_push`, `wind_spellbooks:wind_blade` and `wind_spellbooks:aeropic`. The bridge changes physical interaction only. Strict semantic delta: **+0**.
