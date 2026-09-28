# ShadowsZ 1.1.9 — Deployed Fusion Config Checklist

Status: `OPEN / SINGLE CONFIG VALUE REQUIRED`

The exact 1.1.9 artifact audit already closes the complete semantic denominator at **10 roots**:

- 9 are `COUNTED_EXACT`;
- Shadow Fusion is the only `CONDITIONAL` root.

## Required evidence

Capture the effective current-pack value of:

`fusionEnabled`

from the actual deployed ShadowsZ common/server configuration used by the current instance/world.

Also record:

- current physical JAR fingerprint: `f946eb3a8181e1964279f163f430ccbba6c4edcd`;
- exact config path/file used;
- whether the value is explicit or inherited/generated;
- evidence timestamp/checkpoint.

## Acceptance

If effective `fusionEnabled=false`:

- keep Shadow Fusion inactive/excluded from strict count;
- semantic strict total remains **9 for ShadowsZ**;
- ShadowsZ can leave this config blocker if no other catalog gate appears.

If effective `fusionEnabled=true`:

- promote Shadow Fusion from `CONDITIONAL` to `COUNTED_EXACT`;
- ShadowsZ strict contribution becomes **10**;
- increase the global strict ledger by **+1**.

Missing, ambiguous or stale evidence remains fail-closed.

Runtime/integration QA is separate from this catalog/config closure.
