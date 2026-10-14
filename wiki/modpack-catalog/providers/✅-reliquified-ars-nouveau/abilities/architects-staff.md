# Arcane Masonry — Architect's Staff

- **Provider:** Reliquified Ars Nouveau (`reliquified_ars_nouveau`), versão física `0.8.1`.
- **Status:** ✅ `COUNTED_EXACT` para identidade estática de uma habilidade de relíquia; runtime/Survival ⚠️.
- **Item registrado:** `reliquified_ars_nouveau:architects_staff`.
- **Classe física:** `it.hurts.shatterbyte.reliquified_ars_nouveau.items.ArchitectsStaffItem`.
- **ID primário `AbilityTemplate.builder`:** `bridgecraft`.
- **Nome da habilidade:** Arcane Masonry (localização source-pinned 0.8.1).
- **Contribuição semântica:** uma raiz provider-native já contabilizada; **+0** no checkpoint desta auditoria.

## Evidência física

[Java21 #38461801129](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38461801129): o JAR físico SHA-1 `4be1f4b0fd7fbec6618596e2e7c3705db88a7579` inclui o item, a classe e exatamente uma chamada compilada a `AbilityTemplate.builder` com o ID primário acima. Ver [dossiê 19/19](../EXACT-BINARY-RELIC-ABILITIES-0.8.1.md) e [catálogo source-pinned](../README.md).

## Causalidade, exclusões e gates

O item é contêiner da habilidade; rank, modificadores, sub-habilidades, partículas, projéteis, efeitos e eventos de progressão não contam como raízes extras sem nova prova independente. Quando a ação usa casting ou glyphs de Ars Nouveau, sua execução e recursos permanecem sob a autoridade do Ars/provider. Não duplicar mana/cooldowns, dano ou recompensas no Black Arcana.

A auditoria **não** certifica valores de custo/cooldown, algoritmo de combate, aquisição em Survival, loot efetivo, persistência, compatibilidade Relics/Ars ou servidor dedicado. Qualquer adapter Black Arcana requer contrato real e QA próprio.

---

## Engenharia causal — source 0.8.1

**Root:** `AbilityTemplate.builder("bridgecraft")`. **Fonte:** [`ArchitectsStaffItem.java`](https://github.com/Octo-Studios/reliquified_ars_nouveau/blob/125e1e3a723d8bc7050026e0670f8ac49535c8bc/src/main/java/it/hurts/shatterbyte/reliquified_ars_nouveau/items/ArchitectsStaffItem.java) no commit `125e1e3a723d8bc7050026e0670f8ac49535c8bc`. O JAR confirma identidade estática, **não** identidade binária exata dos corpos de métodos com o source.

- `use` define primeiro ponto a partir do bloco visado (ray pick 64) e armazena `ARCHITECTS_STAFF_FIRST_POINT` como `WorldPosition`; `releaseUsing` servidor rejeita dimensão diferente, gera trajetória voxel com **limite explícito de 4096 iterações** e exclui as pontas.
- Limita unidades de construção a `min(pathList.size(),charges,max(1,round(max_bridge_length)))`; só coloca `BlockRegistry.MAGE_BLOCK` com `TEMPORARY=true` em locais in-bounds, replaceable, sem BlockEntity e desobstruídos. Cobra **somente** `createdBlocks` em `ARCHITECTS_STAFF_CHARGES` e agenda `BRIDGE_ACTIVE_UNTIL=gameTime+round(max(1,bridge_duration)*20)`.
- XP do Relics usa `bridge_created` e `bridge_block_created` quando `createdBlocks>0`. `vital_support` e `ballistic_support` modificam eventos de cura/dano durante a janela; `disappearance` lida com VANISHING e bloqueio temporário de ações em métodos de inventário/eventos.
- **Risco:** world placement, cor temporária e eventual restauração são Ars/host-owned; o método source-local mostrado não prova claims em cada bloco colocado. Obrigatório testar WorldEffectPolicy BA **apenas nas próprias magias**, claims de terceiros, rollback, cap de blocos e upgrades antes de qualquer perk de colocação.

**Status:** 🟡 mecanismo source-located; ⚠️ JAR, configuração e QA físico; ⛔ adapter perks/Mastery não homologado. Nenhuma raiz semântica extra. Providers mantêm execução e recursos; Black Arcana seu runtime, RPG Skill Tree progressão por contrato.

[Matriz 0.8.1](../PERK-ENGINEERING-MATRIX-0.8.1.md).
