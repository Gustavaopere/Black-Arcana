# Bone Hands

**Dossiê documental — 27/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT` somente para registry; lógica `RELEASE_BOUNDED_SOURCE`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`; sem certificação estática. **+0 identidades/+0 strict**: criaturas, ataques e efeitos são filhos desta spell.

## Identidade, proveniência e aquisição

ISS: Magic From The East **1.1.5**, ID **`iss_magicfromtheeast:bone_hands`**, escola própria `iss_magicfromtheeast:spirit`; declarante `net.warphan.iss_magicfromtheeast.spells.spirit.BoneHandsSpell`. [Registry][registry], [classe/defaults][spell].

JAR físico histórico #346 `iss_magicfromtheeast-1.1.5.jar`, MC 1.21.1/NeoForge, publisher [CF 7385201](https://www.curseforge.com/minecraft/mc-mods/magic-from-the-east/files/7385201), **1680780 bytes**, SHA-1 `e3552ea6b7b32b843c48bf0d857237d4b7129ab0`; [identidade binária estática](../EXACT-BINARY-SPELLS-1.1.5.md). Fonte oficial **`WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88`**, candidata limitada à release: commit 27/12/2025 16:35:34 UTC, antes da [publicação oficial](https://www.curseforge.com/api/v1/mods/1224162/files/7385201) às 17:17:39.317 UTC. Não é prova de correspondência integral source↔JAR. O pin 13208302 é posterior e diverge; 904 é anterior a mudanças presentes no publisher. Source f2 compila com Iron’s 3.14.8/Neo 21.1.187/Gecko 4.7.5.1/Curios 9.2.2; pack tem Iron’s 3.16.3/Neo 21.1.250. Host source consultado `e4056af90302d37eb1739f5ff05020b020e6e252`. [Versões][versions], [limites comuns](../SPELL-PERK-BOUNDARIES-1.1.5.md). All Rights Reserved: fatos, paráfrases e permalinks, sem importar código/assets.

[Guia oficial][guide], parafraseado: invoca mãos espirituais presas ao solo que golpeiam alvos ao alcance. Sem override local de loot/crafting/learning nos métodos desta spell; ingresso e elegibilidade seguem [host/config][acquisition]. Rota Survival concreta, scroll instalado, config implantada e gates efetivos **NÃO VERIFICADOS**. Raridade/maxLevel abaixo são defaults, não prova de obtenção.

## Parâmetros e pipeline causal

Esta release possui **mãos temporárias com recasts de novos spawns**, não o summon de dez minutos/HP escalável adicionado em 132. `P=(3+1×(L−1))×SPELL_POWER×spiritPower×POWER_MULTIPLIER`; **A=P**, neutro 3–9 HP nos níveis default 1–7; **T=240+40 L ticks**, 280–520 ticks=14–26 s de contador local. Power não altera T/count/range. [Defaults][spell], [helpers][stats], [host][power-cost].

| Eixo | Default / consumer / unidade |
|---|---|
| Mana / cast / cooldown |`int((40+10(L−1))×MANA_MULTIPLIER)`, 40–100 neutra; INSTANT 0; Uncommon, maxLevel 7; cooldown 60 s=1200 ticks antes de modifiers. [Spell][spell], [host][power-cost]. |
| Recast |R=1+floor(L/3) casts totais: 1 emL 1–2, 2 emL 3–5, 3 emL 6–7. Janela 60 ticks=3 s, castData=null; inicial deixaR−1 restantes. [Cast][spawn], [recast][recast-local], [constructor host][recast-host]. |
| Placement / corpo |TargetBlock Fluid.ANY/range 24 blocks; uma BoneHandsEntity por chamada, corpo 0.4 × 8.5 blocks, tracking 64. Não confundir altura 8.5 com extensão do slam. [Cast][spawn], [tipo][entity-type]. |
| HP / proteção |MAX_HEALTH base 30 não sobrescrito pelo spell; noGravity/noPhysics, sem deslocamento de navegação no goal. Hurt não-bypass acima 10 é limitado a 10 no método local, antes de fases herdadas. [Entidade][mob]. |

1. Host admite/anuncia/debita; sem recast ativo registra janela 60 ticks/null. Depois, **independentemente de já haver recast**, cria outra mão no ponto alvo, define ATTACK_DAMAGE=P e duration=T, posiciona e solicita addFreshEntity, ignorando retorno. Não publica SpellSummonEvent nem chama initSummon/setDuration do manager. Constructor chama setOwner, mas isso não cria fila de expiração nem castData de grupo. [Cast][spawn], [constructor][mob], [host][cast-host], [owner manager][manager].
2. Wrapper jogador com recast já existente não debita mana outra vez, decrementa o restante após onCast; count inclui inicial e janela termina/cooldown segue callback herdado. Sem grupo UUID no recast, não presumir que o segundo cast remove as mãos antigas. A existência do registro nativo não prova cap global: fora da janela/reentrada/AI/outroscasters precisam QA. [Cast][spawn], [recast-host][recast-host], [wrapper][cast-host].
3. Goals copiam target do owner, reagem ao ataque do owner e HurtByTarget. Distância≤9 blocks autoriza animação de slam; entre 9 e 12 observa/gira, acima 12 limpa target/memória. O goal próprio não move a entidade. Não há gate local de LOS no slam, nem target humano individual obrigatório em cada caixa. [AI][mob], [goal][attack-goal].
4. BONE_SLAM declara 40 ticks/timestamp 15; no hitframe calcula direção horizontal, origem=eye−Y 8+forward× 1.5 e **7 caixas** com centros origin+forward×i, i 0–6. Cada caixa usa±(1, 5, 1), portanto dimensões completas **2 × 10 × 2 blocks**; caixas sobrepõem. Consulta Living, pickable e !isFriendlyFireBetween; sem cap/ledger de vítimas ou LOS por caixa. [Goal][attack-goal], [timing][animations].
5. **Consumer executado:**  em cada caixa chama `LivingEntity.hurt(mobAttack(mão),A)` plain, depois hurtMarked=true; não lê retorno, não zera iFrames. Portanto uma entidade pode receber várias tentativas no mesmo slam; não são sete hits garantidos. Esse caminho não passa pelo helper/SpellDamageEvent/Spirit resistance. O método separado doHurtTarget usa a fonte Spirit e Utils, mas o slam do goal não o chama. Incoming host ainda reconhece a própria mão IMagicSummon como direta/causadora de mobAttack e pode aplicar SUMMON_DAMAGE do owner Living. [Goal][attack-goal], [método alternativo][mob-hit], [incoming][summon-damage], [helper][damage-host].
6. Rise inicia contador 20; predecrementa até<0, sem decrementar duration nesse ramo. Depois duration-- e igualdade exata 0 pede retreat. Retreat 20 predecrementa até<0 e descarta; tempo nominal T não inclui essas duas fases. Tick chama super antes; não há guard servidor local em todo o contador. Não alegar expiração exata T wallclock. Não há serialização local de duration/rise/retreat nem override local onRemovedFromLevel chamando onRemovedHelper: a persistência e limpeza de ownership exigem prova/QA próprias. [Tick][mob-tick], [interface][summon-interface], [manager][manager-save].
7. Antimagic via IMagicSummon pede onUnSummon, que ativa flag de retreat; não remove imediatamente. Rise/shouldIgnoreDamage bloqueiam dano não-bypass; fireImmune=true/isPushable=false. Separadamente, `MFTEServerEvent#ignoreKnockBackEntityList` cancela `LivingKnockBackEvent` para BoneHands, JadeExecutioner e ExtractedSoul; isso é veto nativo ao knockback, distinto de resistência base, empurrão por fluido ou do cap de dano. [Handler][knockback-handler]. Sem cura/status/block mutation locais. O handler f2 não possui veto CounterSpell específico de BoneHands; não importar proteção de Samurai/Executioner. [Entidade][mob], [unsummon][mob-unsummon], [Counterspell host][counter-host].

**Prova binária estreita:**  BoneHandsSpell SHA-256 `1ef830f51d3797425c601f7feca9607d70feec51df3493430e675784719ba4ee`; getRecastCount usa idiv 3; onCast literal 60/null e range 24, getDuration 240+40 L, setDuration 106→addFreshEntity 125/pop 128. BoneHandAttackGoal inspecionado usa loopi≤6 e lambda com mobAttack→LivingEntity.hurt, confirmando distinção de consumer. Não equiparar toda classe ao source.132 mudou cast/custo/recast/range/HP/evento/lifecycle: não usar sua variante como release.

## Matriz de alteração por perks

| Eixo | Superfície real / consumidor | Limite de integração | QA |
|---|---|---|---|
| Dano / power |P vira ATTACK_DAMAGE no spawn; slam lê atributo atual. [Stats][stats], [goal][attack-goal]. |NATIVE_ATTRIBUTE SPELL_POWER/Spirit/configPower no cálculo; SUMMON_DAMAGE incoming cobre mão. SpellDamageEvent não cobre slam plain. Nenhum hook específico de amount desse slam comprovado. |Q1/Q3|
| Tipo / owner / status |Slam plain mobAttack, doHurtTarget alternativo Spirit; sem DOT/heal. [Goal][attack-goal], [hit][mob-hit]. |⛔ SEM_HOOK_SEGURO para converter fonte ou acrescentar status; não rotear cópia do golpe por helper. |Q3|
| Range / alvo / área |Placement 24, gate 9/watch 12; 7 caixas 2 × 10 × 2 sobrepostas, sem LOS local. [Cast][spawn], [goal][attack-goal]. |Constantes e consumer locais, sem setter por evento de spell. ⛔ SEM_HOOK_SEGURO para raio/maxTargets/single→AOE/retarget. |Q2/Q5|
| Count / corpo / velocidade |1 spawn/chamada; R 1+floor(L/3); corpo 0.4 × 8.5, noPhysics/sem navegação. [Cast][spawn], [mob][mob]. |Sem SpellSummonEvent nesta release; substituição/count/resize/AI sem seam seguro. N/A para projétil, pierce/acceleration. |Q2|
| Duração / recast |T 240+40 L local+rise/retreat; janela 60 independente/null. [Tick][mob-tick], [cast][spawn]. |setDuration público muda contador da entidade, não grupo/callback persistente; API não é adapter validado. Não transpor initSummon da variante 132. |Q4|
| Mana / cast / cooldown |INSTANT 0, 40+10(L−1), 60 s; recasts host-owned. [Spell][spell], [wrapper][cast-host]. |CONFIG_NATIVE/evento de mana no wrapper; mutarL não refaz admissão. Alterar cooldown não recolhe mãos nem muda T. |Q1/Q4|
| Defesa / persistência / mundo |HP 30, cap 10 não-bypass, veto nativo a LivingKnockBackEvent, retreat, ownership sem fila; sem blocos. [Handler][knockback-handler]. [Mob][mob], [tick][mob-tick]. |CONTRATO_CONDICIONAL para cleanup/persistência; nenhum cap global/refund/rollback demonstrado. |Q3/Q4|

## Deduplicação e validação pendente

A autoridade de casting, recursos, grupos/UUIDs, AI, dano e cleanup é provider/host. Não recriar dano, status, heal, spawn ou despawn num listener para simular perk; escola custom/Mastery e inscrição de adapter seguem o [contrato comum](../SPELL-PERK-BOUNDARIES-1.1.5.md). Deduplicar cast pai→UUID de criatura→ataque/projétil→alvo; uma vítima, partícula ou callback não constitui outra identidade de spell.

- **Q1:**  origem/scroll/Survival/config real, níveis default e modificados, custo/admissão/pagamento, recast, cooldown e interrupção.
- **Q2:**  posição/solo/fluido/LOS/colisão/claims, count, replacement compatível/incompatível, associação original, addFreshEntity=false e ausência de refund demonstrado.
- **Q3:**  dano direto/causador/kill credit, resistência/alliances/PvP, helper veto, atributo SUMMON_DAMAGE por consumer, iFrames, veto de knockback nativo versus resistência base e demais efeitos.
- **Q4:**  morte, antimagic/Counterspell, recast/timeout, owner ausente, chunk unload, logout/relogin/restart e duração restante.
- **Q5:**  dedicado/cliente/multiplayer, escala/hitbox versus visual, AI/sync, limites de carga e dedup/progressão. **Todos PENDING**; sem execução física ou integração mutadora nova.

[registry]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTESpellRegistries.java#L24-L50
[versions]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/gradle.properties#L11-L39
[spell]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/BoneHandsSpell.java#L23-L53
[spawn]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/BoneHandsSpell.java#L72-L88
[stats]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/BoneHandsSpell.java#L90-L96
[recast-local]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/BoneHandsSpell.java#L66-L69
[guide]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/resources/assets/iss_magicfromtheeast/lang/en_us.json#L43-L44
[acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L612
[power-cost]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L257
[cast-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L347
[damage-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L64
[summon-damage]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L114-L131
[melee-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L475-L498
[melee-range]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/mobs/goals/WarlockAttackGoal.java#L44-L46
[manager]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/SummonManager.java#L63-L179
[manager-save]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/SummonManager.java#L239-L378
[recast-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/RecastInstance.java#L27-L35
[summon-interface]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/mobs/IMagicSummon.java#L22-L86
[summon-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellSummonEvent.java#L1-L39
[counter-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/CounterspellSpell.java#L66-L96
[mob]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/bone_hands/BoneHandsEntity.java#L55-L145
[mob-hit]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/bone_hands/BoneHandsEntity.java#L148-L159
[mob-unsummon]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/bone_hands/BoneHandsEntity.java#L77-L104
[mob-tick]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/bone_hands/BoneHandsEntity.java#L227-L249
[attack-goal]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/bone_hands/BoneHandAttackGoal.java#L30-L118
[animations]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/bone_hands/BoneHandsEntity.java#L45-L52
[entity-type]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTEEntityRegistries.java#L90-L94

[knockback-handler]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/events/MFTEServerEvent.java#L98-L107
