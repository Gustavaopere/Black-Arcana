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
| Accursed Rage | `accursedRageChance` | Positive chance is a candidate for stacking; zero alone is not strict exclusion because code uses RNG <= chance. Existing Rage and max-amplifier0 have separate paths. |
| Blazing Brand | `blazingBrandChance` | Positive chance is a candidate; zero is intended disable in comments, but RNG exactly0 satisfies the comparison. Brand application and lifesteal have distinct results. |
| Mecha Pulse | `mechaPulseChargeChance` | Positive chance is a candidate for charge; inspect cooldown, existing charge and threshold. Chance0 is not an explicit guard; threshold0 with absent charge can throw before RNG. |
| Mecha Smite | `mechaSmiteHarmfulEffectsChance`, `mechaSmiteFireDuration`, `mechaSmiteWitherDuration`, `mechaSmiteRegenChance`, `mechaSmiteRegenUsesPercentage`, `mechaSmiteRegenPercentage`, `mechaSmiteRegenThreshold` | Harmful branch requires a satisfied inclusive chance check and at least one duration >0; regeneration is independent and uses strict health < selected threshold. Chance0 alone does not demonstrate disabled. |

These ten values are minimum triage evidence, not a full activation proof. Retain the other effective durations/amplifiers/cooldowns and relevant pre-existing effects. `mechaSmiteFireDuration` and `mechaSmiteWitherDuration` have explicit >0 guards; their zero cases differ from the inclusive RNG checks. They do not create extra semantic identities. See the [23/10/2026 causal audit](IMPLEMENTATION-PERK-BOUNDARIES-1.0.2.md) and individual matrices before classifying an action as disabled.

## Accepted evidence

Use one of:

1. exact deployed config file captured from the current instance;
2. deterministic read-only runtime/config probe reporting the effective values;
3. equivalent authoritative assembled-pack evidence tied to the physical SHA-1 above.

The repository read-only collector now has a bounded route for this provider:

```bash
python docs/qa/provider-catalog-deployed-evidence-collector.py "/path/to/modpack-instance"
```

It reads only `config/simplycataclysm-startup.toml`, retains only the ten keys above, and fingerprints the exact physical JAR. A missing/incomplete key stays fail-closed; the collector never substitutes source defaults. Its bounded extraction is not a proof of all runtime branches; no collector output was obtained in this reaudited batch.

Current archived instance logs confirm that NeoForge loaded and watched `config/simplycataclysm-startup.toml`; those logs do **not** expose the values and therefore do not close this checklist by themselves.

Do not use:

- source defaults alone;
- generic publisher defaults;
- a config from another instance/world;
- client tooltip behavior as proof of server/startup state.

## Promotion rule

Once effective values are known and the relevant state/branch conditions have been reviewed:

- identities whose activation is actually established may enter the strict numerator under the catalog contract; positive chance alone does not establish activation;
- disabled identities remain provider inventory but not strict current-pack actions;
- activation/config closure requires all four to be classified without relying on source defaults or a chance0 label alone. The ✅ directory denotes semantic inventory completeness, separately from this gate.

Runtime combat QA remains separate from semantic/config closure.
