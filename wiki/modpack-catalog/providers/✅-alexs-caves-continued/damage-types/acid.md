# Acid — dano ambiental e contato do Waste Drum (1.0.10)

**Catálogo:** ✅ contrato estático dos dois emissores diretos de `alexscaves:acid` documentado. **Escopo:** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`; **QA física:** `NOT_TESTED`; **integração:** `NO_MUTATION` até homologação específica. Este recorte não conclui o provider, todo o sistema de fluidos, a armadura Hazmat ou a AI do Brainiac.

## 1. Identidade, proveniência e classificação

- **Provider / mod ID:** Alex's Caves Continued / `alexscaves`.
- **Artefato físico:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, Minecraft 1.21.1, 75.279.314 bytes.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **DamageType:** `alexscaves:acid`; ZIP `data/alexscaves/damage_type/acid.json`; SHA-256 `482b88005a50092f022c4cc7058402d148a4102461d6fefcaf837dcb6e4f3b17`.
- **Emissor ambiental:** `com/github/alexmodguy/alexscaves/server/block/AcidBlock.class`; SHA-256 `e2f9c8213633debbcbae6f99f9d1987be60b7de6c73a9825a74eec96b453e959`.
- **Emissor de contato:** `com/github/alexmodguy/alexscaves/server/entity/item/ThrownWasteDrumEntity.class`; entidade `alexscaves:thrown_waste_drum`, produzida pelo ramo de lançamento do Brainiac.

| Campo | Valor literal do recurso | Interpretação delimitada |
|---|---|---|
| `message_id` | `acid` | Mensagem de morte; não é fórmula de dano nem escola RPG |
| `scaling` | `never` | Campo do DamageType; não fixa dano efetivo ou resistência |
| `exhaustion` | `0.1` | Exaustão declarada do tipo de dano; não é mana, stamina ou custo de cast |

Nenhum dos seis JSONs `data/*/tags/damage_type/*.json` presentes no JAR lista diretamente `alexscaves:acid`. O [manifesto dos recursos](EXACT-RESOURCE-MANIFEST-1.0.10.json) sela esse inventário. Tags finais podem receber outras entradas por datapacks/dependências; ausência textual neste artefato não prova ausência na resolução do modpack.

**Contabilidade:** **+0 raízes mágicas novas**. O tipo de dano e seus emissores são contratos de settlement, não dois novos feitiços. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e não fornece os parâmetros certificados de 1.0.10. A [prova comum](../EXACT-ACID-CONTRACT-1.0.10.md) e o [manifesto de contratos](../EXACT-ACID-CONTRACT-1.0.10.json) selam ficha, classes, recursos e localizadores JVM.

## 2. AcidBlock — resistência, desgaste e dano probabilístico

O método é `entityInside(Lnet/minecraft/world/level/block/state/BlockState;Lnet/minecraft/world/level/Level;Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/entity/Entity;)V`. Recebe uma `Entity`; apenas o cálculo de equipamento exige `LivingEntity`. O fluxo próprio de 174 instruções é:

1. **Gate ambiental (`@0–26`):** pula o bloco de desgaste/dano se o tipo da entidade pertence a `ACTagRegistry.RESISTS_ACID` ou se `ACFluids.acidHeight(entity) <= 0.1D`.
2. **Armadura (`@29–179`):** inicia `armorFlag=false`, `damageAccepted=false`, `s=1F`. Para uma LivingEntity, percorre `EquipmentSlot.values()` e mantém somente slots com `isArmor()`. Em cada stack não nulo, damageable e cujo item **não** é `instanceof HazmatArmorItem`, define `armorFlag=true` **antes** de sortear desgaste. Se `entity.getRandom().nextFloat()<0.05F`, solicita **1** de desgaste via `ACCompat.hurtAndBreak(stack,1,living,slot)`, salvo Player criativo. O flag não depende de desgaste aceito nem do número de peças comuns.
3. **Proteção quantitativa (`@179–190`):** para LivingEntity, calcula **`s = 1F - HazmatArmorItem.getWornAmount(living)/4F`** depois do loop de desgaste. Para entidades não vivas, `s` permanece `1F` e `armorFlag=false`.
4. **Chance e magnitude (`@205–276`):** outro sorteio, agora `level.getRandom().nextFloat()<s`, governa a solicitação de dano. Somente nesse ramo calcula o bônus da tag `WEAK_TO_ACID` e chama `ACCompat.hurt`.
5. **Resultado (`@278–296`):** `ACID_BURN` é solicitado apenas quando o booleano retornado por `hurt` é verdadeiro.

No ramo de dano:

```text
weakBonus = entityType in WEAK_TO_ACID ? 10F : 0F
requestedDamage = s * (armorFlag ? (float)0.01D : 1F) + weakBonus
damageAccepted = ACCompat.hurt(entity, causeAcidDamage(level.registryAccess()), requestedDamage)
```

O literal `0.01D` é selecionado em double e convertido a float antes da multiplicação (`@254–272`); as contas de `s` e dano são float. O bônus `10F` não é multiplicado por `s`, mas só é alcançado **depois** de passar a chance `<s`. Com quatro peças Hazmat exatas, `s=0` e esse caminho não solicita dano, inclusive contra uma entidade classificada como fraca. O corpo não tem clamp de resistência nem regra própria de crítico.

Sem Hazmat e sem armadura comum elegível, o valor solicitado é `1F`, ou `11F` quando a tag de fraqueza passa. Com `armorFlag=true`, a parcela base passa a aproximadamente `0.01F`, sem tornar o desgaste proporcional ao dano ou ao número de peças. Esses valores são **solicitações**, não vida removida depois de armadura, eventos e hooks externos. A chance é por chamada elegível de `entityInside`, não uma frequência medida por segundo ou um intervalo próprio fixo.

O corpo não chama `super.entityInside`, não possui guarda própria `isClientSide`, filtro de aliança/owner, PvP ou proteção territorial. A ausência desses testes locais não comprova execução duplicada ou falha no modpack. O ramo posterior `@299–402` trata som de natação para LivingEntity com `moveDist>nextStep`, excluindo Radgill; pode ser alcançado mesmo quando os gates ambientais pularam dano. Esse som e a atualização de `nextStep` não são outro hit nem outra magia.

## 3. Altura de contato, slots e tags

`ACFluids.acidHeight(Lnet/minecraft/world/entity/Entity;)D @0–7` chama `fluidHeight(Entity,TagKey)D` com `ACTagRegistry.ACID`. O overload de dois argumentos passa `null` como segundo tag para `(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/tags/TagKey;Lnet/minecraft/tags/TagKey;)D`. O helper completo:

- deflaciona a AABB da entidade em **`0.001D`** e usa limites `floor(min)` / `ceil(max)`, com máximo exclusivo nos loops X/Z/Y;
- consulta chunks por `getChunkNow(x>>4,z>>4)` e pula colunas sem chunk disponível; não solicita carregamento por outro método nesse corpo;
- considera somente estados não vazios compatíveis com o tag de fluido; neste caminho, o segundo tag é nulo;
- calcula a superfície por **`(double)((float)y + fluidState.getHeight(chunk,pos))`**, com soma em float antes da ampliação, e retorna o máximo de `surface - deflatedBox.minY` quando a superfície está acima dessa base. Começa em zero, sem clamp próprio à altura da entidade ou a `box.maxY`.

Portanto, `>0.1D` é um gate sobre essa altura máxima calculada, não porcentagem de submersão, distância de cast, área de dano ou estado de uma API NeoForge presumido. Localizadores do helper completo: AABB `@0–21`, limites `@23–87`, chunks/loops `@112–224`, tags `@227–253`, superfície/máximo `@256–296`, retorno `@316–318`.

`HazmatArmorItem.getWornAmount(Lnet/minecraft/world/entity/LivingEntity;)I @0–111` conta exatamente quatro combinações de `ItemStack.is(Item)`:

| Slot | Campo de `ACItemRegistry` | Offsets do helper |
|---|---|---|
| `HEAD` | `HAZMAT_MASK` | `@2–26` |
| `CHEST` | `HAZMAT_CHESTPLATE` | `@29–53` |
| `LEGS` | `HAZMAT_LEGGINGS` | `@56–80` |
| `FEET` | `HAZMAT_BOOTS` | `@83–107` |

O domínio desse helper é zero a quatro. Não conta toda instância/subclasse de `HazmatArmorItem`, enquanto o teste de desgaste usa `instanceof` e o universo de `EquipmentSlot.values()/isArmor()`. Os dois predicados não são intercambiáveis. Os registros dos quatro itens são fixados em `ACItemRegistry.<clinit>()V @1443–1508`; peças em outros slots não satisfazem essas comparações.

`ACTagRegistry` usa o namespace **`alexscaves`**: `RESISTS_ACID`/`WEAK_TO_ACID` vêm de `registerEntityTag(String)TagKey` (`<clinit> @599–605`, `@716–722`); `ACID` vem de `registerFluidTag(String)TagKey` (`@806–812`). Os recursos diretos são:

- `data/alexscaves/tags/entity_type/resists_acid.json`: `minecraft:creeper`, `alexscaves:nucleeper`, `alexscaves:radgill`, `alexscaves:brainiac`, `alexscaves:raycat`, `alexscaves:tremorzilla`.
- `data/alexscaves/tags/entity_type/weak_to_acid.json`: `minecraft:iron_golem`.
- `data/alexscaves/tags/fluid/acid.json`: `replace=false`, `alexscaves:acid` e **`alexscaves:acid_flowing`**.
- `data/c/tags/fluid/acid.json`: outro tag, **`c:acid`**, com entradas opcionais `alexscaves:acid` e **`alexscaves:flowing_acid`**. Não substituir o tag realmente consumido nem corrigir editorialmente os IDs diferentes.

Os conteúdos são do JAR fixo; a composição final de tags ainda depende do pack. O comentário de `resists_acid` não constitui uma imunidade universal para todo consumidor desse DamageType.

## 4. Thrown Waste Drum — contato, criação de fluido e cleanup

`server.entity.item.ThrownWasteDrumEntity` estende `Entity`, sem owner próprio ou aquisição de target nesse corpo. O registro `alexscaves:thrown_waste_drum` usa categoria `MISC`, dimensões **0.98F × 0.98F**, velocity updates `true` e tracking range `20`. `ACEntityRegistry.lambda$static$31()EntityType @20–35` chama primeiro `setUpdateInterval(1)` e depois `updateInterval(10)`; a última configuração compilada é **10**, não 1. Esses metadados de rede não são hitbox expandida, raio de dano ou cadência de hits.

`ThrownWasteDrumEntity.tick()V` não chama `super.tick`/`baseTick`. Seu estado temporal é `ON_GROUND_FOR`, um accessor sincronizado `Integer` com default `0`, lido por `getOnGroundFor()I` e escrito sem clamp por `setOnGroundFor(I)V`.

| Etapa própria | Contrato estático / offsets em `tick()V` |
|---|---|
| Movimento | Se não `isNoGravity`, soma `(0,-0.08D,0)`; faz `move(MoverType.SELF,velocity)` e escala a velocidade resultante por `0.9D` (`@0–45`) |
| Ground | Somente quando `onGround()`, incrementa `ON_GROUND_FOR` e multiplica a velocidade por `(0.7D,-0.7D,0.7D)` (`@48–82`). Não há reset no ramo aéreo; não é contador de idade nem de ticks necessariamente consecutivos |
| Consulta de contato | Exige comprimento da velocidade resultante `>0.029999999329447746D` (o valor float 0.03 ampliado). Consulta `LivingEntity` na AABB própria (`@85–140`), sem inflação ou predicado adicional explícito de alvo vivo |
| Dano | Exclui apenas `instanceof BrainiacEntity` no loop; solicita **2F** diretamente por `LivingEntity.hurt(causeAcidDamage(level.registryAccess()),2F)` e descarta o booleano (`@142–168`). Não consulta Hazmat, `RESISTS_ACID`, `WEAK_TO_ACID`, owner, aliança, PvP, distância adicional ou LOS nesse ramo |
| Freio | A existência de um candidato não Brainiac ativa multiplicação X/Z por `0.2D`, Y por `1D` (`@150–151`, `@172–191`), mesmo se `hurt` não aceitou o dano |
| Guarda de lado | A condição de servidor aparece **depois** do contato, no ramo de contador `>=20` (`@194–210`). Não declarar todo `tick` server-only por essa guarda posterior |

Assim, a resistência ambiental de `AcidBlock` não é aplicada novamente pelo contato do drum. O tipo de dano é o mesmo, mas magnitude, seleção e gates são diferentes. Aceitação do dano e interação com outros mods continuam no motor.

### Busca vertical e remoção

No servidor, com contador **igual a 20**, inicia `pos=blockPosition()`. O loop `@227–297` sobe uma posição enquanto:

```text
pos.y < level.getMaxBuildHeight()
AND (!state.isAir() OR (!state.fluidState.isEmpty() AND !state.fluidState.is(ACID)))
```

Portanto, para antes do teto quando encontra estado `isAir()` cujo fluido é vazio ou pertence ao tag de fluido `ACID`; estados não-air sobem independentemente de seu fluido. Esse é o predicado literal, não uma busca genérica pelo chão ou pelo ponto de impacto. Ao encerrar, **sempre** grava `removeWasteAt=pos` (`@300–302`); somente se o estado nessa posição for air tenta `setBlockAndUpdate(pos,ACBlockRegistry.ACID.get().defaultBlockState())`, descartando o retorno (`@305–349`). Não há teste adicional de altura de construção nesse bloco de colocação nem prova aqui da permissão final da alteração.

O contador só aumenta no chão: se permanecer **20 durante ticks aéreos**, o bloco de igualdade pode executar novamente em cada tick servidor, refazer a busca e substituir `removeWasteAt`. Não há flag própria de “já colocou”. Isso é uma possibilidade do controle estático; colocação repetida ou resíduos no modpack não foram reproduzidos.

No servidor, com contador **>=35** e `removeWasteAt != null`, chama `remove(DISCARDED)` **antes** de verificar o fluido nessa posição (`@350–387`). Se o FluidState atual pertence ao tag `alexscaves:acid`, solicita sua substituição por `Blocks.AIR.defaultBlockState()`, novamente ignorando o booleano (`@390–410`). O tag compilado contém diretamente `alexscaves:acid` e `alexscaves:acid_flowing`; membros finais podem ser alterados por datapacks. O guard não exige prova de que aquela instância colocou o fluido atual e não guarda o estado original para rollback.

Não há TTL absoluto em ticks aéreos nesse método: sem alcançar os thresholds do contador ground, os ramos de colocação/cleanup não são solicitados. `readAdditionalSaveData(CompoundTag)V` e `addAdditionalSaveData(CompoundTag)V` têm corpo vazio; não persistem ali `ON_GROUND_FOR` nem `removeWasteAt`. O construtor inicializa a posição de cleanup como null. Sync de contador e spawn não prometem restauração integral nem limpeza após reload, morte/remoção por outro caminho ou mudança de dimensão.

`getAddEntityPacket(ServerEntity)Packet @0–5` delega a `ACPlatform.getEntitySpawningPacket(Entity,ServerEntity)Packet`; o helper constrói `ClientboundAddEntityPacket(entity,serverEntity)`. É um caminho de spawn de rede, distinto da persistência e sem homologação de mutação por perks.

## 5. Emissor Brainiac — custo e vetor inicial delimitados

Em `BrainiacEntity.tick()V @201–218, @305–510`, a criação exige servidor, `hasBarrel()`, animação `ANIMATION_THROW_BARREL`, `getAnimationTick()>=15`, `getTarget()!=null` e target vivo. O recorte consulta o target já escolhido pela AI; não acrescenta teste próprio de range ou LOS nesse bloco. A AI que escolhe a animação e o target, reabastecimento de barrel e cooldowns globais permanecem fora deste contrato de Acid.

Antes de criar a entidade, solicita `setHasBarrel(false)` (`@340–342`). Esse accessor booleano é o recurso consumido no ramo, sem custo próprio de mana ou munição de jogador. `ACCompat.createEntity(EntityType,Level)` delega a `EntityType.create(Level)`; o ramo não testa o retorno para null antes de usar o drum. Define a posição, solicita `level.addFreshEntity(drum)` com booleano ignorado e **depois** define a velocidade. Não condicionar o consumo do barrel à aceitação do spawn a partir desse corpo.

Origem: `spawn = brainiac.getEyePosition() + offset.xRot(-xRot*0.017453292F).yRot(-headYaw*0.017453292F)`, com offset double literal `(0.6499999761581421D,-0.30000001192092896D,0.8999999761581421D)`. Define `u=(target.getEyePosition()-spawn)*(0.3499999940395355D,0D,0.3499999940395355D)+(0D,0.4D,0D)` e velocidade **`normalize(u) * (double)(target.distanceTo(brainiac)*0.2F)`** (`@424–510`). São cálculo de origem e impulso, não homing ou alcance máximo. O yaw do drum usa `-float(atan2(u.x,u.z))*180F/3.1415927F`.

`hasBarrel()Z`/`setHasBarrel(Z)V` acessam o mesmo `SynchedEntityData`; `defineSynchedData(Builder)` declara default true para esse flag. Esta dependência selecionada não fecha todos os skills, recursos ou lifecycle do Brainiac.

## 6. Factory, autoria e custos

`ACDamageTypes.causeAcidDamage` tem descritor `(Lnet/minecraft/core/RegistryAccess;)Lnet/minecraft/world/damagesource/DamageSource;`. A classe `com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.class` tem SHA-256 `389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6`.

Em `@0–31`, a factory busca `Registries.DAMAGE_TYPE`, usa `getHolderOrThrow(ACID)` e constrói `DamageSourceRandomMessages(holder,1)`. `<clinit>()V @0–13` liga a chave a `alexscaves:acid`. O construtor `(Lnet/minecraft/core/Holder$Reference;I)V` chama `DamageSource(Holder)` e armazena `messageCount=1`, sem parâmetro de `Entity`; não transporta ali um owner de Brainiac, tambor ou jogador. A função de mensagem consulta `getDirectEntity`/`getEntity` e um índice sorteado de `messageCount`; apresentação da mensagem e atribuição final de crédito por morte não substituem um contrato de owner.

Os dois callsites diretos do [manifesto de consumidores](EXACT-CONSUMERS-1.0.10.json) permanecem `AcidBlock.entityInside @251` e `ThrownWasteDrumEntity.tick @161`; número de invocações no bytecode não é número de hits em jogo. O bloco usa `ACCompat.hurt(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/damagesource/DamageSource;F)Z`, que encaminha os três argumentos para `Entity.hurt` e devolve seu booleano. O tambor chama `LivingEntity.hurt` diretamente e descarta o resultado.

Não há mana, cooldown ou custo de casting de jogador nesses corpos de dano. O custo ambiental concreto é a solicitação de desgaste do equipamento por slot e sorteio descritos acima; `ACCompat.hurtAndBreak(Lnet/minecraft/world/item/ItemStack;ILnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/EquipmentSlot;)V` delega `ItemStack.hurtAndBreak`, sem fixar desgaste efetivo diante de encantamentos/hooks. No lançamento pelo mob, o recurso concreto é o estado `hasBarrel` consumido pelo ramo Brainiac; não inventar recarga, mana ou custo de item de um jogador. Aquisição de Acid Bucket e todos os métodos de colocação/fluxo de fluido são escopos de equipamento/mundo separados.

## 7. Integração e validação

Uma perk de “resistência a ácido” deve escolher explicitamente a chance ambiental `s`, a magnitude solicitada, o desgaste por slot, o tag ambiental ou o contato do tambor. Compartilhar `alexscaves:acid` não faz o contato reaplicar os guards Hazmat/RESISTS/WEAK do bloco. Altura de contato, AABB de contato, impulso de lançamento e intervalo de atualização da entidade também são superfícies diferentes de alcance ou raio de spell.

Cast/AI, dano, eventos, desgaste, posição de fluido, persistência e remoção permanecem sob autoridade dos sistemas nativos. Não repetir settlement depois do provider nem transformar um setter ou callback em hook homologado. O recorte só dispõe os dois emissores de dano e seus helpers selecionados. `AcidBlock.onPlace` e `neighborChanged` chamam `tickCorrosion(Level,BlockPos)` após o super (`@11–17`, `@13–19`): corrosão de blocos é outro efeito ambiental, não outra solicitação `causeAcidDamage`; seu catálogo completo não é promovido por esta ficha.

Sete campos estáticos fechados: identidade/recurso/factory; fluxos causais; fórmulas/temporização/geometria; targeting e predicados; custos; fronteiras de integração; prova compilada reproduzível. A [prova comum](../EXACT-ACID-CONTRACT-1.0.10.md) reproduz `javap -p -c -s` e a auditoria dos hashes, descritores e offsets do JAR 1.0.10. As [evidências anteriores de recursos](EXACT-RESOURCE-MANIFEST-1.0.10.json) e [factories/consumidores](EXACT-CONSUMERS-1.0.10.json) conservam seus escopos parciais; a certificação atual depende do novo contrato selado.

**Hooks:** `NOT_VERIFIED`; **QA física:** `NOT_TESTED`; configuração/tags efetivas do pack e comportamento multiplayer não certificados. QA necessária: combinações Hazmat/slots e tags, desgaste e dano recusados, entidades não vivas, altura limiar, chunks disponíveis, múltiplos contatos, contador em saltos, recolocação/cleanup de fluido, proteção de mundo, reload/removal externo, PvP e interação de perks entre os dois emissores. Nenhuma dessas questões é classificada como defeito reproduzido.
