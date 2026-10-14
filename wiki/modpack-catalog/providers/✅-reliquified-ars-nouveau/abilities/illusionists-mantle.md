# Deceptive Response — Illusionist's Mantle

- **Provider:** Reliquified Ars Nouveau (`reliquified_ars_nouveau`), versão física `0.8.1`.
- **Status:** ✅ `COUNTED_EXACT` para identidade estática de uma habilidade de relíquia; runtime/Survival ⚠️.
- **Item registrado:** `reliquified_ars_nouveau:illusionists_mantle`.
- **Classe física:** `it.hurts.shatterbyte.reliquified_ars_nouveau.items.back.IllusionistsMantleItem`.
- **ID primário `AbilityTemplate.builder`:** `deception`.
- **Nome da habilidade:** Deceptive Response (localização source-pinned 0.8.1).
- **Contribuição semântica:** uma raiz provider-native já contabilizada; **+0** no checkpoint desta auditoria.

## Evidência física

[Java21 #38461801129](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38461801129): o JAR físico SHA-1 `4be1f4b0fd7fbec6618596e2e7c3705db88a7579` inclui o item, a classe e exatamente uma chamada compilada a `AbilityTemplate.builder` com o ID primário acima. Ver [dossiê 19/19](../EXACT-BINARY-RELIC-ABILITIES-0.8.1.md) e [catálogo source-pinned](../README.md).

## Causalidade, exclusões e gates

O item é contêiner da habilidade; rank, modificadores, sub-habilidades, partículas, projéteis, efeitos e eventos de progressão não contam como raízes extras sem nova prova independente. Quando a ação usa casting ou glyphs de Ars Nouveau, sua execução e recursos permanecem sob a autoridade do Ars/provider. Não duplicar mana/cooldowns, dano ou recompensas no Black Arcana.

A auditoria **não** certifica valores de custo/cooldown, algoritmo de combate, aquisição em Survival, loot efetivo, persistência, compatibilidade Relics/Ars ou servidor dedicado. Qualquer adapter Black Arcana requer contrato real e QA próprio.

---

## Engenharia causal — source 0.8.1

**Root:** `AbilityTemplate.builder("deception")`. **Fonte:** [`back/IllusionistsMantleItem.java`](https://github.com/Octo-Studios/reliquified_ars_nouveau/blob/125e1e3a723d8bc7050026e0670f8ac49535c8bc/src/main/java/it/hurts/shatterbyte/reliquified_ars_nouveau/items/back/IllusionistsMantleItem.java) no commit `125e1e3a723d8bc7050026e0670f8ac49535c8bc` (declara 0.8.1). Identidade física do JAR comprovada; **equivalência dos corpos dos métodos não demonstrada**.

- `LivingIncomingDamageEvent` contabiliza EntityDummy próprios vivos com `MANTLE_ILLUSION_TAG` no raio `illusion_radius`; `illusion_barrier` reduz dano por `clamp(count*damage_reduction_per_illusion,0,0.95)`.
- Se agressor vivo e dano positivo, chance `trigger_chance` pode criar dummy atrás do agressor por `max(20,round(illusion_duration*20))` ticks, redirecionando mobs próximos.
- `LivingDeathEvent` do dummy marcado dispara `paralyzing_revenge`; no evento de morte do player, `fatal_exchange` procura dummy até raio 64, prefere associado ao killer, cria outro clone, define 1 HP, teleporta e cancela morte.
- **QA:** cancelamento de LivingDeathEvent não garante safe-recovery no host; testar totens, PvP, posição segura e prioridade com Last Will.

**Estado:** 🟡 dossiê source-located; ⚠️ config, binário, QA físico, Survival/claims; ⛔ adapter perks/Mastery. Nenhuma raiz nova. Relics/Ars/addon detêm recursos, spells, entidades, XP; Black Arcana seu runtime.

[Matriz 0.8.1](../PERK-ENGINEERING-MATRIX-0.8.1.md).
