# Desolate Dagger — entidade, stab e tipo de dano (1.0.10)

**Catálogo:** ✅ contrato estático do consumidor nativo de `alexscaves:desolate_dagger` documentado. **Escopo:** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`; **QA física:** `NOT_TESTED`; **integração:** `NO_MUTATION` até homologação específica. O recorte não encerra o provider nem certifica dano final ou proc observado no modpack.

## 1. Identidade e autoridade

- **Provider / mod ID:** Alex's Caves Continued / `alexscaves`.
- **Artefato:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, Minecraft 1.21.1, 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Consumidor:** `com/github/alexmodguy/alexscaves/server/entity/item/DesolateDaggerEntity.class`; SHA-256 `f82a3f5f1cc05bbe52dfb7e3742f33c2289cbc37810b069a53b45002cfeb4351`.
- **DamageType:** `alexscaves:desolate_dagger`; ZIP `data/alexscaves/damage_type/desolate_dagger.json`; SHA-256 `a8c5a9d4d72a4c064c1b0fca923d2059eb6b718e9866fb8d19dc539bb0ffec93`.
- **Produtor:** [Desolate Dagger — equipamento e spawn](../equipment/desolate-dagger.md). O hit primário da arma e o stab posterior são consumidores distintos.

| Campo | Valor literal do recurso | Interpretação delimitada |
|---|---|---|
| `message_id` | `desolate_dagger` | Mensagem de morte; não define escola RPG ou fórmula |
| `scaling` | `never` | Campo do DamageType; não garante dano líquido constante |
| `exhaustion` | `0.3` | Exaustão do tipo de dano; não é mana, stamina ou custo de cast |

Entrada direta nos seis arquivos `data/*/tags/damage_type/*.json` do JAR:

- `minecraft:bypasses_cooldown`

O bypass classifica dano no Minecraft; não comprova bypass de cooldown da arma/casting. Tags finais dependem dos dados resolvidos do pack. `dark_arrow.json` tem o mesmo conteúdo/hash e `message_id`, mas são **dois resource IDs diferentes**, com factories e consumidores próprios; não mesclar fórmulas ou targeting.

**Contabilidade:** **+0 raízes mágicas novas**. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e não fornece os parâmetros certificados de 1.0.10. A [prova comum](../EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.md) e o [manifesto selado](../EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.json) fixam ficha, classes, recursos, descritores JVM e offsets.

## 2. Geometria, estado e produção

`DesolateDaggerEntity` estende **`Entity`**, não `AbstractArrow`. `ACEntityRegistry.lambda$static$61()Lnet/minecraft/world/entity/EntityType; @0–37` declara categoria `MISC`, dimensões **0.6F × 0.6F**, velocity updates `true` e update interval **1**. `<clinit>()V @1061–1075` registra `desolate_dagger`. Esses metadados não são raio de dano, alcance ou tamanho do renderer.

O construtor `(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/Level;)V` inicializa `orbitRandom`, `orbitOffset=0`, `prevStab=0`, `playedSummonNoise=false` e `daggerRenderStack` com um novo item Desolate Dagger. Primeiro escreve `orbitFor=20`, depois substitui por **`20+level.random.nextInt(10)`**, isto é, 20–29 (`@56–71`). `orbitFor` é campo comum público; o item produtor o substitui por outro valor. Seu default não é duração universal.

`defineSynchedData(Lnet/minecraft/network/syncher/SynchedEntityData$Builder;)V @0–54` define:

| Accessor | Default | Métodos próprios |
|---|---|---|
| `TARGET_ID` (`Integer`) | `-1` | `getTargetId()I`; `setTargetId(I)V` |
| `PLAYER_ID` (`Integer`) | `-1` | `getPlayerId()I`; `setPlayerId(I)V` |
| `STAB` (`Float`) | `0F` | `getStab()F`; `setStab(F)V` |
| `ITEMSTACK` (`ItemStack`) | Novo `Items.IRON_SWORD` | `getItemStack()Lnet/minecraft/world/item/ItemStack;`; `setItemStack(Lnet/minecraft/world/item/ItemStack;)V` |

Os setters escrevem literalmente em `SynchedEntityData`, sem validar dono, classe de alvo, ID, nível de encantamento ou clamp de stab. `getItemStack` retorna o stack armazenado; seu setter não faz `copy`. `daggerRenderStack` é outro campo, usado pela apresentação, sem leitura na fórmula de dano deste tick. O item passa seu stack ao accessor: isso não constitui snapshot imutável do nível de encantamento.

`getTargetEntity()Lnet/minecraft/world/entity/Entity;` e `getPlayer()Lnet/minecraft/world/entity/Entity;` (`@0–22`) retornam null para ID `-1`; caso contrário, chamam `level().getEntity(id)`. São **IDs inteiros no Level atual**, sem UUID, fallback entre dimensões ou teste de classe Player no resolver chamado `getPlayer`. Não há busca em área ou aquisição autônoma de um substituto.

## 3. Tick, movimento, tempo e persistência

`tick()V` chama `Entity.tick()` primeiro (`@0–1`), copia `getStab()` para `prevStab` e resolve o alvo (`@4–16`). No cliente solicita REDSTONE com argumentos `getRandomX(0.75D)`, `getRandomY()`, `getRandomZ(0.75D)` (`@17–55`). Fora desse gate de lado, `playedSummonNoise` limita a solicitação de som de summon a uma vez por instância desse estado (`@58–82`); não garante um único som global em multiplayer.

Com alvo não nulo, fixa `noPhysics=true` e calcula movimento usando o **STAB anterior ao incremento servidor deste tick**. Defina `a=1F-STAB`:

```text
base = target.position + (0, target.height*0.25F, 0)
orbitRandom.setSeed(entity.getId())
se orbitOffset==0: orbitOffset=orbitRandom.nextInt(360)
offset = Vec3(0, (nextFloat()+target.height)*a, (nextFloat()+target.width)*a)
offset = offset.yRot((float)Math.toRadians(orbitOffset))
deltaMovement = base + offset - currentPosition
```

Localizadores: base `@101–118`, reseed/ângulo `@119–156`, offset/rotação `@159–213`, delta `@215–229`. Não há incremento angular por idade nesse corpo. A sequência dos draws muda quando o ramo do ângulo executa; não prometer órbita circular uniforme, velocidade fixa ou alcance máximo. `noPhysics` não autoriza PvP ou passagem por proteção de mundo.

Somente no servidor (`@232–438`), se `orbitFor>0` **e** `target.isAlive()`, decrementa o contador; caso contrário, escreve **`STAB=min(STAB+0.2F,1F)`**. Um alvo morto mas ainda resolvido entra na progressão; `isAlive` não proíbe adicionalmente a tentativa de dano. Partindo de `STAB=0`, são cinco incrementos até 1, depois de consumir o contador se o alvo permaneceu vivo. O item altera o contador inicial, e setters externos podem alterar esse domínio.

Com alvo nulo e `tickCount>3`, fixa `noPhysics=false` e chama `discard()` (`@526–540`), sem guarda própria de servidor nem retorno imediato. Com alvo presente, calcula yaw/pitch apontando ao `getEyeY()` do alvo (`@438–523`), inclusive após solicitar descarte. Ambos os caminhos seguem para `move(MoverType.SELF,deltaMovement)` e arrasto **`0.8999999761581421D`** (float 0.9 ampliado), em `@543–565`. O ataque abaixo não depende de colisão por contato.

No cliente, `lerpTo(DDDFFI)V` guarda posição, ângulos e passos, e restaura velocidade `lxd/lyd/lzd`; `lerpMotion(DDD)V` grava esses componentes e delta. `tick @568–714` interpola posição se `lSteps>0`, escreve yaw com `wrapDegrees(lyr)`, interpola pitch, decrementa passos e chama `setPos`; sem passos chama `reapplyPosition`. `getStab(F)F` retorna `prevStab+(getStab()-prevStab)*partial`, sem clamp próprio de partial. São superfícies de interpolação, sem hit adicional.

`getAddEntityPacket(Lnet/minecraft/server/level/ServerEntity;)Lnet/minecraft/network/protocol/Packet;` delega a `ACPlatform.getEntitySpawningPacket`, que constrói `ClientboundAddEntityPacket(entity,serverEntity)`. **Spawn sync não é persistência:** `readAdditionalSaveData(Lnet/minecraft/nbt/CompoundTag;)V` e `addAdditionalSaveData` de mesmo descritor têm corpo vazio. Não persistem ali IDs, stack, stab, contador, ângulo, som ou interpolação. Reload/remoção externa precisa de QA; não prometer restauração integral ou ownership durável.

## 4. Ataque, dano solicitado e Sated Blade

O ramo servidor testa **`getStab()>=1F`** após atualizar o estado (`@284–290`). Não compara distância, LOS, AABB da vítima, aliança, dono, PvP ou colisão antes da tentativa. O movimento usou o stab anterior: o limiar não demonstra que a dagger já encostou na vítima.

```text
resolved = getPlayer()
sourceEntity = resolved == null ? thisDagger : resolved
requested = 2F + 2F*ACCompat.enchantLevel(getItemStack(), IMPENDING_STAB)
accepted = ACCompat.hurt(target,
    causeDesolateDaggerDamage(level.registryAccess(),sourceEntity),requested)
if accepted:
    solicitar som de hit
    L = ACCompat.enchantLevel(getItemStack(),SATED_BLADE)
    if L>0 and sourceEntity instanceof Player and saturation<5F:
        setSaturation(currentSaturation + L*0.1F)
discard()
```

- A fórmula (`@312–327`) lê o **stack no stab**, sem nível congelado no spawn. Impending Stab 0/1/2/3 solicita **2/4/6/8F**. Não usa dano-base da espada, velocidade, crítico ou redução própria nesse cálculo. Dano líquido permanece em `Entity.hurt` e consumidores externos.
- A factory é chamada em **339**, `ACCompat.hurt` em **344**, e sua aceitação é testada em **347**. O wrapper apenas encaminha `(Entity,DamageSource,float)` e retorna o booleano.
- `SATED_BLADE` (`@365–431`) só é consultado após dano aceito. Nível 1/2 escreve incremento de saturação **0.1F/0.2F**, sem mudar food level nem chamar cura. A entrada `<5F` não faz clamp do resultado a 5; limites externos pertencem a `FoodData`/outros consumidores.
- **`discard()` em 434–435 é incondicional após a tentativa**, inclusive com `hurt=false`. Dano recusado não preserva este caminho para repetir no tick seguinte. Não há retorno imediato: rotação/movimento/arrasto posteriores ainda existem nesse corpo. É uma solicitação própria seguida de remoção, não contagem de hits medida em jogo.

`PLAYER_ID` começa em `-1`; o produtor `DesolateDaggerItem.acSpawnDaggers` documentado não chama `setPlayerId`. Esse produtor e esses defaults **não estabelecem a chegada ao ramo Player de Sated Blade**: a resolução nula usa a própria entidade dagger como argumento da fonte. Um setter público não cria ponte nativa de autoria ou hook seguro. Chamadas externas/transformações precisam de contrato próprio; não prometer alimentação ao atacante nem declarar defeito reproduzido a partir dessa estrutura.

`ACDamageTypes.causeDesolateDaggerDamage` tem descritor `(Lnet/minecraft/core/RegistryAccess;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;`. Classe `com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.class`, SHA-256 `389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6`. Em `@0–32`, obtém o holder `DESOLATE_DAGGER` e constrói `ACDamageTypes$DamageSourceRandomMessages(holder,sourceEntity,1)`. O construtor `(Lnet/minecraft/core/Holder$Reference;Lnet/minecraft/world/entity/Entity;I)V` delega a `DamageSource(Holder,Entity)` e guarda `messageCount=1`; não recebe projétil/dono em dois argumentos separados. A mensagem prefere `getDirectEntity()` não nulo, senão `getEntity()`, para a tradução com nomes; isso não corrige um player ID ausente.

## 5. Encantamentos, custos e integração

Os JSONs `data/alexscaves/enchantment/impending_stab.json` e `sated_blade.json` usam `#alexscaves:enchantable/desolate_dagger`, slot `mainhand`. Impending tem máximo **3**, peso 10, bigorna 1, mínimo `1+6*(level-1)`, máximo `41+10*(level-1)` e `exclusive_set=[alexscaves:double_stab]`. Sated tem máximo **2**, peso 10, bigorna 1, mínimo `1+11*(level-1)` e máximo `41+10*(level-1)`. São restrições empacotadas; o helper não aplica novo clamp pelo máximo.

`ACCompat.enchantLevel` — `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/resources/ResourceKey;)I`, método SHA-256 `775387837bd0e7dbbd2fd04cd5de0375a6ccd2813de5db375fd152f8b63ad8dc` — itera `ItemStack.getEnchantments().entrySet()`, compara `Holder.is(ResourceKey)` e retorna o valor ou zero. `ACCompat.hurt` — `(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/damagesource/DamageSource;F)Z`, método SHA-256 `77997f2089224cd768dc079fb789bc5ffa96c8647bf5c0cabe932b8c3a3702b5` — tem uma chamada de dano e nenhum branch próprio. Ambos são de `ACCompat.class`, SHA-256 `333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b`.

A entidade não debita mana, fome, durabilidade, quantidade de item ou cooldown nesse tick. Aquisição, reparo, custo do hit primário, quantidade de daggers e contador inicial pertencem ao [equipamento](../equipment/desolate-dagger.md). Saturação condicional é resultado, não custo. Uma alteração no atributo melee não altera automaticamente `2+2L`; alterar range não cria um filtro neste consumidor travado em ID. Tempo, stab, quantidade, target/player IDs e stack são owners distintos que exigem autorização e arbitragem antes de mutação. Não repetir o hit ou o dano posterior numa camada RPG.

## 6. Validação e evidência preservada

A revisão cobre os 20 métodos próprios da entidade, factory/helpers delimitados, dados de dano/encantamento e registro. Descritores/offsets são reproduzíveis por `javap -p -c -s`; o [manifesto](../EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.json) sela a ficha e membros. Permanecem separados e imutáveis: [recursos](EXACT-RESOURCE-MANIFEST-1.0.10.json), [factory/caller](EXACT-CONSUMERS-1.0.10.json), [janelas do tick](EXACT-DAMAGE-PATH-ANCHORS-1.0.10.json) e [helpers](EXACT-DAMAGE-HELPERS-1.0.10.json). Suas flags parciais não homologam runtime.

QA física pendente: dano aceito/recusado, morte/desaparecimento/reuso de IDs, alvo distante/atrás de blocos, reload, sync de stack/stab, interpolação, latência, autoria/Sated Blade, níveis externos aos JSONs, múltiplas daggers e compatibilidade de combate. **Hooks `NOT_VERIFIED`; QA física `NOT_TESTED`; escopo integral do provider aberto.**
