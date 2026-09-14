# Vampire Spells Addon 0.0.9 — provider catalog

## Status

`INSTALLED 0.0.9 / OFFICIAL RELEASE-SOURCE PIN / BRIDGE_COMPAT / ZERO_SEMANTIC_RELEASE_BOUNDED CANDIDATE / +0 SEMANTIC / COMPONENT #67 CANDIDATE / RUNTIME QA FAIL-CLOSED`

## Installed identity

Current sibling modlist authority at `neoforge-rpg-skilltree/main@f3637a09b1479ab8d60fa60e916f1ad539a3ab7d` records:

- provider: **Vampirism Iron's Spells Compatibility / Vampire Spells Addon**;
- mod id: `vampire_spells_addon`;
- installed filename: `vampire_spells_addon-neoforge-1.21.1-0.0.9.jar`;
- target: Minecraft 1.21.1 / NeoForge;
- catalog role: bridge between Vampirism and Iron's Spells 'n Spellbooks.

The official release `1.21.1-0.0.9` targets exact commit `xsharov/VampireSpellsAddon@2d36e94e67611a316b7311b11e4574b499025580` and publishes a NeoForge asset with the same filename. GitHub reports that release asset digest as:

`sha256:8997f71035f29e4d2fe9e37dd76ca5f4b574906d1aed0914df6c119111570fed`

The current sibling repository does not preserve an independent digest for the physical installed JAR. Therefore this catalog closure is **release/source bounded**, not a claim of independently hash-matched physical bytes.

## Semantic disposition

Exact release source inspection closes the provider-owned semantic question:

- `SpellIds` creates only `irons_spellbooks:*` identifiers: `ray_of_siphoning`, `devour`, `holy`, `angel_wing`, `fortify`, `wisp`, `haste`, `cleanse`, and `sunbeam`;
- `SpellEventHandler.register()` resolves Iron's/Vampirism bridges and installs event listeners; it does not register spells, schools or rituals;
- `BloodSpellHandler` alters cost fallback, cooldown, Devour pricing and blood restoration for existing Iron's Blood spells;
- `HolySpellHandler` alters damage/heal/utility behavior for existing Iron's Holy spells;
- the NeoForge `AbstractSpellMixin` targets `io.redspace.ironsspellbooks.api.spells.AbstractSpell` to replace the mana gate and cancel unpaid existing casts;
- the NeoForge entrypoint registers server config and then calls the integration registrar;
- the exact tree contains no provider-owned spell/ritual datapack tree or provider spell registry; shared magic assets are localization overrides under `assets/irons_spellbooks/lang`.

Accordingly:

`BRIDGE_COMPAT / ZERO_SEMANTIC_RELEASE_BOUNDED` / semantic delta **+0**.

The addon changes behavior and resource settlement of parent-owned spell identities. Those Iron's spell identities must not be duplicated as Vampire Spells Addon spells.

## Authority boundary

Iron's Spells remains authority for the referenced spell identities, schools and host casting semantics. Vampirism remains authority for vampire state and blood. Vampire Spells Addon owns only its compatibility policy and bridge behavior between those parent systems.

Black Arcana must not treat this addon as a spell provider merely because it reacts to spell events. No Black Arcana runtime adapter is promoted by this catalog audit.

## Component accounting

Canonical shared state before Phase 2BT is:

- strict reconstructible semantic minimum: **1344**;
- provider-component coverage: **66/100**;
- global semantic denominator: incomplete; no spell/magic percentage declared.

This evidence tranche makes `vampire_spells_addon` eligible for technical component **#67** with semantic **+0**, but component #67 is not canonical until durable merge, exact-SHA CI and shared-ledger reconciliation complete.

## Runtime QA boundary

Still fail-closed:

- independent physical-JAR digest equivalence to the official release asset;
- assembled-pack client/dedicated-server loading with the installed exact parent stack;
- effective serverconfig values;
- reflective contract resolution against the installed Iron's/Vampirism builds;
- mixin application and event-order behavior in the assembled pack;
- blood/mana atomicity, cooldown and damage/heal behavior under live multiplayer;
- duplicate processing with other Vampirism/Iron's compatibility layers;
- any Black Arcana runtime bridge.

These runtime gates do not create additional semantic identities.

## Provenance / clean-room

Evidence is limited to public release metadata and narrow source inspection of the exact release commit: identifiers, registration shape, class roles, resource paths and authority boundaries. No third-party implementation body or asset is copied into Black Arcana.