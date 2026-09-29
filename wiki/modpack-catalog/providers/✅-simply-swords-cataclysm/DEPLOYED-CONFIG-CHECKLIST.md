# Simply Swords: Cataclysm 1.0.2 — deployed STARTUP config closure

Status: `PENDING DEPLOYED EVIDENCE`

## Purpose

Resolve which of the four source-pinned provider abilities are active in the exact current pack without substituting upstream defaults.

## Physical guard

Evidence is valid only when the deployed JAR still matches:

- `simplycataclysm-1.0.2+1.21.1+neoforge.jar`;
- SHA-1 `a2aa0f82ae3a9be2f43a4d47b3cb2201dd4e1469`.

If the artifact changes, re-audit before promoting config results.

## Required effective values

Capture the effective NeoForge STARTUP config state corresponding to the exact source keys:

| Ability | Required effective evidence | Activation classification |
|---|---|---|
| Accursed Rage | `accursedRageChance` | zero => disabled; non-zero => active candidate |
| Blazing Brand | `blazingBrandChance` | zero => disabled; non-zero => active candidate |
| Mecha Pulse | `mechaPulseChargeChance` | zero => no normal charge progression; non-zero => active candidate |
| Mecha Smite | `mechaSmiteHarmfulEffectsChance`, `mechaSmiteFireDuration`, `mechaSmiteWitherDuration`, `mechaSmiteRegenChance`, `mechaSmiteRegenUsesPercentage`, `mechaSmiteRegenPercentage`, `mechaSmiteRegenThreshold` | harmful branch requires non-zero chance plus at least one non-zero harmful duration; regenerative branch is classified independently from chance + selected threshold mode/value |

Also retain the exact source-config context for other durations/amplifiers/cooldowns as runtime/balance evidence. `mechaSmiteFireDuration` and `mechaSmiteWitherDuration` are catalog gates because the provider explicitly documents zero as disabling those harmful effects; they do not create extra semantic identities.

## Accepted evidence

Use one of:

1. exact deployed config file captured from the current instance;
2. deterministic read-only runtime/config probe reporting the effective values;
3. equivalent authoritative assembled-pack evidence tied to the physical SHA-1 above.

The repository read-only collector now has a bounded route for this provider:

```bash
python docs/qa/provider-catalog-deployed-evidence-collector.py "/path/to/modpack-instance"
```

It reads only `config/simplycataclysm-startup.toml`, retains only the ten closure keys above, and fingerprints the exact physical JAR. A missing/incomplete key stays fail-closed; the collector never substitutes source defaults.

Current archived instance logs confirm that NeoForge loaded and watched `config/simplycataclysm-startup.toml`; those logs do **not** expose the values and therefore do not close this checklist by themselves.

Do not use:

- source defaults alone;
- generic publisher defaults;
- a config from another instance/world;
- client tooltip behavior as proof of server/startup state.

## Promotion rule

Once effective values are known:

- active identities may enter the strict numerator;
- disabled identities remain provider inventory but not strict current-pack actions;
- provider can leave ⚠️ only when all four are classified and no other catalog blocker remains.

Runtime combat QA remains separate from semantic/config closure.
