# Apprentice's Codex — exact item registry catalog

## Status

`SOURCE-PINNED 0.9.7.1 / 167/167 ITEM REGISTRY IDS FROZEN / FUNCTIONAL BEHAVIOR AUDIT PARTIAL / ACQUISITION + OPTIONAL-COMPAT QA PENDING`

Source pin: `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`.

This file freezes **registry identity**, not 167 independent provider authorities. Some entries are materials, food, block items, render/weapon content, ammo components or equipment whose detailed runtime behavior still requires its own audit.

## Exact total

`ItemRegistry.ITEMS` contains **167 unique registered item IDs** at the exact 0.9.7.1 source pin.

All IDs below are in namespace `apprenticecodex:`.

## Spell / summoned-weapon-facing content — 12

- `sky_edge_sword`
- `bound_sword`
- `bound_bow`
- `commence_fire_rifle`
- `quick_arms_handgun`
- `breaching_enemy_shotgun`
- `silent_assassin_rifle`
- `lethal_assault_rifle`
- `dual_acrobat_smg`
- `thermal_process_thrower`
- `fly_swatter_launcher`
- `artisan_smash_launcher`

These entries do not imply 12 standalone cast pipelines. Spell files remain authoritative for the corresponding spell lifecycle; provider weapon/item classes own their own held/summoned behavior.

## Materials and consumables — 19

- `arcane_cinder`
- `wisdom_shard`
- `overdrive_broom_engine`
- `spell_extract_shard`
- `crystalline_arcane_shard`
- `bullet_rune`
- `mithril_weave_offcuts`
- `shock_absorption_plate`
- `blast_reactive_plate`
- `wind_accumulation_weave`
- `anti_gravity_weave`
- `scrollwoven_parchment`
- `soul_covered_plate`
- `soul_augmented_weave`
- `comfort_berries`
- `comfort_sandwich`
- `spellstained_arcane_ingot`
- `spellstained_diamond`
- `emberstained_netherite_ingot`

Source-visible food behavior at this pin:

- Comfort Berries apply the provider Mana Regeneration effect for 10 s at amplifier 2;
- Comfort Sandwich applies provider Mana Regeneration for 60 s at amplifier 0.

These are provider consumable effects; Black Arcana must not reinterpret them as Black Arcana mana or a Black Arcana regeneration resource.

## Spellcaster rounds, casings, molds and cards — 19

- `arcane_propellant_charge`
- `spell_bullet_head`
- `spell_bullet_mold`
- `spell_casing_mold`
- `incomplete_spellcaster_round`
- `empty_rapid_spellcaster_casing`
- `empty_basic_spellcaster_casing`
- `empty_arcane_spellcaster_casing`
- `empty_advanced_spellcaster_casing`
- `empty_spell_dominator_casing`
- `empty_multi_purpose_spell_casing`
- `rapid_spellcaster_round`
- `basic_spellcaster_round`
- `arcane_spellcaster_round`
- `advanced_spellcaster_round`
- `spell_dominator_round`
- `multi_purpose_spell_round`
- `spell_invoke_card`
- `spell_autonomy_card`

Ammo/casing identity and consumption belong to Apprentice's Codex. No integration may add a second ammo spend after the provider has settled a shot.

## Armor — 28

### Apprentice Mage — 4

- `apprentice_mage_scarf`
- `apprentice_mage_torso`
- `apprentice_mage_leggings`
- `apprentice_mage_boots`

### Enchantress — 4

- `enchantress_hat`
- `enchantress_robe`
- `enchantress_leggings`
- `enchantress_boots`

### Soulcollector — 4

- `soulcollector_hat`
- `soulcollector_robe`
- `soulcollector_leggings`
- `soulcollector_boots`

### Stealth Rune — 4

- `stealth_rune_armor_head`
- `stealth_rune_armor_body`
- `stealth_rune_armor_leg`
- `stealth_rune_armor_foot`

### Chromatic Magia Dress — 4

- `chromatic_magia_dress_hat`
- `chromatic_magia_dress_coat`
- `chromatic_magia_dress_leggings`
- `chromatic_magia_dress_boots`

### Element Maiden Robe — 4

- `element_maiden_robe_ribbon`
- `element_maiden_robe_robe`
- `element_maiden_robe_leggings`
- `element_maiden_robe_boots`

### Magi Agent Suit — 4

- `magi_agent_suit_hood`
- `magi_agent_suit_coat`
- `magi_agent_suit_leggings`
- `magi_agent_suit_boots`

The spell catalog already proves provider-specific dependencies on some sets, such as full Element Maiden Robe for Divine Possession and Magi Agent Suit hooks on selected firearm spells. Detailed per-piece/set coefficients remain a separate equipment audit.

## Stations, block-items and ink workflow — 12

- `apprentice_desk`
- `crude_ink`
- `partially_used_ink`
- `spellcaster_workbench`
- `spell_calibration_bench`
- `spell_dispenser`
- `creative_spell_dispenser`
- `arcanum_in_a_jar`
- `magnetic_stability_anchor`
- `essence_smoker`
- `atelier_station`
- `alchemy_brewer`

Where an item represents a registered block, `BLOCK-CATALOG.md` is the block-identity authority. Ink items remain item-only workflow content.

## Accessories / Curios-facing utility — 22

- `scarlet_thirst`
- `craftsmans_delight`
- `protection_spell_supporter`
- `spellcaster_ammo_pouch`
- `spellcaster_quiver`
- `absorption_amplify_amulet`
- `autocast_amulet`
- `satellite_followcast_amulet`
- `mana_thruster`
- `magi_compressor_gadget`
- `jumpcast_charm`
- `spell_cast_parrying_ring`
- `attackcast_ring`
- `ashen_circlet`
- `enchanted_circlet`
- `mana_shield_charm`
- `ender_grimoire`
- `archivists_grimoire`
- `spellcaster_accessory_case`
- `explorers_codex`
- `isekai_travel_guidebook`
- `spellstained_runic_tablet`

This is a registry grouping, not a claim that every entry uses the same Curios slot or lifecycle. Those contracts must be established item-by-item before an integration consumes them.

## Spellcaster guns, amplifiers, flasks and utility devices — 18

- `iron_spellcaster_gun`
- `copper_spellcaster_gun`
- `gold_spellcaster_gun`
- `diamond_spellcaster_gun`
- `malignant_spellcaster_gun`
- `iron_spell_amplifier`
- `copper_spell_amplifier`
- `gold_spell_amplifier`
- `diamond_spell_amplifier`
- `silver_spell_amplifier`
- `netherite_spell_amplifier`
- `soulstained_steel_spell_amplifier`
- `photon_siphon`
- `explorers_cane`
- `spellcasters_flask`
- `alchemists_flask`
- `grimoire_manifest`
- `instant_search_brazier`

The spell audit already demonstrates that `alchemists_flask` owns Extract's stored-dose transaction. Other devices require their own exact behavior audit before reuse.

## Casting tools, weapons, shields, brooms and projectile item — 37

- `wooden_wand`
- `pastel_staff`
- `multicast_echo_staff`
- `zenith_staff`
- `focus_staffbow`
- `smashcast_scepter`
- `multipurpose_staffrifle`
- `scrollcaster_gauntlet`
- `chargecast_catalystbook`
- `storage_stabilizer`
- `luminous_device`
- `circuit_heat_staff`
- `charged_twin_blade_staff`
- `mana_force_blade`
- `mana_force_blade_sheath`
- `spell_side_edge`
- `spell_side_edge_mirror`
- `spellcharged_greatsword`
- `copper_swingcast_staff`
- `iron_swingcast_staff`
- `silver_swingcast_staff`
- `gold_swingcast_staff`
- `diamond_swingcast_staff`
- `netherite_swingcast_staff`
- `soulstained_steel_swingcast_staff`
- `mithril_freecast_staff`
- `revolvercast_staff`
- `crystal_bladed_staff`
- `illuminate_stellar_staff`
- `unite_luna_staff`
- `elemental_bow`
- `reflectcast_shield`
- `parrycast_buckler`
- `bulwark_greatshield`
- `floatmount_broom`
- `hoverride_broom`
- `anti_mana_arrow`

`Call Broom` proves that broom deployment state is provider-owned and bound to a uniquely equipped broom item. Staff/gun/shield alternative-cast mechanics likewise remain provider-owned until a specific boundary is audited.

## Authority rules

1. **Iron's** remains authority for canonical mana, schools and standard spell lifecycle used by this addon.
2. **Apprentice's Codex** owns its 167 registered item identities, their ammo/container state, item-specific cast modifiers and equipment semantics.
3. **Black Arcana** must not create a second mana/ammo/dose/storage ledger for these items.
4. Registry presence alone does not create a progression/Mastery hook.
5. Equipment bonus observation must not reapply a provider modifier a second time.
6. Optional integrations remain fail-closed until the exact provider boundary/version is verified.

## Next audit

Registry identity is closed at **167/167**. Detailed behavior remains prioritized for high-impact families: alternative casting tools, autonomous/triggered cast accessories, spellcaster ammo, armor set mechanics, brooms, flasks, shields and station workflows.