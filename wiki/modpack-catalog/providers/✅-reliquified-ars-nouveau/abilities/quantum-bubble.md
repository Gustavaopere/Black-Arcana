# Quantification — Quantum Bubble

- **Provider:** Reliquified Ars Nouveau (`reliquified_ars_nouveau`), versão física `0.8.1`.
- **Status:** ✅ `COUNTED_EXACT` para identidade estática de uma habilidade de relíquia; runtime/Survival ⚠️.
- **Item registrado:** `reliquified_ars_nouveau:quantum_bubble`.
- **Classe física:** `it.hurts.shatterbyte.reliquified_ars_nouveau.items.head.QuantumBubbleItem`.
- **ID primário `AbilityTemplate.builder`:** `stasis`.
- **Nome da habilidade:** Quantification (localização source-pinned 0.8.1).
- **Contribuição semântica:** uma raiz provider-native já contabilizada; **+0** no checkpoint desta auditoria.

## Evidência física

[Java21 #38461801129](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38461801129): o JAR físico SHA-1 `4be1f4b0fd7fbec6618596e2e7c3705db88a7579` inclui o item, a classe e exatamente uma chamada compilada a `AbilityTemplate.builder` com o ID primário acima. Ver [dossiê 19/19](../EXACT-BINARY-RELIC-ABILITIES-0.8.1.md) e [catálogo source-pinned](../README.md).

## Causalidade, exclusões e gates

O item é contêiner da habilidade; rank, modificadores, sub-habilidades, partículas, projéteis, efeitos e eventos de progressão não contam como raízes extras sem nova prova independente. Quando a ação usa casting ou glyphs de Ars Nouveau, sua execução e recursos permanecem sob a autoridade do Ars/provider. Não duplicar mana/cooldowns, dano ou recompensas no Black Arcana.

A auditoria **não** certifica valores de custo/cooldown, algoritmo de combate, aquisição em Survival, loot efetivo, persistência, compatibilidade Relics/Ars ou servidor dedicado. Qualquer adapter Black Arcana requer contrato real e QA próprio.

---

## Engenharia causal — source declarado 0.8.1

**Root:** `AbilityTemplate.builder("stasis")`. **Fonte:** [`head/QuantumBubbleItem.java`](https://github.com/Octo-Studios/reliquified_ars_nouveau/blob/125e1e3a723d8bc7050026e0670f8ac49535c8bc/src/main/java/it/hurts/shatterbyte/reliquified_ars_nouveau/items/head/QuantumBubbleItem.java), commit `125e1e3a723d8bc7050026e0670f8ac49535c8bc`. Auditoria física comprova identidade do `AbilityTemplate`, mas **não** equivalência método-a-método com o bytecode instalado.

- `PlayerTickEvent.Post` servidor mantém `QUANTUM_BUBBLE_CHARGES` com `max(1,round(max_charges))`; recupera cargas por `max(1,round(max(0.05,charge_regen_time)*20))` ticks.
- Para captura, consulta projéteis próximos em `player.getBoundingBox().inflate(2.75)` (expandido na direção do movimento), exclui os próprios, montados, já capturados, setas fincadas e projéteis afastando-se. Cria `BubbleEntity(level,100,0F)`, monta o projétil na bolha, guarda player UUID, velocidade, owner e `releaseTick=gameTime+80`. Consome uma carga e registra XP `projectile_capture`.
- No fim ou `HAS_POPPED`, o handler localiza bolhas próprias até `max(2.75,protection_radius)+6`; marca released, desmonta projétil e restaura movimento vertical descendente ou `projectile_direction` rumo ao owner original, com fator de velocidade 2. `blinding_burst` pode aplicar BLINDNESS em AABB e limpar target de mobs.
- O modifier `bubble_guard` é examinado em `LivingIncomingDamageEvent`; o resultado físico de captura/liberação, owner/PvP e compatibilidade com projéteis de outros mods exigem QA. **Não criar segundo projectile cast/loot**.

**Estado:** 🟡 source-located; ⚠️ configuração, JAR method body, efeitos downstream e QA físico; ⛔ adapter RPG/BA não implementado. Sem nova raiz semântica. Relics/Ars/addon são os donos de casts, recursos e entidades; Black Arcana mantém apenas o runtime próprio.

[Matriz](../PERK-ENGINEERING-MATRIX-0.8.1.md).
