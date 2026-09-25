# Capability Matrix Delta — Fantasy Armor 1.2.4-1.21.1

Status: `CATALOGED / SOURCE-PINNED PASSIVE GEAR MAGIC / +0 SEMANTIC ACTIONS`

| Fantasy Armor capability | Provider-native meaning | Black Arcana consequence |
|---|---|---|
| 29 armor sets | provider equipment identities | do not treat item/set names as spells |
| 116 armor pieces | four wearable pieces per set | equipment content only |
| Moon Crystal | provider crafting/progression item | resource/item; not a cast |
| armor attributes | configurable armor/toughness/KB/speed/health/damage/speed/luck etc. | preserve provider equipment modifier authority |
| full-set MobEffects | passive effects refreshed while a complete matching set is worn | do not duplicate or recast through Black Arcana |
| nine default effect types | Minecraft-owned vanilla MobEffects | no provider semantic identity minted |
| Epic Fight coexistence | external combat/render behavior | test modifier/render composition, not semantic spell overlap |
| Cosmetic Armor coexistence | separates visible armor from functional equipment | functional Fantasy Armor state remains provider-owned |
| 3D model/render layer | visual provider surface | presentation only |

## Semantic boundary

The exact 1.2.4 source pin establishes no spell, ritual, cast, active ability, keybind or active-use action registry.

Therefore:

- provider-owned spells: **0**;
- provider-owned rites/rituals: **0**;
- equivalent discrete magical actions: **0**;
- passive equipment magic: present.

Strict semantic delta: **+0**.

## Runtime boundary

Catalog closure is independent from full-pack runtime QA.

Remain fail-closed for:

- deployed config;
- effect/modifier lifecycle;
- death/relog/restart;
- Epic Fight/Cosmetic Armor/FirstPerson interaction;
- dedicated server;
- resource/model compatibility.
