# TriggerRoarPacket — Ace's Spell Utils 1.2.7.2

**Payload TYPE:** `aces_spell_utils:trigger_roar` · **Registry direction:** `playToClient` S2C · **Protocol:** `4.0.0`, `.optional()` · **Status:** ⚠️ fonte pinada; sem certificação.

## Wire contract e comportamento

- [`TriggerRoarPacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/TriggerRoarPacket.java) contém a implementação exata do `CustomPacketPayload`, `CustomPacketPayload.codec`, read/write e `IPayloadContext`.
- [`PayloadHandler.register`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/PayloadHandler.java) registra este `TYPE` com `STREAM_CODEC` e `handle` via `playToClient`. Não declara C2S neste registrar.
- **Campos no fio e ordem:** `int entityId`; se `entityId < 0`, também `double x,y,z` (posição fixa). Depois enum ordinal byte `RoarStyle`, floats `strength,sharpness,radius,thickness,blur,refraction`, `VarInt durationTicks`, byte ordinal `Easing growth`.
- **Consumer client-side:** Handler agenda `RoarEffect.trigger(pos,config)` para ID negativo, senão `RoarEffect.trigger(entityId,config)`; `NO_ENTITY=-1`. Decoder usa `RoarStyle.byOrdinal` e `Easing.byOrdinal`; não afirmar aceitação de índices arbitrários.
- **Produção server-side e disseminação:** [`RoarHandler.trigger(Entity,..)`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/RoarHandler.java) envia aos jogadores que rastreiam entidade; versão posicional envia `sendToPlayersNear(..., RANGE=128.0)`; overload aceita coleção de destinatários.

## Targeting, geometria e limites

`radius` do RoarConfig é campo de efeito gráfico, não hitbox. RANGE=128 é distância de notificação do produtor posicional, não alcance de dano de spell.

Mana, cooldown, spell level, targeting de combate e dano **não são propriedades deste payload**. Duração/posição declaradas são render/presentation; não constituem autorização server-side para cast, hit ou Mastery. Não criar segunda instância do pipeline host da Ace. O Black Arcana mantém autoridade sobre seu runtime (server casting, WorldEffectPolicy, Strain, Corruption, Arcane Danger) e o RPG Skill Tree se limita a progressão através de contrato real.

## Proveniência e QA

Source `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, release `1.2.7.2-1.21.1`. Artefato da modlist `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 anotado `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` (source→JAR não confrontado); `build.gradle` usa Iron's 3.16.2, pack Iron's 3.16.3. **QA exigida:** handshake opcional 4.0.0, paridade codec, dados malformed, ciclo spawn/detach/tracking/dimension/server-stop e efeitos concorrentes de cliente. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `COMPLETE_PERK_READY=false`. +0 magias registradas.
