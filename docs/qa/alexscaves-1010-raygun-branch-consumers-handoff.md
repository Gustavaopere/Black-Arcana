# Raygun 1.0.10 — caminhos consumidores dos ramos X_RAY e GAMMA_RAY

## Autoridade e escopo

Continua o recorte de branches da [PR #1017](https://github.com/Gustavaopere/Black-Arcana/pull/1017), integrado à `Black-Arcana/main@414a8b751394e19d6b94e4916bb104dc6820c53f` com **24/24 workflows pós-merge aprovados**. A modlist física do sibling fixa Alex's Caves Continued **1.0.10**, JAR publisher SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.

A [sonda read-only](alexscaves_1010_raygun_branch_consumers_probe.py) valida a classe `RaygunItem.class` SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c` e o digest de `onUseTick(Level,LivingEntity,ItemStack,int):void` `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5`. Extraem-se **apenas símbolos de invocação, branches, constantes selecionadas e índices locais** de quatro regiões delimitadas do método compilado:

- `[569,669)`: região opcional de busca adicional por `X_RAY`, `LivingEntity.getBoundingBox @575`, `ProjectileUtil.getEntityHitResult @640` e guarda `ifnull @647`.
- `[920,962)`: seleção `GAMMA_RAY` `4/0 @922–932`, escrita no **slot JVM 23 @932**, e enumeração `Level.getEntities @943`.
- `[1080,1123)`: solicitação de status via `MobEffectInstance`, com argumento `800 ticks` e leitura `iload 23 @1114` após a seleção `4/0` no slot `23`.
- `[1125,1161)`: outra seleção `GAMMA_RAY` `4/0 @1138–1148`, junto do envio visual posteriormente observado.

Um censo de acessos tipados (`fload/fstore`, `aload/astore`, `iload/istore`) ao slot JVM 23 no método identifica **usos estáticos** do slot receptor de `@932`; não supõe que todos os acessos compartilhem uma única definição ou aconteçam em cada disparo.

## Gate de evidência

O [workflow específico](../../.github/workflows/alexscaves-1010-raygun-branch-consumers.yml) deve executar 15 testes sintéticos, baixar o JAR publisher exato, verificar SHA-1/SHA-256/bytes da classe e do método, e produzir o manifesto de inspeção sem reproduzir métodos completos de terceiros. A primeira execução é explicitamente `UNSEALED`. A versão observada de `EXACT-RAYGUN-BRANCH-CONSUMERS-1.0.10.json` deve ser incorporada do log CI e validada em nova HEAD final com `--seal`, com todos os demais workflows pré-merge verdes.

## Limites de interpretação

**Anotações de bytecode não são testes físicos nem contratos de mutabilidade.** Branches estáticos e valores `4/0` não fornecem por si só o tipo de visual, amplifier, quantidade de alvos, cooldown, efeito em bloco ou semântica de status. Mesmo uma chamada a `ProjectileUtil.getEntityHitResult` não prova que uma perk possa mudar o alcance preservando critérios de exclusão, LOS e autorização do servidor.

Persistem: `WorldEffectPolicy`, claims/PvP, estado/charge do provider, validação C2S e deduplicação dos acertos/XP, teste físico do modpack. **⚠️ parcial/condicionado, `NO_MUTATION`, `NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`**. Sem promover Stage 06 ou contadores **28/30**.


## Resultado compilado SHA-exato — descoberta CI #41540446712

A [execução exploratória](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41540446712) passou com **15/15 testes sintéticos** e validou o JAR original e o método `onUseTick` (digest `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5`). O [manifesto exato](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-BRANCH-CONSUMERS-1.0.10.json) contém somente observações de quatro regiões delimitadas, não o corpo integral da implementação.

**Região opcional `X_RAY @569–669` — 48 instruções observadas:** `iload 9 @569` → `ifeq @571` salta para `@669` no valor zero. No ramo não zero aparecem `LivingEntity.getBoundingBox @575`, `AABB.inflate @581`, `LivingEntity.getEyePosition @590`, `getViewVector @607/@619`, `Vec3.add @610/@622`, predicado `invokedynamic @635` e `ProjectileUtil.getEntityHitResult @640`. A região inclui `ifge @600 → @666`, `ifnull @647 → @657`, incremento de contador float `fload 23 @657`, `fconst_1 @659`, `fadd @660`, `fstore 23 @661` e retorno a `@595` por `goto @663`. **Isso evidencia um loop de busca condicional que consulta entidades**, mas não basta para determinar LOS, alcance efetivo e exclusões de alvos em todos os ramos.

**Região `GAMMA_RAY @920–962` — 17 instruções:** `iload 18 @922 → ifeq @924` seleciona literal `iconst_4 @927` ou `iconst_0 @931`, convergindo em **`istore 23 @932`**. Em seguida ocorre `Level.getEntities @943` e entrada em `Iterator.hasNext @955`. O literal selecionado não é quantidade de alvos: o método tem a leitura posterior **`iload 23 @1114`** que interessa à aplicação de efeito.

**Região `GAMMA_RAY @1080–1123` — 15 instruções:** `sipush 800 @1111`, `iload 23 @1114`, `MobEffectInstance.<init>(Holder, int, int) @1116` e `LivingEntity.addEffect @1119`. Logo, há **uma chamada nativa que solicita um status com duração 800 ticks e utiliza como argumento de amplifier o slot 23**, cujo valor é selecionado em `@932` entre 4/0 no ramo documentado. Isso não prova que a solicitação foi aceita, que qualquer alvo atingido receberá o status ou que o comportamento sobreviverá a outras políticas do servidor; a pré-condição `RESISTS_RADIATION` e os guards permanecem relevantes.

**Região `GAMMA_RAY @1125–1161` — 16 instruções:** `iload 18 @1138 → ifeq @1140` determina literal `4 @1143` ou `0 @1147`, com literal **800 @1148**; registra-se `UpdateEffectVisualityEntityMessage.<init>(IIII) @1151` seguido de `AlexsCaves.sendMSGToAll(Object) @1154`. Este é **um caminho de mensagem visual**, não comprovante de status ou proc de dano/XP.

**Atenção à reatribuição tipada de slots JVM:** o **índice 23 não representa uma mesma variável semântica em todo o método**. Foram observadas 13 operações no slot 23: inicialmente `fstore/fload` (`@587–661`), depois `astore/aload` (`@689–858`), e finalmente `istore @932` e `iload @1114`. É proibido associar o contador float do loop de X_RAY ao amplifier inteiro de GAMMA_RAY como se fossem o mesmo dado.

**Continuidade:** ainda faltam validar fisicamente os ramos e guards, os efeitos aceitos em alvos resistentes, ownership/servidor, claims/PvP, hit acceptance, packets e o adapter real de perk. `NO_MUTATION` e `NOT_CERTIFIED`; **nenhuma promoção de Stage 06 ou aumento dos contadores**. A primeira CI é de descoberta. Exigir execução nova com `--seal` sobre a última HEAD e 100% das verificações pré-merge.
