# PayloadHandler — VFX cliente/protocolo 4.0.0

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`PayloadHandler.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/PayloadHandler.java) — `network/PayloadHandler.java`
- [`AddShaderEffectPacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/AddShaderEffectPacket.java) — `network/AddShaderEffectPacket.java`
- [`RemoveShaderEffectPacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/RemoveShaderEffectPacket.java) — `network/RemoveShaderEffectPacket.java`
- [`TriggerImpactFramePacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/TriggerImpactFramePacket.java) — `network/TriggerImpactFramePacket.java`
- [`TriggerChromaticAberrationPacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/TriggerChromaticAberrationPacket.java) — `network/TriggerChromaticAberrationPacket.java`
- [`TriggerRibbonPacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/TriggerRibbonPacket.java) — `network/TriggerRibbonPacket.java`
- [`TriggerRoarPacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/TriggerRoarPacket.java) — `network/TriggerRoarPacket.java`
- [`TriggerDomePacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/TriggerDomePacket.java) — `network/TriggerDomePacket.java`
- [`TriggerShakePacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/TriggerShakePacket.java) — `network/TriggerShakePacket.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

`PayloadHandler.register(RegisterPayloadHandlersEvent)` cria um `PayloadRegistrar` com `.versioned("4.0.0").optional()` e oito registros `playToClient`: AddShaderEffect, RemoveShaderEffect, TriggerImpactFrame, TriggerChromaticAberration, TriggerRibbon, TriggerRoar, TriggerDome e TriggerShake. Helpers do handler ligam/desligam shader pela instância cliente `Minecraft`. Não há C2S declarado nesse registrar.

## Scheduling e lifecycle cliente

[`events/AcesSpellUtilsClient.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsClient.java) é restrita a Dist.CLIENT. Em `ClientTickEvent.Post`, chama na ordem **ImpactFrameEffect → ChromaticAberrationEffect → RibbonManager → RoarEffect → DomeManager → ShakeManager**. Ribbon/dome/shake checam pausa nos managers; os três timelines impact/aberration/roar não checam pausa em seus próprios ticks. Não atribuir um único relógio congelado a todo VFX.

`RenderGuiEvent.Pre`, após a mão e antes do HUD, processa **impact frame → chromatic aberration → roar → dome warp**. Em AFTER_ENTITIES renderiza ribbon/dome e captura matrizes para roar/dome warp. `ViewportEvent.ComputeCameraAngles` soma shake ao pitch/yaw/roll com rates 3/5/4, usando a posição dos olhos e amplitude calculada por viewer. Essa ordem descreve composição visual, sem callbacks de hit.

No logout, limpa RibbonManager/DomeManager/ShakeManager e fecha DomeWarpEffect, além de hardStop das duas músicas de boss. O handler não limpa explicitamente as timelines impact/aberration/roar; elas têm expiry próprio. Add/remove shader usam `gameRenderer.loadEffect`/`shutdownEffect` apenas com LocalPlayer presente, sem ownership por cast ou duração no payload. O shutdown não identifica o dono do shader anterior. Os oito codecs e sua validação permanecem nas [fichas de payload](../payloads/INDEX.md); limites/custos locais de [impact/aberration](../vfx-runtime/impact-aberration-visual-dispatch.md), [roar](../vfx-runtime/roar-notification-routing.md), [ribbon](../vfx-runtime/ribbon-attachment-tracking.md), [trail](../vfx-runtime/trail-manager-tick-lifecycle.md) e [dome/shake](../vfx-runtime/dome-shake-coordination.md) não formam um budget global compartilhado.

## Targeting, geometria, custos e duração

Cliente receptor de efeitos visuais; nenhum payload desse conjunto concede servidor-autoridade de dano, acerto, mana ou cast. O alvo da apresentação vem do remetente/handler, não de um spell próprio do Ace.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

Um pacote visual não confirma execução autoritativa. Black Arcana não deve converter VFX em hit/progress/cast nem pressupor que o protocolo seja disponível em host/modpack sem negociação e QA real de shader/render.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. O `build.gradle` do source fixa a dependência Iron's `3.16.2`; o pack informa `3.16.3`. Não há comprovação de compilação/teste desse conjunto de versões.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**
