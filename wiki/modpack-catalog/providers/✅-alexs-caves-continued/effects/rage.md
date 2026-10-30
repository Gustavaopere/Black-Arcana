# Rage — dano conforme vida perdida e agressão de mobs

- Provider: **Alex's Caves Continued** (`alexscaves`), versão **1.0.10**.
- Registro: `alexscaves:rage`; `ACEffectRegistry.RAGE` → `RageEffect`.
- Autoridade: JAR publisher de 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- Contrato estático: `VERIFIED_EXACT_BINARY`; hook mutador: `NOT_VERIFIED`; QA física: `NOT_TESTED`.

## Identidade e descrição

Rage aumenta `ATTACK_DAMAGE` conforme a fração de vida perdida. Em mobs sem alvo, também pode escolher um alvo de ataque. É um efeito de status consumido pelo sistema de atributos e AI, sem projétil ou cast próprio. Não acrescenta uma nona raiz às oito ações mágicas do provider. O construtor `RageEffect.<init>()V @0–9` declara categoria `NEUTRAL` e cor `12201518` (`0xBA2E2E`). `ACEffectRegistry.<clinit>()V @54–68` registra `rage`; `lambda$static$2()Lnet/minecraft/world/effect/MobEffect; @0–7` constrói a classe.

## Comportamento, atributos e parâmetros

`RageEffect.tick(Lnet/minecraft/world/entity/LivingEntity;I)V @0–59` consulta `Attributes.ATTACK_DAMAGE`. Havendo a instância do atributo, remove o modifier anterior e adiciona um **modifier transitório `ADD_VALUE`** com identificador `alexscaves:effect.rage` e valor:

`bonus = (1F - health / maxHealth) * ((1 + amplifier) * 2.5F)`.

As contas são `float`, convertidas a `double` apenas ao criar o modifier. Com amplifier `0` e metade da vida, a solicitação é `+1.25` ao atributo; com vida cheia, é `0`. Isso não é multiplicador de todo dano nem garantia de dano final: arma, resolução de combate, armadura e outros modifiers continuam externos. O corpo não faz clamp da fração de vida, do amplifier ou do resultado. Se a entidade não possui `ATTACK_DAMAGE`, esse trecho é ignorado; a parte de AI ainda pode executar.

`shouldTick(II)Z @0–9` retorna `duration > 0`, ignorando o amplifier na cadência. A ponte nativa `ACMobEffect.shouldApplyEffectTickThisTick(II)Z @0–6` delega a esse método; `applyEffectTick(Lnet/minecraft/world/entity/LivingEntity;I)Z @0–7` chama `tick` e retorna `true`. Assim, o bônus pode acompanhar a saúde a cada tick elegível; não há timer próprio de Rage nem dano periódico chamado por esse efeito.

## Targeting da agressão

O ramo `tick @62–286` exige **servidor**, entidade `Mob`, `getTarget() == null`, `tickCount % 10 == 0` e `nextInt(2) == 0`. Usa a AABB do mob inflada **80 blocos em cada eixo**; esse valor descreve uma consulta em caixa, não alcance esférico nem distância de ataque.

Consulta `LivingEntity` com `EntitySelector.LIVING_ENTITY_STILL_ALIVE`. Exclui o próprio mob, aliados nos dois sentidos e candidatos recusados por `mob.canAttack`. O primeiro candidato elegível pode ser escolhido; substituições exigem que o novo candidato seja mais próximo **e** outro `nextInt(2) == 0`. Portanto, o resultado não é necessariamente o alvo mais próximo nem uma escolha uniforme. Não há chamada explícita de linha de visão neste loop; `canAttack` continua autoridade nativa.

Quando há candidato, chama `setLastHurtByMob` e `setTarget` (`@275–286`). O efeito não executa um ataque imediatamente. Partículas `ANGRY_VILLAGER` (`@289–368`) são apresentação desse ramo. O teste de limite do loop sorteia novamente `3 + nextInt(3)` em cada comparação; não o reinterpretar como um único sorteio prévio.

## Aplicação, aquisição e custos

O caminho nativo identificado é **Seething Stew**. `ACFoods.lambda$static$0()Lnet/minecraft/world/effect/MobEffectInstance; @0–24` cria Rage por **2200 ticks** (110 s a 20 TPS), usando o overload sem amplifier explícito. `ACFoods.<clinit>()V @105–133` define nutrição `6`, saturação `0.6F`, probabilidade de efeito `1F` e conversão em bowl. `ACFoodBuilder.resolve()Lnet/minecraft/world/food/FoodProperties; @61–110` resolve o supplier e transmite instância/probabilidade a `FoodProperties.Builder.effect`.

`ACItemRegistry.lambda$static$36()Lnet/minecraft/world/item/Item; @0–24` constrói `PrehistoricMixtureItem`, stack máximo `1`, com `ACFoods.SEETHING_STEW`. A receita exata `data/alexscaves/recipe/seething_stew.json` é shapeless: Cooked Dinosaur Chop + Flytrap + Heavy Bone + Bowl → um Seething Stew.

Além de comer, `PrehistoricMixtureItem.interactLivingEntity(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResult; @0–148` pode alimentar um `Mob` no servidor: exige `canFeedMob` e propriedades alimentares, cura pela nutrição e, se o callback específico `DinosaurEntity.onFeedMixture` não consumir o tratamento, aplica os efeitos retornados por `ACCompat.foodEffects`. A aplicação genérica não é garantida em toda espécie. `canFeedMob(Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/entity/Mob;)Z @75–97` recusa o caso normal em que o alvo atual do mob é o jogador alimentador. O caminho aceito consome um item fora do criativo e devolve/dropa bowl (`interactLivingEntity @216–260`). Não existe custo próprio de mana, alcance ou cooldown no corpo de `RageEffect`; custo e alvo pertencem ao emissor.

## Lifecycle, cleanup e integração por perks

`removeRageModifier(Lnet/minecraft/world/entity/LivingEntity;)V @0–30` consulta o mesmo `ATTACK_DAMAGE` e remove apenas `alexscaves:effect.rage`, se presente. `onEffectEnd(Lnet/minecraft/world/entity/LivingEntity;)V @0–5` chama essa rotina. A classe `LivingEntityMixin` fornece as pontes `ac_onEffectRemoved` e `ac_onEffectUpdated`: remoção chama `onEffectEnd`; atualização com o booleano de recálculo verdadeiro chama end/start (`@0–47`). O contrato é a presença desses corpos e da declaração do mixin no JAR, sem prova de execução física de todos os caminhos de remoção.

Perks futuras podem desejar alterar duração, amplifier, fórmula por vida perdida ou aquisição de alvo, mas essas são superfícies diferentes. Mutar apenas o amplifier afeta a fórmula do atributo, não a AABB `80`, o período `10` ou os filtros de AI. Uma perk não deve escrever outro modifier com a identidade reservada do provider nem reaplicar Rage para simular cada hit. O código examinado não demonstra adapter Black Arcana/RPG Skill Tree, autorização PvP, deduplicação entre mods ou hook mutador homologado.

## Validação e limites

Localizadores acima são métodos e offsets de `javap -p -c -s` do artefato SHA-exato. Classes, recursos e ficha são selados no [manifesto de efeitos](../EXACT-EFFECT-CONTRACTS-1.0.10.json); a [prova comum](../EXACT-EFFECT-CONTRACTS-1.0.10.md) registra reprodução e limites. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**, portanto não fornece os números certificados de 1.0.10. Testar no modpack: expiração/remoção/substituição do modifier, reload, vida alterada por outros mods, mobs com targets externos e PvP. Estes pontos são QA pendente, sem alegação de defeito reproduzido.
