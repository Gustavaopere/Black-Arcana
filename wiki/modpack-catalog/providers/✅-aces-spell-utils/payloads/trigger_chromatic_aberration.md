# TriggerChromaticAberrationPacket — payload Ace's Spell Utils 1.2.7.2

**CustomPacketPayload.Type:** `aces_spell_utils:trigger_chromatic_aberration` · **Direção:** S2C `playToClient` · **Protocolo do registrar:** `4.0.0` opcional · **Estado:** ⚠️ source-pinned, compatibilidade/QA física não testadas.

## Fonte e codecs

- [`TriggerChromaticAberrationPacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/TriggerChromaticAberrationPacket.java) define `TYPE`, `STREAM_CODEC`, construtores de read/write e `IPayloadContext`.
- O [`PayloadHandler.register`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/PayloadHandler.java) usa `RegisterPayloadHandlersEvent`, `event.registrar("aces_spell_utils").versioned("4.0.0").optional()`, `playToClient(TYPE, STREAM_CODEC, handle)`. Nenhum `playToServer` é registrado no mesmo arquivo. Contrato **S2C de apresentação**, não autoridade de cast ou dano.
- **Payload e ordem dos campos:** Dois campos `float strength` e `int durationTicks`; read/write Float + Int via `CustomPacketPayload.codec`.

## Efeito e consumidores

`handle` agenda `ChromaticAberrationEffect.trigger(strength, durationTicks)`. [`ChromaticAberrationHandler.trigger`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/ChromaticAberrationHandler.java) em servidor limita `strength` a `0..1` e `durationTicks>=1`, depois manda a cada `ServerPlayer` via `PacketDistributor.sendToPlayer`.

**Targeting e parâmetros:** Render de cada cliente destinatário; sem target de combate, range, area, mana, cooldown ou projectile.

**Risco/limite do contrato:** Clamps no helper produtor, não no decoder. Configuração e render no cliente exigem QA física, especialmente stack com outros shaders.

## Boundary de integração, proveniência e aceitação

- A Ace é autoridade sobre a apresentação, o decoder e os handlers da Ace; Iron's e outros providers conservam casting/custos host-native. Black Arcana mantém servidor como autoridade sobre seus próprios hits, target, mana, Strain, Corruption, Arcane Danger e WorldEffectPolicy. RPG Skill Tree não pode usar visual S2C como evento de Mastery.
- Não copiar payload class/codec para outro mod; se for necessária compatibilidade, comprovar API e versão no JAR exato, handshake opcional, lados e formato dos campos. Sem hook mutador corroborado: **fail-closed**.
- Source: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, release `1.2.7.2-1.21.1`; JAR da modlist `aces_spell_utils-1.2.7.2-1.21.1.jar` (SHA-1 anotado `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`, sem prova classfile). Dependência `build.gradle` Iron's `3.16.2`; host instalado `3.16.3`: não testado.
- **Aceitação:** handshake S2C do protocolo 4.0.0, decode com entradas válidas/inválidas, recebimento em side cliente, load/unload/relog, duração/cancelamento de VFX e interop render. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. **0 spells autônomos novos**.
