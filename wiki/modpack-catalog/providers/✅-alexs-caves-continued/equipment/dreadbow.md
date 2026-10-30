# Dreadbow — carga, janela perfeita, chuva de flechas e modo contínuo

Provider **Alex's Caves Continued**; item `alexscaves:dreadbow`; owner `server.item.DreadbowItem`, subclasse de `ProjectileWeaponItem`. O item implementa `ACTickingItem`, `UpdatesStackTags`, `ACClientExtensionItem` e `ACEnchantableItem`. Este é um contrato de equipamento e de seus dois caminhos de disparo; não acrescenta raiz ao inventário histórico de oito ações sobrenaturais.

Autoridade: JAR **1.0.10**, arquivo publisher `8856293`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A [prova comum](../EXACT-DREADBOW-CONTRACTS-1.0.10.md) e seu manifesto selam esta ficha, classes, recursos e localizadores JVM. O source público `523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**, sem paridade de build comprovada com 1.0.10. Parâmetros `VERIFIED_EXACT_BINARY`; hook mutador `NOT_VERIFIED`; QA física `NOT_TESTED`; receitas/tags efetivas do pack `NOT_VERIFIED`.

## Identidade, aquisição e superfície pública

`ACItemRegistry.<clinit>()V @2497–2511` registra `dreadbow`; `lambda$static$137()Item` constrói `DreadbowItem`. Seu construtor declara raridade do provider `RARITY_DEMONIC` e **500** de durabilidade. A receita física `data/alexscaves/recipe/dreadbow.json`, padrão ` VS / P S / VS` conforme as três linhas literais `" VS"`, `"P S"`, `" VS"`, usa **1 Pure Darkness, 2 Vesper Wings e 3 Shadow Silk**, produzindo um Dreadbow. Overrides do pack não foram executados.

| Entrada / propriedade | Contrato estático |
|---|---|
| `use(Level,Player,InteractionHand)` | Obtém stack da mão e `player.getProjectile(stack)`. Aceita se criativo **ou** projétil não vazio; caso contrário falha. Cria protótipo para armazenar seu tipo em `LastUsedArrowType`, chama `startUsingItem(hand)` e retorna `ACCompat.useConsume`. Shaded Respite não participa desse gate inicial. |
| Duração / animação | `getUseDuration(ItemStack,LivingEntity)=72000`; `getUseAnimation(ItemStack)=BOW`. O limite de uso não é uma espera de72000 ticks para disparar. |
| Munição suportada | `getAllSupportedProjectiles()` retorna `ARROW_ONLY`. A seleção efetiva é delegada a `Player.getProjectile`; este contrato não redefine todas as regras vanilla/modpack dessa seleção. |
| Range padrão | `getDefaultProjectileRange()=64`. É metadado da arma; os cálculos próprios de mira abaixo usam `128*p` e `42*p`, sem clamp por esse64. Não é alcance máximo de voo certificado. |
| Encantabilidade | `getEnchantmentValue()=1`; `isEnchantable(stack)` exige `count==1`. |
| Reequip | `shouldCauseReequipAnimation(old,new,slotChanged)` retorna false quando ambos são Dreadbow; o argumento `slotChanged` não decide nesse caso. |
| Adapter genérico | `shootProjectile(LivingEntity,Projectile,int,float,float,float,LivingEntity)` delega a `shootFromRotation(shooter,xRot,yRot+angle,0,speed,inaccuracy)`. O índice e target recebidos não participam desse corpo; não substitui os dois loops customizados descritos adiante. |

`createArrow(Player,bow,ammo)` usa o argumento ammo se não vazio; se vazio, consulta novamente `player.getProjectile(bow)`. Usa seu `ArrowItem`, ou `Items.ARROW` como factory quando o item não é ArrowItem, e chama `ArrowItem.createArrow(level,selectedStack,player,bow)`. Essa delegação pode carregar comportamento vanilla/de outro mod. Não há `EnchantmentHelper` adicional próprio de Power/Flame/Infinity nesses corpos; isso não prova ausência desses efeitos em uma factory ou hook externo.

## Carga visual e janela de Perfect Shot

Os dados são `DataComponents.CUSTOM_DATA`, por `ACCompat.getTag/getOrCreateTag/setTag`. As leituras retornam cópias de tags; os setters gravam o componente novamente. `UseTime`, `PrevUseTime`, `PerfectShotTicks` e `LastUsedArrowType` não são mana nem cooldown de Black Arcana.

Defina `M = getMaxLoadTime(stack)`: se **Relentless Darkness >0**, `M=5`; caso contrário, **`M=40−8*level(Dark Nock)`**. Para níveis de dados0/1/2/3, o segundo ramo resulta40/32/24/16. Não há clamp de nível/denominador nesse helper; níveis externos às restrições normais do JSON não ganham segurança apenas porque o método existe.

| Helper / consumidor | Fórmula ou regra |
|---|---|
| `getUseTime(stack)` | Lê `UseTime`; sem tag retorna0. |
| `setUseTime(stack,value)` | Antes de escrever `UseTime=value`, grava `PrevUseTime=getUseTime(stack)`. Não limita o valor. |
| `getPerfectShotTicks(stack)` | Lê `PerfectShotTicks`; sem tag retorna0. Não verifica encantamento, jogador, mão ou carga. |
| `setPerfectShotTicks(stack,value)` | Escreve literalmente o int fornecido e o componente; não aplica clamp, custo ou validação de progresso. |
| `getLerpedUseTime(stack,partial)` | `prev + partial*(current−prev)`, com defaults0; não limita `partial`. |
| `getPullingAmount(stack,partial)` | `min(getLerpedUseTime/M,1F)`, sem clamp inferior. É usado pelo renderer, não pelo cálculo de potência de `releaseUsing`. |
| `LastUsedArrowType` | `use` guarda o ID do tipo do protótipo; `getTypeOfArrow` faz lookup no registry quando a string existe, ou retorna null sem ela. O renderer usa esse tipo para a flecha de apresentação; não autoriza munição nem fixa o tipo da próxima entidade real. |

`ItemStackTickMixin.ac_inventoryTick` identifica um item `ACTickingItem` e chama `acInventoryTick(stack,level,entity,selected)`. O Dreadbow implementa essa interface no classfile1.0.10; `alexscaves.mixins.json` lista o mixin e `META-INF/neoforge.mods.toml` declara essa configuração. O callback é, portanto, uma superfície estaticamente conectada, sem alegação de execução física. O método decide `using` por `entity instanceof LivingEntity` e igualdade de `entity.getUseItem()` com este stack; o booleano `selected` não controla sua lógica.

**Todas as escritas/contagens de carga neste callback estão no ramo `level.isClientSide()`**. Depois de capturar `oldUseTime`, executa em ordem:

1. Harmoniza `PrevUseTime` quando difere de `UseTime` e grava a tag.
2. Se usando e `PerfectShotTicks>0`, decrementa1 e envia `UpdateItemTagMessage(entity.id,stack)` ao servidor.
3. Se usando e `oldUseTime<M`, incrementa a carga visual em **1**, ou **3** com Relentless, via `setUseTime`. Com Twilight Perfection positivo, se `newUseTime>=M` e `oldUseTime<=M`, concede **`4+3*(level−1)`** ticks:4/7/10 para níveis1/2/3. Se ainda não cruza esse limiar, escreve0; ambos os ramos enviam a tag. O teste externo `oldUseTime<M` delimita essa concessão, que não é renovada enquanto permanece carregado.
4. Com Relentless, usando e **oldUseTime>=M**, zera `UseTime`; usa o valor capturado antes do incremento, não o recém calculado.
5. Se não usando e `oldUseTime>0`, reduz `UseTime` a `max(0,oldUseTime−5)` e zera a janela perfeita. Não há reset incondicional de `PerfectShotTicks` nesse ramo quando o oldUseTime já é0.
6. Se usando, gera partículas cliente. Esse efeito não dispara flechas nem valida dano.

A janela perfeita é reconhecida no release por **Twilight Perfection >0 e `getPerfectShotTicks(stack)>0`**. Não há contador independente servidor que reconstrua essa janela em `acInventoryTick`. `releaseUsing` não usa `UseTime` para calcular potência nem o zera diretamente ao final. Resultado físico da janela depende de sincronização e ordem dos callbacks;4/7/10 são os valores escritos, não uma promessa de janela medida com latência.

## Disparo normal em `releaseUsing`

O corpo exige `user instanceof Player` e **Relentless Darkness <=0**. Calcula **`t=72000−remainingUseTicks`**, `x=t/M` em float e **`p=(x*x+2*x)/3`**, limitando a1 somente quando `p>1`. Só prossegue se **`(double)p>0.1D`**. Sem Dark Nock, no domínio usual de t inteiro não negativo, o primeiro t que passa a fórmula é6; não transformar isso em regra universal para outros M/valores externos.

Consulta `Precise Volley>0`, `Shaded Respite>0 && !DarknessIncarnateEffect.isInLight(player,11)` e o gate perfeito acima. Toca som de release, seleciona munição e, se Shaded Respite elegível e stack vazio, cria um stack de `Items.ARROW`. Obtém protótipo via `createArrow`; se null, retorna sem o restante da salva/cobrança. **O gate inicial `use` continua exigindo munição para não criativo**, mesmo que o ramo posterior possa construir fallback em escuridão.

### Mira, distribuição espacial e quantidade

| Parte | Fórmula / limites de bytecode |
|---|---|
| Mira inicial | `ProjectileUtil.getHitResultOnViewVector(player,predicate,128F*p)`. O `BootstrapMethods` do item fixa o predicate como **`Entity.canBeHitByProjectile()`**. Não há filtro próprio adicional de aliança, PvP, Player ou classe LivingEntity nesse item. |
| Fallback | Se `hit.getType()==MISS`, refaz a consulta com **`42F*p`** e o mesmo predicate. O novo hit substitui o anterior. Os filtros internos de `ProjectileUtil` são delegados vanilla. |
| Centro elevado | Constrói BlockPos a partir de `(hitX,hitY+1.5D,hitZ)`; enquanto Y abaixo do teto de construção, bloco vazio e contador<15, sobe1. É busca vertical limitada, não alcance esférico ou scanner de proteção. |
| Conversão | `isConvertibleArrow(entity)` exige **`instanceof Arrow` e `Arrow.getColor()==−1`**. Não é teste de ID `minecraft:arrow`; outros tipos derivados podem diferir. |
| Iterações | `ceil(30F*p)` se conversível; **`ceil(8F*p)`** se não. São iterações/solicitações de spawn, não contagem certificada de entidades aceitas ou hits. |
| Spawn de cada flecha | Centro do BlockPos elevado + `(random*16−8, random*4−2, random*16−8)`: caixa candidata de16×4×16. Se bloco ocupado e fluido vazio, ressorteia até6 vezes; se ainda bloqueado/seco, usa o centro. Fluido não vazio encerra esse teste sem exigir bloco vazio. |
| Direção | `hitLocation−spawnPosition`; chama `arrow.shoot(dx,dy,dz,speed,inaccuracy)`. `speed=0.5F+1.5F*nextFloat()`, intervalo nominal **[0.5,2)**; não é multiplicado por p. |
| Imprecisão | Precise:0. Caso contrário, conversível `20F+10F*r`; não conversível `5F+10F*r`. Sem Precise, uma condição `nextFloat()<0.25F` substitui esse valor por outro `nextFloat()` em[0,1). |

O destino é o ponto do hit de mira, não um lock persistente nesta classe sobre a entidade atingida. O item não altera dimensões registradas do projétil. Range de consulta, espaço de spawn, velocidade e colisão posterior são contratos distintos.

### Configuração da flecha e liquidação

No ramo conversível, **cada iteração cria novo `DarkArrowEntity(level,user)`**, escreve `shadowArrowDamage = Precise ?2F:3F` e `setPerfectShot(perfect)`. No não conversível, usa o protótipo da factory; se perfeito, escreve **`baseDamage anterior*2D`**. Colisão, dano aplicado, tags e proteção pertencem ao contrato do [Dark Arrow](../damage-types/dark-arrow.md) ou da entidade externa; o item não calcula o dano final aceito.

Após cada `addFreshEntity(arrow)`, cujo booleano de retorno é descartado, o loop cria outro protótipo via `createArrow` e marca esse próximo protótipo `CREATIVE_ONLY`; faz isso inclusive depois da última tentativa de spawn. O protótipo inicial recebe `ALLOWED` antes do loop. **A conversão substitui o objeto por novo DarkArrow após essa atribuição**: não inferir desse `ALLOWED` que todas as flechas sombrias sejam recuperáveis. No ramo não conversível, os protótipos posteriores mantêm a atribuição `CREATIVE_ONLY` neste corpo. Não há nova checagem de null depois dessas recriações, antes da escrita `pickup`.

Ao final, se houve caminho conversível, solicita som de chuva no ponto de mira, volume12F. Depois, **somente fora criativo**:

- sem Shaded Respite elegível, solicita **1** de desgaste no arco por `ACCompat.hurtAndBreakUsedHand`, delegando a `ItemStack.hurtAndBreak` no slot da mão em uso;
- encolhe a munição em **1 por salva**, salvo quando Shaded Respite elegível e `ammo.is(Items.ARROW)`; munição especial continua consumida mesmo nesse ramo;
- não verifica o booleano dos spawns antes desses débitos. Não há custo por cada flecha da salva nem cooldown/mana/fome explícitos nesse método.

## Modo Relentless em `onUseTick`

Após chamar o super, exige Player, **Relentless Darkness >0** e **`remainingUseTicks %3 ==0`**. O teste usa o argumento restante do callback, não duração transcorrida nem `UseTime`; **não exige `UseTime>=getMaxLoadTime()`**. O helper M=5 atua na carga/animação, sem se tornar atraso mínimo explícito de disparo neste corpo. Cadência física depende da execução dos callbacks no modpack.

Seleciona munição e Shaded Respite como acima, obtém protótipo, calcula conversibilidade. Não repete o gate `creative || !ammo.isEmpty()` do início de uso nem chama `stopUsingItem` por falta de munição nesse corpo; o resultado de uma factory com stack vazio é uma dependência, não uma garantia de disparo gratuito. Para conversível escolhe **`1+nextInt(2)`** iterações (1 ou2); não conversível1. A cada iteração:

| Campo | Regra |
|---|---|
| Pickup | Escreve `ALLOWED` no objeto atual antes de possível conversão; o próximo protótipo criado ao final recebe `CREATIVE_ONLY`, mas volta a `ALLOWED` no início da próxima iteração. A substituição por novo DarkArrow também ocorre depois da atribuição. |
| Dark Arrow | Se conversível, cria novo DarkArrow e escreve **shadow damage2F**; este corpo **não chama `setPerfectShot`**. |
| Posição | Posição inicial da entidade de flecha + `(r−0.5,r−0.5,r−0.5)`, jitter nominal[−0.5,0.5) em cada eixo; não usa o centro elevado da chuva. |
| Direção / velocidade | `player.getViewVector(1F)`; `shoot(...,4F+3F*r,inaccuracy)`, speed nominal **[4,7)**. Imprecisão inicial **0.5F**, acrescida2F depois de cada iteração; segunda iteração usa2.5F. |
| Spawn | `level.addFreshEntity` com retorno descartado, seguido de recriação do protótipo. A leitura inicial de conversibilidade não protege null explicitamente; sem protótipo válido, os acessos posteriores não têm retorno antecipado equivalente ao `releaseUsing`. |

Após o loop, aplica **a mesma regra de custo por callback de disparo**: fora criativo,1 desgaste salvo Shaded Respite elegível e1 munição salvo flecha comum com essa elegibilidade. Não cobra1 munição por cada uma das1/2 flechas. Precise Volley/Twilight Perfection não são consultados nesse corpo, mesmo se tags externas produzirem combinação fora do JSON normal.

## Encantamentos que têm consumidores próprios no item

Todos os JSONs abaixo suportam `#alexscaves:enchantable/dreadbow`, slot `mainhand`; o tag exato contém `alexscaves:dreadbow`. `ACCompat.enchantLevel` procura entries do componente de encantamentos por `Holder.is(ResourceKey)` e retorna o nível encontrado, ou0. Não impõe os máximos do JSON dentro dos cálculos do item.

| Encantamento | Máximo de dados / peso / anvil | Consumer e fórmula |
|---|---|---|
| Dark Nock | 3 /2 /4 | M=40−8L; não muda diretamente speed/alcance independente de p. |
| Twilight Perfection | 3 /2 /4 | Concessão cliente4+3(L−1), countdown e tag; release requer L>0+contador>0; flag DarkArrow ou dobra base damage da não conversível. |
| Precise Volley | 1 /2 /4 | Release: shadow2 em vez3, imprecisão0. Não reduz por si a contagem da salva neste método. |
| Shaded Respite | 1 /1 /8 | Gate de luz<11 pelo helper do Darkness, incluindo root vehicle/sky; poupa desgaste e flecha comum nas regras acima. Não habilita início de uso sem munição no gate `use`. |
| Relentless Darkness | 1 /1 /8 | Redireciona para `onUseTick`, periodicidade remaining%3, M5 visual e incremento visual3. JSON declara exclusão com Precise Volley, Dark Nock e Twilight Perfection; essa compatibilidade de dados não é uma guarda desses três IDs em cada método. |

Os custos de encantamento de dados são funções lineares. `min_cost.base=1` para os cinco; `per_level_above_first` respectivamente **10/7/18/9/20** na ordem da tabela. `max_cost.base=41`, incremento10 para todos. Não são mana/cooldown por cast. Overrides de enchantments/tags e níveis anormais continuam não verificados.

## Autoridade, sincronização e pontos de integração

Os corpos próprios `use`, `releaseUsing` e `onUseTick` **não contêm guarda direta `!isClientSide`** antes das operações descritas. Isso não prova spawn efetivo duplicado em jogo: callbacks vanilla, lado de execução, factories e `Level.addFreshEntity` ainda determinam o resultado físico. O callback de inventário, por sua vez, limita a geração da janela perfeita ao cliente explicitamente.

O item implementa `UpdatesStackTags`. `UpdateItemTagMessage.handle` usa o sender/contexto para obter um Level, resolve `message.entityId`, exige LivingEntity e escolhe mão principal ou secundária cujo **tipo de item** corresponde ao stack recebido. Para um item implementando a interface, aplica a CUSTOM_DATA recebida via `updateTagFromServer`. O corpo não compara a entidade resolvida com o sender nem reconstrói `UseTime`/`PerfectShotTicks`, encantamento ou progresso legítimo. O setter default copia a tag fornecida; não estabelece autoridade segura de uma perk. Essas limitações estáticas não foram reproduzidas como exploit em multiplayer.

`ACItemstackRenderer` consome `getPullingAmount`, `getTypeOfArrow` e `getPerfectShotTicks` para modelo/flecha/olho perfeito. A apresentação positiva não comprova contador servidor sincronizado nem dano aceito. `LastUsedArrowType` e esses getters públicos não são API de autorização.

Sete campos estáticos cobertos: identidade/receita; lifecycle de uso/carga/release; fórmulas, unidades e limites; mira/distribuição e conversão; cobrança/delegação dos custos; consumidores, sincronização e autoridade; e reprodução por bytes/métodos do JAR. Range, quantidades, speed, base damage, janela perfeita e custo possuem owners e momentos diferentes. Qualquer mutação futura precisa escolher um seam servidor e preservar a contagem única de consumo/dano. Hooks `NOT_VERIFIED`; nenhuma alteração runtime foi implementada.

QA física permanece `NOT_TESTED`: gatilhos normal/Relentless, janela de níveis1/2/3 com latência, stack nas duas mãos, inventário/reequip/logout/reload, níveis anormais, Shade com/sem munição e luz10/11/root vehicle, entidades spawn recusadas, flechas vanilla/especiais/modded e factory null, PvP/proteção/alianças, client versus dedicado, contagem real de impactos e integração com perks.

## Localizadores JVM

Prefixo `com.github.alexmodguy.alexscaves`. Offsets são do método de 1.0.10; os descritores/fatos detalhados constam no manifesto selado.

| Método | Descritor / regiões |
|---|---|
| `server.item.DreadbowItem.<init>` / `getUseDuration` | `()V @0–23`; `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;)I @0–2` |
| `DreadbowItem.use` | `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder; @0–114` |
| `DreadbowItem.acInventoryTick` | `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;Z)V @0–400`; cliente@38–400; decremento@85–119; grant@154–253; Relentless/reset@256–305 |
| `DreadbowItem.getMaxLoadTime` / `getUseTime` / `getPerfectShotTicks` | `(Lnet/minecraft/world/item/ItemStack;)I @0–25` / `@0–19` / `@0–20` |
| `DreadbowItem.setUseTime` / `setPerfectShotTicks` | `(Lnet/minecraft/world/item/ItemStack;I)V @0–27` / `@0–18` |
| `DreadbowItem.getLerpedUseTime` / `getPullingAmount` | `(Lnet/minecraft/world/item/ItemStack;F)F @0–46` / `@0–15` |
| `DreadbowItem.getPowerForTime` | `(ILnet/minecraft/world/item/ItemStack;)F @0–30` |
| `DreadbowItem.releaseUsing` | `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;I)V @0–899`; gates@0–180, mira/centro@185–323, quantidade@323–369, flechas@372–801, custo@857–896 |
| `DreadbowItem.onUseTick` | `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V @0–382`; gates@9–63, count@125–153, spawns@159–337, custo@340–379 |
| `DreadbowItem.createArrow` / `isConvertibleArrow` | `(Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/entity/projectile/AbstractArrow; @0–62`; `(Lnet/minecraft/world/entity/Entity;)Z @0–25` |
| `DreadbowItem.shootProjectile` | `(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/projectile/Projectile;IFFFLnet/minecraft/world/entity/LivingEntity;)V @0–21` |
| `mixin.ItemStackTickMixin.ac_inventoryTick` | `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;IZLorg/spongepowered/asm/mixin/injection/callback/CallbackInfo;)V @0–41` |
| `server.message.UpdateItemTagMessage.handle` | `(Lcom/github/alexmodguy/alexscaves/server/message/UpdateItemTagMessage;Lcom/github/alexmodguy/alexscaves/server/message/ACNetworkContext;)V @0–179` |
| `server.item.UpdatesStackTags.updateTagFromServer` | `(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/nbt/CompoundTag;)V @0–5` |
| `server.misc.ACCompat.hurtAndBreakUsedHand` / `enchantLevel` | `(Lnet/minecraft/world/item/ItemStack;ILnet/minecraft/world/entity/LivingEntity;)V @0–13`; `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/resources/ResourceKey;)I @0–61` |

Recursos exatos: receita e tag `enchantable/dreadbow`, cinco JSONs de enchantment acima, lang, configuração de mixins e metadata NeoForge do artefato. Inspeção estática reproduzível não substitui os testes físicos listados.
