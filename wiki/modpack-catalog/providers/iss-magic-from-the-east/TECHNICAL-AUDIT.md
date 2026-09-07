# ISS: Magic From The East 1.1.5 — technical audit

## Provenance

- pack: `iss_magicfromtheeast-1.1.5.jar`;
- Notion: runtime 1.1.5;
- source: `WarPhan78/ISS_MagicFromTheEast-1.21.x@13208302c9fdf5beb171a328558cbef07a25ba46`;
- source `gradle.properties`: `mod_version=1.1.5`;
- upstream source declares Iron's `1.21.1-3.16.2`; pack uses Iron's `3.16.3`.

## Registry

Exactly **22 active spell registrations: 11 Symmetry + 11 Spirit**. Commented spell declarations (`LaunchSpell`, `QigongControllingSpell`) and commented Dune school are excluded.

Provider catalog status: **22/22**.

## School authority

`iss_magicfromtheeast:symmetry` and `iss_magicfromtheeast:spirit` are real provider schools with focus tags, power/resistance attributes, cast sounds and damage types.

## Symmetry authority map

- spell classes own initial parameter calculation;
- projectile/AoE entities own collision, cadence and final spatial settlement;
- Jiangshi/Jade Executioner/Cloud use Iron's summon ownership/lifecycle where the spell calls `SummonManager`;
- Drapes reflection is server-side `ProjectileImpactEvent` logic;
- Reversal Healing is server-side `LivingDamageEvent.Pre`;
- anti-magic removes Bagua via `AntiMagicSusceptible`;
- `CounterSpellEvent` has provider-specific summon resistance logic and explicitly unsummons Jade Drapes.

## Spirit authority map

- `SoulburnEffect` owns the provider-native max-HP-scaled `SOUL_DAMAGE` cadence;
- `ExtractedSoul` + `SoulChallengingEvents` own linked proxy damage, link break punishment and Counterspell handling;
- `AnchoredSoulEffect` owns the teleport-triggered creation of an ExtractedSoul at the old position;
- Bone Hands, Kitsunes, Spirit Samurai and Ashigaru use Iron's `SpellSummonEvent`/`SummonManager` lifecycle from their spell classes;
- Soul Skull, Phantom Cavalry, Anchoring Kunai, Splitting Shuriken and Spirit Bullet entities own collision and final hit behavior;
- Ashigaru ranged/melee composition is provider entity/AI state, not a bridge classification.

## Important config defaults

- `impermanencePercentLimit=0.2`: Impermanence/Underworld Aid cap = 20% target max HP;
- `passChallenging=false`: Counterspell by non-extractor does not safely skip Spirit Challenging by default;
- `maxSoulburnDamage=10.0`;
- `soulburnDamageScaling=5`: Soulburn amplifier-0 pulse is based on 5% target max HP before 1–10 clamp;
- `allowBlockProvidingSoulburn=true`.

Runtime pack config may override these values.

## Static-source QA findings — Symmetry

### Cloud Ride spawn offset

`spawn.add(forward.x, 0.25f, forward.z);` is called without assigning the returned immutable `Vec3`, so the intended forward/up offset does not modify `spawn`. The audited source therefore initializes the cloud at the caster position. Gameplay consequences require live QA.

### Jade Drapes idle animation

`idlePredicate` tests `isAnimatingClose() || isAnimatingClose()`, duplicating the same condition. This appears presentation-only; shield/reflection authority is server-side and separately confirmed.

### Dragon Glide public shield-break claim

The projectile class confirms travel damage, no knockback and 80-tick lifetime. A shield-break interaction was not identified in the audited spell/projectile path. Until a provider handler proves it, shield breaking remains `NÃO VERIFICADO`.

## Static-source QA findings — Spirit

### Anchoring Kunai tooltip vs event coefficient

Tooltip formula is `(level+1)×5%` = 10–45%. `AnchoredSoulEffect`, however, computes `(effectAmplifier+1)×0.5` and passes it to `ExtractedSoul.setBonusPercent`, which divides by 100. Since the projectile uses amplifier = spellLevel, the stored linked-damage coefficient is approximately **1–4.5%**. This is a one-order-of-magnitude divergence in static source and must be runtime-tested/upstream-corrected rather than silently normalized.

### Phantom Charge tooltip vs assigned entity damage

`getUniqueInfo` displays `getSpellPower()/2`, but `onCast` assigns full `getSpellPower()` to every `PhantomCavalryVisualEntity`, whose hit path applies the stored value. Static source therefore advertises 3–8 while assigning 6–16 at neutral levels 1–6.

### Soul Catalyst repeated base onCast

`SoulCatalystSpell.onCast` invokes `super.onCast(...)` inside its 2–6 projectile loop. Any observable base-class side effects from repeated invocation require runtime QA.

### Spirit Bullet ally boundary

The ranged Ashigaru projectile correctly attributes damage to the Ashigaru summoner and clears iFrames. Its local `onHitEntity` owner/alliance condition alone does not prove third-party allied-target filtering; final friendly-fire behavior depends on inherited projectile targeting and must be tested before bridge code assumes it.

## Integration rule

Provider-native first. Bridges must not duplicate Reversal Healing cancellation, Drapes projectile reflection/owner rewrite, AoE settlement, summon lifecycle, iFrame manipulation, Soulburn cadence, ExtractedSoul damage forwarding, teleport-anchor handling or projectile splitting. Any bridge around a QA finding must fail closed until runtime behavior is confirmed rather than choosing whichever conflicting tooltip/source value is more convenient.
