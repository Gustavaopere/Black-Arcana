# Hazen N Stuff 1.4.0.14 — canonical spell cards

Status: `✅ CATALOGED / 38 OF 38 ACTIVE SPELLS MATERIALIZED / COUNTED_SOURCE_PINNED / +38 STRICT / RUNTIME QA SEPARATE`

This index materializes the complete source-pinned spell registry for `Hazentouvel/Hazen_N_Stuff@5fcaf39cf399609f6c1c87d14f8d4807098c9cce`.

## Complete active spell set — 38/38

- [Endraconic Meteor](spells/endraconic-meteor.md) — `hazennstuff:endraconic_meteor` — Ender — Iron's
- [Violent Regurgitation](spells/violent-regurgitation.md) — `hazennstuff:violent_regurgitation` — Blood — Iron's
- [Bone Bolt](spells/bone-bolt.md) — `hazennstuff:bone_bolt` — Blood — Iron's
- [Soul Flaming Strike](spells/soul-flaming-strike.md) — `hazennstuff:soul_flaming_strike` — Fire — Iron's
- [Soul Flame Bolt](spells/soul-flame-bolt.md) — `hazennstuff:soul_flame_bolt` — Fire — Iron's
- [Cinderous Step](spells/cinderous-step.md) — `hazennstuff:cinderous_step` — Fire — Iron's
- [Scorching Slash](spells/scorching-slash.md) — `hazennstuff:scorching_slash` — Fire — Iron's
- [Fiery Dagger](spells/fiery-dagger.md) — `hazennstuff:fiery_dagger` — Fire — Iron's
- [Ice Arrow](spells/ice-arrow.md) — `hazennstuff:ice_arrow` — Ice — Iron's
- [Hailstorm](spells/hailstorm.md) — `hazennstuff:hailstorm` — Ice — Iron's
- [Energy Burst](spells/energy-burst.md) — `hazennstuff:energy_burst` — Lightning — Iron's
- [Ionic Slash](spells/ionic-slash.md) — `hazennstuff:ionic_slash` — Lightning — Iron's
- [Dazzling Obliteration](spells/dazzling-obliteration.md) — `hazennstuff:dazzling_obliteration` — Lightning — Iron's
- [Thorn Chakram](spells/thorn-chakram.md) — `hazennstuff:thorn_chakram` — Nature — Iron's
- [Spider Lily Counterspell](spells/counterspell-spider-lily.md) — `hazennstuff:counterspell_spider_lily` — Nature — Iron's
- [Shard Sword](spells/shard-sword.md) — `hazennstuff:shard_sword` — Nature — Iron's
- [Death Sentence](spells/death-sentence.md) — `hazennstuff:death_sentence` — Nature — Iron's
- [Spectral Axe](spells/spectral-axe.md) — `hazennstuff:spectral_axe` — Evocation — Iron's
- [Parry](spells/parry.md) — `hazennstuff:parry` — Evocation — Iron's
- [Golden Shower](spells/golden-shower.md) — `hazennstuff:golden_shower` — Holy — Iron's
- [Syringe Barrage](spells/syringe-barrage.md) — `hazennstuff:syringe_barrage` — Radiance — HazentouveLib
- [Terraprismic Barrage](spells/terraprismic-barrage.md) — `hazennstuff:terraprismic_barrage` — Radiance — HazentouveLib
- [Call Forth Terraprisma](spells/call-forth-terraprisma.md) — `hazennstuff:call_forth_terraprisma` — Radiance — HazentouveLib
- [Prismatic Shift](spells/prismatic-shift.md) — `hazennstuff:prismatic_shift` — Radiance — HazentouveLib
- [Night's Edge Strike](spells/nights-edge-strike.md) — `hazennstuff:nights_edge_strike` — Shadow — HazentouveLib
- [Umbrashift Barrage](spells/umbrashift-barrage.md) — `hazennstuff:umbrashift_barrage` — Shadow — HazentouveLib
- [Shadow Reaver](spells/shadow-reaver.md) — `hazennstuff:shadow_reaver` — Shadow — HazentouveLib
- [Arcane Cards](spells/arcane-cards.md) — `hazennstuff:arcane_cards` — Shadow — HazentouveLib
- [Soul Seekers](spells/soul-seekers.md) — `hazennstuff:soul_seekers` — Eldritch — Iron's
- [Shooting Star](spells/shooting-star.md) — `hazennstuff:shooting_star` — Cosmic — HazentouveLib
- [Cosmic Bolt](spells/cosmic-bolt.md) — `hazennstuff:cosmic_bolt` — Cosmic — HazentouveLib
- [Evercomet Barrage](spells/evercomet-barrage.md) — `hazennstuff:evercomet_barrage` — Cosmic — HazentouveLib
- [Moonkissed](spells/moonkissed.md) — `hazennstuff:moonkissed` — Cosmic — HazentouveLib
- [Hydrobullet](spells/hydrobullet.md) — `hazennstuff:hydrobullet` — Hydro — Ace's Spell Utils
- [Water Bolt](spells/water-bolt.md) — `hazennstuff:water_bolt` — Hydro — Ace's Spell Utils
- [Razorblade Typhoon](spells/razorblade-typhoon.md) — `hazennstuff:razorblade_typhoon` — Hydro — Ace's Spell Utils
- [Trident Jetstream](spells/trident-jetstream.md) — `hazennstuff:trident_jetstream` — Hydro — Ace's Spell Utils
- [Horn Shell](spells/horn-shell.md) — `hazennstuff:horn_shell` — Hydro — Ace's Spell Utils

## Registry closure

- physical provider: `hazennstuff-1.4.0.14.jar`, mod id `hazennstuff`, runtime `1.4.0.14`, SHA-1 `3be20bacb44c1923348ab6f61b685eec6aacfdcd`;
- exact version-correlated source pin: `Hazentouvel/Hazen_N_Stuff@5fcaf39cf399609f6c1c87d14f8d4807098c9cce`;
- exact release registry contains **38 active** provider spell registrations;
- registry class contains no active provider-side conditional-registration branch, `ModList` gate or config reference;
- the apparent extra `registerSpell(...)` occurrences in raw text are the helper declaration and the commented-out Reign of Tyros line, not active identities.

## Special player craft gates — 3

- `hazennstuff:golden_shower` — Golden Shower Spellbook inventory gate; provider recipe closes the source-level survival path.
- `hazennstuff:nights_edge_strike` — Night's Edge / True Night's Edge inventory gate; provider recipe closes the source-level survival path.
- `hazennstuff:scorching_slash` — Raven's Bane inventory gate; provider recipe closes the source-level survival path.

The other 35 registrations use the inspected host/default craftability/enabled-state contract at provider source level.

## Focus / school reachability

- Fire / Iron's: `irons_spellbooks:fire_focus` <- `hazennstuff:charred_bones`;
- Nature / Iron's: `irons_spellbooks:nature_focus` <- `hazennstuff:overgrown_bone`;
- Hydro / Ace's Spell Utils: `aces_spell_utils:hydro_focus` <- `hazennstuff:arcane_sea_shell`;
- Cosmic / HazentouveLib: `hazentouvelib:focus/cosmic_focus` <- `hazennstuff:stardust`;
- Radiance / HazentouveLib: `hazentouvelib:focus/radiance_focus` <- `hazennstuff:glowing_mushroom`;
- Shadow / HazentouveLib: `hazentouvelib:focus/shadow_focus` <- `hazennstuff:shadow_scale`, `hazennstuff:nightmare_fuel`.

These relationships close catalog-level reachability, not deployed runtime/config behavior.

## Explicit exclusions — +0

- `hazennstuff:brimstone_hellblast` — localization-only;
- `hazennstuff:reign_of_tyros` — class/localization present, exact release registration line commented out;
- `hazennstuff:supernova` — localization-only;
- later-branch content such as `coruscated_discharge` — not projected backward into 1.4.0.14;
- schools, focuses, spell containers, projectiles, effects and provider equipment — support/implementation surfaces, not additional spell identities.

## Authority boundary

Iron's owns host registry/casting/mana/cooldown and generic Scroll Forge/focus behavior. HazentouveLib owns shared Radiance/Shadow/Cosmic school infrastructure. Ace's Spell Utils owns Hydro school/focus infrastructure. Hazen N Stuff owns the 38 `hazennstuff` spell identities and provider-local behavior. Black Arcana does not replay provider settlement or invent parallel school/resource authority.

Sources: [SOURCE-1.4.0.14-SPELL-INVENTORY.md](SOURCE-1.4.0.14-SPELL-INVENTORY.md) and [README.md](README.md).
