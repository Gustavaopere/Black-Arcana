# TrailManager — emissão periódica e descarte — Ace's Spell Utils 1.2.7.2

**Tipo:** superfície de manutenção/routing de VFX do provider · **Estado:** ⚠️ contrato source-pinned, QA física fail-closed.

## Arquivos exatos e responsabilidades

- [`vfx/trail/TrailManager.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/vfx/trail/TrailManager.java)
- [`utils/TrailHandler.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/TrailHandler.java)
- [`events/AcesSpellUtilsServerEvents.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java)
- [`vfx/trail/TrailConfig.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/vfx/trail/TrailConfig.java) e [`vfx/trail/ActiveTrail.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/vfx/trail/ActiveTrail.java)
- [`client/particle/TrailParticle.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/client/particle/TrailParticle.java) — consumidor visual das [opções registradas](../particles/trail.md).

**Fluxo source:** `TrailHandler.attach(Entity,TrailConfig)` rejeita entidade nula/removida/cliente; delega para `TrailManager.attach`, que guarda `ActiveTrail` por UUID em `ConcurrentHashMap`. `AcesSpellUtilsServerEvents.onServerTick(ServerTickEvent.Post)` chama `TrailManager.tick()`; o loop remove trilha de entidade morta, ignora saltos > `1024.0` em distância ao quadrado (32 blocos) redefinindo posição e emite partículas via `MagicManager.spawnParticles` segundo density/spread/speed/yOffset. Em parada de servidor, `TrailManager.clear()` limpa o mapa.

**Targeting/range/tempo/consumo:** Estado de emissão visual da entidade anexada, não projétil de dano. `TrailConfig` limita density a **1..16**, spread/speed a pelo menos 0; yOffset é livre. `of(particle,density)` usa yOffset/spread/speed **0**. Não valida particle null nem finitude desses floats. O limite é por trilha, sem orçamento global de entidades/tráfego.

**Risco e dependências:** A fonte não mostra limitação global de custo por tick no loop; muitas trilhas exigem budget do consumidor. Não confundir `TrailParticle` de VFX com hitbox nem implementar tracking duplicado; QA de teleports/dimensions/entity lifecycle.

## Amostras, substituição e vida da partícula

`ActiveTrail` guarda entidade/config e inicia lastPos na posição corrente. Attach repetido substitui a entrada por UUID e reinicia lastPos; `isAttached` exige também a mesma instância de entidade, e detach remove por UUID. Para `distance²<10⁻⁶`, uma chamada pede `density` partículas na posição atual+YOffset. Para movimento normal, são `density` chamadas com uma partícula em `from.lerp(to,(i+1)/density)`, incluindo o ponto final e excluindo o inicial. Ambos passam spread nos três eixos, speed e force=false a `MagicManager.spawnParticles`; o transporte é do Iron's, sem payload próprio de trail. Esse attachment não tem TTL/NBT/persistência local.

Quando o tipo usado é `aces_spell_utils:trail`, `TrailParticle` usa RGB/scale das opções, quadSize inicial **scale×0.15**, lifetime aleatório inteiro **14..19 ticks**, friction **0.92**, hasPhysics=false e `PARTICLE_SHEET_TRANSLUCENT`. Após cada tick herdado aplica alpha=`1−age/lifetime` e quadSize×**0.96**; o Provider repassa a velocidade recebida. Lifetime da partícula e duração do attachment são contratos diferentes.

## Interoperabilidade e QA

Esse sistema faz apresentação e manutenção do provider. Não cria `AbstractSpell` nem prova hit, gasto de mana, proc, ganho de Mastery ou atualização do mundo. Black Arcana permanece authority para seu próprio casting/hazards/domains/rituais/WorldEffectPolicy/Strain/Corruption/Arcane Danger; RPG Skill Tree só progressão com gates reais. Não implementar segundo handler de estado a partir de evento puramente visual.

Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, versão source `1.2.7.2-1.21.1`; arquivo físico catalogado `aces_spell_utils-1.2.7.2-1.21.1.jar` SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` sem verificação de classfile. Build source depende Iron's `3.16.2`; modpack declara `3.16.3`. **QA:** JAR e event handlers reais, client/dedicated server, tracking/clear/teleport, cenários multicaster, packet sequencing e budgets gráficos; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `COMPLETE_PERK_READY=false`.
