# Goety — auditoria do pipeline de cast e Soul Energy (fonte pública 3.1.1)

> **Atualização factual — 26/10/2026:** o [probe do JAR exato Goety 3.1.4](EXACT-3.1.4-ABI-AND-SYMBOLIC-CALL-AUDIT-20261026.md) confirmou **classes, assinaturas e call-sites selecionados** anteriormente marcados como não verificados. O corpo deste documento continua sendo análise semântica da fonte 3.1.1. A ausência de prova de **algoritmos, eventos efetivamente emitidos, transações e hooks seguros** permanece.

**Data:** 26/10/2026 · **Estado:** ⚠️ SOURCE-ADJACENT / observação e mutação **NÃO HOMOLOGADAS** para a instalação

## 1. Autoridade, proveniência e grau de prova

O modpack usa **Goety 3.1.4**, `goety-3.1.4.jar` (ID `goety`, SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`, conforme [auditoria do artefato exato](EXACT-3.1.4-ARTIFACT-AUDIT.md)). A análise abaixo deriva **somente** do commit do código público **3.1.1** [Vivideru/Goety-3@6c41a04f2d712097c4461f969a6bb8ee277149ef](https://github.com/Vivideru/Goety-3/commit/6c41a04f2d712097c4461f969a6bb8ee277149ef).

**Nenhuma classe, assinatura, evento, dispatcher, valor ou condição descrita aqui foi comprovada no classfile instalado 3.1.4.** Existência de evento no código 3.1.1 **não certifica API suportada no JAR**, nem torna segura a mutação de spell, custo ou cooldown. Não há testes cliente real, multiplayer, cancelamento ou integridade financeira. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.

## 2. Superfícies de API observadas (somente source 3.1.1)

| Fonte pinada | Contrato sintático observado | Limite de semântica |
|---|---|---|
| [`MagicFocus.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/magic/MagicFocus.java) | Guarda um `ISpell` na instância do item e expõe `getSpell()`; seu tooltip obtém custo padrão. | Tooltip **não** é custo liquidado; campos de spell mutáveis no objeto podem afetar compartilhamento entre casters. |
| [`IWand.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/api/items/magic/IWand.java) | `getFocus(stack)` resolve Focus do item; `getSpell(stack)` lê o spell; `cannotCast` considera cooldown e `conditionsMet` no servidor. | Falta de veto não prova débito realizado nem sucesso final. |
| [`ISpell.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/api/magic/ISpell.java) | `defaultSoulCost`, `soulCost`, `SoulCalculation`, `castDuration`, `spellCooldown`, `startSpell/useSpell/stopSpell/SpellResult` e `defaultStats`. | Métodos default de cálculo, não evento de transação confirmada. `SpellStat` não é um contrato de mutação per-player autorizado. |
| [`GoetyEventFactory.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/events/spell/GoetyEventFactory.java) | Publica `StartMagicEvent`, `CastingMagicEvent`, `CastMagicEvent`, `StopMagicEvent`, `TouchMagicEvent`, `BlockMagicEvent` e `ChangeSoulEnergyEvent.Gain/Loss` em `NeoForge.EVENT_BUS`. | Event names são evidência de **3.1.1**, não de API 3.1.4. Cancelamento/`setSpell` não certificam ordenação e exatamente-uma-vez por cast. |
| [`DarkWand.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/magic/DarkWand.java) | `onUseTick`, `releaseUsing`, `finishUsingItem`, `use`, `setSpellConditions`, `SoulUse`, `MagicResults` usam paths diferentes para instantâneo, touch e charging. | Um observador que conte cada evento como cast duplicará canais contínuos, início/parada ou efeito tardio. |
| [`SEHelper.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/utils/SEHelper.java) | `getSoulsAmount` consulta pool ativa ou totem; `decreaseSouls` envia `onSoulEnergyLoss` e debita uma das fontes de Soul. | O evento de Loss não carrega obrigatoriamente um ID de cast; pode observar gastos não mágicos; presença de custo não prova efeito consumado. |

## 3. Ordenação de eventos e diferenças por trajetória

Na [`DarkWand.onUseTick`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/magic/DarkWand.java#L468-L525) da fonte 3.1.1, `GoetyEventFactory.onStartSpell` é chamado **dentro de `onUseTick`**; em seguida a rotina pode invocar `startSpell` quando o tempo de uso marca 1, depois `onCastingSpell` e `useSpell` a cada tick em uma conjuração contínua. `IChargingSpell` pode executar `MagicResults` periodicamente enquanto a varinha permanece em uso. Na [`releaseUsing`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/magic/DarkWand.java#L526-L557), um `StopMagicEvent` antecede `stopSpell` e cooldown condicional; [`finishUsingItem`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/magic/DarkWand.java#L569-L590) consulta `CastMagicEvent` antes do resultado de alguns fluxos.

Na [`GoetyEventFactory`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/events/spell/GoetyEventFactory.java), os dispatchers `onCastSpell` e `onStopSpell` publicam os respectivos eventos, mas não estabelecem por si sós um identificador de liquidação ou garantia de chamada única.

**Conclusão causal restrita ao source:** os eventos acima identificam transições **diferentes**. `StartMagicEvent` não é necessariamente um evento único de abertura; `CastingMagicEvent` é potencialmente recorrente; `CastMagicEvent` não cobre necessariamente todas as execuções que ocorrem durante channeling; `StopMagicEvent` é uma tentativa de encerramento, não certificado de liquidação.

## 4. Soul Energy: pelo menos três representações de custo

1. [`ISpell.SoulCalculation`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/api/magic/ISpell.java) parte de `defaultSoulCost × SoulCostUp`, podendo aplicar equipamento, escolas de magia, ambiente/bioma/dimensão, atributos e truncamento final para `int`. Summon Down pode multiplicar custos de `ISummonSpell`.
2. [`DarkWand.setSpellConditions` e `SoulUse`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/magic/DarkWand.java#L649-L675) mantêm `SOULCOST` no ItemStack; `SoulUse` observa foco encantado com custo multiplicado e aplica `SEHelper.soulDiscount`.
3. [`SEHelper.decreaseSouls`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/utils/SEHelper.java#L263-L287) recebe um valor de entrada, aplica `soulDiscount` ao valor e então chama `GoetyEventFactory.onSoulEnergyLoss`, consumindo Souls da capacidade ativa ou do totem.

**Risco de não equivalência:** no caminho [`DarkWand.MagicResults`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/magic/DarkWand.java#L769-L835), a checagem de saldo `getSoulsAmount(player,SoulUse(...))` e o débito `decreaseSouls(player,SoulUse(...))` percorrem consumidores distintos. Como `SEHelper.decreaseSouls` possui multiplicador próprio, **não se deve presumir igualdade entre custo de validação, valor submetido ao evento Loss e valor efetivamente debitado**. Isso inclui situações em que o equipamento altera descontos. A discrepância física da versão 3.1.4 permanece **hipótese até teste**; esta auditoria não afirma duplicação efetiva nem erro de cobrança instalado.

`ChangeSoulEnergyEvent.Loss` pode ser cancelado ou ter valor ajustado na fonte adjacente; **essa faculdade isolada não o torna hook adequado para perks de economia de mana**, porque não vincula necessariamente a perda a um cast específico, pode ocorrer após a admissão e afeta gastos de outras causas.

## 5. Política de interoperabilidade para Black Arcana / RPG Skill Tree

- **Goety possui autoridade** do custo Soul Energy, cast Focus/Staff, cooldown, cast channeling, efeitos, servants e world effects nativos.
- **Black Arcana** mantém seu casting, hazards, domínio, rituais próprios, proteção do mundo e Arcane Danger. Não inserir um segundo `SpellResult` nem gerar `Backlash` no dano Goety sem contrato aprovado.
- **RPG Skill Tree** só concede Mastery/perks/gates mediante evidência de autoria causal e integração idempotente. Não contabilizar `Start/Casting/Stop/Cast/Loss` como cinco conjurações. Afirmar equivalência entre callback e “sucesso” é bloqueado.
- Um adapter futuro deve certificar, **no JAR exato 3.1.4**, o timing de todas as variantes (instantânea, continuous, charging, touch, block, summons), se o evento é server-only, se permite cancelamento, como a ação é correlacionada e como provar débito/settlement.
- **Mutação de custo, cooldown, target ou instância `ISpell`: ⛔ FAIL-CLOSED** até compatibilidade de bytecode, regra de ownership do objeto, dedup e QA dedicada. Não copiar implementação proprietária para o Black Arcana.

## 6. Plano de verificação e status

Provas requeridas: (1) ABI/eventos do JAR 3.1.4 SHA-exato; (2) configuração física e overrides; (3) invocações Start/Casting/Cast/Stop e cancelamentos por timeline no servidor; (4) round-trip do `SOULCOST` em `ItemStack` e desconto por armadura; (5) gasto com foco encantado, totem e pool ativa; (6) dois casters usando Focus igual simultaneamente; (7) retry/restart/world save; (8) ausência de double-charge e de duplicate Mastery; (9) cliente e modpack reais.

**Estado:** ⚠️ apenas fonte adjacente 3.1.1, sem certificação de hook e sem aprovação de integração. O documento é diagnóstico transversal, **não** objeto mágico adicional nem prova de 100% do Goety; não altera o manifesto `PERK-READY-CERTIFICATIONS.json` ou os índices automáticos.

## Adendo de compatibilidade ABI no JAR físico 3.1.4 — 26/10/2026

O workflow [#40344481668](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40344481668) verificou o SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`. A lista, escopo e digest da evidência estão em [EXACT-3.1.4-ABI-AND-SYMBOLIC-CALL-AUDIT-20261026.md](EXACT-3.1.4-ABI-AND-SYMBOLIC-CALL-AUDIT-20261026.md).

**Confirmado estritamente como assinatura e referência simbólica de bytecode 3.1.4:** `GoetyEventFactory.onStartSpell`, `onCastingSpell`, `onCastSpell`, `onStopSpell`, `onSoulEnergyGain/Loss`; eventos concretos Start/Casting/Cast/Stop/ChangeSoulEnergy; chamadas de `DarkWand.onUseTick` para Start/Casting, de `use/finishUsingItem` para Cast, de `releaseUsing` para Stop, de `canCastTouch` para Touch; `DarkWand.MagicResults` referencia `ISpell.SpellResult`, `SEHelper.getSoulsAmount`, `decreaseSouls` e `addCooldown`; `SEHelper.decreaseSouls` referencia `GoetyEventFactory.onSoulEnergyLoss`.

**Não confirmado no 3.1.4:** emissão em todos os ramos, ordem de débito/resultado, custo numérico, número de invocações por cast, permissão de cancelar sem side effects, identificador causal estável, servidor dedicado/client, exclusividade por conjurador e segurança de mutação. **Existência de `ChangeSoulEnergyEvent.Loss` não comprova que ele representa somente consumo mágico nem que é um hook de perk adequado.**

O status correto deste documento passa a ser **⚠️ source 3.1.1 com adendo factual exato de ABI 3.1.4**. A certificação para perks continua **0** nesta área e os hooks mutadores permanecem **⛔ fail-closed**; nenhuma fórmula histórica deve ser promovida sem confronto binário e teste.

## Adendo posterior: chamada interna de desconto confirmada no JAR 3.1.4 (26/10/2026)

O [probe exato de símbolos/field por método](EXACT-3.1.4-TARGET-SOUL-STRUCTURAL-AUDIT-20261026.md) (GitHub Actions `40362689828`, artifact `12668033309`) eliminou uma lacuna no filtro do relatório ABI precedente: no binário Goety 3.1.4, `SEHelper.decreaseSouls` **referencia `SEHelper.soulDiscount` mesmo sendo uma chamada da própria classe**. `DarkWand.SoulUse` também contém referências a `soulDiscount`; `DarkWand.MagicResults` e `canCastTouch` referenciam rotas de saldo/verificação/débito e o `SEHelper.decreaseSouls` referencia `GoetyEventFactory.onSoulEnergyLoss`.

Esse arranjo **não comprova desconto duplicado incorreto**: chamadas em métodos diferentes não provam que uma mesma quantia foi descontada duas vezes, nem equivalência numérica entre as rotas. Exige-se trace real da transação, equip discount, arredondamento e cancelamento antes de qualquer perk. Goety mantém autoria e liquidação da Soul Energy; `mutating_hook=NOT_VERIFIED` e `physical_qa=NOT_TESTED`. Nenhuma certificação ou Stage é alterado.
