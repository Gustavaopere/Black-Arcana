# Revenant of Honor

**Dossiê documental — 27/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT` somente para registry; lógica `RELEASE_BOUNDED_SOURCE`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`; sem certificação estática. **+0 identidades/+0 strict**: criaturas, ataques e efeitos são filhos desta spell.

## Identidade, proveniência e aquisição

ISS: Magic From The East **1.1.5**, ID **`iss_magicfromtheeast:revenant_of_honor`**, escola própria `iss_magicfromtheeast:spirit`; declarante `net.warphan.iss_magicfromtheeast.spells.spirit.RevenantOfHonorSpell`. [Registry][registry], [classe/defaults][spell].

JAR físico histórico #346 `iss_magicfromtheeast-1.1.5.jar`, MC 1.21.1/NeoForge, publisher [CF 7385201](https://www.curseforge.com/minecraft/mc-mods/magic-from-the-east/files/7385201), **1680780 bytes**, SHA-1 `e3552ea6b7b32b843c48bf0d857237d4b7129ab0`; [identidade binária estática](../EXACT-BINARY-SPELLS-1.1.5.md). Fonte oficial **`WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88`**, candidata limitada à release: commit 27/12/2025 16:35:34 UTC, antes da [publicação oficial](https://www.curseforge.com/api/v1/mods/1224162/files/7385201) às 17:17:39.317 UTC. Não é prova de correspondência integral source↔JAR. O pin 13208302 é posterior e diverge; 904 é anterior a mudanças presentes no publisher. Source f2 compila com Iron’s 3.14.8/Neo 21.1.187/Gecko 4.7.5.1/Curios 9.2.2; pack tem Iron’s 3.16.3/Neo 21.1.250. Host source consultado `e4056af90302d37eb1739f5ff05020b020e6e252`. [Versões][versions], [limites comuns](../SPELL-PERK-BOUNDARIES-1.1.5.md). All Rights Reserved: fatos, paráfrases e permalinks, sem importar código/assets.

[Guia oficial][guide], parafraseado: invoca um Spirit Samurai para proteger o caster. Sem override local de loot/crafting/learning nos métodos desta spell; ingresso e elegibilidade seguem [host/config][acquisition]. Rota Survival concreta, scroll instalado, config implantada e gates efetivos **NÃO VERIFICADOS**. Raridade/maxLevel abaixo são defaults, não prova de obtenção.

## Parâmetros e pipeline causal

Helpers usam L e o campo perLevel 5, ignorando summoner e getSpellPower: **A=6+3 L HP**, **H=50+12.5 L HP**, **armor=6+2 L**. Nos níveis default 1–5: A 9–21, H 62.5–112.5, armor 8–16. Valores fracionários de HP são floats; não arredondar para corações inteiros. BasePower 3/perLevel 5 declarados não tornam HP/dano sensíveis a SPELL_POWER/Spirit power/POWER_MULTIPLIER neste consumer. [Helpers][stats], [defaults][spell], [host][power-cost].

| Eixo | Default / consumer / unidade |
|---|---|
| Mana / cast |`int((80+35(L−1))×MANA_MULTIPLIER)`, 80–220 neutra; LONG 20 ticks base. [Spell][spell], [host][power-cost]. |
| Raridade / cooldown |Rare, maxLevel 5; 240 s=4800 ticks antes de modifiers. [Spell][spell]. |
| Count / placement / duração |1 candidato no targetBlock, Fluid.ANY/range 8 blocks; 12000 ticks=10 min; 2 casts totais. [Cast][spawn], [recast][recast-local]. |
| Corpo / AI |Tipo 0.85 × 2.3 blocks, tracking 64; speed 0.21, interactionRange 3.5; follow speed 1/start 12/stop 5/teleport 25. Corpo/alcance não são o rastro visual da técnica. [Tipo][entity-type], [mob][mob]. |

1. Wrapper host admite, publica evento com custo calculado e debita antes do efeito; mutar L no evento não recompõe admissão/custo. Sem recast, constrói SpiritSamuraiEntity(owner, rise=true), fixa A/armor/H, enche HP, posiciona e anuncia summon. [Cast][spawn], [host][cast-host].
2. **Ordem original/resultado:**  pede spawn do resultado do evento, mas chama finalizeSpawn no **original**, equipando SoulKatana nele; initSummon/duração/castData usam o resultado. Replacement pode nascer sem a katana ou sem os stats previamente configurados. addFreshEntity=false é ignorado; não há refund/rollback local. [Cast][spawn], [equipamento][equipment].
3. AI segue/copia/defende owner e possui attacks/combo. Melee comum lê A via Utils.doMeleeAttack, aplica enchantments e fonte Spirit direta=samurai/causadora=owner; o goal zera iFrames do alvo depois da tentativa, sem condicionar isso ao retorno flag. SpellDamageEvent só cobre a passagem Living+SpellDamageSource no helper; resistência/friendly/hurt e incoming SUMMON_DAMAGE são fases seguintes. [AI][mob], [hit][mob-hit], [goal][attack-goal], [melee][melee-host], [helper][damage-host], [incoming][summon-damage].
4. Técnica é outra resolução: no primeiro hitframe elegível usa impulso `(2.4,.5,2.4)` no vetor normalizado +Y 0.15, guarda posição e consulta **AABB.ofSize 5 × 3 × 5** no samurai naquele instante. Não é cilindro nem trajetória de dano contínuo. Filtra alive/pickable/LOS por vítima, sem cap local; helper resolve amizades. Dano=A sem enchantment do helper melee, fonte de 1 arg direta/causadora=samurai, distinta do melee comum. Incoming ainda identifica IMagicSummon e procura owner; não substituir por outro caster. hasUsedTechnique limita a área a uma execução por ação; knockback 1 no target primário depende de distância≤0.45 ×meleeRange e hasHitTechnique. [Goal][attack-goal], [reset da ação][attack-reset], [host][summon-damage].
5. Ataques comuns declaram 15 ticks/hit timestamp 10; técnica 40 ticks/timestamps 20–35, mas o goal testa primeiro isHitFrame(timer−4) e depois else-if isHitFrame(timer). Não interpretar todos os timestamps como 16 danos nem taxa fixa de DPS. Range do host=interactionRange×scale, 3.5 neutro; combos/LOS/navegação condicionam execução. Sem cura/status/block mutation locais nesses caminhos. [Animações][animations], [goal][attack-goal], [range][melee-range].
6. Rise contador 30 predecrementa até<0, bloqueia movimento/dano não-bypass no consumer local; chama super.tick antes. CounterSpell por caster diferente do owner é cancelado e tenta generic hurt de **Hmax/3**; não garantir perda final de 1/3, pois é tentativa de hurt sujeita à defesa/estado. Owner não recebe esse veto local. Antimagic pela interface pede unsummon, removendo no servidor. [Mob hit/rise][mob-hit], [CounterSpell][counter-local], [interface][summon-interface].

**Prova binária estreita:**  RevenantOfHonorSpell SHA-256 `228dee6449813564cc58801487546bc9bb52aa05d5f44a91b16ae88cd1807701`; constructor perLevel 5, helpers A 6+3 L/H 50+12.5 L/armor 6+2 L localizados. getCreature 170→CHECKCAST SpiritSamuraiEntity 173; addFreshEntity 181 usa resultado, finalizeSpawn 204 usa original, initSummon 215 usa resultado.132 fixa armor 10 e é inadequado para essa fórmula. Nenhuma equivalência integral de classe/métodos é alegada.

### Contrato nativo de summon e autoridade

O constructor da criatura chama setOwner no original antes de SpellSummonEvent. O spell configura atributos/posição no original, obtém o resultado do evento, pede addFreshEntity e executa initSummon no resultado; o boolean de spawn não condiciona o restante. Replacement não copia automaticamente atributos/AI/equipamento, nem limpa a associação prévia do original. Os CHECKCAST binários concretos limitam o tipo substituível. O evento é superfície real; adapter RPG/BA mutador permanece **CONTRATO_CONDICIONAL**, sem aceitar LivingEntity arbitrária. [Cast][spawn], [owner/expiração][manager], [evento][summon-event].

`getRecastCount=2` inclui o cast inicial: RecastInstance começa com 1 restante. Enquanto existe recast, onCast não cria novo grupo; o wrapper nativo não debita mana novamente e o término chama o callback local. O helper de summon remove os UUIDs em término manual; TIMEOUT usa a fila de expiração e COUNTERSPELL pode reinscrever recast. O item Greater Conjurer’s Talisman pode mudar a política de cooldown no timeout. A fila checa a cada 20 ticks com expiração estritamente anterior ao tick atual; duração solicitada não é promessa de remoção no exato mesmo tick. [Recast local][recast-local], [constructor][recast-host], [wrapper][cast-host], [manager][manager], [fila][manager-save].

IMagicSummon herda AntiMagicSusceptible: onAntiMagic pede onUnSummon. Remoção destrutiva passa pelo onRemovedHelper, retira owner/recast/fila; unload tem tratamento próprio. SummonManager possui serialização por UUID e duração restante em logout/server-stop/reentrada; isso não certifica persistência real, migração de dados, caps, chunk unload ou recuperação de spawn falho. [Interface][summon-interface], [persistência/fila][manager-save].

## Matriz de alteração por perks

| Eixo | Superfície real / consumer | Limite de integração | QA |
|---|---|---|---|
| A / HP / armor |Fórmulas fixadas no spawn, atributos reais lidos na execução. [Stats][stats], [hit][mob-hit]. |NATIVE_ATTRIBUTE na entidade, não SPELL_POWER; mutar instância compatível em evento exige política de HP/armor/caps. Adapter CONDITIONAL, sem copiar stats automaticamente ao replacement. |Q1/Q2|
| Amount / tipo / owner |Melee helper e área helper, fontes de 2 arg/1 arg distintas. [Hit][mob-hit], [goal][attack-goal]. |HOOK_VERIFICADO amount/cancel no SpellDamageEvent; SUMMON_DAMAGE nativo cobre IMagicSummon. ⛔ SEM_HOOK_SEGURO para DamageType/owner ou um multiplicador que reexecute técnica. |Q3|
| Range / targeting / área |Placement 8; melee 3.5 ×scale; área 5 × 3 × 5 por técnica; sem cap local de vítimas. [Cast][spawn], [goal][attack-goal]. |ENTITY_INTERACTION_RANGE nativo altera gates melee, não AABB literal. ⛔ SEM_HOOK_SEGURO para retarget/range de placement/área/número. |Q2/Q5|
| Count / corpo / movimento |1 samurai, 0.85 × 2.3; impulsos/AI, nenhum projétil. [Tipo][entity-type], [goal][attack-goal]. |Resize/count/AI sem seam de perk seguro; N/A para projectile pierce/acceleration/lifetime. Velocidade de AI não troca hitbox nem tamanho da área. |Q2|
| Tempo / mana / cooldown |LONG 20, 80+35(L−1), 240 s; 12000 ticks/2 casts. [Spell][spell], [cast][spawn]. |CONFIG_NATIVE e atributos host de cast/cooldown; evento pré-efeito não recompõe admissão. Timer summon/recast/AI são independentes. |Q1/Q4|
| Status / cura / defesa |Sem heal/DOT local; rise protege; CounterSpell tenta Hmax/3. [Hit][mob-hit], [event][counter-local]. |Não duplicar veto/retaliação; nenhuma mutação de cura/status demonstrada. Alterar MAX_HEALTH também muda tentativa CounterSpell, consumer distinto. |Q3/Q4|
| Lifecycle / equipamento / mundo |Original recebe katana, resultado recebe init; manager/UUID/cleanup. [Cast][spawn], [equipment][equipment]. |CONTRATO_CONDICIONAL; manter owner/equipamento/castData. Sem block mutation ou cap global comprovado; não adicionar summon paralelo. |Q2/Q4|

## Deduplicação e validação pendente

A autoridade de casting, recursos, grupos/UUIDs, AI, dano e cleanup é provider/host. Não recriar dano, status, heal, spawn ou despawn num listener para simular perk; escola custom/Mastery e inscrição de adapter seguem o [contrato comum](../SPELL-PERK-BOUNDARIES-1.1.5.md). Deduplicar cast pai→UUID de criatura→ataque/projétil→alvo; uma vítima, partícula ou callback não constitui outra identidade de spell.

- **Q1:**  origem/scroll/Survival/config real, níveis default e modificados, custo/admissão/pagamento, recast, cooldown e interrupção.
- **Q2:**  posição/solo/fluido/LOS/colisão/claims, count, replacement compatível/incompatível, associação original, addFreshEntity=false e ausência de refund demonstrado.
- **Q3:**  dano direto/causador/kill credit, resistência/alliances/PvP, helper veto, atributo SUMMON_DAMAGE por consumer, iFrames, cura e efeitos recusados.
- **Q4:**  morte, antimagic/Counterspell, recast/timeout, owner ausente, chunk unload, logout/relogin/restart e duração restante.
- **Q5:**  dedicado/cliente/multiplayer, escala/hitbox versus visual, AI/sync, limites de carga e dedup/progressão. **Todos PENDING**; sem execução física ou integração mutadora nova.

[registry]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTESpellRegistries.java#L24-L50
[versions]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/gradle.properties#L11-L39
[spell]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/RevenantOfHonorSpell.java#L35-L75
[spawn]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/RevenantOfHonorSpell.java#L106-L137
[stats]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/RevenantOfHonorSpell.java#L139-L149
[recast-local]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/RevenantOfHonorSpell.java#L88-L103
[guide]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/resources/assets/iss_magicfromtheeast/lang/en_us.json#L49-L50
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
[mob]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/spirit_samurai/SpiritSamuraiEntity.java#L77-L140
[mob-hit]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/spirit_samurai/SpiritSamuraiEntity.java#L234-L278
[equipment]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/spirit_samurai/SpiritSamuraiEntity.java#L148-L153
[attack-goal]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/spirit_samurai/SpiritSamuraiAttackGoal.java#L47-L126
[attack-reset]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/spirit_samurai/SpiritSamuraiAttackGoal.java#L141-L152
[animations]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/spirit_samurai/SpiritSamuraiEntity.java#L55-L67
[counter-local]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/events/MFTEServerEvent.java#L227-L237
[entity-type]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTEEntityRegistries.java#L122-L126
