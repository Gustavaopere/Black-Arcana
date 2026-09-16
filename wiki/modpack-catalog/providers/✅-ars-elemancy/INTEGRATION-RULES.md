# Ars Elemancy 1.18.3 — authority and deduplication rules

Status: `SOURCE-PINNED AUTHORITY MAP / NO BLACK ARCANA ADAPTER APPROVED`

1. Ars Nouveau owns spell construction/execution, mana, spell-stat semantics and Ars perk registry behavior.
2. Ars Elemental/Sauce own the elemental school attributes, ElementalArmorRecipe and host focus/bangle contracts used by Ars Elemancy.
3. Ars Elemancy owns its seven fused equipment identities and direct item modifiers/effects.
4. `registerGlyphs()` is empty: do not count Tempest/Cinder/Silt/Mire/Vapor/Lava as local spell inventories.
5. `registerPerks()` is empty: local PerkSlots 4/5/6 are slot capacity values, not perks.
6. A focus-recognition mixin extends the host Ars Elemental checks on the same resolver. It must not create a second Black Arcana cast, mana debit, cooldown, Mastery, Arcane Danger, Corruption or Strain settlement.
7. Focus mana discount and spell amplification are provider-owned. Do not reapply them by inspecting equipped Curios.
8. Environmental focus effects are provider-owned Curio ticks. Do not duplicate them in a Black Arcana per-tick loop.
9. Bangle attributes and armor attributes are provider-owned equipment modifiers. Do not mirror them into RPG Skill Tree or Black Arcana attributes merely because a matching item is equipped.
10. Armor `MAX_MANA` and `MANA_REGEN_BONUS` modify Ars resource semantics; Black Arcana must not create/credit a second mana pool.
11. Damage resistance/absorption delegates through Sauce/Ars Elemental. Do not infer a generic Black Arcana elemental-resistance bridge without exact host contract and deduplication.
12. The `sauce:armor_upgrade` recipe path owns NBT-preserving equipment conversion. Do not replay item conversion or duplicate resource cost.
13. Client rendering and Starbuncle skins are presentation-only.
14. Any future adapter must pin exact provider versions and fail closed if the host mixin/attribute/API seam changes.