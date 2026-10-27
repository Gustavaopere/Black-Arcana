# Jiangshi Invoke

**Dossiê documental — 27/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `RELEASE_BOUNDED_SOURCE`, campos binários estreitos separados; integração `CONTRATO_CONDICIONAL`; sem certificação estática; QA físico `PENDING`. **+0 identidades/+0 strict**: os três Jiangshi são filhos desta spell.

## Identidade, descrição e proveniência

ID **`iss_magicfromtheeast:jiangshi_invoke`**, escola `iss_magicfromtheeast:symmetry`; declarante `net.warphan.iss_magicfromtheeast.spells.symmetry.JiangshiInvokeSpell`; criatura `entity.mobs.jiangshi.SummonedJiangshiEntity extends JiangshiEntity implements IMagicSummon`. [Registry][registry], [spell][spell].

JAR físico histórico #346 **`iss_magicfromtheeast-1.1.5.jar`**, MC 1.21.1/NeoForge, SHA-1 `e3552ea6b7b32b843c48bf0d857237d4b7129ab0`, publisher [CF 7385201](https://www.curseforge.com/minecraft/mc-mods/magic-from-the-east/files/7385201), [prova estática de identidade](../EXACT-BINARY-SPELLS-1.1.5.md). Source oficial `WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88`; build Iron’s 3.14.8/NeoForge 21.1.187 versus pack Iron’s 3.16.3/NeoForge 21.1.250. Host source consultado `e4056af90302d37eb1739f5ff05020b020e6e252`. Pin f 2 é candidato anterior à publicação oficial de CF 7385201 em 27/12/2025 17:17:39.317 UTC, segundo a [API oficial](https://www.curseforge.com/api/v1/mods/1224162/files/7385201); cronologia e observações binárias estreitas não provam equivalência integral dos métodos. O pin 904 anterior é inadequado como baseline comum, pois Cloud Ride/Drapes mudaram antes da release. O antigo pin 13208302 também declara 1.1.5, mas possui mudanças posteriores incompatíveis com o publisher em Bone Hands, armor do Executioner e cura Jiangshi; não transportar seus parâmetros como físicos atuais. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.1.5.md). All Rights Reserved: somente fatos, paráfrases e referências, sem importar implementação/assets.

[Guia oficial][guide], parafraseado: invoca três Jiangshi combatentes para acompanhar o caster. Sem override local de crafting/loot/learning no spell examinado; segue a [elegibilidade/config host][acquisition]. Rota de scroll/config implantada/Survival **NÃO VERIFICADAS**; registro não prova obtenção.

## Parâmetros e pipeline causal

`L` é o nível entregue ao onCast. Helpers locais retornam **A=2+L** de ATTACK_DAMAGE e **H=10+5 L** de MAX_HEALTH, ignorando o argumento summoner. Portanto SPELL_POWER, Symmetry power e POWER_MULTIPLIER não alteram esses dois helpers. O spell também declara basePower 1/perLevel 1, mas não os consome para count/HP/attack/duração. No publisher consultado, `getJiangshiDamage` offsets 0–4 e `getJiangshiHealth`0–7 confirmam essas duas fórmulas; não se equiparou o restante da classe. [Helpers][stats], [defaults][spell], [host][power].

| L default | Mana neutra | HP por criatura | ATTACK_DAMAGE por criatura |
|---|---|---|---|
|1|30|15|3|
|2|40|20|4|
|3|50|25|5|
|4|60|30|6|
|5|70|35|7|
|6|80|40|8|
|7|90|45|9|

1. **Ingresso/custo:**  Common, max default 7; LONG 30 ticks base, cooldown 150 s=3000 ticks antes de modifiers. Mana `int((30+10(L−1))×MANA_MULTIPLIER)`. Wrapper jogador e admissão/eventos são host-owned: anúncio de cast precede efeito; nível novo não recalcula custo construído. [Defaults][spell], [host][cast-host].
2. **Primeiro cast:**  se não há recast ativo, cria exatamente 3 candidatos; cada constructor recebe owner e rise=true e chama setOwner **antes** do evento de replacement. Define A/H, enche HP, head-drop 0, skipXP e finalizeSpawn MOB_SUMMONED. Pede posição no ground helper com scan 10, em círculo nominal `r=1.5+.185×3=2.055blocks`, ângulos `6.281/3×i+yaw`. Não é target remoto, sem teste local de corpo livre/claims ou cap de entidades globais. [Cast][spawn], [constructor/goals][summon].
3. **Replacement/registro:**  publica SpellSummonEvent, obtém creature, solicita addFreshEntity e chama initSummon(owner, result, 12000 ticks, castData), ignorando o boolean de spawn. Constructor já vinculou o original; replacement pode deixar associação do original sem spawn. **Publisher estreito:**  getCreature 261 → CHECKCAST SummonedJiangshiEntity 264 → addFreshEntity 272/pop 275. Não aceitar LivingEntity arbitrária nesse caminho. Não prova manutenção automática de AI/stats/drops no substituto. [Spawn][spawn], [manager][manager].
4. **Recast/lifecycle:**  total 2 casts, remaining inicial 1, janela 12000 ticks=600 s=10 min; segundo cast ativo não cria outra tríade e a conclusão nativa faz unsummon. TIMEOUT usa fila do manager; COUNTERSPELL pode forceAddRecast no helper; item host pode modificar política de cooldown. Com wrapper jogador, recast ativo não debita mana novamente. Duration do manager e recast são estados distintos; setDuration adiciona expiração, não substitui necessariamente outra. [Recast/callback][recast-local], [constructor][recast], [host][recasts], [manager][manager].
5. **AI/hit:**  goals próprios copiam/protegem o owner; follow tem speed 0.6, start 15/stop 5, teleport argument 30. ATTACK_DAMAGE é lido no melee via Utils.doMeleeAttack, que aplica enchantment, helper e knockback/pós-hit condicionados ao retorno. Fonte=Jiangshi spell, entidade direta Jiangshi, causing=summoner. Host helper Living+SpellDamageSource publica SpellDamageEvent, aplica resistência/friendly e hurt. Incoming host detecta IMagicSummon e multiplica por SUMMON_DAMAGE do owner Living; não é multiplicador de HP/count nem outro cast. [AI][summon], [melee][summon-hit], [helper][melee-host], [settlement][damage-host], [boost][summon-boost].
6. **Cura pós-hit:**  JiangshiAttackGoal testa range=`ENTITY_INTERACTION_RANGE×scale` e LOS no hitframe. Só doHurtTarget=true entra no ramo de cura. Com summoner ServerPlayer e RustedCoinsSword equipado cura o próprio Jiangshi por 0.5 ×ATTACK_DAMAGE; nesse mesmo ramo ServerPlayer, sem o Curio, não há else de cura. Fora do ramo ServerPlayer cura 0.25 ×ATTACK_DAMAGE. Não usa HP realmente perdido, não cura caster e não publica SpellHealEvent nesse trecho. Movimento de lunge antecede o gate de distância/LOS. [Goal][attack-goal], [range host][melee-range].
7. **Saída/estado:**  tipo registrado 0.6 × 1.8 blocks/tracking 64; stats-base não substituídos incluem armor 4, speed 0.3, step 3, kb-resist 0.7, safeFall 7, interactionRange 1.8. Rise usa contador 45, predecremento até<0 e não chama super.tick enquanto ativo; não inferir idade global congelada. Não possui save/load local do rise timer/cast token; entidades/atributos e manager têm persistence própria. onRemovedHelper só limpa mapas/fila em reason.shouldDestroy, não todo unload. [Tipo][entity], [stats/goals][summon], [rise][rise], [lifecycle][lifecycle], [save host][manager-save].

## Matriz de alteração por perks

| Eixo | Valor / consumidor / fase | Boundary e limite | QA |
|---|---|---|---|
| Nível / stats / dano | L 1–7 default; A=2+L, H=10+5 L no spawn, sem P; melee lê atributo atual. [Stats][stats]. | Evento de nível host existe, adapter CONDITIONAL; SPELL_POWER não altera helpers. ATTACK_DAMAGE/MAX_HEALTH por instância são atributos reais, mas não callback terceiro seguro pré-spawn. |Q1/Q2|
| Dano / tipo / owner | Symmetry SpellDamageSource direta=summon/causing=owner; helper+SUMMON_DAMAGE incoming. [Hit][summon-hit], [boost][summon-boost]. | Amount/cancel via SpellDamageEvent **HOOK_VERIFICADO** pré-resistência/hurt. SUMMON_DAMAGE **NATIVE_ATTRIBUTE** nessa fase. DamageType conversion **⛔ SEM_HOOK_SEGURO**; manter source/owner. |Q3|
| Alvo / alcance / área | Spawn circular 2.055/ground scan 10; melee range 1.8 ×scale e LOS; AI follow 15/5. [Cast][spawn], [AI][summon], [goal][attack-goal]. | Constantes/AI não são raio de spell exposto. Retarget/single→AOE/budgets **⛔ SEM_HOOK_SEGURO** sem adapter próprio. Sem max-target global demonstrado. |Q2/Q3|
| Entidades / hitbox / projétil |3 Jiangshi; 0.6 × 1.8 blocks. Não há projétil/dano AOE local nesta spell. [Tipo][entity], [spawn][spawn]. | Count/resize/AI/range setters por perk **⛔ SEM_HOOK_SEGURO**; SpellSummonEvent#setCreature tem tipo concreto e side effects de owner. Speed de navegação não equivale a velocidade de projétil. |Q2|
| Tempo / cooldown | LONG 30 base; 150 s; summon/recast 12000 ticks; rise 45 com predecremento. [Spell][spell], [rise][rise]. | Cast/cooldown host nativos conforme [comum](../SPELL-PERK-BOUNDARIES-1.1.5.md), duration local fixa. Alterar um clock não muda expiração/callback/restante de recast. |Q1/Q4|
| Mana / recast | Mana inicial 30+10(L−1), total 2; segundo cast remove nativamente. [Cast][spawn], [wrapper][cast-host]. | CONFIG_NATIVE mana e SpellOnCastEvent#setManaCost **HOOK_VERIFICADO** no wrapper; adapter CONDITIONAL. Sem segunda mana, timer ou despawn paralelo. |Q1/Q4|
| Cura / status / proteção | Cura própria 50% com owner ServerPlayer+Curio; sem Curio nesse ramo não cura; outro ramo 25%, só hit=true; rise bloqueia não-bypass, drown recusado e shouldIgnoreDamage. [Goal][attack-goal], [hurt][summon-hit]. | Não é lifesteal caster/percentual do dano final. Valores/flags sem mutador local comprovado; cura observer não permite reescrever consumer. |Q3/Q4|
| Lifecycle / persistência / mundo | Constructor owner antes do evento, init result depois; manager/recast/UUID/drops/XP; sem block mutation. [Spawn][spawn], [lifecycle][lifecycle]. | Provider controla cleanup; dedup pai→3 UUIDs→vítima/hit. Sem cap/rollback ou token persistente adicional comprovado; **CONTRATO_CONDICIONAL**. |Q4/Q5|

## Ownership e pendências

Assinatura ocupada: tríade de mortos-vivos melee com cura própria por ataque e ciclo nativo de summon/recast. Magia original com slots/budgets próprios é outro contrato; nomes/VFX não criam extensão aceita. RPG/BA não recebem autoridade sobre AI, cura, recursos ou expiração. Escolas custom/Mastery continuam condicionadas no [dossiê comum](../SPELL-PERK-BOUNDARIES-1.1.5.md); não premiar cada hit/summon/partícula como cast novo.

- **Q1:**  config/origem/aquisição, L/default versus modificado, mana admissão/débito, cast 30/redução, cooldown e reentrada.
- **Q2:**  três spawns/solo/claims/colisão, replacement compatível/incompatível, original vinculado sem spawn, addFreshEntity=false e nenhum refund garantido.
- **Q3:**  melee/LOS/range, helper veto/resist/PvP/aliados/owner, SUMMON_DAMAGE, heal 50%/25%/ausente por ramo com hit recusado e duas autorias de eventos.
- **Q4:**  recast/timeout/counterspell/unsummon, death/unload/logout/restart, rise 45 e normalização de atributos/AI.
- **Q5:**  dedicado/cliente/multiplayer/Survival/sync/persistência/dedup. **Todos PENDING**, sem adapter/runtime novo.

[registry]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTESpellRegistries.java#L24-L50
[versions]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/gradle.properties#L11-L39
[power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L257
[cast-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L347
[damage-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L64
[summon-boost]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L114-L130
[source-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L560-L565
[melee-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L475-L498
[manager]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/SummonManager.java#L79-L179
[manager-save]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/SummonManager.java#L239-L270
[lifecycle]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/mobs/IMagicSummon.java#L24-L86
[recast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/RecastInstance.java#L27-L35
[recasts]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/PlayerRecasts.java#L46-L131
[acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L612
[guide]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/resources/assets/iss_magicfromtheeast/lang/en_us.json#L22-L23
[spell]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/symmetry/JiangshiInvokeSpell.java#L38-L62
[spawn]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/symmetry/JiangshiInvokeSpell.java#L106-L143
[stats]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/symmetry/JiangshiInvokeSpell.java#L145-L151
[recast-local]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/symmetry/JiangshiInvokeSpell.java#L89-L104
[summon]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/jiangshi/SummonedJiangshiEntity.java#L24-L75
[summon-hit]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/jiangshi/SummonedJiangshiEntity.java#L78-L127
[rise]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/jiangshi/JiangshiEntity.java#L186-L213
[attack-goal]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/jiangshi/JiangshiEntity.java#L302-L365
[melee-range]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/mobs/goals/WarlockAttackGoal.java#L44-L46
[entity]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTEEntityRegistries.java#L70-L74
