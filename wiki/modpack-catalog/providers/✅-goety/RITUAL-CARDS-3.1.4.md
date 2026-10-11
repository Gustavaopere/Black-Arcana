# Goety 3.1.4 — 238 fichas individuais de rituais não-Focus

Estado: **✅ 238/238 fichas `COUNTED_EXACT`**, por recurso de receita e assinatura semântica exata; **⚠️** execução física/configuração/integração não certificadas nesta materialização.

## Fontes e limites de contagem

- Mod `goety`, JAR instalado `goety-3.1.4.jar`, SHA-1 exato `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`, publisher File `8689429`.
- [Inventário semântico do artefato](EXACT-3.1.4-SEMANTIC-INVENTORY.md): **123 Focuses + 238 rituais não-Focus = 361 objetos** contabilizados neste provider. As fichas **não** geram feitiços novos nem integram o runtime de Black Arcana.
- A auditoria exata contém **342** recursos `goety:ritual`: **83** recursos de aquisição de Focus ficam fora da contagem independente; dos **259** restantes, quatro grupos de receitas alternativas colapsam em **255** assinaturas, e **17** rituais condicionados por dependências ausentes (16 Cyclic e 1 VanillaTweaks) ficam fora do pack atual. Resultado: **238** identidades únicas e disponíveis no universo físico documentado.
- As **238** assinaturas são únicas, assim como os **238** caminhos de recursos na seção auditada. A organização da pasta `rituals/cards/` preserva subpastas do inventário `.json` original, apenas transformando o sufixo documental em `.md`.
- A assinatura `RITUAL_RESULT:`, `CONVERT:`, `ENCHANT:`, `LOCATE:`, `SUMMON:` ou `RITUAL_PATH:` é uma **chave semântica de auditoria**, não um suposto registry ID de spell. Em particular, `CONVERT:?->...` deixa explicitamente a origem desconhecida e `RITUAL_PATH:` não declara um resultado não comprovado.
- **Métrica:** `COUNTED_EXACT`, **+0 novas identidades** neste trabalho. Os mínimos globais seguem **1.851 / 1.849 no escopo solicitado**, com denominador final não fechado.
- **QA condicionado:** a prova hash-matched confirma o recurso e sua classificação documental; não substitui teste em Survival das receitas, config deployada, Soul Energy, targeting, owner, WorldEffectPolicy ou APIs.
- **Clean-room:** os arquivos registram apenas fatos técnicos já preservados na auditoria, sem reproduzir receitas JSON, código ou assets de outros mods.

## Tipos de ação — 238/238

| Classe auditada | Quantidade |
|---|---:|
| `OTHER_RITUAL` | 123 |
| `CONVERSION_RITUAL` | 23 |
| `ENCHANT_RITUAL` | 37 |
| `LOCATE_RITUAL` | 19 |
| `SUMMON_RITUAL` | 2 |
| `THRALL_SUMMON_RITUAL` | 34 |
| **Total** | **238** |

## Tipos de crafting — 238/238

| Categoria de crafting | Quantidade |
|---|---:|
| `deep` | 9 |
| `geoturgy` | 15 |
| `animation` | 3 |
| `forge` | 47 |
| `end` | 7 |
| `expert_nether` | 13 |
| `necroturgy` | 36 |
| `overgrown` | 11 |
| `adept_nether` | 8 |
| `magic` | 48 |
| `storm` | 8 |
| `frost` | 4 |
| `sky` | 9 |
| `divination` | 19 |
| `sabbath` | 1 |
| **Total** | **238** |

## Índice das 238 fichas

| # | Recurso da receita | Assinatura semântica | Classe | Craft type |
|---:|---|---|---|---|
| 1 | [`abyss_crown.json`](rituals/cards/abyss_crown.md) | `RITUAL_RESULT:goety:abyss_crown` | `OTHER_RITUAL` | `deep` |
| 2 | [`abyss_robe.json`](rituals/cards/abyss_robe.md) | `RITUAL_RESULT:goety:abyss_robe` | `OTHER_RITUAL` | `deep` |
| 3 | [`abyss_staff.json`](rituals/cards/abyss_staff.md) | `RITUAL_RESULT:goety:abyss_staff` | `OTHER_RITUAL` | `deep` |
| 4 | [`alarming_charm.json`](rituals/cards/alarming_charm.md) | `RITUAL_RESULT:goety:alarming_charm` | `OTHER_RITUAL` | `geoturgy` |
| 5 | [`animation_core.json`](rituals/cards/animation_core.md) | `RITUAL_RESULT:goety:animation_core` | `OTHER_RITUAL` | `animation` |
| 6 | [`animator.json`](rituals/cards/animator.md) | `RITUAL_RESULT:goety:animator` | `OTHER_RITUAL` | `forge` |
| 7 | [`arca.json`](rituals/cards/arca.md) | `RITUAL_RESULT:goety:arca` | `OTHER_RITUAL` | `forge` |
| 8 | [`black_beast_cursed_armor.json`](rituals/cards/black_beast_cursed_armor.md) | `RITUAL_RESULT:goety:black_beast_cursed_armor` | `OTHER_RITUAL` | `forge` |
| 9 | [`black_beast_dark_armor.json`](rituals/cards/black_beast_dark_armor.md) | `RITUAL_RESULT:goety:black_beast_dark_armor` | `OTHER_RITUAL` | `forge` |
| 10 | [`black_crystal.json`](rituals/cards/black_crystal.md) | `RITUAL_RESULT:goety:black_crystal` | `OTHER_RITUAL` | `forge` |
| 11 | [`black_iron/black_iron_boots.json`](rituals/cards/black_iron/black_iron_boots.md) | `RITUAL_RESULT:goety:black_iron_boots` | `OTHER_RITUAL` | `forge` |
| 12 | [`black_iron/black_iron_chestplate.json`](rituals/cards/black_iron/black_iron_chestplate.md) | `RITUAL_RESULT:goety:black_iron_chestplate` | `OTHER_RITUAL` | `forge` |
| 13 | [`black_iron/black_iron_helmet.json`](rituals/cards/black_iron/black_iron_helmet.md) | `RITUAL_RESULT:goety:black_iron_helmet` | `OTHER_RITUAL` | `forge` |
| 14 | [`black_iron/black_iron_leggings.json`](rituals/cards/black_iron/black_iron_leggings.md) | `RITUAL_RESULT:goety:black_iron_leggings` | `OTHER_RITUAL` | `forge` |
| 15 | [`blade_of_ender.json`](rituals/cards/blade_of_ender.md) | `RITUAL_RESULT:goety:blade_of_ender` | `OTHER_RITUAL` | `end` |
| 16 | [`blazing_cage.json`](rituals/cards/blazing_cage.md) | `RITUAL_RESULT:goety:blazing_cage` | `OTHER_RITUAL` | `expert_nether` |
| 17 | [`bonehead_hammer.json`](rituals/cards/bonehead_hammer.md) | `RITUAL_RESULT:goety:bonehead_hammer` | `OTHER_RITUAL` | `necroturgy` |
| 18 | [`budding_amethyst.json`](rituals/cards/budding_amethyst.md) | `RITUAL_RESULT:minecraft:budding_amethyst` | `OTHER_RITUAL` | `geoturgy` |
| 19 | [`bygone_scroll.json`](rituals/cards/bygone_scroll.md) | `RITUAL_RESULT:goety:bygone_scroll` | `OTHER_RITUAL` | `expert_nether` |
| 20 | [`convert_black_wolf_to_black_beast.json`](rituals/cards/convert_black_wolf_to_black_beast.md) | `CONVERT:?->goety:black_beast` | `CONVERSION_RITUAL` | `overgrown` |
| 21 | [`convert_blazes_to_wildfire.json`](rituals/cards/convert_blazes_to_wildfire.md) | `CONVERT:?->goety:wildfire` | `CONVERSION_RITUAL` | `expert_nether` |
| 22 | [`convert_cow_to_mooshroom.json`](rituals/cards/convert_cow_to_mooshroom.md) | `CONVERT:?->minecraft:mooshroom` | `CONVERSION_RITUAL` | `overgrown` |
| 23 | [`convert_drowned_to_drowned_necromancer.json`](rituals/cards/convert_drowned_to_drowned_necromancer.md) | `CONVERT:?->goety:drowned_necromancer_servant` | `CONVERSION_RITUAL` | `deep` |
| 24 | [`convert_guardian_to_elder_guardian.json`](rituals/cards/convert_guardian_to_elder_guardian.md) | `CONVERT:?->goety:elder_guardian_servant` | `CONVERSION_RITUAL` | `deep` |
| 25 | [`convert_hoglin_to_hoglin_servant.json`](rituals/cards/convert_hoglin_to_hoglin_servant.md) | `CONVERT:?->goety:hoglin_servant` | `CONVERSION_RITUAL` | `adept_nether` |
| 26 | [`convert_mossy_skeleton_to_mossy_necromancer.json`](rituals/cards/convert_mossy_skeleton_to_mossy_necromancer.md) | `CONVERT:?->goety:mossy_necromancer_servant` | `CONVERSION_RITUAL` | `necroturgy` |
| 27 | [`convert_pig_to_hoglin.json`](rituals/cards/convert_pig_to_hoglin.md) | `CONVERT:?->minecraft:hoglin` | `CONVERSION_RITUAL` | `adept_nether` |
| 28 | [`convert_pillager_to_trampler.json`](rituals/cards/convert_pillager_to_trampler.md) | `CONVERT:?->goety:trampler_servant` | `CONVERSION_RITUAL` | `magic` |
| 29 | [`convert_polar_bear_to_polar_bear_servant.json`](rituals/cards/convert_polar_bear_to_polar_bear_servant.md) | `CONVERT:?->goety:polar_bear_servant` | `CONVERSION_RITUAL` | `overgrown` |
| 30 | [`convert_skeleton_horse.json`](rituals/cards/convert_skeleton_horse.md) | `CONVERT:?->minecraft:skeleton_horse` | `CONVERSION_RITUAL` | `necroturgy` |
| 31 | [`convert_skeleton_to_necromancer.json`](rituals/cards/convert_skeleton_to_necromancer.md) | `CONVERT:?->goety:necromancer_servant` | `CONVERSION_RITUAL` | `necroturgy` |
| 32 | [`convert_spider_to_brood_mother.json`](rituals/cards/convert_spider_to_brood_mother.md) | `CONVERT:?->goety:brood_mother_servant` | `CONVERSION_RITUAL` | `overgrown` |
| 33 | [`convert_stray_to_cairn_necromancer.json`](rituals/cards/convert_stray_to_cairn_necromancer.md) | `CONVERT:?->goety:cairn_necromancer_servant` | `CONVERSION_RITUAL` | `necroturgy` |
| 34 | [`convert_trader_to_reprobate.json`](rituals/cards/convert_trader_to_reprobate.md) | `CONVERT:?->goety:reprobate_servant` | `CONVERSION_RITUAL` | `storm` |
| 35 | [`convert_villager_to_neollager.json`](rituals/cards/convert_villager_to_neollager.md) | `CONVERT:?->goety:neollager` | `CONVERSION_RITUAL` | `magic` |
| 36 | [`convert_villager_to_ravaged.json`](rituals/cards/convert_villager_to_ravaged.md) | `CONVERT:?->goety:ravaged` | `CONVERSION_RITUAL` | `magic` |
| 37 | [`convert_villager_to_warlock.json`](rituals/cards/convert_villager_to_warlock.md) | `CONVERT:?->goety:warlock_servant` | `CONVERSION_RITUAL` | `adept_nether` |
| 38 | [`convert_villager_to_witch.json`](rituals/cards/convert_villager_to_witch.md) | `CONVERT:?->goety:witch_servant` | `CONVERSION_RITUAL` | `storm` |
| 39 | [`convert_wither_skeleton_to_wither_necromancer.json`](rituals/cards/convert_wither_skeleton_to_wither_necromancer.md) | `CONVERT:?->goety:wither_necromancer_servant` | `CONVERSION_RITUAL` | `expert_nether` |
| 40 | [`convert_wolf_to_ripper.json`](rituals/cards/convert_wolf_to_ripper.md) | `CONVERT:?->goety:ripper_servant` | `CONVERSION_RITUAL` | `magic` |
| 41 | [`convert_zombify_horse.json`](rituals/cards/convert_zombify_horse.md) | `CONVERT:?->minecraft:zombie_horse` | `CONVERSION_RITUAL` | `necroturgy` |
| 42 | [`convert_zombify_ravager.json`](rituals/cards/convert_zombify_ravager.md) | `CONVERT:?->goety:zombie_ravager` | `CONVERSION_RITUAL` | `necroturgy` |
| 43 | [`cursed_metal_wolf_armor.json`](rituals/cards/cursed_metal_wolf_armor.md) | `RITUAL_RESULT:goety:cursed_metal_wolf_armor` | `OTHER_RITUAL` | `forge` |
| 44 | [`dark/dark_boots.json`](rituals/cards/dark/dark_boots.md) | `RITUAL_RESULT:goety:dark_boots` | `OTHER_RITUAL` | `forge` |
| 45 | [`dark/dark_chestplate.json`](rituals/cards/dark/dark_chestplate.md) | `RITUAL_RESULT:goety:dark_chestplate` | `OTHER_RITUAL` | `forge` |
| 46 | [`dark/dark_helmet.json`](rituals/cards/dark/dark_helmet.md) | `RITUAL_RESULT:goety:dark_helmet` | `OTHER_RITUAL` | `forge` |
| 47 | [`dark/dark_leggings.json`](rituals/cards/dark/dark_leggings.md) | `RITUAL_RESULT:goety:dark_leggings` | `OTHER_RITUAL` | `forge` |
| 48 | [`dark/dark_metal_scythe.json`](rituals/cards/dark/dark_metal_scythe.md) | `RITUAL_RESULT:goety:dark_metal_scythe` | `OTHER_RITUAL` | `forge` |
| 49 | [`dark_scythe.json`](rituals/cards/dark_scythe.md) | `RITUAL_RESULT:goety:dark_scythe` | `OTHER_RITUAL` | `forge` |
| 50 | [`dark_wolf_armor.json`](rituals/cards/dark_wolf_armor.md) | `RITUAL_RESULT:goety:dark_wolf_armor` | `OTHER_RITUAL` | `forge` |
| 51 | [`death_scythe.json`](rituals/cards/death_scythe.md) | `RITUAL_RESULT:goety:death_scythe` | `OTHER_RITUAL` | `necroturgy` |
| 52 | [`diamond_ravager_armor.json`](rituals/cards/diamond_ravager_armor.md) | `RITUAL_RESULT:goety:diamond_ravager_armor` | `OTHER_RITUAL` | `forge` |
| 53 | [`diamond_trampler_armor.json`](rituals/cards/diamond_trampler_armor.md) | `RITUAL_RESULT:goety:diamond_trampler_armor` | `OTHER_RITUAL` | `forge` |
| 54 | [`eerie_pickaxe.json`](rituals/cards/eerie_pickaxe.md) | `RITUAL_RESULT:goety:eerie_pickaxe` | `OTHER_RITUAL` | `forge` |
| 55 | [`enchant/aqua_affinity.json`](rituals/cards/enchant/aqua_affinity.md) | `ENCHANT:minecraft:aqua_affinity` | `ENCHANT_RITUAL` | `magic` |
| 56 | [`enchant/bane_of_arthropods.json`](rituals/cards/enchant/bane_of_arthropods.md) | `ENCHANT:minecraft:bane_of_arthropods` | `ENCHANT_RITUAL` | `magic` |
| 57 | [`enchant/binding_curse.json`](rituals/cards/enchant/binding_curse.md) | `ENCHANT:minecraft:binding_curse` | `ENCHANT_RITUAL` | `magic` |
| 58 | [`enchant/blast_protection.json`](rituals/cards/enchant/blast_protection.md) | `ENCHANT:minecraft:blast_protection` | `ENCHANT_RITUAL` | `magic` |
| 59 | [`enchant/channeling.json`](rituals/cards/enchant/channeling.md) | `ENCHANT:minecraft:channeling` | `ENCHANT_RITUAL` | `magic` |
| 60 | [`enchant/depth_strider.json`](rituals/cards/enchant/depth_strider.md) | `ENCHANT:minecraft:depth_strider` | `ENCHANT_RITUAL` | `magic` |
| 61 | [`enchant/efficiency.json`](rituals/cards/enchant/efficiency.md) | `ENCHANT:minecraft:efficiency` | `ENCHANT_RITUAL` | `magic` |
| 62 | [`enchant/feather_falling.json`](rituals/cards/enchant/feather_falling.md) | `ENCHANT:minecraft:feather_falling` | `ENCHANT_RITUAL` | `magic` |
| 63 | [`enchant/fire_aspect.json`](rituals/cards/enchant/fire_aspect.md) | `ENCHANT:minecraft:fire_aspect` | `ENCHANT_RITUAL` | `magic` |
| 64 | [`enchant/fire_protection.json`](rituals/cards/enchant/fire_protection.md) | `ENCHANT:minecraft:fire_protection` | `ENCHANT_RITUAL` | `magic` |
| 65 | [`enchant/flame.json`](rituals/cards/enchant/flame.md) | `ENCHANT:minecraft:flame` | `ENCHANT_RITUAL` | `magic` |
| 66 | [`enchant/fortune.json`](rituals/cards/enchant/fortune.md) | `ENCHANT:minecraft:fortune` | `ENCHANT_RITUAL` | `magic` |
| 67 | [`enchant/impaling.json`](rituals/cards/enchant/impaling.md) | `ENCHANT:minecraft:impaling` | `ENCHANT_RITUAL` | `magic` |
| 68 | [`enchant/infinity.json`](rituals/cards/enchant/infinity.md) | `ENCHANT:minecraft:infinity` | `ENCHANT_RITUAL` | `magic` |
| 69 | [`enchant/knockback.json`](rituals/cards/enchant/knockback.md) | `ENCHANT:minecraft:knockback` | `ENCHANT_RITUAL` | `magic` |
| 70 | [`enchant/looting.json`](rituals/cards/enchant/looting.md) | `ENCHANT:minecraft:looting` | `ENCHANT_RITUAL` | `magic` |
| 71 | [`enchant/loyalty.json`](rituals/cards/enchant/loyalty.md) | `ENCHANT:minecraft:loyalty` | `ENCHANT_RITUAL` | `magic` |
| 72 | [`enchant/luck_of_the_sea.json`](rituals/cards/enchant/luck_of_the_sea.md) | `ENCHANT:minecraft:luck_of_the_sea` | `ENCHANT_RITUAL` | `magic` |
| 73 | [`enchant/lure.json`](rituals/cards/enchant/lure.md) | `ENCHANT:minecraft:lure` | `ENCHANT_RITUAL` | `magic` |
| 74 | [`enchant/mending.json`](rituals/cards/enchant/mending.md) | `ENCHANT:minecraft:mending` | `ENCHANT_RITUAL` | `magic` |
| 75 | [`enchant/multishot.json`](rituals/cards/enchant/multishot.md) | `ENCHANT:minecraft:multishot` | `ENCHANT_RITUAL` | `magic` |
| 76 | [`enchant/piercing.json`](rituals/cards/enchant/piercing.md) | `ENCHANT:minecraft:piercing` | `ENCHANT_RITUAL` | `magic` |
| 77 | [`enchant/power.json`](rituals/cards/enchant/power.md) | `ENCHANT:minecraft:power` | `ENCHANT_RITUAL` | `magic` |
| 78 | [`enchant/projectile_protection.json`](rituals/cards/enchant/projectile_protection.md) | `ENCHANT:minecraft:projectile_protection` | `ENCHANT_RITUAL` | `magic` |
| 79 | [`enchant/protection.json`](rituals/cards/enchant/protection.md) | `ENCHANT:minecraft:protection` | `ENCHANT_RITUAL` | `magic` |
| 80 | [`enchant/punch.json`](rituals/cards/enchant/punch.md) | `ENCHANT:minecraft:punch` | `ENCHANT_RITUAL` | `magic` |
| 81 | [`enchant/quick_charge.json`](rituals/cards/enchant/quick_charge.md) | `ENCHANT:minecraft:quick_charge` | `ENCHANT_RITUAL` | `magic` |
| 82 | [`enchant/respiration.json`](rituals/cards/enchant/respiration.md) | `ENCHANT:minecraft:respiration` | `ENCHANT_RITUAL` | `magic` |
| 83 | [`enchant/riptide.json`](rituals/cards/enchant/riptide.md) | `ENCHANT:minecraft:riptide` | `ENCHANT_RITUAL` | `magic` |
| 84 | [`enchant/royalty.json`](rituals/cards/enchant/royalty.md) | `ENCHANT:goety:royalty` | `ENCHANT_RITUAL` | `magic` |
| 85 | [`enchant/sharpness.json`](rituals/cards/enchant/sharpness.md) | `ENCHANT:minecraft:sharpness` | `ENCHANT_RITUAL` | `magic` |
| 86 | [`enchant/silk_touch.json`](rituals/cards/enchant/silk_touch.md) | `ENCHANT:minecraft:silk_touch` | `ENCHANT_RITUAL` | `magic` |
| 87 | [`enchant/smite.json`](rituals/cards/enchant/smite.md) | `ENCHANT:minecraft:smite` | `ENCHANT_RITUAL` | `magic` |
| 88 | [`enchant/sweeping_edge.json`](rituals/cards/enchant/sweeping_edge.md) | `ENCHANT:minecraft:sweeping_edge` | `ENCHANT_RITUAL` | `magic` |
| 89 | [`enchant/thorns.json`](rituals/cards/enchant/thorns.md) | `ENCHANT:minecraft:thorns` | `ENCHANT_RITUAL` | `magic` |
| 90 | [`enchant/unbreaking.json`](rituals/cards/enchant/unbreaking.md) | `ENCHANT:minecraft:unbreaking` | `ENCHANT_RITUAL` | `magic` |
| 91 | [`enchant/vanishing_curse.json`](rituals/cards/enchant/vanishing_curse.md) | `ENCHANT:minecraft:vanishing_curse` | `ENCHANT_RITUAL` | `magic` |
| 92 | [`esoteric_tesseract.json`](rituals/cards/esoteric_tesseract.md) | `RITUAL_RESULT:goety:esoteric_tesseract` | `OTHER_RITUAL` | `forge` |
| 93 | [`feline_amulet.json`](rituals/cards/feline_amulet.md) | `RITUAL_RESULT:goety:feline_amulet` | `OTHER_RITUAL` | `geoturgy` |
| 94 | [`forbidden_piece.json`](rituals/cards/forbidden_piece.md) | `RITUAL_RESULT:goety:forbidden_piece` | `OTHER_RITUAL` | `necroturgy` |
| 95 | [`frost_crown.json`](rituals/cards/frost_crown.md) | `RITUAL_RESULT:goety:frost_crown` | `OTHER_RITUAL` | `frost` |
| 96 | [`frost_robe.json`](rituals/cards/frost_robe.md) | `RITUAL_RESULT:goety:frost_robe` | `OTHER_RITUAL` | `frost` |
| 97 | [`frost_staff.json`](rituals/cards/frost_staff.md) | `RITUAL_RESULT:goety:frost_staff` | `OTHER_RITUAL` | `frost` |
| 98 | [`geo_staff.json`](rituals/cards/geo_staff.md) | `RITUAL_RESULT:goety:geo_staff` | `OTHER_RITUAL` | `geoturgy` |
| 99 | [`gold_ravager_armor.json`](rituals/cards/gold_ravager_armor.md) | `RITUAL_RESULT:goety:gold_ravager_armor` | `OTHER_RITUAL` | `forge` |
| 100 | [`gold_trampler_armor.json`](rituals/cards/gold_trampler_armor.md) | `RITUAL_RESULT:goety:gold_trampler_armor` | `OTHER_RITUAL` | `forge` |
| 101 | [`grand_robe.json`](rituals/cards/grand_robe.md) | `RITUAL_RESULT:goety:grand_robe` | `OTHER_RITUAL` | `magic` |
| 102 | [`grand_turban.json`](rituals/cards/grand_turban.md) | `RITUAL_RESULT:goety:grand_turban` | `OTHER_RITUAL` | `magic` |
| 103 | [`grave_glove.json`](rituals/cards/grave_glove.md) | `RITUAL_RESULT:goety:grave_glove` | `OTHER_RITUAL` | `necroturgy` |
| 104 | [`graverobber_shovel.json`](rituals/cards/graverobber_shovel.md) | `RITUAL_RESULT:goety:graverobber_shovel` | `OTHER_RITUAL` | `forge` |
| 105 | [`great_hammer.json`](rituals/cards/great_hammer.md) | `RITUAL_RESULT:goety:great_hammer` | `OTHER_RITUAL` | `forge` |
| 106 | [`grim_infuser.json`](rituals/cards/grim_infuser.md) | `RITUAL_RESULT:goety:grim_infuser` | `OTHER_RITUAL` | `forge` |
| 107 | [`haunted/haunted_armor_stand.json`](rituals/cards/haunted/haunted_armor_stand.md) | `RITUAL_RESULT:goety:haunted_armor_stand` | `OTHER_RITUAL` | `necroturgy` |
| 108 | [`haunted/haunted_broom.json`](rituals/cards/haunted/haunted_broom.md) | `RITUAL_RESULT:goety:haunted_broom` | `OTHER_RITUAL` | `sky` |
| 109 | [`haunted/haunted_jug.json`](rituals/cards/haunted/haunted_jug.md) | `RITUAL_RESULT:goety:haunted_jug` | `OTHER_RITUAL` | `animation` |
| 110 | [`haunted/haunted_mirror.json`](rituals/cards/haunted/haunted_mirror.md) | `RITUAL_RESULT:goety:haunted_mirror` | `OTHER_RITUAL` | `necroturgy` |
| 111 | [`heart_of_the_night.json`](rituals/cards/heart_of_the_night.md) | `RITUAL_RESULT:goety:heart_of_the_night` | `OTHER_RITUAL` | `necroturgy` |
| 112 | [`hook_bell.json`](rituals/cards/hook_bell.md) | `RITUAL_RESULT:goety:hook_bell` | `OTHER_RITUAL` | `forge` |
| 113 | [`hunger_core.json`](rituals/cards/hunger_core.md) | `RITUAL_RESULT:goety:hunger_core` | `OTHER_RITUAL` | `animation` |
| 114 | [`hungry_dagger.json`](rituals/cards/hungry_dagger.md) | `RITUAL_RESULT:goety:hungry_dagger` | `OTHER_RITUAL` | `forge` |
| 115 | [`hunters_bow.json`](rituals/cards/hunters_bow.md) | `RITUAL_RESULT:goety:hunters_bow` | `OTHER_RITUAL` | `forge` |
| 116 | [`infernal_tome.json`](rituals/cards/infernal_tome.md) | `RITUAL_RESULT:goety:infernal_tome` | `OTHER_RITUAL` | `adept_nether` |
| 117 | [`iron_ravager_armor.json`](rituals/cards/iron_ravager_armor.md) | `RITUAL_RESULT:goety:iron_ravager_armor` | `OTHER_RITUAL` | `forge` |
| 118 | [`iron_trampler_armor.json`](rituals/cards/iron_trampler_armor.md) | `RITUAL_RESULT:goety:iron_trampler_armor` | `OTHER_RITUAL` | `forge` |
| 119 | [`locate/ancient_city.json`](rituals/cards/locate/ancient_city.md) | `LOCATE:ancient_city` | `LOCATE_RITUAL` | `divination` |
| 120 | [`locate/blighted_shack.json`](rituals/cards/locate/blighted_shack.md) | `LOCATE:blighted_shack` | `LOCATE_RITUAL` | `divination` |
| 121 | [`locate/crypt.json`](rituals/cards/locate/crypt.md) | `LOCATE:crypt` | `LOCATE_RITUAL` | `divination` |
| 122 | [`locate/dark_manor.json`](rituals/cards/locate/dark_manor.md) | `LOCATE:dark_manor` | `LOCATE_RITUAL` | `divination` |
| 123 | [`locate/desert_pyramid.json`](rituals/cards/locate/desert_pyramid.md) | `LOCATE:desert_pyramid` | `LOCATE_RITUAL` | `divination` |
| 124 | [`locate/end/end_city.json`](rituals/cards/locate/end/end_city.md) | `LOCATE:end_city` | `LOCATE_RITUAL` | `divination` |
| 125 | [`locate/end/final_terminal.json`](rituals/cards/locate/end/final_terminal.md) | `LOCATE:final_terminal` | `LOCATE_RITUAL` | `divination` |
| 126 | [`locate/graveyard.json`](rituals/cards/locate/graveyard.md) | `LOCATE:graveyard` | `LOCATE_RITUAL` | `divination` |
| 127 | [`locate/jungle_temple.json`](rituals/cards/locate/jungle_temple.md) | `LOCATE:jungle_temple` | `LOCATE_RITUAL` | `divination` |
| 128 | [`locate/nether/bastion_remnant.json`](rituals/cards/locate/nether/bastion_remnant.md) | `LOCATE:bastion_remnant` | `LOCATE_RITUAL` | `divination` |
| 129 | [`locate/nether/fortress.json`](rituals/cards/locate/nether/fortress.md) | `LOCATE:fortress` | `LOCATE_RITUAL` | `divination` |
| 130 | [`locate/ominous_blacksmith.json`](rituals/cards/locate/ominous_blacksmith.md) | `LOCATE:ominous_blacksmith` | `LOCATE_RITUAL` | `divination` |
| 131 | [`locate/pillager_outpost.json`](rituals/cards/locate/pillager_outpost.md) | `LOCATE:pillager_outpost` | `LOCATE_RITUAL` | `divination` |
| 132 | [`locate/ruined_monastery.json`](rituals/cards/locate/ruined_monastery.md) | `LOCATE:ruined_monastery` | `LOCATE_RITUAL` | `divination` |
| 133 | [`locate/sorcerous_keep.json`](rituals/cards/locate/sorcerous_keep.md) | `LOCATE:sorcerous_keep` | `LOCATE_RITUAL` | `divination` |
| 134 | [`locate/spider_den.json`](rituals/cards/locate/spider_den.md) | `LOCATE:spider_den` | `LOCATE_RITUAL` | `divination` |
| 135 | [`locate/stronghold.json`](rituals/cards/locate/stronghold.md) | `LOCATE:stronghold` | `LOCATE_RITUAL` | `divination` |
| 136 | [`locate/wind_shrine.json`](rituals/cards/locate/wind_shrine.md) | `LOCATE:wind_shrine` | `LOCATE_RITUAL` | `divination` |
| 137 | [`locate/woodland_mansion.json`](rituals/cards/locate/woodland_mansion.md) | `LOCATE:woodland_mansion` | `LOCATE_RITUAL` | `divination` |
| 138 | [`mystic_core.json`](rituals/cards/mystic_core.md) | `RITUAL_RESULT:goety:mystic_core` | `OTHER_RITUAL` | `magic` |
| 139 | [`nameless_cape.json`](rituals/cards/nameless_cape.md) | `RITUAL_RESULT:goety:nameless_cape` | `OTHER_RITUAL` | `necroturgy` |
| 140 | [`nameless_crown.json`](rituals/cards/nameless_crown.md) | `RITUAL_RESULT:goety:nameless_crown` | `OTHER_RITUAL` | `necroturgy` |
| 141 | [`nameless_staff.json`](rituals/cards/nameless_staff.md) | `RITUAL_RESULT:goety:nameless_staff` | `OTHER_RITUAL` | `necroturgy` |
| 142 | [`necro_brazier.json`](rituals/cards/necro_brazier.md) | `RITUAL_RESULT:goety:necro_brazier` | `OTHER_RITUAL` | `forge` |
| 143 | [`necro_cape.json`](rituals/cards/necro_cape.md) | `RITUAL_RESULT:goety:necro_cape` | `OTHER_RITUAL` | `necroturgy` |
| 144 | [`necro_crown.json`](rituals/cards/necro_crown.md) | `RITUAL_RESULT:goety:necro_crown` | `OTHER_RITUAL` | `necroturgy` |
| 145 | [`necro_staff.json`](rituals/cards/necro_staff.md) | `RITUAL_RESULT:goety:necro_staff` | `OTHER_RITUAL` | `necroturgy` |
| 146 | [`nether_crown.json`](rituals/cards/nether_crown.md) | `RITUAL_RESULT:goety:nether_crown` | `OTHER_RITUAL` | `expert_nether` |
| 147 | [`nether_robe.json`](rituals/cards/nether_robe.md) | `RITUAL_RESULT:goety:nether_robe` | `OTHER_RITUAL` | `expert_nether` |
| 148 | [`nether_staff.json`](rituals/cards/nether_staff.md) | `RITUAL_RESULT:goety:nether_staff` | `OTHER_RITUAL` | `expert_nether` |
| 149 | [`netherite_ravager_armor.json`](rituals/cards/netherite_ravager_armor.md) | `RITUAL_RESULT:goety:netherite_ravager_armor` | `OTHER_RITUAL` | `forge` |
| 150 | [`netherite_trampler_armor.json`](rituals/cards/netherite_trampler_armor.md) | `RITUAL_RESULT:goety:netherite_trampler_armor` | `OTHER_RITUAL` | `forge` |
| 151 | [`ominous_charm.json`](rituals/cards/ominous_charm.md) | `RITUAL_RESULT:goety:ominous_charm` | `OTHER_RITUAL` | `geoturgy` |
| 152 | [`ominous_idol.json`](rituals/cards/ominous_idol.md) | `RITUAL_RESULT:goety:ominous_idol` | `OTHER_RITUAL` | `forge` |
| 153 | [`ominous_pyre.json`](rituals/cards/ominous_pyre.md) | `RITUAL_RESULT:goety:ominous_pyre` | `OTHER_RITUAL` | `forge` |
| 154 | [`ominous_saddle.json`](rituals/cards/ominous_saddle.md) | `RITUAL_RESULT:goety:ominous_saddle` | `OTHER_RITUAL` | `forge` |
| 155 | [`ominous_staff.json`](rituals/cards/ominous_staff.md) | `RITUAL_RESULT:goety:ominous_staff` | `OTHER_RITUAL` | `magic` |
| 156 | [`pendant_of_hunger.json`](rituals/cards/pendant_of_hunger.md) | `RITUAL_RESULT:goety:pendant_of_hunger` | `OTHER_RITUAL` | `geoturgy` |
| 157 | [`philosophers_mace.json`](rituals/cards/philosophers_mace.md) | `RITUAL_RESULT:goety:philosophers_mace` | `OTHER_RITUAL` | `expert_nether` |
| 158 | [`philosophers_stone.json`](rituals/cards/philosophers_stone.md) | `RITUAL_RESULT:goety:philosophers_stone` | `OTHER_RITUAL` | `magic` |
| 159 | [`rampaging_axe.json`](rituals/cards/rampaging_axe.md) | `RITUAL_RESULT:goety:rampaging_axe` | `OTHER_RITUAL` | `forge` |
| 160 | [`reinforced_redstone_block.json`](rituals/cards/reinforced_redstone_block.md) | `RITUAL_RESULT:goety:reinforced_redstone_block` | `OTHER_RITUAL` | `forge` |
| 161 | [`resonance_crystal.json`](rituals/cards/resonance_crystal.md) | `RITUAL_RESULT:goety:resonance_crystal` | `OTHER_RITUAL` | `sky` |
| 162 | [`ring_of_force.json`](rituals/cards/ring_of_force.md) | `RITUAL_RESULT:goety:ring_of_force` | `OTHER_RITUAL` | `magic` |
| 163 | [`ring_of_the_dragon.json`](rituals/cards/ring_of_the_dragon.md) | `RITUAL_RESULT:goety:ring_of_the_dragon` | `OTHER_RITUAL` | `geoturgy` |
| 164 | [`ring_of_the_forge.json`](rituals/cards/ring_of_the_forge.md) | `RITUAL_RESULT:goety:ring_of_the_forge` | `OTHER_RITUAL` | `geoturgy` |
| 165 | [`ring_of_thirst.json`](rituals/cards/ring_of_thirst.md) | `RITUAL_RESULT:goety:ring_of_thirst` | `OTHER_RITUAL` | `geoturgy` |
| 166 | [`ring_of_want.json`](rituals/cards/ring_of_want.md) | `RITUAL_RESULT:goety:ring_of_want` | `OTHER_RITUAL` | `geoturgy` |
| 167 | [`sculk_grower.json`](rituals/cards/sculk_grower.md) | `RITUAL_RESULT:goety:sculk_grower` | `OTHER_RITUAL` | `forge` |
| 168 | [`sea_amulet.json`](rituals/cards/sea_amulet.md) | `RITUAL_RESULT:goety:sea_amulet` | `OTHER_RITUAL` | `deep` |
| 169 | [`shade/shade_gravestone.json`](rituals/cards/shade/shade_gravestone.md) | `RITUAL_RESULT:goety:shade_gravestone` | `OTHER_RITUAL` | `necroturgy` |
| 170 | [`shade/shade_ossuary.json`](rituals/cards/shade/shade_ossuary.md) | `RITUAL_RESULT:goety:shade_ossuary` | `OTHER_RITUAL` | `necroturgy` |
| 171 | [`shriek_obelisk.json`](rituals/cards/shriek_obelisk.md) | `RITUAL_RESULT:goety:shriek_obelisk` | `OTHER_RITUAL` | `forge` |
| 172 | [`soul_absorber.json`](rituals/cards/soul_absorber.md) | `RITUAL_RESULT:goety:soul_absorber` | `OTHER_RITUAL` | `forge` |
| 173 | [`soul_mender.json`](rituals/cards/soul_mender.md) | `RITUAL_RESULT:goety:soul_mender` | `OTHER_RITUAL` | `forge` |
| 174 | [`spiteful_belt.json`](rituals/cards/spiteful_belt.md) | `RITUAL_RESULT:goety:spiteful_belt` | `OTHER_RITUAL` | `geoturgy` |
| 175 | [`star_amulet.json`](rituals/cards/star_amulet.md) | `RITUAL_RESULT:goety:star_amulet` | `OTHER_RITUAL` | `geoturgy` |
| 176 | [`storm_crown.json`](rituals/cards/storm_crown.md) | `RITUAL_RESULT:goety:storm_crown` | `OTHER_RITUAL` | `storm` |
| 177 | [`storm_robe.json`](rituals/cards/storm_robe.md) | `RITUAL_RESULT:goety:storm_robe` | `OTHER_RITUAL` | `storm` |
| 178 | [`storm_staff.json`](rituals/cards/storm_staff.md) | `RITUAL_RESULT:goety:storm_staff` | `OTHER_RITUAL` | `storm` |
| 179 | [`summon_apostle.json`](rituals/cards/summon_apostle.md) | `SUMMON:goety:summon_apostle` | `SUMMON_RITUAL` | `sabbath` |
| 180 | [`summon_storm.json`](rituals/cards/summon_storm.md) | `SUMMON:goety:storm_util` | `SUMMON_RITUAL` | `sky` |
| 181 | [`targeting_monocle.json`](rituals/cards/targeting_monocle.md) | `RITUAL_RESULT:goety:targeting_monocle` | `OTHER_RITUAL` | `geoturgy` |
| 182 | [`teleport_ritual.json`](rituals/cards/teleport_ritual.md) | `RITUAL_PATH:teleport_ritual.json` | `OTHER_RITUAL` | `magic` |
| 183 | [`terminus_scroll.json`](rituals/cards/terminus_scroll.md) | `RITUAL_RESULT:goety:terminus_scroll` | `OTHER_RITUAL` | `forge` |
| 184 | [`thrall/summon_bear_servant_thrall.json`](rituals/cards/thrall/summon_bear_servant_thrall.md) | `SUMMON:goety:bear_servant` | `THRALL_SUMMON_RITUAL` | `overgrown` |
| 185 | [`thrall/summon_black_wolf_thrall.json`](rituals/cards/thrall/summon_black_wolf_thrall.md) | `SUMMON:goety:black_wolf` | `THRALL_SUMMON_RITUAL` | `overgrown` |
| 186 | [`thrall/summon_blackguard_thrall.json`](rituals/cards/thrall/summon_blackguard_thrall.md) | `SUMMON:goety:blackguard_servant` | `THRALL_SUMMON_RITUAL` | `necroturgy` |
| 187 | [`thrall/summon_blastling_thrall.json`](rituals/cards/thrall/summon_blastling_thrall.md) | `SUMMON:goety:blastling_servant` | `THRALL_SUMMON_RITUAL` | `end` |
| 188 | [`thrall/summon_blaze_servant_thrall.json`](rituals/cards/thrall/summon_blaze_servant_thrall.md) | `SUMMON:goety:blaze_servant` | `THRALL_SUMMON_RITUAL` | `expert_nether` |
| 189 | [`thrall/summon_bound_cryologer.json`](rituals/cards/thrall/summon_bound_cryologer.md) | `SUMMON:goety:bound_cryologer` | `THRALL_SUMMON_RITUAL` | `necroturgy` |
| 190 | [`thrall/summon_bound_evoker.json`](rituals/cards/thrall/summon_bound_evoker.md) | `SUMMON:goety:bound_evoker` | `THRALL_SUMMON_RITUAL` | `necroturgy` |
| 191 | [`thrall/summon_bound_geomancer.json`](rituals/cards/thrall/summon_bound_geomancer.md) | `SUMMON:goety:bound_geomancer` | `THRALL_SUMMON_RITUAL` | `necroturgy` |
| 192 | [`thrall/summon_bound_iceologer.json`](rituals/cards/thrall/summon_bound_iceologer.md) | `SUMMON:goety:bound_iceologer` | `THRALL_SUMMON_RITUAL` | `necroturgy` |
| 193 | [`thrall/summon_bound_storm_caster.json`](rituals/cards/thrall/summon_bound_storm_caster.md) | `SUMMON:goety:bound_storm_caster` | `THRALL_SUMMON_RITUAL` | `necroturgy` |
| 194 | [`thrall/summon_bound_wind_caller.json`](rituals/cards/thrall/summon_bound_wind_caller.md) | `SUMMON:goety:bound_wind_caller` | `THRALL_SUMMON_RITUAL` | `necroturgy` |
| 195 | [`thrall/summon_carrion_fly_thrall.json`](rituals/cards/thrall/summon_carrion_fly_thrall.md) | `SUMMON:goety:carrion_fly` | `THRALL_SUMMON_RITUAL` | `overgrown` |
| 196 | [`thrall/summon_ghast_servant_thrall.json`](rituals/cards/thrall/summon_ghast_servant_thrall.md) | `SUMMON:goety:ghast_servant` | `THRALL_SUMMON_RITUAL` | `adept_nether` |
| 197 | [`thrall/summon_gnasher_thrall.json`](rituals/cards/thrall/summon_gnasher_thrall.md) | `SUMMON:goety:gnasher` | `THRALL_SUMMON_RITUAL` | `deep` |
| 198 | [`thrall/summon_guardian_servant_thrall.json`](rituals/cards/thrall/summon_guardian_servant_thrall.md) | `SUMMON:goety:guardian_servant` | `THRALL_SUMMON_RITUAL` | `deep` |
| 199 | [`thrall/summon_hellhound_thrall.json`](rituals/cards/thrall/summon_hellhound_thrall.md) | `SUMMON:goety:hellhound` | `THRALL_SUMMON_RITUAL` | `adept_nether` |
| 200 | [`thrall/summon_hoglin_servant_thrall.json`](rituals/cards/thrall/summon_hoglin_servant_thrall.md) | `SUMMON:goety:hoglin_servant` | `THRALL_SUMMON_RITUAL` | `adept_nether` |
| 201 | [`thrall/summon_ministrosity_thrall.json`](rituals/cards/thrall/summon_ministrosity_thrall.md) | `SUMMON:goety:stone_ministrosity` | `THRALL_SUMMON_RITUAL` | `geoturgy` |
| 202 | [`thrall/summon_phantom_servant_thrall.json`](rituals/cards/thrall/summon_phantom_servant_thrall.md) | `SUMMON:goety:phantom_servant` | `THRALL_SUMMON_RITUAL` | `necroturgy` |
| 203 | [`thrall/summon_reaper_thrall.json`](rituals/cards/thrall/summon_reaper_thrall.md) | `SUMMON:goety:reaper_servant` | `THRALL_SUMMON_RITUAL` | `necroturgy` |
| 204 | [`thrall/summon_redstone_ministrosity_thrall.json`](rituals/cards/thrall/summon_redstone_ministrosity_thrall.md) | `SUMMON:goety:redstone_ministrosity` | `THRALL_SUMMON_RITUAL` | `geoturgy` |
| 205 | [`thrall/summon_skeleton_thrall.json`](rituals/cards/thrall/summon_skeleton_thrall.md) | `SUMMON:goety:skeleton_servant` | `THRALL_SUMMON_RITUAL` | `necroturgy` |
| 206 | [`thrall/summon_skeleton_wolf_thrall.json`](rituals/cards/thrall/summon_skeleton_wolf_thrall.md) | `SUMMON:goety:skeleton_wolf` | `THRALL_SUMMON_RITUAL` | `necroturgy` |
| 207 | [`thrall/summon_snapper_thrall.json`](rituals/cards/thrall/summon_snapper_thrall.md) | `SUMMON:goety:snapper` | `THRALL_SUMMON_RITUAL` | `deep` |
| 208 | [`thrall/summon_snareling_thrall.json`](rituals/cards/thrall/summon_snareling_thrall.md) | `SUMMON:goety:snareling_servant` | `THRALL_SUMMON_RITUAL` | `end` |
| 209 | [`thrall/summon_sprite_thrall.json`](rituals/cards/thrall/summon_sprite_thrall.md) | `SUMMON:goety:sprite` | `THRALL_SUMMON_RITUAL` | `storm` |
| 210 | [`thrall/summon_stormhound_thrall.json`](rituals/cards/thrall/summon_stormhound_thrall.md) | `SUMMON:goety:stormhound` | `THRALL_SUMMON_RITUAL` | `storm` |
| 211 | [`thrall/summon_twilight_goat_thrall.json`](rituals/cards/thrall/summon_twilight_goat_thrall.md) | `SUMMON:goety:twilight_goat` | `THRALL_SUMMON_RITUAL` | `sky` |
| 212 | [`thrall/summon_vanguard_thrall.json`](rituals/cards/thrall/summon_vanguard_thrall.md) | `SUMMON:goety:vanguard_servant` | `THRALL_SUMMON_RITUAL` | `necroturgy` |
| 213 | [`thrall/summon_watchling_thrall.json`](rituals/cards/thrall/summon_watchling_thrall.md) | `SUMMON:goety:watchling_servant` | `THRALL_SUMMON_RITUAL` | `end` |
| 214 | [`thrall/summon_winter_wolf_thrall.json`](rituals/cards/thrall/summon_winter_wolf_thrall.md) | `SUMMON:goety:winter_wolf` | `THRALL_SUMMON_RITUAL` | `frost` |
| 215 | [`thrall/summon_wither_skeleton_thrall.json`](rituals/cards/thrall/summon_wither_skeleton_thrall.md) | `SUMMON:goety:wither_skeleton_servant` | `THRALL_SUMMON_RITUAL` | `expert_nether` |
| 216 | [`thrall/summon_wraith_thrall.json`](rituals/cards/thrall/summon_wraith_thrall.md) | `SUMMON:goety:wraith_servant` | `THRALL_SUMMON_RITUAL` | `necroturgy` |
| 217 | [`thrall/summon_zombie_thrall.json`](rituals/cards/thrall/summon_zombie_thrall.md) | `SUMMON:goety:zombie_servant` | `THRALL_SUMMON_RITUAL` | `necroturgy` |
| 218 | [`thrash_glove.json`](rituals/cards/thrash_glove.md) | `RITUAL_RESULT:goety:thrash_glove` | `OTHER_RITUAL` | `forge` |
| 219 | [`undeath_potion.json`](rituals/cards/undeath_potion.md) | `RITUAL_RESULT:goety:undeath_potion` | `OTHER_RITUAL` | `necroturgy` |
| 220 | [`unholy_fabric.json`](rituals/cards/unholy_fabric.md) | `RITUAL_RESULT:goety:unholy_fabric` | `OTHER_RITUAL` | `expert_nether` |
| 221 | [`unholy_hat.json`](rituals/cards/unholy_hat.md) | `RITUAL_RESULT:goety:unholy_hat` | `OTHER_RITUAL` | `expert_nether` |
| 222 | [`unholy_robe.json`](rituals/cards/unholy_robe.md) | `RITUAL_RESULT:goety:unholy_robe` | `OTHER_RITUAL` | `expert_nether` |
| 223 | [`void_crown.json`](rituals/cards/void_crown.md) | `RITUAL_RESULT:goety:void_crown` | `OTHER_RITUAL` | `end` |
| 224 | [`void_robe.json`](rituals/cards/void_robe.md) | `RITUAL_RESULT:goety:void_robe` | `OTHER_RITUAL` | `end` |
| 225 | [`void_staff.json`](rituals/cards/void_staff.md) | `RITUAL_RESULT:goety:void_staff` | `OTHER_RITUAL` | `end` |
| 226 | [`warg_cursed_armor.json`](rituals/cards/warg_cursed_armor.md) | `RITUAL_RESULT:goety:warg_cursed_armor` | `OTHER_RITUAL` | `forge` |
| 227 | [`warg_dark_armor.json`](rituals/cards/warg_dark_armor.md) | `RITUAL_RESULT:goety:warg_dark_armor` | `OTHER_RITUAL` | `forge` |
| 228 | [`warlock_robe.json`](rituals/cards/warlock_robe.md) | `RITUAL_RESULT:goety:warlock_robe` | `OTHER_RITUAL` | `adept_nether` |
| 229 | [`wayfarers_belt.json`](rituals/cards/wayfarers_belt.md) | `RITUAL_RESULT:goety:wayfarers_belt` | `OTHER_RITUAL` | `sky` |
| 230 | [`wild_crown.json`](rituals/cards/wild_crown.md) | `RITUAL_RESULT:goety:wild_crown` | `OTHER_RITUAL` | `overgrown` |
| 231 | [`wild_robe.json`](rituals/cards/wild_robe.md) | `RITUAL_RESULT:goety:wild_robe` | `OTHER_RITUAL` | `overgrown` |
| 232 | [`wild_staff.json`](rituals/cards/wild_staff.md) | `RITUAL_RESULT:goety:wild_staff` | `OTHER_RITUAL` | `overgrown` |
| 233 | [`wind_core.json`](rituals/cards/wind_core.md) | `RITUAL_RESULT:goety:wind_core` | `OTHER_RITUAL` | `sky` |
| 234 | [`wind_crown.json`](rituals/cards/wind_crown.md) | `RITUAL_RESULT:goety:wind_crown` | `OTHER_RITUAL` | `sky` |
| 235 | [`wind_robe.json`](rituals/cards/wind_robe.md) | `RITUAL_RESULT:goety:wind_robe` | `OTHER_RITUAL` | `sky` |
| 236 | [`wind_staff.json`](rituals/cards/wind_staff.md) | `RITUAL_RESULT:goety:wind_staff` | `OTHER_RITUAL` | `sky` |
| 237 | [`witch_robe.json`](rituals/cards/witch_robe.md) | `RITUAL_RESULT:goety:witch_robe` | `OTHER_RITUAL` | `storm` |
| 238 | [`wolf_totem.json`](rituals/cards/wolf_totem.md) | `RITUAL_RESULT:goety:wolf_totem` | `OTHER_RITUAL` | `overgrown` |

## Fronteiras obrigatórias

- Os 83 recursos de obtenção de Focuses não contam como rituais adicionais; as [123 fichas de Focus](FOCUS-CARDS-3.1.4.md) mantêm identidades separadas.
- Os quatro grupos de alternativas de receita e os 17 recursos incompatíveis com dependências do pack permanecem **excluídos** e não aparecem como fichas `COUNTED_EXACT`.
- Autoridade dos rituais/ritual costs/ownership/permanência/servants permanece em Goety. Black Arcana não implementa um segundo altar/custo/efeito para esses 238 roots nem promove Stage 06.05 por documentação.
