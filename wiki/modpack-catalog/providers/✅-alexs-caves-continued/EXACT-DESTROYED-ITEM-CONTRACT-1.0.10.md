# ACDestroyedItem 1.0.10 — contrato nativo, registro e ponte NeoForge delimitada

```text
claim_scope=STATIC_TECHNICAL_CATALOG_ONLY
evidence_grade=SHA_EXACT_BINARY_BEHAVIOR
static_technical_contract=CERTIFIED_STATIC_7_AXES
mutating_hook=NOT_VERIFIED
physical_qa=NOT_TESTED
perk_certification=NOT_CERTIFIED
mutation=NO_MUTATION
provider_universe_closed=false
```

A [ficha de destruição de itens](systems/destroyed-item.md) conclui os sete eixos estáticos da interface e de seu único implementador no publisher 1.0.10. O [selo nativo](EXACT-DESTROYED-ITEM-CONTRACT-1.0.10.json) documenta o corpo completo, os guardas, os parâmetros e a seleção real do item no registry. A [referência NeoForge 21.1.250](EXACT-DESTROYED-ITEM-ENGINE-REFERENCE-21.1.250.json) prova separadamente a ponte de interfaces e os patches oficiais pertinentes; não transforma uma inspeção de artefatos em execução física do modpack.

A [ficha histórica da PR #1115](systems/EXACT-DESTROYED-ITEM-HISTORICAL-CARD-1.0.10.md) permanece byte a byte: **9.143 bytes**, SHA-256 `80e185f57698f54181bf49bf11998fb67499f158d8c9ec50d3aee01fbb2bec9d`. Seus estados parciais pertencem àquele checkpoint. O [probe de descoberta](../../../../docs/qa/alexscaves_1010_destroyed_item_probe.py) e seu [workflow](../../../../.github/workflows/alexscaves-1010-destroyed-item-probe.yml) não foram reclassificados nem reescritos. Esta entrega acrescenta um selo de contrato, sem criar outra ficha candidata ou raiz mágica.

## Identidade e versões

| Campo | Evidência exata |
|---|---|
| Artefato publisher | `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto 1645389 / arquivo 8856293 |
| Plataforma declarada | Minecraft 1.21.1, NeoForge, Java 21 |
| JAR | 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| JAR SHA-256 | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Interface | `com/github/alexmodguy/alexscaves/server/item/ACDestroyedItem` |
| Interface SHA-256 | `2ccc084cf825941414561ed02362fc3776b5ddddd699c8c62952818956771100` |
| Implementador | `com/github/alexmodguy/alexscaves/server/item/RadioactiveOnDestroyedBlockItem` |
| Implementador SHA-256 | `853e1f6318cfaa2c97ab27955e6b068e4e5f34ab94f4354092233e69bc502f24` |
| Assinatura própria | `onDestroyed(ItemEntity,DamageSource):void` |
| Descritor JVM | `(Lnet/minecraft/world/entity/item/ItemEntity;Lnet/minecraft/world/damagesource/DamageSource;)V` |
| Corpo do implementador | 170 bytes de `Code`, SHA-256 `34f73b931946ae63544f4cbe9e35d1bd10fcab90f25b000bbdc54b98bc8b8881` |
| Censo publisher | 1.555 classes, um implementador direto/concreto, nenhum implementador herdado adicional |

A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e permanece adjacente. Não fornece os valores 1.0.10 desta conclusão. Os artefatos NeoForge têm sua própria identidade e grau de evidência: o ledger físico registra **21.1.250**, enquanto `gradle.properties` usa **21.1.248** para desenvolvimento. A prova principal da ponte usa a versão 21.1.250 oficial; a comparação limitada com 21.1.248 não certifica equivalência integral dessas versões.

## Censo, declaração e recebedor

`ACDestroyedItem` é uma interface pública abstrata com um método, sem corpo de implementação. As únicas referências tipadas ao alvo no publisher são a declaração e `RadioactiveOnDestroyedBlockItem`. O grafo nativo não acrescenta subclasses implementadoras. A existência de uma interface não fornece, isoladamente, um dispatcher, um evento ou uma autorização de perk.

O censo global de nomes/descritivos distingue três declarações `onDestroyed`: a interface de dois argumentos, o implementador de dois argumentos e o método de um argumento em `com/github/alexmodguy/alexscaves/citadel/item/BlockItemWithSupplier`. A referência nativa de chamada ao nome é o `invokespecial` do implementador para `RadioactiveBlockItem.onDestroyed(ItemEntity,DamageSource)`. O owner simbólico não declara esse overload em sua própria classe. Não se confunde uma chamada à superclasse com uma chamada à interface ou com prova de despacho do engine.

O [selo de referência](EXACT-DESTROYED-ITEM-ENGINE-REFERENCE-21.1.250.json) fecha a boundary estática pertinente com artefatos oficiais, sem exigir reconstruir todo o jogo:

| Etapa | Evidência delimitada |
|---|---|
| `Item` e `ItemStack` | Patches de userdev acrescentam as interfaces de extensão correspondentes |
| Destruição em `ItemEntity` | Patch oficial encaminha a destruição para o overload de `ItemStack` com `ItemEntity` e `DamageSource`, antes do descarte posterior |
| `IItemStackExtension.onDestroyed` | Corpo no universal obtém `getItem()` e chama virtualmente o overload de dois argumentos do item |
| Resolução do implementador | O item concreto pode fornecer o override de dois argumentos; no ramo deste contrato, é `RadioactiveOnDestroyedBlockItem` |
| Superchamada do override | Na hierarquia padrão descrita abaixo, a referência à superclasse pode alcançar o default herdado de `IItemExtension`, que encaminha para `Item.onDestroyed(ItemEntity)` de um argumento |
| Overload publisher de um argumento | `BlockItemWithSupplier` trata o caso `ShulkerBoxBlock` e encaminha conteúdo de container; não contém `discard()` nesse corpo |

Os dois defaults são bytecode oficial universal. As declarações adicionais e a alteração de callsite são **patches oficiais**, sem alegação de que o patch, sozinho, seja o classfile final instalado. A inspeção auxiliar de um JAR derivado no cache de compilação não é promovida a distribuição física nem se torna entrada obrigatória da CI. Fonte patch, bytecode universal, classe derivada de desenvolvimento e runtime transformado mantêm autoridades distintas.

A ligação externa `BlockItem → Item` e a ausência de overload interveniente não são demonstradas pelos três trechos oficiais 21.1.250 selecionados. A hierarquia completa foi observada apenas na referência derivada 21.1.248; não se promove essa observação a binário físico 21.1.250. A resolução da superchamada permanece uma derivação condicional à hierarquia padrão e à ausência de transformações/overrides adicionais.

Isso identifica uma ponte versionada plausível pela resolução normal dos símbolos e dos patches, sem garantir execução real em todos os caminhos de dano. Regras completas de `ItemEntity.hurt`, hooks adicionais, cancelamento, transformação de classes, proteção territorial e aceitação de efeitos permanecem fora desta certificação física. Todo o sufixo próprio descrito abaixo depende de a superchamada retornar normalmente.

## Registro correto e não consumidores

A registry pertinente é **`ACBlockRegistry`**, não `ACItemRegistry`. O helper `getBlockSupplier` escolhe factories por seletor, cujo binding de bootstrap e corpo lambda são selados:

| Seletor | Factory / bootstrap | Item produzido | Papel neste contrato |
|---|---|---|---|
| `4` | `lambda$getBlockSupplier$440` / bootstrap 7 | `RadioactiveBlockItem` | Não fornece o override destruído deste contrato |
| `5` | `lambda$getBlockSupplier$441` / bootstrap 8 | `RadioactiveOnDestroyedBlockItem` | Implementador de `ACDestroyedItem` |

O único registro publisher encontrado com seletor **5** é **`WASTE_DRUM` / `alexscaves:waste_drum`**, com o seletor em `@2200`. As entradas `radrock_uranium_ore`, `block_of_uranium` e `unrefined_waste` usam o seletor **4**. Elas são controles negativos importantes: compartilhar radioatividade de inventário não lhes atribui automaticamente a destruição com nuvem/explosão.

O valor **0.01F** do construtor pertence ao campo de chance de radiação de inventário no parent. O corpo `onDestroyed` não consulta esse campo nem faz o sorteio de 1%; essa chance não limita a explosão. Classificação do registry e parâmetro do parent são fluxos separados. Um registro de item não comprova aquisição, equipamento, destruição em Survival ou entrega do callback.

## Ordem causal, parâmetros e resultados solicitados

| Ordem do corpo próprio | Contrato nativo |
|---|---|
| `@0–3` | Chama o overload da superclasse antes de todos os guardas próprios |
| `@6–10` | `DamageSource.isCreativePlayer()` verdadeiro desvia para o retorno `@169` |
| `@13–17` | `ItemEntity.isRemoved()` verdadeiro também desvia para o retorno |
| `@20–21` | Solicita `ItemEntity.discard()` |
| `@24–135` | Cria e configura `AreaEffectCloud` no mundo e posição do item e chama `addFreshEntity` |
| `@138` | Descarta o booleano retornado pelo pedido de inserção |
| `@139–165` | Solicita `Level.explode`, independentemente daquele booleano |
| `@169` | Retorna sem recibo próprio de spawn, dano, efeito ou explosão aceita |

Há dois guardas próprios, ambos posteriores à superchamada. Eles não estabelecem autorização de PvP/claims nem um guard completo de lado servidor. O callback não consulta `isClientSide` nesse corpo. Lado, elegibilidade e execução do chamador não se inferem do nome da interface.

| Parâmetro solicitado | Valor e unidade | Boundary |
|---|---|---|
| Partícula | `GAMMAROACH` | Apresentação, sem tipo de dano associado por analogia |
| Cor da nuvem | `7853582` / `0x77D60E` | Valor visual passado ao helper |
| Efeito carregado | `IRRADIATED`, duração **9600 ticks**, amplifier **1** | Payload da nuvem, não duração efetiva garantida em cada vítima |
| Raio inicial da nuvem | **2.0F** | Distinto da potência da explosão e de sua área efetiva |
| Duração da nuvem | **12000 ticks** | Distinta da duração do payload de status |
| Espera da nuvem | **0 ticks** | Não elimina delays, filtros ou reaplicação próprios do engine |
| Variação de raio | `-getRadius()/getDuration()` após os setters | Aritmética nominal `-2/12000`, sem simulação de lifetime físico |
| Explosão | Fonte explícita **null**, posição `(x,y+0.5,z)`, potência **1.8F**, `ExplosionInteraction.BLOCK` | Pedido potencialmente destrutivo, sem dano líquido, blocos quebrados ou autorização garantidos |

Não há setter de owner da nuvem no corpo. O `DamageSource` recebido não é convertido em dono da explosão ou beneficiário de perk; ele é encaminhado ao super e consultado para Creative. Ausência de owner explícito, fonte null e origem do dano são fatos diferentes. Kill credit, XP, Mastery, loot e deduplicação executável continuam sem homologação.

[Irradiated](effects/irradiated.md) e [Radiation](damage-types/radiation.md) conservam seus contratos de consumo e fonte periódica. O registro do status na nuvem não é uma chamada direta de hurt. A engine decide seleção de entidades, reaplicação, duração aplicada, efeito instantâneo/periódico, persistência e remoção; não se empresta a este callback a homologação integral desses mecanismos.

Custos próprios de mana, stamina, souls, munição, cooldown de casting, cast time, velocidade/homing/vida de projétil e cura são **N/A**. A remoção de `ItemEntity` é descarte da entidade, sem prova de cobrança por unidade da stack ou de durabilidade. A nuvem é uma entidade de área, sem virar spell/projétil lançado por jogador. Eventos de destruição por outras causas e callbacks externos exigem suas próprias provas.

## Sete eixos e integração por perks

| Eixo | Evidência estática | Limite conservado |
|---|---|---|
| Identidade | JAR/classes/método SHA-exatos, assinatura e registry/factory corretos | Fonte 1.1.1 adjacente; artefatos engine com autoridades separadas |
| Comportamento | Super primeiro, guardas Creative/removido, descarte, nuvem e explosão independentes da aceitação do spawn | Super retorno normal é precondição; execução transformada não testada |
| Parâmetros | Seletores 4/5, chance de inventário distinta, payload/radius/lifetime/cor/partícula/potência | Argumentos nativos não são outcomes físicos |
| Targeting | Nenhuma busca direta de vítimas; nuvem e explosão delegadas com posição e fonte explícitas | Sem equivalência a raio de dano, regras PvP ou claims aprovadas |
| Custos/tempo | Descarte versus stack settlement, payload versus duração da nuvem; campos próprios N/A | Não inventa mana/cooldown ou débito por alvo |
| Integração | Ponte NeoForge versionada, owners distintos, registry positivo e negativos; autoridade nativa mantida | `NO_MUTATION`; nenhum setter/callback é hook per-player homologado |
| Validação | Selo nativo e referência reproduzível, negativos causais/registro/artefato e índices consistentes | `NOT_VERIFIED` para hooks; `NOT_TESTED` para QA física |

Black Arcana mantém seu runtime e `WorldEffectPolicy`; não se presume que o efeito de terceiro passe automaticamente por sua proteção. RPG Skill Tree mantém progressão e gates reais. Uma perk não deve reemitir nuvem, explosão ou crédito de XP a partir de um callback sem autoridade e deduplicação comprovadas. Não foi adicionado adapter, hook, Java de runtime ou Stage nesta entrega.

## Reprodução, testes e encerramento do recorte

O [auditor de contrato](../../../../docs/qa/alexscaves_1010_destroyed_item_contract_audit.py) confronta o JAR e o selo. O [auditor de referência NeoForge](../../../../docs/qa/alexscaves_1010_destroyed_item_engine_reference.py) confronta os dois artefatos oficiais 21.1.250 e sua projeção de patches/bridges. O [workflow dedicado](../../../../.github/workflows/alexscaves-1010-destroyed-item-contract.yml) reproduz ambos, sem reconstruir o engine inteiro:

```bash
python docs/qa/alexscaves_1010_destroyed_item_contract_audit.py \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --javap /caminho/jdk-21/bin/javap \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-DESTROYED-ITEM-CONTRACT-1.0.10.json' \
  --output /tmp/destroyed-item-contract.json
```

Critérios de aceitação: reprodução determinística dos selos, rejeição de artefato/operando/branch/registro/ABI divergente e de promoção de segurança; cobertura dos campos próprios e das delegações delimitadas; preservação da ficha histórica/probe anterior; índices gerados sem inconsistências. A CI e o registro da PR documentam os resultados executados. Sucesso da leitura de bytecode/patch não significa spawn, efeito ou destruição física aceitos.

**QA física pendente:** invocação efetiva no NeoForge do pack, Creative versus outras fontes, remoção anterior e reentrada, lado cliente/servidor, aceitação/recusa da nuvem, nuvem recusada com explosão solicitada, vítimas e duração efetiva, resistência/Hazmat, fogo/explosão de outras origens, proteção territorial, autoria, drops, chunks, save/reload e multiplayer. Nenhum desses cenários recebe PASS a partir da inspeção estática.

O objeto já era candidato na `main`; sua conclusão acrescenta **um certificado**, **zero candidatos** e **zero raízes mágicas**. O recorte passa a **222/2396 contratos estáticos**, **472/2396 fichas catalogadas**, **84/84 fichas observadas** do provider e **3/3 sistemas detectados**. Esses números são o recorte desta base, sem fechar todo o universo de integração. Dano 11/11 e encantamentos 51/51 permanecem intactos; providers integralmente homologados para perks continuam 0/164, catálogo de providers encerrado 4/164.

Próximo prefixo sem conclusão nesta entrega: **`server/item/ACDynamicAttributeItem`**. A contribuição concorrente da PR #1116 permanece separada, sem promoção presumida e sem sobrescrita. Catálogo integral do provider, hooks mutadores, mundo protegido e QA física continuam pendentes.
