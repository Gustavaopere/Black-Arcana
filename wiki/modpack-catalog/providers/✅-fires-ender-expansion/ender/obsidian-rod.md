# Obsidian Rod

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT` estática; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; JAR funcional, integração e Survival **PENDING**. **+0 identidades**; parâmetros documentados não são perks implementadas.

## Identidade e proveniência

Fire's Ender Expansion (`mod_id=firesenderexpansion`), spell **`firesenderexpansion:obsidian_rod`**, classe `net.fireofpower.firesenderexpansion.spells.ObsidianRodSpell`, host Iron's; escola default `irons_spellbooks:ender`, Uncommon, níveis1–5. Nome oficial de exibição **Obsidian Rods**; resumo da [descrição oficial][guide]: canaliza hastes que dificultam teleportes. [Registry][registry]. A entidade homônima e `firesenderexpansion:anchored_effect` são filhos, sem novas identidades semânticas.

Ledger físico #281: MC1.21.1/NeoForge, `firesenderexpansion-2.4.1.jar`, SHA-1 `da87a4a0c926dd75236766584cddbae69c6aeff7`; publisher [8167304](https://www.curseforge.com/minecraft/mc-mods/fires-ender-expansion/files/8167304). [Prova binária](../EXACT-BINARY-SPELLS-2.4.1.md)/[Java21 SUCCESS](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38434192044) fecham registry estático. Fingerprint publisher coincide com ledger; perfil instalado não foi remedido.

[Contratos comuns e ownership](../SPELL-PERK-BOUNDARIES-2.4.1.md): source oficial `FireOfPower/firesenderexpansion-1.21.1@5e4067e8112316f55c9f249530ba1917a7bf6643`, build Iron's3.15.6/Neo21.1.215; host consultado Iron's3.16.3 `e4056af90302d37eb1739f5ff05020b020e6e252`, pack Neo21.1.250. [Versões/licença][versions]: **All Rights Reserved**, resumos factuais e referências, sem importar implementação/assets. Source↔JAR não foi equiparado método a método.

## Aquisição, ingresso e causalidade

Sem override local de loot/crafting ou gate de item. Defaults Iron's são elegibilidade, **não distribuição/aquisição Survival comprovada**; enabled, escola, config efetiva e datapacks **NÃO VERIFICADOS**. Ingresso jogador usa wrapper Iron's, mana/cooldown, condições e SpellPreCastEvent; sem seleção prévia de alvo própria. [Spell][spell], [host][host-cast].

1. CONTINUOUS: `getCastTime(L)=60+5L`ticks; neutro65/70/75/80/85. Host aplica `round((60+5L)×CAST_TIME_REDUCTION)` neste tipo. Cooldown default60s=1200ticks. [Tempo][time], [host][host-cast].
2. `onServerCastTick` dispara1 haste se MagicData existe e `(remaining+1)%5==0`. **onCast não dispara**: só chama super. No host jogador, settlement CONTINUOUS acontece a cada10ticks; depois decrementa duração e chama tick somente enquanto casting ativo. Tiro5ticks e cobrança/evento10ticks são agendas distintas; falta de mana/interrupção/fase inicial alteram contagem. [Tick/spawn][shoot], [host manager][manager].
3. Spawn server: olho+forward normalizado×.2, Y ajustado por `rod.height−.5`; owner=caster, dano e duração definidos antes de addFreshEntity. `shoot(look,.05)` soma desvio vetorial aleatório normalizado, renormaliza e preserva módulo do look; host multiplica por speed3. Não há cone em graus declarado. [Spawn][shoot], [projétil][rod-shoot], [host][projectile].
4. Hit Living → `DamageSources.applyDamage`, direct=rod, attacker=owner, spell pai; somente retorno true aplica Anchored amplifier0 por `(int)(2P)`ticks. Qualquer hit de entidade descarta a haste. Override não chama super nem consumeEntityImpact: setters herdados de pierce/ricochet não demonstram continuidade. [Hit][rod-hit], [host damage][host-damage].
5. Impacto Ancient Debris com `Crafting.fragments_obtainable=true` cria1 Infused Obsidian Fragment **antes de tentar** destroyBlock(drops=false); retorno da destruição é ignorado. Depois chama super/discard. Sem gate local de claim/protection/rollback; conversão transacional segura não foi provada. [Impacto][rod-block], [config][config].

`P=(30+8×(L−1))×SPELL_POWER×schoolPower×POWER_MULTIPLIER`, neutro30/38/46/54/62, resolvido a cada disparo. Mana por settlement `(int)((5+1×(L−1))×MANA_MULTIPLIER)`, neutro5/6/7/8/9, **não custo total do canal nem custo por haste**. [Defaults][spell], [host][host-cast].

## Matriz de parâmetros para perks

| Eixo | Valor / consumidor / fase | Boundary, limite e estado | QA |
|---|---|---|---|
| Dano / tipo / cura / crítico | `0.01P` health points/haste, neutro.30/.38/.46/.54/.62. Sem cura/DoT/crítico local. Hit → SpellDamageSource da escola, default `irons_spellbooks:ender_magic`; resistência/friendly-fire/hurt podem negar. [Fórmula][shoot], [hit][rod-hit], [tipo][school], [source][damage-source]. | Power/config **NATIVE_ATTRIBUTE / CONFIG_NATIVE**. `SpellDamageEvent#setAmount(float)`/cancel é **HOOK_VERIFICADO** pré-resistência/friendly-fire/hurt sob host3.16.3; amount tentado não é HP entregue. `setDamage(float)` é seam de instância, adapter **CONTRATO_CONDICIONAL**. Conversão DamageType **⛔ SEM_HOOK_SEGURO**. | Q1/Q2 |
| Alcance / targeting / LOS | Projétil livre no look; sem range de seleção/lock próprio. Host3.16.3 raycast até próxima posição com collider; sweptAABB+.1, hit inflation.3 e hits ordenados por distância; owner/aliados bidirecionais excluídos pelo canHitEntity herdado. [Spawn][shoot], [host][projectile], [colisão][collision]. | Sem setter de range/filtro/single→multi. **⛔ SEM_HOOK_SEGURO**. ProjectileImpactEvent cancelável aparece no ramo entity; ramo block não posta esse evento nesse helper. Não concede bypass de claims. | Q2/Q3 |
| Área / count / budget | Uma haste por tick elegível, sem splash/explosão/cap total próprio; discard no primeiro hit processado. Quantidade total depende do canal. [Tick][shoot], [hit][rod-hit]. | `setExplosionRadius(float)` herdado não tem consumidor radial demonstrado aqui. **⛔ SEM_HOOK_SEGURO** para AOE/count/budget. Settlement observado não deve gerar outra haste. | Q2/Q4 |
| Projétil / AABB / velocidade | Registro1×1blocks/tracking64, speed3blocks/tick, desvio vetorial.05. Host gravidade.05blocks/tick² salvo noGravity, não ligado pelo provider; lifetime `tickCount>300`, descarte fora de entity-ticking chunks. Não é alcance garantido900. [Registro][entity], [rod][rod-shoot], [host vida][projectile], [gravidade][projectile-state]. | `ObsidianRod#setEffectLength(int)` sincronizado e `AbstractMagicProjectile#setDamage(float)` públicos: **HOOK_VERIFICADO** de instância pré-consumo; obter instância/owner/fase/sync continua **CONTRATO_CONDICIONAL**. Sem shared setSpeed nem setter seguro de AABB; resize **⛔ fail-closed**. | Q2/Q4 |
| Canal / cooldown / recast | `60+5L`ticks; tiro5 versus settlement10; cooldown60s default; recast0 herdado. [Tempo][time], [manager][manager]. | CastTimeReduction nativo CONTINUOUS alonga canal, não altera cadência. Config cooldown e `SpellCooldownAddedEvent.Pre#setEffectiveCooldown(int)`/cancel **CONFIG_NATIVE / HOOK_VERIFICADO** pré-cooldown. [Evento][cooldown]. Cadência por perk **⛔ SEM_HOOK_SEGURO**. | Q1/Q4 |
| Mana / falhas | Host debita settlements que consomem mana; falta de mana pode finalizar no check10ticks. Sem refund específico. [Cast][host-cast], [manager][manager]. | `SpellOnCastEvent#setManaCost(int)` **HOOK_VERIFICADO** pré-débito, desconto tardio não supera gate inicial. `setSpellLevel(int)` nesse evento muda onCast, que não dispara rod: não prova alterar nível guardado no tick. Sem segunda cobrança por hit. | Q1/Q4 |
| Anchored / duração / caps | `(int)(2P)`ticks, amp0; neutro60/76/92/108/124. Marker HARMFUL sem tick/cleanup próprio. [Duração][shoot], [setter][rod-state], [efeito][anchored]. | Setter muda duração da haste, não status já aplicado. Sem cap explícito/config/imunidade Anchored próprios localizados. Refresh/enforcement **CONTRATO_CONDICIONAL**; não adicionar cancelamento paralelo. | Q2/Q5 |
| Mundo / itens / config |1fragment por Ancient Debris, drops vanillafalse; `Crafting.fragments_obtainable=true`, global/worldRestart. [Impacto][rod-block], [config][config]. | **CONFIG_NATIVE**, não toggle por jogador. Spawn antes da destruição e retorno ignorado impedem presumir atomicidade/proteção. WorldEffectPolicy/claim bridge **⛔ SEM_HOOK_SEGURO** até validação. | Q3/Q5 |
| Summons / persistência / saída | SummonAI/cap/custo **N/A**. Haste owner=caster; AntiMagic herdada descarta. NBT próprio guarda só Effect Length **sem chamar super**; parent persiste owner/damage/age em seu caminho, omitido por estes overrides. [NBT][rod-nbt], [host estado][projectile-state]. | Não prometer restore/provenance seguro. Descartar haste não remove Anchored entregue. **CONTRATO_CONDICIONAL** para save/load/chunk/logout/morte. | Q4/Q5 |

## Anchored, deduplicação e concepção

`ServerEvents#preventAnchoredTeleportation` cancela EntityTeleportEvent em ServerLevel para LivingEntity ancorada, **exceto TeleportCommand**. `onTeleportSpellCast` cancela separadamente SpellTeleportEvent de ServerPlayer; feedback sobreposto é possível. Pre-cast bloqueia Portal do Iron's para jogador ancorado e suprime o randomTeleport do Core of Ender. Isso não prova interceptar toda mudança direta de dimensão/posição. [Eventos][events], [Portal/Core][portal-gate].

`AnchoredEvasionStopperMixin` retorna false em EvasionEffect#doEffect HEAD; `AnchoredPortalStopperMixin` intercepta PortalManager#canUsePortal* HEAD. [Evasion][evasion], [Portal mixin][portal-mixin]. Build3.15.6 versus host3.16.3 exige provar transformação carregada/overloads; mixin interno não é API genérica de perk.

Provider/Iron's possuem canal, mana, projétil, dano, Anchored e conversão. RPG possui progression/Mastery, lane nativo `irons:ender`; settlement10ticks, tiro5ticks, impacto, status e fragmento são fases do mesmo pai. Dedup por caster/canal/haste/fase, sem XP/proc extra por teleporte recusado. BA mantém custos/WorldEffectPolicy próprios; Enshrouded classifica fontes pelo contrato próprio, sem bridge Shroud por tema Ender. [Contrato comum](../SPELL-PERK-BOUNDARIES-2.4.1.md).

Assinatura ocupada: canal de hastes com baixo dano, anti-teleporte após hit e conversão específica de Ancient Debris. Nova magia requer geometria, recurso e contrato próprios; nome/VFX não demonstram lacuna.

## Verificação pendente

- **Q1:** config efetiva/atributos/níveis fora do default, gate/desconto, settlement/cooldown/scroll/criativo e aquisição Survival.
- **Q2:** dedicado/cliente, fase/cadência, colisão/escudos/aliados/PvP, cancel/zero/resist/hurt, status só após true, sync/setters/provenance.
- **Q3:** Ancient Debris protegido, destruição negada com item já spawnado, loaded chunks/claim e ProjectileImpactEvent entity versus block; sem loot duplicado.
- **Q4:** interrupção/sem mana/lag/power durante canal, budget de hastes, gravidade/lifetime/pierce descartado, unload/reload/antiMagic/logout/morte/owner.
- **Q5:** remoção/expiração/refresh Anchored, comando/pearl/chorus/Portal/Evasion/transição direta, mixins carregados e coexistência Cage/Stride. **PHYSICAL_QA/PERK_RUNTIME/SURVIVAL=PENDING**; nenhum Stage aprovado.

[registry]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/registries/SpellRegistries.java#L13-L34
[versions]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/gradle.properties#L15-L50
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L330
[host-damage]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L64
[school]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/SchoolRegistry.java#L99-L106
[damage-source]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/SpellDamageSource.java#L24-L51
[cooldown]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellCooldownAddedEvent.java#L9-L55
[teleport]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L167-L174
[guide]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/resources/assets/firesenderexpansion/lang/en_us.json#L61-L63
[spell]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/spells/ObsidianRodSpell.java#L25-L49
[time]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/spells/ObsidianRodSpell.java#L52-L58
[shoot]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/spells/ObsidianRodSpell.java#L62-L83
[entity]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/registries/EntityRegistry.java#L44-L48
[rod-shoot]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/entities/spells/ObsidianRod/ObsidianRod.java#L49-L64
[rod-block]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/entities/spells/ObsidianRod/ObsidianRod.java#L66-L77
[rod-hit]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/entities/spells/ObsidianRod/ObsidianRod.java#L80-L87
[rod-state]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/entities/spells/ObsidianRod/ObsidianRod.java#L90-L110
[rod-nbt]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/entities/spells/ObsidianRod/ObsidianRod.java#L136-L149
[anchored]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/effects/AnchoredEffect.java#L7-L10
[config]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/Config.java#L39-L41
[events]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/events/ServerEvents.java#L113-L166
[portal-gate]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/events/ServerEvents.java#L45-L98
[evasion]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/mixins/AnchoredEvasionStopperMixin.java#L18-L34
[portal-mixin]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/mixins/AnchoredPortalStopperMixin.java#L19-L39
[manager]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/MagicManager.java#L26-L108
[projectile]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L74-L114
[collision]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L153-L214
[projectile-state]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L280-L359
