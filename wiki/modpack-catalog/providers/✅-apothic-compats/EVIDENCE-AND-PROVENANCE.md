# Apothic Compats 0.2.4.2 — Evidence and provenance

## Evidence hierarchy used

1. current physical modlist for installed presence/version/hash;
2. exact official source pin for implementation/registry/data boundaries;
3. publisher release metadata/changelog for distributed-release context;
4. current Notion dossier for editorial/operational context;
5. Black Arcana canonical architecture/docs for authority and deduplication rules.

No layer is silently substituted for another.

## Physical evidence

Current physical modlist:

- 595 top-level entries;
- SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`;
- NeoForge `21.1.248`;
- `apothic_compats-0.2.4.2.jar`;
- mod ID `apothic_compats`;
- version `0.2.4.2`;
- JAR SHA-1 `46d3699a4af63531fe84c69fdd2623fbe71fbc75`.

Relevant physical targets include Ars Nouveau `5.13.1`, Malum `1.8.2`, Apotheosis `8.8.0`, Placebo `9.9.2`, Curios `9.5.1+1.21.1`, Apothic Enchanting `1.6.2`, Amendments `1.21-2.1.10` and Supplementaries `1.21.1-3.9.8`.

No mod ID `ae2` and no Ancient Reforging identifier is present in the current physical inventory. Source definitions gated on those providers are therefore classified as dormant in this snapshot, not deleted from the source inventory.

## Exact official source evidence

Repository: `ianm1647/apothic-compats`.

Exact pin:

- commit `0b9c900344dc536e4748e3ad0f3f18e03f2c3ba4`;
- root tree `76e2e650732584a315b3faa3ab94ff8953e6caad`;
- Java subtree `2129a1dcffe47cff7f28647b781078f938407f2d`;
- resources subtree `a9682560521c5c9323681f0fdf89241580da3e11`;
- templates subtree `175c66a639f835c19df7817f7ede3ef7f27a423a`.

The recursively inspected Java tree reports `truncated=false`, so the catalog's source-level negative inventory is based on the complete Java path set at this pin rather than a partial search result.

### Source metadata

`gradle.properties` declares:

- Minecraft `1.21.1`;
- NeoForge development baseline `21.1.242`;
- mod id `apothic_compats`;
- mod name `Apothic Compats`;
- mod version `0.2.4.2`;
- mod license `MIT`;
- description: an Apotheosis compatibility datapack packed into a mod for easy installation.

Development dependency versions include Apotheosis `8.6.0`; physical Apotheosis is `8.8.0`. This is retained as a QA drift boundary.

`src/main/templates/META-INF/neoforge.mods.toml` declares required runtime dependencies on:

- NeoForge;
- Minecraft;
- Placebo `[9.6.1,)`;
- Apotheosis `[8.0.1,)`.

It also declares the provider mixin configuration. Ars Nouveau, Malum and the other compatibility targets are not hard dependencies in that exact metadata template.

## Complete Java/runtime source observations

The exact Java tree includes provider code for:

- core entrypoint/config/conditional Curios registration;
- custom affix codecs;
- generic datagen and tags/data maps/recipes;
- provider-specific affix loot, gear set, affix, gem and invader generators;
- event hooks;
- 11 optional custom Curios items;
- loot categories and slot groups;
- exactly 3 mixin classes.

Negative source inventory:

- no provider spell-registry package/class observed;
- no glyph registry observed;
- no ritual registry observed;
- no packet/payload package/class observed;
- no SavedData subsystem observed;
- no provider-specific cast controller/resource/cooldown pipeline observed.

Resource path searches at the exact tree expose zero `spell` paths and zero `ritual` paths. `ars_nouveau/mana` asset paths correspond to the provider's Apotheosis gem model/texture, not a resource registry.

## Entrypoint and conditional content evidence

`ApothicCompats.java` registers the NeoForge bus, `AffixEvents`, `AttributeEvents`, startup config, provider slot groups/loot categories/custom affix codecs and the data-generation provider suite.

`Comp.java` conditionally registers 11 Curios items only when Curios is loaded and provider config enables the feature.

No second spell runtime is initialized by either path.

## Ars Nouveau evidence

Exact classes include:

- `ArsAffixLootProvider`
- `ArsAffixProvider`
- `ArsGearSetProvider`
- `ArsGemProvider`
- `ArsInvaderProvider`

Observed exact semantic surfaces:

- gem `apothic_compats:ars_nouveau/mana`, conditionally generated when `ars_nouveau` is loaded;
- bonuses consuming Ars `MAX_MANA`, `MANA_REGEN_BONUS`, `SPELL_DAMAGE_BONUS`, `WARDING` and provider mob effects;
- regular Ars armor/melee/ranged affix definitions;
- 14 Ars affix-loot equipment entries;
- 3 Ars gear sets;
- 3 regular Ars Wilden invader definitions;
- additional Ancient Reforging-conditioned variants in source.

These definitions consume provider-native Ars/Apotheosis surfaces. They do not register an Ars spell or create a new mana/cast authority.

## Malum evidence

Exact Malum source includes three custom gems:

- `apothic_compats:malum/soul_stained`
- `apothic_compats:malum/thief`
- `apothic_compats:malum/etheric`

They modify Malum/Lodestone/Apothic attributes/effects according to Apotheosis gem categories and purity.

`MalumExtraGemBonusProvider` adds Malum scythe/staff bonuses to existing Apotheosis gems. `MalumAffixProvider`, `ScytheAffixProvider` and `StaffAffixProvider` generate Malum-targeted affix definitions.

`ModAffixRegistry` conditionally registers exactly four custom Malum affix codecs:

- `apothic_compats:scythe_thunderstruck`
- `apothic_compats:scythe_cleaving`
- `apothic_compats:staff_thunderstruck`
- `apothic_compats:staff_cleaving`

The Cleaving implementations can call normal `Player.attack(...)` on nearby eligible entities after a sufficiently charged attack, protected by a provider-local static recursion flag. The Thunderstruck implementations apply nearby damage from a provider-created mob-attack damage source tagged `IS_LIGHTNING` and `BYPASSES_ARMOR`.

These are provider affix procs and must remain distinct from Black Arcana spell/backlash causality.

## Runtime event evidence

`AttributeEvents.proj`:

- listens to `EntityJoinLevelEvent`;
- operates only on `Projectile` entities;
- returns on client side;
- returns if persistent-data boolean `apothic_compats.proj.done` is already set;
- if owner is a `LivingEntity`, scales projectile delta movement by Apothic Attributes `ARROW_VELOCITY`;
- sets the marker afterward.

This is a one-time provider projectile-attribute pass, not a magic persistence subsystem.

`AffixEvents.modifyIncomingDamageTags` listens at HIGH priority to `EntityInvulnerabilityCheckEvent` and delegates to provider Aether/Create affix helpers only when their target mods are loaded.

## Mixin evidence

`apothic_compats.mixins.json` is required and lists exactly:

1. `CandleHolderBlockMixin`
2. `DoubleSkullBlockMixin`
3. `SkullCandleBlockMixin`

All three adapt target blocks to Apothic Enchanting `EnchantmentStatBlock` statistics. No mixin targets a casting controller, spell registry or Black Arcana runtime.

## Publisher evidence

CurseForge publishes exact file `apothic_compats-0.2.4.2.jar` for NeoForge Minecraft 1.21.1 as project/file `1188699 / 8483936`, released 2026-07-22. Publisher text describes the project as adding Apotheosis datapack compatibility for other mods, labels it Client & Server, and labels the project MIT.

The 0.2.4.2 changelog states an update to Apotheosis 8.6.0 and newer compatibility targets while noting some integrations still need touch-ups for newer additions. That warning is preserved as a drift/coverage QA boundary rather than interpreted as an unbounded compatibility guarantee.

Publisher dependency relations and exact generated metadata are recorded separately. The exact TOML is the stronger authority for formal hard dependency declarations.

## Notion context

Notion page `Apothic Compats` (`3c369db9-f0db-81f9-a8f3-dbba4d755acb`) classifies the provider as a data-driven compatibility layer, not a second affix/gem/progression system. It highlights Ars Nouveau, Malum, Create, Curios, Amendments, Supplementaries and supported mob integrations, and explicitly warns about:

- provider-version drift;
- duplicate classification;
- duplicate loot/affix injection;
- optional-provider absence;
- incomplete future coverage.

The Notion page is editorial/operational context. Physical modlist and exact source remain higher authority for presence/version and implementation claims.

## Black Arcana provenance/authority consequence

No provider class, JSON, asset or algorithm is copied. Source inspection is used only to establish identities, boundaries, causality and deduplication constraints.

Black Arcana must:

- keep its own server-authoritative cast pipeline;
- not count Apothic Compats gems/affixes as spells;
- not create a second Ars/Malum mana/charge settlement path;
- not duplicate the provider's projectile velocity pass;
- not turn provider Cleaving/Thunderstruck damage into a second BA offensive proc chain;
- not infer that Apothic Enchanting `Arcana` equals Black Arcana `Arcane Danger`;
- fail closed when optional providers are absent or an exact compatibility hook is unknown.

## License / reuse note

Exact project metadata and publisher evidence say MIT. The inspected repository root contains `TEMPLATE_LICENSE.txt`, whose own text restricts that license statement to NeoForged MDK template files; it is not used as independent proof of the whole project's licensing. This catalog does not depend on reuse rights because inspection is factual/read-only.
