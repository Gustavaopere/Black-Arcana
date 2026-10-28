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

## Targeting, geometria, custos e duração

Cliente receptor de efeitos visuais; nenhum payload desse conjunto concede servidor-autoridade de dano, acerto, mana ou cast. O alvo da apresentação vem do remetente/handler, não de um spell próprio do Ace.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

Um pacote visual não confirma execução autoritativa. Black Arcana não deve converter VFX em hit/progress/cast nem pressupor que o protocolo seja disponível em host/modpack sem negociação e QA real de shader/render.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. Código-fonte Ace compilou contra Iron's `3.16.2` no build pinado; pack usa `3.16.3` segundo inventário, exigindo teste efetivo.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**
