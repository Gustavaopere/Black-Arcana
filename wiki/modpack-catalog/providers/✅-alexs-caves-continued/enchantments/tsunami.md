# Tsunami — `alexscaves:tsunami` (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Integração:** `NO_MUTATION`. O recorte conclui este encantamento, seu ramo de liberação da Ortholance e os consumidores nativos selecionados da onda. `OrtholanceItem.releaseUsing` e `WaveEntity.tick` permanecem **PARTIAL**; não se concluem a arma integral, o tick/CFG integral da entidade, a aceitação de spawn/dano pela engine ou o provider integral.

## 1. Identidade e proveniência

- **Provider / versão:** Alex's Caves Continued / `alexscaves`, Minecraft 1.21.1, NeoForge, Java 21; `alexscaves-1.0.10-neoforge+1.21.1.jar`, [CurseForge projeto `1645389`, arquivo `8856293`](https://www.curseforge.com/minecraft/mc-mods/alexs-caves-continued/files/8856293), **75.279.314 bytes**.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Identidade / natureza:** `alexscaves:tsunami`, campo `ACEnchantmentRegistry.TSUNAMI`; encantamento de equipamento que seleciona uma onda grande no lançamento nativo da Ortholance. Não é spell independente ou nova escola elemental.
- **Recurso:** `data/alexscaves/enchantment/tsunami.json`, **358 bytes**, SHA-256 `37f1f8c3f8b98084b73b23aa2ec49ba9a925bb9a37089f622cf992234a086242`.
- **Tag de item:** `data/alexscaves/tags/item/enchantable/ortholance.json`, **50 bytes**, SHA-256 `1c96a26e08800182b9c4b3b2f5ba4043389fe1bec0dcd5b12f1e5392cc28a5ac`; contém somente `alexscaves:ortholance`.
- **Nome e descrição literais de `en_us.json`:** “Tsunami”; “Ortholance launch summons a single, gigantic wave”. Paráfrase técnica: a liberação elegível da Ortholance tenta criar uma única onda com escala 5. O texto não comprova inserção aceita, alvo atingido ou dano efetivo. Não há chaves próprias de Tsunami no `pt_br.json` examinado.
- **Produtor:** `com/github/alexmodguy/alexscaves/server/item/OrtholanceItem.class`, **13.850 bytes**, SHA-256 `996b208a60f2c26c275e60e5d0e3a2fd0090cfb0ba1687907cac242de9a17d09`.
- **Consumidor:** `com/github/alexmodguy/alexscaves/server/entity/item/WaveEntity.class`, **13.491 bytes**, SHA-256 `93fdaee0239cc4985b351a6c2ac1edd23a51cf0088cb1172f983d0f869d9e42e`.
- **Provas:** [manifesto individual](../EXACT-TSUNAMI-CONTRACT-1.0.10.json), [reprodução](../EXACT-TSUNAMI-CONTRACT-1.0.10.md), [auditoria comum com perfil `tsunami`](../../../../../docs/qa/alexscaves_1010_action_contract_audit.py) e [regressões semânticas](../../../../../docs/qa/alexscaves_1010_tsunami_cards_test.py).

A varredura dos **1.555 classfiles** do publisher por CP `Fieldref` exato, owner `ACEnchantmentRegistry`, nome `TSUNAMI` e descriptor `Lnet/minecraft/resources/ResourceKey;`, encontra somente `ACEnchantmentRegistry.class` e `OrtholanceItem.class`. O registro liga literal `tsunami` em `<clinit>@239`, chamada `key@242` e `putstatic TSUNAMI@245`; a classe tem SHA-256 `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32`. Referências diretas não inventariam reflexão, transformações ou consumidores externos.

`assets/alexscaves/lang/en_us.json` tem **121.372 bytes**, SHA-256 `a2a3fab567b07ec10b3d946d4e4ce3e65417b6f9348bd49478d8a253a4232d1f`; `pt_br.json` tem **84.238 bytes**, SHA-256 `080bfaf05b6d710383579dfd0d3c01443f9fa873b0c697f5e6ee0740931018a7`. A [fonte pública adjacente pinada](https://github.com/Codx-org/AlexsCavesContinued/tree/523308608422ab8e31974befa7111ecdf495dd37) declara **1.1.1** e serve apenas de corroboração; não é autoridade numérica nem prova de paridade do binário **1.0.10**.

## 2. JSON, aquisição e compatibilidade

| Campo | Valor publisher 1.0.10 | Significado / limite |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.tsunami` | Identidade da tradução |
| `supported_items` | `#alexscaves:enchantable/ortholance` | Elegibilidade declarada do item |
| `weight` | `1` | Peso declarativo; não é chance de spawn ou hit |
| `max_level` | `1` | Apenas I publicado |
| `min_cost` | base `1`, incremento `20` | `1+20(L−1)`; I: 1 |
| `max_cost` | base `41`, incremento `10` | `41+10(L−1)`; I: 41 |
| `anvil_cost` | `8` | Aquisição; não é custo de liberação |
| `slots` | `mainhand` | Slot declarado; não é revalidação própria em cada tick |
| `effects` / `exclusive_set` | Ausentes neste JSON | Comportamento Java; ausência local não prova compatibilidade global |

As tags empacotadas `minecraft:in_enchanting_table`, `minecraft:non_treasure`, `minecraft:on_random_loot` e `minecraft:tradeable` incluem o ID. Cada recurso tem **1.631 bytes**, SHA-256 `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1`. Entre os **51 JSONs de encantamento**, somente `second_wave.json` declara exclusão reversa com `alexscaves:tsunami`: **413 bytes**, SHA-256 `68d843242cc39b33eb952142b168fa8e72a2695bfa8adea6de3e4bba6febb97c`. Respeitar essa exclusão; stacks forçadas não certificam compatibilidade.

A enumeração de caminhos `data/alexscaves/recipe/` não encontrou nome contendo `ortholance` ou `tsunami`; não é prova global de impossibilidade de obtenção. `data/alexscaves/loot_table/gameplay/deep_one_knight_barter.json`, **6.197 bytes**, SHA-256 `57c4a14e6a92f963e726ed92136034a091bdf8929398e8ba2b9d94a6c302c818`, contém o **item Ortholance com weight 10**, sem função de encantamento naquela entrada. Não promete Tsunami na stack. Obtenção, compatibilidade e recursos efetivos permanecem dependentes dos datapacks/modlist carregados.

`ACCompat.enchantLevel` retorna o primeiro nível correspondente da stack ou zero, sem clamp próprio ao máximo I nem validação própria de slot/tag. Os gates de aquisição são diferentes desse reader de execução.

## 3. Liberação: carga, nível, custo e onda única

O produtor real é `OrtholanceItem.releaseUsing(ItemStack,Level,LivingEntity,int)V`, **435 instruções**, offsets `0–869`. O argumento inteiro é o tempo **restante** de uso. `getUseDuration(ItemStack,LivingEntity)I`, **2 instruções**, retorna **72.000 ticks**, enquanto o release limita a carga:

```text
C = clamp(72000 − remainingUseTicks, 0, 60)
F = enchantLevel(stack, FLINGING)
T = enchantLevel(stack, TSUNAMI) > 0
P = 0.1F×C + 0.1F×F
V = movimentoAtualDoUsuário
    + normalize(viewVector(1F)).multiply((double)P, (double)(P×0.15F), (double)P)
```

`C@0–15`, `F@17–24` e `T@26–41` são capturados antes do retorno para **`C<=0`** em `@43–45`. `P` e `V` só são calculados com carga positiva, em `@48–93`, com arredondamentos float/double nativos. O nível Tsunami vira apenas um booleano:

| Nível lido no release | Flag `T` | Consequência no ramo elegível |
|---|---|---|
| 0 ou não positivo | false | Segue o ramo normal, fora do recorte individual Tsunami |
| I | true | Uma tentativa de onda com escala 5 |
| Nível externo positivo acima de I | true | Mesmo ramo; sem escala ou chance adicional por nível |

São valores capturados no release; a onda não relê o encantamento da stack. Flinging altera `V`, que incorpora movimento anterior e inclinação do olhar; Tsunami não introduz um multiplicador próprio em `P`. `V` não é vetor unitário, distância final, raio de efeito ou velocidade inicial copiada à onda.

**Gates distintos:** somente **`C>=10 && !level.isClientSide()`**, em `@95–106`, entra no bloco de som, desgaste, emissão e ataque direto. Cargas positivas de **1–9** e chamadas cliente saltam para `@836`, onde ainda podem pedir movimento ao usuário. Não ampliar a guarda servidor a toda a rotina.

O bloco elegível toca o som nativo e pede **um ponto de desgaste** por `ACCompat.hurtAndBreakUsedHand(stack,1,usuário)@135`, antes da escolha Tsunami. `@138–142` inicia `B=C/5` inteiro; o ramo `T` substitui por **`B=5@149–150`** e executa:

```text
Q = usuário.position() + V
onda = new WaveEntity(level, usuário)
onda.position = (Q.x, usuário.y, Q.z)
onda.lifespan = 20
onda.waveScale = 5F
onda.waitingTicks = 2
onda.yaw = −float(atan2(V.x,V.z) × 57.2957763671875D)
level.addFreshEntity(onda)   // retorno booleano descartado
goto @705
```

O construtor é chamado em `@163–169`; posição em `@174–190`, lifespan em `@193–197`, escala em `@200–204`, espera em `@207–210`, yaw em `@213–234` e tentativa de spawn em `@237–243`. A origem horizontal usa `posição+V`; **Y é o do usuário**, sem `V.y`. O yaw usa o heading horizontal de `V`, incluindo o movimento prévio, e não somente a rotação/visão do usuário. O produtor **não chama `setDeltaMovement` na onda**. Movimento zero/vertical, colisões e offsets físicos exigem QA da engine.

Há **uma tentativa de spawn**; `addFreshEntity@240` tem retorno descartado por `pop@243`. Não comprova inserção aceita, sobrevivência, um único alvo ou um único dano. **`goto@244→705` pula os dois laços normais e o reader/ramo Second Wave `@247–702`.** Mesmo com ambos os níveis forçados, este caminho Tsunami não consulta `SECOND_WAVE`. Não aplicar a ele a fórmula de quantidade do ramo Second Wave, nem transformar o teste forçado em compatibilidade homologada. A [ficha Second Wave](second-wave.md) conserva seu escopo anterior.

## 4. Ataque direto e movimento do usuário

O salto alcança o ataque direto em `releaseUsing@705–833`, ainda sob **C>=10/servidor**. Sua geometria é:

```text
caixaDireta = AABB(usuário.position(), usuário.position() + V×B).inflate(1D)
com Tsunami: B = 5
```

É uma caixa alinhada aos eixos, influenciada por carga, Flinging, visão e movimento anterior. Não é raio fixo de Tsunami, volume da onda ou prova de sweep ao longo do deslocamento. O método consulta `LivingEntity` nessa caixa, exclui o próprio usuário e aliados segundo `usuário.isAlliedTo(vítima)` e exige `usuário.hasLineOfSight(vítima)`.

A fonte direta é **`mobAttack(usuário)`**; o valor pedido é **`(float)ACCompat.attackDamageBonus(stack)`**. O helper e sua lambda somam quantidades dos modificadores `ATTACK_DAMAGE` encontrados em MAINHAND; não somam ali o atributo base do usuário nem executam uma interpretação completa das operações de atributos da engine. O construtor da Ortholance declara ataque **+5D** e velocidade de ataque **−2.4000000953674316D** em MAINHAND, mas isso não torna todo pedido direto universalmente 5 HP nem constitui dano adicional por nível Tsunami.

`hurt@824` tem resultado descartado em `@827`; em seguida solicita **`stopRiding@830`**. Um dano recusado não bloqueia esse pedido de desmontar. O método não utiliza o retorno como recibo de hit ou kill/Mastery. Não confundir desmontagem direta com o knockback próprio da onda.

Depois, `@836–866` solicita movimento ao usuário:

```text
setDeltaMovement(V + (0, (onGround ? 0.2F : 0F) + 0.1F×F, 0))
```

Esse caminho também ocorre para cargas positivas menores que 10 e chamadas cliente, sem passar por desgaste, onda ou ataque direto. A distância percorrida depende da engine e do modpack. Liberação, dano direto, onda e movimento são fases nativas; não são quatro casts ou quatro cobranças.

## 5. Onda: geometria, targeting e dano solicitado

`WaveEntity.defineSynchedData`, **31 instruções**, define **`SLAMMING=false`, `LIFESPAN=10`, `WAITING_TICKS=0`, `Y_ROT=0F`, `WAVE_SCALE=1F`**. Tsunami sobrescreve lifespan/espera/escala para **20/2/5**. Getters/setters sincronizados têm **7 instruções cada**, sem clamp próprio de nível, slot ou tag; existência de setter não é hook mutador seguro.

O registro `ACEntityRegistry.WAVE` liga a supplier `lambda$static$47`, cuja factory aponta ao construtor `WaveEntity(EntityType,Level)`. Declara dimensões básicas **`0.9F×0.9F`**, atualização de velocidade habilitada e intervalo de atualização **1**. `getDimensions(Pose)`, **7 instruções**, escala as dimensões herdadas por `getWaveScale`; `onSyncedDataUpdated`, **10 instruções**, pede `refreshDimensions` quando muda `WAVE_SCALE` e depois chama super. Com escala 5, as dimensões nominais básicas tornam-se **4.5F×4.5F**; AABB corrente e colisões físicas permanecem sob autoridade da engine. Não é esfera com raio 5 ou alcance máximo.

`WaveEntity.attackEntities(float S)V`, **81 instruções**, consulta `LivingEntity` na **AABB corrente própria inflada em `(0.5D,0.5D,0.5D)`**. A fonte é **`mobProjectile(onda,campo owner)`**, sem DamageType próprio de Tsunami. Exclui aliados à onda, `DeepOneBaseEntity` e, se o campo owner não for null, o próprio owner e seus aliados. O corpo não testa LOS, não mantém deduplicação de vítimas e não usa resultados anteriores de dano. Os filtros, fonte e volume diferem do ataque direto da arma.

Por candidato elegível, a ordem é:

1. Pede **`hurt(source,S+1F)@123`** e descarta o booleano em **`@126`**.
2. Pede **`setSlamming(true)@129`**; isso não interrompe o laço de vítimas.
3. Pede **`ACCompat.knockback(vítima,0.1D+0.5D×(double)S,sin(yaw×0.017453292F),−cos(yaw×0.017453292F))@169`**. O helper delega a `LivingEntity.knockback`; magnitude solicitada não é deslocamento observado.

`hurt=false` não bloqueia slam ou knockback. Nenhum desses pedidos comprova hit aceito, dano, empurrão, kill ou crédito único.

O tick passa **`S=2F×getSlamAmount(1F)+1F+getWaveScale()`**. `getSlamAmount(partialTicks)`, **13 instruções**, calcula **`(prevSlamProgress+(slamProgress−prevSlamProgress)×partialTicks)×0.1F`**. Mantida a escala Tsunami 5 e chamando esse interpolante de `A`, os valores nominais são:

| Parâmetro | Fórmula nominal, sujeita aos arredondamentos nativos |
|---|---|
| Argumento `S` de `attackEntities` | `6+2A` |
| Dano bruto pedido por candidato | **`7+2A`** |
| Magnitude de knockback pedida | **`3.1+A`** |

O progresso próprio sobe até 10, correspondendo ao interpolante nominal de 0 a 1. A fórmula não é DPS, perda final de HP, frequência de hits aceitos ou garantia de ataque único. Não há trava própria que impeça novas consultas durante slam; invulnerabilidade, defesas, eventos, remoção e hooks externos conservam autoridade sobre os resultados.

## 6. Tempo, movimento, recursos, owner e NBT

O `tick()V` da onda tem **318 instruções**, offsets `0–619`, com seleção **PARTIAL** declarada abaixo. As janelas selam estas transições:

- Chama supertick e captura progresso anterior. **Espera positiva retorna cedo em ambos os lados**; somente no servidor decrementa `WAITING_TICKS`. Pede invisibilidade e retorna inclusive no tick que reduz a espera a zero (`@12–44`). **Espera 2** é um parâmetro em ticks da entidade, não cooldown ou latência física garantida de dano.
- Fora da espera, remove invisibilidade. Se slamming e progresso menor que 10, incrementa o progresso; se slamming e progresso igual a 10, pede **discard@102**. Não há retorno explícito imediatamente após discard; não presumir que o restante desse callback deixa de executar.
- Quando não `isNoGravity` e fora de água/bolha, soma gravidade **`−0.03999999910593033D`** ao movimento. Calcula **`a=min(activeWaveTicks/10F,1F)`** e aceleração horizontal por **`Vec3(0,0,(double)(a×a×0.2F)).yRot(float(toRadians(−yaw)))`**. Essa aceleração não multiplica por `waveScale`.
- Chama **`attackEntities(S)` somente no servidor**, em `@502–527`, **antes** do move desse trecho. Não comprova hits em toda a trajetória ou sweep físico.
- Solicita **`move(SELF,deltaAtual×0.8999999761581421D+aceleração)`**; depois armazena o vetor solicitado multiplicado por **`(0.9900000095367432D,0.9800000190734863D,0.9900000095367432D)`**. Escala 5 não multiplica automaticamente velocidade, alcance ou distância final.
- Pede slamming quando **`activeWaveTicks>lifespan`** ou **`activeWaveTicks>10 && horizontalDistance(delta)<0.04D`**, em `@570–606`; incrementa o contador ao final. **Lifespan 20** é limiar de pedido de slam, que também pode começar ao atacar. Não é descarte exatamente após 20 ticks ou duração de cast.

`OrtholanceItem.use`, **20 instruções**, retorna fail se **`damageValue>=maxDamage−1`**; caso contrário chama `startUsingItem` e `useConsume`. A supplier de registro da Ortholance, `ACItemRegistry.lambda$static$110`, instancia o item com **durabilidade 340** e **raridade UNCOMMON**. O período de uso, gate de durabilidade, carga, espera, contador ativo e progresso de slam são estados diferentes.

O release solicita **um desgaste de 1**, antes da onda e independentemente do retorno de spawn. O wrapper consulta `getUsedItemHand`, converte a mão em slot e chama `ItemStack.hurtAndBreak`; não há guarda creative própria em `releaseUsing` ou nesse wrapper. A engine decide a liquidação efetiva. Não há cobrança por onda, tick ou vítima. Os consumidores selecionados não pedem munição, mana, stamina, fome, XP ou cooldown próprio; ausência local não comprova custo global zero. `anvil_cost=8` continua aquisição.

**Autoria inicial:** `WaveEntity(Level,LivingEntity)`, **10 instruções**, encadeia o construtor `(EntityType,Level)`, **5 instruções**, e chama **`setOwner@18`**. `setOwner`, **12 instruções**, grava objeto owner e seu UUID. `getOwner`, **27 instruções**, pode resolver `ownerUUID` em `ServerLevel` quando chamado. Porém **`attackEntities` usa diretamente o campo owner, sem chamar esse getter**. O resolvedor existente não comprova reidratação automática de autoria/filtros antes do dano após reload.

`readAdditionalSaveData`, **19 instruções**, e `addAdditionalSaveData`, **14 instruções**, **não chamam super** e leem/gravam diretamente somente **`Owner` UUID, quando existe, e `Lifespan`**. Não serializam ali `WAVE_SCALE`, `WAITING_TICKS`, `Y_ROT`, slamming/progresso, contador ativo, nível Tsunami ou identidade do ramo produtor. Persistência herdada, rotação da engine e sincronização são fronteiras distintas; esses corpos não comprovam perda/restauração física. Não preencher lacunas com estado paralelo, novo owner, reembolso, relançamento compensatório ou reexecução de dano.

## 7. Parâmetros para perks, integração e validação

| Superfície | Contrato individual a preservar |
|---|---|
| Nível / trigger / quantidade | `L>0` no release; `C>=10` e servidor para uma tentativa de onda; sem escala adicional por nível externo positivo |
| Origem / direção / alcance | Horizontal `posição+V`, Y do usuário, yaw do heading de V; alcance final **NÃO VERIFICADO**, sem homing ou busca própria de alvo novo |
| Área / projétil | Escala 5, dimensões nominais 4.5×4.5 e AABB corrente inflada 0.5 por eixo; preservar refresh, colisões e sincronização |
| Dano / tipo / knockback | Onda `mobProjectile(onda,owner)`, pedido `7+2A` e magnitude `3.1+A`; ataque direto separado `mobAttack` com `attackDamageBonus` |
| Tempo / movimento | Carga até 60, espera 2, lifespan 20, slam e aceleração próprios; não são cooldown ou trajetória final garantidos |
| Custo / recursos | Um desgaste solicitado no release elegível; sem segundo débito por onda/vítima nem recibo baseado em retorno descartado |
| Cura / status / mundo | **N/A próprios** nos consumidores selecionados: não introduzem cura, status, conversão elemental ou mutação explícita de blocos; reações da engine conservam autoridade |
| Compatibilidade | Exclusão reversa com Second Wave e salto que ignora seu reader; Flinging afeta V, sem recertificar o encantamento irmão |
| Owner / Mastery | Owner inicial explícito, resolução sob demanda e campo direto no dano; exigir resultado autorizado, autoria demonstrada e crédito único da ação raiz |
| Hook mutador | **`NOT_VERIFIED` / `SEM_HOOK_SEGURO`**; `NO_MUTATION`, sem adapter executável |

Black Arcana mantém seu runtime mágico; Alex's Caves conserva emissão, movimento, dano, custo e liquidação nativos. Enshrouded e RPG Skill Tree podem oferecer progressão/perks apenas por boundary demonstrado no projeto dono. Métodos, campos, setters e callbacks identificados não autorizam mutação segura. Tsunami acrescenta **+0 raízes mágicas novas** às oito existentes; não cria cast independente, segunda cobrança, proc automático por onda/vítima ou promoção de Stage.

O [manifesto individual](../EXACT-TSUNAMI-CONTRACT-1.0.10.json), a [reprodução](../EXACT-TSUNAMI-CONTRACT-1.0.10.md) e os [testes semânticos](../../../../../docs/qa/alexscaves_1010_tsunami_cards_test.py) ligam os sete eixos: **identidade, comportamento, parâmetros, targeting, custos, integração e validação**, segundo a [rubrica estática](../../../meta/PERK-READY-CERTIFICATION-RULES.md). A extração parte do JAR SHA-exato e sela recursos, locale, aquisição, exclusão reversa, Fieldrefs diretos, classes, registro/factories e instruções JVM.

| Método grande | Seleção semântica selada | Limite explícito |
|---|---|---|
| `OrtholanceItem.releaseUsing` | **199 âncoras**: `@0–244` (123) e `@705–869` (76), de **435 instruções** | **PARTIAL**; omite 236 instruções dos ramos normal/Second Wave `@247–702`; o salto `@244→705` está incluído |
| `WaveEntity.tick` | **165 âncoras**: `@0–186` (98) e `@486–619` (67), de **318 instruções** | **PARTIAL**; omite 153 instruções da interpolação/partículas cliente `@189–483` |

Os corpos selecionados completos incluem `use` **20**, `getUseDuration` **2**, construtor Ortholance **30**, construtores Wave **5/10**, `setOwner` **12**, `getOwner` **27**, defaults sincronizados **31**, `getSlamAmount` **13**, `attackEntities` **81**, dimensões **7**, refresh **10**, NBT próprio **19/14**, getters/setters sincronizados e helpers selecionados. Inicializadores grandes de item/entidade conservam janelas delimitadas. Fingerprints integrais não substituem cobertura semântica integral; branches podem sair das janelas. O limite de **256 âncoras por método e 8.192 por manifesto** permanece preservado.

As provas anteriores de [Sea Swing](../EXACT-SEA-SWING-STATIC-1.0.10.json), [Second Wave](../EXACT-SECOND-WAVE-DISCOVERY-1.0.10.json) e [Flinging](../EXACT-FLINGING-1.0.10.json) conservam bytes e escopos. Compartilhar `releaseUsing`/WaveEntity não promove a ficha parcial de Flinging, a Ortholance integral ou os encantamentos irmãos por associação. Uma ficha individual concluída não fecha o universo técnico do provider.

**QA física pendente:** C0/1–9/10/60 e cargas externas; níveis0/I/externos e troca de stack após captura; gate de durabilidade, creative e ambas as mãos; Tsunami/Second Wave forçados verificando o salto, sem redefinir compatibilidade; movimento prévio, heading zero/vertical e coordenada Y; spawn recusado, dimensões e colisões; fontes/volumes/filtros distintos do ataque direto e da onda, LOS e Deep One; `hurt=false` seguido de slam/knockback/stopRiding; candidatos repetidos e invulnerabilidade; espera2, lifespan20, progressos, descarte, água e gravidade; cliente/dedicado, PvP, claims, eventos e datapacks; save/load de escala/espera/yaw/owner, unload, dimensão e sincronização; kills/XP/Mastery após resultado autorizado. Spawn tentado, spawn aceito, dano pedido, dano aceito, desmontagem, knockback e kill são estados diferentes. A fila vigente permanece no [crosswalk alfabético vivo](../ENCHANTMENT-PERK-CROSSWALK-1.0.10.md).
