# Ars Nouveau — Player Mana

State: `SOURCE-PINNED 5.13.1 / PROVIDER AUTHORITY VERIFIED`.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`.

## Capability

Ars exposes `IManaCap` with provider-native operations for current mana, max mana, add/remove/set mana, glyph bonus and book tier. `ManaCap` persists that data through Ars' mana attachment and clamps current mana to `[0, maxMana]`.

## Max mana

`ManaUtil.calcMaxMana(Player)` derives raw max mana from:

`INIT_MAX_MANA + knownGlyphCount * GLYPH_MAX_BONUS + bookTier * TIER_MAX_BONUS`

The value is then represented through Ars' `PerkAttributes.MAX_MANA`, so armor/perk modifiers participate in the final attribute value. Ars posts `MaxManaCalcEvent`, allowing provider/addon modification, and reads an event-supplied reserve fraction.

Usable max mana is `Max * (1 - Reserve)`.

Familiars participate in this reserve path through `MaxManaCalcEvent`; the common familiar runtime contributes a 0.15 reserve modifier per active familiar entity path unless overridden.

## Mana regeneration

`ManaUtil.getManaRegen(Player)` starts from:

`knownGlyphCount * GLYPH_REGEN_BONUS + bookTier * TIER_REGEN_BONUS + INIT_MANA_REGEN`

It then resolves through `PerkAttributes.MANA_REGEN_BONUS` and `ManaRegenCalcEvent`.

Config-backed terms are intentionally left symbolic here. The physical modpack/runtime config is the authority for their actual values.

## Spell settlement

`SpellResolver` validates the spell, computes resolve cost, checks caster mana and only calls `expendMana()` when the cast method returns `CastResolveType.SUCCESS`. Resolve cost and expended cost each pass through Ars' spell-cost events and provider-native discount calculation. Turret tile casters are explicitly exempted from `expendMana()` in this path.

## Authority / Black Arcana boundary

Ars player mana is the authoritative resource for Ars casts. Black Arcana must not create a shadow copy of Ars mana, mirror Thread modifiers into a second resource, or charge an additional Black Arcana mana cost for the same Ars-owned cast. If Black Arcana ever consumes Ars mana through an integration, that must use a verified adapter/transaction contract; otherwise fail closed.

## Auditoria de engenharia — mana do jogador Ars (2026-10-26; PR independente)

**⚠️ Auditoria source-pinned; sem certificação no manifesto.** Versão física `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. Compiled registry proof para 109 glyphs/rituais **não valida** bytecode de mana. Fontes: [IManaCap.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/mana/IManaCap.java), [ManaCap.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/capability/ManaCap.java), [ManaData.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/capability/ManaData.java), [ManaUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/ManaUtil.java), [ManaCapEvents.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/ManaCapEvents.java), [MaxManaCalcEvent.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/MaxManaCalcEvent.java), [ManaRegenCalcEvent.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/ManaRegenCalcEvent.java), [SpellCostCalcEvent.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellCostCalcEvent.java), [SpellResolver.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java).

| Eixo | Contrato técnico da versão e bloqueio para integração |
|---|---|
| **Attachment / persistência** | `ManaCap` lê/grava `AttachmentsRegistry.MANA_ATTACHMENT` e expõe `getCurrentMana/setMana/addMana/removeMana/getMaxMana/setMaxMana/getGlyphBonus/setGlyphBonus/getBookTier/setBookTier`. `setMana` limita ao intervalo `0..getMaxMana()`; `removeMana` converte subtração negativa para 0 antes de atualizar. `ManaData.serializeNBT` escreve `current`, `max`, `glyph`, `book_tier`, `reserved`; `ManaCap.syncToClient` transmite `PacketUpdateMana`. Não criar pool espelho nem persistir segundo saldo em Black Arcana. |
| **Mana máxima** | `ManaUtil.calcMaxMana(Player)`: `rawMax=INIT_MAX_MANA+glyphBonus*GLYPH_MAX_BONUS+bookTier*TIER_MAX_BONUS`; injeta/atualiza modifier transitório `MAX_MANA_MODIFIER` como `ADD_VALUE` no `PerkAttributes.MAX_MANA` e lê valor final do atributo; posta `MaxManaCalcEvent` que expõe `setMax/getMax/setReserve/getReserve`. `Mana.getRealMax()` faz `(int)(Max*(1.0-Reserve))`; esse é usable max, não um novo recurso. Não atribuir valores numéricos aos termos de `ServerConfig` sem config física. |
| **Reserva: ordem do clamp** | `MaxManaCalcEvent.setReserve(float newReserve)` executa literalmente `Mth.clamp(0,newReserve,1)`. Pelo contrato de `clamp(value,min,max)`, isso passa **zero como valor e newReserve como limite inferior**, em vez de `clamp(newReserve,0,1)`. Para entradas 0..1 o resultado coincide com `newReserve`; para `newReserve>1` o getter pode devolver >1, produzindo `Mana.getRealMax()<0`. **Desvio de limites na fonte examinada**, não defeito demonstrado no JAR/pack; testar inputs fora de faixa e addon providers antes de aceitar mutadores. Não supor reserva de 15% por cada familiar: `FamiliarEvents.maxManaCalc` retorna após o primeiro familiar correspondente. |
| **Regeneração e ciclo de tick** | `ManaUtil.getManaRegen(Player)` soma `glyphBonus*GLYPH_REGEN_BONUS+bookTier*TIER_REGEN_BONUS+INIT_MANA_REGEN`, resolve atributo `MANA_REGEN_BONUS` com `MANA_REGEN_MODIFIER` e `ManaRegenCalcEvent`. `ManaCapEvents.playerOnTick(PlayerTickEvent.Pre)` roda só para `ServerPlayer` e quando `gameTime%REGEN_INTERVAL==0`. Primeiro chama `mana.addMana(regenPerSecond)` e **depois** recalcula `calcMaxMana`/`mana.setMaxMana`/`mana.setReserve`; ordem pode importar num tick de mudança de equipamento. O divisor de regen usa `Math.max(1,((int)MEAN_TPS/REGEN_INTERVAL))`. Sync forçado ocorre em `gameTime%60==0`; `MEAN_TPS` é atualizada no server `PlayerTickEvent.Post` a cada 600 ticks. |
| **Eventos de cast, custos distintos** | `SpellResolver.canCast` faz `getResolveCost` e consulta `getCaster().enoughMana(totalCost)`. `getResolveCost` publica `SpellCostCalcEvent.Pre` após descontos de Curios, armor e casterStack; `getExpendedCost` recalcula **separadamente** e publica `SpellCostCalcEvent.Post`. Cada valor é `Math.max(0,event.currentCost)`, mas **não há igualdade/atomicidade garantida entre Pre e Post**. O `expendMana` só é chamado quando `CastResolveType.SUCCESS`, e retorna sem debitar para `TileCaster` tipo `TURRET`. Portanto checagem de saldo e debitação final podem divergir com addons/config/mudanças entre eventos; qualquer bridge deve ser server-authoritative, bounded, replay-safe e não criar segundo charge. |
| **Reprodução e limites** | Respawn, login e mudança de dimensão usam `syncPlayerEvent` para recalcular usable max e enviar `PacketUpdateMana`; o `PlayerEvent.Clone` de ManaCapEvents está comentado com TODO. Nenhum método desta documentação prova migração correta de old NBT, clamp de reserva fora de faixa, side effect transacional do `expendMana` ou contrato mutador BA. |

**QA necessária:** reserva >1/negativa, add-ons alterando `SpellCostCalcEvent.Pre` e `Post` em ordens diferentes, mod Ars 'n' Spells 3.3.4 que integra mana com Iron's sem alterar Source, equipamento entrando/saindo em tick de regen, `ServerConfig.REGEN_INTERVAL`, `PlayerEvent.Clone`, client desync e restauração de save. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. `WorldEffectPolicy` rege apenas world effects próprios BA; RPG Skill Tree mantém perks/Mastery/gates. Ficha permanece ⚠️ até certificação de fonte com evidência de sete campos e CI final.
