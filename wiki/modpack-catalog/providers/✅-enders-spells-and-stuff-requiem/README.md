# Ender's Spells and Stuff: Requiem — 0.1.7

Status: `✅ CATALOGED / PHYSICAL 0.1.7 SHA-PINNED / EXACT 0.1.7 SOURCE-PINNED / 58 REGISTERED ROOTS / 53 STRICT SEMANTIC ACTIONS / 5 TECHNICAL-RESIDUAL ROOTS EXCLUDED / RUNTIME QA FAIL-CLOSED`

## Current physical identity

Current sibling authority:

`neoforge-rpg-skilltree@8f8fdc761320869fb369846ee57aee1bff20ae3e`

Certified dossier:

`PROJECT-INSTRUCTIONS/modlist/Addons/✅-enders-spells-and-stuff-requiem v0.1.7.md`

Physical identity:

- order: #265 in the current dossier checkpoint;
- JAR: `ess_requiem-0.1.7.jar`;
- mod id: `ess_requiem`;
- runtime: `0.1.7`;
- Minecraft 1.21.1 / NeoForge;
- physical SHA-1: `c4648cced4f9e96527cfa4e3f5edcdcead43abb1`;
- Iron's Spells 3.16.3, Ace's Spell Utils 1.2.7.2 and Apothic Attributes 2.10.1 are present;
- Discerning The Eldritch 1.4.4 is present, so the provider's DTE registration branch is active in the current physical set.

## Publisher release

CurseForge project: `1336977`.

Current release:

- file ID: `8762149`;
- filename: `ess_requiem-0.1.7.jar`;
- release date: 2026-08-29;
- NeoForge 1.21.1;
- Client & Server;
- All Rights Reserved.

The publisher page says "42 (+2) spells", but the same page text and the exact 0.1.7 source expose a broader current action surface. The marketing number is therefore preserved as publisher provenance, **not** substituted for the exact source registry.

## Exact source pin

Official repository:

`EnderTheNerd/ESS-Requiem`

Exact release-correlated pin:

`04ab715d657368b177267a8df196c32329acf3f6`

This commit is particularly strong source evidence because it changes:

`mod_version=0.1.6a -> mod_version=0.1.7`

while also enabling the Gong registration and carrying the 0.1.7 fixes.

Exact source surfaces:

- `GGSpellRegistry`: **55** unconditional base registrations;
- `DTESpellRegistry`: **3** registrations behind the DTE-loaded branch;
- current English localization: **58** distinct `spell.ess_requiem.<id>` roots, one-to-one with the 58 registered roots;
- current physical pack includes DTE, so all three DTE registry entries belong to the present registry surface.

Physical-JAR byte equality to a locally reproduced source build is **not** claimed. Evidence state is therefore `COUNTED_SOURCE_PINNED`, not `COUNTED_EXACT`.

## Semantic reconciliation

The semantic metric counts provider-owned player-facing spells/actions and excludes implementation-only, proxy, residual or summon-AI sub-actions.

Current disposition:

- registered roots: **58**;
- strict semantic actions: **53**;
- excluded technical/residual roots: **5**.

Excluded:

1. `arm_of_decay_insta_raise_strong`;
2. `arm_of_decay_insta_raise_weak`;
3. `finality_of_decay`;
4. `gild_summon`;
5. `nightmare_scream`.

Why:

- the two Arm-of-Decay roots are mutually exclusive implementation branches of the same automatic weapon passive trigger rather than independent player-selectable actions;
- the provider's 0.1.2 changelog states that Field of Mourning replaced Finality of Decay; exact 0.1.7 source still registers Finality, but it is uncraftable/unlootable and the current Arm of Decay holder uses Field of Mourning / Corpse Explosion / Decaying Will instead;
- `gild_summon` is an AI sub-action of the player-owned Battle Standard summon;
- `nightmare_scream` is a single-use AI spell of the Nightmare summon.

Conversely, the three Cataphract action roots are counted because exact source routes them from direct player events while Ebony Cataphract is active. `slashing_ability` is also counted because exact source invokes it from a player combat-combo event, not only from summon AI.

Strict semantic contribution:

**+53 `COUNTED_SOURCE_PINNED`**

See `SOURCE-0.1.7-SPELL-INVENTORY.md`.

## Reachability evidence

Exact source closes the important non-default paths:

- Arm of Decay embeds Field of Mourning, Corpse Explosion and Decaying Will;
- the provider summon spellbook embeds Vessel Skeleton;
- Eldritch weapons/curio embed Ebony Cataphract, Night Veil and Damnation;
- Holy weapon Hope embeds Bastion of Light and Overwhelming Light;
- Scythe of Frozen Dreams embeds Glacial Sculpting and Lord of the Final Frost;
- Spellblade weapons embed Dismantle, Cleave and Malevolent Slashing;
- Requiem Staff embeds Blood Domain;
- Dream Ripper embeds DTE spells Forever Dreaming and Nightmare;
- `ess_requiem:blade` uses `#ess_requiem:blade_focus`;
- that focus contains `ess_requiem:emboldened_ingot`, and source provides the relevant recipes.

## Authority boundary

Iron's Spells owns the host registry, casting/mana/cooldown framework and base schools.

Requiem owns:

- its 58 registered source roots;
- its 53 catalog-counted semantic actions;
- its custom Spellblade school;
- its weapons/spellbooks/curios;
- its summons/effects and provider-specific event behavior.

DTE owns its own Eldritch provider content; Requiem owns only its DTE-conditioned addon spell registrations.

Black Arcana must not duplicate provider mana debit, cooldown settlement, summon lifecycle, max-health modifiers, weapon-exclusive spell state or event-triggered combo settlement.

## Runtime QA remains fail-closed

Catalog closure does not prove:

- installed JAR ↔ source-build byte equality;
- current-host 3.16.3 numerical/config compatibility (source build file references an older Iron's development coordinate);
- deployed Iron's per-spell overrides;
- weapon-exclusive cast persistence;
- Strain max-HP lifecycle;
- summon death/despawn exactly-once behavior;
- DTE extras after reload/restart;
- multiplayer attribution;
- Apothic Attribute stacking;
- full-pack dedicated-server/client behavior.

## Result

**✅ Cataloged.**

The current physical provider is 0.1.7, its exact release-correlated source registry contains 58 roots, and 53 provider-owned player-facing semantic actions are reconstructible under the Black Arcana metric.

Strict semantic delta: **+53**.
