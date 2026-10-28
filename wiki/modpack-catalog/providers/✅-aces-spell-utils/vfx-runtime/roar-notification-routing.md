# RoarHandler — roteamento por tracking ou posição — Ace's Spell Utils 1.2.7.2

**Tipo:** superfície de manutenção/routing de VFX do provider · **Estado:** ⚠️ contrato source-pinned, QA física fail-closed.

## Arquivos exatos e responsabilidades

- [`utils/RoarHandler.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/RoarHandler.java)
- [`network/TriggerRoarPacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/TriggerRoarPacket.java)

**Fluxo source:** `RoarHandler.trigger(Entity,RoarConfig)` só envia para entidades válidas no servidor via `sendToPlayersTrackingEntityAndSelf`. `trigger(ServerLevel,Vec3,RoarConfig)` envia próximo à posição `RANGE=128.0` blocos via `sendToPlayersNear`. Overload de `Collection<ServerPlayer>` envia individualmente `TriggerRoarPacket` com ID da entidade.

**Targeting/range/tempo/consumo:** Entidade ou ponto fixo do efeito visual, e conjunto de espectadores conforme rota; `RANGE` é distribuição de payload, não target/AoE real de magia.

**Risco e dependências:** Roar remoto é apresentação do cliente. `entityId<0` no packet significa posição fixa, e `RoarConfig.radius` é geometria visual; não duplicar cast ou procurar impacto usando ID de roar.

## Interoperabilidade e QA

Esse sistema faz apresentação e manutenção do provider. Não cria `AbstractSpell` nem prova hit, gasto de mana, proc, ganho de Mastery ou atualização do mundo. Black Arcana permanece authority para seu próprio casting/hazards/domains/rituais/WorldEffectPolicy/Strain/Corruption/Arcane Danger; RPG Skill Tree só progressão com gates reais. Não implementar segundo handler de estado a partir de evento puramente visual.

Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, versão source `1.2.7.2-1.21.1`; arquivo físico catalogado `aces_spell_utils-1.2.7.2-1.21.1.jar` SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` sem verificação de classfile. Build source depende Iron's `3.16.2`; modpack declara `3.16.3`. **QA:** JAR e event handlers reais, client/dedicated server, tracking/clear/teleport, cenários multicaster, packet sequencing e budgets gráficos; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `COMPLETE_PERK_READY=false`.
