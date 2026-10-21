# Ars Elemancy 1.18.3 — matriz causal de equipamentos para perks

**Checkpoint 17/10/2026, PR #825 draft.** Fichas novas por família de escola (equipamento/atributos), sem novas identidades mágicas. `ars_elemancy-1.21.1-1.18.3.jar` presente na modlist; SHA-1 físico documentado `f7e01437c86fc74e2abb2ad93554dc20c30b214b`; source release-aligned `Lyrellion/Ars-Elemancy@dfb18286106aca1ca39a9b0053d64a1ef5041751`. Registry, callbacks de Curios, Armor PerkSlots e aplicação local são **SOURCE_CAUSALITY**, não paridade binária integral nem QA de jogo. Ars Nouveau 5.13.1, Ars Elemental 0.7.10.1, Curios e Sauce são hosts e versões físicas relevantes, não contratos de mutação automaticamente aprovados.

## Duas barras distintas — progresso auditável

- **GLOBAL — —%**: piso documental da série vigente **1.857 objetos semânticos / 1.855 estritos**, denominador total global aberto; nesta etapa **+0 spells e +0 perks implementadas**.
- **ARS ELEMANCY — 7/7 (100%)** famílias de equipamento com ficha causal source-pinned; universo de registry já documentado **105/105 items** (7 foci, 7 bangles, 7 essências, 84 armaduras), **0 glyphs e 0 perks Ars próprias**. Homologação de atributos em runtime/client/provider = ⚠️ PENDENTE; adapter RPG = ⛔ nenhum. 7/7 não representa 105/105 verificações individuais de mods físicos.

## Famílias (foco, bangle, armadura por escola)

| Família | Escola | Ficha | Bangle/foco e condições relevantes | Foco ambiental | WeaknessMap do source |
|---|---|---|---|---|---|
| `tempest` | Air + Water | [tempest](equipment/tempest.md) | +0.06 Movement Speed, +1.2 Attack Knockback; +0.5 Swim Speed, condicional +0.035 Movement Speed na água/chuva | Air (Shocked/Y>200), Water (úmido/natação) | air→earth; water→air |
| `cinder` | Air + Fire | [cinder](equipment/cinder.md) | +0.06 Movement Speed, +1.2 Attack Knockback; condicional +0.035 Movement Speed se biome temperature >1.8 | Air (Shocked/Y>200), Fire (chamas/lava) | air→earth; fire→water |
| `silt` | Air + Earth | [silt](equipment/silt.md) | +0.06 Movement Speed, +1.2 Attack Knockback e +0.3 Knockback Resistance; foco Earth +0.2 Knockback Resistance | Air (Shocked/Y>200), Earth (Y<0) | air→earth; earth→fire |
| `mire` | Earth + Water | [mire](equipment/mire.md) | +0.3 Knockback Resistance, +0.5 Swim Speed, condicional +0.035 Movement Speed na água/chuva; foco Earth +0.2 Knockback Resistance | Earth (Y<0), Water (úmido/natação) | earth→fire; water→air |
| `vapor` | Fire + Water | [vapor](equipment/vapor.md) | Condicional +0.035 Movement Speed em bioma quente, +0.5 Swim Speed e +0.035 Movement Speed na água/chuva | Fire (chamas/lava), Water (úmido/natação) | fire→water; water→air |
| `lava` | Fire + Earth | [lava](equipment/lava.md) | Condicional +0.035 Movement Speed em bioma quente, +0.3 Knockback Resistance; foco Earth +0.2 Knockback Resistance | Fire (chamas/lava), Earth (Y<0) | fire→water; earth→fire |
| `elemancer` | SpellSchools.ELEMENTAL | [elemancer](equipment/elemancer.md) | ⚠️ RAMOS CONDICIONAIS: lista de subschools do host não inspecionada aqui; não imputar somatório das quatro escolas | Dependente do SpellSchools.ELEMENTAL.getSubSchools() efetivo | N/A — branch elemental direta |

Cada uma das sete fichas enumera **15 IDs de item** (`1 focus + 1 essence + 1 bangle + 12 armor`). O family-count 7 deriva das famílias de escolas/gear, não de 7 spells. Os **105 itens já constavam do registry** e não devem ser somados ao total semântico de spells.

## Regras transversais de perk

**Curios foci:** `ElemancyFocus.applyItemModifiers` chama `SpellStats.Builder.addAmplification(getBoostMultiplier()×2)` quando `element.isPartOfSchool(spellPart)`. `getBoostMultiplier` lê config específica por escola (default 1.0), e `getDiscount()` retorna `elemental_maj_focus_discount` default 0.25. Essas constantes são input para as fórmulas Ars/Ars Elemental — **não** são automaticamente +200% de damage nem prova de 25% líquido de mana. `curioTick` avalia efeitos a cada 20 ticks server-side. Regen/status de 60/120/200 ticks deve ser contado como provider-effects, não novos casts ou XP passivo.

**Curios bangles:** school.subSchools determina `ADD_VALUE` aos atributos, com condições de temperatura/água. Alterar `AttributeInstance` diretamente no RPG sem identidades/ordem/cleanup homologados pode duplicar buffs e causar interferência com Epic Fight; manter `NATIVE_ATTRIBUTE` como authority do provider.

**Armaduras:** `ElemancyArmor` adiciona por peça `MAX_MANA+100` e `MANA_REGEN_BONUS+4`; `getManaDiscount` usa `Mth.ceil(getDiscount(spell.unsafeList()))` via implementação herdada. Classes:
- Light: por subescola **+12.5 defense, +2 power, −25 defense** na escola `weaknessMap`;
- Medium: por subescola **+25 defense, +1 power, −12.5 defense** na fraqueza;
- Heavy: por subescola **+50 defense, +0.5 power, +25 defense** na fraqueza, *positivo no código*, não corrigir por interpretação;
- Elemancer usa branch `SpellSchools.ELEMENTAL`: Light **+12.5/+2**, Medium **+25/+1**, Heavy **+75/+0.5**, sem iterar weaknessMap nesse branch.

**PerkSlots de Ars:** `ars_elemancy:four/five/six` são **valores de slot** (4/5/6), não nós de progressão RPG nem buffs próprios. `ArsNouveauRegistry.registerGlyphs/registerPerks` vazio. Sem adapter para mover slots entre providers.

**DamageTypes:** quatro `TagKey<DamageType>` `fire_damage/water_damage/earth_damage/air_damage` existem na fonte, mas não são prova de casts, dano elemental novo ou host registry preenchido. Elemental tags, power e defense precisam ser lidos/medidos na versão física.

## Fonte e limites de prova

- [ModRegistry — escolas e tags](https://github.com/Lyrellion/Ars-Elemancy/blob/dfb18286106aca1ca39a9b0053d64a1ef5041751/src/main/java/lyrellion/ars_elemancy/registry/ModRegistry.java#L42-L54).
- [ModItems — sete foci/bangles e armor](https://github.com/Lyrellion/Ars-Elemancy/blob/dfb18286106aca1ca39a9b0053d64a1ef5041751/src/main/java/lyrellion/ars_elemancy/registry/ModItems.java#L24-L92).
- [ElemancyFocus — callbacks, buffs e desconto](https://github.com/Lyrellion/Ars-Elemancy/blob/dfb18286106aca1ca39a9b0053d64a1ef5041751/src/main/java/lyrellion/ars_elemancy/common/items/foci/ElemancyFocus.java#L34-L115).
- [ElemancyBangle — atributo por subschool](https://github.com/Lyrellion/Ars-Elemancy/blob/dfb18286106aca1ca39a9b0053d64a1ef5041751/src/main/java/lyrellion/ars_elemancy/common/items/bangles/ElemancyBangle.java#L30-L68).
- [LightArmorE](https://github.com/Lyrellion/Ars-Elemancy/blob/dfb18286106aca1ca39a9b0053d64a1ef5041751/src/main/java/lyrellion/ars_elemancy/common/items/armor/LightArmorE.java#L24-L43), [MediumArmorE](https://github.com/Lyrellion/Ars-Elemancy/blob/dfb18286106aca1ca39a9b0053d64a1ef5041751/src/main/java/lyrellion/ars_elemancy/common/items/armor/MediumArmorE.java#L23-L37), [HeavyArmorE](https://github.com/Lyrellion/Ars-Elemancy/blob/dfb18286106aca1ca39a9b0053d64a1ef5041751/src/main/java/lyrellion/ars_elemancy/common/items/armor/HeavyArmorE.java#L28-L42).

**Gates pendentes:** host `SpellSchools.ELEMENTAL.getSubSchools()` e ordem real dos attributemodifiers em Curios; 4 peças + perks tier, SavedData/relog, equip/unequip, hot/rain/swim/lava/altitude, item duplicado nos slots, shared ResourceLocation dos modifiers, conflicts com Epic Fight e dano pós-resistência, mana efetiva (não config nominal). Integração RPG apenas por API contratada com owner/success e idempotência. Stage 06.05 🟡, Stage 09 físico PENDING, sem merge por documentação.
