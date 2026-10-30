# Magnetizing — magnetização

- Provider: **Alex's Caves Continued** (`alexscaves`), versão instalada **1.0.10**.
- Identidade: `alexscaves:magnetizing`, campo `ACEffectRegistry.MAGNETIZING`, classe `server.potion.MagnetizedEffect`.
- Autoridade: JAR publisher File **8856293**, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- Contrato estático: **`VERIFIED_EXACT_BINARY`**; hook mutador **`NOT_VERIFIED`**; configuração efetiva **`NOT_VERIFIED`**; QA física **`NOT_TESTED`**.

## 1. Identidade e unidade catalogada

É um status de suscetibilidade magnética, não um projétil nem uma nova raiz de lançamento. `ACEffectRegistry.<clinit>()V @22–35` registra `magnetizing`; `lambda$static$0()Lnet/minecraft/world/effect/MobEffect;` instancia `MagnetizedEffect`. Seu construtor `()V @1–6` usa categoria `NEUTRAL` e cor decimal `5461356` (`0x53556C`). A fonte pública pinada `523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**; somente o JAR acima sustenta os números desta ficha.

## 2. Lifecycle e separação entre status e movimento

`MagnetizedEffect.shouldTick(II)Z @0–9` testa exclusivamente **duração >0**; não escala frequência nem força com amplifier. `ACMobEffect.shouldApplyEffectTickThisTick(II)Z` delega os dois inteiros sem transformá-los, e `applyEffectTick(Lnet/minecraft/world/entity/LivingEntity;I)Z` chama `tick` e retorna `true`.

`tick(Lnet/minecraft/world/entity/LivingEntity;I)V @0–56` faz apenas sincronização: servidor, `entity.tickCount%20==0`, instância presente; envia `UpdateEffectVisualityEntityMessage(id,id,2,duration)`. `onEffectStart(Lnet/minecraft/world/entity/LivingEntity;I)V @0–46` envia a mesma mensagem no servidor quando encontra a instância. O amplifier recebido não é lido nesses corpos. O efeito não registra atributo de velocidade, força, dano ou raio.

O movimento é outro consumidor. `EntityMixin.ac_tick(Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfo;)V @72–80` chama `MagnetUtil.isPulledByMagnets` e, se verdadeiro, `tickMagnetism`. Quando a entidade deixa de satisfazer esse predicado, o ramo `@103–121` restaura a face magnética `DOWN` e atualiza dimensões se necessário. A presença do mixin e de seus corpos é evidência estática; não comprova aplicação efetiva de todas as injeções no modpack.

## 3. Targeting, materiais e limites

`MagnetUtil.isDynamicallyMagnetic(Lnet/minecraft/world/entity/LivingEntity;Z)Z @0–87` aceita imediatamente qualquer entidade viva com Magnetizing. Sem o efeito, o argumento `legsOnly=true` consulta **FEET**, enquanto `false` percorre todos os slots e procura `ACTagRegistry.MAGNETIC_ITEMS`. O nome `legsOnly` não significa slot LEGS.

`isPulledByMagnets(Lnet/minecraft/world/entity/Entity;)Z` tem ramos para ItemEntity com item magnético, LivingEntity dinamicamente magnética que não seja jogador espectador, FallingBlockEntity com bloco magnético, e fallback do tipo no tag `MAGNETIC_ENTITIES`. Não chamar isso de exclusão global de espectadores: o fallback de tipo ainda existe. `attachesToMagnets(Lnet/minecraft/world/entity/Entity;)Z @0–42` usa entidade viva dinamicamente magnética com `legsOnly=true` e **não agachada**, ou fallback por tag de tipo; não possui seu próprio teste de espectador.

As constantes `MAGNETIC_ITEMS/BLOCKS/ENTITIES` correspondem aos tags físicos `ferromagnetic_items`, `ferromagnetic_blocks`, `ferromagnetic_entities`. O tag `magnetic_attachables` contém os três blocos scarlet neodymium: node, pillar e block. São dados extensíveis por datapack. Magnetizing remove a necessidade de equipamento magnético para o ramo vivo, mas não produz sozinho um campo de força em volta do portador.

Seis entidades rejeitam diretamente o efeito em `canBeAffected(Lnet/minecraft/world/effect/MobEffectInstance;)Z @0–31`: **Boundroid, Boundroid Winch, Ferrouslime, Magnetron, Notor e Teletor**. Cada uma exige aceitação pelo super e efeito diferente de Magnetizing. Isso não impede que outro ramo de magnetismo as trate por tipo/material.

## 4. Parâmetros reais do consumidor magnético

`MagnetUtil.tickMagnetism(Lnet/minecraft/world/entity/Entity;)V` encontra POIs atratores e repulsores apenas em `ServerLevel`, passando distância de busca **5** (`@0–76`). Os helpers `getNearbyAttractingMagnets` / `getNearbyRepellingMagnets` chamam `PoiManager.findAll` com ocupação `ANY`; a distância passada a esse sistema não equivale a alcance universal de uma poção.

Para cada POI, `lambda$tickMagnetism$2/$3(Lnet/minecraft/world/entity/Entity;ILnet/minecraft/core/BlockPos;)V @0–92` calcula `r=clamp(distanceToCenter/5,0,1)` e `impulse=direction*(1-r)*0.25D`. O vetor de direção é mantido se seu comprimento `<1D`, senão normalizado. A direção aponta para o centro no atrator e para fora no repulsor; o acumulador torna-se `oldDelta*0.9D+impulse`. São passos por POI, com composição sequencial; não uma força única por nível de efeito. `tickMagnetism @77–81` captura o delta após os POIs e `@544–552` grava esse vetor escalado por aproximadamente `0.08D`.

A caminhada usa `COMMON_CONFIG.walkingOnMagnets && attachesToMagnets(entity)` (`@92–122`). O default compilado é **true**, chave `walking_on_magnets` (`ACServerConfig.<init> @419–436`); valor efetivo do servidor não foi lido. Desativar essa chave condiciona a aderência, sem apagar todos os caminhos de atração/repulsão.

`calculateClosestDirection(Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/core/Direction; @0–165` retorna DOWN ao agachar; caso contrário amostra as seis direções, com expansão `0.50001F`, usa distância inicial `height+width` e seleciona blocos do tag `MAGNETIC_ATTACHABLES`, dando prioridade ao teto. Esses números descrevem teste de superfície, não raio de dano.

Na aderência, `processMovementControls(FLnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/core/Direction;)Lnet/minecraft/world/phys/Vec3;` consulta **`Attributes.MOVEMENT_SPEED`** e entradas `xxa/zza`: nas paredes, o componente lateral usa o atributo escalado por aproximadamente `0.6D` e o vertical usa entrada frontal vezes o atributo. O componente normal usa `0.75F` quando pulando sobre superfície magnética, senão `-0.1F`; no teto, o método usa velocidade existente e fator horizontal `0.98D`. Portanto uma perk de velocidade pode interferir no consumidor de parede, mas isso não demonstra um adapter homologado nem que todos os modos escalem igualmente.

`tickMagnetism` também trata salto, supressão de queda quando aderido, pose/dimensões, metal móvel e amortecimento. O amplifier do efeito não participa dessas fórmulas. Duração maior preserva elegibilidade por mais tempo; aumentar amplifier não aumenta automaticamente alcance ou força.

## 5. Duração, custos e aquisição

`ACEffectRegistry.lambda$static$8()Lnet/minecraft/world/item/alchemy/Potion; @16–33` cria a poção **magnetizing** com **3.600 ticks** e amplifier 0. `lambda$static$9` cria **long_magnetizing** com **9.600 ticks**, também amplifier 0. A duração reside na instância da poção; splash/lingering e efeitos reaplicados podem ter liquidação própria.

`registerBrewing(Ljava/util/function/Consumer;)V @0–82` entrega receitas de **Awkward + Ferrouslime Ball → Magnetizing** e **Magnetizing + Redstone → Long Magnetizing** por `ProperBrewingRecipe`. Essas relações de registro não demonstram obtenção legítima dos ingredientes nem brew físico no pack. O próprio status não solicita mana, fome, durabilidade ou cooldown; os custos da poção e de outras aplicações pertencem ao produtor. Não há dano ou tipo de dano próprio para remapear a uma escola de magia.

## 6. Rede, encerramento e integração por perks

O pacote visual usa tipo **2** para selecionar Magnetizing. `UpdateEffectVisualityEntityMessage.handle(...;Lcom/github/alexmodguy/alexscaves/server/message/ACNetworkContext;)V` resolve alvo/origem no mundo do player escolhido, exige alvo do tipo `LivingEntity` (sem teste `isAlive` nesse gate), origem existente e distância entre ambos `<32F`; no ramo tipo 2, escolhe o efeito e usa amplifier padrão 0. O envio periódico do efeito usa `id,id`, de modo que essa distância não restringe seu alcance de aplicação. A classe de mensagem não substitui a prova de direção/autorização do registro de rede; não expor esse handler como API segura de perks.

`MagnetizedEffect` não sobrescreve `onEffectEnd`; o default de `ACMobEffect` é vazio. Ao expirar, a entidade pode continuar magnética por equipamento ou tag, portanto o cleanup não é simplesmente “remover status zera movimento”. A restauração de face observada em `EntityMixin` depende de deixar de satisfazer `isPulledByMagnets`. Não há garantia derivada desses corpos de zerar todos os componentes cinéticos, restaurar câmera em todos os casos ou sincronizar imediatamente cada cliente.

Os pontos candidatos são duração da aplicação, materiais/tipos elegíveis, POIs, config global e consumidor de movimento. Uma perk por jogador deve preservar a autoridade do provider, não alterar globalmente o tag ou config para simular uma propriedade individual, e não aplicar o impulso uma segunda vez. Black Arcana e RPG Skill Tree não possuem hook mutador homologado nesta ficha.

## 7. Evidência e validação pendente

A [auditoria reproduzível](../EXACT-EFFECT-CONTRACTS-1.0.10.md) sela a ficha, classes, recursos, descritores e instruções do JAR exato. Ações mágicas, poções, suscetibilidade, deslocamento e VFX são unidades diferentes; o recorte desta ficha não encerra a tecnologia magnética completa do provider.

QA física necessária: poção normal/longa, amplifier alto, ausência/presença de boots, agachamento, espectador e fallback por tags, múltiplos POIs, config desligada, paredes/teto, velocidade do RPG, expiração durante aderência, unload/reload e multiplayer. Nenhum resultado de gameplay ou hook foi declarado validado.
