# Ars Elemancy 1.18.3 — technical audit

Status: `SOURCE CATALOG COMPLETE / RUNTIME+CONFIG+CLIENT+FULL-PACK QA PENDING`

Source checkpoint: `Lyrellion/Ars-Elemancy@dfb18286106aca1ca39a9b0053d64a1ef5041751`.

## Confirmed

- version metadata at source checkpoint: 1.18.3;
- physical provider version: 1.18.3;
- 105 item registrations;
- 84 armor pieces / 21 sets;
- 7 foci, 7 essences, 7 bangles;
- 0 local glyphs;
- 0 local perks;
- 6 locally constructed dual SpellSchools plus Elemancer using host `ELEMENTAL`;
- 33 ArmorMaterial entries;
- 3 local PerkSlot values;
- 0 provider block registrations found;
- 0 custom payload registrations;
- focus recognition mixin into Ars Elemental;
- Source costs: essences 3000, bangles 7000, armor 7000, tracked focus JSON 0;
- Curios tags: `an_focus` and `bracelet` cover all seven respective items;
- generated resources are included in `sourceSets.main.resources`.

## Findings requiring runtime/dependency QA

1. Same mod version number exists across multiple upstream commits; source pin is not byte-identical build proof.
2. Root `LICENSE` is GNU GPL v3 while `neoforge.mods.toml` declares GNU LGPL v3.0.
3. HeavyArmorE applies `+25` to the mapped weakness defense path, unlike negative values in lighter tiers; preserve source behavior until runtime confirms intent.
4. Armor tooltip displays tier 5 while `getMinTier()` returns 2.
5. Java datagen explicitly constructs medium armor families while tracked `src/main/resources` contains light/heavy recipes too.
6. A local `ars_elemancy:armor_upgrade` RecipeType/Serializer exists, while tracked armor JSON uses `sauce:armor_upgrade`.
7. Elemancer Bangle effect expansion depends on the exact host `SpellSchools.ELEMENTAL` subschool contract.
8. Armor mana-discount formula and damage absorption final formula are inherited from host APIs and require exact dependency contract audit before reproducing numerically.
9. Pyrobuncle model registration writes to the Frostbuncle model key.
10. Curios is directly used but omitted from the audited runtime dependency declarations; the physical pack currently supplies it.
11. Effective configs/datapack overrides remain unverified.

## Black Arcana disposition

No runtime adapter is justified by this catalog alone. Fused gear increases overlap pressure around multi-element specialization, elemental resistance, mana support and equipment-based spell amplification; these are existing provider capabilities, not automatic gaps for a Black Arcana school.