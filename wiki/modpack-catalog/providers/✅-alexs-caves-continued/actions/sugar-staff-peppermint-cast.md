# Sugar Staff — Peppermint Cast

- Provider: **Alex's Caves Continued** (`alexscaves`)
- Version: `1.0.10`
- Exact physical/publisher SHA-1: `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`
- Owner: `alexscaves:sugar_staff`
- Trigger: normal direct item use
- State: `COUNTED_EXACT`

## Semantic identity

Normal use selects the provider Peppermint Cast branch and creates its peppermint action pattern around/from the player. This is distinct from the sneaking Hex branch because the player deliberately selects a separate causal action.

## Exact acquisition

Exact provider data closes Sugar Staff through Licowitch loot.

## Boundary

Numerical tuning, cooldowns, targeting, entities, effects, particles and sounds remain provider authority. Black Arcana catalogs the identity and must not replay provider settlement.

Sources: `../EXACT-1.0.10-ARTIFACT-AUDIT.md`, `../ITEM-ACTION-DISPOSITION-1.0.10.md`.

## Contrato técnico exato — JAR 1.0.10

A leitura estática abaixo usa o JAR físico/publisher de **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Métodos, descritores JVM e offsets de bytecode são localizadores reproduzíveis com `javap -p -s -c`, não APIs externas prometidas. A [prova técnica comum](../EXACT-TECHNICAL-CONTRACTS-1.0.10.md) registra o escopo da evidência. **Parâmetros estáticos: `VERIFIED_EXACT_BINARY`; configuração/hook mutador: `NOT_VERIFIED`; QA no jogo: `NOT_TESTED`.**

O trabalho de fonte público do PR #944 permanece como corroboração: `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **`mod.version = "1.1.1"`** em [`stonecutter.properties.toml:16`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/stonecutter.properties.toml#L16). Esse snapshot não é fonte comprovado da versão física `1.0.10`; os números certificados nesta seção vêm dos bytes do JAR, sem alegação de paridade de build.

### 1. Identidade

`SugarStaffItem.use` com `!player.isShiftKeyDown()` seleciona a raiz deliberada `sugar-staff-peppermint-cast`; Hex continua sendo a outra escolha do jogador. Quantidade, órbita, punting, seeking e colisões liquidam o mesmo cast: **0 novas raízes semânticas**. Item `alexscaves:sugar_staff`; entidade `SpinningPeppermintEntity`.

### 2. Comportamento e lifecycle

`SugarStaffItem.use @7–18, @186–468` cria peppermints, atribui owner, aplica cooldown e solicita durabilidade apenas no servidor. `SpinningPeppermintEntity.tick()V @4–59` inicializa `despawnsIn` de `getLifespan()` se `-1`, decrementa se positivo e, quando já não positivo, descarta no servidor. O método continua após `discard`; `80` é o valor inicial do contador, não prova de exatamente 80 chamadas totais ao corpo de tick.

O tick aplica órbita ou trajetória reta (`@465–733`), e chama `hurtEntities()V` em `@736–737`, sem guard server-side próprio nessa chamada. O owner do cast é atribuído no servidor; não duplicar os efeitos locais como outra autoridade de dano. `hurtEntities()V @184–197` descarta se **qualquer dano foi aceito** e `getSeekingEntityId()!=-1`, sem exigir que a entidade danificada fosse o alvo selecionado.

Persistência própria: `readAdditionalSaveData`/`addAdditionalSaveData(Lnet/minecraft/nbt/CompoundTag;)V` tratam `DespawnsIn`, `Straight`, `Owner`, `AroundX/Y/Z`, `SpinSpeed`, `SpinRadius`, `StartAngle`, `SpinAngle`, `Lifespan`; **não** salvam `SEEKING_ENTITY`. O read verifica as três coordenadas, mas constrói literalmente `Vec3(AroundX, AroundZ, AroundZ)` (`read @64–123`), enquanto o write grava X/Y/Z corretos (`write @45–79`). `getOwner()Lnet/minecraft/world/entity/LivingEntity; @0–58` resolve UUID no servidor e o tick chama esse getter em `@244–247`. Não prometer continuidade integral de seeking/órbita após reload.

### 3. Parâmetros e getters

| Fato certificado | Localizador binário |
|---|---|
| Quantidade `3 + level(MULTIPLE_MINT)` | `SugarStaffItem.use @186–196` |
| Spawn em `player.position() + (0, height*0.45F, 0)`; owner jogador; ângulo inicial `i*360/(float)count`; lifespan de cast `80` | `use @238–257, @386–418` |
| Punting positivo: `STRAIGHT=true`, yaw `180 + headYaw + (i-1)*15`, speed inicial `8F` | `use @260–302` |
| Sem Punting: `STRAIGHT=false`, yaw `180+(i-1)*30`, speed inicial `12F` | `use @312–339` |
| Seekcandy positivo + alvo: grava **entity ID**, speed inicial `50F` | `use @342–372` |
| Todos recebem radius inicial `3.5F` | `use @379–383` |
| Defaults sincronizados de classe: radius/speed `1F`, ângulo `0F`, straight `false`, lifespan **`200`**, seeking ID `-1`, centro vazio | `SpinningPeppermintEntity.defineSynchedData(Lnet/minecraft/network/syncher/SynchedEntityData$Builder;)V @0–85` |
| Todo tick sobrescreve radius para `3F` e speed para **`7F`** antes do movimento | `tick()V @62–71` |
| Com owner Player e ID resolvido: radius passa a `4F - 4F*min(1F,tickCount/30F)` e centro segue vetor ao olho do alvo, limitado a módulo 1 | `tick()V @357–453` |
| Órbita usa `min(1F,tickCount/30F)*getSpinRadius()`, ângulo `startAngle+spinAngle`, delta `0.05D*getSpinSpeed()`, incrementando spinAngle pelo speed | `tick()V @638–733` |
| Trajetória reta adiciona vetor local Z `-0.01F*getSpinSpeed()`; com gravidade, arrasto `0.9F` e Y `-0.08D`; colisão vertical soma Y `0.9F` e multiplica X/Z `0.4D` | `tick()V @482–596` |
| Dano solicitado `3F` via `mobProjectile(this, owner)`; knockback `0.3F` ampliado para double, só se `hurt` retorna true | `hurtEntities()V @5–17, @140–178` |
| `getSpinSpeed()F`, `getSpinRadius()F`, `getStartAngle()F`, `getLifespan()I`, `getSeekingEntityId()I`, `isStraight()Z` leem dados sincronizados, não constantes imutáveis | getters `@0–16`; setters `(F)V`, `(I)V`, `(Z)V @0–14` |
| `SugarStaffItem.getEnchantmentValue()I = 1`; `isEnchantable(Lnet/minecraft/world/item/ItemStack;)Z` exige `count == 1` | getters `@0–1`, `@0–13` |

**Sobrescrita runtime:** `8F/12F/50F` e `3.5F` são configuração inicial do item. O tick grava speed `7F` e radius `3F`; o ramo seeking ainda pode sobrescrever o radius nesse tick. Não registrar `50F` como velocidade sustentada nem `3F` como raio universal. O centro da órbita é capturado antes de atualizá-lo (`tick @74–78`), por isso um setter não prova leitura imediata no mesmo tick.

### 4. Targeting, área e filtros

O item passa `32D` a `SeaStaffItem.getClosestLookingAtEntityFor` (`use @25–33`), descritor `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;D)Lnet/minecraft/world/entity/Entity;`. A função usa clip `VISUAL/NONE` e, no fallback, caixa `±0.5D` no hit inflada `15D` e depois `dist`; elege o candidato mais próximo **do hit**. Exige `Mob`, diferente do jogador, não aliado em ambos os sentidos e linha de visão, sem chamada explícita `isAlive` (`SeaStaffItem helper @3–40, @114–174, @206–275`). Portanto `32` não é cap radial certificado de aquisição/voo.

`getSeekingEntityId()I` guarda um ID efêmero, resolvido por `Level.getEntity(int)` (`tick @357–380`), sem nova validação explícita de aliança/linha de visão nesse ramo. Se a resolução falha, o centro volta à posição do jogador. Seeking orienta o centro; não muda por si só `STRAIGHT`.

`hurtEntities()V @0–140` consulta `LivingEntity` na **AABB própria**, sem inflação ou teste radial extra. Exige `!bolt.isAlliedTo(target)`, owner não nulo e target diferente do owner; para owner comum exige `!target.isAlliedTo(owner)`, e para `LicowitchEntity` delega `!licowitch.isFriendlyFire(target)`. Não confundir o raio da órbita com a hitbox individual nem tratar cada tick como spell independente.

### 5. Custos, recarga e dados do item

`SugarStaffItem.use` tem descritor `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;`. Cooldown inicial **80** ticks (`@201–203`); Punting o troca por **20** (`@305–307`); Seekcandy **com alvo** o troca depois por **50** (`@375–377`), prevalecendo sobre Punting. `@456–461` aplica o valor através de `ACCompat.addCooldown(Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/item/ItemStack;I)V`, que chama `ItemCooldowns.addCooldown(stack.getItem(), ticks) @0–12`: o cooldown pertence ao item e é compartilhado com a escolha Hex.

`use @464–468` solicita **1** de durabilidade por cast via `ACCompat.hurtAndBreakUsedHand(Lnet/minecraft/world/item/ItemStack;ILnet/minecraft/world/entity/LivingEntity;)V @0–13`; o wrapper usa `getUsedItemHand()`, converte para slot e delega `ItemStack.hurtAndBreak`. Não há checagem `instabuild` própria nesse ramo do item nem chamada direta de mana; a aplicação efetiva de durabilidade pertence ao engine. `ACItemRegistry.lambda$static$184()Lnet/minecraft/world/item/Item; @11–22` registra durabilidade `100`, raridade `UNCOMMON`.

`data/alexscaves/loot_table/entities/licowitch.json` (4.120 bytes, SHA-256 `157ba186f052f989fc31bd016ae3352eaa77c58ec1a8a639c91774f239e34526`) inclui `sugar_staff`, condicionado a kill pelo jogador e chance base `0.025`, com Looting linear base `0.035` e incremento `0.01` por nível acima do primeiro. `data/alexscaves/tags/item/enchantable/sugar_staff.json` (51 bytes, SHA-256 `eb9f84b401224aba54ba91a239e4dd5b775d82012cecf9b03e8f9608e12b11fc`) contém o item. JSONs embarcados declaram Multiple Mint máximo `2`, Punting/Seekcandy `1`; a fórmula do bytecode não aplica cap próprio. Datapacks efetivos: `NOT_VERIFIED`.

### 6. Integração e autoridade

`use`, `tick`, `hurtEntities` e os setters são internos observados; hook mutador externo com ordem de aplicação e persistência comprovadas: **`NOT_VERIFIED`**. Perks de speed/radius/lifespan exigem seam com momento de leitura verificado e ficam **⛔ fail-closed**. Black Arcana não cria segundo peppermint, não repete dano/knockback a cada tick e não reaplica cooldown ou durabilidade.

### 7. Validação e localizadores

Bytecode e dados embarcados: `VERIFIED_EXACT_BINARY`; configuração efetiva, seam mutador, reload no modpack: `NOT_VERIFIED`; QA física: `NOT_TESTED`. `3F` é dano solicitado, sem garantia de dano cumulativo, invulnerabilidade vencida ou DPS.

| Entrada no JAR | Bytes | SHA-256 |
|---|---:|---|
| `com/github/alexmodguy/alexscaves/server/item/SugarStaffItem.class` | 7.145 | `d670f887debdfb95f93a52b0c58b3033154a9aa20777fb8bd2a1673ee1407c3f` |
| `com/github/alexmodguy/alexscaves/server/entity/item/SpinningPeppermintEntity.class` | 14.538 | `655e607acf3d22a9caf6be93d9010f7a11c3836e4c680b04878110e61aca4f90` |

Corroboração pública preservada: [`SugarStaffItem.java`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/item/SugarStaffItem.java), [`SpinningPeppermintEntity.java`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/entity/item/SpinningPeppermintEntity.java), [`SeaStaffItem.java`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/item/SeaStaffItem.java), snapshot **1.1.1**, sem prova de paridade com 1.0.10.

Static evidence grade: `SHA_EXACT_BINARY_BEHAVIOR`. Claim scope: `STATIC_TECHNICAL_CATALOG_ONLY`. Hook: `NOT_VERIFIED`. Physical QA: `NOT_TESTED`.
