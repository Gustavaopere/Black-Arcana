# Bubbled — bolha, respiração e movimento

**Provider:** Alex's Caves Continued (`alexscaves`), **versão física 1.0.10**. **ID:** `alexscaves:bubbled`; campo `ACEffectRegistry.BUBBLED`; implementação `server.potion.BubbledEffect`. Categoria `HARMFUL`, cor `0x21B5FF`. É um efeito aplicado a uma entidade, sem cast, projétil, raio ou custo próprios; não acrescenta uma nona raiz mágica às [oito ações](../actions/INDEX.md).

**Autoridade:** JAR publisher de 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A fonte pública `523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e não certifica os parâmetros desta ficha. Evidência `VERIFIED_EXACT_BINARY`; hook mutador `NOT_VERIFIED`; QA física `NOT_TESTED`. [Proveniência e reprodução](../EXACT-TECHNICAL-CONTRACTS-1.0.10.md).

## Identidade e execução

`ACEffectRegistry.<clinit>()V @88–102` registra `bubbled`; `lambda$static$4()Lnet/minecraft/world/effect/MobEffect; @0–7` constrói `BubbledEffect`. O construtor `()V @0–9` fixa categoria e cor, sem adicionar modificadores de atributos. `shouldTick(II)Z @0–1` retorna `true`; não usa duração nem amplifier. A ponte `ACMobEffect.shouldApplyEffectTickThisTick(II)Z @0–6` delega a esse método, e `applyEffectTick(Lnet/minecraft/world/entity/LivingEntity;I)Z @0–7` chama `tick` e retorna `true`. A elegibilidade e expiração da instância continuam no ciclo de efeitos do Minecraft.

O corpo relevante é `BubbledEffect.tick(Lnet/minecraft/world/entity/LivingEntity;I)V`. O segundo argumento não é lido: subir amplifier não multiplica automaticamente dano, arrasto, ar ou gravidade. O método não contém um gate próprio de lado servidor; a chamada normal pelo ciclo de efeitos e a sincronização do mod precisam ser preservadas. Invocá-lo manualmente pode duplicar processamento.

## Parâmetros, targeting e dano

| Caminho exato | Consequência no bytecode 1.0.10 |
|---|---|
| `canBreatheUnderwater() \|\| ACCompat.isAquatic(entity)` (`tick @0–11`) | Seleciona o ramo aquático; `ACCompat.isAquatic(Lnet/minecraft/world/entity/LivingEntity;)Z @0–13` consulta o tag vanilla `EntityTypeTags.AQUATIC` |
| Aquático e **fora** de `RESISTS_BUBBLED` (`@14–27`) | Repõe ar a `getMaxAirSupply()`; fora do chão soma `(0,-0.08D,0)` à velocidade (`@30–58`) |
| Aquático dentro de `RESISTS_BUBBLED` | Sai desse processamento; não cai no ramo de sufocamento |
| Não aquático, sem `MobEffectUtil.hasWaterBreathing`, e sem `Player.abilities.invulnerable` (`@64–90`) | Multiplica velocidade por `(0.800000011920929D,1D,0.800000011920929D)`, representando `0.8F` ampliado, e escreve `max(ar-2,-20)` (`@93–123`) |
| Ar resultante `<= -20` (`@126–132`) | Reseta ar a `0`, solicita oito partículas de bolha e `hurt(damageSources().drown(),2F)` (`@135–280`); resultado de `hurt` é descartado |

O valor `2F` é dano **solicitado**, com fonte vanilla de afogamento; não é dano líquido garantido nem escola elemental do RPG. O tag `resists_bubbled` participa do **ramo aquático**, não é uma proibição geral de receber a instância. O JSON exato `data/alexscaves/tags/entity_type/resists_bubbled.json` contém somente `alexscaves:deep_one_mage`; datapacks podem ampliar o conjunto. Imunidade aquática não remove necessariamente o efeito visual.

O efeito não seleciona aliados ou inimigos. Quem aplica a instância decide o alvo; este método recebe uma `LivingEntity` e usa os gates acima. Não contém busca em área, limite de distância ou teste de PvP. Uma perk que altere duração deve preservar a filtragem da origem; uma que altere dano/arrasto exigiria intervenção comprovada no consumidor, pois amplifier é ignorado neste corpo.

## Consumidores, aplicação e duração

`WaterBoltEntity.damageMobs()V @32–58` busca `LivingEntity` na AABB própria inflada `2D` em cada eixo. Exclui aliados, `DeepOneBaseEntity`, owner e aliados do owner (`@90–126`). Somente quando `ACCompat.hurt(...,3F)` retorna `true` **e** `isBubbling()` é verdadeiro, aplica `new MobEffectInstance(BUBBLED,200)` (`@133–181`): 200 ticks nominais, amplifier padrão do construtor sem parâmetro de nível. A criação do bolt com Enveloping Bubble pertence à [ficha Sea Staff](../actions/sea-staff-water-bolt.md); não reaplicar o debuff a partir de um evento de dano genérico.

`DeepOneMageEntity.tick()V @0–108` é outra origem: fora de água/bolha, sem o efeito, adiciona uma instância de **200 ticks** a si próprio; estando em água/bolha, remove-a. O próprio mage aparece no tag de resistência. Isso demonstra que **ter o efeito** e **sofrer sua física** são condições diferentes. O trecho não possui um gate adicional de servidor; não inferir a execução efetiva em cada lado sem QA.

`CommonEvents.livingTick(Lnet/neoforged/neoforge/event/tick/EntityTickEvent$Pre;)V @0–67` remove Bubbled quando `ACFluids.isInAnyFluid(entity)` é verdadeiro. Esse helper retorna `maxFluidHeight(entity)>0D`; não limita a água. A leitura percorre a AABB deflacionada em `0.001D` e estados de fluidos em chunks já disponíveis (`ACFluids.fluidHeight(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/tags/TagKey;Lnet/minecraft/tags/TagKey;)D @0–318`). Duração nominal não assegura permanência por 200 ticks.

`LivingEntityMixin.ac_increaseAirSupply(ILorg/spongepowered/asm/mixin/injection/callback/CallbackInfoReturnable;)V @0–29` substitui o retorno pelo argumento original quando Bubbled está presente: bloqueia esse caminho de recuperação de ar. `EntityMixin.ac_isInWater(Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfoReturnable;)V @0–80` retorna `true` para portador aquático, com mapa de efeitos disponível, fora do tag de resistência. É um retorno sintético de `isInWater`, não a criação de fluido no mundo.

## Cliente, rede, custos e cleanup

`UpdateEffectVisualityEntityMessage.handle(Lcom/github/alexmodguy/alexscaves/server/message/UpdateEffectVisualityEntityMessage;Lcom/github/alexmodguy/alexscaves/server/message/ACNetworkContext;)V` resolve os IDs no mundo do jogador, exige entidade afetada viva no sentido de **tipo `LivingEntity`** e origem existente, e distância origem–destino `<32F` (`@30–87`); não chama `isAlive` nesse gate. `potionType=1` escolhe Bubbled e toca o som (`@152–180`); depois remove via `removeEffectNoUpdate` ou adiciona instância com duração do pacote (`@231–280`). O produtor Water Bolt envia duração `200` a todos no ramo servidor (`damageMobs @184–213`). O nome “Visuality” não torna a mensagem apenas partículas: seu handler manipula instâncias. Direção/protocolo e autorização integral da rede continuam em escopo próprio, sem certificar este handler como hook seguro.

`CameraMixin.ac_getFluidInCamera(Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfoReturnable;)V @0–64` devolve `FogType.WATER` com câmera inicializada, jogador local com efeito e primeira pessoa. `GameRendererMixin.ac_renderLevelAfterHand(Lnet/minecraft/client/DeltaTracker;Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfo;Lcom/mojang/blaze3d/vertex/PoseStack;)V @0–80` chama a camada de bolha para a entidade câmera em primeira pessoa; `ACPotionEffectLayer.render(...)V @178–205` exige efeito e `isAlive` para o desenho externo. Esses consumidores não demonstram dano, colisão ou tamanho físico da bolha.

Não há cobrança de mana, cooldown, item ou durabilidade no tick do efeito. Custos e obtenção vêm da origem, como Sea Staff, enquanto o mage aplica a si mesmo. A classe declara `getCurativeItems()Ljava/util/List; @0–3` retornando lista vazia, mas esta assinatura isolada **não prova** que o caminho de cura/leite do NeoForge 1.21.1 a consome; não prometer imunidade a leite. A remoção explícita por fluido e pelo mage está comprovada; expiry, morte, reload, efeitos externos e compatibilidade precisam de QA. Não há estado próprio salvo ou restaurado neste override nem cleanup de velocidade que reverta o arrasto acumulado.

## Integração e validação

Contrato estático documentado: identidade, ramo aquático, ar, fonte de dano, aplicação, consumidores de movimento/cliente e remoção. Qualquer perk deve atuar uma vez no caminho homologado do provider, respeitar o custo da origem e distinguir duração da instância de dano periódico. Não foi validado adapter Black Arcana/Enshrouded/RPG Skill Tree para alterar estes valores.

QA pendente: alvos aquáticos e não aquáticos, tags alterados por datapack, Water Breathing, invulnerabilidade, recuperação de ar, qualquer fluido, dano negado, aplicação repetida, cliente/servidor, PvP, multiplayer e reload. A [prova técnica dos efeitos](../EXACT-EFFECT-CONTRACTS-1.0.10.md) sela classes, recursos e offsets; a aprovação do auditor confirma bytes e localizadores, sem executar o modpack. **`STATIC_TECHNICAL_CATALOG_ONLY`; `NOT_VERIFIED` para hooks; `NOT_TESTED` para QA física.**
