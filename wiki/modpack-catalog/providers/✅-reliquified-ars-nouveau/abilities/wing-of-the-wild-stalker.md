# Predatory Flight — Wing of the Wild Stalker

- **Provider:** Reliquified Ars Nouveau (`reliquified_ars_nouveau`), versão física `0.8.1`.
- **Status:** ✅ `COUNTED_EXACT` para identidade estática de uma habilidade de relíquia; runtime/Survival ⚠️.
- **Item registrado:** `reliquified_ars_nouveau:wing_of_the_wild_stalker`.
- **Classe física:** `it.hurts.shatterbyte.reliquified_ars_nouveau.items.body.WingWildStalkerItem`.
- **ID primário `AbilityTemplate.builder`:** `wild_flight`.
- **Nome da habilidade:** Predatory Flight (localização source-pinned 0.8.1).
- **Contribuição semântica:** uma raiz provider-native já contabilizada; **+0** no checkpoint desta auditoria.

## Evidência física

[Java21 #38461801129](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38461801129): o JAR físico SHA-1 `4be1f4b0fd7fbec6618596e2e7c3705db88a7579` inclui o item, a classe e exatamente uma chamada compilada a `AbilityTemplate.builder` com o ID primário acima. Ver [dossiê 19/19](../EXACT-BINARY-RELIC-ABILITIES-0.8.1.md) e [catálogo source-pinned](../README.md).

## Causalidade, exclusões e gates

O item é contêiner da habilidade; rank, modificadores, sub-habilidades, partículas, projéteis, efeitos e eventos de progressão não contam como raízes extras sem nova prova independente. Quando a ação usa casting ou glyphs de Ars Nouveau, sua execução e recursos permanecem sob a autoridade do Ars/provider. Não duplicar mana/cooldowns, dano ou recompensas no Black Arcana.

A auditoria **não** certifica valores de custo/cooldown, algoritmo de combate, aquisição em Survival, loot efetivo, persistência, compatibilidade Relics/Ars ou servidor dedicado. Qualquer adapter Black Arcana requer contrato real e QA próprio.

---

## Engenharia causal — source 0.8.1

**Root:** `AbilityTemplate.builder("wild_flight")`. **Fonte:** [`body/WingWildStalkerItem.java`](https://github.com/Octo-Studios/reliquified_ars_nouveau/blob/125e1e3a723d8bc7050026e0670f8ac49535c8bc/src/main/java/it/hurts/shatterbyte/reliquified_ars_nouveau/items/body/WingWildStalkerItem.java) no commit `125e1e3a723d8bc7050026e0670f8ac49535c8bc`. O JAR confirma identidade estática, **não** identidade binária exata dos corpos de métodos com o source.

- `PlayerTickEvent.Post` no servidor só contabiliza voo enquanto `player.isFallFlying()`: acumula `distance_flown` a partir de movimento e concede XP `flight_time` a cada 20 ticks; ao parar de voar, limpa `WING_WILD_STALKER_LAST_ELECTRICITY_ID` no stack.
- `LivingDamageEvent.Pre` recebido durante voo aplica modifier `flight_guard`, soma frações clamped por Curio e limita redução total a 95%; o evento de **dano causado direto pelo próprio jogador** durante voo aplica `predator_strike` com fator `1+Σflight_attack_bonus`. Essas rotas de modificação não equivalem a dano final confirmado.
- Root `wild_flight` registra `aerial_dash` e synergy `electricity`; o movimento de dash e efeitos elétricos podem envolver handlers de pacote/entidade em outras classes, **não** comprovados apenas por esses três callbacks.
- **Risco:** proteção ao voar, dano PvP, client packets, custos/cooldowns de dash e reconexão requerem QA. Não duplicar voo, imortalidade ou lightning no Black Arcana nem atribuir Mastery com base em evento de movimento bruto.

**Status:** 🟡 mecanismo source-located; ⚠️ JAR, configuração e QA físico; ⛔ adapter perks/Mastery não homologado. Nenhuma raiz semântica extra. Providers mantêm execução e recursos; Black Arcana seu runtime, RPG Skill Tree progressão por contrato.

[Matriz 0.8.1](../PERK-ENGINEERING-MATRIX-0.8.1.md).
