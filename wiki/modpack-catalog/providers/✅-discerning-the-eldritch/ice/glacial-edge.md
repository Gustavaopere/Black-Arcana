# Glacial Edge / Glacial Cleave

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades/+0 strict**: efeitos, entidades e fases derivados não são novas spells.

## Identidade e proveniência

Provider **Discerning The Eldritch**, `mod_id=discerning_the_eldritch`, JAR físico histórico **`discerning_the_eldritch-1.4.4-1.21.jar`**, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`; [publisher CF8816497](https://www.curseforge.com/minecraft/mc-mods/discerning-the-eldritch/files/8816497), [prova estática de identidade](../EXACT-BINARY-SPELLS-1.4.4-1.21.md). Source oficial `AceTheEldritchKing/Discerning_The_Eldritch@7bbd81f902c65a4452f47656ebd948cae8cd5833`. Build Iron’s 3.16.2/NeoForge 21.1.244/Azure 3.1.0 versus pack Iron’s 3.16.3/NeoForge 21.1.250/Azure 3.1.11; Ace 1.2.7.2 coincide na versão declarada, sem prova de ABI. Host lido Iron’s `e4056af90302d37eb1739f5ff05020b020e6e252`. Versão declarada não equipara métodos source↔JAR. Sinais MIT/PolyForm Shield conflitantes: fatos/paráfrases/permalinks, sem importar implementação/assets. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md).

Spell **`discerning_the_eldritch:glacial_edge`**, escola default `irons_spellbooks:ice`, Rare, níveis default1–8; declarante `net.acetheeldritchking.discerning_the_eldritch.spells.ice.GlacialEdgeSpell`, consumer `entity.spells.glacial_edge.GlacialEdge`. Display oficial **Glacial Cleave** é alias da mesma identidade, não segunda spell. [Defaults][spell], [guia][guide]. Guia parafraseado: corte de gelo que aplica Chilled ao atingir.

Sem override local de crafting/loot/learning/precondição; aquisição segue host/config, rota Survival concreta **NÃO VERIFICADA**. Gates DTE/host e ordem de admissão→evento→débito→onCast permanecem no [contrato comum](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md). [Wrapper][host-cast], [aquisição][acquisition].

## Parâmetros e execução

`P=(15+2(L−1))×SPELL_POWER×ICE_SPELL_POWER×POWER_MULTIPLIER`; dano armazenado **`D=.25P×F` HP**, onde F=1.5 se mainhand tem tag FROZEN_WEAPONS, senão1. Não soma W. Tag source inclui Ice Spear, Snowgrave e Boreal Blade, com replace=false; datapacks podem alterar. [Fórmula/spawn][cast], [tag][frozen], [power][host-power].

| L default | Mana neutra | P neutro | D sem tag / com tag (HP tentados) |
|---|---|---|---|
| 1 | 55 | 15 | 3.75 / 5.625 |
| 2 | 60 | 17 | 4.25 / 6.375 |
| 3 | 65 | 19 | 4.75 / 7.125 |
| 4 | 70 | 21 | 5.25 / 7.875 |
| 5 | 75 | 23 | 5.75 / 8.625 |
| 6 | 80 | 25 | 6.25 / 9.375 |
| 7 | 85 | 27 | 6.75 / 10.125 |
| 8 | 90 | 29 | 7.25 / 10.875 |

1. **Cast/custo:** LONG20ticks/1s base; host efetivo `round(20×(2−softCap(CAST_TIME_REDUCTION)))`. Mana `int((55+5(L−1))×MANA_MULTIPLIER)`; cooldown default25s/500ticks; recast local0. `#onCast` cria1 GlacialEdge(owner=caster), posição `casterPos+(0,eyeHeight−.5×bulletHeight,0)`, chama shootFromRotation com speed1/variance1 e depois grava D snapshot e solicita spawn. Spawn result ignorado. [Defaults][spell], [cast][cast], [ctor/speed][projectile].
2. **Geometria/voo:** registry5×1blocks/tracking64; noGravity=true, `getSpeed=1` como argumento de lançamento, travel soma delta à posição. Se gravity reativada, override reduz Y em .05000000074505806 por tick. VFX lateralradius4 não altera a hitbox. Host ray usa AABB swept.inflate(.1), interseção com inflation.3 e sorting por distância; flags homing/ricochet/pierce começam false/0/0, sem configuração local de homing. Range máximo selecionável não existe nesta spell; distância efetiva depende do vetor/lifecycle/colisões. [Registry][entity], [voo][projectile], [trail][trail], [host collision][collision].
3. **Lifecycle:** lifetimeInTicks começa200, decrementa e descarta quando≤0, mas o método continua para super.tick sem return. Host também expira age>300. Parent consumo de impact não é chamado pelo onHitEntity local; não há ledger local de vítimas nem descarte normal de impactoEntity explicitado. Repetição em ticks/colisões e criação de campos precisa QA; pierce0 não demonstra um único hit total. ImpactBlock chama super e discard. [Tick][projectile], [callbacks][impact], [host][host-projectile], [consumo de impacto][host-impact].
4. **Dano/status:** `GlacialEdge#onHitEntity` chama super, tenta helper com D e fonte da spell(owner, direta=projétil), depois solicita **Chilled100ticks/amp1** em Living **mesmo se dano falhou/cancelou**. Não possui guarda server própria nesse override; execução física e side guards precisam QA. Fonte SpellDamageSource Ice (`irons_spellbooks:ice_magic`) declara freezeTicks80; listener Post host, se canFreeze, soma160 ao acumulador ticksFrozen. Isso é distinto de Chilled e não garante80ticks de imobilização. [Impacto][impact], [fonte][cast], [escola][school], [helper/procs][helper].
5. **FrostField filho:** cada onHit chama super e tenta criar campo somente no servidor, em ground-adjusted hitLocation (helper2). Owner=owner do projétil, duration100ticks, radius6, circular=true. Host efetivo é12×1.2blocks; query Living, distância²3D<36, filtros owner/allies e ground-context do AoeEntity. FrostField reapplicationDelay1 e applyEffect tenta `Utils.addFreezeTicks(target,10)` quando não friendly; helper limita a `ticksRequiredToFreeze×5`. Não há dano próprio no applyEffect. Nominalmente consulta a cada tick ativo; refresh/empilhamento, alvos e quantidade de campos continuam físicos. [Campo spawn][field], [FrostField][frost-field], [Aoe][aoe-hit], [cap freeze][freeze-util].
6. **Túmulo/antiMagic/save:** entombEntity existe, porém **sua chamada está comentada**; não documentar IceTomb como efeito ativo. onAntiMagic local só emite fog, sem chamar super nem descartar. NBT é herdado (Damage/Age/homing/ricochet/pierce), sem salvar lifetimeInTicks local; shouldBeSaved host exclui remoção UNLOADED_TO_CHUNK. Nada disso prova retomada/cleanup seguro. [Código não chamado/antiMagic][inactive], [NBT/antiMagic host][host-state].

## Matriz de alteração por perks

| Eixo | Valor / consumer / fase | Boundary real e limite | QA |
|---|---|---|---|
| Dano / power / tag | .25P×(1 ou1.5), snapshot pré-spawn. [Cast][cast], [tag][frozen]. | SPELL_POWER/ICE_SPELL_POWER **NATIVE_ATTRIBUTE**, POWER_MULTIPLIER **CONFIG_NATIVE**; helper Living permite SpellDamageEvent amount/cancel **HOOK_VERIFICADO**, adapter **CONDITIONAL**. Tag é global, não toggle por jogador; crítico local N/A. | Q1/Q2 |
| Tipo / freeze / Chilled | IceSpellSource freeze80→Post accumulator+160 se canFreeze; Chilled100/amp1 após tentativa. [Impact][impact], [host][helper]. | Amount não altera DamageType/status duration. Source setters por objeto existem, seam DTE pré-source não demonstrado; conversão/freeze/Chilled por perk **⛔ SEM_HOOK_SEGURO** até adapter. | Q2/Q3 |
| Alcance / targeting / filtros | Projétil direcionado por rotação, host swept ray; sem ray de aquisição local. Owner/aliados filtrados no host. [Cast][cast], [collision][collision]. | Sem resolver mutável pré-spawn ou range independentemente validado. Retarget/count/single→AOE **⛔ SEM_HOOK_SEGURO**. | Q2/Q4 |
| Hitbox / velocidade / pierce |5×1, speed argument1/variance1, noGravity; lifetime local200 versus host300. [Entity][entity], [projectile][projectile]. | setDamage(float) real; getSpeed não é setter. Homing/pierce herdados são superfícies por instância, sem callback terceiro universal; resize/speed/pierce **CONTRATO_CONDICIONAL / ⛔ fail-closed** até verificar consumo/cleanup. | Q2/Q4 |
| Área derivada / budgets | FrostField r6/duration100/reapplication1, dimensão12×1.2 e distância3D; mais de um campo por trajetória é possível sem ledger local. [Field][field], [host][frost-field]. | AoeEntity setters radius/duration são reais; não provam hook DTE de spawn/cap de campos. Resize/cadência/targetcap **⛔ SEM_HOOK_SEGURO** sem adapter e orçamento. | Q3/Q4 |
| Cast / mana / cooldown | LONG20 base, mana55+5(L−1) antes de config, cooldown25s, recast0 local. [Defaults][spell], [host][host-power]. | CTR/cooldown atributos e config **NATIVE_ATTRIBUTE / CONFIG_NATIVE**; cast mana/level e cooldownPre events **HOOK_VERIFICADO** genérico no [contrato comum](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md), adapter **CONDITIONAL**. | Q1/Q4 |
| Summons / mundo | Não é summonAI; túmulo não chamado; campo não modifica blocos no consumer lido. [Inactive][inactive], [FrostField][frost-field]. | Slots/AI/custo summon **N/A**; claims/PvP/WorldEffectPolicy não são comprovados pelo spell ser Ice. Não criar túmulo paralelo por perk. | Q2/Q4 |
| Saída / persistência / antiMagic | ImpactBlock descarta, antiMagic local VFX apenas, lifetime local não salvo e parent NBT/age separados. [Impact][impact], [inactive][inactive], [host][host-state]. | Cleanup/unload/restart/side/sync **CONTRATO_CONDICIONAL**; não tratar evento de antiMagic como prova de remoção. | Q3/Q4 |

## Ownership, concepção e pendências

DTE/Iron’s mantêm projétil, custo, Chilled/freeze e campo; RPG progressão/Mastery, BA runtime/world safety e Enshrouded sua classificação/Shroud. Dedup cast→projétil→impacto→campo→freeze; VFX e cada tick de FrostField não são novos casts. Assinatura ocupada: slash Ice viajante com bônus por tag de arma, Chilled, freeze e campo persistente curto. Nova magia precisa orçamento e contrato próprios; túmulo comentado não é capacidade disponível.

- **Q1:** config/origens/Survival, L1–8/power/tag/datapack, mana, cast20/CTR/cooldown, spawnfalse.
- **Q2:** trajetória/variance/carrier motion/hitbox, block/entity/shield/impact cancel, ally/PvP/claims, amount0/cancel/resist/hurtfalse com Chilled, callbacks por side/repetição.
- **Q3:** freeze80 versus accumulator160, Chilled100/amp1/merge, FrostField100/r6/10tickIncrement/cap/ground e campos sobrepostos; antiMagic sóVFX.
- **Q4:** budgets, lifetime200/300/finaltick, unload/save localtimer/owner morto/restart/sync/cliente, dedup/kill credit. **Todos físicos PENDING**; sem adapter/perk/runtime novo.

[versions]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/gradle.properties#L11-L48
[host-power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L257
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L333
[helper]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L119
[weapon]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L787-L802
[source-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/SpellDamageSource.java#L24-L71
[spell]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/ice/GlacialEdgeSpell.java#L27-L67
[guide]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/assets/discerning_the_eldritch/lang/en_us.json#L185-L186
[acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L612
[cast]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/ice/GlacialEdgeSpell.java#L90-L118
[frozen]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/data/discerning_the_eldritch/tags/item/frozen_weapons.json#L1-L8
[entity]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEEntityRegistry.java#L129-L135
[projectile]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/spells/glacial_edge/GlacialEdge.java#L34-L86
[trail]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/spells/glacial_edge/GlacialEdge.java#L89-L125
[impact]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/spells/glacial_edge/GlacialEdge.java#L133-L196
[field]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/spells/glacial_edge/GlacialEdge.java#L154-L165
[inactive]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/spells/glacial_edge/GlacialEdge.java#L151-L202
[school]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/SchoolRegistry.java#L69-L77
[host-projectile]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L74-L114
[collision]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L153-L214
[host-state]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L290-L358
[frost-field]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/snowball/FrostField.java#L16-L32
[aoe-hit]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AoeEntity.java#L94-L150
[freeze-util]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L950-L955

[host-impact]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L361-L405
