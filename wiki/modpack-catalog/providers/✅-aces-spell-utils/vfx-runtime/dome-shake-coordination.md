# DomeHandler e ShakeHandler — cascata de apresentação — Ace's Spell Utils 1.2.7.2

**Tipo:** superfície de manutenção/routing de VFX do provider · **Estado:** ⚠️ contrato source-pinned, QA física fail-closed.

## Arquivos exatos e responsabilidades

- [`utils/DomeHandler.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/DomeHandler.java)
- [`utils/ShakeHandler.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/ShakeHandler.java)
- [`network/TriggerDomePacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/TriggerDomePacket.java)
- [`network/TriggerShakePacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/TriggerShakePacket.java)
- [`vfx/dome/DomeConfig.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/vfx/dome/DomeConfig.java)

**Fluxo source:** `DomeHandler.trigger(ServerLevel,Vec3,DomeConfig)` retorna sem parâmetros essenciais, senão envia `TriggerDomePacket` até `RANGE=256.0` blocos e chama `ShakeHandler.trigger` com `ShakeConfig(config.radius()*3.0F, 1.6F, min(12,max(1,config.durationTicks()/3)),10)`. `ShakeHandler.trigger` envia `TriggerShakePacket` para players a distância `config.radius()`, e overload `Entity` extrai a posição em ServerLevel. `DomeConfig` define clamp de raio `0.5..128`, duração `1..1200` ticks e settleAt `0.01..1` no construtor.

**Targeting/range/tempo/consumo:** Centro `Vec3` e audiência visual, não hitbox ou seleção de alvo. Cascata pode ter dois payloads (dome+shake) para mesmo evento VFX, sem segundo ataque.

**Risco e dependências:** Não confundir Dome visual com `AbstractDomainEntity` ou Black Arcana spell domains; o código não mostra mutação de blocos, persistência ou dano de área. Se integrar apresentações, respeitar budgets/QA render de grandes raios.

## Interoperabilidade e QA

Esse sistema faz apresentação e manutenção do provider. Não cria `AbstractSpell` nem prova hit, gasto de mana, proc, ganho de Mastery ou atualização do mundo. Black Arcana permanece authority para seu próprio casting/hazards/domains/rituais/WorldEffectPolicy/Strain/Corruption/Arcane Danger; RPG Skill Tree só progressão com gates reais. Não implementar segundo handler de estado a partir de evento puramente visual.

Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, versão source `1.2.7.2-1.21.1`; arquivo físico catalogado `aces_spell_utils-1.2.7.2-1.21.1.jar` SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` sem verificação de classfile. Build source depende Iron's `3.16.2`; modpack declara `3.16.3`. **QA:** JAR e event handlers reais, client/dedicated server, tracking/clear/teleport, cenários multicaster, packet sequencing e budgets gráficos; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `COMPLETE_PERK_READY=false`.
