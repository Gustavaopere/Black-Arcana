# Arcane Reserve — Mana Ring

- **Provider:** Reliquified Ars Nouveau (`reliquified_ars_nouveau`), versão física `0.8.1`.
- **Status:** ✅ `COUNTED_EXACT` para identidade estática de uma habilidade de relíquia; runtime/Survival ⚠️.
- **Item registrado:** `reliquified_ars_nouveau:mana_ring`.
- **Classe física:** `it.hurts.shatterbyte.reliquified_ars_nouveau.items.ring.ManaRingItem`.
- **ID primário `AbilityTemplate.builder`:** `resonance`.
- **Nome da habilidade:** Arcane Reserve (localização source-pinned 0.8.1).
- **Contribuição semântica:** uma raiz provider-native já contabilizada; **+0** no checkpoint desta auditoria.

## Evidência física

[Java21 #38461801129](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38461801129): o JAR físico SHA-1 `4be1f4b0fd7fbec6618596e2e7c3705db88a7579` inclui o item, a classe e exatamente uma chamada compilada a `AbilityTemplate.builder` com o ID primário acima. Ver [dossiê 19/19](../EXACT-BINARY-RELIC-ABILITIES-0.8.1.md) e [catálogo source-pinned](../README.md).

## Causalidade, exclusões e gates

O item é contêiner da habilidade; rank, modificadores, sub-habilidades, partículas, projéteis, efeitos e eventos de progressão não contam como raízes extras sem nova prova independente. Quando a ação usa casting ou glyphs de Ars Nouveau, sua execução e recursos permanecem sob a autoridade do Ars/provider. Não duplicar mana/cooldowns, dano ou recompensas no Black Arcana.

A auditoria **não** certifica valores de custo/cooldown, algoritmo de combate, aquisição em Survival, loot efetivo, persistência, compatibilidade Relics/Ars ou servidor dedicado. Qualquer adapter Black Arcana requer contrato real e QA próprio.

---

## Engenharia causal adicional — source 0.8.1 (2026-10-13)

**Limite da prova:** o binário físico tem SHA-1 `4be1f4b0fd7fbec6618596e2e7c3705db88a7579` e a identidade `AbilityTemplate` foi comprovada em auditoria Java 21; os comportamentos detalhados abaixo foram lidos do source público versionado `Octo-Studios/reliquified_ars_nouveau@125e1e3a723d8bc7050026e0670f8ac49535c8bc`, declarado 0.8.1. **Não foi demonstrada equivalência byte-a-byte das implementações de métodos ao JAR físico.** Defaults são templates do Relics, não configuração efetiva/estado de jogador.

**Habilidade:** `resonance` (Arcane Reserve); item `reliquified_ars_nouveau:mana_ring`, classe [`ManaRingItem.java`](https://github.com/Octo-Studios/reliquified_ars_nouveau/blob/125e1e3a723d8bc7050026e0670f8ac49535c8bc/src/main/java/it/hurts/shatterbyte/reliquified_ars_nouveau/items/ring/ManaRingItem.java), handlers nativos `MaxManaCalcEvent`, `ManaRegenCalcEvent`, `LivingHealEvent`, `SpellCostCalcEvent.Pre`, `PlayerTickEvent.Post`.

### Cálculos e recursos

- `onMaxManaCalc` soma os valores não negativos `max_mana_bonus` das cópias equipadas e aplica `event.setMax(round(event.getMax()*(1+bonus)))`. Se não houver bônus positivo, não muda o evento. Isso opera a capacidade de mana **Ars**, não um recurso próprio de Black Arcana.
- `mana_regen` habilitado: soma `mana_regen_bonus` entre itens equipados e modifica `event.setRegen(event.getRegen()*(1+bonus))`.
- `healing_to_mana` habilitado: no `LivingHealEvent` com valor positivo, adiciona mana `event.getAmount()*max(0,mana_per_health)` diretamente à capability Ars, medindo a diferença real do saldo antes/depois e sincronizando. **A leitura do valor do evento não prova cura final após toda a cadeia de listeners**; idempotência e timing requerem QA.
- `mana_debt` habilitado: em `SpellCostCalcEvent.Pre` servidor, se `availableManaCost=floor(currentMana)` é inferior a `event.currentCost`, calcula `borrowedMana=currentCost-availableManaCost`, penalidade como **soma** de `debt_cost_increase` das cópias elegíveis e adiciona `debtToAdd=borrowedMana*(1+debtPenalty)`, repartido igualmente entre esses stacks. O provider então limita `event.currentCost` ao mana disponível. Esse caminho altera o custo no **evento nativo** e persiste dívida no data component `MANA_RING_DEBT`; não deve ser cobrado uma segunda vez pelo Black Arcana.
- No `PlayerTickEvent.Post`, somente quando `gameTime % ServerConfig.REGEN_INTERVAL==0`, calcula orçamento de pagamento a partir de `ManaUtil.getManaRegen(player)`, mana disponível e intervalo. Percorre stacks com dívida e reduz `MANA_RING_DEBT`; se houve pagamento, chama `manaCap.removeMana(repaidTotal)` e sincroniza. A semântica do método `ManaUtil` e a unidade efetiva do intervalo são do Ars host.

### Riscos e QA específicos

- **Acúmulo de Curios:** bônus e penalidades são somados por stack; testar mais de um anel e limites; não inferir um valor fixo de max mana.
- **Causalidade:** `LivingHealEvent` + XP da relíquia; `SpellCostCalcEvent.Pre` + criação de dívida; `PlayerTickEvent.Post` + reembolso de dívida têm recibos distintos. Não tratar pagamento de dívida como novo gasto mágico ou nova Mastery.
- **Invariantes a provar:** não-negatividade da dívida, preservação do saldo, reload de data component, evento cancelado, distribuição quando múltiplos itens existem, interplay com o multicasting da Archmage Glove.


### Implicações para Black Arcana e RPG

- Reliquified Ars Nouveau/Relics são autoridades do item, habilidade, ranks, experiência, efeitos e dados; Ars Nouveau mantém autoridade por mana, resolver, spell context e spells. Black Arcana não repete cast, recurso ou consequência. RPG Skill Tree só pode consultar/conceder perks mediante boundary comprovado.
- **Perk A:** estatísticas nativas e eventos *observados na fonte* não autorizam escrita arbitrária. **Perk B:** nenhum evento de integração Black Arcana/RPG com garantia de causalidade foi homologado. **Perk C/D:** adapter/rate caps e token de cast exigem contrato, **⛔ fail-closed** até confirmação.
- QA pendente: instância física atual de Relics 0.12.8, Ars Nouveau 5.13.1, Curios atual, config, save/restart, multiplayer, equipamento duplicado, eventos cancelados, custos e Mastery. Nenhum GameTest ou Survival desse item foi executado nesta etapa.
- **Clean-room:** relatamos fatos de execução em nossas palavras; não copiamos código-fonte/asset do provider para o Black Arcana.

[Matriz desta etapa](../PERK-ENGINEERING-MATRIX-0.8.1.md) · [Índice do provider](../README.md).
