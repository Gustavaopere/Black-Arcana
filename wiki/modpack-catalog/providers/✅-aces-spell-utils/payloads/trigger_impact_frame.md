# TriggerImpactFramePacket — payload Ace's Spell Utils 1.2.7.2

**CustomPacketPayload.Type:** `aces_spell_utils:trigger_impact_frame` · **Direção:** S2C `playToClient` · **Protocolo do registrar:** `4.0.0` opcional · **Estado:** ⚠️ source-pinned, compatibilidade/QA física não testadas.

## Fonte e codecs

- [`TriggerImpactFramePacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/TriggerImpactFramePacket.java) define `TYPE`, `STREAM_CODEC`, construtores de read/write e `IPayloadContext`.
- O [`PayloadHandler.register`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/PayloadHandler.java) usa `RegisterPayloadHandlersEvent`, `event.registrar("aces_spell_utils").versioned("4.0.0").optional()`, `playToClient(TYPE, STREAM_CODEC, handle)`. Nenhum `playToServer` é registrado no mesmo arquivo. Contrato **S2C de apresentação**, não autoridade de cast ou dano.
- **Payload e ordem dos campos:** Sete campos na ordem `int brightColor`, `int darkColor`, `float intensity`, `float threshold`, `int durationTicks`, `int flickerTicks`, `float aberrationStrength`; codec write/read simétricos.

## Efeito e consumidores

`handle` agenda `ImpactFrameEffect.trigger` com os sete parâmetros no cliente. [`ImpactFrameHandler.trigger`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/ImpactFrameHandler.java) no produtor servidor aplica `Mth.clamp(intensity,0,1)`, `Mth.clamp(threshold,0,1)`, `Math.max(1,durationTicks)`, `Math.max(1,flickerTicks)`, `Mth.clamp(aberrationStrength,0,1)` e usa `PacketDistributor.sendToPlayer` para cada player escolhido.

**Targeting e parâmetros:** Jogadores destinatários escolhidos pelo servidor; duração em ticks de render/impact frame, não cooldown de feitiço; cores/threshold são visuais, sem hitbox.

**Risco/limite do contrato:** O clamp pertence ao handler produtor, não ao construtor/deserializador do pacote. Não presumir proteção idêntica para qualquer emissor externo que construa o payload. Uma tela de flash NÃO demonstra ataque recebido ou evento de dano liquidado.

## Boundary de integração, proveniência e aceitação

- A Ace é autoridade sobre a apresentação, o decoder e os handlers da Ace; Iron's e outros providers conservam casting/custos host-native. Black Arcana mantém servidor como autoridade sobre seus próprios hits, target, mana, Strain, Corruption, Arcane Danger e WorldEffectPolicy. RPG Skill Tree não pode usar visual S2C como evento de Mastery.
- Não copiar payload class/codec para outro mod; se for necessária compatibilidade, comprovar API e versão no JAR exato, handshake opcional, lados e formato dos campos. Sem hook mutador corroborado: **fail-closed**.
- Source: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, release `1.2.7.2-1.21.1`; JAR da modlist `aces_spell_utils-1.2.7.2-1.21.1.jar` (SHA-1 anotado `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`, sem prova classfile). Dependência `build.gradle` Iron's `3.16.2`; host instalado `3.16.3`: não testado.
- **Aceitação:** handshake S2C do protocolo 4.0.0, decode com entradas válidas/inválidas, recebimento em side cliente, load/unload/relog, duração/cancelamento de VFX e interop render. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. **0 spells autônomos novos**.
