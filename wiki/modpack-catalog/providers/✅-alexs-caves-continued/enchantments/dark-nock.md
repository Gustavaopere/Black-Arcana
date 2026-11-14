# Dark Nock — aceleração condicionada da carga do Dreadbow (publisher 1.0.10)

**Estado:** ✅ **contrato técnico estático individual certificado**, escopo `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`, exclusivamente para `alexscaves:dark_nock` no publisher 1.0.10. O selo causal SHA-exato valida os 13 métodos nativos pertinentes e dois classfiles com referência direta, reproduzindo o relatório completo a partir do JAR. A identidade do Dreadbow/Arrow continua compartilhada, não configura uma nova raiz de magia. `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `mutation=NO_MUTATION` · **perks mutadores não autorizados**.

**Efeito:** reduz o denominador da carga do **Dreadbow** de `40 ticks` (sem o encantamento) para **32 / 24 / 16 ticks** nos níveis **I / II / III**, respectivamente. O tempo ajusta **a função de potência do disparo normal e o progresso visual**, fazendo com que a mesma quantidade de ticks de uso produza potência maior. **Não** é um multiplicador independente de velocidade da flecha, raio de área, hitbox, dano base ou quantidade fixa de projéteis.

## 1. Proveniência e escopo

| Fonte | Evidência técnica |
|---|---|
| Mod e runtime | Alex's Caves Continued, `alexscaves`, Minecraft **1.21.1** / **NeoForge** |
| Publisher JAR exato | `alexscaves-1.0.10-neoforge+1.21.1.jar`, **75.279.314 bytes** |
| SHA-1 / SHA-256 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` / `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Recurso físico | `data/alexscaves/enchantment/dark_nock.json`, **358 bytes**, SHA-256 `569cb5857db11189b2eb8a1163d53a440587ab02e2f14bc8296aaaf91dcd8033` |
| Classfile do consumer | `com/github/alexmodguy/alexscaves/server/item/DreadbowItem.class`, SHA-256 `b9cd6e843f923877775e38b89214e8649c10d4d5be704ed9dd377900439d44ae` |
| Comprovação reutilizada | [manifesto SHA-exato Dreadbow](../EXACT-DREADBOW-CONTRACTS-1.0.10.json), [memorial técnico do contrato](../EXACT-DREADBOW-CONTRACTS-1.0.10.md), [equipamento Dreadbow](../equipment/dreadbow.md), [decisões de disparo delimitadas](../damage-types/EXACT-DREADBOW-DECISIONS-1.0.10.json) e [Dark Arrow](../damage-types/dark-arrow.md) |

O código-fonte público `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara versão **1.1.1**, portanto **não** é autoridade geral para o binário 1.0.10. Excepcionalmente, o **conteúdo bruto** do `dark_nock.json` desse snapshot possui SHA-256 **idêntico** ao do recurso publisher listado no manifesto 1.0.10; **somente a identidade desses bytes de JSON** está estabelecida, sem presumir paridade entre classfiles das versões.

Esta é uma **ficha de encantamento** e não substitui as fichas já certificadas do Dreadbow, Dark Arrow ou das outras quatro propriedades de encantamento do arco. Código e assets proprietários do provider não foram copiados para o runtime do Black Arcana. Provas anteriores são referenciadas, não reemitidas.

## 2. JSON de encantamento e compatibilidade

O recurso `alexscaves:dark_nock` registra:

| Campo | Valor publisher exato 1.0.10 |
|---|---|
| `description.translate` | `enchantment.alexscaves.dark_nock` |
| `supported_items` | `#alexscaves:enchantable/dreadbow` |
| `weight` | `2` (peso de seleção, não probabilidade direta de proc) |
| `max_level` | `3` (III) |
| `min_cost.base` / `per_level_above_first` | `1` / `10` |
| `max_cost.base` / `per_level_above_first` | `41` / `10` |
| `anvil_cost` | `4` |
| `slots` | `mainhand` |
| `exclusive_set` neste recurso | Não declarado |

Os custos de encantamento parametrizados para I/II/III são, respectivamente: mínimo **1/11/21** e máximo **41/51/61**. Esses números **não** são mana, durabilidade consumida por tiro, cooldown ou carga do arco.

O item aplicável pertence à tag física `data/alexscaves/tags/item/enchantable/dreadbow.json`, que no contrato publicado contém `alexscaves:dreadbow`. Não confundir `slots=["mainhand"]` com alcance, mira, dupla mão ou quantidade de projéteis.

**Exclusão assimétrica na declaração:** o recurso físico de **Relentless Darkness** declara `alexscaves:dark_nock` em seu `exclusive_set`, junto de `precise_volley` e `twilight_perfection`; o recurso de Dark Nock **não** declara exclusões próprias. Isso informa a compatibilidade de dados do provider, **não** comprova como alterações por outros datapacks ou comandos serão resolvidas na configuração real.

## 3. Consumer JVM: `DreadbowItem.getMaxLoadTime`

**Owner:** `com.github.alexmodguy.alexscaves.server.item.DreadbowItem`, classfile SHA-256 acima.

**Método:** `getMaxLoadTime(ItemStack)I`, descritor `(Lnet/minecraft/world/item/ItemStack;)I`. O [manifesto exato](../EXACT-DREADBOW-CONTRACTS-1.0.10.json) registra as âncoras JVM:

- `@1`: campo `ACEnchantmentRegistry.RELENTLESS_DARKNESS`; `@4` lê seu nível por `ACCompat.enchantLevel`; `@7` testa a presença (nível positivo); `@10` fornece `5` no ramo Relentless.
- `@12`: `bipush 40`; `@14`: `bipush 8`; `@17`: `ACEnchantmentRegistry.DARK_NOCK`; `@20`: `ACCompat.enchantLevel`; `@24`: `isub`; `@25`: `ireturn`.
- A multiplicação pelo nível entre os literais e a subtração é parte do contrato analisado do helper **já registrado** na [ficha do Dreadbow](../equipment/dreadbow.md).

Definindo `L=ACCompat.enchantLevel(stack,DARK_NOCK)` e `R=ACCompat.enchantLevel(stack,RELENTLESS_DARKNESS)`:

`M(stack) = 5` quando `R>0`; caso contrário, `M(stack)=40−8×L`.

| Nível Dark Nock declarado | `L` | `M` sem Relentless | Redução nominal em relação a `40` |
|---|---:|---:|---:|
| Sem encantamento | 0 | 40 ticks (2,00 s) | 0% |
| I | 1 | 32 ticks (1,60 s) | 20% |
| II | 2 | 24 ticks (1,20 s) | 40% |
| III | 3 | 16 ticks (0,80 s) | 60% |

**Prioridade:** se `R>0` for forçado numa stack com Dark Nock, o helper escolhe **5** antes de consultar `L`. Além disso, o fluxo normal de `releaseUsing` exige `R<=0`; o ramo Relentless dispara em `onUseTick` com regras diferentes. A exclusividade declarativa normalmente desestimula essa combinação, mas **não** substitui guarda de runtime em dados inválidos.

**Domínio:** o helper **não limita `L`** a 0–3. Em níveis artificialmente elevados pode devolver zero ou número negativo (por exemplo, `L=5` produz `M=0` sem Relentless), o que compromete a divisão de carga dos helpers. Não interpretar níveis inválidos como tiers de perk seguros, nem afirmar crash físico sem teste.

## 4. Consumo indireto por carga e potência

O `DreadbowItem` usa o mesmo `M` em dois domínios **distintos**:

1. **Carga/visual:** `acInventoryTick(ItemStack,Level,Entity,boolean)V`, chamado pela superfície `ACTickingItem`/`ItemStackTickMixin` e descrito na ficha do equipamento, só escreve os contadores `UseTime` e `PrevUseTime` no ramo cliente (`level.isClientSide()`). Normalmente `UseTime` cresce **1 por callback elegível** enquanto `UseTime<M`; o incremento 3 de Relentless é separado. `getPullingAmount(ItemStack,float)F` produz `min(getLerpedUseTime(stack,partial)/M,1F)` para apresentação. Não é confirmação de carga servidor.
2. **Potência usada no release:** `releaseUsing(ItemStack,Level,LivingEntity,int)V` calcula o tempo de uso a partir dos **argumentos vanilla**: `t = getUseDuration(stack) − remainingUseTicks`, com `getUseDuration=72000`. Em seguida chama `getPowerForTime(t,stack)`, que usa `M`: `x=t/M` e `p=min((x²+2x)/3,1)` para `p>1`. Não há clamp inferior geral. O número `72000` é limite da animação/uso, **não** carga exigida para disparar.

O ramo normal exige `p>0.1D` (comparação em double depois de calcular `p` float). No domínio comum de tempo `t` inteiro, não negativo, `R=0` e `L∈[0,3]`, o primeiro `t` nominal que satisfaz esse gate é:

| `L` | `M` | Primeiro `t` com `p>0,1` | `t` para `p=1` |
|---:|---:|---:|---:|
| 0 | 40 | 6 ticks | 40 ticks |
| I | 32 | 5 ticks | 32 ticks |
| II | 24 | 4 ticks | 24 ticks |
| III | 16 | 3 ticks | 16 ticks |

Essa é uma **consequência aritmética** da fórmula/gate estático com os níveis declarados, **não** medição de cliente, latência de callback, quantidade de tiros físicos ou condição de acesso aos recursos. O gatilho de início de uso ainda depende de jogador criativo **ou de munição válida**.

**Sem efeito direto na janela de Perfect Shot:** `TWILIGHT_PERFECTION` define seu bônus de `PerfectShotTicks` e exige seu próprio nível/contador para aplicar o multiplicador; a redução de `M` pode antecipar o momento do limiar no contador cliente, mas **Dark Nock não concede automaticamente `Perfect Shot`, nem cria contador server-owned**.

## 5. Relação com mira, projeção, dano e custo da arma

O `p` alimenta outros métodos do disparo normal, já documentados no [contrato SHA-exato do Dreadbow](../equipment/dreadbow.md). **Consequência:** comparar dois arcos com `t` idêntico pode revelar parâmetros distintos porque `M` mudou. Isso não significa que Dark Nock tenha introduzido novos efeitos por nível.

| Eixo solicitado para desenho de perks | Contrato compartilhado da arma | O que Dark Nock realmente altera |
|---|---|---|
| **Alcance da busca de alvo** | No release, `ProjectileUtil.getHitResultOnViewVector` recebe `128F×p`; se `MISS`, refaz com `42F×p`; `getDefaultProjectileRange()=64` é metadado distinto | **Indiretamente**, `p` cresce com menos `t`. Não cria targeting alternativo, um cap novo ou range fixo |
| **Quantidade de flechas** | Salva normal solicita `ceil(30F×p)` iterações se a munição é conversível; `ceil(8F×p)` caso contrário | **Indiretamente**, antecipa a potência de que depende essa contagem; não garante entidades aceitas/hits |
| **Área/espalhamento** | Posição inicial candidata dentro de caixa `16×4×16` em torno do centro elevado; direção para o ponto visado | Nenhum multiplicador independente de área, geometria ou dispersão por `L` |
| **Velocidade** | Para o lançamento sombrio normal, speed nominal `0.5F + 1.5F×randomFloat()`, intervalo `[0,5,2)` | Sem multiplicador de velocidade por `L` no ramo documentado |
| **Dimensão de projétil** | `DarkArrowEntity` tem dimensão de entidade registrada `1.1F×0.5F`; colisão herdada | Sem alteração de tamanho/hitbox/raio por `L` |
| **Dano e tipo** | Conversão usa `alexscaves:dark_arrow`, com `shadowArrowDamage` solicitado de `3F` ou `2F` quando `PRECISE_VOLLEY`, podendo dobrar com Perfect Shot | Não modifica dano solicitado por nível; antecipar disparo não é buff direto de dano |
| **Consumo** | Fora criativo, caminho normal pode pedir `1` durabilidade do arco e `1` de munição por salva, sujeito a `SHADED_RESPITE` e regras da munição | Não reduz custo nem transforma múltiplas flechas em múltiplas cobranças |
| **Tempo / duração** | `M` afeta potência/carga; depois do lançamento, `DarkArrowEntity.tick()` controla fading e colisão | **Aqui está o efeito direto**: `M=40−8L`; não muda lifetime dos projéteis |
| **Modo contínuo** | `RELENTLESS_DARKNESS` habilita `onUseTick` com condição `remainingUseTicks % 3 == 0`, spawn/velocidades diferentes | Dark Nock não atua como cooldown desse modo; combinação não é suportada pelos dados normais |

**Limites de targeting:** o Dreadbow mira pelo resultado de raycast e segue regras delegadas à engine; Dark Nock não cria busca de entidades em área, lock-on persistente, alteração de categoria de alvo ou escolha de aliado/inimigo. A resolução de hits e o dano solicitado pertencem ao `DarkArrowEntity`, ao tipo de dano, à factory das flechas e ao motor. Mudanças em PvP, permissões, imunidades, proteção e atributos requerem boundary real; números de pedido não equivalem a efeitos aceitos.

**Limites de quantidade:** `ceil(30p)`/`ceil(8p)` contam **tentativas de spawn**, não munição consumida por flecha, entidades inseridas, vítimas atingidas ou eventos de Mastery. O retorno de `Level.addFreshEntity` é descartado no loop da arma segundo a ficha existente; não deduzir sucesso de cada tentativa.

## 6. Orientações de implementação de perks e autoridade

**Regra de contrato:** o item nativo `DreadbowItem` decide `M`, a potência, a elegibilidade de disparo, a munição, a mira, as solicitações de spawn e os débitos. `DarkArrowEntity` processa colisão/dano. Black Arcana é autoridade de **seu próprio casting/runtime**, e RPG Skill Tree fornece perks, atributos, Mastery e gates somente por **bridge real e limitada**.

| Proposta de perk | Situação / condição obrigatória |
|---|---|
| Reduzir tempo de carga | **⛔ bloqueado:** não há `mutating_hook` verificado para sobrescrever `M`, `UseTime` ou calcular potência do provider no servidor |
| Aumentar alcance ou número de flechas | **⛔ bloqueado:** esses valores são derivados de `p` e sujeitos a limites de spawn/target; é necessário seam server-authoritative e orçamento de entidades |
| Converter alvo para área / homing / mudar flecha | **⛔ bloqueado:** não é mecanismo de Dark Nock; exigiria outra integração comprovada, evitando projéteis e pipelines duplicados |
| Alterar dano, tamanho, velocidade ou duração | **⛔ bloqueado:** não há conexão direta segura de `L` a esses campos, nem API mutadora certificada |
| Conceder Mastery por disparo/impacto | **⛔ bloqueado:** sem prova de origem/settlement, dedupe e lançamento aceito, contar tentativas ou callbacks arrisca XP duplicado |
| Usar atributo somente de leitura em UX/progressão | **⚠️ condicionado:** números de `M` são documentáveis como metadados; a leitura no cliente não é validação de autoridade ou ativação real |

**Risco adicional de sincronização:** a carga visual e `PerfectShotTicks` têm caminho de atualização de tags do cliente para o servidor no item; a ficha-base documenta que esse fluxo não prova reconstrução/validação server-side do contador. Não tratar `UseTime`/`PerfectShotTicks` recebidos como autorização para perks de perfect shot nem espelhar o protocolo sem contrato próprio.

**QA pendente:** gatilhos nos níveis 0/I/II/III e diferença entre 3/4/5/6 ticks; flechas normais e modificadas; comportamento no cliente vs dedicado; efeitos de Relentless em stacks forçadas, níveis inválidos, combinações de encantamentos e datapacks; limites reais de busca/shot count, aceitação de spawn, custo e desgaste; situações sem munição, Perfect Shot com latência, perda/reload da stack, PvP/claims e dedupe de Mastery. Nenhuma dessas observações foi promovida a `PASS`.

## 7. Certificação causal individual — reprodução do JAR 1.0.10

**Selo canônico:** [EXACT-DARK-NOCK-CAUSAL-1.0.10.json](../EXACT-DARK-NOCK-CAUSAL-1.0.10.json). A [sonda SHA-exata](../../../../../docs/qa/alexscaves_1010_dark_nock_causal_probe.py), seus [7 testes de regressão](../../../../../docs/qa/alexscaves_1010_dark_nock_causal_probe_test.py) e o [workflow CI dedicado](../../../../../.github/workflows/alexscaves-1010-dark-nock-causal.yml) verificam, no publisher instalado, a igualdade do JAR (SHA-1, SHA-256, tamanho), os SHA-256 de todos os classfiles do manifesto Dreadbow, a identidade dos JSONs e tags, a presença dos dois owners diretos de `DARK_NOCK`, as janelas JVM originais e as instruções/arestas diretas dos consumidores. O snapshot ainda exige que o **relatório completo regenerado** tenha SHA-256 `f19e0377f1388f81f34aea4514800d3be4a602ae07ad46dba4e8d47579f55f28`. A execução inicial de descoberta no GitHub Actions confirmou esse relatório; certificação final exige também execução com `--seal`.

**Cobertura delimitada:** os classfiles com token binário `DARK_NOCK` são somente `ACEnchantmentRegistry` e `DreadbowItem` no JAR examinado. O primeiro registra identidade; o segundo consome nível e carga. Foram reconciliados **13 métodos nativos de DreadbowItem, 938 instruções JVM parseadas e 99 branches diretos com destino válido**; não são 13 magias ou casts, nem uma prova global de ausência de consumidores indiretos. O manifesto pai SHA-256 `88cf1e305688ed82cd08559ec9bcb35bc1745116be88ffc435593184e8e07e89` mantém as dependências de Dreadbow e Dark Arrow, sem duplicá-las.

| Eixo do contrato | Resultado da prova estática | Limite conservado |
|---|---|---|
| Identidade | JAR e `dark_nock.json` SHA-exatos; `max_level=3` e tag `#alexscaves:enchantable/dreadbow` | Config/datapack ativo não aferido |
| Comportamento e condições | Ramo Relentless sobrepõe o seletor, caso contrário `M=40−8L`; `releaseUsing` consome `getPowerForTime` e gate `p>0,1` | Níveis inválidos podem causar denominador não positivo |
| Parâmetros | `40/32/24/16` ticks e primeiros limiares nominais `6/5/4/3`, junto da aritmética visual/servidor e ramo de disparo existentes | Sem aumento direto de dano, raio, hitbox ou multiplicador de velocidade |
| Targeting | `ProjectileUtil`, factories, arco e flecha no ramo de release nativo, sem novo alvo associado a Dark Nock | Aceitação efetiva de entidades, PvP/claims e engine desconhecidos |
| Custos | Encantamento `1/11/21` a `41/51/61`, bigorna `4`; débitos de uso e munição pertencem ao Dreadbow | Não representa novo custo de mana ou desconto de durabilidade |
| Integração | Alterações possíveis de UX/atributos somente como proposta; nenhum hook seguro provado para alterar `M` ou o release | `NO_MUTATION`, sem Mastery/perk mutador |
| Validação | Selo SHA-exato, censo JVM completo dos métodos delimitados, testes fail-closed, CI de leitura do JAR | `physical_qa=NOT_TESTED`, sincronização de tags não homologada |

**Comando reprodutível:** `python3 docs/qa/alexscaves_1010_dark_nock_causal_probe.py --jar <publisher-1.0.10.jar> --javap <jdk21>/bin/javap --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-DREADBOW-CONTRACTS-1.0.10.json' --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-DARK-NOCK-CAUSAL-1.0.10.json' --output <relatorio.json>`. A sonda compara os dados com o selo sem executar o mod. O resultado do relatório verifica o **contrato técnico estático**, não execução física ou permissão para mutar o provider.

**Fechamento:** `resource_and_native_JVM_evidence=SHA_EXACT`; `individual_full_certification=STATIC_TECHNICAL_CATALOG_ONLY`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `NO_MUTATION`. Dark Nock conta como **um contrato estático individual**, mas não encerra o provider, não certifica hook nem acrescenta nova raiz mágica.

**Próxima identidade alfabética:** `alexscaves:dazing_sweep`.
