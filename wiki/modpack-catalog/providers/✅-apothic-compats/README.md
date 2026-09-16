# Apothic Compats — 0.2.4.2

Status: `EXACT PHYSICAL ARTIFACT + EXACT 0.2.4.2 OFFICIAL SOURCE / APOTHEOSIS COMPAT DATAPACK+RUNTIME HELPERS / ARS NOUVEAU+MALUM MAGIC-ADJACENT SURFACES / 0 SPELLS+0 GLYPHS+0 RITUALS+0 CAST RESOURCE / 3 MIXINS / PROVIDER PROC+PROJECTILE CAUSALITY PRESERVED / FULL-PACK QA FAIL-CLOSED`

## Installed identity

- physical JAR: `apothic_compats-0.2.4.2.jar`
- mod id: `apothic_compats`
- display name: `Apothic Compats`
- physical version: `0.2.4.2`
- physical SHA-1: `46d3699a4af63531fe84c69fdd2623fbe71fbc75`
- Minecraft: `1.21.1`
- loader: NeoForge
- physical pack loader: NeoForge `21.1.248`
- physical modlist: 595 top-level entries, SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`

The provider is an Apotheosis/Apothic compatibility layer. It must not be treated as a second spell system merely because some compatibility definitions consume Ars Nouveau or Malum attributes/effects.

## Exact official source

Official repository: `ianm1647/apothic-compats`.

Exact inspected source pin:

- commit: `0b9c900344dc536e4748e3ad0f3f18e03f2c3ba4`
- root tree: `76e2e650732584a315b3faa3ab94ff8953e6caad`
- Java tree: `2129a1dcffe47cff7f28647b781078f938407f2d`
- resources tree: `a9682560521c5c9323681f0fdf89241580da3e11`

Exact `gradle.properties` declares Minecraft `1.21.1`, NeoForge baseline `21.1.242`, mod id `apothic_compats`, mod version `0.2.4.2`, mod license `MIT`, and describes the project as an Apotheosis compatibility datapack packed into a mod.

The exact generated metadata template declares required dependencies on NeoForge, Minecraft, Placebo `[9.6.1,)`, and Apotheosis `[8.0.1,)`, plus the provider mixin config. Ars Nouveau, Malum and the other target mods are compatibility targets rather than hard metadata dependencies; provider data are guarded by mod-loaded conditions where applicable.

Physical pack drift is explicit: source development metadata targets Apotheosis `8.6.0`, while the pack contains Apotheosis `8.8.0`. That remains runtime/data QA, not evidence for a Black Arcana fallback.

## Magic semantic inventory

At the exact source ceiling:

- standalone provider spells: **0**
- glyphs: **0**
- rituals: **0**
- provider-owned mana/cast resource: **0**
- provider custom cast pipeline: **0 observed**
- provider packet/payload surface: **0 observed**
- provider SavedData-style magic persistence subsystem: **0 observed**

The complete Java tree contains no provider spell/glyph/ritual registry package or class. Resource paths likewise expose no spell or ritual resources. Asset/model paths containing `ars_nouveau/mana` are Apotheosis gem presentation assets, not a new mana resource.

## Core Apothic surface

The entrypoint registers:

- provider data generation for loot entries, gear sets, affixes, gems, invaders, tags, recipes and data maps;
- `AffixEvents` and `AttributeEvents` on the NeoForge bus;
- provider loot categories and slot groups;
- custom affix codecs;
- optional Curios items;
- exactly 3 required mixins.

If Curios is loaded and the provider config enables custom Curios, `Comp.Curios` registers 11 provider items: `back_plate`, `florid_belt`, `body_chain`, `flashy_bracelet`, `fancy_charm`, `embellished_curio`, `adorned_boots`, `showy_gloves`, `head_cover`, `ornamented_necklace`, and `ornate_ring`.

These are compatibility/equipment objects, not spells.

## Ars Nouveau compatibility boundary

Physical Ars Nouveau is `5.13.1`. The exact provider source supplies conditional Apotheosis definitions that consume Ars-native attributes, effects, entities and equipment.

Observed Ars surfaces include:

- one Apotheosis gem, `apothic_compats:ars_nouveau/mana`;
- gem bonuses to Ars `MAX_MANA`, `MANA_REGEN_BONUS`, `SPELL_DAMAGE_BONUS`, `WARDING`, and the Ars Freezing effect;
- regular Ars affixes affecting max mana and Ars mob effects such as Freezing, Blast, Shocked, Snare and Mana Regen;
- 14 Ars equipment affix-loot entries: Sorcerer, Arcanist and Battlemage armor pieces plus Enchanter's Sword and Enchanter's Shield;
- 3 Ars gear sets: Sorcerer, Arcanist and Battlemage;
- 3 regular Ars invaders: Wilden Guardian, Wilden Hunter and Wilden Stalker.

Source also defines Ancient Reforging-conditioned variants, but no Ancient Reforging mod ID is present in the current physical modlist. Those conditional definitions are therefore not promoted to active-pack runtime behavior.

Ars Nouveau remains authority over its mana, spell attributes, effects, entities and casting. Apotheosis remains authority over affix/gem/loot execution. Apothic Compats owns only its compatibility definitions. Black Arcana must not create a second Ars mana settlement path or interpret the provider gem as BA mana.

## Malum compatibility boundary

Physical Malum is `1.8.2`. Exact source defines:

- exactly 3 Malum-targeted Apotheosis gems: `apothic_compats:malum/soul_stained`, `apothic_compats:malum/thief`, `apothic_compats:malum/etheric`;
- Malum/Lodestone attribute bonuses including Soul Ward, scythe proficiency, spirit spoils, geas limit, charge capacity/duration/recovery, arcane resonance, magic damage/proficiency/resistance and related provider effects;
- extra bonuses that make existing Apotheosis gems interact with Malum scythe/staff categories;
- Malum armor/scythe/staff affix definitions;
- four custom provider affix codecs when Malum is loaded: `scythe_thunderstruck`, `scythe_cleaving`, `staff_thunderstruck`, `staff_cleaving`.

The two Cleaving implementations can issue additional normal player attacks against nearby eligible entities after a sufficiently charged attack, with a provider-local recursion guard. The two Thunderstruck implementations apply nearby damage from a provider-created mob-attack damage source tagged lightning and bypass-armor.

These are offensive provider affix procs, not Black Arcana spells. BA must preserve their causal identity and must not intentionally re-enter them through Backlash, cast-result duplication, or an adapter that turns the same provider damage into a second offensive proc chain.

## Projectile attribute boundary

`AttributeEvents` observes server-side `EntityJoinLevelEvent` for every `Projectile`, scales its delta movement by the owner's Apothic `ARROW_VELOCITY` attribute when the owner is a `LivingEntity`, and marks the projectile with persistent-data boolean `apothic_compats.proj.done` to avoid repeat application.

This is a provider-owned projectile/attribute pass. It is not a spell cast pipeline or persistent player/world magic state. Black Arcana projectile implementations must not duplicate the same velocity scaling merely because a projectile originated from a BA cast; provider event ordering and interaction remain runtime QA.

## Apothic Enchanting mixin boundary

The exact mixin config contains exactly three required mixins:

1. `CandleHolderBlockMixin`
2. `DoubleSkullBlockMixin`
3. `SkullCandleBlockMixin`

They adapt Supplementaries/Amendments blocks to Apothic Enchanting's `EnchantmentStatBlock` interface:

- Candle Holder contributes Arcana based on candle count;
- Double Skull contributes Quanta based on wither-skull composition;
- Skull Candle contributes Arcana from candle count and Quanta from wither-skull type.

This `Arcana` is Apothic Enchanting terminology, not Black Arcana's `Arcane Danger` or spell runtime. No authority mapping is implied.

## Other runtime hooks

`AffixEvents` handles `EntityInvulnerabilityCheckEvent` at high priority and conditionally delegates damage-tag handling to the provider's Aether Magical Dart and Create Magical Potato affixes when those target mods are loaded.

The source also contains compatibility data for multiple non-magic providers. Those surfaces are part of this component's closure but do not become Black Arcana spell identities or increase the semantic spell count.

## Authority and deduplication result

- Apotheosis/Apothic owns affix, gem, loot, invader, category and attribute semantics consumed here.
- Ars Nouveau owns its own spell/mana/effect/entity runtime.
- Malum/Lodestone owns its magic attributes, effects, charge/soul-ward semantics and item behavior.
- Apothic Enchanting owns Eterna/Quanta/Arcana enchanting-stat semantics.
- Apothic Compats owns the compatibility definitions, custom affix codecs, conditional Curios content, projectile attribute pass and other explicitly observed provider glue.
- Black Arcana retains its single server-authoritative casting pipeline, transactional costs, server targeting, BA cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash causality and `WorldEffectPolicy`.
- RPG Skill Tree receives no runtime authority from these integrations.

Do not create parallel datapacks/affixes/loot injection for a surface already supplied here without exact deduplication evidence. Provider absence must fail closed; thematic similarity is not a bridge contract.

## Evidence ceiling / remaining QA

Still fail-closed:

- byte-for-byte source↔physical-JAR reproducibility;
- full physical-JAR class/resource parity with the exact source pin;
- live compatibility of source development baseline Apotheosis 8.6.0 against physical Apotheosis 8.8.0;
- provider reload behavior and duplicate-key/data-map interaction across the complete pack;
- live ordering between the global projectile-velocity event and BA/provider projectile initialization;
- offensive affix-proc interaction with other attack/damage listeners;
- dormant Ancient Reforging and AE2 compatibility behavior if those providers are later added;
- dedicated-server/full-pack runtime QA.

## License / clean-room

Exact metadata declares `MIT`, and the publisher labels the distributed project MIT. The repository does not expose a normal project `LICENSE` file at the inspected root; `TEMPLATE_LICENSE.txt` explicitly licenses NeoForged MDK template files, not by itself the whole project implementation. This catalog therefore records the metadata/publisher license evidence without treating the template license as a broader grant.

Inspection is factual and read-only for compatibility cataloging. No third-party source, assets, models, textures, sounds or implementation are copied into Black Arcana.
