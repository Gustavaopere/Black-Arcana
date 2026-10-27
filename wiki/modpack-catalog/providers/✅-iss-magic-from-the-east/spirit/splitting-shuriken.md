# Splitting Shuriken

**Dossiê documental — 27/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT` **somente no registry**; lógica `RELEASE_BOUNDED_SOURCE`; integração `CONDITIONAL`; QA físico `PENDING`. **+0 identidades / +0 strict**: projéteis, proxies, efeitos e impactos são filhos da spell. Nenhuma equivalência integral de métodos nem integração jogável é certificada.

## Identidade, proveniência e ingresso

Provider ISS: Magic From The East, `mod_id=iss_magicfromtheeast`; spell **`iss_magicfromtheeast:splitting_shuriken`**, escola default **`iss_magicfromtheeast:spirit`**. Declarante `net.warphan.iss_magicfromtheeast.spells.spirit.SplittingShurikenSpell`. [Registro][registry], [escola][school].

JAR histórico **`iss_magicfromtheeast-1.1.5.jar`**, MC 1.21.1/NeoForge, publisher [CF7385201](https://www.curseforge.com/minecraft/mc-mods/magic-from-the-east/files/7385201), 1.680.780 bytes, SHA-1 `e3552ea6b7b32b843c48bf0d857237d4b7129ab0`; [identidade binária](../EXACT-BINARY-SPELLS-1.1.5.md). A lógica abaixo é **`RELEASE_BOUNDED_SOURCE`** do candidato oficial **`WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88`**. Esse commit de 27/12/2025, 16:35 UTC, antecede o upload de 17:17 UTC; data e versão 1.1.5 restringem a proveniência, **não provam equivalência integral de métodos com o JAR**. A inspeção `javap` abaixo confirma somente os literais/chamadas declarados, sem certificado de equivalência nem aceite físico.

Build do candidato: **NeoForge 21.1.187 / Iron’s 3.14.8**; pack: **NeoForge 21.1.250 / Iron’s 3.16.3**. O host consultado é `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`; seus contratos abaixo são condicionais à composição real do pack. Defaults não são configuração implantada. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.1.5.md). Metadata **All Rights Reserved**; MIT do template é limitada aos arquivos do template. Apenas fatos, paráfrases e permalinks, sem importar código ou assets.

Esta classe não sobrescreve aquisição, aprendizado ou resolver de pre-cast. A escola usa constructor host com requiresLearning=false/allowLooting=true; crafting ainda depende da config e origem/admissão do host. Isso é elegibilidade, sem garantir scroll/rota Survival. [Spell][spell], [constructor escolar][school-constructor], [aquisição host][acquisition-host].

[Guia][guide], parafraseado: um projétil que se divide em outros menores após contato de entidade, com metade do dano armazenado. A divisão ocorre no hit, não como shotgun no cast ou ao acertar bloco.

## Localizadores e unidades

`L` é o nível recebido pelo executor; `P` usa os fatores host `SPELL_POWER × SpiritPower × POWER_MULTIPLIER`. Multiplicadores 1 definem o cenário neutro, sem afirmar configuração implantada. Dano é expresso em HP pedidos; 20 ticks correspondem a 1 s nominal, distâncias a blocks e velocidades a blocks/tick. Não confundir tentativa do helper, retorno de `hurt` e perda final de HP. [Escala, mana e tempo host][power].

| Campo | Classe e métodos concretos / autoridade |
| --- | --- |
| Defaults e escala | `SplittingShurikenSpell#<init>/getDefaultConfig/getCastType/getUniqueInfo`; `AbstractSpell#getManaCost/getSpellPower`. [Spell][spell], [host][power]. |
| Emissão e contagem | `SplittingShurikenSpell#onCast`, `SplittingShurikenProjectile#setIsPrimary/setSplitCount`. [Spawn][spawn], [dados][data]. |
| Trajetória, hit e divisão | `SplittingShurikenProjectile#<init>/getSpeed/onHitEntity/onHitBlock`; `AbstractMagicProjectile#shoot/handleHitDetection`. [Dados][data], [velocidade/bloco][block], [divisão][split], [host][projectile-hit], [lançamento][projectile-shoot]. |
| Estado e saída | `SplittingShurikenProjectile#defineSynchedData`; herda `AbstractMagicProjectile#tick/onAntiMagic/readAdditionalSaveData/addAdditionalSaveData`. [Dados][data], [lifecycle][projectile-host], [estado][projectile-state]. |

## Fórmulas e sequência causal

`P=(4+(L−1))×SPELL_POWER×SpiritPower×POWER_MULTIPLIER`. Defaults L 1–10: mana 15–42, D primário=P 4–13 health points, count de filhos `N=L+2`=3–12, D de cada filho=P/2=2–6.5 antes de alterações posteriores no campo damage. Não são 3–12 novas spells. [Spell][spell], [power][power].

1. **Cast/custo:** INSTANT 0 ticks, cooldown 3 s=60 ticks antes de modifiers; mana `int((15+3(L−1))×MANA_MULTIPLIER)`. Sem charge/recast local. onCast cria 1 SplittingShurikenProjectile, marca IS_PRIMARY=true, grava splitCount=L+2/D=P, posição `caster.position+(0,eyeHeight−height/2,0)`, shoot(lookAngle), pede addFreshEntity e ignora boolean. [Spawn][spawn], [wrapper][cast-host].
2. **Primário/colisão:** tipo `iss_magicfromtheeast:spirit_shuriken` registrado 0.3×0.3 blocks; noGravity. getSpeed=1.5, host shoot aplica esse fator ao vetor de olhar. Usa hitDetection host: swept AABB.inflate 0.1 e interseção 0.3, owner/aliados/Minecraft filtrados, ordenação por distância e ProjectileImpactEvent de entidade antes de onHit. Isso não é raio de explosão. [Entity][entity], [constructor/data][data], [host][projectile-hit].
3. **Entity hit:** onHitEntity chama super, tenta helper com **getDamage atual**, fonte SplittingShuriken direta=projétil/causador=getOwner atual; depois, **independente do boolean do dano**, testa isPrimary && owner instanceof LivingEntity && splitCount>0. Assim SpellDamageEvent cancelado/amount reduzido não cancela sozinho a divisão nem muda o damage armazenado dos filhos. Cancelar o evento de impacto upstream pode impedir todo callback naquele caminho. O parent pode despachar `onHitBlock` para ShieldPart/AbstractShieldEntity e descartar o projétil; sem guarda local `isRemoved` após `super.onHitEntity`, o restante do método ainda pode tentar dano e divisão. [Hit/split][split], [helper][damage-host].
4. **Filhos:** N=splitCount, offset angular=`360/N` por divisão inteira. Laço cria N shuriken com owner Living atual, D=getDamage()/2, setDeltaMovement do vetor(0,0,1) rotacionado 1° em X e offset×i em Y; **não chama shoot/getSpeed** nos filhos. Módulo inicial nominal 1 block/tick, distinto de 1.5 do primário; sem aceleração local. Ângulos não cobrem 360° com espaçamento exato quando N não divide 360. Posição de todos é hitResult.location, não necessariamente centro/posição da vítima. addFreshEntity retorna boolean ignorado; sem refund/segunda mana. [Split][split].
5. **Término:** filhos não recebem setIsPrimary, ficando false e splitCount 0 pelo caminho normal, sem cascata recursiva. Pai descarta após tentativa/split; onHitBlock chama super e descarta, sem dividir. Não há ledger local de vítimas entre os vários filhos ou target cap global; vários filhos podem tentar a mesma vítima, sujeito ao host/iFrames/listeners. [Data][data], [impactos][split], [bloco][block].
6. **Lifecycle/persistência:** herda expiry > 300 ticks, checkDespawn por chunk e antiMagic. IS_PRIMARY é sincronizado, splitCount é field público com setter sem clamp; classe não salva ambos em NBT. Host salva Damage/Age/homing/pierce, não a condição primária/count MFTE: não garantir retomada de split após load. Factory/reload/cliente e eventos de impacto sem guarda local no onHitEntity requerem QA. [Data][data], [state][projectile-state], [base][projectile-host].

**Inspeção binária estreita:** no publisher SHA-1 citado, `SplittingShurikenProjectile#onHitEntity` faz `applyDamage`/descarta retorno (45/48), divisão inteira `360/count` (90–95), rotação X pelo literal 0.017453292 (122–124), dano dividido por 2 (164–166) e `setDeltaMovement` no filho (173), sem chamar `shoot` nesse trecho. Confirma apenas esses campos/chamadas; não equivale à classe inteira, ao host 3.16.3 ou ao resultado físico. [Divisão no candidato][split].

**N/A comprovados:** `SplittingShurikenSpell#onCast`/`SplittingShurikenProjectile#onHitEntity` não aplicam cura, DoT, buff, teleporte, ritual, mutação de blocos, summon slots ou AI. Não há range ofensivo fixo ou cap global de vítimas; tracking 64 é sincronização. Homing, pierce e ricochet herdados não são configurados neste executor; não há aceleração local. [Spawn][spawn], [divisão][split], [host][projectile-host].

## Matriz para perks

**Leitura de mutabilidade:** `NATIVE_ATTRIBUTE` = atributo consumido no caminho indicado; `CONFIG_NATIVE` = configuração global; `HOOK_VERIFICADO` = campo realmente mutável no evento host citado; `CONDITIONAL` = adapter ainda não implementado/validado; `⛔ SEM_HOOK_SEGURO` = alteração sem seam específico demonstrado. Os hooks gerais de cast/dano não expõem alvo, geometria, tipo ou contagem automaticamente; ver [contrato comum](../SPELL-PERK-BOUNDARIES-1.1.5.md).

| Eixo | Valor, consumer e fase | Superfície real / limite | QA |
| --- | --- | --- | --- |
| Dano/power | D parent=P; D child=getDamage(parent)/2 no hit, não metade do amount final/HP. [Spell][spell], [split][split]. | SPELL_POWER/spirit_spell_power **NATIVE_ATTRIBUTE**, POWER_MULTIPLIER **CONFIG_NATIVE global**; helper Living SpellDamageEvent#setAmount/cancel **HOOK_VERIFICADO** por tentativa, adapter parent/child/owner **CONDITIONAL**. | Q1/Q3 |
| Tipo/crítico | Todas fontes continuam SplittingShuriken/spirit_magic; causador=getOwner atual. [Fonte][source], [factory][source-type], [escola][school]. | Amount não muda DamageType/spell identity. Conversão/crítico/reownership **⛔ SEM_HOOK_SEGURO** sem contrato de descendentes e atribuição. | Q3 |
| Target/área | Sem seleção de alvo remoto; hit primário dispara radial N na posição do impacto. [Spawn][spawn], [split][split]. | Não é área esférica/dano instantâneo a N targets. Retarget/single→AOE/LOS/filter alterações **⛔ SEM_HOOK_SEGURO**. ProjectileImpactEvent cancela callback, não é setter de resolver. | Q2/Q3 |
| Projétil/count/speed | 1 pai → N = L + 2 filhos condicionados; 0.3×0.3; pai 1.5, filhos módulo 1; offset 360/N inteiro. [Data][data], [split][split], [entity][entity]. | setSplitCount(int), setIsPrimary() e setDamage(float) são públicos por instância, sem hook terceiro pré-impacto fechado. Sem clamp em setter; N normal 3–12 não é cap universal. Resize/spread/speed/count independente **CONDITIONAL / ⛔ fail-closed**. | Q2/Q4 |
| Tempo/cooldown | INSTANT 0 ticks, 3 s default; vida host > 300, bloco/entity descartam localmente. [Spell][spell], [base][projectile-host]. | Cooldown config/atributo/evento no [comum](../SPELL-PERK-BOUNDARIES-1.1.5.md) não muda lifetime/callbacks. Nenhum timer local de DOT/charge. | Q1/Q4 |
| Mana/recast | `int((15+3(L−1))×config)` por cast inicial, sem recast ou pagamento por filho. [Power][power], [wrapper][cast-host]. | setManaCost/setSpellLevel reais no wrapper; nível novo não recalcula admissão/custo já criado. Sem segunda cobrança/spawn de fallback. | Q1 |
| Status/mundo/summons | Sem heal/DOT/status/block mutation/AI/slots próprios. [Hit][split], [bloco][block]. | Não creditar dano/XP por emitir filho, partículas ou tentativa cancelada. Summon systems **N/A**; não transplantar SummonManager. | Q3 |
| Sync/persistência/dedup | IS_PRIMARY synced; splitCount não synced/salvo pela classe; Damage/Age host. [Data][data], [state][projectile-state]. | Correlacionar cast→pai→UUID do filho→vítima; sem cast-token nativo completo provado. Load/reflect/ownerless/cancelamento e Mastery custom **PENDING/CONDITIONAL** no [comum](../SPELL-PERK-BOUNDARIES-1.1.5.md). | Q4/Q5 |

Assinatura ocupada: projétil primário com divisão radial condicionada a entity hit, dano armazenado reduzido e filhos sem recursão pelo flag normal. Nova magia original deve definir gatilho, orçamento e persistência sem duplicar cada child como spell independente.

- **Q1:** config/origens/Survival, L/power/mana/cooldown, spawn recusado e mutação de nível/custo nos eventos.
- **Q2:** primário/filhos, 0.3 box versus swept 0.3, speed 1.5/1, ângulos N=3..12/nondivisors, alvo inicial/owner/aliados/PvP/claims, paredes e targets concorrentes.
- **Q3:** impacto vetado versus dano vetado, campo parent versus amount/HP, owner living/ownerless/refletido, mesma vítima por vários filhos/iFrames/kill credit.
- **Q4:** flag/count cliente, load/relog/restart/unload/antiMagic/expiry 300, setter N 0/negativo/extremo e budgets; não inferir split persistido.
- **Q5:** dedicado/cliente/multiplayer/Survival/sync e dedup pai-filhos. **Todos PENDING**; nenhum adapter/runtime novo.

[registry]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTESpellRegistries.java#L24-L50
[versions]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/gradle.properties#L11-L36
[power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L257
[cast-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L332
[acquisition-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L634
[school-constructor]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/SchoolType.java#L30-L44
[school]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTESchoolRegistries.java#L32-L54
[source]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L560-L565
[source-type]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/SpellDamageSource.java#L24-L51
[damage-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L64
[damage-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellDamageEvent.java#L24-L50
[guide]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/resources/assets/iss_magicfromtheeast/lang/en_us.json#L57-L58
[spell]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/SplittingShurikenSpell.java#L22-L80
[spawn]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/SplittingShurikenSpell.java#L68-L80
[entity]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTEEntityRegistries.java#L148-L152
[data]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/splitting_shuriken/SplittingShurikenProjectile.java#L33-L63
[block]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/splitting_shuriken/SplittingShurikenProjectile.java#L75-L89
[split]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/splitting_shuriken/SplittingShurikenProjectile.java#L91-L116
[projectile-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L78-L114
[projectile-hit]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L153-L213
[projectile-state]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L289-L359
[setters]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L445-L499

[projectile-shoot]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L46-L114
