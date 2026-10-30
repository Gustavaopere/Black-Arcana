# Sea Staff — Water Bolt

- Provider: **Alex's Caves Continued** (`alexscaves`)
- Version: `1.0.10`
- Exact physical/publisher SHA-1: `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`
- Owner: `alexscaves:sea_staff`
- Trigger: direct item use
- State: `COUNTED_EXACT`

## Semantic identity

One deliberate player action causes Alex's Caves Continued to create and launch its Water Bolt action. Entity ticks, targeting, impact and enchantment modifiers are downstream settlement of this same root.

## Exact acquisition

Exact provider data closes Sea Staff through Deep One Mage barter loot.

## Boundary

Numerical tuning, cooldowns, targeting, entities, effects, particles and sounds remain provider authority. Black Arcana catalogs the identity and must not replay provider settlement.

Sources: `../EXACT-1.0.10-ARTIFACT-AUDIT.md`, `../ITEM-ACTION-DISPOSITION-1.0.10.md`.

## Contrato técnico exato — JAR 1.0.10

A leitura estática abaixo usa o JAR físico/publisher de **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Métodos, descritores JVM e offsets de bytecode são localizadores reproduzíveis com `javap -p -s -c`, não APIs externas prometidas. A [prova técnica comum](../EXACT-TECHNICAL-CONTRACTS-1.0.10.md) registra o escopo da evidência. **Parâmetros estáticos: `VERIFIED_EXACT_BINARY`; configuração/hook mutador: `NOT_VERIFIED`; QA no jogo: `NOT_TESTED`.**

O trabalho de fonte público do PR #944 permanece como corroboração: `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **`mod.version = "1.1.1"`** em [`stonecutter.properties.toml:16`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/stonecutter.properties.toml#L16). Esse snapshot não é fonte comprovado da versão física `1.0.10`; os números certificados nesta seção vêm dos bytes do JAR, sem alegação de paridade de build.

### 1. Identidade

`SeaStaffItem.use` escolhe uma única raiz deliberada `sea-staff-water-bolt`. Triple Splash, homing, colisões, Bubbling e ricochete liquidam essa raiz sob autoridade do provider; **0 novas raízes semânticas**. O item é `alexscaves:sea_staff`, a entidade é `WaterBoltEntity`.

### 2. Comportamento e lifecycle

O método `use` cria as entidades apenas no servidor (`@74–355`), atribui owner e UUID do alvo, e contabiliza `Stats.ITEM_USED` (`@355–363`). `WaterBoltEntity.tick()V` consulta o alvo no servidor (`@4–158`), move o projétil, aplica arrasto `0.9F` e gravidade `-0.07F` quando habilitada (`@368–399`), e delega colisão a `ProjectileUtil`/`EventHooks.onProjectileImpact` (`@655–690`). Esses valores de movimento não são alcance máximo de voo.

`onHitEntity(Lnet/minecraft/world/phys/EntityHitResult;)V @32–75` exige servidor, hit não pertencente ao owner e `tickCount > 2`; chama `damageMobs` e inicializa `dieIn=5` se era `-1`. `onHitBlock(Lnet/minecraft/world/phys/BlockHitResult;)V @32–56` chama o mesmo dano no servidor, sem a condição `tickCount > 2`. Hits posteriores podem chamar dano durante a contagem; ela não é um bloqueio global de novos hits. `tick()V @693–718` decrementa e descarta quando chega a zero; `@330–362` também descarta se a AABB não contém ar e a entidade não está em água/bolha. `remove(Lnet/minecraft/world/entity/Entity$RemovalReason;)V` emite o splash de remoção uma vez no servidor.

As rotinas NBT próprias `readAdditionalSaveData`/`addAdditionalSaveData(Lnet/minecraft/nbt/CompoundTag;)V @0–11` leem/escrevem apenas `Bubbling`, sem chamada ao super nesses overrides. Não persistem ali UUID do alvo, `seekAmount`, `ricochet` ou `dieIn`; não prometer restauração integral do cast após reload.

### 3. Parâmetros e getters

| Fato certificado | Localizador binário |
|---|---|
| Um bolt baseline; `TRIPLE_SPLASH > 0` gera 3, yaw adicional `0/-50/+50°` | `SeaStaffItem.use @95–145` |
| `shootFromRotation` recebe pitch do jogador, yaw + spread, offset `-20F`, velocidade `2F` central / `1F` lateral, imprecisão `12F` | `use @241–269` |
| Origem deslocada pela largura do jogador `*1.1F`, `eyeY-0.4F`, ângulo da cabeça `+45°` mão principal / `-45°` secundária | `use @158–238` |
| `seekAmount = 0.3F + 0.2F * level(SOAK_SEEKING)` | `use @314–324`; default do construtor `0.3F` |
| Homing exige alvo, `(tickCount > 3 \|\| (double)seekAmount > 0.3D)`, `dieIn == -1`, distância `>1.5F`, e `(tickCount < 20 \|\| ((double)seekAmount > 0.3D && tickCount < 40))` | `WaterBoltEntity.tick()V @19–89` |
| Ajuste de movimento: `v * (1F-(seekAmount-0.3F)*0.3F) + normalize(targetPos + 0.85F*height - pos)*seekAmount` | `tick()V @92–155` |
| Dano solicitado `3F`, `mobProjectile(this, owner living ou null)`, AABB própria inflada `2D` em cada eixo | `damageMobs()V @0–58, @133–139` |
| `ENVELOPING_BUBBLE > 0`: `nextBoolean()` por bolt; se dano aceito e flag ativa, `BUBBLED` por `200` ticks e mensagem visual `1,200` | `SeaStaffItem.use @272–294`; `WaterBoltEntity.damageMobs()V @133–213` |
| `BOUNCING_BOLT > 0` ativa um ricochete. O último candidato elegível, atribuído **antes** do resultado de `hurt`, serve de origem; a flag é consumida | `use @297–311`; `damageMobs()V @129–139, @219–239` |
| Filho do ricochete copia posição e Bubbling, recebe novo UUID alvo e impulso unitário; mantém defaults `seekAmount=0.3F`, `ricochet=false`, sem herdar o nível Soak Seeking | `onRicochetHit(Lnet/minecraft/world/entity/Entity;)V @154–266`; construtor |
| `isBubbling()Z`, `getArcingTowards()Lnet/minecraft/world/entity/Entity;` leem dados sincronizados; o segundo resolve UUID via `ServerLevel.getEntity` | getters `@0–16`, `@0–40`; setters `(Z)V`, `(Ljava/util/UUID;)V @0–14` |
| `getEnchantmentValue()I = 1`; `isEnchantable(Lnet/minecraft/world/item/ItemStack;)Z` aceita `count == 1` | `SeaStaffItem` getters `@0–1`, `@0–13` |

**Precisão numérica:** `0.3F`, ampliado para double, vale `0.30000001192092896D`, maior que o literal `0.3D` usado nas condições. Até o valor baseline passa esse teste; não reinterpretar os limites de homing como exclusivos de encantamento. A leitura é estática, sem QA física do trajeto.

### 4. Targeting, área e filtros

`SeaStaffItem.getClosestLookingAtEntityFor` tem descritor `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;D)Lnet/minecraft/world/entity/Entity;`. `use @81–90` passa `128D`: a função faz clip `VISUAL/NONE` até `eyes + look*dist` (`@3–40`); no fallback constrói caixa `±0.5D` no ponto de hit, infla `15D` e depois `dist` (`@114–174`). Escolhe o candidato mais próximo **do ponto de hit**, não do jogador (`@250–275`). Portanto **128 não é alcance máximo geométrico** dos candidatos nem do bolt. O ramo EntityHitResult também existe no bytecode; sua existência não prova que `Level.clip` o produzirá.

Ambos os ramos exigem `Mob`, diferente do jogador, ausência de aliança nos dois sentidos e linha de visão (`@63–104`, `@206–247`). Não há chamada explícita `isAlive` nesses filtros; `LivingEntity`/`Mob` não deve ser traduzido como um novo filtro de vida.

Impacto consulta `LivingEntity` na AABB inflada e exclui aliado do bolt, `DeepOneBaseEntity`, owner e entidades aliadas ao owner (`damageMobs()V @90–126`). Ricochete consulta a AABB do último candidato inflada `32D` por eixo, aplica os mesmos filtros, exclui o atingido, exige distância `>3D` dele e escolhe o mais próximo dele (`onRicochetHit @5–149`); não há teste próprio de linha de visão nesse método. Aquisição, homing, área de impacto e busca do ricochete são quatro contratos distintos.

### 5. Custos, recarga e dados do item

`SeaStaffItem.use` tem descritor `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;`. Em `@366–381`, solicita **1** de durabilidade via `ACCompat.hurtAndBreak` apenas se `!instabuild`; o wrapper converte a mão em slot e delega `ItemStack.hurtAndBreak` (`ACCompat`, descritor `(Lnet/minecraft/world/item/ItemStack;ILnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/InteractionHand;)V @0–10`). Não há chamada direta de cooldown nem cobrança de mana neste caminho; isso não certifica custo efetivo diante de mods/hook externos. `ACItemRegistry.lambda$static$108()Lnet/minecraft/world/item/Item; @11–23` registra durabilidade `850`, raridade `UNCOMMON`.

`acInventoryTick(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;Z)V @32–88` trata `SEAPAIRING`: servidor, encantamento positivo, stack não em uso, `nextFloat()<0.02F`, entidade em água/chuva/bolha; escreve literalmente `setDamageValue(Math.min(0, damage-1))`. É manutenção passiva, não cast novo, e **não** uma subtração limitada por `Math.max`.

O JAR contém `data/alexscaves/loot_table/gameplay/deep_one_mage_barter.json` (4.482 bytes, SHA-256 `18682ca468355f61eda02c903fdb9c0dfbda88094c5caf343b1ae5ef437c44eb`), com entrada `alexscaves:sea_staff`, peso `12`. O tag `data/alexscaves/tags/item/enchantable/sea_staff.json` (49 bytes, SHA-256 `22e45ab74b71d7152ccc531a633e5149df9c12eece40464c85c50f5a600fd80e`) contém esse item. Os JSONs de encantamento declaram máximos Soak Seeking `3`, Triple Splash/Enveloping Bubble/Bouncing Bolt/Seapairing `1`; Bouncing Bolt lista Triple Splash em `exclusive_set`. São dados embarcados, sujeitos à precedência de datapacks.

### 6. Integração e autoridade

`use`, `damageMobs`, `onRicochetHit`, setters e `EventHooks.onProjectileImpact` são superfícies observadas. Hook externo capaz de alterar parâmetros com ordem, cancelamento, ownership e anti-duplicação comprovados: **`NOT_VERIFIED`**. Uma perk deve distinguir aquisição, homing, impacto e ricochete e fica **⛔ fail-closed** até esse contrato existir. Black Arcana não relança bolts, não repete `mobProjectile`, não reaplica Bubbling e não paga durabilidade de novo.

### 7. Validação e localizadores

`VERIFIED_EXACT_BINARY` descreve apenas bytecode/dados embarcados. Configuração efetiva, mixins, eventos mutadores e parâmetros após reload: `NOT_VERIFIED`; execução física/QA: `NOT_TESTED`. O dano é uma solicitação ao provider/engine, não HP efetivamente perdido nem soma de DPS certificada.

| Entrada no JAR | Bytes | SHA-256 |
|---|---:|---|
| `com/github/alexmodguy/alexscaves/server/item/SeaStaffItem.class` | 9.765 | `cb3153a35e7f4c3ab23e68693aec110edf03ecd050c3b485e35ccbb257b4bbc6` |
| `com/github/alexmodguy/alexscaves/server/entity/item/WaterBoltEntity.class` | 16.812 | `342c011b0178e1f65cd2e6ef315fe6bad49bd5ead237b2274e822560e2eac401` |

Corroboração pública preservada: [`SeaStaffItem.java`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/item/SeaStaffItem.java), [`WaterBoltEntity.java`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/entity/item/WaterBoltEntity.java), snapshot **1.1.1**, sem prova de paridade com 1.0.10.

Static evidence grade: `SHA_EXACT_BINARY_BEHAVIOR`. Claim scope: `STATIC_TECHNICAL_CATALOG_ONLY`. Hook: `NOT_VERIFIED`. Physical QA: `NOT_TESTED`.
