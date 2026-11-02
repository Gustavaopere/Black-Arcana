# Handoff técnico — FTB Chunks 2101.1.22: explosões e claims

**Recorte:** continuação das PRs [#1007](https://github.com/Gustavaopere/Black-Arcana/pull/1007)–[#1010](https://github.com/Gustavaopere/Black-Arcana/pull/1010). A modlist física do sibling registra FTB Chunks NeoForge 2101.1.22 e NeoForge 21.1.250. O Black Arcana continua responsável por `WorldEffectPolicy`; o FTB Chunks não é substituto implícito desse contrato.

A PR #1010 identificou, no JAR publisher 2101.1.22, `FTBChunksForge.mobGriefing(EntityMobGriefingEvent)`, a tag padrão somente com `minecraft:enderman` e uma consulta a `ChunkDimPos(event.getEntity())`. Aquela verificação **não** inspecionou proteção contra explosões.

## Pergunta específica

Existe, no artefato publisher exato, handler `ExplosionEvent.Detonate` e quais classes/métodos JVM ele chama? Como são tratadas as listas de blocos/entidades e chunks? Quais limites impedem inferir proteção para `TremorzillaEntity.breakBlocksAround` quando executa `Level.destroyBlock` ou `BlockState.onBlockExploded` diretamente?

## Processo de descoberta e gate de CI

- A [sonda read-only](ftbchunks_2101_explosion_seam_probe.py) valida o SHA do JAR e da classe `FTBChunksForge.class` já observados na PR #1010; identifica um handler com descritor de `ExplosionEvent$Detonate` e eventuais helpers `lambda$<handler>$...`. Exporta apenas ABI, hashes, callsites simbólicos, offsets e branches selecionados, sem código de implementação.
- O [workflow](../../.github/workflows/ftbchunks-2101-explosion-seam.yml) baixa a versão exata publicada pelo FTB Team e gera evidência limitada. A primeira execução sem o manifesto `FTBCHUNKS-2101-EXPLOSION-ABI.json` é explicitamente **exploratória**. O manifesto só deve ser criado com valores provenientes do JAR real e validado em execução posterior com `--seal`.
- Testes sintéticos de negativas/deriva e a CI integral são gates adicionais, mas não substituem aplicação real de chunks protegidos em servidor.

## Limites inegociáveis

Um listener de `ExplosionEvent.Detonate`, mesmo confirmado, só estabelece um possível caminho de proteção para operações que disparam **aquele evento**. Não concluir que ele intercepta todas as chamadas a `BlockState.onBlockExploded`, `Level.destroyBlock`, spawns ou dano ao alvo. Alterações posteriores de datapacks, mixins, priority de listeners, configuração de claims, resolução de chunks e loaded-chunk state não são certificadas por bytecode isolado.

**Estado:** ⚠️ parcial/condicionado; `NO_MUTATION`; `NOT_CERTIFIED`; `physical_qa=NOT_TESTED`. Nenhuma nova ficha ou provider concluído, sem promoção do Stage 06, e sem autorização de perks que ampliem destruição.
