# Ars Nouveau 5.13.1 — dezesseis Effects finais: inventários, estados e entidades

Revisão de **25/10/2026**, base `Black-Arcana/main@88368f2d37a14de855c54579bc53cd1b173581a1` (PR #914). Este lote acrescenta dezesseis contratos estáticos aos93 existentes, preservando os trabalhos anteriores. O recorte passa a **67/67 Effects**, **85/85 glyphs**, **24/24 rituais**, **109/138 fichas Ars** e **109/2075 fichas candidatas globais**. Os **164 providers** continuam sem certificação integral: **0/164**. Ainda restam29 fichas Ars detectadas — seis familiares, vinte perks e três sistemas — e o universo integral de conteúdo integrável continua aberto.

Os85 glyphs são componentes composicionais (cinco Forms, treze Augments,67 Effects), não85 magias prontas ou uma enumeração de todas as combinações do jogador. As barras do [catálogo global](../INDEX.md), do [provider](INDEX.md), dos [glyphs](glyphs/INDEX.md) e dos [Effects](glyphs/effects/INDEX.md) distinguem fichas estáticas de escopo integral do mod. Uma subpasta com todas as fichas detectadas certificadas não homologa runtime, hooks ou provider inteiro.

## Proveniência e limites da evidência

Source oficial `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, release **5.13.1**, MC1.21.1. Publisher Modrinth [qEFs5RRw](https://modrinth.com/mod/ars-nouveau/version/qEFs5RRw), `ars_nouveau-1.21.1-5.13.1.jar`, **20107711 bytes**, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, SHA-256 `99dff85e8778f7ae21dfd51cdedadf20f555a834fc757c0afe5f03c10eea96f2`. A [auditoria compilada](EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) confirma109 pares de ID/classe (85 glyphs e24 rituais), sem provar equivalência integral dos métodos Java com o JAR, registry carregado ou gameplay. O perfil instalado original não foi novamente medido; o publisher coincide com o fingerprint físico histórico #047.

O [manifesto](../../meta/PERK-READY-CERTIFICATIONS.json) mantém sete campos de evidência por ficha, `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `evidence_grade=PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`, **`mutating_hook=NOT_VERIFIED`** e **`physical_qa=NOT_TESTED`**. Foram usados fatos, fórmulas, paráfrases e referências; não foram incorporados implementações completas ou assets upstream. Config efetiva, addons, proteção de claims, interação entre listeners, reload e execução física continuam por validar.

## Contratos por objeto

| Effect | Consumidor e distinção necessária para perks |
|---|---|
| [Access Ender Inventory](glyphs/effects/access-ender-inventory.md) | Acesso ao menu depende do caster e dos ramos de targeting; a interface aberta não prova transferência de itens. |
| [Infuse](glyphs/effects/infuse.md) | Registro de potion providers, consumo, frasco vazio, fallback de PotionItem/Potion Jar e modo de emissão são etapas distintas. |
| [Interact](glyphs/effects/interact.md) | Interação usa caster/fake player, item e hit próprios; extração, uso e devolução não formam uma transação universal. |
| [Item Pickup](glyphs/effects/item-pickup.md) | Seleção e inserção são separadas; o payload de Post contém o restante, não necessariamente a quantidade recebida. |
| [Toss](glyphs/effects/toss.md) | Budget por quantidade solicitada, slots elegíveis, preferências e quantidade realmente extraída diferem; comparação com a main hand não identifica um slot único. |
| [Name](glyphs/effects/name.md) | Nome da entidade/bloco e mutação da offhand do caster têm ramos diferentes; localizar um name tag não significa consumi-lo. |
| [Wololo](glyphs/effects/wololo.md) | Dye discreto, cor contínua, implementação de IWololoable e cache de receitas são consumidores distintos; o nome FixedStack não comprova um limite efetivo para todos os métodos. |
| [Intangible](glyphs/effects/intangible.md) | Substituição, duração processada, restauração do estado e serialização pertencem ao tile; não é uma permissão genérica para alterar blocos protegidos. |
| [Prestidigitation](glyphs/effects/prestidigitation.md) | Bloco de partículas e efeitos em entidade possuem receptores e tempos próprios; emissão visual não confirma efeito mecânico ou novo cast. |
| [Animate Block](glyphs/effects/animate-block.md) | Animação de bloco, cabeças, alvo de ataque, tempo gasto por hit e retorno a falling block têm ciclos de vida específicos. |
| [Bubble](glyphs/effects/bubble.md) | Captura, status sincronizado de pop, remoção e bônus em dano recebido são operações distintas; pop não é um novo golpe direto. |
| [Summon Decoy](glyphs/effects/summon-decoy.md) | Redirecionamento inicial de alvos e entidade persistente são separados; não inferir taunt contínuo, filtro universal de hostilidade ou LOS. |
| [Summon Steed](glyphs/effects/summon-steed.md) | Montaria, owner, atributos, expiração e serialização precisam ser tratados no consumidor da entidade. |
| [Summon Undead](glyphs/effects/summon-undead.md) | Contagem depende de Split; o skeleton usa dano periódico após expirar, não descarte imediato uniforme. |
| [Summon Vex](glyphs/effects/summon-vex.md) | Tempo limitado herdado de vanilla e campo de tempo exposto pela interface Ars não são o mesmo estado; ownership também tem mais de um receptor. |
| [Summon Wolves](glyphs/effects/summon-wolves.md) | Número de lobos, atributos, owner, AI e descarte por expiração pertencem ao caminho específico, não ao de Vex ou Skeleton. |

Cada ficha inclui classe/métodos/linhas, fórmulas, unidades, filtros, receitas, defaults, campos não aplicáveis e condições de invalidação. Limitações de vanilla não inspecionada são tratadas como fronteiras de evidência; não foram preenchidas com números inferidos.

## Inventário: referência, extração, inserção e restituição

[`InventoryManager.extractItem`][extract] seleciona um handler e extrai de uma referência; Randomize escolhe um slot elegível dentro do handler escolhido, não um item uniforme de todos os inventários. No [`highestPrefInventory`][preference], cada handler começa com preferência LOW mesmo sem achar um item correspondente. Uma seleção de handler não garante que o glyph encontrará um item válido em algum inventário posterior. As fichas documentam os limites de slots e o modo de criação do manager em cada caster.

[`preferredForStack`][preference] devolve uma PriorityQueue, enquanto [`insertStackWithReference`][insert] a percorre com for-each; o caminho observado não comprova ordenação estrita de todas as inserções. O retorno da inserção é o restante. Os callbacks que o recebem não devem tratar esse stack como loot adquirido sem verificar a diferença efetiva e o inventário de destino.

[`ExtractedStack`][restitution] distingue `returnStack`, `returnOrDrop` e `replaceAndReturnOrDrop`. `returnOrDrop` não esvazia seu campo stack quando a devolução completa retorna vazio; repetir a operação não tem garantia de idempotência. Um adapter não deve chamar novamente restituição do provider como se fosse rollback próprio. Eventos, outputs, mundo e contadores podem ocorrer em momentos diferentes; o contrato de perk precisa seguir a operação realmente confirmada.

## Invocações: gates, owner, tempo e eventos

[`AbstractEffect.canSummon`][summon-helper] exige player real e ausência de Summoning Sickness, salvo creative. Isso é um helper usado por certos glyphs, não um veto global automático a toda entidade mágica: Animate e Bubble têm seus próprios caminhos. O helper `summonLivingEntity` atribui ownerID, tenta `addFreshEntity`, pode continuar contexto por Summoning Focus e publica [`SummonEvent`][summon-event]; o retorno booleano do spawn não é validado ali. O evento não é uma confirmação universal de nascimento bem-sucedido, dano ou cast novo.

[`SummoningFocus`][focus] tem consumidores concretos: modifica dano nos stats, tenta dobrar o tempo e aplicar Strength/Speed no evento de summon, replica certos casts Self em summons próximos e reage à morte com dano de thorns. O evento de summon consulta `getOwner()`, enquanto os listeners de cast/morte consultam `getOwnerAlt()`. Uma classe que mantém owners ou contadores distintos, como Vex, pode não seguir a interpretação esperada de todos esses caminhos. Não anunciar o mesmo bônus, duração ou Dispel para todas as invocações por analogia.

Expiração, morte por combate, despawn, owner ausente, unload/reload e perda de referência ao caster não são um único evento. Os consumidores podem descartar, sofrer dano periódico ou usar lógica vanilla herdada. `SummonEvent.Death.wasExpiration` é um campo do evento; sua presença não torna todos os ramos de cleanup equivalentes ou garante atribuição original de custo e Mastery. Captura de Bubble e retorno de blocos animados também requerem confirmação própria de estado/persistência.

## APIs, autoridades e validação

As [superfícies públicas de resolução](EFFECT-STATIC-CONTROL-FIELDS-FIFTEEN-5.13.1.md) continuam reais: builder original mutável em `SpellModifierEvent` e veto de `EffectResolveEvent.Pre`. Reatribuição de campos do evento não substitui automaticamente os locais do resolver. `Post`, tick, partícula, contexto filho, tentativa de inserção, spawn solicitado ou pop não equivalem a dano, transferência ou cast pagos confirmados. Scalar, flag, presença, contagem e receita original precisam ser alterados na fase e no consumidor corretos.

Ars conserva composição, targeting, recursos, aprendizagem, inventários e entidades nativas. RPG Skill Tree conserva progressão/perks/gates por contrato; Black Arcana conserva sua transação, Corruption, Strain e WorldEffectPolicy; Enshrouded conserva seus sistemas ambientais. Nenhum desses limites autoriza repetir o efeito de Ars, assumir ownership ou premiar cada tick/contexto como cast independente.

O fechamento documental dos85 glyphs e24 rituais não certifica as29 fichas Ars restantes nem o universo integral de sistemas integráveis. Config implantada, capacidade de mutação segura por perks, execução em servidor/cliente, multiplayer, proteção de claims e persistência física continuam pendentes. Mudança de release, source, config, receitas, listeners ou consumidores exige reauditoria. Não houve implementação de adapter, alteração de runtime ou promoção de Stage.

[insert]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/InventoryManager.java#L60-L94
[extract]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/InventoryManager.java#L96-L124
[preference]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/InventoryManager.java#L210-L276
[restitution]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/ExtractedStack.java#L19-L68
[summon-helper]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractEffect.java#L69-L89
[summon-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SummonEvent.java#L14-L43
[focus]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/curios/SummoningFocus.java#L44-L98
