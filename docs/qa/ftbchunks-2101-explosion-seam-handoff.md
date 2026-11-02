# Handoff técnico — FTB Chunks 2101.1.22: explosões e claims

**Recorte:** continuação das PRs [#1007](https://github.com/Gustavaopere/Black-Arcana/pull/1007)–[#1010](https://github.com/Gustavaopere/Black-Arcana/pull/1010). A modlist física do sibling registra FTB Chunks NeoForge 2101.1.22 e NeoForge 21.1.250. O Black Arcana continua responsável por `WorldEffectPolicy`; o FTB Chunks não é substituto implícito desse contrato.

A PR #1010 identificou, no JAR publisher 2101.1.22, `FTBChunksForge.mobGriefing(EntityMobGriefingEvent)`, a tag padrão somente com `minecraft:enderman` e uma consulta a `ChunkDimPos(event.getEntity())`. Aquela verificação **não** inspecionou proteção contra explosões.

## Pergunta específica

Existe, no artefato publisher exato, handler `ExplosionEvent.Detonate` e quais classes/métodos JVM ele chama? Como são tratadas as listas de blocos/entidades e chunks? Quais limites impedem inferir proteção para `TremorzillaEntity.breakBlocksAround` quando executa `Level.destroyBlock` ou `BlockState.onBlockExploded` diretamente?

## Processo de descoberta e gate de CI

- A [sonda read-only](ftbchunks_2101_explosion_seam_probe.py) valida o SHA do JAR e da classe `FTBChunksForge.class` já observados na PR #1010; identifica um handler com descritor de `ExplosionEvent$Detonate` e eventuais helpers `lambda$<handler>$...`. Exporta apenas ABI, hashes, callsites simbólicos, offsets e branches selecionados, sem código de implementação.
- O [workflow](../../.github/workflows/ftbchunks-2101-explosion-seam.yml) baixa a versão exata publicada pelo FTB Team e gera evidência limitada. A primeira execução sem o manifesto `FTBCHUNKS-2101-EXPLOSION-ABI.json` é explicitamente **exploratória**. O manifesto só deve ser criado com valores provenientes do JAR real e validado em execução posterior com `--seal`.
- Testes sintéticos de negativas/deriva e a CI integral são gates adicionais, mas não substituem aplicação real de chunks protegidos em servidor.

## Resultado observado no JAR exato (descoberta CI #41454208921)

O artefato Maven `ftb-chunks-neoforge-2101.1.22.jar` (**655.807 bytes**, SHA-256 `4ba1b3352184fa7f6e2aa4bca76edd074867697d62344dfa50dcccdb4dab5217`) foi verificado e inspecionado com Java 21. O [manifesto de ABI selecionada](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/FTBCHUNKS-2101-EXPLOSION-ABI.json) guarda hashes, descritores, offsets e chamadas.

**Descoberta importante:** a versão compilada não apresenta handler com descritor de `net.neoforged.neoforge.event.level.ExplosionEvent$Detonate` entre as classes candidatas encontradas por referências de constant-pool. A classe principal `FTBChunksForge.class` contém 4 métodos declarados e nenhum método relacionado a explosões no recorte. Em `FTBChunks.class` (SHA-256 `358473a336917b4b13103a9dec51384fe61c9424058a794e51277f8204140e9e`) foram localizados:

| Método exato | Descritor JVM | Observação estática |
|---|---|---|
| `ignoreExplosion` | `(Level, Explosion)Z` | Examina `Level.isClientSide`, `Explosion.getToBlow`, entidade de origem e config `PROTECT_UNKNOWN_EXPLOSIONS` |
| `explosionDetonate` | `(Level, Explosion, List)V` | Examina `DISABLE_PROTECTION`, `ignoreExplosion`, `Explosion.getToBlow`, `Explosion.clearToBlow`, coleções e `BlockPos` |
| `lambda$explosionDetonate$6` | `(ChunkDimPos)Boolean` | Consulta `ClaimedChunkManagerImpl.getChunk` e `ClaimedChunkImpl.allowExplosions` |

No recorte de classes do próprio JAR que contêm referências a `ExplosionEvent` ou ao símbolo `explosionDetonate`, a sonda não encontrou uma **invocação JVM direta** a `FTBChunks.explosionDetonate` (zero callsites selecionados). O JAR declara `ftbchunks-common.mixins.json`. Isso **não demonstra que o método é inativo**: transformações, mixins, hooks externos, invocação indireta e outros artefatos não foram reconstruídos. A assinatura `(Level, Explosion, List)V` não deve ser apresentada como `ExplosionEvent.Detonate` do NeoForge sem evidência adicional.

O recorte prova existência dos métodos e referências compiladas; **não prova cobertura de claims por bloco, filtragem final de `getToBlow`, nem que operações diretas do Tremorzilla ativem esse caminho**. A próxima etapa técnica é validar a configuração e a aplicação real do mixin/hook responsável pela invocação, com execução de servidor protegendo chunks diferentes e verificação de `Level.destroyBlock` versus efeitos de explosão.

A [primeira execução](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41454208921) foi exploratória. A HEAD final precisa repetir a CI em modo `--seal` antes do merge.

## Limites inegociáveis

Um listener de `ExplosionEvent.Detonate`, mesmo confirmado, só estabelece um possível caminho de proteção para operações que disparam **aquele evento**. Não concluir que ele intercepta todas as chamadas a `BlockState.onBlockExploded`, `Level.destroyBlock`, spawns ou dano ao alvo. Alterações posteriores de datapacks, mixins, priority de listeners, configuração de claims, resolução de chunks e loaded-chunk state não são certificadas por bytecode isolado.

**Estado:** ⚠️ parcial/condicionado; `NO_MUTATION`; `NOT_CERTIFIED`; `physical_qa=NOT_TESTED`. Nenhuma nova ficha ou provider concluído, sem promoção do Stage 06, e sem autorização de perks que ampliem destruição.
