# Triple Splash — `alexscaves:triple_splash` (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Integração:** `NO_MUTATION`. O recorte conclui este encantamento, a quantidade/geometria de lançamento e os consumidores nativos selecionados do Water Bolt. Não conclui o tick/CFG integral do projétil, a aceitação de spawn/dano pela engine, persistência herdada ou o provider integral.

## 1. Identidade e descrição original

- **Provider / versão:** Alex's Caves Continued / `alexscaves`, Minecraft 1.21.1, NeoForge, Java 21; `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Recurso:** `data/alexscaves/enchantment/triple_splash.json`, **363 bytes**; SHA-256 `6946e2d21814f3e398925f2886a6284b140032b255a05f9598c8e00e2bc315be`.
- **Tag de item:** `data/alexscaves/tags/item/enchantable/sea_staff.json`, **49 bytes**; SHA-256 `22e45ab74b71d7152ccc531a633e5149df9c12eece40464c85c50f5a600fd80e`; contém somente `alexscaves:sea_staff`.
- **Nome e descrição literais de `en_us.json`:** “Triple Splash”; “Sea Staff fires two additional water bolts”. Tradução explicativa: o Sea Staff tenta lançar dois Water Bolts adicionais, conforme o gate abaixo. Não há chaves próprias de Triple Splash no `pt_br.json` examinado.
- **Consumidor direto:** `server/item/SeaStaffItem.class`, **9.765 bytes**, SHA-256 `cb3153a35e7f4c3ab23e68693aec110edf03ecd050c3b485e35ccbb257b4bbc6`. **Projétil:** `server/entity/item/WaterBoltEntity.class`, **16.812 bytes**, SHA-256 `342c011b0178e1f65cd2e6ef315fe6bad49bd5ead237b2274e822560e2eac401`. Prefixo de classes: `com/github/alexmodguy/alexscaves/`.
- **Provas:** [manifesto individual](../EXACT-TRIPLE-SPLASH-CONTRACT-1.0.10.json), [reprodução](../EXACT-TRIPLE-SPLASH-CONTRACT-1.0.10.md) e ação raiz [Sea Staff — Water Bolt](../actions/sea-staff-water-bolt.md).

A busca de Fieldrefs exatos de `ACEnchantmentRegistry.TRIPLE_SPLASH` nos **1.555 classfiles** do JAR localizou `ACEnchantmentRegistry` e `SeaStaffItem`. Não exclui reflexão, transformações ou consumidores externos. `ACEnchantmentRegistry.<clinit>@302–308` liga o literal `triple_splash` à chave `TRIPLE_SPLASH`; é janela delimitada do initializer. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e serve apenas de corroboração adjacente. Os parâmetros desta ficha vêm dos recursos e bytes **1.0.10**.

## 2. JSON, nível e aquisição

| Campo | Valor publisher | Significado / limite |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.triple_splash` | Chave de tradução |
| `supported_items` | `#alexscaves:enchantable/sea_staff` | Elegibilidade declarada do equipamento |
| `weight` | `2` | Peso de dados; não é chance de proc |
| `max_level` | `1` | Apenas I publicado |
| `min_cost` | base `1`, incremento por nível acima do primeiro `15` | Expressão declarativa `1+15(L−1)`; I: 1 |
| `max_cost` | base `41`, incremento `10` | Expressão declarativa `41+10(L−1)`; I: 41 |
| `anvil_cost` | `4` | Custo de aquisição do encantamento, separado do uso |
| `slots` | `mainhand` | Slot declarado; o consumidor usa a stack da mão recebida |
| `effects` / `exclusive_set` | Ausentes neste JSON | Comportamento Java; ausência local não prova compatibilidade global |

As tags empacotadas `minecraft:in_enchanting_table`, `minecraft:non_treasure`, `minecraft:on_random_loot` e `minecraft:tradeable` incluem o ID. O scan dos **51 JSONs de encantamento** encontrou exclusão reversa em `bouncing_bolt.json`: seu `exclusive_set` contém `alexscaves:triple_splash`. Isso documenta a incompatibilidade declarada com Bouncing Bolt, sem garantir os dados efetivos de datapacks ou o resultado de toda operação da engine. Não pressupor coexistência legítima desses dois encantamentos só porque seus consumidores aparecem em `use`.

`ACCompat.enchantLevel` procura o primeiro nível correspondente na stack ou retorna zero, sem clamp próprio ao máximo I e sem revalidar slot/tag. A tag de item e os gates de aquisição são distintos da leitura de nível na execução.

A aquisição nativa do equipamento está em `data/alexscaves/loot_table/gameplay/deep_one_mage_barter.json`, **4.482 bytes**, SHA-256 `18682ca468355f61eda02c903fdb9c0dfbda88094c5caf343b1ae5ef437c44eb`: a entrada `alexscaves:sea_staff` tem peso **12**. Esse peso não é uma probabilidade isolada nem garante Triple Splash no item obtido. Aquisição e compatibilidade efetivas no modpack permanecem pendentes.

## 3. Comportamento: quantidade e geometria de lançamento

`SeaStaffItem.use(Level,Player,InteractionHand)InteractionResultHolder`, **189 instruções**, captura a stack da mão usada em `@0–5`. O bloco `@74–352` exige **`!Level.isClientSide()`**. Dentro dele, adquire um alvo uma vez em `@81–93` e lê Triple Splash em `@95–111`:

```text
N = enchantLevel(stack, TRIPLE_SPLASH) > 0 ? 3 : 1
para i = 0 até N−1:
    spreadYaw = i == 0 ? 0F : (i == 1 ? −50F : +50F)
    velocidadeSolicitada = i > 0 ? 1F : 2F
```

| Nível lido pelo consumidor | Iterações / pedidos de inserção | Yaw adicional | Velocidade passada a `shootFromRotation` |
|---|---:|---|---|
| 0, ou nível não positivo | 1 | `0°` | `2F` |
| I | 3 | `0°`, `−50°`, `+50°` | `2F`, `1F`, `1F` |
| Nível externo positivo acima de I | 3 | Mesmo conjunto | Mesmo conjunto |

É uma seleção booleana, **não `1+2L`**, e não acrescenta dois bolts por cada nível externo. O loop `@113–352` cria um `WaterBoltEntity(Level,LivingEntity)` por iteração; esse construtor atribui o jogador como owner em `@50–52`. Não há novo comando de cast por bolt.

A origem é calculada em cada iteração por `use@158–238`, sem termo de spread ou índice na posição:

```text
a = yHeadRot + (mão == MAIN_HAND ? 45° : −45°)
x = playerX − playerWidth × 1.1 × sin(a × 0.017453292F)
y = eyeY − 0.4
z = playerZ + playerWidth × 1.1 × cos(a × 0.017453292F)
```

`1.1` e `0.4` são representações nominais: os literais double são **`1.100000023841858D`** e **`0.4000000059604645D`**; o ângulo intermediário é float. A fórmula usa **`yHeadRot`** na origem, enquanto a direção de tiro usa **`getYRot()`**. Não confundir a rotação da cabeça, o offset da mão e o spread por projétil.

Em `@241–269`, cada chamada `shootFromRotation(Entity,FFFFF)V` recebe, nesta ordem: **jogador, pitch do jogador, yaw do jogador + spread, offset de pitch `−20F`, velocidade `2F/1F`, imprecisão `12F`**. A função de tiro herdada pertence à engine. Os ±50° são offsets de entrada, não garantia de leque físico exato de 100°, separação fixa após homing ou alcance final; a imprecisão, a movimentação do atirador e a evolução nativa do bolt continuam relevantes.

Cada iteração chama `Level.addFreshEntity` em `@342–348` e **descarta o retorno booleano**. Assim, 3 iterações significam **3 tentativas**, sem certificar três entidades inseridas, três alvos distintos, três hits ou triplo dano/DPS.

## 4. Targeting, impacto e lifecycle compartilhados

`getClosestLookingAtEntityFor(Level,Player,double)Entity`, **119 instruções**, recebe **`128D`** uma vez antes do loop. Faz clip `VISUAL/NONE` de `eyes` até `eyes+look×128`. O fallback constrói uma caixa de ±`0.5D` no ponto de hit, infla `15D` e depois a distância recebida; consulta `LivingEntity` e escolhe o candidato mais próximo **do ponto de hit**, não do jogador. Ambos os ramos próprios exigem `Mob`, diferente do jogador, ausência de aliança nos dois sentidos e linha de visão. Não há teste explícito próprio de `isAlive` nesses filtros. O ramo `EntityHitResult` existe, mas isso não prova que `Level.clip` o produzirá. **128 é argumento de consulta, não alcance físico máximo nem raio de AOE.**

Se esse alvo não é null, cada bolt recebe sua UUID em `use@327–339`. Portanto os laterais podem compartilhar o mesmo alvo inicial; o método não busca um alvo novo por spread. `getArcingTowards` resolve a UUID por `ServerLevel.getEntity`; o homing no prefixo de `tick` é servidor e depende do alvo resolvido, distância, `dieIn`, ticks e `seekAmount`.

Cada bolt recebe `seekAmount=0.3F+0.2F×level(SOAK_SEEKING)` em `use@314–324`. Triple Splash não altera essa fórmula nem aumenta o dano unitário. A fórmula, as janelas de correção e a sutileza **`(double)0.3F > 0.3D`** pertencem ao contrato próprio de [Soak Seeking](soak-seeking.md); não reinterpretar o teste como presença de Triple Splash. A separação angular inicial pode ser modificada pelo homing.

O circuito nativo compartilhado comprovado conserva:

- **Impacto em entidade:** `onHitEntity@32–75` exige servidor, entidade atingida diferente do próprio owner e `tickCount>2`. Chama `damageMobs` e inicializa **`dieIn=5`** se era `−1`.
- **Impacto em bloco:** `onHitBlock@32–56` chama o mesmo dano no servidor, sem o gate `tickCount>2`, e inicializa o mesmo contador. A condição `dieIn==−1` controla a inicialização, **não bloqueia todas as chamadas de dano posteriores**.
- **Área e fonte solicitadas:** `damageMobs@0–58` usa a AABB do bolt inflada **`2D` em cada eixo** e consulta `LivingEntity`; cria a fonte por **`mobProjectile(this, owner LivingEntity ou null)`**. Isso não certifica o DamageType efetivo da factory externa ou uma esfera de raio 2.
- **Filtros de dano:** rejeita aliado do bolt, `DeepOneBaseEntity`, owner e candidatos aliados ao owner quando este existe (`@90–126`). O pedido é **`ACCompat.hurt(candidate,source,3F)`** em `@133–139`; o valor é por candidato elegível naquela chamada, sem garantir HP perdido após defesas, invulnerabilidade, PvP ou claims.
- **Encantamentos irmãos:** `ENVELOPING_BUBBLE>0` controla flag aleatória por bolt e o ramo condicionado ao retorno de hurt; `BOUNCING_BOLT>0` controla `ricochet`. Esses efeitos não pertencem a Triple Splash. O último candidato elegível é atribuído antes do retorno de hurt; não inferir que o ricochete comprova dano aceito. Em `damageMobs@219–239`, a flag é limpa antes de chamar `onRicochetHit` com esse candidato.
- **Descendente de ricochete, quando esse ramo for alcançado:** `onRicochetHit` consulta a AABB desse candidato inflada `32D` por eixo; rejeita aliados do bolt, Deep Ones, o próprio candidato e, quando existe, owner/aliados do owner. Exige distância `>3D` do candidato e seleciona o mais próximo dele, sem teste próprio de linha de visão. Só cria o filho com novo alvo e owner `LivingEntity`: o construtor atribui esse owner; `copyPosition(this)` copia a posição do bolt pai; o corpo grava a UUID do novo alvo, acrescenta vetor normalizado ao movimento e copia Bubbling. Não copia `seekAmount` ou `ricochet`, que conservam defaults `0.3F` e false. O retorno da nova tentativa de `addFreshEntity` também é descartado. Esse recorte compartilhado não certifica a ficha individual de Bouncing Bolt/Enveloping Bubble nem anula sua incompatibilidade declarada com Triple Splash.
- **Remoção e colisão:** janelas de `tick@330–399` cobrem descarte em blocos sem ar fora de água/bolha, arrasto nominal `0.9F` e gravidade nominal `−0.07F` quando habilitada; `@655–718` cobrem consulta de colisão, gate `EventHooks.onProjectileImpact`, decremento de `dieIn` positivo e descarte ao chegar a zero. `remove` emite o splash visual uma vez no servidor. Esses valores não estabelecem duração máxima de voo ou cooldown.

O tick tem **362 instruções**; esta ficha usa **janelas locais delimitadas**, sem alegar seu CFG integral ou o comportamento de superclasses/eventos externos. A escolha do alvo, homing, área de dano e eventual ricochete são superfícies distintas.

## 5. Custos, autoria, estado e persistência

Depois do loop e do join servidor/cliente, `use@355–363` solicita o stat `Stats.ITEM_USED`. Em `@366–381`, se **`!player.getAbilities().instabuild`**, pede **1 ponto de durabilidade** da stack usada por `ACCompat.hurtAndBreak(stack,1,player,hand)`. O wrapper converte a mão em slot e delega a `ItemStack.hurtAndBreak`. É **um pedido no fim da invocação**, não um por cada bolt, e não usa o retorno dos spawns como recibo. O valor efetivo de desgaste/quebra pertence à engine.

Som, swing, leitura de Soak Seeking, stat e pedido de desgaste estão fora da guarda local de criação servidor. Não expandir a exclusividade servidor do loop para todo `use`, nem concluir dupla cobrança física: despacho de uso e processamento da engine continuam fronteiras externas. O método retorna por `ACCompat.useSidedSuccess`.

Não há cobrança própria adicional de Triple Splash por bolt, mana, stamina, fome, XP ou munição nesse caminho, nem timer próprio de cooldown/carga. `anvil_cost=4` é dado de aquisição. [Seapairing](seapairing.md) conserva sua manutenção passiva separada; não transformar reparo em recibo ou desconto de cada cast.

O owner é atribuído no construtor; a fonte de dano usa `getOwner` e trata owner não LivingEntity como null para a factory. A stack não é relida pelo bolt para recalcular a quantidade: **N é local à invocação de `use`**, não um estado que gere novos bolts em ticks posteriores. Os dados sincronizados próprios incluem `BUBBLING` e `ARC_TOWARDS_ENTITY_UUID`, com defaults false e Optional vazio; `seekAmount`, `ricochet` e `dieIn` são campos próprios.

Os overrides completos `readAdditionalSaveData` e `addAdditionalSaveData`, **6 instruções cada**, leem/gravam somente **`Bubbling`**, sem chamada a super. Não serializam ali owner, UUID do alvo, `seekAmount`, `ricochet`, `dieIn`, índice do loop ou nível Triple Splash. Essa omissão própria não certifica persistência herdada, perda/restauração física, sincronização integral ou autoria após reload. Não criar um segundo estado persistente ou relançamento para compensá-la por inferência. Save/load, unload, reconexão e dimensão exigem QA.

## 6. Parâmetros úteis para perks e autoridade

| Superfície | Contrato individual a preservar |
|---|---|
| Quantidade / nível | `L>0 ? 3 : 1`; uma leitura antes do loop, sem escala adicional para níveis positivos externos |
| Spread / origem / velocidade | Offsets `0/−50/+50°`, origem dependente de mão/cabeça, velocidade de entrada `2/1/1`, offset de pitch `−20F`, imprecisão `12F`; não equivalem a alcance, precisão final ou cone fixo |
| Targeting / alcance | Um alvo inicial compartilhado, filtros do helper e `128D` de consulta; distinguir hit físico e busca/homing |
| Dano / tipo / área / tamanho | **N/A como multiplicadores próprios de Triple Splash:** o ID escolhe a quantidade; `3F`, fonte e AABB inflada pertencem ao Water Bolt. Não há aumento próprio comprovado de dano unitário, hitbox ou área |
| Tempo / duração / frequência | **N/A próprios:** sem recarga, DoT, duração ou intervalo introduzidos pelo ID. Ticks, contador de remoção e callback nativos não são cadência de cast |
| Custo / recurso | Um pedido de desgaste por `use` que alcança o bloco, com exceção `instabuild`; não cobrar por bolt nem vincular crédito a stat/swing |
| Sinergias / compatibilidade | Respeitar exclusão reversa de Bouncing Bolt; Soak Seeking e Bubbling têm parâmetros/consumidores próprios, sem certificação automática de irmãos |
| Autoria / Mastery / XP | Uma ação raiz do Sea Staff, **+0 raízes mágicas novas**; distinguir tentativa de inserção, inserção aceita, colisão, pedido de hurt e resultado autorizado. Deduplicar crédito dos bolts e de eventuais descendentes |

Black Arcana mantém seu runtime mágico; Alex's Caves conserva movimento, seleção, dano e liquidação nativos. Enshrouded e RPG Skill Tree podem fornecer progressão/perks apenas por boundary demonstrado. Métodos, campos públicos, setters e `EventHooks.onProjectileImpact` são superfícies observadas, **não hooks mutadores seguros certificados**. Nenhum adapter executável, segundo cast, segunda cobrança ou promoção de Stage é autorizado: **`NO_MUTATION` / `fail-closed`**.

## 7. Evidência, contabilidade e QA

O [manifesto individual](../EXACT-TRIPLE-SPLASH-CONTRACT-1.0.10.json), a [reprodução](../EXACT-TRIPLE-SPLASH-CONTRACT-1.0.10.md) e os [testes semânticos](../../../../../docs/qa/alexscaves_1010_triple_splash_cards_test.py) ligam os sete eixos: identidade, comportamento, parâmetros, alvo, custos, integração e validação. A reprodução parte do JAR SHA-exato e fixa recursos, traduções, Fieldrefs diretos, classes e instruções JVM. A busca global não equivale a inventário de consumidores reflexivos ou transformados.

Os corpos selecionados completos incluem `SeaStaffItem.use` **189**, seu helper de alvo **119**, construtores do bolt/defaults, getters/setters sincronizados, `onHitEntity` **37**, `onHitBlock` **28**, `damageMobs` **105**, `onRicochetHit` **122**, `remove` **59** e NBT próprio **6/6** instruções. O `tick` de **362 instruções** permanece **PARTIAL**, com janelas selecionadas dentro do limite de 256 âncoras por método; fingerprint do corpo não substitui cobertura semântica integral. O initializer do registro também é janela delimitada.

As provas anteriores de [Sea Staff](../EXACT-TECHNICAL-CONTRACTS-1.0.10.json), [Soak Seeking](../EXACT-SOAK-SEEKING-STATIC-1.0.10.json) e [Seapairing](../EXACT-SEAPAIRING-CONTRACT-1.0.10.json) conservam bytes e escopos. A presença de encantamentos irmãos no mesmo corpo não conclui seus contratos individuais.

**Contabilidade:** uma ficha individual; **+0 raízes mágicas novas**. `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, provider integral aberto. As vinte fichas parciais anteriores continuam parciais; não há promoção de Stage.

QA física pendente: níveis 0/I/externos, mãos e rotação cabeça/corpo; quantidade tentada versus aceita, spawn recusado e reentrada; spread/velocidade/imprecisão e alvo compartilhado; homing, colisão, eventos cancelados, dano aceito/recusado, defesas, PvP, aliados e claims; custos/creative, cliente e dedicado; exclusão e datapacks; save/load, unload, dimensão, autoria e sincronização; crédito único de Mastery após resultado autorizado. A fila atual é mantida no [crosswalk alfabético](../ENCHANTMENT-PERK-CROSSWALK-1.0.10.md).
