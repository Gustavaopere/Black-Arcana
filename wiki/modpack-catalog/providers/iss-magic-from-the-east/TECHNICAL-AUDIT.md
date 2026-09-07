# ISS: Magic From The East 1.1.5 — technical audit

## Provenance

- pack: `iss_magicfromtheeast-1.1.5.jar`;
- Notion: runtime 1.1.5;
- source: `WarPhan78/ISS_MagicFromTheEast-1.21.x@13208302c9fdf5beb171a328558cbef07a25ba46`;
- source `gradle.properties`: `mod_version=1.1.5`.

## Registry

Exactly 22 active spell registrations: 11 Symmetry + 11 Spirit. Commented spell declarations and Dune school are excluded.

## Symmetry authority map

- spell classes own initial parameter calculation;
- projectile/AoE entities own collision, cadence and final spatial settlement;
- Jiangshi/Jade Executioner/Cloud use Iron's summon ownership/lifecycle where the spell calls `SummonManager`;
- Drapes reflection is server-side `ProjectileImpactEvent` logic;
- Reversal Healing is server-side `LivingDamageEvent.Pre`;
- anti-magic removes Bagua via `AntiMagicSusceptible`;
- `CounterSpellEvent` has provider-specific summon resistance logic and explicitly unsummons Jade Drapes.

## Important config defaults

`Impermanence's Verdict` damage cap: `impermanencePercentLimit=0.2`, i.e. **20% of target max HP** by default. Runtime pack config can override this value.

## Static-source QA findings — Symmetry

### Cloud Ride spawn offset

`spawn.add(forward.x, 0.25f, forward.z);` is called without assigning the returned immutable `Vec3`, so the intended forward/up offset does not modify `spawn`. The cloud is therefore initialized at the caster position by the audited source. Gameplay consequences require live QA.

### Jade Drapes idle animation

`idlePredicate` tests `isAnimatingClose() || isAnimatingClose()`, duplicating the same condition. This appears presentation-only; shield/reflection authority is server-side and separately confirmed.

### Dragon Glide public shield-break claim

The projectile class confirms travel damage, no knockback and 80-tick lifetime. A shield-break interaction was not identified in the spell/projectile classes audited for this pass. Until a provider event/entity handler proves it, shield breaking remains `NÃO VERIFICADO` rather than copied from public prose.

## Integration rule

Provider-native first. Bridges must not duplicate Reversal Healing cancellation, reflection owner/damage rewrite, AoE damage, summon lifecycle, iFrame manipulation or missing-health scaling.
