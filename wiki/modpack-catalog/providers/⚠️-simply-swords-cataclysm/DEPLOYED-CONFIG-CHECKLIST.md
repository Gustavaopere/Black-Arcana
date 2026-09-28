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
| Mecha Smite | `mechaSmiteHarmfulEffectsChance`, `mechaSmiteRegenChance`, regeneration threshold mode/value | classify active if provider behavior remains causally reachable; do not collapse harmful and regenerative branches |

Also retain the exact source-config context for durations/amplifiers/cooldown as runtime/balance evidence, but those values do not create extra semantic identities.

## Accepted evidence

Use one of:

1. exact deployed config file captured from the current instance;
2. deterministic read-only runtime/config probe reporting the effective values;
3. equivalent authoritative assembled-pack evidence tied to the physical SHA-1 above.

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
