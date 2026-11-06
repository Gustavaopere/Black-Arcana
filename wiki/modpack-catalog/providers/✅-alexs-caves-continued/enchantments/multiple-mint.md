# Multiple Mint — `alexscaves:multiple_mint` (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Integração:** `NO_MUTATION`. O recorte conclui o encantamento e os consumidores delimitados de quantidade/distribuição de peppermints; não conclui Punting, Seekcandy, Spell Lasting, o renderer ou o provider integral.

## 1. Identidade e descrição original

- **Provider / versão:** Alex's Caves Continued / `alexscaves`, Minecraft 1.21.1; `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Recurso:** `data/alexscaves/enchantment/multiple_mint.json`, 364 bytes; SHA-256 `e7357f60b417fa10f5c64518dc51ab61365dca1a410c342ef2aa0604de40af03`.
- **Tag de item:** `data/alexscaves/tags/item/enchantable/sugar_staff.json`; SHA-256 `eb9f84b401224aba54ba91a239e4dd5b775d82012cecf9b03e8f9608e12b11fc`.
- **Descrição literal de `en_us.json`:** “An additional peppermint is summoned for each level”. Tradução explicativa: cada nível acrescenta uma tentativa de criar peppermint. Não há entrada própria no `pt_br.json` examinado; a descrição não certifica inserção bem-sucedida no mundo.
- **Produtor:** `server/item/SugarStaffItem.class`, SHA-256 `d670f887debdfb95f93a52b0c58b3033154a9aa20777fb8bd2a1673ee1407c3f`. **Consumidor:** `server/entity/item/SpinningPeppermintEntity.class`, SHA-256 `655e607acf3d22a9caf6be93d9010f7a11c3836e4c680b04878110e61aca4f90`. Prefixo de classes: `com/github/alexmodguy/alexscaves/`.
- **Provas:** [manifesto individual](../EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.json), [reprodução](../EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.md) e [ação Peppermint Cast](../actions/sugar-staff-peppermint-cast.md).

A busca nas classes do JAR por referência ao campo `MULTIPLE_MINT` encontrou o registro `ACEnchantmentRegistry` e o item `SugarStaffItem`; não comprova ausência de reflexão, transformações ou consumidores externos. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e é apenas corroboração adjacente. Os parâmetros abaixo vêm dos bytes **1.0.10**.

## 2. JSON, níveis e aquisição

| Campo | Valor literal publisher | Significado / limite |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.multiple_mint` | Chave de tradução |
| `supported_items` | `#alexscaves:enchantable/sugar_staff` | Tag contém somente `alexscaves:sugar_staff` |
| `weight` | `5` | Peso declarado, não chance medida |
| `max_level` | `2` | Domínio normal publicado I–II |
| `min_cost` | `base=1`, `per_level_above_first=9` | I/II: 1/10 pelo modelo JSON |
| `max_cost` | `base=41`, `per_level_above_first=10` | I/II: 41/51 pelo modelo JSON |
| `anvil_cost` | `2` | Custo de encantamento, não débito por projétil |
| `slots` | `mainhand` | Slot declarado no recurso |
| `effects` / `exclusive_set` | Ausentes neste JSON | Não comprova ausência de comportamento Java ou compatibilidade global |

O registro associa `MULTIPLE_MINT` à chave `multiple_mint`. `ACCompat.enchantLevel` lê os encantamentos atuais da stack, retorna o primeiro inteiro cujo Holder corresponde à chave, ou zero. Esse leitor e a soma no item não aplicam clamp ao máximo II nem revalidam tag/slot. Níveis/componentes forçados ficam fora do domínio homologado para perks.

As quatro tags empacotadas `minecraft:in_enchanting_table`, `minecraft:non_treasure`, `minecraft:on_random_loot` e `minecraft:tradeable` contêm o ID. O loot `entities/licowitch.json` declara Sugar Staff condicionado a morte por jogador: chance sem Looting `0.025`, e chance encantada linear com base `0.035` e incremento `0.01` por nível acima do primeiro. São dados de aquisição do item, sem garantir drop, encantamento na instância ou resolução efetiva dos datapacks do modpack.

## 3. Gatilho e quantidade ligada ao ângulo inicial

`SugarStaffItem.use(Level,Player,InteractionHand)InteractionResultHolder` obtém a stack e só executa spawn/custo/cooldown dentro da guarda servidor `@7–11`. Lê o estado de sneak, solicita swing e chama a aquisição do Sea Staff com argumento `32D` antes de escolher a ação. Sneak seleciona a **Hex**, que é outra raiz já existente. Multiple Mint só é lido no ramo **sem sneak**, em `@186–196`; não adiciona carga ou callback de release.

```text
count = 3 + enchantLevel(stack, MULTIPLE_MINT)  // uma leitura, antes do desgaste
for i = 0; i < count; i++:
    startAngle = (float)(i * 360) / (float)count
    // configurar entidade e solicitar addFreshEntity
```

| Nível lido | Tentativas no caminho normal | Separação dos ângulos iniciais |
|---|---:|---:|
| 0 — sem encantamento | 3 | 120° |
| I | 4 | 90° |
| II | 5 | 72° |

**A quantidade também é o denominador da distribuição angular.** O local 7 recebe `3+L` em `@196`, limita o loop em `@208–212` e é relido na divisão `@394–405`. `i*360` é aritmética inteira antes da conversão para float. A entidade não relê Multiple Mint; não tratar o nível como multiplicador de dano, raio ou duração por hit.

Cada tentativa cria/casta uma `SpinningPeppermintEntity`, posiciona em `player.position + (0,height*0.45F,0)`, configura movimento, owner, ângulo e lifespan **80**, e solicita inserção em `@418`. O booleano é descartado em `@421`; `iinc @422` ocorre sem contador de sucesso ou retry. O caller não tem guarda local de null antes de configurar a entidade. As quantidades da tabela são tentativas em conclusão normal, não entidades, hits ou kills garantidos. Uma falha intermediária não constitui uma transação atômica com os custos finais.

## 4. Geometria, movimento, targeting e dano

O registro `ACEntityRegistry.lambda$static$75` declara categoria **MISC**, largura **0.8F** e altura **0.4F** para `spinning_peppermint`. A entidade não sobrescreve `getDimensions` entre seus métodos próprios. **Dimensões, raio de órbita e escala visual são superfícies diferentes**; Multiple Mint não escala a hitbox neste consumidor.

| Parâmetro | Configuração do item | Leitura / limite no consumidor |
|---|---|---|
| Spawn | Posição do jogador com Y `height*0.45F` | Não prova inserção aceita |
| Raio | `3.5F` | Tick sobrescreve para `3F`; seeking pode sobrescrever novamente |
| Speed | `8F` com Punting; `12F` sem Punting; `50F` com Seekcandy + alvo | Tick escreve `7F` antes do movimento; não são velocidades sustentadas comprovadas |
| Straight / yaw | Punting positivo: true e `180+headYaw+(i−1)*15`; sem Punting: false e `180+(i−1)*30` | Seeking não altera por si só STRAIGHT |
| Ângulo inicial | `(i*360)/(float)count` | Órbita usa startAngle + spinAngle; não é yaw de disparo nem raio de colisão |
| Órbita | Centro sincronizado | Usa `min(1F,tickCount/30F)*spinRadius`, delta escalado por `0.05D*spinSpeed`, spinAngle incrementado por speed |
| Seeking | ID da entidade adquirida | Com owner Player e ID resolvido, radius vira `4−4*min(1F,tickCount/30F)`; o centro é posição do peppermint + vetor ao olho do alvo limitado a módulo 1 |

O tick captura `getSpinAroundPosition()` no local 1 em `@74–78` **antes** de atualizações do centro por owner/seeking. O ramo orbital posterior consome esse local capturado; um setter de centro não comprova consumo imediato no mesmo tick. O ramo reto acrescenta vetor local Z `−0.01F*spinSpeed`, rotacionado pelo yaw; quando há gravidade, aplica arrasto `0.9F` e Y `−0.08D`. Colisão vertical acrescenta Y `0.9F` e multiplica X/Z por `0.4D`. Mais peppermints não convertem automaticamente trajetória reta em órbita, homing ou AoE.

**Aquisição:** `SeaStaffItem.getClosestLookingAtEntityFor(Level,Player,double)Entity` usa `32D` no clip, com `VISUAL/NONE`. O fallback consulta uma caixa em torno do hit, `±0.5`, inflada por 15 e pelo argumento; escolhe o candidato mais próximo **do hit**. Exige Mob, diferente do jogador, aliança falsa em ambos os sentidos e linha de visão, sem `isAlive` explícito nesse helper. Portanto `32` não é um cap radial certificado de voo/alcance. A seleção de Mob não exclui Player dos consumidores independentes de colisão.

**Colisão/dano:** `hurtEntities()` consulta LivingEntity na **AABB própria**, sem inflação ou teste radial extra. Exige `peppermint.isAlliedTo(target)==false`, campo owner não nulo e target diferente de owner. Para owner comum, testa `target.isAlliedTo(owner)`; para Licowitch, consulta `isFriendlyFire`. Esses testes têm direção própria e não são uma autorização geral de PvP ou proteção de mundo.

A factory usada é `DamageSources.mobProjectile(this,owner)`, com pedido de dano **3F** via `ACCompat.hurt`; o encantamento não troca DamageType nem acrescenta um bônus por impacto. Só retorno true permite knockback `0.30000001192092896D` (`0.3F` alargado). Após iterar, **qualquer** dano aceito com seeking ID diferente de −1 permite `discard`, sem exigir que a vítima fosse a entidade selecionada para seeking. O método e sua chamada final no tick não têm guarda própria adicional de lado lógico. Owner/configuração/engine continuam fronteiras para os efeitos reais; não declarar dano cliente autorizado, DPS proporcional à quantidade, invulnerabilidade vencida ou Mastery por spawn.

## 5. Duração, owner e persistência

O construtor inicia `despawnsIn=-1`. Defaults sincronizados: centro vazio, radius/speed **1F**, startAngle **0F**, straight **false**, lifespan **200** e seeking ID **−1**. O cast normal sobrescreve lifespan para **80**; esse valor difere do default da classe.

No primeiro tick com contador −1, copia `getLifespan()` para `despawnsIn`; se positivo, decrementa na mesma chamada. Esse decremento não tem guarda própria de lado lógico. Quando o contador já não é positivo, o ramo servidor solicita `discard @59`, mas continua executando o corpo, inclusive movimento e a chamada `hurtEntities @737`. Não garantir exatamente 80 ticks totais de existência ou ausência de tentativa de dano na chamada que solicita remoção. Alterar `LIFESPAN` depois da inicialização não reinicializa automaticamente o contador nesse caminho.

`setOwner` armazena LivingEntity e UUID, ou limpa ambos para null. `getOwner` só busca UUID quando o campo owner está nulo, no **ServerLevel atual**, via `getEntity(UUID)` e teste LivingEntity. Não é uma resolução global, offline ou entre dimensões; owner atribuído não prova crédito de kill, procs ou XP.

Os corpos NBT tratam `DespawnsIn`, `Straight`, `Lifespan`, owner UUID condicional, centro `AroundX/Y/Z`, `SpinSpeed`, `SpinRadius`, `StartAngle` e `SpinAngle`. **Não salvam seeking ID.** O write grava X/Y/Z, mas o read exige as três chaves e constrói literalmente **`Vec3(AroundX,AroundZ,AroundZ)`** em `@99–120`. A divergência está no binário; não é uma falha de reload reproduzida no modpack. Continuidade de seeking, owner, órbita e interpolação após unload/restart continua pendente.

## 6. Custos e cooldown

O registro do Sugar Staff declara durabilidade **100** e raridade **UNCOMMON**; enchantability **1**, com `isEnchantable` condicionado a stack de contagem 1. O item não soma um débito por nível ou por peppermint no loop.

No caminho normal, o cooldown começa em **80** ticks; Punting positivo o muda para **20** dentro do loop. Seekcandy positivo **com alvo adquirido** o muda depois para **50**, prevalecendo sobre Punting. O helper final `@456–461` usa `stack.getItem()` no gerente de cooldown do Player; a chave é o Item, compartilhado com a outra escolha do Sugar Staff, não cada projétil ou stack única. Em seguida, `@464–468` solicita desgaste **1** por callback via `hurtAndBreakUsedHand`, que usa a mão em uso e delega à engine.

São pedidos finais após o loop, sem multiplicação pelo número de entidades ou condicionamento a inserções aceitas. Não é garantia de execução única sob callbacks reentrantes, nem débito/reembolso atômico caso uma operação anterior falhe. Não há débito próprio de mana, stamina, fome ou consumível nos corpos auditados. Níveis forçados que produzam contagem não positiva podem pular o loop, inclusive os overrides de cooldown internos, e ainda alcançar som/cooldown/desgaste normais; esse domínio não foi testado fisicamente.

## 7. Integração e evidência

| Perk / sistema pretendido | Contrato a preservar | Estado |
|---|---|---|
| Quantidade / distribuição | Leitura única `3+L`, limite do loop e denominador angular compartilhados | Hook `NOT_VERIFIED`; não duplicar o cast nem contar tentativa como spawn aceito |
| Tamanho / área / alcance | Dimensões 0.8×0.4, AABB de dano, órbita e aquisição por clip são distintas | Não transformar raio da órbita ou argumento 32 em raio universal de dano |
| Movimento | Configuração inicial, sobrescritas do tick e centro capturado em momentos distintos | Setter interno não é seam de integração homologada |
| Dano / autoria / Mastery | Factory nativa, hurt aceito, owner e descarte por seeking | Não multiplicar dano/XP por quantidade solicitada ou por som |
| Duração / persistência | Lifespan inicializado uma vez, contador próprio, seeking não salvo e centro relido com divergência | Hook e QA de reload pendentes |
| Custo / cooldown | Pedidos finais por callback, precedência Punting/Seekcandy e cooldown por Item | Não repetir wear/cooldown por entidade |
| Black Arcana / Enshrouded / RPG Skill Tree | Provider conserva cast, targeting, dano, movimento e remoção | `NO_MUTATION`; nenhum adapter executável ou Stage promovido |

O [manifesto individual](../EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.json) e os [testes semânticos](../../../../../docs/qa/alexscaves_1010_multiple_mint_cards_test.py) protegem identidade, quantidade/ângulo, guards, aceitação de spawn, custos, tamanho, lifecycle e persistência. Métodos extensos têm checkpoints causais delimitados, sem promessa de CFG completo ou homologação da rede/render. A [prova comum](../EXACT-TECHNICAL-CONTRACTS-1.0.10.json), a ficha da ação e os certificados anteriores permanecem preservados.

**Contabilidade:** uma ficha individual de encantamento; **+0 raízes mágicas novas**. `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, provider integral aberto. As vinte fichas parciais anteriores permanecem parciais.

QA física pendente: níveis 0/I/II e componentes forçados, sneak/normal e as duas mãos, combinações Punting/Seekcandy, criação nula/spawn recusado, movimento/colisão/dano aceito, owner/PvP/alianças, callbacks e custos, alteração de lifespan após início, seeking/órbita em unload/restart e multiplayer. Próxima identidade sem ficha individual: `alexscaves:peppermint_punting`.
