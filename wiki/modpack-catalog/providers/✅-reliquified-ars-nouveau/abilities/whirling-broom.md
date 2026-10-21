# Whirling Flight — Whirling Broom

- **Provider:** Reliquified Ars Nouveau (`reliquified_ars_nouveau`), versão física `0.8.1`.
- **Status:** ✅ `COUNTED_EXACT` para identidade estática de uma habilidade de relíquia; runtime/Survival ⚠️.
- **Item registrado:** `reliquified_ars_nouveau:whirling_broom`.
- **Classe física:** `it.hurts.shatterbyte.reliquified_ars_nouveau.items.WhirlingBroomItem`.
- **ID primário `AbilityTemplate.builder`:** `broom`.
- **Nome da habilidade:** Whirling Flight (localização source-pinned 0.8.1).
- **Contribuição semântica:** uma raiz provider-native já contabilizada; **+0** no checkpoint desta auditoria.

## Evidência física

[Java21 #38461801129](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38461801129): o JAR físico SHA-1 `4be1f4b0fd7fbec6618596e2e7c3705db88a7579` inclui o item, a classe e exatamente uma chamada compilada a `AbilityTemplate.builder` com o ID primário acima. Ver [dossiê 19/19](../EXACT-BINARY-RELIC-ABILITIES-0.8.1.md) e [catálogo source-pinned](../README.md).

## Causalidade, exclusões e gates

O item é contêiner da habilidade; rank, modificadores, sub-habilidades, partículas, projéteis, efeitos e eventos de progressão não contam como raízes extras sem nova prova independente. Quando a ação usa casting ou glyphs de Ars Nouveau, sua execução e recursos permanecem sob a autoridade do Ars/provider. Não duplicar mana/cooldowns, dano ou recompensas no Black Arcana.

A auditoria **não** certifica valores de custo/cooldown, algoritmo de combate, aquisição em Survival, loot efetivo, persistência, compatibilidade Relics/Ars ou servidor dedicado. Qualquer adapter Black Arcana requer contrato real e QA próprio.

---

## Engenharia causal — source declarado 0.8.1

**Root:** `AbilityTemplate.builder("broom")`. **Fonte:** [`WhirlingBroomItem.java`](https://github.com/Octo-Studios/reliquified_ars_nouveau/blob/125e1e3a723d8bc7050026e0670f8ac49535c8bc/src/main/java/it/hurts/shatterbyte/reliquified_ars_nouveau/items/WhirlingBroomItem.java), commit `125e1e3a723d8bc7050026e0670f8ac49535c8bc`. Auditoria física comprova identidade do `AbilityTemplate`, mas **não** equivalência método-a-método com o bytecode instalado.

- `use` no servidor verifica cooldown persistido `WHIRLING_BROOM_COOLDOWN_UNTIL`, rejeita player montado em `WhirlingBroomEntity`, descarta broom antiga do mesmo passageiro no raio 96 e cria nova `WhirlingBroomEntity` com parâmetros nativos `speed`, `max_height`, `broom_health`, `damage_reduction`, sprint e synergy `storm_flight`.
- Persiste saúde atual do veículo e ID do stack, `startRiding(broom,true)`; `inventoryTick` regenera a saúde via `health_regen_interval` e controla cooldown/saúde do próprio item.
- `LivingIncomingDamageEvent` com player como passageiro e modifier `flight_guard` reduz dano via `clamp(Σdamage_reduction,0,0.95)`. `ProjectileImpactEvent` cancela impacto em player no veículo se `projectile_phase` está ativo ou impacto na entidade broom (ramo próprio).
- **Perks:** movimento do veículo, sprint mana, colisões e event packets pertencem à `WhirlingBroomEntity` e rede do addon; não transformar dados cliente em autoridade. QA de mounts, servidor e storm synergy obrigatória.

**Estado:** 🟡 source-located; ⚠️ configuração, JAR method body, efeitos downstream e QA físico; ⛔ adapter RPG/BA não implementado. Sem nova raiz semântica. Relics/Ars/addon são os donos de casts, recursos e entidades; Black Arcana mantém apenas o runtime próprio.

[Matriz](../PERK-ENGINEERING-MATRIX-0.8.1.md).
