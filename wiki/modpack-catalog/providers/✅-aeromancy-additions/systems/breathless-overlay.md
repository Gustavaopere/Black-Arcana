# HUD — overlay de Breathless

**Contrato:** suporte de Aeromancy Additions `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. Não é nova identidade de magia. `hooks=NOT_VERIFIED`; `physical_runtime=NOT_TESTED`; **0 certificações / +0 magias / +0 adapters aprovados**. O JAR oficial de publicação foi adquirido separadamente; isso não comprova paridade com o JAR instalado historicamente (SHA-1 histórico de 35 caracteres inválido). [Proveniência e limites](../SOURCE-CONTRACTS-1.2.8.md).

## Registro e efeito visual

`AAOverlay.instance` implementa `LayeredDraw.Layer` e é registrado como `aero_additions:screen_effects` acima de todas as camadas GUI por `AAClientEvents.registerLayers`. A camada de contador Airstep fica acima deste overlay.

Cada chamada de `render` acumula o campo estático `ticks += deltaTracker.getGameTimeDeltaTicks()` **antes** dos gates de GUI/player. Retorna com GUI oculta, player espectador ou player nulo. Havendo `player.hasEffect(AASpells.MobEffects.BREATHLESS)`, chama `renderOverlay` com textura `textures/entity/wind_shield_layer.png`, cor `(0.35,0.35,0.35)` e alpha `0.1`. O gatilho é o MobEffect do player, sem consulta a `AeromancySpellData.ASPHYXIATING` ou ao cache.

A renderização cobre largura/altura da tela, usa offset de textura `(80*ticks,ticks)` e dimensões de textura `(2*screenWidth,2*screenHeight)`. Desativa depth test/escrita de profundidade, usa blending aditivo `ONE/ONE`, aplica cor e depois restaura cor branca, blend padrão e profundidade. Não tem operação de dano, efeito de status ou desserialização.

| Eixo | Contrato para perks |
|---|---|
| Dano | N/A: dano pertence a [Breathless](../effects/breathless.md), não ao overlay. |
| Alcance | N/A de gameplay: cobre a tela local. |
| Alvo | Player local com MobEffect BREATHLESS. |
| Tempo | Offset animado por delta de ticks de render; gate depende da presença do MobEffect. Nenhum decremento de duração aqui. |
| Custo | N/A: sem cast/mana/cooldown. |

Não usar render como callback de progressão/perk. Nenhum controle de intensidade por atributo é visível. [Integração cliente](client-events.md) · [lifetime](state-lifecycle-network-ui.md). Render e interação com outras camadas do modpack permanecem `NOT_TESTED`.


**Fonte imutável:** [AAOverlay.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAOverlay.java#L19-L55) · [Registro](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAClientEvents.java#L77-L80) · [MobEffect separado](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/asphyxiate/BreathlessEffect.java#L13-L38).
