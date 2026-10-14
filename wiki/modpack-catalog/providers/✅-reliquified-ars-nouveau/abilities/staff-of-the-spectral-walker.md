# Spectral Dash — Staff of the Spectral Walker

- **Provider:** Reliquified Ars Nouveau (`reliquified_ars_nouveau`), versão física `0.8.1`.
- **Status:** ✅ `COUNTED_EXACT` para identidade estática de uma habilidade de relíquia; runtime/Survival ⚠️.
- **Item registrado:** `reliquified_ars_nouveau:staff_of_the_spectral_walker`.
- **Classe física:** `it.hurts.shatterbyte.reliquified_ars_nouveau.items.StaffOfTheSpectralWalkerItem`.
- **ID primário `AbilityTemplate.builder`:** `spectral`.
- **Nome da habilidade:** Spectral Dash (localização source-pinned 0.8.1).
- **Contribuição semântica:** uma raiz provider-native já contabilizada; **+0** no checkpoint desta auditoria.

## Evidência física

[Java21 #38461801129](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38461801129): o JAR físico SHA-1 `4be1f4b0fd7fbec6618596e2e7c3705db88a7579` inclui o item, a classe e exatamente uma chamada compilada a `AbilityTemplate.builder` com o ID primário acima. Ver [dossiê 19/19](../EXACT-BINARY-RELIC-ABILITIES-0.8.1.md) e [catálogo source-pinned](../README.md).

## Causalidade, exclusões e gates

O item é contêiner da habilidade; rank, modificadores, sub-habilidades, partículas, projéteis, efeitos e eventos de progressão não contam como raízes extras sem nova prova independente. Quando a ação usa casting ou glyphs de Ars Nouveau, sua execução e recursos permanecem sob a autoridade do Ars/provider. Não duplicar mana/cooldowns, dano ou recompensas no Black Arcana.

A auditoria **não** certifica valores de custo/cooldown, algoritmo de combate, aquisição em Survival, loot efetivo, persistência, compatibilidade Relics/Ars ou servidor dedicado. Qualquer adapter Black Arcana requer contrato real e QA próprio.

---

## Engenharia causal — source 0.8.1

**Root:** `AbilityTemplate.builder("spectral")`. **Fonte:** [`StaffOfTheSpectralWalkerItem.java`](https://github.com/Octo-Studios/reliquified_ars_nouveau/blob/125e1e3a723d8bc7050026e0670f8ac49535c8bc/src/main/java/it/hurts/shatterbyte/reliquified_ars_nouveau/items/StaffOfTheSpectralWalkerItem.java) no commit `125e1e3a723d8bc7050026e0670f8ac49535c8bc`. O JAR confirma identidade estática, **não** identidade binária exata dos corpos de métodos com o source.

- `use` de jogador servidor exige carga positiva e grava posição/dimensão do início, `MOVE_TICKS`, `CHARGES`, estado de spectral e fall immunity em data components. `onUseTick` consome **uma carga por 20 move ticks** no interior de `INTANGIBLE_AIR` e aplica velocidade dirigida; modifier `immortality` fornece `RelicsMobEffects.IMMORTALITY` por 5 ticks renováveis.
- `spectral_vision` pesquisa `LivingEntity` no AABB `entity_reveal_radius` e aplica `GLOWING` por 10 ticks. O percurso cria/refresca `BlockRegistry.INTANGIBLE_AIR` com amostras à frente, raio `2.5`, distância predita clamped `[2,5]`, passo clamped `[0.15,0.3]`; rejeita blocos com BlockEntity, indestrutíveis, ar e os negados por `BlockUtil.destroyRespectsClaim`.
- `releaseUsing` verifica posição salva e pode retornar por teleporte para ponto de segurança; mantém proteções breves contra queda na saída. Efeito de mundo e ciclo do `IntangibleAirTile` permanecem provider-native.
- **Risco:** escaneamentos volumétricos, mutação/restauração de blocos, chunk loading, PvP e fallback de posição segura requerem teste dedicado. Não converter movimento espectral em teleporte/cast próprio BA nem conceder Mastery por cada voxel temporário.

**Status:** 🟡 mecanismo source-located; ⚠️ JAR, configuração e QA físico; ⛔ adapter perks/Mastery não homologado. Nenhuma raiz semântica extra. Providers mantêm execução e recursos; Black Arcana seu runtime, RPG Skill Tree progressão por contrato.

[Matriz 0.8.1](../PERK-ENGINEERING-MATRIX-0.8.1.md).
