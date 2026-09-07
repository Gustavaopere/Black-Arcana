# Vampirism Integrations 1.10.2 — Technical Audit

Source pin: `TeamLapen/VampirismIntegrations@bff02b9686408691aea2c0c910ccb712edb18bd5`.

Status: `SOURCE-LEVEL CURRENT-PACK BRIDGES AUDITED / RUNTIME QA PENDING`

## Loader architecture

`VampirismIntegrationsMod` creates one `ModCompatLoader`, registers a fixed set of `IModCompat` implementations, and delegates lifecycle steps to those compats.

The central loader:

- checks `ModList.isLoaded(targetModId)`;
- creates `enable_compat_<modid>` config entries only for targets that are present while config is built;
- validates optional Maven-style accepted version ranges;
- prepares only enabled, compatible targets;
- catches compatibility exceptions during lifecycle dispatch and unloads the failing compat instead of continuing to call it;
- exposes the resulting set through `/vampirism-integrations loaded`.

This is a **fail-soft compat loader**, not an authority-merging framework.

## Exact central registration list

Current 1.10.2 constructor registrations:

1. `VampirismCompat`
2. `BOPCompat`
3. `WailaModCompat`
4. `EvilCraftCompat`
5. `CrafttweakerCompat`
6. `TANCompat`
7. `MCACompat`
8. `ChoiceTheoremOverhauledVillage`
9. `ColdSweatCompat`
10. `GuardVillagerCompat`

Explicitly commented/non-central entries include Blood Magic, Diet, TConstruct, Survive, Better Animals/Better Animals Plus, Graveyard, Player Companion, Consecration and `JadeModCompat`.

The commented Jade entry is not evidence that Jade is inactive because the actual `JadePlugin` uses independent Jade discovery.

## Base Vampirism compatibility

`VampirismCompat` is explicitly documented by its own source as a dummy integration for Vampirism itself. It declares accepted Vampirism version range `[1.8.0,)`.

The current pack's Vampirism `1.10.13` satisfies that declared range.

This dummy compat must not be counted as a separate gameplay feature.

## Cold Sweat bridge

### Compatibility contract

- mod id: `cold_sweat`
- accepted range: `[2.2.3,)`
- installed: `2.4.2`
- enabled default: true

### Event hooks

`ColdSweatEventHandler` listens for:

- `PlayerFactionEvent.FactionLevelChanged`;
- `PlayerEvent.PlayerRespawnEvent`;
- `PlayerEvent.PlayerLoggedInEvent`.

It then reconciles transient Cold Sweat attributes against `Helper.isVampire(player)`.

### Modifier identity and idempotency

Both modifiers use the shared id:

`vampirism:vampire_modifier`

Before adding a modifier, the handler checks whether that modifier id already exists. When the player is not a Vampire, it removes that modifier.

This gives the bridge an explicit idempotency mechanism and prevents stacking its own modifier on repeated login/respawn/faction events.

### Failure behavior

Attribute access/update is wrapped in a broad `Throwable` catch. The first failure logs an error; subsequent failures are suppressed by `warnTemperature=false`.

Integration consequence: absence of a crash does **not** prove that the thermal modifier applied. Runtime validation must inspect final Cold Sweat attributes/behavior.

## Jade bridge

`JadePlugin` is annotated `@WailaPlugin` and implements `IWailaPlugin`.

This is independent of `ModCompatLoader`. The plugin registers common/server data providers and client components directly through Jade registration callbacks.

### Authority

Jade remains a read/presentation surface. Data shown by the plugin is derived from Vampirism block entities/player/entity state. The plugin must not be treated as a gameplay settlement path.

### Deduplication implication

Black Arcana should not observe Jade rendering as an event or progression signal. If a capability needs actual faction, blood, altar or machine state, query the authoritative provider/API rather than scraping or duplicating Jade data.

## Conditional data maps

The JAR contributes entries under the **Vampirism data-map namespaces**, not a parallel conversion registry.

Audited maps:

- `vampirism:entity_blood`
- `vampirism:entity_converter`
- `vampirism:fluid_blood_conversion`
- `vampirism:item_blood`

This means the integration extends provider-owned Vampirism registries/data maps when targets are present. Black Arcana must preserve those canonical conversions rather than normalizing external blood resources independently.

## Current-pack inactive source paths

The current modlist does not contain the target mods for BOP, WAILA, EvilCraft, CraftTweaker, Tough As Nails, MCA, CTOV or Guard Villagers. Therefore their Java compats are not prepared by the central loader under the audited snapshot.

Data-map targets BOP, EvilCraft, Blood Magic, TConstruct, MCA and Capybara are likewise absent and their conditional entries remain inactive.

## Jade source anomaly resolved

At first glance the main constructor's commented `JadeModCompat` can be misread as “no Jade support”. The exact source disproves that interpretation because `JadePlugin` is a separately discoverable `@WailaPlugin`. With Jade 15.10.6 installed, the plugin surface is present independently of the central loader.

This distinction is now canonical for 1.10.2.

## MineColonies source boundary

MineColonies is present in the current pack and appears in `gradle.properties`, `build.gradle` source-set/exclusion logic and deploy metadata. No MineColonies Java compat class or loader registration was found in the exact source pin.

Therefore:

- build dependency/support declaration: CONFIRMED;
- current installed MineColonies presence: CONFIRMED;
- concrete 1.10.2 runtime integration implementation: **NOT FOUND IN AUDITED SOURCE**;
- capability status: FAIL-CLOSED / DO NOT CLAIM.

## Runtime QA checklist

1. Run `/vampirism-integrations loaded` and confirm central loader reports `vampirism` and `cold_sweat` under default/current config.
2. Validate Vampire login/respawn/faction transition applies one, and only one, `vampirism:vampire_modifier` to each Cold Sweat threshold attribute.
3. Validate curing/leaving Vampire removes those modifiers.
4. Measure/inspect the effective freezing/burning thresholds in Cold Sweat 2.4.2; do not rely solely on prose labels.
5. Confirm Jade displays entity blood and player/entity faction with the installed Jade 15.10.6.
6. Validate Jade machine/altar overlays do not crash against Vampirism 1.10.13 block-entity API changes.
7. Confirm no absent conditional data-map entry logs registry/data-load errors.
8. If MineColonies integration is expected by gameplay documentation, test the installed JAR for a runtime path before promoting any capability; source alone currently does not provide one.

## Validation state

Source identity, loader topology, current active target detection, Cold Sweat semantics, Jade plugin registration and conditional blood maps are audited.

Do not mark `RUNTIME QA CONFIRMED`.