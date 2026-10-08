# T.O Magic n' Extras — current-host default-enabled checkpoint

Status: `EXACT FILE-6342780 CLASS PROBE + CURRENT IRON'S 3.16.3 SOURCE PIN / 21 HOST-DEFAULT CRAFTABLE+ENABLED / EFFECTIVE CONFIG CONDITIONAL / CURRENT PHYSICAL UNPROVEN`

## Scope

This checkpoint closes the **default `enabled` gate** for the same 21 exact File `6342780` registrations already classified as host-default craftable.

It does not prove effective server/datapack configuration, player-specific Scroll Forge eligibility, unconditional survival acquisition, or equality with current physical Traveloptics SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`.

## Exact Traveloptics probe

Authority:

- CurseForge project/file: `1046916 / 6342780`;
- exact publisher SHA-1: `3808493ce45cdfeb6408e85578adecf13df698e8`;
- temporary NON-MERGE PR: **#651**;
- audit HEAD: `1899c862e2b422fbde3638fc4e752aec39172e3c`;
- dedicated workflow: `Traveloptics Scroll Forge Default Gates Clean-room Audit`;
- workflow run: **37335314647** — `SUCCESS`;
- job: **111848490451** — `SUCCESS`;
- text-only artifact: **11355503614**;
- artifact digest: `sha256:df4f51a887bd9532b3fd6bad1a40341506100022914797274a0cdddad4a42e6b`.

The audit located these 21 concrete classes by exact class-entry identity:

- `BloodHowlSpell`;
- `PsychicBoltSpell`;
- `ReversalSpell`;
- `SpectralBlinkSpell`;
- `OrbitalVoidSpell`;
- `CursedMinefieldSpell`;
- `VoidEruptionSpell`;
- `VortexPunchSpell`;
- `AstralSenseSpell`;
- `AshenBreathSpell`;
- `LingeringStrainSpell`;
- `MeteorStormSpell`;
- `LavaBombSpell`;
- `NullflareSpell`;
- `CursedRevenantsSpell`;
- `DespairSpell`;
- `RapidLaserSpell`;
- `DeathLaserSpell`;
- `EmPulse`;
- `AerialCollapseSpell`;
- `SteleCascadeSpell`.

For each target it retained only bounded class/config-gate facts. Results:

- target rows: **21**;
- direct `DefaultConfig.setDeprecated(...)` calls: **0/21**;
- direct `DefaultConfig.enabled` writes: **0**;
- concrete `isEnabled()` overrides: **0/21**;
- concrete `canBeCraftedBy(Player)` overrides: **0/21**;
- provider class entries scanned for direct enabled-default mutators: **250**;
- provider classes with a direct `setDeprecated` reference or direct `enabled` field write: **0**.

No method bodies, source reconstruction, assets, localization prose or JAR bytes are retained.

## Current Iron's 3.16.3 host contract

Current physical host authority:

- JAR: `irons_spellbooks-1.21.1-3.16.3.jar`;
- SHA-1: `017fd8140c477f9ae602cf95594f1c23bef1d6e3`;
- exact public source pin: `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`.

At that exact source pin:

- `DefaultConfig.enabled` initializes to **true**;
- `DefaultConfig.setDeprecated(boolean deprecated)` assigns `enabled = !deprecated`;
- `SpellConfigParameter.ENABLED` has generic default **true**;
- `SpellConfigManager` seeds each spell's default `ENABLED` value from `spell.getDefaultConfig().enabled`;
- `AbstractSpell.isEnabled()` resolves the active `SpellConfigParameter.ENABLED`;
- Scroll Forge recipe enumeration requires `spell.isEnabled() && spell.allowCrafting()`;
- `AbstractSpell.canBeCraftedBy(player)` adds the learning condition when the school requires learning.

The same host manager also allows per-spell/datapack/global configuration and `ModifyDefaultConfigValuesEvent` mutation. Therefore default enabled is not effective deployed enabled.

## Conclusion for the 21 registrations

Combining exact File `6342780` provider evidence with current Iron's 3.16.3 host semantics:

- provider default `enabled`: **true**;
- provider default `allowCrafting`: **true**;
- concrete provider `isEnabled()` override: **none**;
- concrete provider `canBeCraftedBy(Player)` override: **none**;
- default Scroll Forge host gates `enabled && allowCrafting`: **satisfied at the publisher+host default layer**.

Canonical classification:

`HOST/PUBLISHER-DEFAULT CRAFTABLE + ENABLED / EFFECTIVE SCROLL-FORGE ELIGIBILITY CONDITIONAL`.

## Remaining conditions

This does **not** establish effective eligibility because:

- per-spell/server/datapack/global config can override `enabled`;
- effective `allow_crafting` can be overridden;
- `ModifyDefaultConfigValuesEvent` can mutate host defaults;
- focus/school compatibility remains required;
- player learning may still gate `canBeCraftedBy(player)`;
- current physical Traveloptics `7b74816e...` is not byte-proven equal to File `6342780`.

No strict current-physical semantic contribution changes. Traveloptics remains **⚠️ partial / conditioned / strict +0**.
