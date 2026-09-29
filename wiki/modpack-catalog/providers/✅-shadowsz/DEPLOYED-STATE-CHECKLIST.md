# ShadowsZ 1.1.9 — deployed state closure checklist

Status: `⚠️ REQUIRED FOR STRICT PROMOTION`

## Exact artifact already closed

Do **not** repeat the exact-artifact denominator audit unless the physical JAR changes.

Pinned facts:

- JAR: `shadowsz-1.1.9.jar`;
- physical/publisher SHA-1: `f946eb3a8181e1964279f163f430ccbba6c4edcd`;
- exact semantic denominator: **10**;
- exact roots: 3 Umbral spells + Shadow Eyes + Shadow Arising + Summon + Dismiss + Position Swap + Despawn Wild + Shadow Fusion;
- audit PR: #443;
- audit HEAD: `2ea4f054a2cecc487bc27d629824a865a502e4dd`;
- audit run: `36430580803` GREEN.

## Remaining deployed evidence

Capture from the **current assembled world/server**, with the physical fingerprint above rechecked:

1. effective gamerule:
   - `shadowszRestrictPowers`;

2. effective ShadowsZ config:
   - `fusionEnabled`.

Defaults from the JAR are not deployment evidence.

## Promotion matrix

### If `shadowszRestrictPowers = false`

Natural player attunement remains available according to the provider contract.

- `fusionEnabled = false` -> **9 strict semantic roots**;
- `fusionEnabled = true` -> **10 strict semantic roots**.

### If `shadowszRestrictPowers = true`

Normal survival players cannot acquire the power through the provider's natural attunement path; only operators may claim it.

Under the current normal-player semantic reachability rule:

- keep all ShadowsZ roots **CONDITIONAL / +0 STRICT** unless a separately authoritative normal-player grant route is intentionally deployed and evidenced.

## Non-blocking settings

The following exact config booleans do not create additional semantic roots and are not required to close the current denominator:

- `progressMode`;
- `levelingEnabled`;
- `equipmentEnabled`;
- `blackTexture`.

They remain relevant to runtime/progression QA but not to the 10-root semantic inventory.

## Collector route

The canonical read-only collector now captures both remaining deployed-state inputs:

```bash
python docs/qa/provider-catalog-deployed-evidence-collector.py "/path/to/modpack-instance" \
  --world "/path/to/authoritative/world"
```

Review:

- `mods.shadowsz[0].current_physical_1_1_9_equality`;
- `shadowsz.fusion_enabled_matches`;
- `shadowsz.restrict_powers_gamerules`.

The collector never substitutes the artifact defaults. `defaultconfigs` is template evidence only, and the gamerule row must come from the authoritative saved world. If the server is running, save/flush world state before collection so `level.dat` represents the intended deployed state.

## Evidence format

Record:

- world/server identifier or exact release-candidate context;
- physical JAR SHA-1;
- exact gamerule value;
- exact config file/path and `fusionEnabled` value;
- capture date;
- whether the server/world was restarted after config changes where required.

Do not infer values from publisher docs, artifact defaults, generated defaults or a different save/server.