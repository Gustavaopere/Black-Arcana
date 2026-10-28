# RoarHandler — roteamento por tracking ou posição — Ace's Spell Utils 1.2.7.2

**Tipo:** superfície de manutenção/routing de VFX do provider · **Estado:** ⚠️ contrato source-pinned, QA física fail-closed.

## Arquivos exatos e responsabilidades

- [`utils/RoarHandler.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/RoarHandler.java)
- [`network/TriggerRoarPacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/TriggerRoarPacket.java)
- [`vfx/roar/RoarConfig.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/vfx/roar/RoarConfig.java), [`RoarStyle.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/vfx/roar/RoarStyle.java) e [`RoarTimeline.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/vfx/roar/RoarTimeline.java)
- [`client/roar/RoarEffect.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/client/roar/RoarEffect.java)

**Fluxo source:** `RoarHandler.trigger(Entity,RoarConfig)` só envia para entidades válidas no servidor via `sendToPlayersTrackingEntityAndSelf`. `trigger(ServerLevel,Vec3,RoarConfig)` envia próximo à posição `RANGE=128.0` blocos via `sendToPlayersNear`. Overload de `Collection<ServerPlayer>` envia individualmente `TriggerRoarPacket` com ID da entidade.

**Targeting/range/tempo/consumo:** Entidade ou ponto fixo do efeito visual, e conjunto de espectadores conforme rota; `RANGE` é distribuição de payload, não target/AoE real de magia.

**Risco e dependências:** Roar remoto é apresentação do cliente. `entityId<0` no packet significa posição fixa, e `RoarConfig.radius` é geometria visual; não duplicar cast ou procurar impacto usando ID de roar.

## Unidades, clamps e lifetime da apresentação

`RoarConfig` declara **radius/thickness em UV com correção de aspecto**, onde centro→borda vertical vale 0.5, não em blocos. Limites (fallback para não finito): strength **0..1 (0.4)**, sharpness **0..8 (1)**, radius **0..2 (1)**, thickness **0.01..1 (0.15)**, blur/refraction **0..0.5 (0)**; duração **1..1200 ticks**. Style null→ZOOM e growth null→LINEAR. `zoom` zera radius/blur/refraction; `ring` zera strength e fixa sharpness=1. `of(strength,duration)` usa zoom/sharpness 1/EASE_OUT_QUAD. `RoarStyle` tem ZOOM e RING; ordinal desconhecido→ZOOM, e a ordem atravessa rede/shader.

`RoarTimeline.start` substitui o roar anterior, sem lista por fonte. Radius cresce por `config.radius()*growth.ease(progress)`; intensidade tem attack nos primeiros **10%**, hold até **66%** e fade linear no restante. Expira quando elapsedTicks≥duration. `RoarEffect` acompanha a entidade por ID e usa posição interpolada + metade da altura; fonte ausente só impede render daquele frame, sem retry de spawn nem extensão do timer. A versão posicional conserva Vec3 fixo. Câmera a menos de **1.5 bloco** da origem fixa o centro em 0.5/0.5; fonte atrás da câmera é descartada e centro projetado é limitado a −1..2.

O PostChain é `aces_spell_utils:shaders/roar.json`, redimensionado com a janela e fechado ao fim da timeline. Falha de carga marca `failed=true`, sem reset/retry explícito na classe. Origem offscreen, carga tardia, pause/logout/dimensão e roars concorrentes exigem QA; não confundir substituição visual com cancelamento de cast do servidor.

## Interoperabilidade e QA

Esse sistema faz apresentação e manutenção do provider. Não cria `AbstractSpell` nem prova hit, gasto de mana, proc, ganho de Mastery ou atualização do mundo. Black Arcana permanece authority para seu próprio casting/hazards/domains/rituais/WorldEffectPolicy/Strain/Corruption/Arcane Danger; RPG Skill Tree só progressão com gates reais. Não implementar segundo handler de estado a partir de evento puramente visual.

Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, versão source `1.2.7.2-1.21.1`; arquivo físico catalogado `aces_spell_utils-1.2.7.2-1.21.1.jar` SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` sem verificação de classfile. Build source depende Iron's `3.16.2`; modpack declara `3.16.3`. **QA:** JAR e event handlers reais, client/dedicated server, tracking/clear/teleport, cenários multicaster, packet sequencing e budgets gráficos; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `COMPLETE_PERK_READY=false`.
