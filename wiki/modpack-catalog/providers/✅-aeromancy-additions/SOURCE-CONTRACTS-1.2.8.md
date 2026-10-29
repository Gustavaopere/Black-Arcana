# Aeromancy 1.2.8 — mapa dos contratos e proveniência

Fonte oficial: [`snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`](https://github.com/snackerpirater/aero-additions/tree/ae282b32d25ad76ef8d01c637ec05566a767ae4c). Árvore Git: `fcee08e613fbfa030f034268a0240c8693ab7f45`. [Fechamento](SOURCE-CATALOG-CLOSURE-1.2.8.md) · [manifesto](SOURCE-CATALOG-MANIFEST-1.2.8.json) · [índice](INDEX.md).

## Universo e inicialização

O inventário usa `git ls-files` da revisão limpa: **205 arquivos**, sendo **66 Java de implementação + sete `package-info.java`**, 77 recursos principais, 42 recursos gerados, um template de metadados e 12 arquivos de projeto/build. Cada caminho recebe SHA-256, tamanho e referência a fichas ou disposição de suporte no manifesto; nenhuma classe desconhecida é descartada como decoração.

[`Aeromancy` L27–41](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/Aeromancy.java#L27-L41) registra sons, spells, itens, aba criativa e attachments no mod event bus. [`AASpells.register` L50–78](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L50-L78) liga os registros de spells, entidades, escola, atributos e efeitos. O bootstrap é suporte compartilhado; os registros e consumidores com comportamento recebem fichas próprias.

| Superfície | Universo delimitado | Evidência documental |
|---|---|---|
| Spells | Dez chamadas de registro ativas; cinco comentadas | [Spells](spells/), [classes inativas](systems/unregistered-spell-code.md) |
| Combate e movimento | Seis efeitos e cinco EntityTypes; Shockwave sem registro | [Efeitos](effects/), [entidades](entities/) |
| Equipamento | Nove itens, dois atributos e uma escola Wind | [Itens](items/), [atributos](attributes/), [escola](schools/wind.md) |
| Estado e transporte | Um attachment, três payloads registrados e uma classe não registrada | [Estado](systems/aeromancy-spell-data.md), [registro de rede](systems/payload-registration.md), [payloads](payloads/) |
| Compatibilidade | Dois mixins comuns requeridos; protocolo opcional `1.0.0` | [Mixins](mixins/), [ciclo de vida](systems/state-lifecycle-network-ui.md) |
| Exposição e assets | Uma aba criativa e quatro SoundEvents registrados | [Aquisição/datagen](data-contracts/acquisition-and-datagen.md), [sons](data-contracts/sound-events.md) |

Os IDs locais têm namespace `aero_additions`. O DeferredRegister de serializers de entidades é declarado sem entradas nem binding ao event bus. A classe `AASyncEntityDataPacket` não está registrada e seu handler é vazio. Modelos, traduções, texturas ou um ID em código inativo não aumentam a lista de registros ativos.

## Dados, aquisição e pontos úteis para perks

Há 56 recursos de dados: oito receitas, oito advancements de receitas, 30 tags, dois damage types, um upgrade-orb type, dois loot modifiers, duas loot tables, uma lista global de loot modifiers, um override de config de spell e um material de jewelry. Os outros 63 recursos são assets ou configuração de mixins. As fichas de [dados](data-contracts/) especificam os valores e os consumidores.

As quatro receitas shaped usam namespace Aero; as quatro smithing usam `minecraft`. A receita `minecraft:windmaker_skirt` produz o item registrado `aero_additions:windmaker_leggings`; a diferença entre os nomes não é ausência de item. O Updraft Tome tem rota de loot no ominous vault e apresentação JEI, sem receita de crafting demonstrada. Breeze Rod entra no foco Wind e no foco do host. O override de `irons_spellbooks:gust` muda sua escola, sem criar um décimo primeiro spell Aero.

A tag em `data/minecraft/tags/damage_type/entity_type/deflects_projectiles.json` está sob a registry de damage types apesar de conter um ID de entidade; sua presença não prova uma tag válida de entity types. `sounds.json` contém `airblast_success`, mas não há um quinto SoundEvent registrado em `AASounds`.

Cada ficha delimita dano/tipo, geometria, aquisição de alvo, movimento/força, tempo, custo, autoridade e persistência quando há consumidor aplicável. Um atributo, setter ou callback existente é uma superfície candidata: não comprova um hook de mutação por jogador. Alterar estado cliente, cache de HUD ou tamanho de modelo não altera automaticamente o estado servidor, a seleção de alvo ou a hitbox.

## Fonte, publisher e instalação

| Evidência | Identidade e limite |
|---|---|
| Fonte | Revisão acima; versão declarada `1.2.8`; 205 hashes de arquivos no manifesto |
| Publisher | [CurseForge file 8251034](https://www.curseforge.com/minecraft/mc-mods/aeromancy-additions/files/8251034); [download oficial](https://edge.forgecdn.net/files/8251/034/aero_additions-1.2.8.jar), 753884 bytes |
| SHA-1 publisher | `dee32c9fa84a9b3796e39846608f8f77591ea56f` |
| SHA-256 publisher | `b2dad354467a2cf1a92519ba68c8e2c32807a976d7b235132d625b7f0f90eea8` |
| ZIP publisher | 308 entradas: 213 arquivos e 95 diretórios; 85 classfiles Aero, dos quais 73 externos e 12 internos; major 65 |
| Comparação de recursos | Todos os 119 recursos da fonte presentes: 83 iguais em bytes, 36 iguais somente após normalização CRLF/LF, zero outras diferenças |
| Comparação de classes | Os SourceFile dos 85 classfiles correspondem aos 73 Java rastreados, incluindo anotações; igualdade de nomes não prova corpos de métodos |
| Instalação | Modlist física declara `aero_additions` `1.2.8`; checksum histórico de 35 caracteres inválido; `installed_artifact_identity=NOT_VERIFIED` |

Os nove arquivos exclusivos do publisher são manifest, TOML expandido, dois arquivos jarjar (incluindo ExpandAbility `12.0.0`) e cinco caches de datagen. A dependência embutida não é somada às classes externas Aero. Os hashes publicados são evidência do arquivo obtido do publisher; não substituem hash independente do arquivo instalado.

## Contratos herdados e QA

[`gradle.properties` L8–28](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/gradle.properties#L8-L28) declara Minecraft `1.21.1`, NeoForge `21.1.228`, Iron's `3.16.1` e IronsLib `1.1.0`. O [template L28–67](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/templates/META-INF/neoforge.mods.toml#L28-L67) exige os mixins, Iron's `[1.21.1-3.15.0,1.21.1-4.0.0)` e ExpandAbility `[12.0.0,13.0.0)`.

Black Arcana compile/dev usa NeoForge `21.1.248`; a modlist física fixa `21.1.250` e Iron's `3.16.3`. As fichas que consultam a fonte do host `3.16.3` identificam esse pin separadamente. Herança examinada nessa versão não prova binding efetivo do provider compilado contra `3.16.1`, nem aplicação de mixins no pack.

Não há src/test nem GameTests implementados no universo rastreado. O workflow upstream configura JDK 17 enquanto o projeto declara toolchain Java 21; não se presume build upstream aprovado. O catálogo não executou gameplay, servidor Aero, persistência, aquisição, PvP ou proteção de mundo. [QA exigida](UPSTREAM-TESTS-RUNTIME-QA.md). CI do Black Arcana valida sua própria alteração e não homologa esse provider.

Os metadados declaram MIT; TEMPLATE_LICENSE.txt cobre explicitamente o template NeoForged MDK. Nenhum corpo de implementação, asset ou texto localizado upstream foi importado para Black Arcana. O manifesto retém identificadores, hashes e relações técnicas.

## Host Minecraft 1.21.1

Esta evidência auxiliar resolve o significado de argumentos do host usados nas fichas; fica fora do denominador de **205 arquivos Aero**. Foi examinada a implementação vanilla Minecraft **1.21.1**, sem execução de gameplay ou prova de equivalência do pack instalado. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; certificações **0**. Patches, mixins e consumidores IronsLib efetivos continuam QA separado.

Os dois artefatos já estavam no cache local; seus SHA-1 calculados coincidem com o manifesto de versão em cache:

| Artefato oficial, fixado pelo conteúdo | Bytes | SHA-1 | SHA-256 |
|---|---:|---|---|
| [Client 1.21.1](https://piston-data.mojang.com/v1/objects/30c73b1c5da787909b2f73340419fdf13b9def88/client.jar) | 26836906 | `30c73b1c5da787909b2f73340419fdf13b9def88` | `499f6897d1837516680f3114072d8106e11c9adcd933fe5cf051b551089b0c99` |
| [Mappings oficiais](https://piston-data.mojang.com/v1/objects/2244b6f072256667bcd9a73df124d6c58de77992/client.txt) | 9598610 | `2244b6f072256667bcd9a73df124d6c58de77992` | `140c47931cccc8fc9e4c22d7603e2d714d1a953a146f51ea7397d95c955536ec` |

A leitura usa também o arquivo derivado local `decompile_2472655742d9c696829d7485873443343ff9aa5b_output.jar` do cache NeoForm, SHA-256 `fae60f0810878cfedb00d79a4c5b256655bed8e7094f17f57206335d851ad098`. Os intervalos abaixo referem-se às entradas desse arquivo, não a uma suposta publicação oficial de código fonte. Os nomes foram associados pelos mappings oficiais e os quatro contratos foram conferidos com `javap -p -c` nas classes originais do client.

| Arquivo/contrato delimitado | Localizador no arquivo derivado | Confirmação no bytecode original e consequência |
|---|---|---|
| `net/minecraft/world/level/SimpleExplosionDamageCalculator.java` | Campos/construtor **L13–22**, `shouldDamageEntity`/`getKnockbackMultiplier` **L41–59**; entrada SHA-256 `de9db81bc7f7884260ec125b1fe193896de086bc5e2792c246ae8c0674ce8ade` | Mappings **L98545–98556**: classe `ddn`, campos `a=explodesBlocks`, `b=damagesEntities`, `c=knockbackMultiplier`. Construtor grava argumento 2 em `b`; `a(dco,bsr)` retorna `b`; `a(bsr)` usa `c`, com zero para Player que está voando. O literal Aero `(true,false,Optional.of(1.22×D),tag)` desliga o dano de explosão a entidades e escala knockback. |
| `net/minecraft/world/level/Explosion.java` | **L272–304**; entrada SHA-256 `6e99e0295c0b02e690353ae5df91bbc34dffc7ad32d263a4b83ba75803424cdc` | Classe `dco`, método `c()`; offsets **774–806** condicionam `hurt` ao calculator `shouldDamageEntity`; **807–830** calculam o termo de knockback separadamente. Mappings do calculator **L97809–97816** identificam esses métodos. Dano direto local de Magic Wind Charge continua sendo uma tentativa separada de **1.0F**; o campo chamado `damage` não substitui essa constante. |
| `net/minecraft/world/effect/MobEffect.java` | `addAttributeModifiers` **L150–158**, `AttributeTemplate.create` **L184–187**; entrada SHA-256 `831d8ef264b90bc04b261cf24804ec8be762d82fa346d31ed1272a4e124df772` | Mappings **L72356–72366**: `AttributeTemplate=brx$a`; `a(int)` multiplica a quantidade base por **amplifier+1**, offsets **8–16**. Wind Shield fornece base **0.03 ADD_VALUE**, e o spell usa amplifier `level−1`, produzindo modifiers nominais **0.03/0.06/0.09/0.12/0.15**. Isso não certifica a probabilidade final de dodge ou seu settlement IronsLib. |
| `net/minecraft/core/BlockPos.java` | `breadthFirstTraversal` **L478–503** | Mapping **L36909** identifica `jd.a(BlockPos,int,int,BiConsumer,Predicate)`; offsets **89–127** exigem posição única e predicado true antes de incrementar/testar o cap. O origin aceito também conta. Em Flush, **90/140/190** limita posições aceitas, sem provar esse número de blocos removidos ou de posições consultadas. |

Para reproduzir a conferência, verificar os hashes dos dois downloads, localizar os nomes acima nos mappings e executar com JDK 21:

```sh
javap -p -c -classpath minecraft_1.21.1_client.jar ddn dco 'brx$a' jd
```

A conclusão verificável fica nos artefatos oficiais fixados acima e nos contratos delimitados nesta seção. O superclass `AbstractWindCharge` também contém callbacks de hit/explosão, e o addon chama `super` antes dos callbacks próprios: contagem de dano aceito, impulsos, atribuição e efeitos físicos não são certificados por essa leitura estática.
