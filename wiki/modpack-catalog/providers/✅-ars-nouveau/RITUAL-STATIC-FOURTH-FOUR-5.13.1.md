# Ars Nouveau 5.13.1 — lote 4: Burrowing, Cloudshaping, Challenge e Sanctuary

**4 contratos técnicos estáticos adicionais (12/24 → 16/24 Rituals)** sem criar novos IDs, alterar runtime Java, Stage 06.05/09, ou transferir authority ao sibling RPG Skill Tree.

## Identidade e escopo da prova

- Modlist física no `neoforge-rpg-skilltree/main`: `ars-nouveau v5.13.1`, `ars_nouveau` em Minecraft 1.21.1 / NeoForge.
- Fonte imutável `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`.
- [Prova binária 85 glyphs + 24 rituals](EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) fixa classes e IDs registrados, **não** bytecode equivalence dos métodos ou aceitação de cliente/modpack.
- `STATIC_TECHNICAL_CATALOG_ONLY`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.

| Ritual | Classe, trigger e alvo | Fatos indispensáveis ao desenho de perks |
|---|---|---|
| [Burrowing](rituals/burrowing.md) | `RitualDig`, `gameTime%20==0`; quatro offsets de `BlockPos` por camada abaixo do brazier | Harvest level 5, `destroyRespectsClaim`, `playerDestroy` antes de `destroyBlockSafely(...false...)`, segundo BreakEvent e resultado não verificado. `EntityRitualProjectile` é lifecycle/presentation, não quem quebra blocos. Progress avança mesmo quando falha. |
| [Cloudshaping](rituals/cloudshaping.md) | `RitualCloudshaper`, `progress>=18` em ticks de 20; alteração global no `server.overworld()` | Clear usa delay `12000..180000`; Rain `12000..24000`; Thunder `3600..15600`, todos `UniformInt` sorteados. Gunpowder e Lapis Block são inputs distintos, não mana/spell. A classe usa `if` independentes, embora a admissão normal permita apenas um modificador. |
| [Challenge](rituals/challenge.md) | `RitualPillagerRaid`, `progress>=18`; `ServerPlayer` inicial em AABB.inflate(5.0); vanilla `createOrExtendRaid` | `setFinished` exige raid não nula. Modifier aceita `Tags.Items.GEMS_EMERALD` em dificuldade não HARD, mas aumento `raid.numGroups=7` exige `didConsumeItem(Items.EMERALD)` exato. Não contabilizar ondas como casts nem assumir vila existente sem o manager. |
| [Sanctuary](rituals/sanctuary.md) | `DenySpawnRitual` `extends RangeRitual` → `RitualEventQueue` → `EventHandler` → `FinalizeSpawnEvent`/`VillageSiegeEvent` | Natural+Enemy/whitelist sem blacklist e dentro de `radius²`, ou siege numa verificação diferente. Base radius32, + Rotten Flesh até 128 entradas na lógica de item; descrição de raio máximo128 diverge do código. Flag `deniedSpawn` paga `getSourceCost=500` via `takeSourceNow()` quando `gameTime%1200==0`, não por mob; queue seleciona primeiro ritual compatível. |

## Proibições e precauções de engenharia

1. **World safety:** `BlockUtil.destroyRespectsClaim` e `BlockEvent.BreakEvent` do Ars não substituem `WorldEffectPolicy` para um ritual próprio Black Arcana. Burrowing não fornece confirmação por bloco de drop ou sucesso; não contabilizar como ganho/perk causal comprovado.
2. **Global world state:** Weather de Cloudshaping não é buff de área e não suporta automaticamente stacking/cooldown de spell. Randomização e clima do Overworld são provider-native.
3. **Vanilla raid authority:** decisão de village/raid, wave e spawn pertence ao `Raid` manager; modificador de tag não garante `Items.EMERALD` exato. `raid.numGroups` não é API de progressão do RPG.
4. **Event-driven spawn cancellation:** `RitualEventQueue.getRitual` lista braziers por dimensão, pula chunks unloaded e retorna o primeiro que passar pelo predicado; a ordem deriva de um `HashSet`, sem priorização de players. `DenySpawnRitual` não cancela spawn de todos os tipos. `RangeRitual` registra posição a cada 20 ticks; isso não é custo por tick nem hook público de mutação.
5. **Source/ingredientes:** Burrowing, Cloudshaping e Challenge **herdam** `AbstractRitual.getSourceCost()=0`, não comprovação de item grátis. Sanctuary declara `500`, com flag/retries no `RitualBrazierTile` e eventual falta de Source. Não substituir Source por mana própria do Black Arcana.
6. **Sem novas perks implementadas:** RPG Skill Tree só pode fornecer atributos/perks/Mastery/gates via adapter comprovado, com deduplicação e causalidade. Casts, rituais, hazards, persistência e execução Black Arcana continuam próprios e separados.

**Validação necessária:** os GameTests e dedicated-server smoke do Black Arcana verificam integridade de seu próprio runtime, mas não constituem prova de equivalência de método nem teste end-to-end dos rituais do Ars.

**QA física pendente:** equivalência exata de métodos do JAR, alterações de config, multiplayer, side do projectile, chunks carregados, NBT sem `radius`, seleção de braziers sobrepostos, Source starvation/retry, proteção de mundo/claims, drops, raids de mods, clima global, save/restart e execução no pack. Todos `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`; não promover Stage 06.05 nem Stage 09.

**Contadores da branch em relação à main #907:** Rituals **16/24**, Ars Nouveau **69/138**, global **69/2075**; providers fechados **0/164**. Estes valores são revisão documental, sujeitos a sincronização com a main e testes automatizados.
