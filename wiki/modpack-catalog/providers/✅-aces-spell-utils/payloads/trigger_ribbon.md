# TriggerRibbonPacket — Ace's Spell Utils 1.2.7.2

**Payload TYPE:** `aces_spell_utils:trigger_ribbon` · **Registry direction:** `playToClient` S2C · **Protocol:** `4.0.0`, `.optional()` · **Status:** ⚠️ fonte pinada; sem certificação.

## Wire contract e comportamento

- [`TriggerRibbonPacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/TriggerRibbonPacket.java) contém a implementação exata do `CustomPacketPayload`, `CustomPacketPayload.codec`, read/write e `IPayloadContext`.
- [`PayloadHandler.register`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/PayloadHandler.java) registra este `TYPE` com `STREAM_CODEC` e `handle` via `playToClient`. Não declara C2S neste registrar.
- **Campos no fio e ordem:** `int entityId`, `boolean attach`, seguida da serialização completa de `RibbonConfig`: `VarInt` número de cores (1..8 ao ler), ints RGB, ordinal byte de easing, `Curve width` (float head/tail + easing byte), `Curve alpha` idem, `VarInt length`, `boolean additive`.
- **Consumer client-side:** Em `context.enqueueWork` chama `RibbonManager.attach(entityId,config)` ou `RibbonManager.detach(entityId)`. O decoder exige `1 <= colorCount <= ColorRamp.MAX_STOPS`, que vale **8**, e lança `DecoderException` fora disso; `Easing.byOrdinal` é outro ponto de validação e não prova sucesso para ordinais ilegais.
- **Produção server-side e disseminação:** [`RibbonHandler`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/RibbonHandler.java) mantém `ConcurrentHashMap<UUID,Attached>`, manda `sendToPlayersTrackingEntityAndSelf`, reenfileira ao começar tracking e limpa mortos no tick. O pacote usa ID runtime da entidade, não UUID no wire.

## Targeting, geometria e limites

Config e attach são VFX por entityId, sujeitos a tracking/reload e reuso de ID. Não cria entidade, não imputa dano, não prova crit, proc ou cast.

Mana, cooldown, spell level, targeting de combate e dano **não são propriedades deste payload**. Duração/posição declaradas são render/presentation; não constituem autorização server-side para cast, hit ou Mastery. Não criar segunda instância do pipeline host da Ace. O Black Arcana mantém autoridade sobre seu runtime (server casting, WorldEffectPolicy, Strain, Corruption, Arcane Danger) e o RPG Skill Tree se limita a progressão através de contrato real.

## Proveniência e QA

Source `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, release `1.2.7.2-1.21.1`. Artefato da modlist `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 anotado `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` (source→JAR não confrontado); `build.gradle` usa Iron's 3.16.2, pack Iron's 3.16.3. **QA exigida:** handshake opcional 4.0.0, paridade codec, dados malformed, ciclo spawn/detach/tracking/dimension/server-stop e efeitos concorrentes de cliente. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `COMPLETE_PERK_READY=false`. +0 magias registradas.
