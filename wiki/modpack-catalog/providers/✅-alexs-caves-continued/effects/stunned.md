# Stunned — controle de movimento, AI e dano direto

- Provider: **Alex's Caves Continued** (`alexscaves`), versão **1.0.10**.
- Registro: `alexscaves:stunned`; `ACEffectRegistry.STUNNED` → `StunnedEffect`.
- Autoridade: JAR publisher de 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- Contrato estático: `VERIFIED_EXACT_BINARY`; hook mutador: `NOT_VERIFIED`; QA física: `NOT_TESTED`.

## Identidade e descrição

Stunned é um efeito nocivo de controle. Combina modifier de velocidade, redução do movimento vertical ascendente e suspensão de flags de goals de mobs; um evento separado cancela certos danos produzidos por entidades atordoadas. Não representa um cast autônomo e não acrescenta raiz às oito ações mágicas do provider. `ACEffectRegistry.<clinit>()V @38–51` registra `stunned`; `lambda$static$1()Lnet/minecraft/world/effect/MobEffect; @0–7` constrói `StunnedEffect`.

## Atributos, tick e limites reais

| Contrato exato | Localizador em `StunnedEffect` |
|---|---|
| Categoria `HARMFUL`, cor `16776133` (`0xFFFBC5`) | `<init>()V @0–6` |
| Modifier `Attributes.MOVEMENT_SPEED`, identidade `alexscaves:effect.stunned`, valor `-1D`, operação `ADD_MULTIPLIED_BASE` | `<init>()V @9–29` |
| Se `deltaMovement.y > 0`, escreve `deltaMovement * (1D, 0.1D, 1D)` | `tick(Lnet/minecraft/world/entity/LivingEntity;I)V @0–25` |
| Para `Mob`, fixa pitch atual/anterior em `30F` | `tick @103–124` |
| No servidor, desabilita flags `MOVE`, `JUMP`, `LOOK` no `goalSelector` | `tick @127–167` |
| Tick elegível quando `duration > 0`; amplifier ignorado nesse teste e no corpo próprio de tick | `shouldTick(II)Z @0–9` |

O modifier não é um `setSpeed(0)`: ele participa do sistema vanilla de atributos. A definição base é `-1D`; escala por amplifier, combinação com outros modifiers e limites finais são autoridade de `MobEffect`/atributos do Minecraft. O corpo não zera o movimento horizontal, não reduz a queda e não prova bloqueio de toda locomoção, teleporte ou skill externa. A ponte `ACMobEffect.applyEffectTick(Lnet/minecraft/world/entity/LivingEntity;I)Z @0–7` chama `tick`; `shouldApplyEffectTickThisTick(II)Z @0–6` delega `shouldTick`.

Partículas: por tick, solicita `STUN_STAR` se `nextFloat() < width * 0.12F`; envia ID da entidade como argumento de partícula (`tick @28–100`). Isso é apresentação, sem dano. `ClientEvents.computeCameraAngles(Lnet/neoforged/neoforge/client/event/ViewportEvent$ComputeCameraAngles;)V @644–704` aplica ao jogador sob o efeito roll `sin((tickCount + partialTick) * 0.2F) * 10D`; não muda targeting do servidor.

## Consumidor de dano e consumidores de mobs

`CommonEvents.acLivingAttack(Lnet/neoforged/neoforge/event/entity/living/LivingIncomingDamageEvent;)Z @158–211` retorna verdadeiro se o `DamageSource.getDirectEntity()` é uma `LivingEntity` com Stunned. `livingAttack(...LivingIncomingDamageEvent;)V @0–10` usa o retorno para `setCanceled(true)`. O teste é sobre a **entidade direta da fonte**, não genericamente o dono: um projétil de um atirador atordoado não satisfaz esse ramo apenas por seu owner estar atordoado. O handler possui também outros ramos, que não são parte de Stunned. O efeito em si não chama `hurt`.

`TremorsaurusEntity.wantsToAttack(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z @0–48` rejeita o Tremorsaurus candidato que já possui tentativas de domesticação ou Stunned. `onFeedMixture(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/player/Player;)Z @0–160` reconhece Serene Salad + Stunned, remove o efeito e transmite a remoção visual. No servidor incrementa tentativas: sorteio `nextInt(2)==0` quando tentativas `>3`, ou sucesso garantido quando `>8`, chama `tame(player)`. Logo, ampliar o efeito pode mudar uma janela de domesticação, além de combate.

`TremorzillaEntity.isStunned()Z @0–18` consulta o registro. Em `tick()V @2198–2206`, esse teste pula `tickBeamTargeting`; em `@2344–2355` impede iniciar `ANIMATION_PREPARE_BREATH` naquele ramo. Não há prova aqui de que o efeito cancele toda instância de beam já existente ou toda AI do Tremorzilla.

## Aplicação, targeting, custo e aquisição

**Primitive Club:** `hurtEnemy(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z @0–7` chama `acHurtEnemy` com o mesmo descritor. Este solicita `1` de durabilidade na mainhand (`@0–6`), depois, apenas no servidor, sorteia `nextFloat() < 0.8F` e tenta Stunned no alvo principal por **`150 + nextInt(150)` ticks** (`150–299`), amplifier `0`, ambient/partículas `false` (`@32–95`). A aceitação de `addEffect` governa a etapa seguinte; uma tentativa não garante aplicação.

Com aplicação principal aceita e **Dazing Sweep** positivo, `f = level + 1.2F` e `AABB.ofSize(target.position(), f, f, f)` (`@135–173`). `f` é comprimento de cada lado da caixa, não seu raio; o JSON exato define nível máximo `2` e slot mainhand. Consulta entidades diferentes do atacante com predicado `canBeHitByProjectile`. O loop exclui alvo principal e entidades aliadas ao atacante, exige `distanceTo(principal) <= f` e `LivingEntity` (`@175–262`); não adiciona teste explícito de linha de visão nem aliança no sentido inverso. Solicita `1F` de dano `mobAttack(attacker)`, ignora o booleano de `hurt` e tenta Stunned por **`80 + nextInt(80)` ticks** (`80–159`), amplifier `0`, mesmo quando esse dano não foi aceito (`@264–330`). Não transportar essa área para o efeito genérico ou atribuir dano periódico a Stunned.

A receita `data/alexscaves/recipe/primitive_club.json` usa Heavy Bone + duas Cycad. `data/alexscaves/enchantment/dazing_sweep.json` define máximo `2`, peso `2`, custo de bigorna `4`, min cost `1 + 10*(level-1)`, max cost `41 + 10*(level-1)`; `supported_items` referencia o tag de Primitive Club. São valores estáticos de aquisição/tuning, sem valor efetivo do modpack inferido.

**Stinky Fish:** `ACFoods.lambda$static$6()Lnet/minecraft/world/effect/MobEffectInstance; @0–23` cria Stunned por **100 ticks** via overload sem amplifier explícito; `<clinit>()V @449–473` define nutrição `1`, saturação `0.1F`, probabilidade `1F`. `ACItemRegistry.lambda$static$118()Lnet/minecraft/world/item/Item; @0–26` associa essas propriedades a um item de raridade `RARE`. O helper `ACFoodBuilder.resolve()Lnet/minecraft/world/food/FoodProperties; @61–110` transmite instância/probabilidade a `FoodProperties.Builder.effect`. Não há custo de mana, cooldown, alcance ou área próprios em `StunnedEffect`; cada emissor define essas condições.

## Remoção, sincronização e integração

Serene Salad remove Stunned em `PrehistoricMixtureItem.finishUsingItem(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)Lnet/minecraft/world/item/ItemStack; @0–30`. Ao alimentar mob elegível no servidor, `interactLivingEntity(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResult; @118–148` também remove, salvo o callback específico de dinossauro que trata seu próprio caminho. `canFeedMob(...Player;...Mob;)Z @0–41` permite especificamente Serene Salad num Tremorsaurus atordoado. Alimentação aceita consome um item fora do criativo e devolve/dropa bowl (`interactLivingEntity @216–260`). Receita de salad: Fiddlehead + Tree Star + Pine Nuts + Bowl.

`UpdateEffectVisualityEntityMessage.handle(Lcom/github/alexmodguy/alexscaves/server/message/UpdateEffectVisualityEntityMessage;Lcom/github/alexmodguy/alexscaves/server/message/ACNetworkContext;)V @35–87` resolve alvo e entidade de origem e exige distância entre eles `<32F`. Tipo `3` seleciona Stunned (`@199–212`); o ramo remove usa `removeEffectNoUpdate`, enquanto o outro cria instância com duração recebida/amplifier `0` (`@231–280`). Esta mensagem acompanha aplicação visual; sua existência não homologa API para perks nem prova autenticação de um novo emissor externo.

`StunnedEffect` não implementa cleanup próprio de flags; herda `ACMobEffect.onEffectEnd(...LivingEntity;)V`, cujo corpo é vazio. A remoção normal do modifier de atributo pertence ao lifecycle vanilla, e restauração efetiva de controle/AI deve ser testada no pack. Não declarar o mob preso após expiração a partir dessa ausência de override.

Uma perk pode desejar mudar duração, probabilidade do Club, amplifier, geometria do sweep ou filtro de dano; são consumidores distintos. Aumentar amplifier não muda os literais `0.8`, `150`, `80`, `f` ou a comparação de entidade direta no evento. Nenhum hook mutador Black Arcana/RPG foi homologado; evitar repetir dano/aplicação após o settlement do provider.

## Validação e limites

Os descritores e offsets vêm de `javap -p -c -s` do JAR SHA-exato. Ficha, classes e JSONs de suporte são selados no [manifesto de efeitos](../EXACT-EFFECT-CONTRACTS-1.0.10.json); a [prova comum](../EXACT-EFFECT-CONTRACTS-1.0.10.md) registra reprodução e limites. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e não fornece números certificados de 1.0.10. QA pendente: expiração/remoção das flags, interação com skills de movimento e outros modifiers, multiplayer, fontes indiretas de dano e domesticação. Nenhum comportamento físico ou defeito reproduzido é afirmado.
