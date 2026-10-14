# Mana Barrier — Cloak of Concealment

- **Provider:** Reliquified Ars Nouveau (`reliquified_ars_nouveau`), versão física `0.8.1`.
- **Status:** ✅ `COUNTED_EXACT` para identidade estática de uma habilidade de relíquia; runtime/Survival ⚠️.
- **Item registrado:** `reliquified_ars_nouveau:cloak_of_concealment`.
- **Classe física:** `it.hurts.shatterbyte.reliquified_ars_nouveau.items.back.CloakOfConcealmentItem`.
- **ID primário `AbilityTemplate.builder`:** `absorption`.
- **Nome da habilidade:** Mana Barrier (localização source-pinned 0.8.1).
- **Contribuição semântica:** uma raiz provider-native já contabilizada; **+0** no checkpoint desta auditoria.

## Evidência física

[Java21 #38461801129](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38461801129): o JAR físico SHA-1 `4be1f4b0fd7fbec6618596e2e7c3705db88a7579` inclui o item, a classe e exatamente uma chamada compilada a `AbilityTemplate.builder` com o ID primário acima. Ver [dossiê 19/19](../EXACT-BINARY-RELIC-ABILITIES-0.8.1.md) e [catálogo source-pinned](../README.md).

## Causalidade, exclusões e gates

O item é contêiner da habilidade; rank, modificadores, sub-habilidades, partículas, projéteis, efeitos e eventos de progressão não contam como raízes extras sem nova prova independente. Quando a ação usa casting ou glyphs de Ars Nouveau, sua execução e recursos permanecem sob a autoridade do Ars/provider. Não duplicar mana/cooldowns, dano ou recompensas no Black Arcana.

A auditoria **não** certifica valores de custo/cooldown, algoritmo de combate, aquisição em Survival, loot efetivo, persistência, compatibilidade Relics/Ars ou servidor dedicado. Qualquer adapter Black Arcana requer contrato real e QA próprio.

---

## Engenharia causal — source 0.8.1

**Root:** `AbilityTemplate.builder("absorption")`. **Fonte:** [`back/CloakOfConcealmentItem.java`](https://github.com/Octo-Studios/reliquified_ars_nouveau/blob/125e1e3a723d8bc7050026e0670f8ac49535c8bc/src/main/java/it/hurts/shatterbyte/reliquified_ars_nouveau/items/back/CloakOfConcealmentItem.java), commit `125e1e3a723d8bc7050026e0670f8ac49535c8bc` (declarado 0.8.1). A identidade foi auditada no JAR físico, mas **equivalência do corpo de métodos compilado ↔ source não foi demonstrada**.

- `LivingIncomingDamageEvent` exige `ServerPlayer` e capability de mana do Ars; `manaPerDamage=max(0,stat)`. Absorção = `min(incoming,currentMana/manaPerDamage)` quando custo positivo, ou `incoming` quando custo zero.
- Deduz `manaSpent=absorbedDamage*manaPerDamage` via `manaCap.removeMana`; se `remainingDamage<=0`, cancela evento, senão chama `event.setAmount(remainingDamage)`.
- `damage_reflection` usa janela `reflect_window*20` ticks e reduz hits consecutivos; `damage_to_healing` cura fração `healing_conversion` da absorção; `damage_distribution` divide `absorbedDamage/targets.size()` entre `LivingEntity` vivos e não aliados num AABB.
- **Perks:** status de absorção, cura, custo e dano não transferem authority para Black Arcana. AABB e ordem de eventos exigem limites físicos e QA.

**Estado:** 🟡 comportamento localizado no source; ⚠️ configuração, método binário, Survival e multiplayer pendentes; ⛔ hooks seguros de perks e Mastery não homologados. Sem segunda execução, duplicação de mana ou novas identidades mágicas. Relics/Ars/addon são donos dos recursos e do comportamento; RPG Skill Tree é somente progression provider.

[Matriz 0.8.1](../PERK-ENGINEERING-MATRIX-0.8.1.md).
