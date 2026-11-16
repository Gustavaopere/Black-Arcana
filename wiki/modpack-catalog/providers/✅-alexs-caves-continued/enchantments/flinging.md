# Flinging — impulso e geometria da Ortholance (1.0.10)

**Contrato técnico estático individual:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Integração:** `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `mutation=NO_MUTATION`. O recorte documenta o encantamento, o produtor integral `OrtholanceItem.releaseUsing` e os consumidores nativos necessários; não homologa mutações por perks, resultados físicos ou o provider integral.

`alexscaves:flinging` modifica a velocidade solicitada ao **usuário da Ortholance**. O mesmo vetor intermediário participa da posição das ondas e da caixa do ataque direto. A descrição de “ir mais longe” não representa alcance fixo em blocos, aumento próprio de dano, voo garantido ou novo cast do Black Arcana.

## 1. Identidade, versão e proveniência

| Objeto | Evidência publisher 1.0.10 |
|---|---|
| Provider / mod ID | Alex's Caves Continued / `alexscaves` |
| Plataforma | Minecraft 1.21.1 / NeoForge / Java 21 |
| Modlist instalada | `alexscaves-1.0.10-neoforge+1.21.1.jar`, [modlist sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/modlist.md), item 019 |
| Artefato publisher | [CurseForge projeto 1645389, arquivo 8856293](https://www.curseforge.com/minecraft/mc-mods/alexs-caves-continued/files/8856293), **75.279.314 bytes** |
| JAR SHA-1 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| JAR SHA-256 | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Identidade / símbolo | `alexscaves:flinging` / `ACEnchantmentRegistry.FLINGING` |
| Recurso | `data/alexscaves/enchantment/flinging.json`, **359 bytes**, SHA-256 `0680721d1687f85991e11ee33908b67aa8b720339e7b09eeaaaf92cf604356f2` |
| Tag de suporte | `data/alexscaves/tags/item/enchantable/ortholance.json`, **50 bytes**, SHA-256 `1c96a26e08800182b9c4b3b2f5ba4043389fe1bec0dcd5b12f1e5392cc28a5ac`; contém `alexscaves:ortholance` |
| Produtor | `OrtholanceItem.class`, SHA-256 `996b208a60f2c26c275e60e5d0e3a2fd0090cfb0ba1687907cac242de9a17d09` |
| Consumidor de ondas | `WaveEntity.class`, SHA-256 `93fdaee0239cc4985b351a6c2ac1edd23a51cf0088cb1172f983d0f869d9e42e` |
| Registro | `ACEnchantmentRegistry.class`, SHA-256 `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32` |

Os caminhos de classes acima são relativos a `com/github/alexmodguy/alexscaves/server/`: item em `item/OrtholanceItem.class`, entidade em `entity/item/WaveEntity.class` e registro em `enchantment/ACEnchantmentRegistry.class`.

**Texto literal do publisher `en_us`:** “Flinging”; “Ortholance launch moves the player much further”. Não há chave própria de Flinging no `pt_br.json` examinado. São texto funcional e parâmetro de localização; não substituem a fórmula compilada nem comprovam distância física. `en_us.json` tem SHA-256 `a2a3fab567b07ec10b3d946d4e4ce3e65417b6f9348bd49478d8a253a4232d1f`; `pt_br.json`, `080bfaf05b6d710383579dfd0d3c01443f9fa873b0c697f5e6ee0740931018a7`.

**Prova atual:** [manifesto causal SHA-exato](../EXACT-FLINGING-CAUSAL-1.0.10.json), [reprodução e limites](../EXACT-FLINGING-CAUSAL-1.0.10.md), [auditor causal](../../../../../docs/qa/alexscaves_1010_flinging_causal_audit.py) e [workflow dedicado](../../../../../.github/workflows/alexscaves-1010-flinging-causal.yml). O [manifesto anterior de janelas](../EXACT-FLINGING-1.0.10.json), sua [sonda](../../../../../docs/qa/alexscaves_1010_flinging_probe.py), [testes](../../../../../docs/qa/alexscaves_1010_flinging_probe_test.py) e [workflow](../../../../../.github/workflows/alexscaves-1010-flinging.yml) conservam seus bytes e seu escopo histórico limitado.

A fonte pública adjacente [Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37](https://github.com/Codx-org/AlexsCavesContinued/tree/523308608422ab8e31974befa7111ecdf495dd37) declara **1.1.1**. Ela serve para localizar candidatos de pesquisa; os números e fluxos desta ficha vêm do binário **1.0.10**, sem pressupor paridade.

## 2. JSON, aquisição e compatibilidade

| Campo | Valor publisher | Significado |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.flinging` | Identidade da localização |
| `supported_items` | `#alexscaves:enchantable/ortholance` | Suporte declarativo à Ortholance |
| `weight` | `10` | Peso de aquisição; não chance de impulso, spawn ou hit |
| `max_level` | `3` | Níveis I–III declarados |
| `min_cost` | base `1`, incremento `8` | `1+8×(L−1)`; I/II/III: **1/9/17** |
| `max_cost` | base `41`, incremento `10` | `41+10×(L−1)`; I/II/III: **41/51/61** |
| `anvil_cost` | `1` | Custo de encantamento, não desgaste ou mana do lançamento |
| `slots` | `["mainhand"]` | Slot declarado no recurso |
| `effects` / `exclusive_set` | Ausentes neste JSON | A mecânica está no código Java; ausência local não prova compatibilidade global |

As quatro tags empacotadas `minecraft:in_enchanting_table`, `minecraft:non_treasure`, `minecraft:on_random_loot` e `minecraft:tradeable` incluem o ID; cada arquivo tem **1.631 bytes**, SHA-256 `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1`. A inspeção dos **51 JSONs** de encantamento não encontrou exclusão reversa referenciando `alexscaves:flinging`. Isso descreve dados empacotados; não certifica datapacks efetivos, aquisição final ou compatibilidade do modpack.

`ACCompat.enchantLevel(stack,key)`, `(ItemStack,ResourceKey)I`, percorre `stack.getEnchantments().entrySet()`, compara o holder à chave e retorna o primeiro nível correspondente, ou zero. **Não aplica clamp próprio ao máximo III, nem valida slot, tag, jogador ou lado nesse helper.** No release o nível é capturado da stack passada ao callback, uma vez para Flinging; não é relido para cada onda/vítima. Não presumir que níveis externos sejam limitados a 3 ou usar a mera existência do reader como hook mutador seguro.

## 3. Uso, carga e impulso solicitado

`OrtholanceItem.use(Level,Player,InteractionHand)` tem **20 instruções**. Obtém a stack da mão solicitada e retorna fail quando **`damageValue>=maxDamage−1`** (`@9–27`); caso contrário pede **`startUsingItem(hand)@30`** e retorna `ACCompat.useConsume(stack)`. O corpo não testa o nível de Flinging nem força somente a mão principal: o slot declarativo e o caminho de execução são contratos distintos.

`getUseAnimation` retorna **BOW**; `getUseDuration(ItemStack,LivingEntity)I` retorna **72.000 ticks** em duas instruções. Esse teto de sessão não é a carga máxima efetiva do lançamento. O produtor de Flinging é:

```text
OrtholanceItem.releaseUsing(ItemStack,Level,LivingEntity,int)V
435 instruções JVM, offsets 0–869
parsed_method_sha256 = 00705e7177cb6fe2914531158bd978b64d497ca4c8262f8e7634c1b4ec9ef7ae
```

Definindo `R` como tempo **restante** recebido, `C` como carga, `F` como nível de Flinging, `D` como movimento anterior e `U` como vetor de visão normalizado:

```text
C = clamp(72000 − R, 0, 60)                       // @0–15
F = enchantLevel(stack, FLINGING)                 // @17–24
T = enchantLevel(stack, TSUNAMI) > 0              // @26–41
se C <= 0: retornar                              // @43–45 →869
P = 0.1F×C + 0.1F×F                              // @48–61
U = normalize(usuário.getViewVector(1F))
V = D + U.multiply((double)P, (double)(P×0.15F), (double)P)
                                                     // @63–93
```

`0.1F` e `0.15F` são constantes float; os produtos e a soma de `P` têm arredondamento float antes das conversões double. `V` já inclui o movimento anterior. Ele não é um vetor unitário, um deslocamento realmente percorrido ou a velocidade final ainda acrescida da parcela vertical.

| Nível F | Parcela adicional em P | Parcela vertical final própria |
|---:|---:|---:|
| 0 | `0` | `0` |
| I | `+0.1F` | `+0.1F` |
| II | `+0.2F` nominal | `+0.2F` nominal |
| III | `+0.3F` nominal | `+0.3F` nominal |

Ao final do callback, `@836–866` solicita:

```text
setDeltaMovement(V + (0, (onGround ? 0.2F : 0F) + 0.1F×F, 0))
```

A soma vertical é feita em float e convertida a double. O termo de solo depende de `onGround()` chamado **no final**, não de um snapshot anterior ao processamento das ondas e vítimas. Esse pedido substitui o delta por um vetor formado a partir de `D` capturado em `@64`; não refaz a leitura do movimento depois dos callbacks de dano.

**Gates separados:** `C<10@99` e `level.isClientSide()@106` saltam diretamente para **`@836`**. Portanto cargas positivas **1–9** e chamadas cliente ainda podem pedir esse movimento, embora pulem som, desgaste, ondas e ataque direto. **C=0** retorna sem pedir movimento. O release aceita `LivingEntity`, não exige `Player` em seu próprio corpo; o uso normal de item passa por `use(Player,hand)`, sob autoridade da engine.

Flinging não fornece distância final em blocos, tempo de voo, imunidade a queda, alcance de raycast ou efeito “alvo/área” próprio. Gravidade, arrasto, colisões, velocidade anterior, direção de visão, engine e intervenções de outros mods decidem o deslocamento físico.

## 4. Ramo servidor: custo, ondas e influência indireta do vetor

Somente **`C>=10 && !level.isClientSide()`** entra no bloco **`@109–833`**. Ele toca o som da Ortholance com volume solicitado `4F`, pitch `1F`, categoria NEUTRAL e solicita **um desgaste de 1** em `ACCompat.hurtAndBreakUsedHand(stack,1,usuário)@135`, antes de escolher o ramo de ondas.

O wrapper de desgaste obtém `usuário.getUsedItemHand`, converte MAIN_HAND em MAINHAND e a outra mão em OFFHAND, e chama `ItemStack.hurtAndBreak`. Não possui guarda creative própria; a engine liquida o desgaste real. Não é uma segunda cobrança de Flinging nem um débito por onda ou vítima. Uma falha/recusa de inserção de entidade não introduz reembolso nesse fluxo.

### 4.1. Ramo normal e Second Wave

`B=C/5` é divisão inteira (`@138–142`), de **2 a 12** nas cargas elegíveis. Sem Tsunami, o laço `i=0..B−1` (`@247–456`) calcula:

```text
q = (float)i / (float)B
lifespan = 3 + trunc((1F−q)×3F)
Q = usuário.position() + V.scale((double)(q×2F))
yawBase = −float(atan2(V.x,V.z)×57.2957763671875D)
```

Por iteração, tenta duas ondas (`@371` e `@449`) na posição **`(Q.x, usuário.y, Q.z)`**, com lifespan calculado e yaws **`yawBase+60F−15F×i`** / **`yawBase−60F+15F×i`**. A posição vertical não recebe `V.y`. O produtor não copia `V` como delta da onda; `V` participa das posições e do heading. As duas ondas usam escala/espera basais da entidade, **1F/0**, que não são amplificadas diretamente por Flinging.

Depois desse laço, se `enchantLevel(stack,SECOND_WAVE)>0@459–466`, executa outro laço com **`N=max(1,B−1)`**, duas tentativas por iteração, a mesma construção com `q=i/N`, mas com **`waitingTicks=8`** (`@604/@689`). A [ficha Second Wave](second-wave.md) e sua [prova estática](../EXACT-SECOND-WAVE-STATIC-1.0.10.md) conservam o escopo próprio. São, nominalmente, **`2B`** pedidos no primeiro laço e **`2×max(1,B−1)`** adicionais quando esse ramo é alcançado e elegível, sem garantia de spawn ou hit aceito.

### 4.2. Tsunami e desvio do segundo laço

Com `T=true`, `@149–150` sobrescreve **B para 5** e o produtor tenta **uma onda** em **`(posição+V).x, usuário.y, (posição+V).z`**, com **lifespan 20**, **waveScale 5F**, **waitingTicks 2** e heading horizontal de V. O **`goto@244→705`** pula os dois laços normais e a leitura de Second Wave. Stacks forçadas contendo ambos não transformam esse salto em execução do segundo ramo.

O JSON de **Second Wave** declara exclusividade com Tsunami. Flinging apenas participa do vetor usado por esses ramos; não é o seletor de nenhum deles. A [ficha Tsunami](tsunami.md), o [manifesto individual](../EXACT-TSUNAMI-CONTRACT-1.0.10.json) e a [prova anterior](../EXACT-TSUNAMI-CONTRACT-1.0.10.md) permanecem imutáveis.

Todos os `addFreshEntity` desse release descartam o booleano de retorno. Tentativa de emissão, inserção aceita, sobrevivência, impacto, dano e kill/Mastery não são estados equivalentes. As ondas seguem o lifecycle nativo do provider, sem criar outro cast deliberado de jogador.

## 5. Geometria completa do ataque direto e dano

O bloco **`@705–735`** constrói precisamente:

```text
caixaDireta = AABB(usuário.position(), usuário.position() + V.scale((double)B)).inflate(1D)
B = C/5 no ramo normal; B = 5 no ramo Tsunami
```

A ligação é **`iload 10@719 → i2d@721 → Vec3.scale(D)@722`**. Não existe um alcance fixo de 3 blocos nesse argumento. O endpoint usa **V intermediário**, anterior à parcela vertical final de `setDeltaMovement`, e ambas as posições são consultadas na fase do ataque, depois das tentativas de ondas. Trata-se de uma caixa alinhada aos eixos entre dois pontos e inflada por 1 em cada direção; não é raio esférico, hitbox da onda, volume varrido com colisões ou prova de caminho realmente percorrido.

A consulta é **`level.getEntitiesOfClass(LivingEntity.class,caixaDireta)@758`**. O laço exclui aliados (`usuário.isAlliedTo@793`) e o próprio usuário (`equals@802`), e exige **`usuário.hasLineOfSight@811`**. Nesse ataque direto não há filtro próprio de Deep One equivalente ao consumidor de ondas, nem homing, escolha do mais próximo ou identificação única de alvo principal; isso não autoriza dano a alvos protegidos pela engine.

O produtor constrói **`mobAttack(usuário)@742`** e lê uma vez **`ACCompat.attackDamageBonus(stack)@748`**. Para cada candidato elegível pede `hurt(fonte,(float)bônus)@824`, **descarta o booleano em `@827`** e pede **`stopRiding()@830`** em seguida. O pedido de desmontar não é condicionado ao retorno de `hurt`; não é knockback nem recibo de dano/kill.

`ACCompat.attackDamageBonus` soma os `amount()` dos modificadores de `ATTACK_DAMAGE` vistos em **MAINHAND**, pela lambda `lambda$attackDamageBonus$2`. O helper não soma ali o atributo base do usuário nem interpreta integralmente as operações da engine. O construtor da Ortholance declara modificadores basais **+5D de ataque** e **−2.4000000953674316D de velocidade de ataque**, em `acModifiers` para MAINHAND; isso não prova dano final universal de 5 HP. **Flinging não multiplica esse argumento de dano nem troca a DamageSource no release**: sua influência direta é no movimento, com consequência indireta em posições/caixa.

O corpo completo selecionado não adiciona neste laço deduplicação persistente, recibo de hit, registro de kill ou prêmio de Mastery. Integrar progressão exige comprovar resultado aceito e autoria no boundary real, sem usar contagem de ondas ou chamadas `hurt` como crédito.

## 6. Ondas: tempo, área, autoria e persistência

Os consumidores nativos são compartilhados com as provas SHA-exatas de [Sea Swing](../EXACT-SEA-SWING-STATIC-1.0.10.md), [Second Wave](../EXACT-SECOND-WAVE-STATIC-1.0.10.md) e [Tsunami](../EXACT-TSUNAMI-CONTRACT-1.0.10.md), no mesmo classfile. O manifesto causal de Flinging explicita sua cobertura atual; não reclassifica as janelas históricas como corpos integrais.

- **Defaults sincronizados:** `SLAMMING=false`, `LIFESPAN=10`, `WAITING_TICKS=0`, `Y_ROT=0F`, `WAVE_SCALE=1F`. O produtor sobrescreve lifespan nos ramos normais e escala/espera/lifespan em Tsunami. Escala da onda não é nível de Flinging; os getters/setters não são hooks seguros por existirem.
- **Dimensões:** a factory de Wave declara base **0.9F×0.9F**, conforme o registro em `ACEntityRegistry` selado no [contrato Tsunami reutilizado](../EXACT-TSUNAMI-CONTRACT-1.0.10.json); `getDimensions(Pose)` aplica `getWaveScale` e a mudança sincronizada de escala pede `refreshDimensions`. A consulta de dano usa a **AABB corrente própria inflada por 0.5D em cada eixo**, diferente da caixa direta de lançamento. Escala 5 tem dimensões nominais básicas 4.5×4.5, não raio 5 ou alcance final.
- **Dano da onda:** `attackEntities(S)` consulta `LivingEntity`, exclui aliados à onda, `DeepOneBaseEntity` e, quando owner não é null, o owner e seus aliados. Pede **`hurt(mobProjectile(onda,campo owner),S+1F)`**, descarta o booleano, pede **`setSlamming(true)`** e depois knockback de magnitude solicitada **`0.1D+0.5D×S`**, com direção derivada do yaw. Seu corpo não testa LOS nem guarda dedupe próprio por vítima. Os filtros e a fonte são diferentes do ataque direto da Ortholance.
- **Argumento S:** o tick passa **`2F×getSlamAmount(1F)+1F+waveScale`**. O interpolante de slam deriva de progresso anterior/atual multiplicado por 0.1F. Com escala basal 1, dano nominal pedido é **`3+2A`** e knockback **`1.1+A`**; com Tsunami 5, **`7+2A`** e **`3.1+A`**, respectivamente, chamando o interpolante de A. Flinging não entra nessas fórmulas. Nenhuma delas prova HP perdido, DPS ou deslocamento de knockback.
- **Tempo e movimento:** espera positiva retorna cedo em ambos os lados, mas é decrementada somente no servidor. Fora dela, o tick governa slam, gravidade, aceleração própria pelo yaw, movimento e descarte; chama `attackEntities` somente no servidor. `activeWaveTicks>lifespan`, baixa velocidade horizontal após 10 ticks e ataques podem pedir slam. Lifespan não é instante fixo de descarte ou duração garantida de dano; durante slam não há uma trava local que proíba novas consultas de vítimas.
- **Autoria inicial:** `WaveEntity(Level,LivingEntity)` chama `setOwner`, que grava o objeto owner e UUID. `getOwner()` pode resolver UUID em ServerLevel; **`attackEntities` usa diretamente o campo owner**, sem chamar o getter. A existência do resolvedor não prova reidratação automática antes do dano após reload.
- **NBT próprio:** overrides `readAdditionalSaveData`/`addAdditionalSaveData` não chamam super e leem/gravam diretamente somente **Owner UUID, quando existe, e Lifespan**. Não serializam ali escala, espera, yaw sincronizado, progresso de slam, contador ativo, nível Flinging ou identidade do ramo. Persistência herdada da engine e sincronização de runtime são fronteiras diferentes; não presumir conservação de atraso/escala/autoria física após load.

Flinging não grava estado próprio por cast no item nesses corpos; usa o nível da stack no release e pedidos de movimento sobre a entidade viva. Não há pacote de rede, handshake de casting, receipt ou replay guard próprio do encantamento demonstrado por esses consumidores. A engine controla dispatch do uso, sincronização de movimento, colisões, proteção e resultado das chamadas; a inspeção não homologa seu uso multiplayer por um adapter externo.

## 7. Contratos úteis para perks e sistemas

| Eixo / intenção | Contrato documentado | Fronteira de integração |
|---|---|---|
| Identidade / nível / alvo | Encantamento de Ortholance, I–III declarados, nível capturado da stack; movimento é do usuário | Não transformar em spell target/área independente ou aplicar reader fora do boundary do item |
| Impulso / altura | P=`0.1C+0.1F`; multiplicação por `(P,0.15P,P)` e parcela vertical final própria | `NOT_VERIFIED`: preservar ordem, float/double, movimento anterior e gate de solo; sem hook mutador aprovado |
| Alcance / targeting | Caixa direta de posição a posição+V×B, inflada1; LOS, aliado e self; nenhuma distância final em blocos certificada | Não converter P ou B em raio universal nem atravessar claims/colisões |
| Ondas / quantidade / tamanho | `2B` tentativas normais; ramo Second Wave e onda Tsunami têm contratos próprios; dimensão da entidade usa escala | Não reemitir entidades, copiar runtime, amplificar procs por onda/tick ou atribuir nível Flinging à escala |
| Dano / tipo / empurrão | Direto `mobAttack` + `attackDamageBonus`, onda `mobProjectile`; retorno de hurt descartado; stopRiding e knockback separados | Não criar segundo hurt, trocar fonte ou afirmar hit aceito sem settlement nativo |
| Tempo / cooldown | Uso72.000, carga clamp60, gates10, espera/lifespan/slam independentes | Nenhum cooldown próprio solicitado no release selecionado; isso não prova ausência global de cooldown/eventos |
| Custos / recursos | Desgaste1 por release elegível em servidor; custos de enchanting são outro sistema | Sem mana/stamina/XP/munição próprios nos consumidores selecionados; N/A local, não promessa de custo global zero |
| Cura / status / mundo | **N/A próprios:** não há no efeito de movimento um pedido de cura, status, conversão elemental, criação/remoção de blocos ou familiar | Reações da engine e de outros mods preservam autoridade; não inventar parâmetros ausentes |
| Persistência / autoria | Nível capturado no release; owner inicial explícito da onda e NBT próprio delimitado | Não preencher reload com owner paralelo, relançamento compensatório, reembolso ou reexecução de dano |
| Mastery / progressão | Uso, movimento, ataque direto e ondas pertencem à mesma ação raiz | Crédito somente após resultado autorizado e autoria demonstrada, com deduplicação no sistema dono |
| Hook / execução | Classes, campos, métodos e setters são superfícies identificadas | **`NOT_VERIFIED`, `NO_MUTATION`**; nenhuma API/hook seguro ou perk executável homologada |

Black Arcana governa seu runtime mágico e world safety; Alex's Caves conserva a liberação, movimento, ondas, dano e liquidação nativos. RPG Skill Tree fornece progressão/perks/atributos/Mastery por boundary real; Enshrouded conserva seus próprios sistemas. A ficha oferece parâmetros e limites para design, sem transferir autoridade ou criar adapter imaginário. Cada modificador exige implementação no projeto dono e testes do modpack.

## 8. Certificação estática, reprodução e QA pendente

Os sete eixos da [rubrica](../../../meta/PERK-READY-CERTIFICATION-RULES.md) estão documentados: **identidade, comportamento, parâmetros, targeting, custos, integração e validação**. O [manifesto causal atual](../EXACT-FLINGING-CAUSAL-1.0.10.json) liga recursos e classes SHA-exatos aos métodos nativos; a [prova](../EXACT-FLINGING-CAUSAL-1.0.10.md) registra reprodução, seleções, branches e limites. O auditor lê o JAR, não executa o combate. Um digest integral comprova identidade do corpo extraído, não a aceitação física das chamadas.

A certificação conclui o contrato técnico estático individual de Flinging. Não transforma os estados históricos `PARTIAL` de manifestos anteriores em aprovações integrais; não fecha a Ortholance inteira, todos os comportamentos externos ou o universo do provider. Os testes verificam coerência/fidelidade estática e rejeitam evidências alteradas; não constituem servidor real com todo o modpack e hooks mutadores.

**QA física pendente:** níveis0/I/II/III e externos; carga0/1/9/10/60, ambas as mãos e gate de durabilidade; solo/ar/água e movimento prévio, olhar zero/vertical, colisões e quedas; cliente/dedicado, latência, FPS/TPS, cancelamento e troca de slot; bloqueio de spawn e de dano, stopRiding com hurt recusado, LOS/aliados/Deep One e entidades montadas; Tsunami/Second Wave forçados sem redefinir sua compatibilidade; comparação entre caixa direta e volume das ondas, repetição de candidatos e invulnerabilidade; espera, lifespan, slam e descarte; save/reload, unload, mudança de dimensão e owner órfão; PvP, claims, datapacks e intervenções de outros mods; autoria e crédito único de XP/Mastery após resultados aceitos.

**Contabilidade delimitada:** **+1 contrato técnico estático certificado**, **+0 fichas novas**, **+0 raízes mágicas**, **+0 hooks mutadores homologados**, **+0 providers encerrados**, **+0 promoção de Stage**. As contagens vigentes pertencem aos índices gerados. Próxima ficha parcial alfabética: **`alexscaves:gamma_ray`**.
