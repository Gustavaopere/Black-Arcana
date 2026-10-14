# Orbit of Devotion — Emblem of Devotion

- **Provider:** Reliquified Ars Nouveau (`reliquified_ars_nouveau`), versão física `0.8.1`.
- **Status:** ✅ `COUNTED_EXACT` para identidade estática de uma habilidade de relíquia; runtime/Survival ⚠️.
- **Item registrado:** `reliquified_ars_nouveau:emblem_of_devotion`.
- **Classe física:** `it.hurts.shatterbyte.reliquified_ars_nouveau.items.charm.EmblemOfDevotionItem`.
- **ID primário `AbilityTemplate.builder`:** `devotion`.
- **Nome da habilidade:** Orbit of Devotion (localização source-pinned 0.8.1).
- **Contribuição semântica:** uma raiz provider-native já contabilizada; **+0** no checkpoint desta auditoria.

## Evidência física

[Java21 #38461801129](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38461801129): o JAR físico SHA-1 `4be1f4b0fd7fbec6618596e2e7c3705db88a7579` inclui o item, a classe e exatamente uma chamada compilada a `AbilityTemplate.builder` com o ID primário acima. Ver [dossiê 19/19](../EXACT-BINARY-RELIC-ABILITIES-0.8.1.md) e [catálogo source-pinned](../README.md).

## Causalidade, exclusões e gates

O item é contêiner da habilidade; rank, modificadores, sub-habilidades, partículas, projéteis, efeitos e eventos de progressão não contam como raízes extras sem nova prova independente. Quando a ação usa casting ou glyphs de Ars Nouveau, sua execução e recursos permanecem sob a autoridade do Ars/provider. Não duplicar mana/cooldowns, dano ou recompensas no Black Arcana.

A auditoria **não** certifica valores de custo/cooldown, algoritmo de combate, aquisição em Survival, loot efetivo, persistência, compatibilidade Relics/Ars ou servidor dedicado. Qualquer adapter Black Arcana requer contrato real e QA próprio.

---

## Engenharia causal — source 0.8.1

**Root:** `AbilityTemplate.builder("devotion")`. **Fonte:** [`charm/EmblemOfDevotionItem.java`](https://github.com/Octo-Studios/reliquified_ars_nouveau/blob/125e1e3a723d8bc7050026e0670f8ac49535c8bc/src/main/java/it/hurts/shatterbyte/reliquified_ars_nouveau/items/charm/EmblemOfDevotionItem.java) no commit `125e1e3a723d8bc7050026e0670f8ac49535c8bc` (declara 0.8.1). Identidade física do JAR comprovada; **equivalência dos corpos dos métodos não demonstrada**.

- `curioTick` gerencia UUIDs `EMBLEM_OF_DEVOTION_STACK_ID` e `DEVOTION_MAINTENANCE_TICK_TAG`. Descarta `EntityOrbitProjectile` cujo `DEVOTION_STACK_ID_TAG` não pertence a Curios equipados.
- Exige spell scribed válida com `size()>1`, começando em `MethodTouch`. Consulta orbes no raio 24 e limita por `max(1,round(max_orbs))`; intervalo `max(1,round(max(0.05,spawn_interval)*20))` ticks.
- Cria `EntityOrbitProjectile` com `SpellResolver`, owner player e tags de stack/slot; `onUnequip` descarta orbes próprios no raio 64, limpa atributos/absorção. `SpellCostCalcEvent` fixa custo zero somente para caster tool EmblemOfDevotionItem.
- **QA:** colisões e XP via mixins, lifecycle, limites e efeitos downstream não foram revalidados; não criar segundo scheduler ou mana.

**Estado:** 🟡 dossiê source-located; ⚠️ config, binário, QA físico, Survival/claims; ⛔ adapter perks/Mastery. Nenhuma raiz nova. Relics/Ars/addon detêm recursos, spells, entidades, XP; Black Arcana seu runtime.

[Matriz 0.8.1](../PERK-ENGINEERING-MATRIX-0.8.1.md).
