# Darkness Incarnate — efeito de voo e apresentação sombria

Provider **Alex's Caves Continued**; ID `alexscaves:darkness_incarnate`; campo `ACEffectRegistry.DARKNESS_INCARNATE`; implementação `server.potion.DarknessIncarnateEffect`, subclasse de `ACMobEffect`. O registro constrói um efeito `BENEFICIAL`, cor decimal `5312014`. Este contrato descreve o estado aplicado à entidade; não acrescenta outra raiz ao [cast do Cloak](../actions/cloak-darkness-incarnate.md).

Autoridade: JAR **1.0.10**, arquivo publisher `8856293`, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A [prova comum dos efeitos](../EXACT-EFFECT-CONTRACTS-1.0.10.md) e seu manifesto selam os bytes examinados. O source público `523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e não é autoridade de parâmetros de 1.0.10. Estado estático `VERIFIED_EXACT_BINARY`; hook mutador `NOT_VERIFIED`; QA física `NOT_TESTED`; configuração efetiva do pack `NOT_VERIFIED`.

## Identidade e descrição funcional

O estado habilita voo no jogador servidor, acelera sua velocidade de voo, zera a distância de queda e acrescenta impulso vertical quando a entidade está no chão. Luz forte pode encerrá-lo. A apresentação cliente inclui trilha, shader e escurecimento do modelo; esses consumidores visuais não concedem voo nem alteram a luz física do mundo.

`ACEffectRegistry.<clinit>()V @121–135` registra o nome `darkness_incarnate`. A classe do efeito não registra `AttributeModifier` próprio: o voo escreve diretamente `Abilities`, e não um atributo de velocidade, alcance ou dano.

## Aplicação, duração e custo

| Produtor exato | Regra estática e limite |
|---|---|
| `DarknessArmorItem.onKeyPacket(Entity,ItemStack,int)` | Passando `canChargeUp(entity,false)`, zera `CloakCharge` e aplica o efeito com duração `darknessCloakFlyTime`, amplifier `0`, não ambient, sem partículas/ícone. Default declarado **200 ticks**; intervalo **20..2147483647**. Carga declarada **1000 ticks**, mesmo intervalo. Não interpretar esses defaults como configuração instalada. |
| `DarkenedAppleItem.finishUsingItem(ItemStack,Level,LivingEntity)` | Exige efeito já presente e `ACCompat.food(stack,entity) != null`; cria nova instância com **duração atual +600 ticks** e mesmo amplifier, usa `forceAddEffect(instance,null)` e dispara advancement, depois delega ao `Item.finishUsingItem`. Não concede o estado a uma entidade sem efeito. Não trata a duração infinita separadamente nesse método. |
| Comida / aquisição da maçã | `ACFoods.<clinit>()V @536–554` declara nutrição `4`, saturação `0.35F`, `alwaysEat`; não adiciona Darkness Incarnate por probabilidade de comida. A receita ` D /DPD/ D ` usa uma maçã e quatro `alexscaves:pure_darkness`. |

A classe de efeito não debita mana, fome, durabilidade nem cooldown por tick. O Cloak cobra a carga na ativação; a maçã passa pelo consumo vanilla do item. Os detalhes de elegibilidade, ordem da carga, receita do equipamento e limites do pacote estão na ficha do Cloak. Não reexecutar esses débitos em Black Arcana. Mudanças em duração devem preservar a diferença entre início, atualização e extensão de uma instância existente.

## Tick, voo e encerramento

`ACMobEffect.applyEffectTick(LivingEntity,int)Z` chama `tick` e retorna `true`; `shouldApplyEffectTickThisTick(int,int)Z` delega a `shouldTick`. Em Darkness, `shouldTick(duration,amplifier)` retorna **duration >0**. A duração infinita representada por valor não positivo não é convertida aqui em um tick positivo; a semântica de execução vanilla/modpack para efeitos infinitos exige QA própria.

| Operação | Regra de 1.0.10 |
|---|---|
| `tick(LivingEntity,int)` | Chama `superTick`, depois `toggleFlight(entity,true)`; se `onGround`, acrescenta `(0,0.1D,0)` à velocidade. O amplifier recebido não escala esses valores. |
| Voo habilitado | Apenas em lado servidor e `ServerPlayer`: define `mayfly=true`, `flying=true`, velocidade `0.05F*4F = 0.2F`. A função zera `fallDistance` também depois desse bloco, para a entidade recebida. |
| Voo encerrado | Escreve velocidade **0.05F**. Fora spectator, escreve `flying=false`; para não criativo escreve também `mayfly=false`; se houver `DarknessIncarnateUserAccessor`, sinaliza Slow Falling. Não restaura um snapshot do voo anterior. |
| Atualização de abilities | `onUpdateAbilities()` é chamado somente se o valor anterior de `flying` difere do booleano solicitado ao método; não concluir que qualquer alteração de speed/mayfly produz pacote próprio. |
| Pós-voo | `LivingEntityMixin.ac_livingTick` consome a flag e adiciona **80 ticks** de Slow Falling vanilla, amplifier `0`, sem partículas/ícone, então limpa a flag. |
| Cancelamento por luz | `CommonEvents.livingTick` verifica a presença do estado e `tickCount %5==0`; remove quando `isInLight(entity,11)` retorna true. O teste usa a **posição de bloco do root vehicle**, block light e substitui a luz por `15` quando vê o céu e `ACCompat.sunAboveHorizon` passa. Limiar **>=11**. |
| Fim / atualização | `onEffectEnd` reinicia os dois contadores internos e chama `toggleFlight(false)`. Mixins de remoção chamam `onEffectEnd`; atualização com booleano `true` chama end seguido de start. Os eventos Remove/Expired também têm caminhos próprios de voo desligado e som de saída. |

Não há filtro de armadura no corpo de `tick` nem no cancelamento por luz; perder o Cloak não é condição explícita desses métodos para remover o efeito. O callback de luz examinado não introduz uma guarda própria `!isClientSide`. Mobs também recebem o impulso no chão e reset de queda, mas o bloco que escreve `Abilities` exige `ServerPlayer`. Portanto, alterar o tipo de alvo não transforma automaticamente todos os alvos em jogadores voadores.

## Contadores e apresentação cliente

`lastDuration` e `firstDuration` são **campos da instância de MobEffect**, não dados anexados ao portador. `onEffectStart`/`onEffectEnd` os reiniciam para `-1`. `shouldTick` atualiza `lastDuration` e inicializa `firstDuration`; `getActiveTime()` retorna `firstDuration-lastDuration`. Não usar esse valor como cronômetro individual autoritativo de uma perk. Possível influência entre portadores na intensidade visual precisa de reprodução; não foi demonstrada falha em jogo.

`getIntensity(entity,partial,max)` retorna `0` sem efeito; para `isInfiniteDuration()` retorna literalmente **`max`**, sem normalização; nos outros casos calcula `min(max,min(activeTime+partial,duration+partial))/max`. O consumidor `ACPotionEffectLayer.render` passa `max=25F`. A função não exige `max>0`; preservar esses limites em qualquer análise visual.

| Consumidor cliente | Papel comprovado |
|---|---|
| `ACPotionEffectLayer.render` | Efeito presente, configuração `radiationGlowEffect` e entidade viva habilitam overlay preto translúcido com a intensidade acima. O nome da config não é uma escola de dano. |
| `ClientEvents.renderStage` | Seleciona shader Watcher para câmera elegível com o estado; concorre com outros ramos de shader. Não é filtro de targeting servidor. |
| `ClientEvents.clientLivingTick` e `acPostRenderLiving` | Mantêm/apresentam a trilha sombria de entidade viva; não aplicam dano nem debitam carga. |
| `ACLightmapAdditions.ambientBonus` | Quando `biomeAmbientLight` permite o cálculo e a câmera LivingEntity tem o estado, usa piso visual `max(ambient,0.35F)`; não altera block light do teste de cancelamento. |

## Integração e validação

Os sete campos estáticos estão cobertos: identidade compilada; comportamento/lifecycle; fórmulas e limites; targeting do portador e gates do voo; custos dos produtores; consumidores/autoridade; e evidência binária reproduzível. Não há dano ou projétil próprio para trocar de escola ou redimensionar. Duração, carga, luz, destino do efeito e velocidade de voo têm owners distintos. Um adapter precisa observar uma ativação liquidada uma única vez, preservar a ordem dos callbacks e arbitrar a posse de voo com outros mods. Reaplicar `addEffect`, zerar carga ou restaurar abilities em paralelo não constitui hook homologado.

QA física permanece `NOT_TESTED`: duração normal/infinita, extensão por maçã, troca/remoção de armadura, luz10/11, root vehicle, expiração/remoção/atualização, morte/logout/dimensão, criativo/spectator, dois portadores simultâneos e voo concedido por outro mod. O retorno de `getCurativeItems()` é lista vazia na classe, mas a execução de uma política de cura específica não foi certificada a partir dessa assinatura isolada.

## Localizadores binários

Prefixo das classes: `com.github.alexmodguy.alexscaves`. Descritores são JVM; offsets pertencem ao método indicado no JAR exato.

| Classe / método | Descritor / offsets relevantes |
|---|---|
| `server.potion.DarknessIncarnateEffect.<init>` | `()V @0–19` |
| `DarknessIncarnateEffect.shouldTick` / `getActiveTime` | `(II)Z @0–41`; `()I @0–9` |
| `DarknessIncarnateEffect.tick` / `toggleFlight` | `(Lnet/minecraft/world/entity/LivingEntity;I)V @0–80`; `(Lnet/minecraft/world/entity/LivingEntity;Z)V @0–166` |
| `DarknessIncarnateEffect.onEffectStart` / `onEffectEnd` | `(Lnet/minecraft/world/entity/LivingEntity;I)V @0–10`; `(Lnet/minecraft/world/entity/LivingEntity;)V @0–16` |
| `DarknessIncarnateEffect.getIntensity` / `isInLight` | `(Lnet/minecraft/world/entity/LivingEntity;FF)F @0–78`; `(Lnet/minecraft/world/entity/LivingEntity;I)Z @0–55` |
| `server.item.DarkenedAppleItem.finishUsingItem` | `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)Lnet/minecraft/world/item/ItemStack; @0–99` |
| `server.item.DarknessArmorItem.onKeyPacket` | `(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/item/ItemStack;I)V @0–126` |
| `server.event.CommonEvents.livingTick` | `(Lnet/neoforged/neoforge/event/tick/EntityTickEvent$Pre;)V @68–125` |
| `CommonEvents.livingRemoveEffect` / `livingExpireEffect` | `(Lnet/neoforged/neoforge/event/entity/living/MobEffectEvent$Remove;)V @0–74`; `(Lnet/neoforged/neoforge/event/entity/living/MobEffectEvent$Expired;)V @0–44` |
| `mixin.LivingEntityMixin.ac_onEffectAdded` / `ac_onEffectUpdated` / `ac_onEffectRemoved` | `(Lnet/minecraft/world/effect/MobEffectInstance;Lnet/minecraft/world/entity/Entity;Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfo;)V @0–34`; `(Lnet/minecraft/world/effect/MobEffectInstance;ZLnet/minecraft/world/entity/Entity;Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfo;)V @0–47`; `(Lnet/minecraft/world/effect/MobEffectInstance;Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfo;)V @0–28` |
| `LivingEntityMixin.ac_livingTick` | `(Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfo;)V @0–32` |
| `server.config.ACServerConfig.<init>` | `(Lnet/neoforged/neoforge/common/ModConfigSpec$Builder;)V @689–745` |
| `client.render.entity.layer.ACPotionEffectLayer.render` | `(Lcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/MultiBufferSource;ILnet/minecraft/world/entity/Entity;FFFFFF)V @395–504` |
| `client.render.ACLightmapAdditions.ambientBonus` | `()F @0–104` |

Recursos selados: `data/alexscaves/recipe/darkened_apple.json` e `assets/alexscaves/lang/en_us.json`. A receita física do pack continua sujeita a overrides externos.
