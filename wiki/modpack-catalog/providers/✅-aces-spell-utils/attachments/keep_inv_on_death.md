# keep_inv_on_death — attachment de Ace's Spell Utils 1.2.7.2

**Registry:** `NeoForgeRegistries.ATTACHMENT_TYPES` · **ID:** `aces_spell_utils:keep_inv_on_death` · **Tipo:** `AttachmentType<Boolean>` · **Status:** ⚠️ source-pinned.

## Registro, persistência e lifecycle

[`ASAttachmentRegistry.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ASAttachmentRegistry.java) registra `AttachmentType.builder(() -> false).serialize(Codec.BOOL).copyOnDeath().build()`. Default `false`, serialização boolean em dados de attachment, flag `copyOnDeath`. `AcesSpellUtils` registra `ASAttachmentRegistry` no mod event bus.

O [handler de keep inventory](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java) usa o attachment nos eventos `LivingDeathEvent`, `LivingExperienceDropEvent`, `PlayerEvent.Clone`, e regras de Curios; [`PlayerMixin.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/mixins/server/PlayerMixin.java) cancela drop de equipamento quando ativo. A interface `IKeepInventoryEntity.range=128` é empregada em busca por AABB inflado por `range*2`; a condição não prova raio euclidiano de 128.

**Owner:** jogador com state boolean server-owned. Não é magia, custo, cooldown, efeito de área ou cast. `copyOnDeath` combinado com remoção explícita no Clone requer confirmação de ordem real para evitar duplicação ou perda de inventário. Não instalar pipeline de duplicação de XP/Curios/inventário. Ver [ficha da família](../systems/keep-inventory-companion.md).

## Aceitação

Reproduzir morte/respawn com gamerule keepInventory habilitada/desabilitada, Curios, XP, multiplayer, distância, NBT antes/depois, e mixin. Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, JAR 1.2.7.2 com SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` apenas catalogado. `physical_qa=NOT_TESTED`, `mutating_hook=NOT_VERIFIED`, `COMPLETE_PERK_READY=false`.
