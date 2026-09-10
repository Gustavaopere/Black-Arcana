# Apotheotic Creation 2.0.0 — Evidence and provenance

## Physical authority

Current physical modpack authority:

- Minecraft 1.21.1;
- NeoForge 21.1.248;
- 595 top-level entries;
- modlist SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`;
- artifact `apotheoticcreation-2.0.0.jar`;
- mod id `apotheoticcreation`;
- display name `Apotheosis/Create Addon`;
- embedded/runtime version 2.0.0;
- physical SHA-1 `6bbb91aea834941b47a6af3318b091f64e4375ab`;
- physical Create 6.0.10;
- physical Apotheosis 8.8.0.

Presence/version/hash claims come from the physical inventory rather than publisher naming alone.

## Publisher evidence

Current CurseForge surface identifies:

- project `956637`;
- author/uploader line `themaxpowa`;
- exact file `8391265`;
- file name `apotheoticcreation-2.0.0.jar`;
- uploaded 2026-07-08;
- release type;
- NeoForge / Minecraft 1.21.1;
- project license MIT;
- project description: compatibility for Apotheosis affixes/rarities in Create attribute filters;
- publisher `Source` link resolves to `https://github.com/maxpowa/ApotheoticCreation`.

This distinguishes the physical/original provider from similarly named forks and ports.

## Exact official source pin

Official repository: `maxpowa/ApotheoticCreation`.

Exact Minecraft 1.21.1 / 2.0.0 source:

- commit `ed56ccf54e1be132c983c524597300e852098840`;
- commit message `feat: support minecraft 1.21.1`;
- source tree `5c5d51ef69b5f0f50d398d7f0479b8ca83894f7d`;
- active source branch line `mc/1.21.1`;
- recursive tree inspection reports `truncated=false`.

The exact tree contains a single Java source file: `src/main/java/us/maxpowa/apc/ApotheoticCreation.java`.

## Exact source metadata

At the exact source pin, `gradle.properties` declares:

- Minecraft 1.21.1 / range `[1.21.1]`;
- NeoForge development baseline 21.1.235;
- mod id `apotheoticcreation`;
- display name `Apotheosis/Create Addon`;
- mod version 2.0.0;
- license MIT;
- description `Create addon to allow attribute filter identification of Apotheosis affix items.`;
- Create version range `[6,)`, with development artifact line 6.0.10-280;
- Apotheosis version range `[8,)`, with development baseline 8.5.4.

The exact `neoforge.mods.toml` declares Create and Apotheosis mandatory, ordered `AFTER`, side `BOTH`, using those version ranges. The physical Create 6.0.10 and Apotheosis 8.8.0 satisfy the declared ranges. This range check is not a full runtime-compatibility proof.

## Exact registry evidence

The single Java class registers against `CreateBuiltInRegistries.ITEM_ATTRIBUTE_TYPE` during NeoForge `RegisterEvent` and declares two IDs:

- `apotheoticcreation:rarity`;
- `apotheoticcreation:affix`.

No additional addon registry type is present in the complete Java source.

### Rarity attribute

`RarityAttribute`:

- uses `LootRarity.CODEC.fieldOf("rarity")` for map serialization;
- uses `RarityRegistry.INSTANCE.holderStreamCodec()` for stream serialization;
- obtains item rarity through `AffixHelper.getRarity(stack)`;
- returns false when the provider holder is unbound;
- otherwise matches the item's provider rarity to the selected rarity;
- enumerates either no attribute for an unbound rarity or one `RarityAttribute` for the bound provider rarity.

This is a consumer/translation path. Apotheosis remains authority for `LootRarity` identity and item rarity state.

### Affix attribute

`AffixAttribute`:

- uses `AffixRegistry.INSTANCE.holderCodec().fieldOf("affix")` for map serialization;
- uses `AffixRegistry.INSTANCE.holderStreamCodec()` for stream serialization;
- obtains the item's provider affix map through `AffixHelper.getAffixes(stack)`;
- matches when that map contains the selected provider affix holder;
- enumerates bound provider affixes as Create item attributes;
- excludes affix ID paths `socket` and `durable` from `getAllAttributes` enumeration.

The source proves an enumeration exclusion; it does not prove that every possible explicitly constructed/deserialized `AffixAttribute` for those IDs is universally impossible. The catalog therefore records only the narrower observed contract.

## Serialization ownership

The two attribute classes define their own `MapCodec` and `StreamCodec`. That means Apotheotic Creation owns serialization of the selected rarity/affix attribute value. Those codecs can participate when Create persists or synchronizes an enclosing Attribute Filter.

This does **not** establish an addon-owned persistence or network subsystem. In the complete exact source tree there is no standalone payload registration, no SavedData, no attachment container and no independent filter-storage implementation. Create remains authority for the enclosing filter storage/transport lifecycle.

## Negative-surface evidence

Because the recursive tree is complete and the Java surface is one class, the audit can close several addon-owned negative facts at this pin:

- no standalone spell/glyph/ritual registry;
- no mana/cast resource;
- no standalone addon-owned payload registration;
- no addon-owned SavedData/attachment/persistence container;
- no mixin surface;
- no separate affix/rarity content registry;
- no machine-gem/socket/buff runtime.

These negative claims are deliberately narrower than “no serialization”: the addon does own codecs for its two attribute values. They are scoped to the exact 2.0.0 source pin and do not generalize to future versions.

## Authority interpretation

- Apotheosis owns affix and rarity definitions/state.
- Create owns `ItemAttributeType` framework behavior, enclosing Attribute Filter storage/transport and logistics consumers.
- Apotheotic Creation owns the narrow bridge registering provider-aware Create attribute types plus serialization of those two attribute values.
- Downstream blocks such as Smart Observers, Brass Tunnels, funnels or other Create systems do not become independent addon APIs merely because they consume normal filters.
- Apokinetics is a separate concern for machine-gem/socket/upgrades and is not replaced by this addon.
- Black Arcana retains canonical casting, targeting, resource transaction, cooldown/charge, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash and world-safety authority.
- RPG Skill Tree receives no authority from this metadata/filter bridge.

For current catalog purposes, no Black Arcana runtime adapter is required. Reimplementing the same rarity/affix classification would create unnecessary duplicate processing and ownership ambiguity.

## Unproven / intentionally fail-closed

- source/JAR byte reproducibility;
- exact physical-vs-CurseForge file hash equality;
- full-modpack runtime behavior of Create Attribute Filters;
- custom datapack rarity/affix behavior;
- multiple-affix UI matching/composition semantics;
- Create whitelist/blacklist behavior;
- Smart Observer / Brass Tunnel / funnel routing behavior;
- persisted-filter reload/restart compatibility;
- future-version API parity.

## Licensing / clean-room provenance

Observed license evidence:

- exact `gradle.properties`: MIT;
- exact root `LICENSE.md`: MIT, copyright 2023 maxpowa;
- current CurseForge project surface: MIT;
- no separate asset-license file observed in the complete exact source tree.

Black Arcana treats the repository as `REFERENCE_ONLY / COMPATIBILITY_TARGET` for factual interoperability/catalog evidence. No provider code, assets or text are copied/adapted. A permissive source license does not make copying necessary; provider-native interoperability remains preferred.