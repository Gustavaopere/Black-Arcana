# TriggerDomePacket — Ace's Spell Utils 1.2.7.2

**Payload TYPE:** `aces_spell_utils:trigger_dome` · **Registry direction:** `playToClient` S2C · **Protocol:** `4.0.0`, `.optional()` · **Status:** ⚠️ fonte pinada; sem certificação.

## Wire contract e comportamento

- [`TriggerDomePacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/TriggerDomePacket.java) contém a implementação exata do `CustomPacketPayload`, `CustomPacketPayload.codec`, read/write e `IPayloadContext`.
- [`PayloadHandler.register`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/PayloadHandler.java) registra este `TYPE` com `STREAM_CODEC` e `handle` via `playToClient`. Não declara C2S neste registrar.
- **Campos no fio e ordem:** `double x,y,z` e `DomeConfig`: `float radius`, `VarInt durationTicks`, `float settleAt`, ordinal byte growth, shell com 1..8 cores + easing + curva alpha + floats rimPower/crownFade, pulse amount/speed, warp strength/rows/density/rate.
- **Consumer client-side:** `handle` agenda `DomeManager.spawn(pos,config)`. O decoder recusa count de cores <1 ou > `ColorRamp.MAX_STOPS=8` via `DecoderException`. O construtor `DomeConfig` aplica bounds: radius finito `0.5..128` (fallback 8), duration ticks `1..1200`, settleAt `0.01..1` (fallback `0.18`).
- **Produção server-side e disseminação:** [`DomeHandler.trigger`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/DomeHandler.java) envia a players até `RANGE=256.0` blocos e também chama `ShakeHandler.trigger` com radius `config.radius()*3`, magnitude `1.6`, duração limitada a `1..12` ticks por `durationTicks/3`, fade `10`.

## Targeting, geometria e limites

Dome é **casca visual**, não `AbstractDomainEntity`, dano, campo de colisão, proteção de blocos ou ritual Black Arcana. VFX de shake acompanhante pode duplicar apenas se outro efeito visual for enviado; não replicar automaticamente.

Mana, cooldown, spell level, targeting de combate e dano **não são propriedades deste payload**. Duração/posição declaradas são render/presentation; não constituem autorização server-side para cast, hit ou Mastery. Não criar segunda instância do pipeline host da Ace. O Black Arcana mantém autoridade sobre seu runtime (server casting, WorldEffectPolicy, Strain, Corruption, Arcane Danger) e o RPG Skill Tree se limita a progressão através de contrato real.

## Proveniência e QA

Source `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, release `1.2.7.2-1.21.1`. Artefato da modlist `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 anotado `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` (source→JAR não confrontado); `build.gradle` usa Iron's 3.16.2, pack Iron's 3.16.3. **QA exigida:** handshake opcional 4.0.0, paridade codec, dados malformed, ciclo spawn/detach/tracking/dimension/server-stop e efeitos concorrentes de cliente. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `COMPLETE_PERK_READY=false`. +0 magias registradas.
