# Raygun 1.0.10 — desvios condicionais `X_RAY` e `GAMMA_RAY`

## Escopo e fonte de autoridade

Continua a [PR #1016](https://github.com/Gustavaopere/Black-Arcana/pull/1016) integrada em `Black-Arcana/main@8a6bb3ef44f58bea93872f48401363b1a662f5e6`. A versão física de autoridade é Alex's Caves Continued `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.

A [sonda read-only](alexscaves_1010_raygun_condition_branches_probe.py) usa a classe `RaygunItem.class` SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c` e o método exato `onUseTick(Level,LivingEntity,ItemStack,int):void` digest `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5`, proveniente de `javap` Java 21.

## Objetivo delimitado

Esta rodada investiga *o primeiro desvio JVM posterior* a cada uma das **3 leituras do slot 9** (offsets `105`, `122`, `569`) e **5 leituras do slot 18** (`367`, `402`, `922`, `1029`, `1138`), estabelecidas pelo censo de classes da PR #1016. Para cada uma, guarda somente uma janela de 4 instruções anteriores e 6 posteriores e, quando o opcode imediatamente seguinte for `if...`, confirma os offsets de destino e fallthrough presentes na classe.

Outras seis janelas pequenas delimitam `ACCompat.enchantLevel @47`, atribuição `X_RAY @58`, `GAMMA_RAY @332`, atribuição no slot 18 em `@346`, ray trace `@69` e pedido de dano `@1041`. A CI exige SHA da classe/método, recusa offsets e destinos inválidos e executa regressões sintéticas fail-closed.

**A primeira CI é `UNSEALED DISCOVERY`.** O manifesto `EXACT-RAYGUN-CONDITION-BRANCHES-1.0.10.json` será criado exclusivamente com o resultado real e validado com `--seal` na HEAD final, juntamente com todos os workflows obrigatórios antes de qualquer merge.

## Limites de conclusão

Esta evidência cobre **desvios diretos observados, não CFG completo**. O método JVM pode ter estruturas de loop, exceções, reatribuições e domínios de seleção distintos. Mesmo uma condição `ifeq` imediatamente após `iload 9` **não certifica** que X_RAY ignora blocos, muda alcance efetivo ou ultrapassa proteção de claims. `GAMMA_RAY` e `local 18` não devem ser convertidos em dano final ou perk alterável sem validação da atribuição causal, guards e runtime.

A arquitetura continua: servidor autoritativo do Black Arcana, `WorldEffectPolicy`, custos/estado do provider, prevenção de duplicação e contracts reais; RPG Skill Tree permanece sibling de progressão. **Status:** ⚠️ Raygun parcial/condicionado; `NO_MUTATION`, `NOT_CERTIFIED`, `physical_qa=NOT_TESTED`; Stage 06 e índices de fichas inalterados.


## Resultado compilado — descoberta #41513797349

A [CI exploratória](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41513797349) executou **12 testes sintéticos** e a sonda no JAR publisher 1.0.10 SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. O método `onUseTick` foi verificado pelo digest exato `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5`. O [manifesto selável](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-CONDITION-BRANCHES-1.0.10.json) foi extraído diretamente do log do JAR e guarda apenas janelas limitadas.

| Local / leitura | Desvio JVM imediato | Destino quando o valor é zero | Fallthrough quando não zero | Evidência local |
|---|---|---|---|---|
| `X_RAY slot 9 @105` | `ifeq @107` | `@115` | `@110` | seleciona referência de `HitResult` (`aload 11` versus `aload 12`) |
| `X_RAY slot 9 @122` | `ifeq @124` | `@132` | `@127` | segunda seleção entre referências dos resultados anteriores |
| `X_RAY slot 9 @569` | `ifeq @571` | `@669` | `@574` | entra em cálculo com `getBoundingBox @575` e `fload 8 @578` quando não zero |
| `GAMMA_RAY slot 18 @367` | `ifeq @369` | `@386` | `@372` | referência à partícula `BLUE_RAYGUN_EXPLOSION` no fallthrough |
| `GAMMA_RAY slot 18 @402` | `ifeq @404` | `@421` | `@407` | referência à partícula `BLUE_HAZMAT_BREATHE` no fallthrough |
| `GAMMA_RAY slot 18 @922` | `ifeq @924` | `@931` | `@927` | seleciona literalmente `4` ou `0` |
| `GAMMA_RAY slot 18 @1029` | `ifeq @1031` | `@1038` | `@1034` | seleciona `1.5f` ou `2.0f` antes de `ACCompat.hurt @1041` |
| `GAMMA_RAY slot 18 @1138` | `ifeq @1140` | `@1147` | `@1143` | seleciona literalmente `0` ou `4` para um caminho posterior, não resultado de dano certificado |

Os pontos de produção também estão ancorados: `X_RAY @44` → `ACCompat.enchantLevel @47` → `ifle @50` → `istore 9 @58`; `GAMMA_RAY @332` → `ACCompat.enchantLevel @335` → `ifle @338` → `istore 18 @346`. O mesmo método compilado apresenta as leituras selecionadas acima. Este recorte não demonstra a aplicabilidade global dos ramos, nem se os hits são aceitos pelo servidor.

**Conclusão bounded:** a seleção de referências de `HitResult` e a região adicional de busca de entidade são condicionadas estaticamente pela flag derivada de X_RAY; partículas e valores usados na chamada de dano são condicionados estaticamente pela flag derivada de GAMMA_RAY. Esses fatos não homologam alcance, penetração de blocos, colisão, owner, PvP, proteção de claims, frequência ou número de acertos. Permanece obrigatório observar a implementação transformada no modpack e os contratos de `WorldEffectPolicy`.

**Gate restante:** validar `--seal` na HEAD final, com 100% dos workflows pré-merge aprovados; nenhum avanço de 28/30, nenhum hook mutador ou Stage 06.
