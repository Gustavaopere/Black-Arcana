# Mana Thrift — Ring of Thrift

- **Provider:** Reliquified Ars Nouveau (`reliquified_ars_nouveau`), versão física `0.8.1`.
- **Status:** ✅ `COUNTED_EXACT` para identidade estática de uma habilidade de relíquia; runtime/Survival ⚠️.
- **Item registrado:** `reliquified_ars_nouveau:ring_of_thrift`.
- **Classe física:** `it.hurts.shatterbyte.reliquified_ars_nouveau.items.ring.RingOfThriftItem`.
- **ID primário `AbilityTemplate.builder`:** `thrift`.
- **Nome da habilidade:** Mana Thrift (localização source-pinned 0.8.1).
- **Contribuição semântica:** uma raiz provider-native já contabilizada; **+0** no checkpoint desta auditoria.

## Evidência física

[Java21 #38461801129](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38461801129): o JAR físico SHA-1 `4be1f4b0fd7fbec6618596e2e7c3705db88a7579` inclui o item, a classe e exatamente uma chamada compilada a `AbilityTemplate.builder` com o ID primário acima. Ver [dossiê 19/19](../EXACT-BINARY-RELIC-ABILITIES-0.8.1.md) e [catálogo source-pinned](../README.md).

## Causalidade, exclusões e gates

O item é contêiner da habilidade; rank, modificadores, sub-habilidades, partículas, projéteis, efeitos e eventos de progressão não contam como raízes extras sem nova prova independente. Quando a ação usa casting ou glyphs de Ars Nouveau, sua execução e recursos permanecem sob a autoridade do Ars/provider. Não duplicar mana/cooldowns, dano ou recompensas no Black Arcana.

A auditoria **não** certifica valores de custo/cooldown, algoritmo de combate, aquisição em Survival, loot efetivo, persistência, compatibilidade Relics/Ars ou servidor dedicado. Qualquer adapter Black Arcana requer contrato real e QA próprio.

---

## Engenharia causal — source declarado 0.8.1

**Root:** `AbilityTemplate.builder("thrift")`. **Fonte:** [`ring/RingOfThriftItem.java`](https://github.com/Octo-Studios/reliquified_ars_nouveau/blob/125e1e3a723d8bc7050026e0670f8ac49535c8bc/src/main/java/it/hurts/shatterbyte/reliquified_ars_nouveau/items/ring/RingOfThriftItem.java), commit `125e1e3a723d8bc7050026e0670f8ac49535c8bc`. Auditoria física comprova identidade do `AbilityTemplate`, mas **não** equivalência método-a-método com o bytecode instalado.

- `SpellCostCalcEvent.Pre` e `.Post` tratam caster `ServerPlayer` e somam `mana_cost_reduction` de cada Ring of Thrift equipado; `currentCost=max(0,round(originalCost*(1-totalReduction)))` sem clamp local da soma além do piso zero.
- `free_cast` sorteia `clamp(free_cast_chance,0,1)` no Pre, zera custo e incrementa `ran_ring_of_thrift_pending_free_casts` no persistent data do player; no Post, consome um token pendente e credita estatística/XP. **Esse token é player-scoped e não está comprovadamente ligado a cast UUID na fonte local**.
- `delayed_refund` programa `refundAmount=currentCost*clamp(refund_percent,0,1)`, soma valores pendentes anteriores no data component `RING_OF_THRIFT_REFUND_AMOUNTS` e armazena data em `REFUND_TIMES` com atraso `refund_delay*20`; `PlayerTickEvent.Post` repassa mana via capability Ars quando chega o prazo.
- `casting_momentum` aumenta `RING_OF_THRIFT_COMBO_STACKS` e `COMBO_UNTIL` após `SpellCastEvent`, alterando `ManaRegenCalcEvent`. QA obrigatória: duas fases de custo, interleaving com Mana Ring, child casts e reconexão; **BA não pode descontar/creditar esse custo novamente**.

**Estado:** 🟡 source-located; ⚠️ configuração, JAR method body, efeitos downstream e QA físico; ⛔ adapter RPG/BA não implementado. Sem nova raiz semântica. Relics/Ars/addon são os donos de casts, recursos e entidades; Black Arcana mantém apenas o runtime próprio.

[Matriz](../PERK-ENGINEERING-MATRIX-0.8.1.md).
