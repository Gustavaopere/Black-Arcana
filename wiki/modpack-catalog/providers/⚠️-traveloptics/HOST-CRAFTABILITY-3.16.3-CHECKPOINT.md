# T.O Magic n' Extras — current-host craftability checkpoint

Status: `EXACT ALPHA CLASS PROBE + CURRENT IRON'S 3.16.3 SOURCE PIN / DEFAULT CRAFTABILITY + ENABLED CLOSED FOR 21 / EFFECTIVE CONFIG CONDITIONAL / SURVIVAL REACHABILITY NOT CLOSED`

## Scope

This checkpoint narrows the craftability state of the **21** exact Traveloptics File `6342780` registrations that are outside the already-audited provider base groups:

- 10 `AbstractUniqueSpell` registrations — exact provider gate `allowCrafting() = false`;
- 2 `AbstractWeaponSpell` registrations — exact provider gate `allowCrafting() = true`;
- 21 remaining registrations — no provider-owned `allowCrafting`, `isEnabled` or `canBeCraftedBy` override had been found, but their concrete `DefaultConfig` craftability value still needed a bounded audit.

This document closes only that last **default craftability** question. It does not prove complete survival acquisition.

## Exact Traveloptics probe

Authority:

- CurseForge project/file: `1046916 / 6342780`;
- exact alpha SHA-1: `3808493ce45cdfeb6408e85578adecf13df698e8`;
- temporary NON-MERGE audit PR: **#588**;
- audit HEAD: `e88a3dd0b5b432419b5d5ab4ab1cbb58e505aa2a`;
- workflow run: `37211969636` — **SUCCESS**;
- text-only artifact: `11306474344`;
- artifact digest: `sha256:68603e34a3cc337f08d2dc7d490ac1b5b16f5683704ea720375278b2e40f5ce1`.

The audit located each of the 21 concrete classes by exact class entry name and inspected bytecode transiently for both direct `DefaultConfig.setAllowCrafting(boolean)` calls and direct writes to `DefaultConfig.allowCrafting`. It also scanned the 223 top-level provider-owned classes for any direct setter reference or direct field write. Only class identity and bounded mutator counts were retained.

Result:

- rows: **21**;
- direct `setAllowCrafting(false)`: **0**;
- direct `setAllowCrafting(true)`: **0**;
- direct setter absent: **21**;
- unresolved/dynamic setter arguments: **0**;
- direct `DefaultConfig.allowCrafting` field writes in the 21 target classes: **0**;
- provider-owned top-level classes scanned: **223**;
- provider classes with any direct craftability setter reference or direct field write: **0**.

No method bodies, source reconstruction, assets, localization prose or binary content are retained.

## Current Iron's host contract

Current physical modlist authority records:

- JAR: `irons_spellbooks-1.21.1-3.16.3.jar`;
- mod id: `irons_spellbooks`;
- runtime version: `1.21.1-3.16.3`;
- physical SHA-1: `017fd8140c477f9ae602cf95594f1c23bef1d6e3`.

The exact public source line for that runtime is pinned at:

- repository: `iron431/irons-spells-n-spellbooks`;
- source commit: `e4056af90302d37eb1739f5ff05020b020e6e252`;
- `gradle.properties`: `mod_version=1.21.1-3.16.3`, Minecraft `1.21.1`.

Relevant host facts at that pin:

- `DefaultConfig.allowCrafting` initializes to **true**;
- `SpellConfigParameter.ALLOW_CRAFTING` has generic default **true**;
- `AbstractSpell.allowCrafting()` resolves `SpellConfigParameter.ALLOW_CRAFTING` through `SpellConfigManager`;
- `DefaultConfig.enabled` initializes to **true** and `setDeprecated(true)` changes it to false;
- `SpellConfigParameter.ENABLED` has generic default **true**;
- `AbstractSpell.canBeCraftedBy(player)` still applies the spell-learning condition when `requiresLearning()` is active;
- `AbstractSpell.isEnabled()` resolves the active `SpellConfigParameter.ENABLED`.

A follow-up exact-alpha probe in NON-MERGE PR **#651** closes the provider-default `enabled` side for these same 21 classes: **0/21** direct `setDeprecated(...)` calls, **0** direct `DefaultConfig.enabled` writes, **0/21** concrete `isEnabled()` overrides and **0/21** concrete `canBeCraftedBy(Player)` overrides. A provider-wide scan of **250** class entries found **0** direct enabled-default mutators. Dedicated run `37335314647` / job `111848490451` succeeded; text-only artifact `11355503614`, digest `sha256:df4f51a887bd9532b3fd6bad1a40341506100022914797274a0cdddad4a42e6b`. See [`HOST-ENABLED-3.16.3-CHECKPOINT.md`](HOST-ENABLED-3.16.3-CHECKPOINT.md).

## Catalog conclusion

For the **21** exact registrations covered by this probe:

**host-default craftability = true and publisher/host-default enabled = true under the current Iron's 3.16.3 contract**, because the provider concrete classes do not set a different `DefaultConfig.allowCrafting` or `DefaultConfig.enabled` value and do not override `isEnabled()` / `canBeCraftedBy(Player)`. These are default-layer facts, not effective deployed config.

This is deliberately narrower than “survival obtainable”:

- effective server/datapack spell config may override `allow_crafting`;
- effective `isEnabled()` remains config-resolved even though its provider/host default is now proven true; Scroll Forge recipe generation requires both active `isEnabled()` and active `allowCrafting()`;
- the Scroll Forge menu additionally depends on a compatible focus/school path;
- player-specific learning may still make `canBeCraftedBy(player)` false where applicable;
- a host-default-craftable spell may still require resources/progression not audited here;
- current physical Traveloptics SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4` is not proven byte-equal to File `6342780`.

Therefore the catalog may classify these 21 cards as **`HOST/PUBLISHER-DEFAULT CRAFTABLE + ENABLED / EFFECTIVE ELIGIBILITY CONDITIONAL`**. This does not establish effective Scroll Forge eligibility or unconditional survival reachability.

## Aggregate gate classification

Across the 33 exact publisher-baseline registrations:

- **21** — host/publisher-default craftable **and enabled** under current Iron's 3.16.3; effective Scroll Forge eligibility remains conditioned by active config/focus/player gates;
- **2** — provider Weapon gate explicitly `allowCrafting=true`;
- **10** — provider Unique gate explicitly `allowCrafting=false`;
  - **9** of those 10 have exact structured loot anchors;
  - `traveloptics:blackout` remains the unresolved object-level acquisition exception.

The provider therefore remains **⚠️ partial/conditioned** and contributes **+0 strict** for the current physical artifact.
