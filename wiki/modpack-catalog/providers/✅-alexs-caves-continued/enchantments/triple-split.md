# Triple Split — `alexscaves:triple_split` (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Integração:** `NO_MUTATION`. O recorte conclui este encantamento, seu snapshot no disparo e a divisão nativa selecionada do Gumball. `ShotGumItem.acInventoryTick` permanece **PARTIAL**; não se concluem a arma integral, a aceitação de spawn/dano pela engine, a persistência herdada ou o provider integral.

## 1. Identidade e descrição original

- **Provider / versão:** Alex's Caves Continued / `alexscaves`, Minecraft 1.21.1, NeoForge, Java 21; `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Recurso:** `data/alexscaves/enchantment/triple_split.json`, **361 bytes**; SHA-256 `fd4f773c48969b4c2537f443cc80d91e1385d545763be78feaefc5816ac551a0`.
- **Tag de item:** `data/alexscaves/tags/item/enchantable/shot_gum.json`, **48 bytes**; SHA-256 `3ccaf9482a8187e3c99f45ff7d5a28c7c73fe39c1840daef13f294821301e31d`; contém somente `alexscaves:shot_gum`.
- **Nome e descrição literais de `en_us.json`:** “Triple Split”; “Gumballs split into three additional Gumballs after hitting their first target”. Tradução explicativa: Gumballs com a flag de divisão tentam criar três filhos no callback de entidade abaixo. O texto não comprova primeiro dano aceito, três spawns aceitos ou três hits. Não há chaves próprias de Triple Split no `pt_br.json` examinado.
- **Reader direto:** `server/item/ShotGumItem.class`, **13.156 bytes**, SHA-256 `08aa8b9aa1781f2ead7d899e4fde758ea44bc527a2ee5968997e5b3ffdd32238`. **Consumidor da flag:** `server/entity/item/GumballEntity.class`, **15.427 bytes**, SHA-256 `343cc816bcb545241205a6dd1f94c34c37990273aa360bfc82c9fb9485f0f535`. Prefixo de classes: `com/github/alexmodguy/alexscaves/`.
- **Provas:** [manifesto individual](../EXACT-TRIPLE-SPLIT-CONTRACT-1.0.10.json), [reprodução](../EXACT-TRIPLE-SPLIT-CONTRACT-1.0.10.md) e contexto nativo de [Shot Gum](../equipment/shot-gum.md), [Gumball](../damage-types/gumball.md) e [Targeted Ricochet](targeted-ricochet.md), que conservam seus escopos anteriores.

A busca de Fieldrefs exatos de `ACEnchantmentRegistry.TRIPLE_SPLIT` nos **1.555 classfiles** do publisher localizou `ACEnchantmentRegistry` e `ShotGumItem`. Não exclui reflexão, transformações ou consumidores externos. `ACEnchantmentRegistry.<clinit>@437–443` liga o literal `triple_split` à chave `TRIPLE_SPLIT`; é janela delimitada do initializer. A fonte pública adjacente declara **1.1.1** e serve apenas de corroboração; os parâmetros desta ficha pertencem aos bytes e recursos **1.0.10**.

## 2. JSON, nível e aquisição

| Campo | Valor publisher | Significado / limite |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.triple_split` | Chave de tradução |
| `supported_items` | `#alexscaves:enchantable/shot_gum` | Elegibilidade declarada do equipamento |
| `weight` | `2` | Peso de dados; não é chance de divisão |
| `max_level` | `1` | Apenas I publicado |
| `min_cost` | base `1`, incremento por nível acima do primeiro `12` | Expressão declarativa `1+12(L−1)`; I: 1 |
| `max_cost` | base `41`, incremento `10` | Expressão declarativa `41+10(L−1)`; I: 41 |
| `anvil_cost` | `4` | Aquisição do encantamento, separada de munição por disparo |
| `slots` | `mainhand` | Slot declarado; não é revalidação da mão a cada impacto |
| `effects` / `exclusive_set` | Ausentes neste JSON | Comportamento Java; ausência local não prova compatibilidade global |

As tags empacotadas `minecraft:in_enchanting_table`, `minecraft:non_treasure`, `minecraft:on_random_loot` e `minecraft:tradeable` incluem o ID. Cada um desses recursos tem **1.631 bytes**, SHA-256 `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1`. O scan dos **51 JSONs de encantamento** encontra exclusão reversa somente em `targeted_ricochet.json`: seu `exclusive_set` contém `alexscaves:triple_split` (**422 bytes**, SHA-256 `adb5dfde437fbe38910045b6ec593103c43224224c8ab3a0101dec522a5ebb1e`). Flags compartilhadas no Java não legitimam a coexistência desses encantamentos.

`ACCompat.enchantLevel` lê o primeiro nível correspondente na stack ou retorna zero, sem clamp próprio ao máximo I nem validação própria de slot/tag. Os gates de aquisição são distintos da leitura de nível na execução.

A receita de equipamento `data/alexscaves/recipe/shot_gum.json`, **493 bytes**, SHA-256 `11851d66a5e83898a166bb8f92fda1660f305bdc20b1dd0c2f8b5939ae2425a1`, produz **1 Shot Gum** com o padrão literal `SPP / III / IN `: 1 Sugar Glass, 2 Gumball Piles, 4 ingredientes de `alexscaves:ingots/iron` e 1 de `alexscaves:nuggets/iron`. A receita não garante o encantamento no resultado. Obtenção, compatibilidade e dados efetivos do modpack permanecem pendentes de datapacks/modlist.

## 3. Comportamento: snapshot e emissão primária

`ShotGumItem.acInventoryTick(ItemStack,Level,Entity,boolean)V` possui **285 instruções**. O recorte **PARTIAL** sela `@0–10` e `@81–607`, **254 instruções**, omitindo a atualização visual/tag `Prev*` em `@12–78`. Em `@0–10`, captura `S=isShooting(stack)` e `T=getShootTime(stack)`; só **`S && T==5`** alcança o disparo em `@81–89`. O argumento booleano `selected` não é lido. Som e `setShooting(false)` precedem a leitura dos encantamentos.

Em `@154–169`, o reader calcula um booleano local; cada primário recebe esse snapshot por `setSplitsOnHit` em `@437–441`:

```text
splitPrimário = enchantLevel(stack, TRIPLE_SPLIT) > 0
```

| Nível lido no tick de disparo | Flag no primário | Ramo de divisão quando alcançado |
|---|---|---|
| 0 ou não positivo | false | Não entra |
| I | true | Três tentativas de filhos por callback |
| Nível externo positivo acima de I | true | Mesmo ramo; sem escala adicional |

É um snapshot do disparo, sem escala `3L` ou chance própria. O impacto lê o estado do projétil; não relê a stack. Alterar o encantamento depois não demonstra atualização de projéteis existentes.

Para holder `LivingEntity`, o laço de `acInventoryTick@291–515` tenta emitir **dois primários normais** ou **um explosivo**, conforme `EXPLOSIVE_FLAVOR`; Triple Split não escolhe essa quantidade. O construtor primário `GumballEntity(Level,LivingEntity)` atribui esse holder como owner por `setOwner@18`. Os setters iniciais incluem dano **4F**, máximo de bounces **`4+2×level(BOUNCY_BALL)`**, targeting e flag explosiva; o tiro usa velocidade **1.5F normal / 0.5F explosivo**, dispersão **5F**. São parâmetros nativos da arma, sem nova certificação individual dos encantamentos irmãos.

A construção e os setters precedem a guarda servidor: **somente a tentativa de `addFreshEntity@498–511`** nesse laço exige `!isClientSide`. O retorno booleano é descartado. Não ampliar essa guarda para todo o tick, o débito de cargas ou a divisão de filhos. A cadeia de uso/tick do equipamento conserva sua prova anterior.

## 4. Impacto, geometria e filhos

`GumballEntity.onHit(HitResult)V`, **79 instruções**, chama **`ThrowableProjectile.onHit@2` antes dos filtros locais**. Depois, bloco com collision shape não vazio pede bounce; entidade que não é o próprio owner nem outro Gumball entra em `hitEntityIds`, e o bounce de entidade exige `!splitsOnHit()` em `@154–168`. Esses filtros posteriores não bloqueiam previamente o callback da superclasse. `ownedBy` não estabelece exclusão geral de pets ou entidades pertencentes a terceiros.

`onHitEntity(EntityHitResult)V`, **162 instruções**, conserva esta ordem:

1. Captura vítima `@0–4`, owner `@5–9` e dano `@10–14`.
2. Em `@16–77`, pode retornar antes de dano e divisão quando o owner é Gumbeeper possuído, resolve sua Licowitch e esta classifica a vítima `LivingEntity` como friendly fire. Esse contexto não certifica a IA de mobs.
3. Cria a fonte por `causeGumballDamage(registryAccessDaVítima,owner)@78–89`. A factory nativa usa o owner como argumento de entidade, sem um par separado projétil/dono; o contrato de dano Gumball conserva sua autoridade.
4. Com owner não null, vítima igual ao owner ou aliança em **qualquer sentido** pula o pedido de dano para `@143`. Com owner null, esses testes são pulados para o caminho de dano.
5. Pede **`Entity.hurt(source,danoCapturado)@139`** e **descarta o retorno em `@142`**.
6. Só então **`splitsOnHit()@144`** controla a divisão. Ela pode ocorrer após dano pulado por owner/aliança ou após `hurt=false`; a saída friendly-fire especial anterior é distinta.

`hitEntityIds` **não deduplica o dano próprio**: `onHitEntity` não consulta essa lista. Ela exclui candidatos na busca de Targeted Ricochet; o `List.add` posterior em `onHit` também não testa `contains`. Colisão despachada, pedido de dano, dano aceito e divisão são estados distintos.

O laço `onHitEntity@150–342` usa **`i=0,1,2`**, chama `ACCompat.createEntity(GUMBALL,level)` por iteração e tenta inserir o filho. Ao completar as três iterações, pede **descarte do pai em `@345–346`**. São três tentativas por callback que alcança o ramo, sem garantia de três entidades inseridas ou três alvos distintos. O corpo não tem guarda própria de lado, guarda para retorno null da factory, confirmação de spawn, deduplicação ou trava de reentrada.

Geometria própria de cada iteração, em `@182–284`:

```text
u = normalize(deltaMovement atual do pai)
heading = -float(atan2(u.x,u.z)) × 180F / 3.1415927F
s = isExplosive(pai) ? 0.699999988079071D : 1.5D
v_i = Vec3(0,0,s).yRot(float(-toRadians(heading + 30F − 30F×i)))
posiçãoFilho = vítima.eyePosition + v_i
deltaMovementFilho = v_i
```

Os offsets angulares de entrada são **`+30°,0°,−30°`** em relação ao heading horizontal, sem componente Y nesse vetor. A origem usa **os olhos da vítima + vetor**, não a posição do pai. São parâmetros de movimento, sem alcance máximo, raios de targeting ou cone físico final garantido. Heading, flag explosiva e getters são lidos dentro de cada iteração; callbacks externos de dano/spawn impedem presumir snapshot imutável do pai. Movimento zero/vertical e trajetória real exigem QA da engine.

| Propriedade do filho | Operação própria no split |
|---|---|
| `SPLITS_ON_HIT` | **false**, `@287–290`; desativa recursão nesse estado nativo, sem garantia contra mutação externa |
| `DAMAGE` | Getter corrente do pai → setter `@293–299`; pode diferir do dano capturado antes de `hurt` |
| `TARGETS_ON_BOUNCE` | Getter corrente → setter `@302–308`; não legitima coexistência de encantamentos incompatíveis |
| `EXPLOSIVE` | Getter corrente → setter `@311–317` |
| `MAXIMUM_BOUNCES` | Getter corrente → setter `@320–326`; copia total **M**, não restante `M−B` |
| Owner | Não é argumento da factory nem recebe `setOwner` neste laço |
| Cor / bounces / IDs / progresso | Não são copiados explicitamente; construtor sorteia cor `0..11` e cria lista vazia, e o default sincronizado de bounces é `0` |
| Inserção | `addFreshEntity@329–338`; booleano descartado |

`ACCompat.createEntity` delega a `EntityType.create(Level)`. O registro Gumball aponta ao construtor **`(EntityType,Level)`**, **19 instruções**, que não atribui owner; o construtor primário **`(Level,LivingEntity)`**, **10 instruções**, é que chama `setOwner`. Isso não prova owner null sob todos os hooks externos nem defeito físico reproduzido, mas impede atribuir automaticamente kills, XP ou Mastery dos filhos ao jogador.

## 5. Custos, estado, lifecycle e persistência

Após o laço primário, `acInventoryTick@518–550` poupa cargas de Player creative; nos demais casos grava **`max(cargas−1,0)`** uma vez. O débito não depende de spawn aceito nem se multiplica por descendente; não está sob a guarda local de inserção servidor. O equipamento conserva quatro cargas por recarga e consumo survival de uma Gumball Pile no caminho já documentado. O impacto/split não cobra outra munição, durabilidade, mana, stamina ou XP próprio nesses consumidores; a ausência local não prova custo global zero. `anvil_cost=4` é aquisição.

As chaves de stack `Shooting`, `ShootTime`, `Gumballs`, `CrankAngle` e `Prev*` têm autoridade do equipamento. São distintas do snapshot `SPLITS_ON_HIT` e do progresso visual do projétil. Triple Split não introduz cooldown ou duração próprios.

`defineSynchedData`, **43 instruções**, define `SPLITS_ON_HIT=false` em `@61–68`, além de `DAMAGE=2F`, `TARGETS_ON_BOUNCE=false`, `EXPLOSIVE=false`, `MAXIMUM_BOUNCES=5`, `BOUNCES=0` e `COLOR=0`; o construtor sobrescreve a cor com aleatório `0..11`. `splitsOnHit()` e `setSplitsOnHit(Z)V` têm **7 instruções cada**, sem clamp, nível, slot ou tag próprios. Estado sincronizado observado não constitui API mutadora segura.

O Gumball conserva dimensões nativas **`0.25F×0.25F`**, gravidade **`0.07999999821186066D`** e lifecycle nativo. O descarte normal compara **`B>M`**; o explosivo trata parada/progresso em **`B>=M`**. Em `tick()V`, **165 instruções**, explosivo com `B>=M` incrementa progresso enquanto `<=20F`; quando já `>20F`, no servidor pede **`Level.explode(getOwner(),x,y+0.5,z,2F,false,NONE)`** e descarte. Progresso e colisões não são cooldown nem duração de Triple Split. Explosão e factory de dano direto mantêm contratos distintos.

Os overrides completos `addAdditionalSaveData` e `readAdditionalSaveData`, **9 instruções cada**, **chamam super** e gravam/leem diretamente somente **`Color`**. Não serializam explicitamente split, dano, targeting, explosivo, máximo, contagem, lista ou progresso. Esses corpos não demonstram conservação/perda física, persistência de owner, restauração da cadeia de filhos ou convergência de cliente/rede. Save/load, unload, dimensão, latência e autoria permanecem pendentes; não criar estado paralelo ou novo owner para preencher essa lacuna por inferência.

## 6. Parâmetros úteis para perks e autoridade

| Superfície | Contrato individual a preservar |
|---|---|
| Identidade / nível / quantidade | `TRIPLE_SPLIT` → snapshot `L>0` → `SPLITS_ON_HIT`; três tentativas por callback alcançado, filhos com split false |
| Origem / direção / velocidade | Olhos da vítima + `v_i`, heading do movimento corrente, offsets `+30/0/−30°`, vetor de módulo nominal `1.5/0.7`; não são alcance final ou cone garantido |
| Alvo novo / homing / alcance | **N/A como modificadores diretos:** o split usa a vítima do callback e movimento do pai, sem busca de alvo novo; targeting por bounce pertence a Targeted Ricochet |
| Dano / DamageType / área / hitbox | **N/A como modificadores diretos:** o ID controla divisão; dano corrente copiado, fonte, dimensões e explosão pertencem ao Gumball. Três tentativas não demonstram triplo HP perdido ou DPS |
| Cura / status / knockback | **N/A próprios:** não há aplicação direta introduzida pelo ID nesses consumidores; reações ao dano e comportamento nativo permanecem em suas autoridades |
| Duração / cooldown / frequência | **N/A próprios:** ticks, progresso explosivo, bounces e callback não são nova cadência de cast ou DoT de Triple Split |
| Custo / recursos | Um débito de carga quando o disparo alcança esse bloco, salvo Player creative; sem segunda cobrança por filho ou recibo baseado no retorno descartado de spawn |
| Sinergias / compatibilidade | Respeitar exclusão reversa com Targeted Ricochet; copiar targeting/explosivo/máximo não certifica encantamentos irmãos |
| Autoria / XP / Mastery | Owner primário explícito e ausência de cópia própria para filhos são fronteiras distintas; exigir resultado autorizado e crédito único da ação raiz |

Black Arcana mantém seu runtime mágico; Alex's Caves conserva emissão, movimento, divisão, dano e liquidação nativos. Enshrouded e RPG Skill Tree podem oferecer progressão/perks apenas por boundary demonstrado. Métodos, campos, setters e callbacks observados não são hooks mutadores seguros certificados. A divisão de munição nativa acrescenta **+0 raízes mágicas novas**; não autoriza adapter executável, segundo cast, segunda cobrança ou promoção de Stage: **`NO_MUTATION` / `fail-closed`**.

O targeting opcional já documentado em [Targeted Ricochet](targeted-ricochet.md) conserva seu escopo individual anterior. Esta ficha não o recertifica pelo método compartilhado. Spawn tentado, spawn aceito, callback, dano pedido, dano aceito e kill/Mastery precisam de autoridades e deduplicação demonstradas; a lista `hitEntityIds` não fornece esse recibo.

## 7. Evidência, contabilidade e QA

O [manifesto individual](../EXACT-TRIPLE-SPLIT-CONTRACT-1.0.10.json), a [reprodução](../EXACT-TRIPLE-SPLIT-CONTRACT-1.0.10.md) e os [testes semânticos](../../../../../docs/qa/alexscaves_1010_triple_split_cards_test.py) ligam os sete eixos: identidade, comportamento, parâmetros, alvo, custos, integração e validação. A reprodução parte do JAR SHA-exato e fixa recursos, locale, aquisição, Fieldrefs diretos, classes e instruções JVM; não inventaria consumidores reflexivos ou transformados.

Os corpos selecionados completos incluem `onHitEntity` **162**, `onHit` **79**, `tick` **165**, definição sincronizada **43**, construtores Gumball **19/10**, getters/setters sincronizados **7 cada**, factory e NBT próprio **9/9** instruções. **`acInventoryTick` tem 285 instruções e permanece PARTIAL**, com janelas `@0–10` e `@81–607` somando **254 instruções** dentro do limite de 256 âncoras por método. Fingerprint integral não substitui cobertura semântica integral; inicializadores de registro também conservam janelas delimitadas.

As provas anteriores [Gumball](../EXACT-GUMBALL-CONTRACTS-1.0.10.json), [split compartilhado](../EXACT-GUMBALL-SPLIT-ENCHANT-1.0.10.json) e [Targeted Ricochet](../EXACT-TARGETED-RICOCHET-STATIC-1.0.10.json) conservam bytes e escopos. O uso de Shot Gum e consumidores compartilhados não promove a arma, fichas parciais ou encantamentos irmãos por associação.

**Contabilidade:** uma ficha individual; **+0 raízes mágicas novas**. `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, provider integral aberto. As vinte fichas parciais anteriores continuam parciais; não há promoção de Stage.

QA física pendente: níveis 0/I/externos e snapshot após troca de stack; primários normais/explosivos e custo único; callback após dano pulado/recusado, reentrada e descarte do pai; owner, aliados, Gumball e friendly-fire especial; filhos com/sem owner, procs e kills; heading zero/vertical, geometria, factory null e spawn recusado; bounces, flags incompatíveis e explosão; defesas, eventos, PvP e claims; cliente/dedicado, save/load, unload, dimensão e sincronização; crédito único de Mastery após resultado autorizado. A fila atual é mantida no [crosswalk alfabético vivo](../ENCHANTMENT-PERK-CROSSWALK-1.0.10.md).
