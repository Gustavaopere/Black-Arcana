# Soak Seeking — rastreamento dos Water Bolts do Sea Staff (Alex's Caves Continued 1.0.10)

**Estado do objeto:** ✅ contrato técnico **estático individual**, limitado ao JAR publisher SHA-exato 1.0.10, à aquisição declarada e aos consumidores nativos comprovados. **Integração mutadora:** `NOT_VERIFIED` · **QA física:** `NOT_TESTED` · **política:** `NO_MUTATION` / `fail-closed`. O encantamento modifica a ação [Sea Staff — Water Bolt](../actions/sea-staff-water-bolt.md), **não** cria um segundo cast ou uma nova raiz semântica.

## 1. Identidade, tradução e proveniência

| Campo | Contrato |
|---|---|
| Provider | Alex's Caves Continued · mod ID `alexscaves` |
| Ambiente | Minecraft **1.21.1**, **NeoForge**, **Java 21** |
| JAR exato | `alexscaves-1.0.10-neoforge+1.21.1.jar` · **75.279.314 bytes** |
| SHA-1 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| SHA-256 | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Identidade | `alexscaves:soak_seeking` · `ACEnchantmentRegistry.SOAK_SEEKING` |
| Recurso | `data/alexscaves/enchantment/soak_seeking.json`; **362 bytes**, SHA-256 `cfec967d084e9dc3870b90bc05d62375524af447ae280aa7fea63458e644b66b` |
| Tag | `data/alexscaves/tags/item/enchantable/sea_staff.json`; **49 bytes**, SHA-256 `22e45ab74b71d7152ccc531a633e5149df9c12eece40464c85c50f5a600fd80e` |
| Texto publisher `en_us` | Nome “Soak Seeking”; a descrição informa que os Water Bolts do Sea Staff seguem alvos com maior precisão |
| Locale `pt_br` | Sem chaves próprias de Soak Seeking no JSON auditado; a descrição em português acima é **paráfrase técnica**, não tradução oficial do provider |

A [sonda read-only](../../../../../docs/qa/alexscaves_1010_soak_seeking_static_probe.py) comparou o publisher com os hashes físicos usados na [auditoria 1.0.10](../EXACT-1.0.10-ARTIFACT-AUDIT.md) e com o [contrato SHA-exato de Sea Staff](../EXACT-TECHNICAL-CONTRACTS-1.0.10.json). O [manifesto individual](../EXACT-SOAK-SEEKING-STATIC-1.0.10.json) registra recursos, traduções, classes, quatro métodos e instruções JVM delimitadas. A árvore pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara versão 1.1.1 e **não** foi usada como autoridade numérica da versão 1.0.10.

## 2. Aquisição e parâmetros do encantamento

| Campo do JSON publisher | Valor / interpretação |
|---|---|
| `description.translate` | `enchantment.alexscaves.soak_seeking` |
| `supported_items` | `#alexscaves:enchantable/sea_staff` → `alexscaves:sea_staff` |
| `weight` | **10**: peso declarativo de encantamento, não velocidade do projétil |
| `max_level` | **3** (I–III) |
| `min_cost` | `base=1`, `per_level_above_first=5`; expressão declarativa **1 + 5(L−1)** |
| `max_cost` | `base=41`, `per_level_above_first=10`; expressão declarativa **41 + 10(L−1)** |
| `anvil_cost` | **1**: custo de bigorna configurado pelo recurso |
| `slots` | `[mainhand]` no dado de aquisição |
| `exclusive_set` | **N/A no recurso**: chave ausente, o que não comprova compatibilidade irrestrita em datapacks |
| Recursos `mana`, `stamina`, `charges` próprios | **N/A no produtor/consumidor auditados**; os custos do encantamento acima não são custo de uso |

As tags efetivas de enchanting, loot e trade no mundo carregado não foram verificadas; o JSON e a tag não provam aquisição efetiva em uma instância de jogo com datapacks. Nenhum custo por nível ou por tick de Soak Seeking aparece como cobrança independente no caminho auditado.

## 3. Gatilho e grafo causal exato

O usuário ativa a ação raiz `alexscaves:sea_staff` por `SeaStaffItem.use(Level, Player, InteractionHand)`. O método lê `ACEnchantmentRegistry.SOAK_SEEKING` da `ItemStack` por `ACCompat.enchantLevel` em **@63–72**, converte o inteiro para `float` e armazena o nível para o disparo. No trecho servidor de criação de cada Water Bolt, **@314–324** atribui `WaterBoltEntity.seekAmount`; `@327–339` solicita a UUID do alvo adquirido e `@342–348` chama `Level.addFreshEntity`, descartando o valor booleano de retorno. Portanto **solicitação de spawn não é garantia de spawn aceito**.

O censo estático do arquivo exato examinou **1.555 classfiles** e encontrou o token binário direto `SOAK_SEEKING` somente em `ACEnchantmentRegistry.class` e `SeaStaffItem.class`. A busca de token não exclui acesso reflexivo, datapacks, mixins ou consumidores de terceiros; o consumo efetivo do parâmetro ocorre em `WaterBoltEntity.tick()`, que lê o campo `seekAmount`, sem precisar mencionar o símbolo do encantamento.

A cadeia de classes/métodos verificada usa o prefixo `com/github/alexmodguy/alexscaves/`:

| Método | Instruções JVM | SHA-256 do método compilado | Âncoras anteriores confrontadas |
|---|---:|---|---:|
| `server/item/SeaStaffItem.use` | 189 | `fc071fd36310ddb6a082d46113930b78fa89d1f0b4a1a9bfc749d2bd11c1ba7c` | 18 |
| `server/entity/item/WaterBoltEntity.tick` | 362 | `1739f6c4c86a4e1d753243ed087cfdc3033e6bf2c90bafc2ed7771c0195d5082` | 11 |
| `WaterBoltEntity.onRicochetHit` | 122 | `5b9bcc73dc65afc1e728f864f733cb297af322e6bba32bc1f9988a19a7ac3fad` | 7 |
| `WaterBoltEntity.damageMobs` | 105 | `5a74cbf8fa1793ffeb6f0107be742e82cf2035d27f96f238e0a672ce005e653d` | 7 |

Foram verificadas **43 âncoras** pré-existentes no conjunto; hash de método e âncora cobrem exatamente o compilado observado, mas **não** são um hook mutador público.

## 4. Fórmula e condições de homing

No produtor, o cálculo de cada projétil principal é:

`seekAmount = 0.3F + 0.2F * (float)enchantLevel(stack, SOAK_SEEKING)` (`SeaStaffItem.use @314–324`).

| Nível publicado | `seekAmount` nominal | Fator nominal da velocidade anterior `1−(seekAmount−0.3)*0.3` |
|---|---:|---:|
| Sem encantamento (0) | 0,3 | 1,00 |
| I | 0,5 | 0,94 |
| II | 0,7 | 0,88 |
| III | 0,9 | 0,82 |

Os valores da tabela são representações decimais nominais: as operações no JAR usam `float` e podem produzir diferenças de arredondamento. A correção completa em `WaterBoltEntity.tick @92–155` é, em forma vetorial:

`v_novo = v_atual * (1F − (seekAmount − 0.3F) * 0.3F) + normalize(pos_alvo + 0.85F * altura_alvo − pos_projétil) * seekAmount`.

Isso **não** garante velocidade final `seekAmount` blocos/tick nem dano, alcance ou tamanho de projétil proporcionais ao nível. A contribuição vetorial para o alvo e o resíduo da velocidade anterior interagem direcionalmente.

O homing no `tick()` exige simultaneamente:
1. processamento no servidor e `getArcingTowards()` resolvendo alvo;
2. `tickCount > 3` **ou** `(double)seekAmount > 0.3D`;
3. `dieIn == -1` e distância ao alvo `>1.5F`;
4. `tickCount < 20` **ou** (`(double)seekAmount > 0.3D` e `tickCount < 40`).

**Precisão de ponto flutuante relevante para perks:** mesmo o literal de inicialização `0.3F`, quando convertido a `double`, é aproximadamente `0.30000001192092896D`, maior que `0.3D` no bytecode. Portanto as duas comparações com `0.3D` **também podem ser verdadeiras para o baseline sem encantamento**. Não converter os gates em “Soak Seeking desbloqueia homing antes do tick 4 e até o tick 39” sem essa ressalva. Os limites de tick são janelas de **correção de trajetória**, não duração garantida do projétil nem cooldown.

## 5. Alvo, trajetória, efeitos e custos compartilhados

A ação original do Sea Staff busca uma entidade por `getClosestLookingAtEntityFor` usando argumento `128D` e critérios de clip/seleção descritos na [ficha da ação](../actions/sea-staff-water-bolt.md). Esse argumento é uma distância de consulta, **não** alcance físico máximo do Water Bolt nem raio circular AOE. O produtor salva UUID de alvo no novo projétil; o `tick()` consulta o alvo novamente no servidor. O encantamento **não introduz por si só** seleção alternativa de alvos, passagem através de blocos ou bypass de PvP/claims.

A ação normal solicita velocidade inicial `2F` para o bolt central (`1F` para bolts laterais de Triple Splash), imprecisão `12F`, e usa movimentação, gravity e colisões nativas. A resolução de `damageMobs()` solicita **3F de dano** com fonte `mobProjectile(this, owner LivingEntity ou null)`, filtrando owner, aliados e Deep Ones na AABB do projétil inflada em **2D por eixo**. Esses são valores **compartilhados com a ação Sea Staff**: Soak Seeking não altera diretamente esse literal de dano ou raio de impacto; `ACCompat.hurt` e eventos de impacto ainda condicionam o resultado aplicado. Enveloping Bubble controla o ramo de status Bubbling; Bouncing Bolt controla o ramo de ricochete; não imputá-los como efeitos próprios de Soak Seeking.

`SeaStaffItem.use @366–381` solicita **1 ponto de durabilidade por uso**, exceto com `instabuild`, pela API wrapper `ACCompat.hurtAndBreak`. Não há cobrança de mana, cooldown individual de Soak Seeking nem custo de durabilidade adicional proporcional a `L` nesse método. A ausência de chamada direta de cooldown não comprova ausência de mudanças por engine, configuração ou outros mods.

**Ricochete:** `WaterBoltEntity.onRicochetHit` cria um bolt secundário com seu valor default de `seekAmount=0.3F` e não copia o nível da stack nem o campo de homing do bolt pai no corpo certificado. Assim, não presumir que Soak Seeking potencializa o segundo bolt gerado por Bouncing Bolt. O filho pode copiar outras propriedades (como Bubbling), que não tornam o efeito de homing herdado.

## 6. Autoria, persistência e clientes

A ação define owner do projétil e UUID inicial do alvo nativamente. Nos overrides próprios `readAdditionalSaveData` e `addAdditionalSaveData` do `WaterBoltEntity`, a prova base aponta serialização de `Bubbling`, **não** de `seekAmount`, UUID do alvo, `dieIn` ou `ricochet`. Não prometer continuidade fiel do homing após save/reload, unload, reconexão ou troca de dimensão. O efeito numérico se estabelece na criação do bolt; **não** há leitura continuada do nível da stack no `tick()` auditado.

A leitura do encantamento acontece no uso, enquanto a atualização do alvo no `tick()` é **server-side**. Esse recorte estático não homologa HUD, predição cliente, multiplayer, integridade da origem do cast, aceitação final da entidade pelo mundo ou comportamento com datapacks que forcem níveis fora de 0–III.

## 7. Matriz de integração com perks, atributos e Mastery

| Superfície | Possível contrato de design | Limite técnico real |
|---|---|---|
| `seekAmount` | Escalonar correção de trajetória após criar o bolt | Campo e consumer internos; **nenhuma API mutadora segura certificada** |
| Janela de homing | Condicionar ticks 3/20/40 e término `dieIn` | Não reinterpretar `0.3F > 0.3D` como teste de presença do enchant |
| Precisão e velocidade | Alterar vetor/targeting na origem apenas mediante boundary real | Velocidade inicial, direção e seek são parâmetros diferentes |
| Alvo e alcance | Melhorar seleção sob validação servidor, PvP/claims e LoS | `128D` é argumento de consulta; **não** conceder range fictício |
| Dano e AOE | Nenhum modificador de dano/raio provado em Soak Seeking | `3F` e `2D` pertencem ao Sea Staff/Water Bolt |
| Ricochete | Considerar transmissão explícita para bolt filho em design futuro | Código atual **não** herda `seekAmount` |
| Durabilidade e custo | Ajustar gastos somente em operação transacional autorizada | `1` ponto por uso é pedido do Sea Staff, não débito extra do enchant |
| Mastery/XP | Creditar somente a raiz do cast e resultados aceitos, com deduplicação | Não contar ticks, projéteis, colisões e ricochetes como casts independentes |

**Autoridade:** Black Arcana mantém seu runtime mágico; RPG Skill Tree pode fornecer progressão e perks apenas atrás de boundary comprovado, sem roubar a autoridade de Alex's Caves no movimento/dano nativo. Na ausência de hook mutador seguro: **`NO_MUTATION` e `fail-closed`**.

## 8. Validação, reprodução e pendências

1. A sonda executa `sha_file` no JAR exato, lê JSONs e locais, pesquisa o símbolo direto em **1.555 classfiles**, confere classes SHA-256 e todas as **43 âncoras** anteriores dos quatro métodos; gera somente janelas JVM limitadas.
2. O manifesto [`EXACT-SOAK-SEEKING-STATIC-1.0.10.json`](../EXACT-SOAK-SEEKING-STATIC-1.0.10.json) fixa o relatório individual. Reproduzir com Java 21: `python3 docs/qa/alexscaves_1010_soak_seeking_static_probe.py --jar /caminho/publisher.jar --javap javap --seal wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SOAK-SEEKING-STATIC-1.0.10.json`.
3. Os [testes sintéticos](../../../../../docs/qa/alexscaves_1010_soak_seeking_static_probe_test.py) exercitam deriva de opcode, offset, operando, descriptor, âncora ausente, método vazio e limite de extração; a [CI individual](../../../../../.github/workflows/alexscaves-1010-soak-seeking-static.yml) baixa o JAR publisher e refaz o selo e os índices.
4. A prova de `WaterBoltEntity.damageMobs` e o resto do ciclo causal estão no [contrato base](../EXACT-TECHNICAL-CONTRACTS-1.0.10.json) e na [ficha Sea Staff](../actions/sea-staff-water-bolt.md). A certificação individual de Soak Seeking **não** transfere certificação a Triple Splash, Bouncing Bolt ou outros encantamentos.

**Não verificado / fora do escopo:** hook mutador, gameplay real/QA física, aceitação efetiva de dano/spawn, disponibilidade de alvo após unload/reload, datapacks e config ativa, PvP/claims, limites herdados da engine, modlist futura e universo integral do provider. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `provider_closed=false`, `NO_MUTATION`.

**Estado da certificação:** contrato técnico estático individual concluído após validação SHA-exata e CI, sem representar autorização de integração de perks ou fechamento global do provider.
