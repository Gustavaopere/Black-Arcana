# Spirit Dinosaur — `alexscaves:spirit_dinosaur` (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Política de integração:** `NO_MUTATION`. O recorte cobre este DamageType, seus dois consumidores e os emissores nativos delimitados; não encerra o equipamento inteiro, a engine herdada ou o universo do provider.

## 1. Identidade e proveniência

- **Provider / mod ID:** Alex's Caves Continued / `alexscaves`, Minecraft 1.21.1; `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Resource ID:** `alexscaves:spirit_dinosaur`; `data/alexscaves/damage_type/spirit_dinosaur.json`; SHA-256 `82db1eedb1377b9cf24f35db29f646df542da43c7d2c96896ae0bace36014eb4`.
- **Espírito:** `com/github/alexmodguy/alexscaves/server/entity/item/DinosaurSpiritEntity.class`, SHA-256 `c4f6bbf7dab4aeeb2abd5b8cd227759d2ea1692115d1b3d14b62598a0b3900d7`; estende `Entity`; **32 membros próprios**, incluindo `<clinit>`, mais cinco do enum.
- **Lança:** `com/github/alexmodguy/alexscaves/server/entity/item/ExtinctionSpearEntity.class`, SHA-256 `084a315c5a63dabc8c6ff1bc91ad008b0b2374e4d7f953bf3692c77394093774`; estende `AbstractArrow`; **18 membros próprios**, incluindo `<clinit>`. Os snapshots anteriores contavam 31 e 17 por excluir esse inicializador.
- **Provas:** [manifesto consolidado](../EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json) e [limites/reprodução](../EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.md). A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e é corroboração adjacente; os parâmetros certificados vêm do binário 1.0.10.

| Campo | Valor literal do recurso | Interpretação delimitada |
|---|---|---|
| `message_id` | `spirit_dinosaur` | Chave de mensagem, não escola de magia ou fórmula |
| `scaling` | `never` | Metadado do DamageType, não dano líquido invariável |
| `exhaustion` | `0.3` | Exaustão de dano, não custo de mana/stamina/casting |

Memberships textuais diretas nos arquivos nativos:

- `minecraft:bypasses_cooldown`
- `minecraft:is_fire`

Não representam tags finais resolvidas após datapacks/mods. `bypasses_cooldown` não reduz cooldown de lançamento; `is_fire` não é, por si só, uma chamada de ignição. A lança solicita ignição por um caminho explícito distinto.

## 2. Factory, autoria e construção

`ACDamageTypes.class` tem SHA-256 `389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6`. A factory `causeSpiritDinosaurDamage`, descritor `(Lnet/minecraft/core/RegistryAccess;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;`, resolve `SPIRIT_DINOSAUR` e usa `DamageSourceRandomMessages(Holder.Reference,Entity,int)`. A entidade fornecida pelo chamador é um argumento de autoria nativa, sem garantia de crédito final, PvP ou Mastery.

| Chamador direto | ABI JVM | Fonte fornecida | Offset da factory |
|---|---|---|---:|
| `DinosaurSpiritEntity.tickTremorsaurus` | `(Lnet/minecraft/world/entity/player/Player;)V` | Player resolvido pelo UUID | 131 |
| `ExtinctionSpearEntity.onHitEntity` | `(Lnet/minecraft/world/phys/EntityHitResult;)V` | Owner; fallback para a própria lança quando nulo | 58 |

Esses são dois callsites compilados, não dois acertos por lançamento. Subterranodon e Grottoceratops não chamam essa factory em seus corpos. Os emissores atribuem UUID de um `LivingEntity`, mas o consumidor resolve apenas Player; um UUID de mob não cria automaticamente um caster válido.

A factory passa `messageCount=1` ao construtor; esse inteiro seleciona variantes da mensagem de morte, não quantidade de hits. O lookup de registry usa Optional.get/getHolderOrThrow, sem fallback local de outro DamageType. `ACCompat.hurt(Entity,DamageSource,float)` devolve o booleano de `Entity.hurt`, sem novo cálculo próprio de críticos, Mastery ou deduplicação.

Os registros `ACEntityRegistry.lambda$static$25` / `$24` declaram, respectivamente, espírito **1F×1F** e lança **0.5F×0.5F**, categoria MISC, update interval **1**, receive velocity updates **true** e fireImmune. São dimensões declaradas; tamanho visual, volume de ataque e range de colisão são contratos diferentes. O binding de `ACEntityDataRegistry.OPTIONAL_UUID` delega ao serializer nativo de UUID opcional, sem codec próprio ou prova de entrega de rede.

`ACCompat.createEntity` devolve `EntityType.create(level)`, sem fallback não nulo, guard adicional de servidor ou confirmação de inserção. Os bindings/lambdas de registro são selados junto dos descritores; não se certifica startup real do loader, mixins externos ou reflexão. O levantamento direto dos 1.555 class entries encontrou os três criadores nativos abaixo nas classes de item/lança; esse levantamento por símbolos não exclui emissores indiretos de outros mods.

## 3. Três tipos de espírito, targeting e movimento

O construtor do espírito começa com `fadeIn=0F`, `duration=0`, `abilityProgress=0F` e `dealtDamage=false`. Os dados sincronizados usam UUID vazio, tipo ordinal `0`, ID do alvo `−1`, delay `0`, fading/usingAbility `false`, nível `0` e rotação `0F`. Getters/setters não implementam um domínio seguro para perks.

`getUsingPlayer()` retorna null sem UUID. No cliente consulta `Level.getPlayerByUUID`; no servidor usa `Server.getPlayerList().getPlayer(uuid)` (`@34–41`), sem guarda própria de mesma dimensão/Level ou vida. `getAttackingEntity()` resolve o inteiro na **Level local**, retornando null para `−1`; não é um UUID persistente nem realiza validação própria de aliado, owner ou tipo LivingEntity.

| Tipo / ordinal | Aquisição e comportamento | Tempo e condição de encerramento |
|---|---|---|
| `SUBTERRANODON` / 0 | Alvo pelo ID; soma ao próprio delta vertical `0.03D + (float)(0.005F×E)`. Quando elegível, zera delta do alvo e fixa sua posição em `spirit.position−(0,target.BbHeight,0)` | Enquanto alvo não nulo e `duration < 40+5×E`, incrementa duration; senão fading. Sem dano próprio |
| `GROTTOCERATOPS` / 1 | Órbita do Player: vetor `(0,1,2)` rotacionado por `−radians(rotateOffset+player.tickCount×5)`, delta `0.25×(destino−posição)`, XRot `10F`, `noPhysics=true` | Sem contador próprio de duração. Só o teste de parada é servidor: item em uso diferente de `EXTINCTION_SPEAR` solicita fading. Sem dano próprio |
| `TREMORSAURUS` / 2 | Olha para os olhos do alvo, define `noPhysics=true`. Em alcance estrito `distanceTo(alvo) < alvo.BbWidth+3.5D`, pode tentar dano; fora, persegue a posição | `if (duration++ > 20)` solicita fading; primeira comparação verdadeira partindo de zero usa duration anterior `21`, na 22ª passagem. Não é descarte aos 20 ticks |

No Subterranodon, impulso é escrito **depois** do movimento/damping comum e afeta movimento posterior. Não há teste local de alvo vivo, LivingEntity, owner/aliados, LOS, distância máxima ou lado servidor nesse corpo; os setters de posição não constituem autorização para mover alvos protegidos.

No Tremorsaurus fora do alcance, o vetor `target.position−spirit.position` só é normalizado se comprimento **>1D**; escreve delta `vetor×0.15000000596046448D`. Dentro do alcance não zera explicitamente o delta anterior. `usingAbility=true` é escrito mesmo fora de alcance. Não há consulta de área, raio de aquisição ou filtro local de LOS/aliança/vida; o alvo já foi fornecido como ID. Largura de registro/colisão e o limiar de distância são parâmetros diferentes.

### Ordem de tick e fading

`tick()` chama `Entity.tick`, resolve o Player e copia os valores visuais anteriores. Se delay é positivo, decrementa um, zera fade, solicita som quando chega a zero e **retorna mesmo nessa passagem de transição**. Movimento, dispatch e temporizadores dos subtipos não avançam nesse ramo; o tick herdado já ocorreu.

Após o delay: fading reduz fade positivo em `1F`; quando `!fading && fade<10F`, ele cresce em `1F`. UsingAbility aumenta abilityProgress até `5F`; desligado, reduz até zero. Fading com fade `<=0` solicita `discard @195`, **sem return** antes do restante. Em seguida solicita partículas apenas no cliente, move por delta anterior (`@235–243`), multiplica delta por `0.8999999761581421D` (`0.9F` alargado), e executa o subtype se Player não é null. Player null solicita fading e pula o dispatch.

Não há guarda própria de servidor sobre movimento, relocalização do alvo ou dispatch/dano Tremorsaurus. Partículas, interpolação e o teste de parada Grottoceratops têm guards particulares. Ausência de guarda no corpo não prova execução duplicada no modpack nem autoriza um adapter a repetir o callback.

A interpolação cliente usa `lSteps` para aproximar coordenadas e XRot, decrementando um; `lerpTo` armazena posição/XRot/passos e restaura `lerpMotion`. O argumento de yaw não é consumido no corpo próprio. São controles de apresentação/movimento, não duração de cast ou range certificado da rede.

## 4. Dano solicitado e diferenças entre os consumidores

### Tremorsaurus

Com alvo não nulo, alcance satisfeito, `abilityProgress>=5F` e `!dealtDamage`, o método pede:

```text
source = causeSpiritDinosaurDamage(registryAccess, player)
amount = (float)(3 + 2 * E)  // operações int antes da conversão
accepted = ACCompat.hurt(target, source, amount)
if (accepted) dealtDamage = true
fading = true
```

Offsets: `dealtDamage @116`; factory `@131`; constantes/multiplicação/adição `@134–142`; helper `@143`; `ifeq @146` pula a escrita da flag `@151`; fading `@156`. O helper delega a `Entity.hurt`; o valor solicitado não é dano líquido garantido.

**Dano recusado pode ser tentado novamente:** fading não bloqueia o dispatch e não há return após discard. Uma recusa deixa `dealtDamage=false`; uma passagem posterior elegível pode voltar ao helper enquanto a entidade ainda é processada. A flag só evita novas tentativas depois de true nessa instância/estado; não fornece token global de cast, deduplicador de eventos ou contagem medida de hits. Timeout, fade visual e aceitação são condições independentes.

### Impacto de Extinction Spear

`onHitEntity` começa em **10F**; só para vítima `LivingEntity` soma `ACCompat.damageBonus(getDefaultPickupItem(),vítima) @29`, com `fadd @32`. Velocidade/carga do arremesso e `3+2×E` do espírito não entram nessa expressão própria. O helper de enchantment e a engine mantêm seus cálculos externos.

A ordem é source com owner/fallback (`@35–58`), **`dealtDamage=true @63–65`**, solicitação de **ignição por 5 segundos `@82–85`**, então **`ACCompat.hurt @92`**. A recusa em `ifeq @95` não desfaz a flag nem a solicitação prévia de fogo. `findHitEntity` retorna null quando a flag é true; senão delega a `AbstractArrow.findHitEntity`. Isso suprime consultas posteriores da classe, sem comprovar imunidade a callbacks externos ou dano aceito.

Quando hurt retorna true e o tipo da vítima é exatamente `ENDERMAN`, `return @108` pula todo o restante: efeitos posteriores, spawn, redução de velocidade e som final. Para outros acertos aceitos:

1. Vítima LivingEntity e owner LivingEntity permitem `ACCompat.postAttackEffects(vítima,owner,source) @139`; vítima LivingEntity recebe `doPostHurtEffects @145`, inclusive sem owner LivingEntity.
2. Owner não nulo permite **uma tentativa** de `SUBTERRANODON`: posição na vítima, Y `targetY+BbHeight`, UUID do owner, ID da vítima, olhar para olhos do owner e nível de `PLUMMETING_FLIGHT`. `addFreshEntity @277` tem retorno descartado em `@280`. Não requer Player nesse ramo; um owner não Player ainda esbarra na resolução de Player do espírito.
3. A cauda comum reduz delta por componentes `(-0.01,-0.1,-0.01) @286–298` e solicita som. **Acerto recusado também alcança essa cauda.** O retorno antecipado do Enderman aceito a evita.

O corpo não acrescenta guard próprio de servidor, filtro explícito de aliado/PvP/LOS ou raio de área. Colisão/eligibilidade herdadas de `AbstractArrow`, eventos e engine continuam fronteiras externas. Não se infere hit garantido, spawn aceito ou repetição segura em outro lado lógico.

### Bloco, wiggling, explosão e retorno

`onHitBlock` chama a implementação herdada e define WIGGLING. `tick` chama `AbstractArrow.tick` primeiro; sua lógica própria de retorno só entra com **`(inGround || isNoPhysics()) && owner!=null`**. Owner deve estar vivo; se for `ServerPlayer`, também não pode ser espectador. Owner ausente pula essa lógica própria, sem remover as regras herdadas de lifetime.

- Owner inválido: somente servidor com pickup `ALLOWED` tenta soltar `getDefaultPickupItem` com argumento `0.1F`; o resultado é descartado. A chamada seguinte a `discard` não fica sob esse guard de servidor.
- Owner válido e WIGGLING: compara o **valor anterior de `ticksWiggling++ > 20`**; partindo de zero, é a 22ª avaliação desse ramo, não um tempo universal de 20 ticks após impacto. Define WIGGLING false e só no servidor chama `explode`. O setter não reinicia o contador; uma nova oscilação não recebe automaticamente outra janela completa.
- `explode()` solicita `TephraExplosion(level,owner,x,getY(0.5),z,1.5F,KEEP)`, `explode()` e `finalizeExplosion(true)`. É outro mecanismo de explosão nativa: não se transforma na factory `spirit_dinosaur` nem em aprovação automática de WorldEffectPolicy. Os internals restantes de dano/blocos desse sistema não são encerrados por esta ficha.
- No ramo não WIGGLING, escreve noPhysics e, se necessário, zera delta antes de calcular **`0.95×deltaAtual + 0.3×normalize(owner.eyePosition−posição)`**. Movimento e pickup são herdados; não há teleport, cap próprio de range ou limiar próprio de descarte por distância.

`tryPickup(Player)` só delega à superclasse se owner for null ou igual ao Player. Esse filtro adicional não ignora capacidade de inventário, modo de pickup ou outras regras herdadas. `shouldRender` retorna true e partículas são clientes; nenhum deles define alcance/hitbox.

O construtor por shooter copia o ItemStack para a superclasse e novamente para o campo próprio `spearItem`. `getDefaultPickupItem()` retorna esse campo, com fallback de stack padrão se null. A cópia própria é usada no bônus/encantamento e não deve ser confundida com garantia de restauração da stack de pickup herdada.

## 5. Emissores, custos, encantamentos e persistência

`ExtinctionSpearItem` tem nove membros próprios e deriva de `SpearItem`, com 12. O dispatch base `hurtEnemy→acHurtEnemy` alcança o produtor sobrescrito. Os emissores próprios não têm guard local de servidor e descartam os booleanos de inserção; isso documenta seus limites, sem afirmar duplicação física em jogo.

| Callback nativo | Emissão e parâmetros | Custo / guarda |
|---|---|---|
| `releaseUsing` | Player; arremessa uma ExtinctionSpearEntity com `shootFromRotation(player,XRot,YRot,0,3.5F×p,1F)` | Exige `p>0.1D`; pede durabilidade 1 MAINHAND **antes da cópia**; após tentativa de inserção, remove uma unidade se não instabuild e registra ITEM_USED |
| `onUseTick` | Só quando `timeUsing==getUseDuration(stack,null)`: tenta criar `N=3+HERD_PHALANX` Grottoceratops na posição do usuário, UUID e rotações `i×360F/N` | Não debita diretamente mana/durabilidade nesse corpo; sem clamp próprio de N e sem teste de spawn aceito |
| `acHurtEnemy` | Solicita fogo 5s; tenta Tremorsaurus no ponto médio horizontal atacante/vítima, **Y=attackerY+1**, UUID do atacante, ID da vítima, CHOMPING_SPIRIT e delay **5** | Depois chama custo base de durabilidade 1 MAINHAND. O callback não mede dano líquido, kill ou spawn aceito |
| Impacto aceito da entidade | SUBTERRANODON associado ao owner/vítima e PLUMMETING_FLIGHT, conforme seção 4 | Sem segundo débito próprio de inventário; owner null e Enderman aceito não produzem esse espírito |

A carga usa `t=72000−timeLeft`, `x=t/20F`, **`p=(x²+2x)/3F`**, limitado somente acima a `1F`. No domínio nativo não negativo, primeiro arremesso permitido em **3 ticks** e carga máxima em **20**; não existe clamp inferior nesse helper para entradas arbitrárias. `72000` é a duração de uso, não lifetime de entidade ou cooldown. O item base rejeita iniciar uso quando a stack é damageable e `damageValue>=maxDamage−1`; senão solicita startUsingItem e resultado consume. Isso não é a remoção da stack, que ocorre no release.

Instabuild usa pickup `CREATIVE_ONLY` e não executa o shrink direto; a solicitação de durabilidade ainda está no caminho anterior e sua efetivação é da engine. Não há rollback local de débito quando inserção é recusada. No release de qualquer Player, inclusive carga insuficiente, chama `killGrottoGhostsFor(player,false)` depois do ramo de arremesso. Não há `addCooldown`, custo Ars/mana/stamina/Soul Energy próprio nesses corpos; isso não define custo global zero para uma integração.

O construtor de Extinction fornece **8D** ao setup de atributos base; no MAINHAND o base solicita modifiers ADD_VALUE de **ATTACK_DAMAGE +8** e **ATTACK_SPEED −3**. São modifiers do item, não a fórmula `10+damageBonus` do impacto, nem `3+2×E` do espírito ou um cooldown final garantido. Mineração só solicita durabilidade 2 se destroySpeed diferente de zero; não produz estes espíritos pelo caminho próprio.

### Grottoceratops: seleção e consumo defensivo

`killGrottoGhostsFor` consulta espíritos no **body AABB do Player expandido em 30 por eixo**, não esfera de raio 30. Filtra UUID igual, tipo GROTTOCERATOPS e `!fading`; não há null-check próprio antes de UUID.equals. Com false marca todos os elegíveis como fading e retorna true mesmo sem match. Com true procura uma única instância, marcando-a se encontrada; a comparação é **`closest.distanceTo(player) > candidate.distanceTo(closest)`**, portanto não se certifica escolha geométrica do mais próximo ao jogador.

`CommonEvents.acCancelDamage` possui um consumidor indireto: vítima Player usando Extinction Spear chama `killGrottoGhostsFor(player,true)`. Quando retorna true, marca seu booleano de cancelamento e solicita som SHIELD_BLOCK (`@91–143`). Outras condições do mesmo handler podem ter marcado a flag antes; o ramo Grotto não é automaticamente pulado. Não há isenção própria por atacante/tipo de dano nesse trecho específico.

O adapter instalado **NeoForge `livingHurt(LivingDamageEvent.Pre)`** pede `setNewDamage(0F)` quando o helper retorna true, em vez do `setCanceled(true)` da fonte Forge adjacente. Isso não prova que o `Entity.hurt` original retornou false, que efeitos posteriores foram cancelados ou que o evento foi entregue/ordenado no modpack. A interação defensiva está documentada estaticamente; invulnerabilidade efetiva e seleção física do espírito continuam pendentes.

### Encantamentos e recursos do item

O registro do item declara **durabilidade 1300**, raridade DEMONIC e fireResistant. `getEnchantmentValue=1`; enchantable somente com stack count `1`; reparo adicional aceita `TECTONIC_SHARD` via `ACRepairableItem.isExtraRepairMaterial`, ou a validação herdada. A receita shaped empacotada usa ` T ` / `TST` / `ABA`: três tectonic_shard, uma limestone_spear, duas amber_curiosity e um heavy_bone. O resultado é extinction_spear, com count omitido no JSON; não é comprovação de receita habilitada ou aquisição real no pack.

| ID de encantamento | `max_level` | `min_cost`: base / por nível acima do primeiro | `max_cost`: base / por nível acima do primeiro | Consumidor relevante |
|---|---:|---|---|---|
| `chomping_spirit` | 2 | 1 / 10 | 41 / 10 | Nível do Tremorsaurus e fórmula `3+2×E` |
| `herd_phalanx` | 3 | 1 / 13 | 41 / 10 | Quantidade `3+nível` de Grottoceratops |
| `plummeting_flight` | 3 | 1 / 13 | 41 / 10 | Nível do Subterranodon e duração/impulso |

Os três têm weight `2`, anvil_cost `4`, slot mainhand e supported_items `#alexscaves:enchantable/extinction_spear`; a tag empacotada contém somente extinction_spear. Esses custos são de encantamento, não mana por cast. `ACCompat.enchantLevel` retorna o primeiro valor armazenado cuja Holder corresponde à chave, ou zero; **não limita o inteiro ao max_level do JSON**. Portanto fórmulas int, quantidades, delay/rotação e setters não oferecem domínio seguro para valores arbitrários; dados efetivos continuam sujeitos a componentes/datapacks/mods.

O bônus da lança vem de `ACCompat.damageBonus`: se a **Level da vítima** é ServerLevel, retorna `EnchantmentHelper.modifyDamage(serverLevel,stack,vítima,vítima.damageSources().generic(),0F)`; em outra Level retorna `0F`. Não é uma fórmula universal de +nível. A sobrecarga `postAttackEffects(LivingEntity,LivingEntity,DamageSource)` usada pela lança testa a Level do **primeiro argumento** e delega `EnchantmentHelper.doPostAttackEffects(serverLevel,primeiroArgumento,source)`; o segundo LivingEntity não é repassado nesse corpo 1.0.10. Não trocar pela sobrecarga que recebe Entity nem inferir callbacks garantidos de atacante/vítima.

O helper de durabilidade encaminha os argumentos a `ItemStack.hurtAndBreak`; consume/pass não removem a stack por si. O stat hook de SpearItem chama `ACCompat.itemAttributes`, que percorre os slots e monta modifiers nativos, com fallback quando todos são null. **Paridade de fonte:** a classe instalada `ItemStackAttributeModifiersMixin` é apenas construtor; a lógica de stat deste item vem do override direto, não da injeção vista na fonte 1.1.1.

### Persistência e entradas de estado

Os métodos próprios `DinosaurSpiritEntity.readAdditionalSaveData` / `addAdditionalSaveData` só leem/escrevem `UsingPlayerUUID` e `DinosaurType`, sem chamada própria a `super` nesses dois corpos. Não persistem explicitamente ID de alvo, nível, delay, rotação, duração, progresso, fading, usingAbility ou dealtDamage. Persistência genérica de `Entity` é outra camada; não declarar ausência de todo NBT. Reconstrução não restaura automaticamente esses estados transitórios.

O enum selado contém **três entradas**, mas `getDinosaurType` executa `values()[Mth.clamp(raw,0,values().length)]` (`@0–15`). O limite superior é **3**, sem ser um índice válido de `0..2`. O setter público por enum usa ordinal; leitura NBT alcança o setter inteiro. Uma entrada raw `3` ou maior chega estaticamente ao índice `3`; valores negativos são limitados a zero. É risco de contrato de entrada observado no código, **sem crash físico reproduzido**. Não certificar setters/NBT arbitrários como hooks seguros.

A lança não declara overrides próprios de save/read adicionais: seu `spearItem`, `dealtDamage`, `WIGGLING` e `ticksWiggling` não têm serialização adicional própria nessa classe. O ciclo herdado de `AbstractArrow` continua externo; essa observação não comprova perda total de NBT nem retorno/pickup correto após reload.

## 6. Integração com Black Arcana, Enshrouded e RPG Skill Tree

| Perk / sistema pretendido | Contrato que precisa preservar | Estado |
|---|---|---|
| Dano/efeitos/Mastery | Player resolvido versus owner/fallback, dano recusado versus flag, ignição anterior e callbacks posteriores | `NOT_VERIFIED`; nenhum proc por simples callsite, som ou criação de entidade |
| Range, target ou área | ID local preatribuído, distância estrita e tamanho do alvo; a lança usa colisão herdada | Aumentar limiar não cria AoE, LOS, autorização PvP ou captura segura de alvo |
| Duração, delay ou cooldown | Delay retorna; fading não interrompe dispatch; tempo do tipo e uso do item têm owners próprios | Não converter fade visual ou tag de dano em cooldown de magia |
| Projétil, velocidade e tamanho | Física herdada, dimensões de registro, vetor da lança, perseguição e relocalização do Subterranodon | Sem hook mutador por jogador comprovado; não confundir render scale com hitbox |
| Invocação e multiplicidade | Callbacks diferentes produzem três tipos; retornos de inserção descartados | Não repetir spawn, custo, settlement ou tentativas de dano em adapter |
| Persistência/servidor | UUID versus ID volátil, campos não persistidos e ausência de alguns guards locais | Reload, multiplayer e stack efetiva continuam QA pendente |

Black Arcana preserva autoridade nativa de custo, dano, autoria e movimento. WorldEffectPolicy e proteção de alvo não são automaticamente aplicados por uma leitura de bytecode; RPG Skill Tree fornece progressão/perks/Mastery apenas por boundary verificada. Não há implementação de adapter, conversão de escola, alteração de damage tags, nova ação Enshrouded ou promoção de Stage nesta ficha.

## 7. Validação, evidência e limites

O [selo consolidado](../EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json) cobre todos os membros próprios das duas entidades e enum, os emissores do item/base e os helpers/recursos delimitados. Não certifica toda a física de `Entity`/`AbstractArrow`, todos os encantamentos globais, o item inteiro ou o provider. Os descriptors, recursos e âncoras são reexaminados no publisher JAR por SHA-1/SHA-256/tamanho; testes semânticos conferem as ordens causais que impedem confundir tentativa com dano aceito.

Preservados como evidência histórica: [12 métodos selecionados da PR #988](../EXACT-SPIRIT-DINOSAUR-1.0.10.json), [JSON/tags](EXACT-RESOURCE-MANIFEST-1.0.10.json) e [factories/consumidores](EXACT-CONSUMERS-1.0.10.json). Seus limites parciais não são reescritos e não homologam execução física. Fonte 1.1.1 e mixins externos não substituem o JAR 1.0.10.

**Contabilidade:** uma ficha já existente do tipo de dano; **+0 raízes mágicas novas**. O universo continua aberto e mantém oito raízes históricas. `STATIC_TECHNICAL_CATALOG_ONLY` não concede mutação: `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`.

QA física pendente: dano recusado/repetido e ordem de efeitos, spawn recusado, owner ausente/não Player/outra dimensão, colisões/aliados/PvP, relocalização protegida, retorno/pickup, uso simultâneo cliente/servidor, enchant levels não nativos, NBT inválido, save/reload, desconexão e composição com perks. Nenhum desses resultados é presumido a partir do certificado estático.
