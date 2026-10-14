# Thorn Burst — Spiked Cloak

- **Provider:** Reliquified Ars Nouveau (`reliquified_ars_nouveau`), versão física `0.8.1`.
- **Status:** ✅ `COUNTED_EXACT` para identidade estática de uma habilidade de relíquia; runtime/Survival ⚠️.
- **Item registrado:** `reliquified_ars_nouveau:spiked_cloak`.
- **Classe física:** `it.hurts.shatterbyte.reliquified_ars_nouveau.items.back.SpikedCloakItem`.
- **ID primário `AbilityTemplate.builder`:** `thorn_burst`.
- **Nome da habilidade:** Thorn Burst (localização source-pinned 0.8.1).
- **Contribuição semântica:** uma raiz provider-native já contabilizada; **+0** no checkpoint desta auditoria.

## Evidência física

[Java21 #38461801129](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38461801129): o JAR físico SHA-1 `4be1f4b0fd7fbec6618596e2e7c3705db88a7579` inclui o item, a classe e exatamente uma chamada compilada a `AbilityTemplate.builder` com o ID primário acima. Ver [dossiê 19/19](../EXACT-BINARY-RELIC-ABILITIES-0.8.1.md) e [catálogo source-pinned](../README.md).

## Causalidade, exclusões e gates

O item é contêiner da habilidade; rank, modificadores, sub-habilidades, partículas, projéteis, efeitos e eventos de progressão não contam como raízes extras sem nova prova independente. Quando a ação usa casting ou glyphs de Ars Nouveau, sua execução e recursos permanecem sob a autoridade do Ars/provider. Não duplicar mana/cooldowns, dano ou recompensas no Black Arcana.

A auditoria **não** certifica valores de custo/cooldown, algoritmo de combate, aquisição em Survival, loot efetivo, persistência, compatibilidade Relics/Ars ou servidor dedicado. Qualquer adapter Black Arcana requer contrato real e QA próprio.

---

## Engenharia causal — source declarado 0.8.1

**Root:** `AbilityTemplate.builder("thorn_burst")`. **Fonte:** [`back/SpikedCloakItem.java`](https://github.com/Octo-Studios/reliquified_ars_nouveau/blob/125e1e3a723d8bc7050026e0670f8ac49535c8bc/src/main/java/it/hurts/shatterbyte/reliquified_ars_nouveau/items/back/SpikedCloakItem.java), commit `125e1e3a723d8bc7050026e0670f8ac49535c8bc`. Auditoria física comprova identidade do `AbilityTemplate`, mas **não** equivalência método-a-método com o bytecode instalado.

- `LivingIncomingDamageEvent` servidor aplica `guardian_resilience` quando `SPIKED_CLOAK_RESISTANCE_UNTIL>gameTime`, reduzindo o dano em `clamp(resistance_bonus,0,0.95)` por stack.
- Se `incoming >= maxHealth*clamp(damage_threshold_fraction,0,1)`, calcula `spikesToShoot=MathUtils.multicast(random,clamp(trigger_chance,0,1),max(1,round(max_spikes)))`. Gera `EntityChimeraProjectile` em círculo ao redor do player, com owner e tags `ran_spiked_cloak_spike`, dano, `chain_depth=0`.
- `bleeding_spikes` embute nível e duração de BLEEDING nas tags dos projéteis; `spike_bloom` embute `chain_chance` e `chain_max_spikes`; a efetiva recursão/dano do projétil pode estar em outro código/mixin e permanece por auditar. `guardian_resilience` estende a janela por `resistance_duration*20` ticks.
- **Perks:** spawn não é hit, `burst_trigger` é XP próprio; claims, caps de projéteis e mixins de on-hit exigem análise física, sem proc de Mastery para cada spike.

**Estado:** 🟡 source-located; ⚠️ configuração, JAR method body, efeitos downstream e QA físico; ⛔ adapter RPG/BA não implementado. Sem nova raiz semântica. Relics/Ars/addon são os donos de casts, recursos e entidades; Black Arcana mantém apenas o runtime próprio.

[Matriz](../PERK-ENGINEERING-MATRIX-0.8.1.md).
