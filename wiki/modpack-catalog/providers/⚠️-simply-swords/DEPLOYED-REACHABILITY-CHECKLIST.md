# Simply Swords 1.70.2 — deployed reachability checklist

Status: `⚠️ CATALOG CLOSURE / EXACT ACTION DENOMINATOR 66 / DEPLOYED REACHABILITY OPEN`

## Purpose

Close only the remaining **deployed player-reachability** gate for the already
closed Simply Swords 1.70.2 semantic denominator.

Do not re-enumerate the 66 action roots. The exact action denominator is already
closed by `EXACT-1.70.2-ARTIFACT-ACTION-AUDIT.md`.

## Required physical fingerprint

Evidence must come from an instance carrying:

- JAR: `simplyswords-neoforge-1.70.2-1.21.1.jar`;
- mod id: `simplyswords`;
- runtime: `1.70.2-1.21.1`;
- SHA-1: `05b074ff774467f1fe9fb5592151b7845c321cbc`.

If the fingerprint differs, stop and re-audit the changed physical line.

## Bounded deployed config evidence

The release-line source checkpoint
`Sweenus/SimplySwords@359a8031b1a3243d1a3b013dbaa0cbba70ea8278`
declares Fzzy Config `0.7.6+1.21`.

At that checkpoint:

- `GeneralConfig` has config id `simplyswords:general`;
- `LootConfig` has config id `simplyswords:loot`;
- Fzzy Config 0.7.6 uses identifier namespace as the default folder,
  identifier path as the default filename, and TOML as the default file type.

Therefore the bounded collector may read only:

### `config/simplyswords/general.toml`

- `enableUniqueWeaponAwakening`

Interpretation:

- `true`: ordinary Unique weapon Awakening remains enabled; per-stack
  Awakening/unlock evidence is still required;
- `false`: this does **not** disable ordinary Unique abilities. Exact provider
  documentation/source semantics indicate ordinary Unique weapons operate at
  maximum Awakening while Runic Forge Awakening is disabled. Do not treat
  `false` as a zero-action state.

### `config/simplyswords/loot.toml`

- `enableLootDrops`;
- `runicLootTableWeight`;
- `uniqueLootTableWeight`;
- `enableContainedRemnants`;
- `disabledUniqueWeaponLoot`;
- `uniqueLootTableOptions`.

The collector retains only bounded values and validated resource IDs.
Missing/malformed/ambiguous values remain fail-closed.

## Still-open evidence after collector capture

Even a complete bounded collector report does not automatically promote the
provider. Review must still close, where applicable:

1. per-stack Awakening/unlock state for normally obtainable Unique forms;
2. ordinary survival acquisition/reformation paths for the 66 roots;
3. compatibility-dependent materialization, including source-defined optional
   integrations only when their host providers are actually present;
4. deployed datapack/script/addon suppression or replacement that changes
   current player reachability;
5. addon ownership reconciliation so one causal action is not counted twice.

## Promotion rule

Promote Simply Swords from ⚠️ only when current-pack evidence proves the
normally player-reachable subset of the already closed 66-root denominator.

The final semantic delta must be derived from that deployed subset. Source
defaults, creative/operator access, registry presence alone, and a complete
collector report by itself are insufficient.

Runtime combat correctness, Epic Fight/Lootr compatibility, persistence,
Runic Forge transactions and save migration remain separate QA after catalog
closure.
