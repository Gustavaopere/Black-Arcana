# Life Drain

- Registry ID: `ars_nouveau:thread_life_drain`
- Source class: `VampiricPerk`
- Minimum slot: Tier 1 (inherited default).
- Trigger: `SpellDamageEvent.Post`.
- Runtime formula in 5.13.1: `healAmount = event.damage * (0.2f * countForPerk(thread_life_drain, caster))`; the caster is healed by that amount after spell damage resolves.
- Acquisition: Enchanting Apparatus; reagent `ars_nouveau:blank_thread`; Mendosteen Pod + Sculk Catalyst + 2 Abjuration Essence; `sourceCost: 0`.
- Source da aquisição: [receita datagen](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/ApparatusRecipeProvider.java#L1033-L1038); o [builder](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/ApparatusRecipeBuilder.java#L24-L37) mantém `sourceCost` inteiro em0 quando a receita não fornece override.

## Authority / integration

This is Ars-owned spell lifesteal on post-damage causality. Black Arcana must not apply an additional generic lifesteal proc to the same Ars spell hit. In particular, Black Arcana Backlash remains excluded from normal offensive proc chains by canonical architecture.

## Evidence state

`SOURCE-PINNED 5.13.1 @ 112920ff774831f204031da75b4c4e73d3765157`.

## Certificação técnica estática — Thread of Life Drain (2026-10-26)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** Ars Nouveau `5.13.1` (JAR SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`), source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. [VampiricPerk.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/perk/VampiricPerk.java#L11-L32), [PerkEvents.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/PerkEvents.java#L148-L155), [PerkUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/PerkUtil.java#L60-L81), [IEffectResolvePerk.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/IEffectResolvePerk.java#L8-L34), [SpellDamageEvent.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellDamageEvent.java#L11-L43). `evidence_grade=PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`, sem equivalência classfile de perk comprovada.

| Campo | Observação de código e limite |
|---|---|
| Trigger real | `VampiricPerk extends Perk implements IEffectResolvePerk`, ID `ars_nouveau:thread_life_drain`. `PerkEvents.postSpellDamageEvent(SpellDamageEvent.Post)` percorre `PerkUtil.getPerksFromLiving(event.caster)` e chama `onPostSpellDamageEvent(event,perkInstance)` para **cada** instância que implementa `IEffectResolvePerk`. `getPerksFromLiving` concatena slots/instâncias, **sem deduplicar** identidades nesse método. |
| Fórmula por callback | `VampiricPerk.onPostSpellDamageEvent` calcula `healAmount=event.damage*(0.2f*PerkUtil.countForPerk(perkInstance.getPerk(),event.caster))`; chama `event.caster.heal(healAmount)`. `countForPerk` devolve **o maior valor de slot** equipado da mesma perk, e não soma. **Se múltiplas instâncias idênticas chegarem ao dispatcher**, o mesmo máximo entra em cada callback; portanto a fonte permite múltiplas tentativas de heal por `SpellDamageEvent.Post`. Não converter automaticamente em um único bônus global fixo. |
| Eventos/cancelamento | O handler lê `event.damage` no estágio **Post** e não testa `damage>0` nem confirmação da quantidade efetivamente curada. A implementação de `LivingEntity.heal` e a quantidade final dependem do engine, outros listeners e saúde atual; nenhum `addFreshEntity` ou spell adicional é acionado nesta classe. Não contar heal requested como vida realmente restaurada nem causar novo `SpellDamageEvent` de uma segunda pipeline. |
| Custos e escopo | Thread adquirido pelo Enchanting Apparatus segundo receita/sourceCost0 da ficha-base; `onPostSpellDamageEvent` não gasta mana diretamente. O gatilho precisa de spell damage Ars; **Backlash, hazards e DOT Black Arcana não podem ser tratados automaticamente como SpellDamageEvent.Post** para ativar o lifesteal sem bridge comprovado. `WorldEffectPolicy` BA não governa `heal()` Ars. RPG Skill Tree só pode contabilizar progresso no processo canônico/deduplicado. |

**QA pendente:** duplicação de thread no equipamento, efetiva multiplicação dos heals, prioridade de `SpellDamageEvent.Post`, dano real vs evento, death/zero HP, heal cancelado e medição server-client; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.
