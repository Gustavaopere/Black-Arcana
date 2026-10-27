# Ashigaru Squad

**Dossiê documental — 27/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT` somente para registry; lógica `RELEASE_BOUNDED_SOURCE`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`; sem certificação estática. **+0 identidades/+0 strict**: criaturas, ataques e efeitos são filhos desta spell.

## Identidade, proveniência e aquisição

ISS: Magic From The East **1.1.5**, ID **`iss_magicfromtheeast:ashigaru_squad`**, escola própria `iss_magicfromtheeast:spirit`; declarante `net.warphan.iss_magicfromtheeast.spells.spirit.AshigaruSquadSpell`. [Registry][registry], [classe/defaults][spell].

JAR físico histórico #346 `iss_magicfromtheeast-1.1.5.jar`, MC 1.21.1/NeoForge, publisher [CF 7385201](https://www.curseforge.com/minecraft/mc-mods/magic-from-the-east/files/7385201), **1680780 bytes**, SHA-1 `e3552ea6b7b32b843c48bf0d857237d4b7129ab0`; [identidade binária estática](../EXACT-BINARY-SPELLS-1.1.5.md). Fonte oficial **`WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88`**, candidata limitada à release: commit 27/12/2025 16:35:34 UTC, antes da [publicação oficial](https://www.curseforge.com/api/v1/mods/1224162/files/7385201) às 17:17:39.317 UTC. Não é prova de correspondência integral source↔JAR. O pin 13208302 é posterior e diverge; 904 é anterior a mudanças presentes no publisher. Source f2 compila com Iron’s 3.14.8/Neo 21.1.187/Gecko 4.7.5.1/Curios 9.2.2; pack tem Iron’s 3.16.3/Neo 21.1.250. Host source consultado `e4056af90302d37eb1739f5ff05020b020e6e252`. [Versões][versions], [limites comuns](../SPELL-PERK-BOUNDARIES-1.1.5.md). All Rights Reserved: fatos, paráfrases e permalinks, sem importar código/assets.

[Guia oficial][guide], parafraseado: invoca um esquadrão de Spirit Ashigaru para auxiliar o caster. Sem override local de loot/crafting/learning nos métodos desta spell; ingresso e elegibilidade seguem [host/config][acquisition]. Rota Survival concreta, scroll instalado, config implantada e gates efetivos **NÃO VERIFICADOS**. Raridade/maxLevel abaixo são defaults, não prova de obtenção.

## Parâmetros e cast

Helpers ignoram summoner e getSpellPower: **A=2+floor(L/2) HP**, **H=20+3 L HP**, **armor=2+floor(L/2)**; divisão inteira ocorre antes do cast para float. Nos níveis default 1–8: A 2–6, H 23–44, armor 2–6. **N=L** candidatos; cada terceiro índice 1-based vira ranged, portanto ranged=floor(L/3), melee=L−floor(L/3): emL 8 são 2 ranged+6 melee. O campo perLevel 3 entra em H; não equivale a POWER_MULTIPLIER. SPELL_POWER/Spirit power não mudam esses helpers. [Defaults][spell], [helpers][stats], [cast][spawn], [host][power-cost].

| Eixo | Default / consumer / unidade |
|---|---|
| Mana / cast / cooldown |`int((60+20(L−1))×MANA_MULTIPLIER)`, 60–200 neutra; LONG 20 ticks; 180 s=3600 ticks antes de modifiers. Uncommon, maxLevel 8. [Spell][spell], [host][power-cost]. |
| Placement / duração |Anel nominal 1.87 blocks, ângulo 6.281/L×i+yaw, ground scan 10; 12000 ticks=10 min; 2 casts totais. Não é alcance de tiro. [Cast][spawn], [recast][recast-local]. |
| Tipo / melee range |Corpo 0.6 × 1.8 blocks, tracking 64; interactionRange 4 por default e 25 no ranged antes do evento. WarlockAttackGoal multiplica pelo scale; não é atributo FOLLOW_RANGE 24 nem alcance do placement. [Tipo][entity-type], [mob][mob], [range][melee-range]. |

1. Wrapper host admite/debita antes da execução. Primeiro cast sem recast constrói L candidatos(owner, rise=true), define modo/interactionRange, A/H/armor, HP cheio e posição. Posta evento por candidato; spawn e initSummon usam resultado, ignoram boolean de inserção. Mutar L no anúncio pré-efeito não recompõe custo/admissão já calculados. [Cast][spawn], [host][cast-host].
2. AI segue e copia/defende owner; movimento-base 0.33, follow speed 1/start 12/stop 5/teleport 25. Flags melee/range são booleanos independentes: setters só ativam, save/load pode conservar ambos; o goal prioriza ramo melee se os dois forem true. Não oferecer troca de modo como operação exclusiva/atômica comprovada. [Goals/atributos][mob], [persistência][mob-save], [flags][modes].
3. Melee: hitframe da ação 20 ticks/timestamp 13 verifica range e LOS, chama Utils.doMeleeAttack com fonte Spirit direta=Ashigaru/causadora=owner, depois zera iFrames do target mesmo que flag=false. Helper Living+SpellDamageSource aceita amount/cancel, aplica resistência/friendly e hurt; incoming identifica summon e aplica SUMMON_DAMAGE do owner Living. [Goal][attack-goal], [melee][mob-hit], [host][melee-host], [helper][damage-host], [incoming][summon-damage].
4. Ranged: ação 50 ticks/timestamp 30 cria um SpiritBulletProjectile; posiciona à frente do corpo e na altura dos olhos, shoot(lookAngle), damage=**1.5 ×A** antes de modifiers. Não há teste local de LOS/distância no ramo que efetivamente emite a bala; seleção/AI e colisão herdada são consumers adicionais. O atributo interactionRange 25 participa dos gates de AI, não garantia de 25 blocks exatos de trajetória. [Goal][attack-goal], [timing][animations].
5. Bala: constructor chama super.tick **antes** de owner/posição/dano serem atribuídos pelo caller, depois desativa gravidade. getSpeed=3 dá lançamento nominal 3 blocks/tick; corpo 0.1 × 0.1 blocks. Host expira em tickCount>300, além de chunk/despawn/colisão; o tick extra do constructor pertence à idade. Sem setter local de homing/pierce/ricochet/acceleration; blocos colidem e descartam. VFX não determina área de dano. [Projectile][bullet], [tipo][bullet-type], [host projétil][projectile-host].
6. Hit da bala chama super, usa condição local `entity!=owner || !isAlliedTo(owner)`, que isoladamente não prova filtro geral de aliados. Host canHitEntity rejeita owner/aliança bidirecional; helper também filtra. Com shooter Ashigaru e highOwner presente, fonte Spirit direta=bala/causadora=highOwner; caso contrário, causadora=Ashigaru. Ramo normal não tem IMagicSummon direto/causador: **SUMMON_DAMAGE não escala automaticamente a bala** por aquele listener. Zera iFrames e descarta; sem Soulburn/heal local. [Hit][bullet], [host][projectile-host], [helper][damage-host], [incoming][summon-damage].
7. Rise 25 predecrementa até<0 após super.tick; hurt não-bypass durante rise/shouldIgnoreDamage é recusado. Unsummon servidor remove com partículas; onRemovedHelper limpa associações em destruição. Não foi identificado veto CounterSpell específico de Ashigaru no handler f 2; caminho padrão host/IMagicSummon permanece, sem prometer imunidade. [Entidade][mob-hit], [cleanup][mob-save], [interface][summon-interface], [Counterspell host][counter-host].

**Prova binária estreita:**  AshigaruSquadSpell SHA-256 `d82808204ed8c5ad31b40e619ecf561a2fe9c7023690678ec534cce5dfbad96f`; constructor perLevel 3, HP 20+3 L e helpers A/armor 2+integer(L/2). getCreature 287→CHECKCAST SpiritAshigaruEntity 290; addFreshEntity descarta retorno.132 fixa armor 6, inadequado para o publisher. Call sites previamente inspecionados da bala usam getDamageSource(this, highOwner) ou(this, getOwner), não fonte direta=Ashigaru. Sem equivalência integral de métodos.

### Contrato nativo de summon e autoridade

O constructor da criatura chama setOwner no original antes de SpellSummonEvent. O spell configura atributos/posição no original, obtém o resultado do evento, pede addFreshEntity e executa initSummon no resultado; o boolean de spawn não condiciona o restante. Replacement não copia automaticamente atributos/AI/equipamento, nem limpa a associação prévia do original. Os CHECKCAST binários concretos limitam o tipo substituível. O evento é superfície real; adapter RPG/BA mutador permanece **CONTRATO_CONDICIONAL**, sem aceitar LivingEntity arbitrária. [Cast][spawn], [owner/expiração][manager], [evento][summon-event].

`getRecastCount=2` inclui o cast inicial: RecastInstance começa com 1 restante. Enquanto existe recast, onCast não cria novo grupo; o wrapper nativo não debita mana novamente e o término chama o callback local. O helper de summon remove os UUIDs em término manual; TIMEOUT usa a fila de expiração e COUNTERSPELL pode reinscrever recast. O item Greater Conjurer’s Talisman pode mudar a política de cooldown no timeout. A fila checa a cada 20 ticks com expiração estritamente anterior ao tick atual; duração solicitada não é promessa de remoção no exato mesmo tick. [Recast local][recast-local], [constructor][recast-host], [wrapper][cast-host], [manager][manager], [fila][manager-save].

IMagicSummon herda AntiMagicSusceptible: onAntiMagic pede onUnSummon. Remoção destrutiva passa pelo onRemovedHelper, retira owner/recast/fila; unload tem tratamento próprio. SummonManager possui serialização por UUID e duração restante em logout/server-stop/reentrada; isso não certifica persistência real, migração de dados, caps, chunk unload ou recuperação de spawn falho. [Interface][summon-interface], [persistência/fila][manager-save].

## Matriz de alteração por perks

| Eixo | Superfície real / consumidor | Limite de integração | QA |
|---|---|---|---|
| Stats / dano |A/H/armor porL; melee atributoA, bala 1.5 A snapshot. [Stats][stats], [goal][attack-goal]. |NATIVE_ATTRIBUTE na criatura, sem efeito dos power stats nos helpers. HOOK_VERIFICADO amount/cancel helper; SUMMON_DAMAGE cobre melee, não automaticamente bala normal. Adapter CONDITIONAL. |Q1/Q3|
| Tipo / owner / status |Fonte melee direta=summon, bala direta=projectile; sem DOT/heal local. [Hit][mob-hit], [bala][bullet]. |⛔ SEM_HOOK_SEGURO para converter tipo/owner ou acrescentar Soulburn; preservar crédito e iFrames. |Q3|
| Count / targeting / range |N=L, mistura floor(L/3); AI range 4/25 ×scale; spawn 1.87. [Cast][spawn], [range][melee-range]. |Atributo range é nativo, mas não controla placement/distância máxima de tiro. Count/mode/retarget sem contrato externo seguro; flags não são enum exclusivo. |Q2|
| Área / corpo / projétil |Corpo 0.6 × 1.8, bala 0.1 × 0.1; tiro por ação, no AOE local. [Tipos][entity-type], [bala][bullet-type]. |⛔ SEM_HOOK_SEGURO para resize/pierce/homing/multishot/área; não emitir segundo tiro para simular perk. |Q2/Q5|
| Velocidade / lifetime |AI 0.33, bala launch 3; host age>300; spawn 12000. [Mob][mob], [bullet][bullet], [host][projectile-host]. |MovementSpeed nativo não altera speed getter nem vida útil da bala; setter de cast-time não altera timers filhos. |Q2/Q4|
| Cast / mana / cooldown |LONG 20, 60+20(L−1), 180 s; 2 casts. [Spell][spell], [recast][recast-local]. |CONFIG_NATIVE/atributos host e anúncio real; mutarL não reabre admissão. Não cobrar cada soldado/tiro como outro cast. |Q1|
| Persistência / mundo |Flags melee/range persistidas, owner/UUID/manager; sem block mutation. [Save][mob-save], [manager][manager-save]. |CONTRATO_CONDICIONAL; preservar callbacks/sync e testar unload/modo duplo; sem cap global ou refund comprovado. |Q4/Q5|

## Deduplicação e validação pendente

A autoridade de casting, recursos, grupos/UUIDs, AI, dano e cleanup é provider/host. Não recriar dano, status, heal, spawn ou despawn num listener para simular perk; escola custom/Mastery e inscrição de adapter seguem o [contrato comum](../SPELL-PERK-BOUNDARIES-1.1.5.md). Deduplicar cast pai→UUID de criatura→ataque/projétil→alvo; uma vítima, partícula ou callback não constitui outra identidade de spell.

- **Q1:**  origem/scroll/Survival/config real, níveis default e modificados, custo/admissão/pagamento, recast, cooldown e interrupção.
- **Q2:**  posição/solo/fluido/LOS/colisão/claims, count, replacement compatível/incompatível, associação original, addFreshEntity=false e ausência de refund demonstrado.
- **Q3:**  dano direto/causador/kill credit, resistência/alliances/PvP, helper veto, atributo SUMMON_DAMAGE por consumer, iFrames, cura e efeitos recusados.
- **Q4:**  morte, antimagic/Counterspell, recast/timeout, owner ausente, chunk unload, logout/relogin/restart e duração restante.
- **Q5:**  dedicado/cliente/multiplayer, escala/hitbox versus visual, AI/sync, limites de carga e dedup/progressão. **Todos PENDING**; sem execução física ou integração mutadora nova.

[registry]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTESpellRegistries.java#L24-L50
[versions]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/gradle.properties#L11-L39
[spell]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/AshigaruSquadSpell.java#L33-L65
[spawn]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/AshigaruSquadSpell.java#L105-L143
[stats]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/AshigaruSquadSpell.java#L145-L155
[recast-local]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/AshigaruSquadSpell.java#L87-L102
[guide]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/resources/assets/iss_magicfromtheeast/lang/en_us.json#L51-L52
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
[mob]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/spirit_ashigaru/SpiritAshigaruEntity.java#L72-L122
[mob-save]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/spirit_ashigaru/SpiritAshigaruEntity.java#L125-L159
[mob-hit]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/spirit_ashigaru/SpiritAshigaruEntity.java#L277-L302
[modes]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/spirit_ashigaru/SpiritAshigaruEntity.java#L209-L231
[animations]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/spirit_ashigaru/SpiritAshigaruEntity.java#L54-L62
[attack-goal]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/spirit_ashigaru/SpiritAshigaruAttackGoal.java#L38-L112
[bullet]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spirit_bullet/SpiritBulletProjectile.java#L23-L84
[entity-type]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTEEntityRegistries.java#L128-L132
[bullet-type]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTEEntityRegistries.java#L133-L137
[projectile-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L46-L132
