# Petal Lift — Whirlisprig Petals

- **Provider:** Reliquified Ars Nouveau (`reliquified_ars_nouveau`), versão física `0.8.1`.
- **Status:** ✅ `COUNTED_EXACT` para identidade estática de uma habilidade de relíquia; runtime/Survival ⚠️.
- **Item registrado:** `reliquified_ars_nouveau:whirlisprig_petals`.
- **Classe física:** `it.hurts.shatterbyte.reliquified_ars_nouveau.items.WhirlisprigPetalsItem`.
- **ID primário `AbilityTemplate.builder`:** `petal_lift`.
- **Nome da habilidade:** Petal Lift (localização source-pinned 0.8.1).
- **Contribuição semântica:** uma raiz provider-native já contabilizada; **+0** no checkpoint desta auditoria.

## Evidência física

[Java21 #38461801129](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38461801129): o JAR físico SHA-1 `4be1f4b0fd7fbec6618596e2e7c3705db88a7579` inclui o item, a classe e exatamente uma chamada compilada a `AbilityTemplate.builder` com o ID primário acima. Ver [dossiê 19/19](../EXACT-BINARY-RELIC-ABILITIES-0.8.1.md) e [catálogo source-pinned](../README.md).

## Causalidade, exclusões e gates

O item é contêiner da habilidade; rank, modificadores, sub-habilidades, partículas, projéteis, efeitos e eventos de progressão não contam como raízes extras sem nova prova independente. Quando a ação usa casting ou glyphs de Ars Nouveau, sua execução e recursos permanecem sob a autoridade do Ars/provider. Não duplicar mana/cooldowns, dano ou recompensas no Black Arcana.

A auditoria **não** certifica valores de custo/cooldown, algoritmo de combate, aquisição em Survival, loot efetivo, persistência, compatibilidade Relics/Ars ou servidor dedicado. Qualquer adapter Black Arcana requer contrato real e QA próprio.

---

## Engenharia causal — source 0.8.1

**Root:** `AbilityTemplate.builder("petal_lift")`. **Fonte:** [`WhirlisprigPetalsItem.java`](https://github.com/Octo-Studios/reliquified_ars_nouveau/blob/125e1e3a723d8bc7050026e0670f8ac49535c8bc/src/main/java/it/hurts/shatterbyte/reliquified_ars_nouveau/items/WhirlisprigPetalsItem.java) no commit `125e1e3a723d8bc7050026e0670f8ac49535c8bc`. O JAR confirma identidade estática, **não** identidade binária exata dos corpos de métodos com o source.

- `use` exige carga e `lift_speed>0`, consome uma carga, ativa `WHIRLISPRIG_PETALS_ACTIVE` e `LIFT_TICKS=80`; velocidade de lançamento `jumpVelocity=sqrt(0.16*lift_speed)`, diretamente vertical por padrão ou conforme vetor de visão com `directed_lift`.
- `inventoryTick` mantém `slow_fall` com modifier de `Attributes.GRAVITY` quando item em mão, player em ar e sem agachar. Recuperação de charges só inicia após pousar e encerrar lift assist; intervalo `max(1,round(max(0.05,charge_regen_time)*20))` ticks. Modifiers e data components ficam no provider.
- Reusos em sequência acumulam `WHIRLISPRIG_PETALS_BONUS_STACKS`; em `LivingDamageEvent.Pre`, `airborne_volley` consome os bônus e eleva dano por `baseDamage*(1+bonusStacks*ranged_bonus_damage)` quando player está no ar.
- **Anomalia local a validar:** o ramo `directed_lift` concede XP com source `projectile_reflect` e métrica `projectiles_reflected`, apesar de usar apenas movimento do player no trecho examinado. Não renomear semanticamente nem inferir reflexão real de projétil sem outro callsite/teste; QA regressiva da correção 0.8.1 obrigatória.

**Status:** 🟡 mecanismo source-located; ⚠️ JAR, configuração e QA físico; ⛔ adapter perks/Mastery não homologado. Nenhuma raiz semântica extra. Providers mantêm execução e recursos; Black Arcana seu runtime, RPG Skill Tree progressão por contrato.

[Matriz 0.8.1](../PERK-ENGINEERING-MATRIX-0.8.1.md).
