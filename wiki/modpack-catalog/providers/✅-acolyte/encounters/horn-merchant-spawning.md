# Horn Merchant spawning — Acolyte 1.0.3

**Tipo:** scheduler `CustomSpawner` do mercador `acolyte:horn_merchant`. O catálogo de trades pertence à economia; este é o acesso ao encontro.

`ModCommonSetup.onLevelTick` executa o spawner no `LevelTickEvent.Post` do **Overworld servidor**, cria uma instância estática se ainda ausente e chama `tick(level,true,true)`. O construtor começa com delay de **24.000 ticks**. A tentativa seguinte redefine o delay para **24.000–35.999 ticks**, antes de testar `allowHornMerchantSpawning`. O gate aleatório aceita valores 0–15 de `nextInt(100)`: **16/100**, não 15/100. Ambos os booleanos da interface estão presentes no descritor, mas não são consultados pelo método observado.

A tentativa usa um jogador aleatório; sem jogador retorna zero. Cada offset X/Z tem sinal independente e módulo **24–39 blocos**. A posição é projetada pelo heightmap `MOTION_BLOCKING_NO_LEAVES`; exige posição dentro da world border e bloco de destino de ar. Cria o mercador com `MobSpawnType.EVENT`; sucesso retorna 1 e define despawn delay **48.000 ticks**, falha retorna 0. Este método não demonstra busca alternativa se o único local falhar, cap de mercadores, biome restriction ou regra de luz/dificuldade. Timer é campo da instância estática, sem persistência de timer demonstrada aqui.

**Evidência exata:** `net/raptorzizi/acolyte/entity/mobs/horn_merchant/HornMerchantSpawner.class`, `<init>()V` PCs 4–11; `tick(Lnet/minecraft/server/level/ServerLevel;ZZ)I` PCs 0–74 (delay 0–35, gamerule 36–50, gate 51–68); `spawnMerchantNearPlayer(Lnet/minecraft/server/level/ServerLevel;)I` PCs 0–165 (offsets 16–70, heightmap/border/ar 72–126, spawn/despawn 127–163). `net/raptorzizi/acolyte/setup/ModCommonSetup.class`, `onLevelTick(Lnet/neoforged/neoforge/event/tick/LevelTickEvent$Post;)V` PCs 0–53.

**Integração:** a assinatura é um consumidor de lifecycle e não um ponto aprovado para duplicar mercadores ou garantir o resultado de troca. O ciclo de disponibilidade e os trades físicos do pack permanecem pendentes de QA.

## Limite de integração e QA

Acolyte controla este contexto de encontro/configuração; Iron’s mantém a identidade e resolução das magias, scrolls e recompensas de seu namespace. A observação do JAR não valida um ponto mutador para Black Arcana. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. Não foi comprovada igualdade de hash com o JAR instalado. Esta ficha resume fatos de interoperabilidade, sem reproduzir implementação, NBT ou assets.

**Base:** publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`; [contratos binários](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).
