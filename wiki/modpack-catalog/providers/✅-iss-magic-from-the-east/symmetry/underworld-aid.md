# Underworld Aid / Impermanence’s Verdict

**Dossiê documental — 27/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `RELEASE_BOUNDED_SOURCE / SOURCE_CAUSALITY`; integração `CONDITIONAL / CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades/+0 strict**: entidades, partes, buffs e callbacks são filhos desta spell.

## Identidade e proveniência

Provider ISS: Magic From The East, `mod_id=iss_magicfromtheeast`; spell **`iss_magicfromtheeast:underworld_aid`**, escola própria `iss_magicfromtheeast:symmetry`; declarante `net.warphan.iss_magicfromtheeast.spells.symmetry.UnderworldAidSpell`. [Registry][registry], [escola][school].

JAR de referência MC 1.21.1/NeoForge **`iss_magicfromtheeast-1.1.5.jar`**, SHA-1 `e3552ea6b7b32b843c48bf0d857237d4b7129ab0`, 1.680.780 bytes; [publisher CF7385201](https://www.curseforge.com/minecraft/mc-mods/magic-from-the-east/files/7385201), [inventário binário histórico](../EXACT-BINARY-SPELLS-1.1.5.md). Candidato oficial de source **`WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88`**, 27/12/2025, anterior ao upload publicado: lógica **`RELEASE_BOUNDED_SOURCE`**, sem equivalência integral demonstrada entre source e métodos do JAR. Data e versão iguais não provam essa equivalência. O candidato declara 1.1.5, NeoForge 21.1.187/Iron’s 3.14.8; o pack usa NeoForge 21.1.250/Iron’s 3.16.3. Os contratos do host abaixo vêm de Iron’s 3.16.3 `e4056af90302d37eb1739f5ff05020b020e6e252`, portanto sua combinação também exige teste. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.1.5.md). Defaults não fecham a config implantada. Metadata **All Rights Reserved**; MIT do template tem escopo limitado ao template. Só fatos, paráfrases e permalinks, sem importar implementação ou assets.

**Corroboração binária estreita:** `UnderworldAidSpell#getDamage` usa power; `getRadius` retorna 4, `getDuration` 80 e `getPercentBonus` divide L por 10. Isso corrobora esses campos/calls, sem fechar config efetiva, scheduler ou método completo. [Limites da evidência](../SPELL-PERK-BOUNDARIES-1.1.5.md).

[Guia oficial][guide], parafraseado: chama um campo que restringe e julga alvos conforme a vida perdida. O guia menciona teto 40% de maxHP, porém o consumidor lê config com default **20%**; não normalizar essa divergência. Spell não sobrescreve aquisição: elegibilidade escola/config/aprendizado host não prova obtenção Survival; rota específica **NÃO VERIFICADA**. [Host][acquisition], [cap][config].

## Pipeline e parâmetros

`L`=nível entregue ao onCast; `P=L×SPELL_POWER×symmetryPower×POWER_MULTIPLIER`. Defaults Rare, L 1–4, LONG, 40 ticks = 2 s base, cooldown 160 s = 3.200 ticks antes de modifiers, mana `int((180+90(L−1))×MANA_MULTIPLIER)` (180/270/360/450 neutra). D base snapshot=P, coeficiente b=L/10 (0.1–0.4), raio 4 blocks/duração 80 ticks constantes. Tempo efetivo LONG no host: `round(40×(2−softCap(CAST_TIME_REDUCTION)))` ticks. [Spell/defaults][spell], [helpers][helpers], [host][power].


Os níveis máximos acima são defaults de configuração; este `onCast` não aplica clamp local de L. As fórmulas `int(...)` usam conversão Java para inteiro (truncamento em direção a zero nos valores positivos usuais). Mudar L em evento posterior não refaz admissão, custo anterior ou estado já capturado pelo host. [AbstractSpell#getManaCost/getSpellPower/getEffectiveCastTime][power], [AbstractSpell#castSpell][cast-host].
1. **Ingresso/posição:** pré-helper 32/bbInflation15/sendFailure=false, boolean ignorado; no onCast consome posição atual de target resolvido. Sem target válido, `Utils.raycastForEntity(...,32,true,0.15)` e moveToRelativeGroundLevel(...,6). Não há revalidação local de range/LOS do target durante wind-up. [Cast][cast], [helper host][target-helper], [raycast do host][raycast-host].
2. **Spawn:**1 VerdictCircle recebe owner/circular/r 4/duration 80/damageP e **field público percentBonus=b**, depois setPos e addFreshEntity sem conferir sucesso. TargetedAreaEntity separado usa radius 4/duration 80/fade/owner=círculo e é visual. Não há refund local se um spawn falha. [Cast][cast], [visual][visual], [ordem de cobrança][cast-host].
3. **Scheduler/filtros:** host AoE em servidor, delay 0/reapplicationDelay 10; query Living sobre AABB efetiva.inflate(0,1,0), alive/pickable/não-spectator, distância 3D<4 e ground context (`onGround OU ΔY<.5`). Override local não exclui aliados; applyEffect exclui somente owner e o helper mantém friendly policy própria. Sem LOS/cap/ordenação local de alvos. [Verdict][circle], [AoE][aoe].
4. **Settlement por vítima/poll:** antes do dano, tenta Slowness 20 ticks/amp 4, Blindness 20/amp 1 e Darkness 20/amp 1, sem verificar addEffect. Recalcula `missingHP=maxHealth−health` **nesse poll**; `D0=damageSnapshot+missingHP×percentBonus`; `cap=maxHealth×IMPERMANENCE_LIMIT_PERCENT`. Se D0≥cap usa `(float)cap`, senão D0; nos defaults positivos equivale min(P+missingHP×L/10,0.2maxHP). Não há clamp inferior próprio. Usa helper SpellDamageSource Symmetry, direta=círculo/causador=owner; status já foi pedido mesmo se damage=false. Não são 4 explosões distintas do guia. [Terminal][circle], [config][config], [helper][damage].
5. **Geometria e clocks:** registry7×0.5 blocks versus getDimensions herdado 2r×1.2=8×1.2 em r 4; refreshDimensions local vazio. Query depende da **AABB efetiva**, não de equivalência presumida desses números. Além de duration herdado 80, field static público `onWorldTick=80` faz discard quando `tickCount>80` **antes de chamar super.tick mesmo assim**. Aumentar setDuration isoladamente não remove esse outro limite. Nominal polls 10..80; físico/primeiro-último tick e comportamento de entidade já removida exigem QA. [Entidade][entity-reg], [tick][circle], [host][aoe-state].
6. **Saída:** antiMagic descarta; shouldBeSaved=false. percentBonus não possui save/sync próprio demonstrado. Debuffs20 podem sobreviver ao campo até expirar/merge; sem rollback ou remoção deles no discard observado. [Circle][circle].

## Matriz para perks

| Eixo | Valor e consumidor | Superfície real, fase e limite | QA |
| --- | --- | --- | --- |
| Power/dano/cap | P snapshot; D0=P+missingHP atual×b, limitado a maxHP×c em applyEffect. [Helpers][helpers], [terminal][circle]. | SPELL_POWER/symmetry_spell_power **NATIVE_ATTRIBUTE**, POWER_MULTIPLIER **CONFIG_NATIVE**; SpellDamageEvent#setAmount/cancel no helper é pré-resist/hurt, mas **depois do cap local**. Adapter **CONDITIONAL**; não executar bônus de execute novamente. | Q1/Q3 |
| Config/coeficiente | b=L/10 field público por instância; c default.2, config SERVER Spells.impermanencePercentLimit/worldRestart. [Cast][cast], [config][config], [registro SERVER][config-server]. | c **CONFIG_NATIVE global**, não perk por alvo. Field b não é evento terceiro de spawn nem contrato seguro pós-poll; **CONTRATO_CONDICIONAL**. Não usar40% do guia como valor implantado. | Q1/Q3 |
| Tipo/crit | Symmetry SpellDamageSource, crítico próprio N/A. [School][school], [factory][source], [terminal][circle]. | Amount não altera DamageType; conversão **⛔ SEM_HOOK_SEGURO**. Cura/heal/lifesteal próprio N/A neste método. | Q3 |
| Range/target/área | Pré32/15, fallback 32/.15/ground6; r 4∩AABB efetiva∩ground, não-owner. [Cast][cast], [AoE][aoe]. | Constantes privadas; setRadius herdado clamp0..32 tem refresh local vazio, não prova resize seguro. Resolver, área, cap de targets/retarget **⛔ SEM_HOOK_SEGURO** sem adapter específico. | Q2/Q4 |
| Projétil/summon | 1 AoE Projectile +1 visual, sem voo/AI/summon; speed/pierce/spread N/A. [Cast][cast]. | Não transplantar AbstractMagicProjectile/SummonManager; count não é API de replicação. Sem segundo campo/dano. | Q2/Q4 |
| Cast/custo/cooldown | LONG 40, mana 180+90(L−1), cooldown 160 s antes modifiers; sem recast local. [Spell][spell], [host][power]. | Inputs/eventos nativos no [comum](../SPELL-PERK-BOUNDARIES-1.1.5.md) **VERIFIED/CONDITIONAL**; não alterar Singleton para simular desconto/perk. | Q1 |
| Duração/cadência/status | Duration80 +static onWorldTick80; poll 10; três efeitos20 com amps4/1/1. [Circle][circle], [host][aoe]. | setDuration/setReapplicationDelay são superfícies herdadas por instância, mas clock static independe; alterar static afeta todas. Status20 literals sem setter de duração ligado a getEffectDuration; **CONDITIONAL / fail-closed**. | Q3/Q4 |
| Mundo/persistência | Ground placement, sem block mutation local; antiMagic/remove e noSave. [Cast][cast], [circle][circle]. | Claims/chunks/cleanup/percentBonus persistido não fechados. Não ledger/rollback/cura/execute adicional BA. | Q2/Q5 |

Ownership/dedup: cast→UUID circle→poll/vítima→status e helper; status pedido não comprova HP entregue. RPG/BA não recalculam execute ou marcam cada poll como cast/Mastery; escola custom exige o contrato do [comum](../SPELL-PERK-BOUNDARIES-1.1.5.md). Assinatura ocupada: campo de controle com escalonamento por missingHP e teto maxHP. Uma nova magia original requer cap/autoridade próprios.

- **Q1:** config c/default 20 versus guia40, origem/Survival/mana/cooldown/tempo/L 1–4 e snapshots alterados.
- **Q2:** alvo em movimento, fallback/ground/LOS, AABB real versus r 4/visual, verticalidade/aliados/PvP/claims/chunks e budget.
- **Q3:** missingHP por poll, cap/float/resistência/setAmount depois do cap, hurtfalse mas status, target fullHP/overheal e efeitos recusados/mesclados.
- **Q4:** polls 10..80/tickCount>80 e super após discard, duration alterado sem static, overlap/antiMagic e debuffs residuais.
- **Q5:** dedicado/cliente/multiplayer/sync/unload/restart/noSave, autoria/dedup/Mastery. **Todos PENDING**, nenhum runtime/adapter novo.

[versions]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/gradle.properties#L11-L36
[registry]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTESpellRegistries.java#L24-L50
[school]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTESchoolRegistries.java#L32-L54
[power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L257
[cast-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L332
[acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L612
[guide]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/resources/assets/iss_magicfromtheeast/lang/en_us.json#L24-L25
[spell]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/symmetry/UnderworldAidSpell.java#L42-L69
[cast]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/symmetry/UnderworldAidSpell.java#L81-L122
[helpers]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/symmetry/UnderworldAidSpell.java#L124-L135
[circle]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/verdict_circle/VerdictCircle.java#L30-L101
[entity-reg]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTEEntityRegistries.java#L75-L79
[config]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/configs/MFTEServerConfigs.java#L16-L24
[target-helper]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L665-L710
[aoe]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AoeEntity.java#L21-L149
[aoe-state]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AoeEntity.java#L222-L327
[damage]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L64
[source]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L560-L566
[visual]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/target_area/TargetedAreaEntity.java#L68-L108

[raycast-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L316-L354

[config-server]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/ISS_MagicFromTheEast.java#L48-L51
