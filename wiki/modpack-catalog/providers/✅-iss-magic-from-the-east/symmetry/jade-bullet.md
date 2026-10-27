# Jade Bullet

**Dossiê documental — 27/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `RELEASE_BOUNDED_SOURCE`; integração `CONDITIONAL`; mutabilidade `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades / +0 strict**: efeitos/projéteis filhos não são novas spells.

## Identidade, proveniência e ingresso

ISS: Magic From The East, mod_id `iss_magicfromtheeast`, spell **`iss_magicfromtheeast:jade_bullet`**, escola default **`iss_magicfromtheeast:symmetry`**. Classe `net.warphan.iss_magicfromtheeast.spells.symmetry.JadeBulletSpell`. [Registro][registry], [escola/tipo][school].

JAR físico histórico #346 `iss_magicfromtheeast-1.1.5.jar`, SHA-1 `e3552ea6b7b32b843c48bf0d857237d4b7129ab0`, publisher [CF 7385201](https://www.curseforge.com/minecraft/mc-mods/magic-from-the-east/files/7385201); [22 identidades binárias](../EXACT-BINARY-SPELLS-1.1.5.md). Source oficial candidato de release `WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88`, de 27/12/2025, anterior ao upload do publisher: **RELEASE_BOUNDED_SOURCE**, sem prova de equivalência integral de métodos com o JAR. O pin declara versão 1.1.5, MC 1.21.1, NeoForge 21.1.187 e Iron’s 3.14.8; o pack usa NeoForge 21.1.250 e Iron’s 3.16.3. O host consultado é `e4056af90302d37eb1739f5ff05020b020e6e252` (3.16.3): cada comportamento herdado abaixo é um contrato desse host, condicionado à combinação efetiva. Config implantada **NÃO VERIFICADA**. Metadata All Rights Reserved; MIT apenas do template: fatos, paráfrases e permalinks, sem importar código ou assets. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.1.5.md).

No JAR publisher de SHA-1 acima, inspeção estreita com `javap` (JDK 21) confirmou as chamadas `setDamage`, `shoot` e `addFreshEntity`, o retorno 1.6 de `getSpeed`, a constante de raio 2.5, o fator de onda 0.5 e o uso de `DamageSources.applyDamage`. Isso sustenta apenas esses campos; filtros, ordem completa, herança e reentrância seguem a leitura source/host condicionada, sem certificar execução física.

[Guia oficial][guide], parafraseado: lança uma bala de jade que solicita dano direto e uma onda de impacto. Classes não sobrescrevem aquisição/loot/crafting/learning; seguem escola/config/gates Iron’s. Rota concreta Survival e config implantada **NÃO VERIFICADAS**, sem presumir creative-only. [Host][acquisition]. No wrapper jogador, admissão/pre-cast precedem onCast; SpellOnCastEvent e débito precedem efeito, e cooldown segue o settlement. Alterar L no evento não recalcula custo ou snapshots anteriores. [Ordem][cast-host].

## Fórmulas e pipeline causal

Os parâmetros e a ordem local abaixo pertencem ao **source limitado à release**, salvo os campos binários explicitados. `L` é o nível recebido no `onCast`; os intervalos usam os níveis default e multiplicadores neutros iguais a 1, sem impor um clamp adicional ao nível efetivo. `P` e `D` são dano solicitado em health points, antes de resistência, veto e iFrames; 20 ticks correspondem nominalmente a 1 s. Mana é inteira pelo truncamento do host. Defaults/config nativa são globais e não constituem um setter de perk por jogador.

`P=(2+(L−1))×SPELL_POWER×symmetryPower×C`, C=POWER_MULTIPLIER. Defaults Common/L 1–10, P neutro 2–11, mana neutra 10–55, INSTANT 0 ticks, cooldown 5 s = 100 ticks, sem recast próprio. [Spell][spell], [host][power].

1. `JadeBulletSpell#onCast` cria 1 JadeBulletProjectile com owner=caster; grava P e posição=feet+(0, eyeHeight−bulletHeight/2, 0). Tipo 0.4 × 0.4 blocks resulta em eye−Y 0.2 no caminho normal. Chama shoot(lookAngle), host define delta=lookAngle × getSpeed 1.6; noGravity=true. Retorno de addFreshEntity ignorado, sem refund local. [Spell][spell], [entity][bullet], [tipo][entity], [shoot][projectile].
2. Herda detecção: query swept AABB inflada 0.1/interseção 0.3, canHit exclui owner e aliança nas duas direções, eventos de impacto da entidade antes de onHit. Herda travel e expiry>300 ticks. Alcance máximo de seleção N/A; 1.6 × 300 não é alcance garantido por causa de colisão/homing/cleanup/outros listeners. [Host][projectile], [hit][hit-host].
3. `#onHitEntity` chama super, tenta helper **P** na vítima com SpellDamageSource (direta=bullet, causing=owner, spell JadeBullet), chama doAoeDamage e discard. Não testa boolean do dano nem isRemoved depois do parent. Em bloco, super → doAoeDamage → discard. [Impacto][impact], [settlement][damage-host].
4. `#doAoeDamage` consulta bbox.inflate 2.5 e canHitEntity, depois **distanceToSqr(position)<6.25**, pedindo **0.5 P** por elegível. Centro de física é posição atual do projétil; o argumento location é usado só para VFX. O Blastwave recebe parâmetro visual 1.2, que não governa o raio físico 2.5 blocks nem a hitbox 0.4 × 0.4 blocks. Alvo direto não é excluído e não há ledger entre direto/AOE; isso permite outra tentativa, sem garantir 1.5 P de HP por resistência/iFrames/veto. Sem cap de alvos ou LOS extra local. Dano direto e onda não têm guarda de servidor própria nesses overrides; o `if (!level.isClientSide)` da onda cobre apenas VFX. Confirmar autoridade/sync no caminho efetivo do host. [AOE][impact].
5. Parent onHitEntity pode despachar onHitBlock para escudo mágico quando shouldPierceShields = false. O override local continua depois, sem guard isRemoved; host handleHitDetection também pode despachar colisão de bloco após entidade. Assim uma AoE por callback não prova uma única AoE global por impacto/tick. Precisam QA budgets/reentrância, sem duplicar onda por adapter. [Impacto][impact], [parent shields][shield-host], [detecção][hit-host].
6. Damage/Age e dados herdados têm save/load; não há ledger/vínculo de cast pai persistido próprio. AntiMagic herdado descarta, shouldBeSaved exclui remoção UNLOADED_TO_CHUNK, sem homologar retomada segura. [Host state][state-host].

## Matriz de alteração por perks

| Eixo | Valor / consumidor / fase | Boundary real e limite | QA |
|---|---|---|---|
| Dano / power | DiretoP +0.5 P por elegível da onda; snapshot no spawn. [Spell][spell], [impact][impact]. | **NATIVE_ATTRIBUTE**: SPELL_POWER/symmetry_spell_power; **CONFIG_NATIVE** global: C. **HOOK_VERIFICADO**: [SpellDamageEvent][damage-event] aceita amount/cancel no helper Living. Adapter CONDITIONAL por owner+bullet+fase, não multiplicar a segunda tentativa duas vezes. | Q1/Q3 |
| Tipo / crítico | SpellDamageSource Symmetry → symmetry_magic; sem crítico/lifesteal/status próprio adicional. [Escola][school], [tipos][types], [impact][impact]. | Setter de amount não converte DamageType; conversão **⛔ SEM_HOOK_SEGURO**. Crítico local **N/A**. | Q3 |
| Target / range / área | Ray/travel host; AOE radius 2.5 por distância de origens, bbox inflada; sem LOS/cap local. [Impact][impact], [host][hit-host]. | Radius é literal, setExplosionRadius herdado não é consumido pela fórmula 2.5. Retarget/single → AOE/range **⛔ SEM_HOOK_SEGURO** sem resolver específico. | Q2/Q3 |
| Projétil / hitbox |1 bullet 0.4 × 0.4, noGravity, speed 1.6 blocks/tick nominal; host expiry>300. [Bullet][bullet], [tipo][entity], [host][projectile]. | SetDamage/homing/pierce herdados por instância não são seam terceiro pré-spawn universal. Resize/velocidade/count **CONTRATO_CONDICIONAL / ⛔ fail-closed**. | Q2/Q4 |
| Tempo / cooldown | INSTANT 0; cooldown 5 s/100 ticks antes modifiers; onda em callback, não DOT. [Spell][spell]. | Config/atributos/evento cooldownPre verificados genericamente no [comum](../SPELL-PERK-BOUNDARIES-1.1.5.md); não confundir timer de projétil com cooldown. | Q1/Q4 |
| Mana / recast | `int((10+5(L−1))×MANA_MULTIPLIER)`, 1 cast/sem recast local. [Spell][spell], [host][power]. | Wrapper expõe setters de custo/nível pré-onCast; integração CONDITIONAL e não recalcula custo por nível automaticamente. Sem mana extra por onda. | Q1/Q3 |
| Shield / ordem / dedup | Parent pode gerar callback de bloco, depois child ainda direto+AOE; vítima direta também elegível na onda. [Impact][impact], [shield-host][shield-host]. | Não assumir 1 hit/1 AoE absoluto. Impact observer não reconfigura todas as consultas/fases. Sem novo ledger/dano paralelo. | Q3/Q4 |
| Estado / mundo | Save Damage/Age herdado; sem mutation de blocos/heal/teleporte/summon. [Host state][state-host], [impact][impact]. | SummonAI/cap, DOT e world rollback **N/A**; sync/load/cleanup PENDING. | Q4 |

Assinatura ocupada: tiro direto com onda radial por impacto. Dedup exige cast → bullet → vítima → fase direta/onda/callback; não considerar o VFX outro cast ou confirmação de HP.

## Ownership, dedup e verificação

MFTE/Iron’s mantêm spell, recursos, entidades, dano e cleanup. RPG Skill Tree mantém progressão; BA seu runtime/world policy; Enshrouded sua classificação/Shroud. A escola Symmetry custom e sua lane Mastery continuam condicionadas ao contrato de token descrito no [comum](../SPELL-PERK-BOUNDARIES-1.1.5.md); não presumir `irons:symmetry` integrado.

- **Q1:** source/JAR/hosts/config, origens, nível/atributos, mana/cooldown e eventos de nível/custo antes/depois de snapshots.
- **Q2:** hitbox versus VFX, alvos finos/grandes, blocos/LOS/aliados/owner/PvP/claims, spawn recusado, número vivo e budgets.
- **Q3:** helper cancel/amount/resistência/iFrames, tentativas versus HP final, escudos, múltiplos callbacks e correlação de filhos/vítima.
- **Q4:** cliente/dedicado/multiplayer, persistência/unload/relog/restart/antiMagic, timers/owner e sync, ausência de segunda mana/XP/efeito.

Todos físicos **PENDING**; a ficha não implementa perk/adapter nem promove Stage.
[versions]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/gradle.properties#L11-L36
[registry]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTESpellRegistries.java#L24-L37
[school]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTESchoolRegistries.java#L32-L44
[types]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/damage/MFTEDamageTypes.java#L11-L17
[power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L257
[cast-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L332
[acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L612
[damage-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L64
[damage-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellDamageEvent.java#L13-L50
[source-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L560-L565
[projectile]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L51-L115
[hit-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L153-L213
[state-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L289-L359
[shield-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L361-L405
[spell]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/symmetry/JadeBulletSpell.java#L17-L70
[guide]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/resources/assets/iss_magicfromtheeast/lang/en_us.json#L34-L35
[bullet]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/jade_bullet/JadeBulletProjectile.java#L23-L32
[impact]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/jade_bullet/JadeBulletProjectile.java#L70-L112
[entity]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTEEntityRegistries.java#L158-L162
