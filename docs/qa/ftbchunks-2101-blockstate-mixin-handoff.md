# Handoff — BlockStateMixin compilado do FTB Chunks 2101.1.22

## Escopo e autoridade

Continua as PRs [#1010](https://github.com/Gustavaopere/Black-Arcana/pull/1010)–[#1012](https://github.com/Gustavaopere/Black-Arcana/pull/1012) sobre a proteção de blocos do Tremorzilla. Versões da modlist física do sibling `neoforge-rpg-skilltree`: FTB Chunks NeoForge **2101.1.22**, loader NeoForge **21.1.250**, Alex's Caves Continued **1.0.10**. O `Black Arcana` conserva toda autoridade do runtime e de `WorldEffectPolicy`.

A PR #1012 identificou `ftbchunks-common.mixins.json` com 12 mixins declarados/presentes e as assinaturas de `FTBChunks.explosionDetonate` em 238 classes do publisher JAR, sem invocação JVM direta do método entre classes desse mesmo JAR. Nenhuma conclusão de dispatch dinâmico nem proteções por claims foi autorizada.

## Inspeção adicional — classe e anotações

A [sonda somente de leitura](ftbchunks_2101_blockstate_mixin_probe.py) exige o artefato publisher `ftb-chunks-neoforge-2101.1.22.jar` SHA-256 `4ba1b3352184fa7f6e2aa4bca76edd074867697d62344dfa50dcccdb4dab5217`, o `BlockStateMixin.class` SHA-256 `2920670a37b9ebf4d7768ddf37f488fd685f2e88d4630a82310b75393039d5ce` e `ftbchunks-common.mixins.json` SHA-256 `bd5f99632e804411285c53d1d5fc3cf90f938f265c62e2862b0fc790c00d5ad8`.

O parser Python independente lê somente metadados de classfile: constant pool, anotações de classe/método, nomes/descritores JVM, hashes/tamanhos de bytecode por método. Não exporta corpo de métodos de terceiros nem transfere lógica à implementação Black Arcana. Detecta assinaturas de `@Mixin`, `@Inject`, `@Redirect`, `@Overwrite` somente se realmente presentes; não presume que existem.

O [workflow](../../.github/workflows/ftbchunks-2101-blockstate-mixin.yml) executa testes sintéticos com negativos e baixa o JAR exato do Maven publisher. Na primeira execução coleta evidência `UNSEALED DISCOVERY`. A seguir, apenas valores efetivamente observados devem compor `FTBCHUNKS-2101-BLOCKSTATE-MIXIN-ABI.json`; rerodar com `--seal` sobre a HEAD final e aguardar toda CI pré-merge.

## Invariantes, bloqueios e próximos passos

Mesmo anotações de transformação bem identificadas são metadados **estáticos**; nenhum teste do servidor real ou efeito sobre claims é demonstrado. Não assumir `BlockStateMixin` como interceptador de `Level.destroyBlock`, `BlockState.onBlockExploded` ou `Explosion.getToBlow` sem respectivas referências/anotações e comportamento demonstrado. Continuam pendentes inspeção dos outros mixins de blocos, eventuais hooks externos, regras de claims e QA física.

**Estado:** ⚠️ parcial/condicionado · `NO_MUTATION` · `NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`. Nenhuma ficha adicional, nenhuma perk mutadora, nenhum avanço de Stage 06.
