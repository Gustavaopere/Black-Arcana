# Create: Wizardry — 1.21.1-0.5.1-pre1

Status: `SOURCE-PINNED CURRENT PHYSICAL COMPONENT / CREATE↔IRON'S MAGIC AUTOMATION / ZERO PROVIDER-OWNED SPELL IDENTITIES / +0 SEMANTIC / RUNTIME QA FAIL-CLOSED`

## Current physical identity

The current sibling physical authority at `neoforge-rpg-skilltree@4767f5c637c02c6d91ccb43a86ea1539f42a2e9b` certifies:

- physical order: **#166**;
- JAR: `create_wizardry-1.21.1-0.5.1-pre1.jar`;
- mod id: `create_wizardry`;
- runtime version: `1.21.1-0.5.1-pre1`;
- Minecraft: 1.21.1;
- role: Create ↔ Iron's Spells 'n Spellbooks integration / magic automation.

The sibling dossier does not preserve an independent installed-JAR hash for this row. Physical-JAR ↔ source-build byte equality is therefore **not** claimed.

## Exact public source checkpoint

Official public repository:

`TTZPlayz/Create-Wizardry@9c4e53aad0ee9477187487443b597b77ef06f323`

The commit is `CW 0.5.1 - Pre-Release 1`. Its `gradle.properties` declares:

- `mod_id=create_wizardry`;
- `mod_version=1.21.1-0.5.1-pre1`;
- Minecraft 1.21.1;
- Iron's development dependency 1.21.1-3.16.1;
- Create development range `(6.0.6, 6.0.10]`;
- `mod_license=All Rights Reserved`.

This is a version-correlated source pin, not a reproducibility claim for the installed JAR.

## Semantic spell disposition

The exact source checkpoint was inspected specifically for provider-owned spell identity surfaces.

Observed:

- **75** Java source files;
- **328** files under `src/main/resources/`;
- **0** provider spell resource paths under the `create_wizardry` namespace;
- no `registerSpell` surface found;
- no `SpellRegistry` surface found;
- no `DeferredRegister<AbstractSpell>` surface found;
- no `Registries.SPELL` surface found;
- no `SPELLS.register` surface found;
- no `spell.create_wizardry.*` localization/identity namespace found.

The main mod entrypoint registers provider fluids, blocks, block entities, items, mob effects, particles, creative tabs, triggers and advancements. It does **not** register a provider-owned Iron's spell registry.

Therefore:

`ZERO_SEMANTIC_HOST_SPELL_AUTOMATION`

Create: Wizardry contributes **+0 independent semantic spell identities** to the Black Arcana catalog.

## Host-spell automation is not new spell ownership

Create: Wizardry does consume and execute Iron's spell objects.

The current source includes:

- Blaze Caster logic using Iron's `SpellData` and `AbstractSpell`;
- direct invocation of the selected host spell's cast path using Iron's `CastSource.MOB`;
- Mana Siphon logic that reads Iron's spell containers and manipulates mana/spellcasting state;
- a `SpellPreCastEvent` policy that blocks depleted players from casting;
- a mixin over Iron's spell-casting mobs to suppress casts while siphoned.

These are automation, delivery and policy surfaces over host-owned spell identities. They do not mint `create_wizardry:<spell>` identities and must not duplicate Iron's spell count.

## Blaze Caster host blacklist

The exact source checkpoint explicitly blacklists **31 host spell path names** from Blaze Caster use:

- melee/contact: `echoing_strikes`, `flaming_strike`, `shadow_slash`, `volt_strike`, `divine_smite`, `touch_dig`, `heartstop`, `wall_of_fire`;
- movement: `teleport`, `recall`, `blood_step`, `frost_step`, `burning_dash`, `thunder_step`, `evasion`, `charge`, `ascension`, `angel_wing`, `portal`;
- inventory/summon utility: `summon_ender_chest`, `summon_horse`, `summon_polar_bear`;
- self effects: `sacrifice`, `invisibility`, `haste`, `spider_aspect`;
- healing/support: `heal`, `greater_heal`, `ice_tomb`, `healing_circle`, `fortify`.

This list is a provider-owned compatibility policy for an automation surface. It is **not** a new 31-spell registry and is not counted semantically here.

## Other provider-owned magic surfaces

Create: Wizardry owns magic-adjacent integration content, including:

- Mana Siphon;
- Blaze Caster;
- Channeler;
- Liquid Mana and arcane fluid transport;
- Arcane Essence processing;
- ink/material automation;
- provider blocks/items;
- two provider mob effects: `create_wizardry:mana_depletion` and `create_wizardry:siphon_lock`.

Those status effects and machines remain catalog-relevant for interoperability and deduplication, but they are not independent spell/glyph/ritual identities under the current semantic metric.

## Authority boundary

- **Iron's Spells 'n Spellbooks** owns spell identities, schools, base casting, mana contracts, cooldowns and spell resolution.
- **Create** owns kinetic/process infrastructure.
- **Create: Wizardry** owns its automation blocks, resource conversion/transport, host-spell automation policy and associated integration behavior.
- **Black Arcana** must not create a second spell identity or a second settlement path merely because Wizardry can mechanically cast an Iron's spell.
- **RPG Skill Tree** remains progression/Mastery/perk authority through verified contracts only.

## Clean-room / license boundary

The exact source metadata declares All Rights Reserved. The GitHub repository metadata does not provide a standard SPDX license assertion. This catalog therefore uses public source only for factual catalog/interoperability evidence: identity, registry shape, ownership boundaries and observable integration surfaces.

No implementation body, asset, recipe, model, localization prose or formula is copied into Black Arcana.

## Runtime QA boundary

Still fail-closed until the exact assembled pack is directly exercised:

- installed-JAR hash equality to the public source build;
- dedicated-server/client boot with the current physical Create and Iron's stack;
- effective provider config;
- Blaze Caster spell selection and blacklist behavior against all installed Iron's addons;
- exactly-once mana/cooldown/effect settlement for automated casts;
- caster/owner attribution and protection behavior;
- summoned/projectile ownership from automated casts;
- Mana Siphon drain/refund/transformation behavior;
- Liquid Mana transport and loss/duplication behavior;
- reload/restart/chunk lifecycle;
- multiplayer concurrency;
- progression/economy impact of automated inks and magical materials.

Catalog closure does not imply runtime compatibility PASS.

## Result

**✅ Cataloged as a current magic-relevant integration component with 0 provider-owned spell identities.**

Semantic delta: **+0**. The current strict semantic minimum is unchanged by this provider.
