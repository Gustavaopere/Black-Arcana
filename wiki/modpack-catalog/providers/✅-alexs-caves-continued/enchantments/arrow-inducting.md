# Arrow Inducting — `alexscaves:arrow_inducting` (1.0.10)

**Contrato técnico individual:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. A ficha conclui o recurso publisher, a conversão no evento e o comportamento próprio da Seeking Arrow no recorte estático descrito. **Hook mutador:** `NOT_VERIFIED`; **QA física:** `NOT_TESTED`; **integração:** `NO_MUTATION`. A herança da engine tem proveniência de compilação separada; o runtime transformado do modpack continua não verificado. Nenhuma perk executável ou nova raiz de cast resulta desta conclusão.

## 1. Identidade e proveniência

- **Provider / ID:** Alex's Caves Continued / `alexscaves:arrow_inducting`; encantamento passivo reativo do **Resistor Shield** (`alexscaves:resistor_shield`).
- **Publisher:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**. O `META-INF/neoforge.mods.toml` declara `modId=alexscaves`, versão `1.0.10`, Minecraft `[1.21.1]`, NeoForge e dependência obrigatória `codxlib >=1.3.6`.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Recurso:** `data/alexscaves/enchantment/arrow_inducting.json`, SHA-256 `80d52e42318ad732b32ba6118dea8f5b315b8d2d702da32d202ff95246a973e5`.
- **Descrição literal em `en_us.json`:** “Resistor Shield transforms any deflected arrows into seeking arrows”. O nome publicado é “Arrow Inducting”; o `pt_br.json` da mesma release não contém nome nem descrição para este ID. A frase do provider resume a intenção; as guardas compiladas abaixo determinam o contrato técnico.
- **Prova atual:** [manifesto consolidado SHA-exato](../EXACT-ARROW-INDUCTING-CONTRACT-1.0.10.json) e [regressão semântica da ficha](../../../../../docs/qa/alexscaves_1010_arrow_inducting_cards_test.py). Hashes da ficha, recursos e classes, além das âncoras dos métodos, ficam no manifesto.

A fonte adjacente [Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37](https://github.com/Codx-org/AlexsCavesContinued/tree/523308608422ab8e31974befa7111ecdf495dd37) declara **1.1.1**. Serve de contexto, sem autoridade sobre os valores do publisher **1.0.10** auditado aqui.

## 2. Configuração, aplicação e aquisição

| Campo | Valor publisher 1.0.10 | Significado delimitado |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.arrow_inducting` | Chave de tradução |
| `supported_items` | `#alexscaves:enchantable/resistor_shield` | Tag empacotada contém somente `alexscaves:resistor_shield` |
| `weight` | `2` | Peso de configuração, sem probabilidade observada |
| `max_level` | `1` | Nível nativo I; o leitor Java não aplica clamp local |
| `min_cost` | `base=1`, `per_level_above_first=18` | Para I: 1 |
| `max_cost` | `base=41`, `per_level_above_first=10` | Para I: 41 |
| `anvil_cost` | `4` | Campo de encantamento, sem relação com mana ou dano |
| `slots` | `mainhand`, `offhand` | Slots declarados; o evento lê a stack efetivamente usada |

O JSON não declara `effects` nem `exclusive_set`; a conversão está no consumidor Java. A varredura dos recursos nativos não encontrou exclusão de Arrow Inducting em outro `exclusive_set`; as únicas tags nativas de encantamento empacotadas são as quatro de aquisição abaixo. Isso fecha as **exclusões declaradas neste publisher**, sem garantir compatibilidade com datapacks ou outros mods.

O ID está explicitamente nas tags `minecraft:in_enchanting_table`, `minecraft:non_treasure`, `minecraft:on_random_loot` e `minecraft:tradeable`. São declarações de disponibilidade; resolução final das tags e chances reais de mesa, loot e trade dependem do jogo e dos datapacks ativos. A tag de item tem SHA-256 `2b5d57ffc709293f994b472c07cd44ed34647efec41106b819621c060366f3e0`; as quatro tags de aquisição compartilham SHA-256 `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1`.

A receita shaped do escudo é `SSS` / ` H ` / `AAA`: três `scarlet_neodymium_ingot`, um `heart_of_iron` e três `azure_neodymium_ingot`; o resultado é `alexscaves:resistor_shield`, com `count` omitido no JSON. O item declara stack máxima **1**, durabilidade **1000**, raridade **UNCOMMON**, `getEnchantmentValue=1` e `isEnchantable(stack)` somente quando `stack.count==1`. A raridade é do item; o encantamento conserva o peso numérico 2.

## 3. Ingresso completo e substituição da flecha

**Classe:** `server/event/CommonEvents.class`, SHA-256 `d132caad67ecab68844091ee396d37fecc4860440d338dcd82384f1555f8ad43`. O helper completo `acLivingAttack(LivingIncomingDamageEvent)Z` tem **91 instruções**, digest `3b6a9d9699a101ff2c4aa61dc08308857a1480fdd11f711c5ce04e2638244368`. Seu caller `livingAttack` tem **8 instruções** e só chama `event.setCanceled(true) @10` se o helper retornar true.

As cinco guardas da região de Arrow convergem para `@158` quando falham:

1. `event.getSource().getDirectEntity()` precisa ser uma **`AbstractArrow`** (`instanceof @9`, desvio `@12`). Outros projéteis não entram por essa guarda.
2. A entidade defensora precisa estar bloqueando (`isBlocking @24`, desvio `@27`).
3. Sua stack de uso precisa ser exatamente **`ACItemRegistry.RESISTOR_SHIELD`** (`getUseItem @34`, `ItemStack.is @48`, desvio `@51`). Estar apenas equipado em um slot não satisfaz essa leitura.
4. `ACCompat.enchantLevel(stack, ARROW_INDUCTING) @66` precisa ser **positivo** (`ifle @69`). O helper devolve o primeiro valor armazenado cujo Holder corresponde à ResourceKey, ou zero; não limita a leitura a `max_level=1`. Um nível positivo não nativo passa pela mesma conversão, sem escala adicional por nível nesse ramo.
5. O tipo da flecha original precisa ser diferente de **`ACEntityRegistry.SEEKING_ARROW`** (`if_acmpeq @84`). Essa exclusão evita reconverter o próprio tipo nativo; não é um cooldown por jogador.

`isBlocking` é o flag consultado: o helper não testa direção do escudo, deflexão efetivamente aceita, piercing ou bypass de escudo. A descrição de “deflected arrows” não acrescenta essas guardas ao binário.

Se todas passam, o helper cria **uma nova** `SeekingArrowEntity(Level,LivingEntity)` com o **defensor** como entidade viva (`@92–102`); copia a posição da flecha original (`@110`); aplica `velocidadeOriginal × -0.4D` (`@119–125`) e `YRotOriginal + 180F` (`@134–138`). Em seguida solicita `Level.addFreshEntity @150`, **descarta seu booleano em `@153`** e chama `original.discard @155`. O descarte não é condicionado ao sucesso do spawn. Essa sequência não copia NBT, efeitos, dano, piercing, item ou encantamentos da flecha original; o projétil novo segue seus construtores nativos.

**Cancelamento delimitado:** a região Arrow não chama `setCanceled`, não retorna true e não garante negar o hit no defensor. Ela continua no trecho `@158–211`; o único resultado true do helper pertence ao ramo posterior cuja entidade direta é uma **`LivingEntity` com `STUNNED`** (`hasEffect @200`, `@203`, true em `@206`). Esse ramo distinto pode levar o caller ao cancelamento. Não transferir esse true à conversão Arrow nem concluir o resultado global do dano a partir do descarte da flecha. Não há guarda própria de lado lógico na conversão; execução e autoridade efetivas do evento dependem da engine e dos handlers carregados.

## 4. Busca, alvo e trajetória próprios

**Classe:** `server/entity/item/SeekingArrowEntity.class`, SHA-256 `1102754436829c3dcadb1450d6ab15efb354a3f4e58a2a262a78c5013d7f0e25`. `tick()V` completo: **185 instruções**, digest `eb936d76c3fbdcf1be042312dd7dba664af91244529443c7806aa6a4a2c7e152`.

O método chama primeiro `AbstractArrow.tick @1`. Só depois lê o ID de alvo e considera a busca própria; `inGround` (`@10–13`) ou `stopSeeking` (`@17–20`) desviam essa etapa para `@272`. Portanto o flag desliga o steering próprio, sem interromper a física herdada do tick.

| Caminho | Contrato completo do método próprio |
|---|---|
| **Aquisição: ID `-1`** | Executa somente quando `!level.isClientSide()` (`@29–35`). Consulta entidades na AABB da flecha expandida em `r = min(10, 3 + tickCount / 4)` (`@45–82`), com divisão inteira. O predicado `lambda$tick$0` delega a `canHitEntity` herdado; não é uma lista incondicional de LivingEntities. |
| **Escolha** | Conserva o candidato elegível estritamente mais próximo (`distanceTo @121/@126`, `ifge @130`). Rejeita `ownedBy(candidato) @136` e, quando há owner, `candidato.isAlliedTo(owner) @149`. Distâncias iguais conservam o primeiro elegível da lista. O candidato é uma `Entity`; não há exigência própria de LivingEntity ou hostilidade, seleção obrigatória do atirador original, busca de menor HP ou filtro próprio adicional de LOS nesse laço. |
| **Lock** | Se houve candidato, pede `SEEKING_ARROW_LOCKON` com volume **5F** e pitch **1F** (`@166–180`) e grava seu ID (`setArcTowardsID @188`). O salto `@191 → 272` faz a aquisição terminar **sem steering no mesmo tick**. Se não houve candidato, o ID permanece `-1` e outra aquisição pode ocorrer no tick seguinte. |
| **Seguimento: ID diferente de `-1`** | Resolve `level.getEntity(id) @199`. Esse ramo não repete a guarda de servidor, `canHitEntity`, `ownedBy` ou aliança. Se a resolução for null (`@204 → 272`), não limpa o ID e não readquire outro alvo; ticks seguintes continuam usando o ID armazenado. |
| **Geometria e movimento** | Mira em `alvo.position + (0, 0.65F × alvo.getBbHeight(), 0)` (`@208–228`). Só faz steering quando o comprimento desse deslocamento é **maior que a largura do alvo** (`@233–242`). Aplica `vNova = vAtual × 0.30000001192092896D + normalize(deslocamento) × 0.699999988079071D` (`@247–269`), sem normalizar novamente a soma. Não é velocidade constante garantida, teleporte, alcance máximo ou raio de dano. |

A expansão `r` vale 3 antes de `tickCount=4`, cresce em passos de quatro ticks e satura em 10 a partir de `tickCount=28` no valor lido pelo método. Ela expande a **caixa de busca atual**; não fixa a distância total de voo nem cria AoE. A consulta herdada de colisão continua distinta do armazenamento e seguimento de um alvo.

Após a etapa de busca, o trecho cliente exige `isClientSide && !inGround` (`@276–286`) e pede partículas `SCARLET_SHIELD_LIGHTNING @391`. Partículas e som não demonstram hit, dano elétrico ou aceitação de spawn.

## 5. Ciclo de vida, dimensões, recursos e persistência

O manifesto atual sela os **12 membros comportamentais declarados** que já compunham o roster histórico e o **inicializador estático `<clinit>()V` de 5 instruções** que define o accessor de sincronização. A cobertura própria não depende só da presença de nomes:

| Membro próprio | Corpo / consequência estática |
|---|---|
| Construtor `(EntityType,Level)` — 5 instruções | Delega ao construtor base de `AbstractArrow`; usado pela factory registrada. |
| Construtor `(Level,DDD)` — 17 | Usa o tipo e a stack `SEEKING_ARROW`; a assinatura não recebe LivingEntity nem fornece owner por esse parâmetro. |
| Construtor `(Level,LivingEntity)` — 15 | Usado pela conversão; passa o defensor, tipo e stack `SEEKING_ARROW` para `AbstractArrow`. Não copia o projétil anterior. |
| `defineSynchedData` — 10 | Chama a base e define `ARC_TOWARDS_ENTITY_ID` com sentinela **`-1`**. |
| `getArcTowardsID` / `setArcTowardsID` — 7 / 7 | Leem/escrevem o inteiro por `SynchedEntityData.get/set`; não são serialização NBT. |
| `tick` / `lambda$tick$0` — 185 / 4 | Fluxos completos de aquisição/seguimento acima; lambda delega à elegibilidade herdada. |
| `doPostHurtEffects(LivingEntity)` — 4 | Só grava **`stopSeeking=true`**. Não chama super, `hurt`, efeito de status ou descarte; a chamada pelo impacto é herdada e condicionada. |
| `getAddEntityPacket` — 4 | Delega a `ACPlatform.getEntitySpawningPacket(entity,serverEntity)`; não comprova autenticação ou entrega física da rede. |
| `getDefaultHitGroundSoundEvent` / `getDefaultPickupItem` — 4 / 7 | Retornam `SEEKING_ARROW_HIT` e nova stack `SEEKING_ARROW`; isso não garante pickup/drop ou hit aceito. |

A binding de `ACEntityRegistry.SEEKING_ARROW` resolve `lambda$static$11`: categoria **MISC**, dimensões registradas **`0.5F × 0.5F`**, intervalo de atualização **1** e `setShouldReceiveVelocityUpdates(true)`. Sua factory aponta ao construtor `(EntityType,Level)`. São dimensões e parâmetros de rede nativos; o encantamento não possui multiplicador próprio de tamanho, dano em área ou escala visual, e a hitbox efetiva após transformações não foi testada.

**Custo de uso:** a região de conversão e os corpos próprios da flecha não debitam mana, stamina, Soul Energy, munição adicional, durabilidade extra por conversão nem cooldown próprio. Isso não torna o bloqueio gratuito: o Resistor Shield tem durabilidade e o jogo pode cobrar o bloqueio. O uso nativo do item chama `startUsingItem(hand)`; quando agachado troca a polaridade, solicita som e retorna `ACCompat.useConsume`, que é `InteractionResultHolder.consume` **sem shrink da stack**. O ramo próprio de uso do escudo solicita **1** de durabilidade em `t==10 && !level.isClientSide()`, com `t=getUseDuration(stack,null)-remainingUseTicks`; esse custo pertence ao uso do escudo, sem contador de flechas convertidas. Criativo, Unbreaking, quebra efetiva e custos herdados do bloqueio não estão liquidados por esta prova.

A prova desse custo usa a região delimitada `ResistorShieldItem.onUseTick @584–601`; o método tem **276 instruções** e não é declarado integralmente coberto nesta ficha. Essa janela de contexto não substitui a prova completa do ramo de conversão e dos membros próprios da flecha.

Não há método próprio de lifetime, `onHitEntity`, `onHitBlock`, `addAdditionalSaveData` ou `readAdditionalSaveData`, nem reset próprio do ID de alvo. O provider não serializa `stopSeeking` e `ARC_TOWARDS_ENTITY_ID` por esses overrides; sincronização de entidade não demonstra persistência em NBT. A física, colisão, despawn e parte da persistência são herdados. Ausência de override não significa duração infinita ou ausência de dano.

O item também não declara override de duração de uso ou animação/ação de bloqueio. Esses comportamentos de `ShieldItem` são herdados e ficam fora da prova de metadados do publisher; o valor `t` acima não fixa a duração total da Seeking Arrow.

## 6. Herança: evidência de compilação separada do publisher

A cadeia abaixo vem do [manifesto herdado já reproduzido](../EXACT-ARROW-INDUCTING-INHERITED-ENGINE-1.0.10.json) e da [sonda de proveniência da engine](../../../../../docs/qa/alexscaves_1010_arrow_inherited_engine_probe.py): classpath **efetivo de compilação** de Minecraft **1.21.1**, NeoForge **21.1.248**, ModDevGradle **2.0.144**. O JAR de engine selecionado tem **22.702.897 bytes**, SHA-256 `fd58bb47e9ebbeefaa42871888e113b0bd1e643babc6877a237b6c8713a7a1c4`; classes `AbstractArrow=2cc85f8cb1bacba5c59c462c636f7bfad754db859253b75900a55f9888acccef` e `Projectile=42e5b3a088bd4446abab0fe8cd2e61368095fe664aa38d6b256ab0424625326d`.

Variantes do cache `rename`, `binaryPatch`, `copyUnpatchedClasses`, `binaryWithNeoForge` e `applyDevTransforms` têm classfiles diferentes. A seleção acima corresponde ao compilador; **não é o código final transformado por ModLauncher/mixins do pack instalado**. Os hashes do provider não transferem sua autoridade SHA-exata ao runtime da engine.

| Eixo herdado | Evidência delimitada no binário de compilação |
|---|---|
| **Dano / tipo** | O construtor base inicia `baseDamage=2.0D`. `Projectile.onHit` despacha hits de entidade/bloco e contém deflexão; `AbstractArrow.onHitEntity` tem 323 instruções no manifesto de compilação, solicita fonte por `DamageSources.arrow @47`, passa por `EnchantmentHelper.modifyDamage @92`, chama `Entity.hurt @298` e trata o booleano em `@301`. **2.0D é o estado inicial da base**, sem promessa de dano pedido, dano aceito, HP final ou número de hits da Seeking Arrow. |
| **Pós-hit** | A chamada virtual `doPostHurtEffects @397` fica depois da checagem de retorno do `hurt` e de outros guardas. Quando alcança o override do provider, fixa `stopSeeking=true`; não afirmar que toda colisão executa o callback. |
| **Autoria** | `SeekingArrow(Level,LivingEntity)` delega ao construtor de `AbstractArrow` que chama `setOwner @28`; `Projectile.setOwner` grava `ownerUUID @9` e `cachedOwner @14`. Assim o defensor é encaminhado à autoria inicial por essa cadeia de compilação. `getOwner` pode resolver o UUID em `ServerLevel.getEntity(UUID) @52`; isso não garante crédito de kill, XP ou Mastery. |
| **Persistência** | A base grava/lê `Owner`, `LeftOwner`, `HasBeenShot`; `AbstractArrow` acrescenta campos como `life`, `inGround`, `damage`, `pickup`, `crit`, `PierceLevel`, `item` e `weapon`. É uma rota herdada de persistência, sem garantia de resolução de owner ausente, unload, cross-dimension, ID reutilizado ou save/reload do pack transformado. |
| **Colisão / elegibilidade** | `AbstractArrow.canHitEntity` delega a `Projectile.canHitEntity`, com filtros adicionais da base. Essa rota alimenta o predicado de aquisição, mas a perseguição de um ID já gravado não refaz os filtros no método próprio. Proteção PvP, claims, eventos terceiros e aceitação real permanecem fronteiras externas. |

## 7. Sete eixos do contrato e fronteiras de perks

| Eixo | Contrato estático consolidado | Fronteira de integração |
|---|---|---|
| **1. Targeting** | Conversão de `AbstractArrow` com cinco guardas; aquisição do elegível mais próximo, exclusão do owner e de candidato aliado ao owner; seguimento por ID sem rechecagem | Não tratar alvo armazenado como permissão contínua, origem do disparo ou settlement de proc |
| **2. Range / área** | AABB atual expandida em `min(10,3+tickCount/4)` para aquisição; nenhum AoE próprio | Caixa de busca não autoriza perk de alcance total, dano radial ou hit garantido |
| **3. Velocidade / direção** | Inversão inicial `-0.4D`, YRot `+180F`; steering `0.30000001192092896D / 0.699999988079071D`, geometria de altura/largura; não normaliza a soma | Alterar vetor exige boundary própria e autoridade; não duplicar tick nem assumir velocidade constante |
| **4. Projétil / tamanho** | Uma nova Seeking Arrow, registro `0.5F × 0.5F`, update 1; spawn sem checagem seguido do descarte original | Sem autorização para mudar hitbox, escala, quantidade ou preservar automaticamente payload da flecha original |
| **5. Dano / tipo** | Provider não define dano próprio no override pós-hit; herança compilada oferece pipeline de flecha e `baseDamage` inicial 2.0D | Não criar DamageType elétrico/mágico, duplicar `hurt` ou promover baseDamage a HP final |
| **6. Duração / recursos** | Sem lifetime/cooldown/custo adicional próprios por conversão; `stopSeeking` desliga somente busca; durabilidade e tempo de uso pertencem ao escudo/base | Não usar custo de mesa/bigorna como recurso de cast nem tomar silêncio do provider por gratuidade do bloqueio |
| **7. Autoria / proteção / procs** | Defensor entra no construtor; owner/persistência base têm prova de compilação; ID ausente fica armazenado sem retarget | Crédito de kill/XP/Mastery, deduplicação, PvP/claims e reload requerem verificação específica; nenhum proc presumido |

O RPG Skill Tree conserva a responsabilidade por perks/Mastery e o Black Arcana preserva o processamento nativo. Callback, descriptor JVM, setter de campo ou tag não constituem hook mutador seguro. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`: esta ficha documenta o comportamento e não implementa adapter, perk, dano adicional ou mudança de Stage.

## 8. Provas, histórico e conclusão delimitada

A [prova consolidada atual](../EXACT-ARROW-INDUCTING-CONTRACT-1.0.10.json) fecha o contrato estático individual com recursos, corpos nativos completos do caller de evento **8**, helper **91**, `tick` **185**, demais membros próprios da flecha, inicializador estático e helpers selecionados, além de bindings de registro e da janela delimitada de custo do escudo. A [regressão semântica](../../../../../docs/qa/alexscaves_1010_arrow_inducting_cards_test.py) protege guardas, retorno/cancelamento, spawn sem confirmação, aquisição/seguimento, geometria, custo e limites de herança. As verificações comparam o publisher SHA-exato e os selos; não são uma sessão física de Minecraft.

A trilha anterior permanece disponível como evidência histórica, com os limites de cada etapa: [identidade e primeiras janelas](../EXACT-ARROW-INDUCTING-1.0.10.json) / [sonda original](../../../../../docs/qa/alexscaves_1010_arrow_inducting_probe.py), [roster de ciclo de vida](../EXACT-ARROW-INDUCTING-LIFECYCLE-ROSTER-1.0.10.json) / [sonda de roster](../../../../../docs/qa/alexscaves_1010_arrow_inducting_lifecycle_probe.py), [âncoras causais](../EXACT-ARROW-INDUCTING-CAUSAL-FLOW-1.0.10.json) / [sonda causal](../../../../../docs/qa/alexscaves_1010_arrow_causal_flow_probe.py) e [herança de compilação](../EXACT-ARROW-INDUCTING-INHERITED-ENGINE-1.0.10.json). As antigas lacunas de tradução, conteúdo da tag, seleção completa e callback próprio estão resolvidas acima; o grau parcial dessas etapas não é o estado atual desta ficha.

**Conclusão:** uma ficha individual concluída **somente** em `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`; **+0 raízes mágicas novas**, **+0 providers integrais concluídos**. O universo integral do provider permanece aberto. Hooks mutadores continuam `NOT_VERIFIED`, QA física `NOT_TESTED`, política `NO_MUTATION`; transformação ModLauncher/pack, hit/dano efetivamente aceitos, crédito de combate, proteção, rede, datapacks ativos e save/reload reais continuam sem certificação física. O próximo contrato parcial alfabético é `alexscaves:astral_transferring`.
