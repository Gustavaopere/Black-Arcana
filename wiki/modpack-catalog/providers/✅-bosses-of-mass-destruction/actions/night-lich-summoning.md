# Night Lich Summoning

- Provider: **Bosses of Mass Destruction** (`bosses_of_mass_destruction`)
- Version: `1.3.3`
- Exact physical/publisher SHA-1: `446ff63afb858ad49149d24b72541739de83d38d`
- Setup/owner item: **Soul Star**
- Provider target: Chiseled Stone Altar network
- Semantic type: deliberate boss-summoning action
- State: `CONDITIONAL`

## Identity and trigger

`SoulStarItem.useOn` recognizes the provider's Chiseled Stone Altar setup. The deliberate semantic root is placing/using Soul Stars on the altar network to complete the provider summon arrangement.

The separate Soul Star `use` branch that launches a locator toward the Lich tower is navigation and is excluded from this action identity.

## Settlement

Exact artifact evidence closes that the provider:

- consumes/uses the Soul Star on the altar path;
- marks the relevant altar state as lit/filled;
- schedules Night Lich spawning once the required altar arrangement is satisfied.

Altar visuals, scheduler phases and resulting boss AI are downstream of this root.

## Config and production gate

Exact `LichConfig$SummonMechanic` bytecode exposes:

- `isEnabled` binary default: **true**;
- `numEntitiesKilledToDropSoulStar` binary default: **50**.

The provider's death-event handling reads `summonMechanic.isEnabled` before Soul Star progress/drop behavior.

The effective deployed value of `lichConfig.summonMechanic.isEnabled` is not captured. The source/binary default is not substituted for deployed state.

## Reachability disposition

The action identity and provider settlement are exact-current, but normal Soul Star production remains configuration-conditioned.

Therefore this root remains `CONDITIONAL` and contributes **+0 additional strict** until deployed config evidence closes the gate.

## Evidence boundary

Do not infer that the current world uses the binary default. The folder can remain ✅ cataloged while this individual action stays outside the strict numerator.

Source: `../EXACT-1.3.3-ARTIFACT-AUDIT.md`.
