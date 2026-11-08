# Sharp Cane — `alexscaves:sharp_cane` (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Integração:** `NO_MUTATION`. O recorte conclui este encantamento, seu parâmetro inicial e o ramo nativo selecionado de busca/pedido de dano. Não conclui o tick/CFG integral do gancho, a aplicação de dano pela engine, a persistência herdada ou o provider integral.

## 1. Identidade e descrição original

- **Provider / versão:** Alex's Caves Continued / `alexscaves`, Minecraft 1.21.1; `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Recurso:** `data/alexscaves/enchantment/sharp_cane.json`, 366 bytes; SHA-256 `d9d75a98966a4881b93ea877d2e8d9be15539dc7a162ba32de5dce112b41c181`.
- **Tag de item:** `data/alexscaves/tags/item/enchantable/candy_cane_hook.json`, 55 bytes; SHA-256 `b1d1990dd02fec11c14976f0f0a893e30b6c25e443efc013428cbdd4ef334310`; contém somente `alexscaves:candy_cane_hook`.
- **Descrição literal de `en_us.json`:** “Hook deals three damage per level when attaching to a target”. Tradução explicativa: o gancho pede três pontos de dano por nível no ramo de aquisição abaixo. A descrição não demonstra dano líquido, tipo final de dano ou que todo caminho de attachment chama `hurt`. Não há chave própria no `pt_br.json` examinado.
- **Consumidor:** `server/entity/item/CandyCaneHookEntity.class`, 20.848 bytes; SHA-256 `e590bb67ea2b594861a30b05a5099fbd5eafe2920ff867883aaa6fd7cec478f8`. **Emissor:** `server/item/CandyCaneHookItem.class`, 9.327 bytes; SHA-256 `d999251e494c45420e58881181e9d67757247b6865dc4a547bf0da8a46cf8e44`. Prefixo de classes: `com/github/alexmodguy/alexscaves/`.
- **Provas:** [manifesto individual](../EXACT-SHARP-CANE-CONTRACT-1.0.10.json), [reprodução](../EXACT-SHARP-CANE-CONTRACT-1.0.10.md) e [Far Flung](far-flung.md), que conserva seu escopo histórico parcial.

A busca de Fieldrefs exatos de `ACEnchantmentRegistry.SHARP_CANE` nos 1.555 classfiles do JAR localizou `ACEnchantmentRegistry` e `CandyCaneHookEntity`; o item não consulta esse nível diretamente. O scan não exclui reflexão, transformações ou consumidores externos. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e serve apenas de corroboração adjacente. Os valores abaixo pertencem ao binário e aos recursos **1.0.10**.

## 2. Comportamento: snapshot e pedido nativo de dano

O construtor `CandyCaneHookEntity(Player,Level,ItemStack,boolean)V`, com **231 instruções**, lê a stack recebida em `@421–426`, converte o nível para float e multiplica por `3.0F` em `@429–432`, passando o resultado a `setDamage(F)` em `@433`:

```text
DAMAGE = 3F × enchantLevel(stack, SHARP_CANE)
```

| Nível lido na criação | Parâmetro DAMAGE |
|---:|---:|
| 0 | 0F |
| I | 3F |
| II | 6F |

`setDamage(F)V` e `getDamage()F` têm **7 instruções** cada: escrevem/leem o Float sincronizado `DAMAGE`, sem clamp próprio. `defineSynchedData`, **47 instruções**, define seu default **0F** em `@71–78`. A sequência da fórmula não exige nível positivo nem limita o nível ao máximo II publicado. Níveis externos não recebem por isso uma garantia de segurança ou de valor aplicado.

É um **snapshot na criação**: o pedido de dano do tick lê `getDamage()`, sem reler o nível da stack. Alterar o encantamento depois do lançamento não demonstra atualização automática do gancho existente.

O prefixo selecionado de `tick()V` tem esta ordem relevante:

1. Chama `ThrowableProjectile.tick` em `@1`, **antes** de capturar owner em `@5` e hooked entity em `@10`. A superclasse pode produzir callbacks antes dessa captura. O ramo próprio de seleção/dano exige servidor: `isClientSide@23` / `ifne607@26`.
2. Depois dos ramos de recolhimento e de alvo já existente, só a busca sem hooked entity pode chegar ao pedido de dano aqui selado.
3. Encontrando candidato, escreve primeiro seu **`HookedEntityUUID`** em `@522–528`.
4. Lê `DAMAGE` e pula o dano se for **igual a 0F**, por `fcmpl/ifeq563@532–537`. O teste não é `damage>0`.
5. Obtém `damageSources().thrown(this,owner)` em `@540–549`, chama **`candidate.hurt(source,getDamage())`** em `@551–559` e **descarta o booleano** em `pop@562`.

**UUID atribuído e dano aceito são estados distintos.** A atribuição precede `hurt` e não depende de seu retorno. Os valores 3F/6F são argumentos do pedido nativo, sem garantir dano líquido após defesa, invulnerabilidade, PvP, proteções ou outros hooks. A factory `DamageSources.thrown` pertence à engine; esta ficha não certifica seu DamageType efetivo.

`onHitEntity(EntityHitResult)V` é outro caminho: seu corpo completo tem **24 instruções**, zera delta movement, grava hooked position, obtém a entidade, normaliza Gum Worm Segment para head e grava seu UUID em `@37–42`. **Não lê DAMAGE nem chama hurt nesse corpo.** Como o supertick antecede a captura do alvo, colisão física e busca do tick não são eventos intercambiáveis. A relação efetiva entre eles exige QA; a diferença estática não declara defeito reproduzido nem dano em todo impacto.

## 3. Parâmetros, JSON e aquisição

| Campo | Valor publisher | Significado / limite |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.sharp_cane` | Chave de tradução |
| `supported_items` | `#alexscaves:enchantable/candy_cane_hook` | Elegibilidade declarada |
| `weight` | `10` | Peso de dados; não é chance de acerto |
| `max_level` | `2` | Máximo II publicado |
| `min_cost` | base `1`, incremento por nível acima do primeiro `8` | I: 1; II: 9 |
| `max_cost` | base `41`, incremento `10` | I: 41; II: 51 |
| `anvil_cost` | `1` | Custo do encantamento, separado do uso do gancho |
| `slots` | `mainhand` | Slot declarado; não é revalidação da mão a cada pedido de dano |
| `effects` / `exclusive_set` | Ausentes neste JSON | Comportamento Java; ausência local não prova compatibilidade global |

`ACEnchantmentRegistry.<clinit>` liga o literal `sharp_cane` à chave `SHARP_CANE` em `@473–479`; são âncoras delimitadas, sem certificar o initializer inteiro. `ACCompat.enchantLevel` lê o primeiro nível correspondente na stack ou retorna zero, sem clamp próprio ao máximo II nem validação própria de slot/tag.

As quatro tags empacotadas `minecraft:in_enchanting_table`, `minecraft:non_treasure`, `minecraft:on_random_loot` e `minecraft:tradeable` incluem o ID. O scan dos 51 JSONs publisher não encontrou exclusão reversa deste ID. Essas constatações não garantem obtenção, compatibilidade ou dados efetivos do modpack. Os custos de aquisição não são mana, XP ou durabilidade por acerto.

## 4. Targeting, área e parâmetros herdados

O ramo de hooked entity já existente, `tick@220–352`, trata alvo vivo/morto e posição do gancho. Para Gum Worm usa posição especializada; para outras entidades, posição mais metade da altura. Seus caminhos saltam ao join `@563` e **não chamam o hurt de Sharp Cane**: não há repetição desse pedido a cada tick enquanto o mesmo estado de alvo existe.

Quando hooked entity é null, o ramo nativo faz:

1. Obtém a **AABB do próprio gancho** e aplica `inflate(1D)` em `@355–360`; consulta `Level.getEntities(this,aabb,predicate)` em `@368–380`. O `BootstrapMethods` liga esse predicate a **`Entity.isAlive()`**. É filtro de entrada da consulta, sem teste de dano aceito, LOS ou proteção.
2. Normaliza `GumWormSegmentEntity` para seu head em `@412–437`; rejeita candidato null, `CandyCaneHookEntity` e qualquer `Projectile` em `@439–457`.
3. Com owner não null, rejeita o owner e aceita candidato mais próximo; também permite que Gum Worm substitua candidato não-GumWorm quando a comparação de distância não favorece a substituição (`@460–507`). Não é garantia universal de alvo mais próximo ou prioridade absoluta de Gum Worm.
4. Com owner null, `ifnull510@461` pula a comparação com owner, distância e essa condição de Gum Worm. Não presumir a mesma seleção de alvo mais próximo nesse caso.

| Superfície de perk | Contrato individual |
|---|---|
| Dano | Sharp Cane só altera o DAMAGE inicial por `3F×L`; o ramo acima usa esse parâmetro |
| Tipo de dano | Fonte solicitada por `thrown(this,owner)`; DamageType e dano aplicado permanecem fronteira da engine |
| Tipo de alvo / permissões | Filtros nativos acima; não há teste próprio de aliados, PvP, claims ou LOS nesse prefixo. Rejeições podem ocorrer em fronteiras externas |
| Área / tamanho | AABB própria `inflate(1D)` é busca nativa; N/A como multiplicador próprio de Sharp Cane. Não é raio de explosão, aumento da hitbox ou dano em área |
| Alcance / velocidade / gravidade | N/A como modificadores próprios de Sharp Cane; conservam construtor, movimento, colisão e consumidores nativos. Far Flung e Straight Hook têm consumidores separados |
| Duração / cooldown / frequência | Sem duração, cooldown ou timer próprio identificado para Sharp Cane. Lifecycle e recolhimento pertencem ao gancho; o pedido observado não é um DoT periódico |

Não deduzir distância física máxima da AABB de busca, nem dar dano a todos os resultados da lista: o trecho acumula **um candidato** e faz um pedido ao final.

## 5. Emissor, custos e persistência

`CandyCaneHookItem.use(Level,Player,InteractionHand)InteractionResultHolder`, **188 instruções**, obtém a stack da mão usada e a outra mão. Guarda servidor em `@29–33` e consulta `canLaunchHook` em `@42`. O construtor da entidade recebe Player, Level, a stack usada e o booleano offhand em `@125–145`; depois escreve owner em `@153` e reeling=false em `@159`.

O item pede `addFreshEntity` em `@172` sob `!isClientSide` e **descarta seu retorno booleano** em `@175`. Em seguida grava `LastLaunchedHookUUID@183` e `Reeling=false@189` na stack. Registro de UUID, stat ou animação não comprova inserção aceita, alvo adquirido ou dano aplicado.

`canLaunchHook`, **54 instruções**, consulta a tag/UUID, resolve `ServerLevel.getEntity`, testa tipo Hook, vivo, ownership e mão/argumento booleano. São gates nativos de elegibilidade/reuso; a existência desse método não constitui hook externo homologado, atomicidade de spawn ou proteção contra reentrada.

Os pedidos de desgaste estão nos **ramos de recolhimento** de `use`: valor **1** via `ACCompat.hurtAndBreak` em `@299` para a outra stack quando ela é um gancho ativo ainda não recolhendo, e em `@328` para a stack usada quando ainda não recolhendo, sob os demais gates do corpo. Há cenários de duas mãos; não afirmar uma única cobrança em toda invocação. Sharp Cane não acrescenta débito por hit ou lançamento, e o bloco de `hurt` não cobra novamente durabilidade, mana, stamina, fome ou XP. O valor efetivo de desgaste e quebra permanece delegado à engine.

Os overrides próprios `readAdditionalSaveData` / `addAdditionalSaveData`, **23/22 instruções**, chamam super e leem/gravam `Reeling`, `HookedEntityUUID` condicional e `Offhand`. **Não leem nem gravam DAMAGE.** O default 0F e essa omissão própria não provam perda ou restauração física do dano após reload: persistência herdada/engine, sincronização e reconstrução da entidade continuam fronteiras de validação. Não criar estado paralelo de Sharp Cane para preencher essa lacuna por inferência.

## 6. Integração, autoridade e Mastery

| Intenção | Contrato a preservar | Estado |
|---|---|---|
| Escala de dano | Snapshot `3F×L` na stack de criação; Float sincronizado, gate `!=0F` e pedido nativo no ramo de busca | Hook `NOT_VERIFIED`; não reler nível a cada tick sem contrato novo |
| Proc / XP / Mastery | Spawn tentado, UUID atribuído, callback de colisão, tentativa de hurt e dano aceito são estados distintos | Não conceder crédito por attachment/UUID ou pelo booleano descartado |
| Targeting / área | Uma seleção nativa, normalização de segmento, owner e ramo owner-null | Não ampliar área, duplicar alvo ou produzir um segundo hit no adapter |
| Custo / mãos | Recolhimento e stacks nativas conservam seus gates e pedidos de desgaste | Sem segunda cobrança ou segundo cast |
| Persistência / rede | DAMAGE sincronizado, omissão nos overrides NBT próprios e estado de gancho/stack têm autoridades distintas | Reload, cliente e dedicado pendentes |
| Black Arcana / Enshrouded / RPG Skill Tree | Candy Cane Hook conserva execução nativa; progressão externa depende de fronteira demonstrada | `NO_MUTATION`; nenhum adapter executável ou Stage promovido |

O encantamento modifica um equipamento nativo; **não cria raiz mágica, novo cast Black Arcana ou novo DamageType**. A existência de campos, setters, assinaturas e callbacks não autoriza mutação externa. Os contratos anteriores de Far Flung mantêm seus bytes e limites; o construtor compartilhado não certifica encantamentos irmãos por associação.

## 7. Evidência, contabilidade e validação

O [manifesto individual](../EXACT-SHARP-CANE-CONTRACT-1.0.10.json), a [reprodução](../EXACT-SHARP-CANE-CONTRACT-1.0.10.md) e os [testes semânticos](../../../../../docs/qa/alexscaves_1010_sharp_cane_cards_test.py) ligam identidade, aquisição, registro, snapshot, callback de hit, busca, fonte solicitada, custos e limites de persistência.

Os corpos selecionados completos incluem construtor **231**, definição sincronizada **47**, getter/setter DAMAGE **7/7**, `onHitEntity` **24**, `use` **188**, `canLaunchHook` **54** e NBT próprio **23/22** instruções. **`tick()V` possui 546 instruções e permanece PARTIAL.** O recorte sela o prefixo local `@0–562` (**255 instruções**) e o join `@563` (**256 âncoras** no total), dentro do budget de 256 por método; não se declara tick integral ou CFG integral completo. O initializer de registro também permanece janela delimitada. A engine, o supertick e as chamadas externas conservam suas fronteiras.

**Contabilidade:** uma ficha individual, **+0 raízes mágicas novas**. `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, provider integral aberto. As vinte fichas parciais anteriores continuam parciais; não há promoção de Stage.

QA física pendente: busca versus `onHitEntity`/supertick; níveis 0/I/II/externos e snapshot após mudar a stack; retorno de hurt, defesas, PvP, alianças e proteções; owner null, Gum Worm e segmentos; reeling, duas mãos e custos; spawn recusado; cliente/dedicado e sincronização; unload/reload, dimensão e persistência DAMAGE; atribuição única de Mastery após resultado autorizado. A fila atual é mantida no [crosswalk alfabético](../ENCHANTMENT-PERK-CROSSWALK-1.0.10.md).
