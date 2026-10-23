# Holy Lightning

**Revisão documental: 22/10/2026.** `technical_perk_dossier: 1`; `source_status: SOURCE_PINNED`; fidelidade `SOURCE_CAUSALITY` restrita aos pins abaixo. Catálogo ✅; runtime/perks ⚠️ condicionados. **+0 identidades mágicas.**

| Identidade e evidência | Valor / limite da prova |
|---|---|
| Provider / host / tipo | Ypsilon's Fundamentalism (Fundamental Principles); `mod_id=ypfundamentals`; host Iron's Spells 'n Spellbooks; `spell`, escola default Holy. |
| ID real / classe | `ypfundamentals:holy_lightning`; `com.ypsi.fundamentalism.spells.holy.HolyLightningSpell`; registro singleton via `ModSpells#registerSpell(AbstractSpell)` ([Registry]). Nome de exibição separado do ID. |
| Artefato físico histórico | Minecraft 1.21.1 / NeoForge; `ypfundamentals-1.1.7.1.jar`, SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`; [publicação CurseForge 8558503](https://www.curseforge.com/minecraft/mc-mods/fundamental-principles/files/8558503). [Auditoria histórica](../EXACT-BINARY-SPELLS-1.1.7.1.md) e [Java21 SUCCESS](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38436717443): `COUNTED_EXACT` só identidade/registry/classe/escola, sem prova de métodos ou gameplay. SHA-256: NÃO VERIFICADO. |
| Source consultado | Ypsilon `a9b8f8222fb2a800edece8c1568984bd2a764fc2`, metadados 1.1.7.1 / MIT ([Metadados]); dependência declarada Iron's **3.16.2** ([Versão]). Herança consultada separadamente em Iron's **3.16.3** `e4056af90302d37eb1739f5ff05020b020e6e252`. Não se afirma equivalência binária/source nem compatibilidade operacional 3.16.2→3.16.3. |
| Descrição oficial / resumo original | [Guia e nome no recurso de idioma][Guia]: arremessa uma lança sagrada veloz que causa dano no impacto. Nenhum asset ou implementação foi copiado. |

Os números seguintes são **defaults/fórmulas do source**, não config implantada. `n` é o nível resolvido pelo host; as listas usam nível nominal e multiplicadores neutros = 1. Gates, categorias ASM/Principles e valores efetivos exigem QA no pack. [Contrato comum de custos, eventos e compatibilidade](../SPELL-PERK-BOUNDARIES-1.1.7.1.md).

## Matriz por campo

`P_host=(14+6(n−1))×spell_power×holy_spell_power×power_multiplier`, via `AbstractSpell#getSpellPower(int,Entity)` [Host valores]. `P` é o retorno efetivo: em Player, se o mixin se aplicar, `(P_host+modifier_categorias)×fatigue_ratio`; aplicação/config/categorias são condicionais [Power mixin]. Neutro, sem bônus/penalidades de Principles: **14 / 20 / 26 / 32 health points por tentativa**; nome lightning/VFX não troca a escola Holy por Lightning.

| Campo | Default / fórmula / unidade | Declarante, fase e boundary real | Mutabilidade / limite / teste |
|---|---|---|---|
| Nível / raridade / escola | 1–4; Rare; Holy. Spell e entity type usam `ypfundamentals:holy_lightning` em registries distintos. | `HolyLightningSpell#defaultConfig/getSpellResource` [Spell]; `ModEntities#HOLY_LIGHTNING_PROJECTILE` [Entidade registry]. | `NATIVE/CONFIG_NATIVE`; não são duas identidades mágicas; Q1. |
| Mana | `80+30(n−1)` = 80 / 110 / 140 / 170; host aplica mana multiplier e `int`. | Construtor [Spell] + `getManaCost` [Host valores]; `castSpell` cobra server antes do spawn [Host cast]. | `NATIVE` config; `CONDITIONAL` `SpellOnCastEvent#setManaCost(int)` [Evento cast]. Sem refund local; Q2. |
| Cast / cooldown / recast | LONG; base 40 ticks = 2 s, efetivo `round(40×(2−softCap(cast_time_reduction)))`; cooldown default 15 s = 300 ticks, depois host. Recast herdado 0. | [Spell] [Host valores] [Host cooldown]. `softCap(x)=x` até 1.5, senão `2−0.25/(x−1)` [Softcap]. | `NATIVE` atributos/config; `CONDITIONAL` evento cooldown. Cast e lifetime têm authorities distintas; Q2. |
| Spawn / seleção / quantidade | Uma `HolyLightningProjectile`, owner=caster; spawn `caster.position+(0,eyeHeight,0)+caster.forward`, direção look. Sem seleção prévia, alvo salvo ou range numérico da spell. | `HolyLightningSpell#onCast` [Spawn], fluxo server do host. | `SEM_HOOK_SEGURO` para multi-spawn/retarget/alcance artificial. Q3. |
| Hitbox / detecção | EntityType **1.25×1.25 blocks**; sem override de dimensions nesta subclasse. Host broadphase usa AABB expandida pelo movimento +0.1; teste final é segmento contra target AABB inflada **0.3 blocks**, não esfera de raio 1.25. | [Entidade registry] [Projectile]; `AbstractMagicProjectile#handleHitDetection/raycastForEntitiesAlongPath` [Host hit]; [Intersect]. | `SEM_HOOK_SEGURO` para redimensionamento/target→AOE; renderer não altera colisão. Q3. |
| Velocidade / aceleração / alcance | Velocidade **inicial 6 blocks/tick** = 120 blocks/s a 20 TPS; noGravity=false; host subtrai 0.05 blocks/tick ao componente Y a cada travel. Sem drag/espalhamento próprios; trajetória sofre gravidade, não é hitscan. | `getSpeed`, construtor [Projectile]; `shoot/travel/getDefaultGravity` [Host projectile] [Host lifecycle]. | `SEM_HOOK_SEGURO` para velocidade/gravidade; produto speed×TTL não é alcance garantido, por arco e impactos. Q3/Q4. |
| LOS / blocos / filtros | Raycast varrido por tick usa ClipContext.COLLIDER/Fluid.NONE; pode truncar candidatos por bloco. Owner/aliados filtrados em `canHitEntity`; settlement tem PvP/team. Não há validação de claims específica provada. | [Host hit] [Host projectile] [Host resist]. `onHitBlock` da subclasse é vazio, mas `onHit` ainda chama super e descarta em **qualquer impacto** [Impacto]. | `CONDITIONAL` cancelamento de `ProjectileImpactEvent` para entidade; não prova setter de alvo ou proteção de blocos. Q4. |
| Dano / DamageType | `onHitEntity` tenta P por `ModSpells.HOLY_LIGHTNING.get().getDamageSource(this,getOwner())`; default **`irons_spellbooks:holy_magic`**. Não há dano de raio, chain lightning, ignite ou explosão secundária na classe. Tags Holy/magic só conforme datagen/pack efetivo. | [Impacto] [Host source] [Host schools] [Host tipos] [Host tags]. Handler não tem guard server próprio; dispatch principal vem da entidade/host. | `NATIVE_ATTRIBUTE` power genérico/Holy; `CONDITIONAL` amount pré-resist/hurt em living [Host dano] [Evento dano]. Conversão de tipo = ⛔ `SEM_HOOK_SEGURO`; Q5. |
| Pierce / settlement / lifetime | Subclasse não configura pierce/ricochet/homing; `onHit` toca thunder no server, chama super e **discard**. Não mantém trajetória após impacto. Sem TTL próprio; host descarta com `tickCount>300` = primeiro elegível 301, nominal 15 s. | [Impacto] [Host projectile]; defaults sincronizados pierce/ricochet 0 [Host lifecycle]. | `SEM_HOOK_SEGURO` para pierce/lifetime; setPierceLevel herdado não remove discard particular. Q4/Q6. |
| Anti-magic / persistência | Callback herdado faz partículas+discard; owner/NBT/lifecycle herdados; despawn fora de entity-ticking range e regra de save em unload pertencem ao host. | `AbstractMagicProjectile#checkDespawn/onAntiMagic/shouldBeSaved` [Host projectile] [Host lifecycle]. | `CONDITIONAL` para observação; sem cap de projéteis ativos local. Q6. |
| Visual / área / summons / mundo | Renderer usa planos com halfWidth=2, halfHeight=1 e animação, separado da AABB 1.25×1.25; partículas de cleanse no trail/impacto. Sem AOE, summon AI ou alteração de blocos. | `HolyLightningRenderer#renderModel` [Render]; [Projectile]. | `N/A` para raio de efeito; render scale não cria hitbox. Q3. |

## Pipeline, obtenção e autoria

Host valida admissão, aprendizado/mana/cooldown e `SpellPreCastEvent`; a spell não acrescenta pré-targeting [Host gates]. Concluído LONG: `SpellOnCastEvent` → mana → uma entidade com owner/posição/look/dano → `addFreshEntity` → som/super → cooldown [Host cast] [Spawn]. Cast interrompido, efeitos de Principles e recursos efetivos exigem servidor [Principles]. Loot/crafting/aprendizado herdam host; receita, chance e fonte Survival concreta: **NÃO VERIFICADAS** [Host obtenção].

Entity hit → `DamageSources#applyDamage` → `SpellDamageEvent` para living → resistência da escola → filtro friendly fire → `hurt` [Host dano] [Host resist]. O dano final depende também de armor/iFrames/eventos; o valor P não é dano recebido garantido. Impacto/partículas/som e remoção são derivados de uma mesma entidade; não criar dano, proc, mana ou mastery paralelos. Iron's/Ypsilon mantêm settlement/Principles; RPG Skill Tree mantém progressão/gates; Black Arcana seu runtime/WorldEffectPolicy. Assinatura ocupada: **lança Holy balística veloz, encerrada no impacto**. Nenhuma perk/adapter/runtime foi implementada.

## QA e pendências explícitas

- **Q1:** identidade do JAR histórico e parâmetros/source auditados; config/métodos binários e compatibilidade 3.16.2→3.16.3: **PENDING**.
- **Q2:** mana/cast/cooldown sob atributos, origem, interrupção e Principles; falha de spawn não tem rollback local. **PENDING**.
- **Q3:** medir AABB, broadphase, segmento+0.3, VFX, spawn adiantado e velocidade/queda; disparo junto a parede e alvos pequenos/multipart. **PENDING**.
- **Q4:** owner/aliados/PvP, bloco antes/depois do alvo, `ProjectileImpactEvent` cancelado, vários alvos alinhados e remoção. Não promover a piercing sem observação. **PENDING**.
- **Q5:** verificar dano real, tipo/tags efetivos, resistência, armor/iFrames, hooks amount e lado da execução de `onHitEntity`. **PENDING**.
- **Q6:** TTL >300, anti-magic, owner morto/desconectado, chunk/unload/save; GameTest, cliente/dedicado, multiplayer e Survival: **PENDING**.

[Versão]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/gradle.properties#L11-L16
[Metadados]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/gradle.properties#L30-L36
[Registry]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/ModSpells.java#L29-L58
[Guia]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/resources/assets/ypfundamentals/lang/en_us.json#L49-L72
[Spell]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/holy/HolyLightningSpell.java#L24-L60
[Spawn]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/holy/HolyLightningSpell.java#L73-L85
[Projectile]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/holy_lightning/HolyLightningProjectile.java#L25-L57
[Impacto]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/holy_lightning/HolyLightningProjectile.java#L59-L77
[Entidade registry]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/ModEntities.java#L29-L33
[Render]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/entity/spells/holy_lightning/HolyLightningRenderer.java#L38-L88
[Softcap]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L177-L182
[Intersect]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L294-L308
[Host valores]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L257
[Host cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L346
[Host gates]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L373-L401
[Host obtenção]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L612
[Host cooldown]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/MagicManager.java#L94-L122
[Host projectile]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L51-L214
[Host hit]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L153-L200
[Host lifecycle]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L280-L320
[Host dano]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L64
[Host resist]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L134-L173
[Host source]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/SpellDamageSource.java#L20-L51
[Host schools]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/SchoolRegistry.java#L89-L107
[Host tipos]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/ISSDamageTypes.java#L16-L39
[Host tags]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/datagen/DamageTypeTagGenerator.java#L31-L95
[Evento dano]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellDamageEvent.java#L24-L50
[Evento cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellOnCastEvent.java#L20-L74
[Principles]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/event/ModEvents.java#L516-L645
[Power mixin]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/mixins/principlesMixins/PowerSpellsMixin.java#L30-L65
