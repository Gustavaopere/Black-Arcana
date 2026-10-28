# TrailManager — emissão periódica e descarte — Ace's Spell Utils 1.2.7.2

**Tipo:** superfície de manutenção/routing de VFX do provider · **Estado:** ⚠️ contrato source-pinned, QA física fail-closed.

## Arquivos exatos e responsabilidades

- [`vfx/trail/TrailManager.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/vfx/trail/TrailManager.java)
- [`utils/TrailHandler.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/TrailHandler.java)
- [`events/AcesSpellUtilsServerEvents.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java)

**Fluxo source:** `TrailHandler.attach(Entity,TrailConfig)` rejeita entidade nula/removida/cliente; delega para `TrailManager.attach`, que guarda `ActiveTrail` por UUID em `ConcurrentHashMap`. `AcesSpellUtilsServerEvents.onServerTick(ServerTickEvent.Post)` chama `TrailManager.tick()`; o loop remove trilha de entidade morta, ignora saltos > `1024.0` em distância ao quadrado (32 blocos) redefinindo posição e emite partículas via `MagicManager.spawnParticles` segundo density/spread/speed/yOffset. Em parada de servidor, `TrailManager.clear()` limpa o mapa.

**Targeting/range/tempo/consumo:** Estado de emissão visual da entidade anexada, não projétil de dano. O manager interpola movimentos em `config.density()` amostras; sem garantia de orçamento global para density arbitrária na API.

**Risco e dependências:** A fonte não mostra limitação global de custo por tick no loop, e altas densities exigem budget/cap do consumidor. Não confundir `TrailParticle` de VFX com hitbox nem implementar tracking duplicado; QA de teleports/dimensions/entity lifecycle.

## Interoperabilidade e QA

Esse sistema faz apresentação e manutenção do provider. Não cria `AbstractSpell` nem prova hit, gasto de mana, proc, ganho de Mastery ou atualização do mundo. Black Arcana permanece authority para seu próprio casting/hazards/domains/rituais/WorldEffectPolicy/Strain/Corruption/Arcane Danger; RPG Skill Tree só progressão com gates reais. Não implementar segundo handler de estado a partir de evento puramente visual.

Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, versão source `1.2.7.2-1.21.1`; arquivo físico catalogado `aces_spell_utils-1.2.7.2-1.21.1.jar` SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` sem verificação de classfile. Build source depende Iron's `3.16.2`; modpack declara `3.16.3`. **QA:** JAR e event handlers reais, client/dedicated server, tracking/clear/teleport, cenários multicaster, packet sequencing e budgets gráficos; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `COMPLETE_PERK_READY=false`.
