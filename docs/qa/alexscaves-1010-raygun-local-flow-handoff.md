# Raygun 1.0.10 — censo de acessos a locais JVM e precedência de branches

## Objetivo

Continua a [PR #1015](https://github.com/Gustavaopere/Black-Arcana/pull/1015), integrada em `Black-Arcana/main@2c6454ef2168d5425749eeac7493c30c6eea86fe`, para investigar o que os offsets do `RaygunItem.onUseTick` **efetivamente observam**, antes de falar de alteração de range, X_RAY, target ou dano.

A versão de autoridade é o publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A classe `RaygunItem.class` deve ter SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c` e o método `onUseTick(Level,LivingEntity,ItemStack,int):void` SHA-256 de parse `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5`.

## Método de auditoria

A [sonda de leitura](alexscaves_1010_raygun_local_flow_probe.py) lista todas as instruções `iload`/`istore`, `fload`/`fstore`, `aload`/`astore`, `lload`/`lstore`, `dload`/`dstore` e `iinc` que acessam **somente os slots JVM 7, 8, 9, 18**, com janelas restritas junto às atribuições e seis pontos conhecidos: `fload 7 @38`, `fstore 8 @41`, `X_RAY @44`, `istore 9 @58`, `iload 18 @1029` e `ACCompat.hurt @1041`.

**Atenção:** o índice de uma variável local JVM é um slot de armazenamento, **não uma identidade semântica estável** no método inteiro. Branches podem redefinir o mesmo slot. O censo preserva offset, opcode, tipo e proximidade, mas **não** implementa dataflow, reaching definitions, CFG completo ou exception edges. Não declarar que todos os usos de `local 9` dependem de X_RAY ou que todo `local 18` significa um mesmo modo sem prova de caminho.

O [workflow dedicado](../../.github/workflows/alexscaves-1010-raygun-local-flow.yml) aplica 12 regressões negativas/sintéticas, confirma os hashes oficiais e produz apenas um JSON limitado com as operações relevantes. A primeira execução é `UNSEALED DISCOVERY`, seguida do manifesto `EXACT-RAYGUN-LOCAL-FLOW-1.0.10.json` derivado do resultado real e validação por `--seal` na HEAD final. A integração depende da CI premerge inteira.

## Condição de segurança

- `NO_MUTATION`: não alterar range/targeting, custos, hits ou os operandos do provider.
- `NOT_CERTIFIED`: as fichas Raygun e Tremorzilla Beam permanecem ⚠️ parciais/condicionadas.
- `physical_qa=NOT_TESTED`: CI de análise estática/GameTests do Black Arcana **não equivale a testar o Raygun carregado no modpack físico**.
- `WorldEffectPolicy`, PvP, claims, pacotes C2S, estados `ChargeUsed/UseTime` e deduplicação de dano/XP continuam autoridades e riscos separados.
- Não promover Stage 06, contadores ou `COMPLETE_PERK_READY`.

A próxima decisão após o selo deve distinguir **quais atribuições por ramo alimentam** os alvos de dano e de distância; somente então considerar uma interface realmente suportada pelo provider ou manter o bloqueio.


## Resultado observado no JAR exato — CI exploratória #41510061345

A [execução de descoberta](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41510061345) aprovou **12/12 testes sintéticos** e verificou o publisher JAR original (75.279.314 bytes), a classe `RaygunItem.class` (SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c`) e as **523 instruções** de `onUseTick` (digest `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5`). Os fatos estão no [manifesto do censo](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-LOCAL-FLOW-1.0.10.json).

| Slot JVM | Instrução de escrita observada | Leituras observadas no método | Interpretação com restrições |
|---|---|---|---|
| `7` (float) | `fstore 7 @33` | `fload @38, @270, @360` | `@28 fdiv`, desvio `@29 goto @33` e alternativa `@32 fconst_1` precedem a atribuição. Há valor por branch; não basta para certificar a curva de range |
| `8` (float) | `fstore 8 @41` | `fload @66, @75, @90, @578, @597` | `25.0f @35 × fload 7 @38` é armazenado em `8 @41`. São acessos estáticos; as diferenças de branch e raytrace ainda não equivalem a alcance final |
| `9` (int) | `istore 9 @58` | `iload @105, @122, @569` | A comparação com `ACCompat.enchantLevel(X_RAY) @47` produz 0/1 via `ifle @50`, `iconst_1 @53` e `iconst_0 @57`. O efeito posterior de cada leitura requer análise de branch |
| `18` (int) | `istore 18 @346` | `iload @367, @402, @922, @1029, @1138` | `@341 iconst_1` / `@345 iconst_0` convergem em `@346`, depois da consulta ao encantamento `GAMMA_RAY @332` observada anteriormente. Ainda não se comprova a fórmula de seleção nem a reachability de cada leitura |

**Relação entre dano e slot 18:** a janela da PR #1015 mostra `iload 18 @1029` → `ifeq @1031` → `fconst_2 @1034` ou `ldc_w 1.5f @1038` → `ACCompat.hurt @1041`, seguida por guarda do retorno `ifeq @1044`. Isso é uma escolha de valores de **dano solicitado** na região compilada e não demonstra dano aceito, bônus de `GAMMA_RAY` em todos os caminhos, incidência por hit ou autoridade PvP.

A população selecionada contém **4 acessos** ao slot 7, **6** ao 8, **4** ao 9 e **6** ao 18. Esses são contadores de referências JVM no método, não quantidades de disparos, acertos, alvos ou ticks.

O censo concluiu uma lacuna de **proveniência imediata das atribuições e conjunto de leituras**. Ele **não** resolve path conditions, todas as reaching definitions, ramo de X_RAY em `@105/@122/@569` ou seleção definitiva de `GAMMA_RAY` em `@346`. Não marcar o Raygun como `COMPLETE_PERK_READY`; a próxima verificação deve tratar a condição do branch e o carregamento/controle de servidor de forma específica.

O manifesto foi criado a partir da descoberta; é obrigatório rodar a CI **selada** na última HEAD da PR antes do merge.
