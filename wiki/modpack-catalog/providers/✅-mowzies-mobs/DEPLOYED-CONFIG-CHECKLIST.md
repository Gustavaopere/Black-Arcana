# Mowzie's Mobs 1.8.2 — deployed config closure checklist

Status: `CURRENT EXACT ARTIFACT CLOSED / ONE DEPLOYED BOOLEAN REMAINS`

## Already closed — do not redo

- current JAR: `mowziesmobs-1.21.1-1.8.2.jar`;
- mod id: `mowziesmobs`;
- exact physical/publisher SHA-1: `d64475cd77444b056ece6472c79d40293dc63c6c`;
- exact current active `PLAYER_ABILITIES` array: 13 slots;
- semantic reconciliation: 10 strict independent powers, 1 conditional Tunneling power, 2 technical/subaction exclusions;
- `TunnelingAbility.canUse()` reads provider config `ConfigHandler$EarthrendGauntlet.enableTunneling`.

Do not re-enumerate the registry unless the physical version changes.

## Required deployed evidence

Run the bounded collector against the actual current assembled instance/world:

```bash
python docs/qa/provider-catalog-deployed-evidence-collector.py "/path/to/modpack-instance" \
  --world "/path/to/authoritative/world"
```

Required report evidence:

1. exactly one `mods.mowzies_mobs` row for `mowziesmobs-1.21.1-1.8.2.jar`;
2. `current_physical_1_8_2_equality = true`;
3. an authoritative effective observation for `mowzies_mobs.enable_tunneling_matches` tied to the actual deployed config/world.

The collector checks `config/`, `defaultconfigs/` and discovered/explicit world `serverconfig/`. `defaultconfigs` is template evidence only. Resolve precedence from the actual deployed instance/world; do not substitute the source default.

## Acceptance

If the exact physical fingerprint matches and the effective deployed value is:

- **true** — promote `tunneling` to strict-counted; Mowzie's strict semantic contribution becomes **11**;
- **false** — close `tunneling` as deployed-disabled; strict contribution remains **10**;
- **missing / ambiguous / conflicting without precedence proof** — remain ⚠️.

Either authoritative boolean resolves the catalog conditionality. Runtime/network/balance QA remains separate and may stay fail-closed after catalog closure.

## Files to update after closure

- this provider README;
- `PLAYER-MAGIC-INVENTORY.md`;
- `wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md` only if the effective value is true and the strict numerator changes;
- `CATALOG-COVERAGE-CURRENT.md`, `CURRENT-MAGIC-PROVIDERS.md` and global catalog status;
- folder prefix ⚠️ → ✅ only after the declared catalog scope is fully resolved.

## Authority rule

Mowzie's Mobs owns the power/runtime. Black Arcana records the deployed semantic availability; it does not create a fallback Tunneling implementation or duplicate Mowzie's settlement.
