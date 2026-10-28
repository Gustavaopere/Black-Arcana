# RibbonHandler — anexação, tracking e limpeza — Ace's Spell Utils 1.2.7.2

**Tipo:** superfície de manutenção/routing de VFX do provider · **Estado:** ⚠️ contrato source-pinned, QA física fail-closed.

## Arquivos exatos e responsabilidades

- [`utils/RibbonHandler.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/RibbonHandler.java)
- [`events/AcesSpellUtilsServerEvents.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java)
- [`network/TriggerRibbonPacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/TriggerRibbonPacket.java)

**Fluxo source:** `RibbonHandler` mantém `ConcurrentHashMap<UUID, Attached(Entity,RibbonConfig)>` no servidor. `attach` armazena entidade e envia `TriggerRibbonPacket(id,true,config)` via `sendToPlayersTrackingEntityAndSelf`; `detach` remove do mapa e envia `attach=false`. `resend(ServerPlayer,target)` reenvia config para novos espectadores; `pruneDead` remove registros de entidades não vivas; `clear` na parada do servidor. `AcesSpellUtilsServerEvents.onStartTracking(PlayerEvent.StartTracking)` chama `resend` para ServerPlayer e `onServerTick(ServerTickEvent.Post)` executa `pruneDead`.

**Targeting/range/tempo/consumo:** Entidade rastreada no mundo e cliente de espectadores; wire transmite `entityId` runtime e config. Não há damage source, spell ID, mana ou alcance de cast nesse canal.

**Risco e dependências:** O mapa é estático por UUID e usa igualdade de instância no `isAttached` e `resend`. Testar relog, id reuse, teleporte/dimensão, stop; ausência de reenvio pode desincronizar só o visual, não deve alterar estado server gameplay.

## Interoperabilidade e QA

Esse sistema faz apresentação e manutenção do provider. Não cria `AbstractSpell` nem prova hit, gasto de mana, proc, ganho de Mastery ou atualização do mundo. Black Arcana permanece authority para seu próprio casting/hazards/domains/rituais/WorldEffectPolicy/Strain/Corruption/Arcane Danger; RPG Skill Tree só progressão com gates reais. Não implementar segundo handler de estado a partir de evento puramente visual.

Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, versão source `1.2.7.2-1.21.1`; arquivo físico catalogado `aces_spell_utils-1.2.7.2-1.21.1.jar` SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` sem verificação de classfile. Build source depende Iron's `3.16.2`; modpack declara `3.16.3`. **QA:** JAR e event handlers reais, client/dedicated server, tracking/clear/teleport, cenários multicaster, packet sequencing e budgets gráficos; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `COMPLETE_PERK_READY=false`.
