# Kitsune Pack

**Dossiê documental — 27/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT` somente para registry; lógica `RELEASE_BOUNDED_SOURCE`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`; sem certificação estática. **+0 identidades/+0 strict**: criaturas, ataques e efeitos são filhos desta spell.

## Identidade, proveniência e aquisição

ISS: Magic From The East **1.1.5**, ID **`iss_magicfromtheeast:kitsune_pack`**, escola própria `iss_magicfromtheeast:spirit`; declarante `net.warphan.iss_magicfromtheeast.spells.spirit.KitsunePackSpell`. [Registry][registry], [classe/defaults][spell].

JAR físico histórico #346 `iss_magicfromtheeast-1.1.5.jar`, MC 1.21.1/NeoForge, publisher [CF 7385201](https://www.curseforge.com/minecraft/mc-mods/magic-from-the-east/files/7385201), **1680780 bytes**, SHA-1 `e3552ea6b7b32b843c48bf0d857237d4b7129ab0`; [identidade binária estática](../EXACT-BINARY-SPELLS-1.1.5.md). Fonte oficial **`WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88`**, candidata limitada à release: commit 27/12/2025 16:35:34 UTC, antes da [publicação oficial](https://www.curseforge.com/api/v1/mods/1224162/files/7385201) às 17:17:39.317 UTC. Não é prova de correspondência integral source↔JAR. O pin 13208302 é posterior e diverge; 904 é anterior a mudanças presentes no publisher. Source f2 compila com Iron’s 3.14.8/Neo 21.1.187/Gecko 4.7.5.1/Curios 9.2.2; pack tem Iron’s 3.16.3/Neo 21.1.250. Host source consultado `e4056af90302d37eb1739f5ff05020b020e6e252`. [Versões][versions], [limites comuns](../SPELL-PERK-BOUNDARIES-1.1.5.md). All Rights Reserved: fatos, paráfrases e permalinks, sem importar código/assets.

[Guia oficial][guide], parafraseado: invoca raposas espirituais que lutam pelo caster e aplicam Soulburn na mordida. Sem override local de loot/crafting/learning nos métodos desta spell; ingresso e elegibilidade seguem [host/config][acquisition]. Rota Survival concreta, scroll instalado, config implantada e gates efetivos **NÃO VERIFICADOS**. Raridade/maxLevel abaixo são defaults, não prova de obtenção.

## Parâmetros, cast e resolução

`L` é o nível recebido por onCast. Helpers ignoram summoner: **A=0.5+L/2.0 HP**, **H=10+4 L HP**, **N=1+floor(L/2)** criaturas, nos níveis positivos default 1–10. Assim A 1–5.5, H 14–50, N 1–6; divisão do count é inteira, não arredondamento para cima. `spellPowerPerLevel=4` é campo lido pelo HP, não POWER_MULTIPLIER. Apesar de basePower 0/perLevel 4 declarados, estes helpers não chamam getSpellPower: SPELL_POWER, Spirit power e config de power não alteram seus resultados. [Defaults][spell], [helpers][stats], [host][power-cost].

| Eixo | Default / consumer / unidade |
|---|---|
| Mana | `int((30+15(L−1))×MANA_MULTIPLIER)`, 30–165 neutra; conversão Java trunca para int. [Spell][spell], [host][power-cost]. |
| Cast / cooldown | LONG 20 ticks base=1 s; 180 s=3600 ticks antes de modificadores. [Spell][spell]. |
| Duração / recast |12000 ticks=600 s=10 min solicitados ao manager; 2 casts totais, segundo encerra grupo. [Cast][spawn], [recast][recast-local]. |
| Spawn |N posições em anel nominalr=1.87 blocks; ângulo 6.281/N×i+yaw; ground helper scan 10 a partir da altura dos olhos. Não é alcance remoto de ataque. [Cast][spawn]. |
| Corpo / movimento |EntityType 0.7 × 0.6 blocks, tracking 64; speed-base 0.5 e follow 0.6/15/5/teleport 25 são parâmetros de AI, não velocidade de projétil. [Tipo][entity-type], [AI][mob]. |

1. Host admite o cast, calcula o custo e publica SpellOnCastEvent antes do efeito. Nível alterado nesse evento não recompõe o custo já construído/admissão. Primeiro cast sem recast monta N SummonedKitsune com owner, A/H, HP cheio e posição; emite um evento por candidato, insere seu resultado e inicia duração/grupo. Não existe teste local de espaço livre/cap global de entidades ou rollback do custo. [Cast][spawn], [wrapper][cast-host].
2. SummonedKitsune é Fox+IMagicSummon, xpReward 0, sem item/food/leash como rota de controle. Goals atacam, saltam, seguem e copiam/protegem owner. Mordida utiliza MeleeAttackGoal e seu cooldown herdado; o handler não fixa uma taxa global de DPS. [AI/atributos][mob], [flags][mob-flags].
3. `doHurtTarget` pede Soulburn 60 ticks/amp 0 ao Living **antes** do helper, zera invulnerableTime e então chama Utils.doMeleeAttack com fonte Spirit, direta=Kitsune e causando=owner. Buff recusado, dano vetado ou miss posterior não revertem automaticamente a tentativa anterior. Atributo A não é dano final: enchantments, SpellDamageEvent/resist/friendly, hurt e SUMMON_DAMAGE do owner são fases posteriores distintas. [Hit][mob], [melee][melee-host], [helper][damage-host], [incoming][summon-damage].
4. Soulburn usa Hmax×scaling/100, defaults 5%, com ramos mínimo 1/máximo 10 HP; amp muda a cadência `20>>amp`, não a magnitude. Amp 0 é cadence 20 ticks de duração restante. Hurt usa fonte plain `soul_damage` sem caster original, fora de SpellDamageEvent; não propagar Spirit power ou SUMMON_DAMAGE da mordida ao DOT. Config SERVER global, entradas de Soulburn sem worldRestart local; config implantada não conferida. Source f2 não possui o teste de tag SOULBURN_IMMUNE adicionado em 132. [Effect][soulburn], [config][config].
5. Unsummon servidor emite partículas e remove; onRemovedHelper realiza cleanup destrutivo. Sem cura/área de dano própria, sem block mutation. Partículas a cada 10 ticks são apresentação. [Lifecycle][mob], [VFX/flags][mob-flags].

**Prova binária estreita:**  classe KitsunePackSpell SHA-256 `75ad03d07d301219fe35783eecfb8b62c6c8b6069253eda14e6bd6fac31be0d5`; constructor escreve perLevel 4 e getKitsuneHealth usa 10+4 L. Count 1+L/2 inteiro e dano 0.5+L/2 float foram inspecionados. onCast getCreature 236→CHECKCAST SummonedKitsune 239→addFreshEntity 247/pop 250→initSummon 258. JAR não contém SummonedKitsuneAlpha; o loop não cria alpha.132 mudou HP para 8+2 L e adicionou alpha; não importar esses valores. Inspeção não prova método inteiro ou gameplay.

### Contrato nativo de summon e autoridade

O constructor da criatura chama setOwner no original antes de SpellSummonEvent. O spell configura atributos/posição no original, obtém o resultado do evento, pede addFreshEntity e executa initSummon no resultado; o boolean de spawn não condiciona o restante. Replacement não copia automaticamente atributos/AI/equipamento, nem limpa a associação prévia do original. Os CHECKCAST binários concretos limitam o tipo substituível. O evento é superfície real; adapter RPG/BA mutador permanece **CONTRATO_CONDICIONAL**, sem aceitar LivingEntity arbitrária. [Cast][spawn], [owner/expiração][manager], [evento][summon-event].

`getRecastCount=2` inclui o cast inicial: RecastInstance começa com 1 restante. Enquanto existe recast, onCast não cria novo grupo; o wrapper nativo não debita mana novamente e o término chama o callback local. O helper de summon remove os UUIDs em término manual; TIMEOUT usa a fila de expiração e COUNTERSPELL pode reinscrever recast. O item Greater Conjurer’s Talisman pode mudar a política de cooldown no timeout. A fila checa a cada 20 ticks com expiração estritamente anterior ao tick atual; duração solicitada não é promessa de remoção no exato mesmo tick. [Recast local][recast-local], [constructor][recast-host], [wrapper][cast-host], [manager][manager], [fila][manager-save].

IMagicSummon herda AntiMagicSusceptible: onAntiMagic pede onUnSummon. Remoção destrutiva passa pelo onRemovedHelper, retira owner/recast/fila; unload tem tratamento próprio. SummonManager possui serialização por UUID e duração restante em logout/server-stop/reentrada; isso não certifica persistência real, migração de dados, caps, chunk unload ou recuperação de spawn falho. [Interface][summon-interface], [persistência/fila][manager-save].

## Matriz de alteração por perks

| Eixo | Superfície real / consumidor | Limite de integração | QA |
|---|---|---|---|
| Dano / HP |A/H são fórmulas de L no spawn; melee lê ATTACK_DAMAGE atual; MAX_HEALTH real. [Stats][stats], [hit][mob]. |NATIVE_ATTRIBUTE na criatura; SPELL_POWER/Spirit power não alteram helpers. Evento de summon permite observar/mutar instância compatível; adapter e recálculo HP/caps CONDITIONAL. |Q1/Q3|
| Amount / tipo / owner |Helper Living+SpellDamageSource publica amount/cancel; incoming escala summon direto. [Helper][damage-host], [incoming][summon-damage]. |HOOK_VERIFICADO de amount/cancel, sem conversão de tipo/owner. ⛔ SEM_HOOK_SEGURO para trocar DamageType ou atribuir caster ao DOT. |Q3|
| Count / alvo / área / range |N=1+floor(L/2), anel 1.87, AI/target host; mordida individual. [Cast][spawn], [AI][mob]. |Count/retarget/área/hitbox não têm setter de spell por evento; ⛔ SEM_HOOK_SEGURO para aumentar vítimas/slots fora do nível admitido. Nenhum cap global demonstrado. |Q2/Q5|
| Velocidade / projétil |Movimento Fox, salto e navegação; nenhum projétil nesta cadeia. [AI][mob]. |N/A para speed/acceleration/pierce de projétil; mudar movement attribute não redefine geometria de mordida. |Q2|
| DOT / estados / cura |Soulburn 60/amp 0 antes do dano; sem heal local. [Hit][mob], [effect][soulburn]. |CONFIG_NATIVE global de Soulburn, não bônus individual seguro. Duração/amplifier/cadence requerem consumer próprio; não duplicar DOT. |Q3|
| Tempo / custos / recast |Mana 30+15(L−1), LONG 20, cooldown 180 s; janela 12000. [Spell][spell], [cast][spawn]. |CONFIG_NATIVE/atributos de cast host e SpellOnCastEvent existem; mudança de L não recompõe custo. Duração/grupo/callback não acompanham um setter de cast-time. |Q1/Q4|
| Cleanup / persistência / mundo |Owner/UUID/grupo+manager, sem block mutation. [Mob][mob], [manager][manager-save]. |Provider mantém autoridade; invariantes de replacement/timeout/owner não homologados. ⛔ SEM_HOOK_SEGURO para novo spawn/despawn paralelo. |Q4/Q5|

## Deduplicação e validação pendente

A autoridade de casting, recursos, grupos/UUIDs, AI, dano e cleanup é provider/host. Não recriar dano, status, heal, spawn ou despawn num listener para simular perk; escola custom/Mastery e inscrição de adapter seguem o [contrato comum](../SPELL-PERK-BOUNDARIES-1.1.5.md). Deduplicar cast pai→UUID de criatura→ataque/projétil→alvo; uma vítima, partícula ou callback não constitui outra identidade de spell.

- **Q1:**  origem/scroll/Survival/config real, níveis default e modificados, custo/admissão/pagamento, recast, cooldown e interrupção.
- **Q2:**  posição/solo/fluido/LOS/colisão/claims, count, replacement compatível/incompatível, associação original, addFreshEntity=false e ausência de refund demonstrado.
- **Q3:**  dano direto/causador/kill credit, resistência/alliances/PvP, helper veto, atributo SUMMON_DAMAGE por consumer, iFrames, cura e efeitos recusados.
- **Q4:**  morte, antimagic/Counterspell, recast/timeout, owner ausente, chunk unload, logout/relogin/restart e duração restante.
- **Q5:**  dedicado/cliente/multiplayer, escala/hitbox versus visual, AI/sync, limites de carga e dedup/progressão. **Todos PENDING**; sem execução física ou integração mutadora nova.

[registry]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTESpellRegistries.java#L24-L50
[versions]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/gradle.properties#L11-L39
[spell]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/KitsunePackSpell.java#L32-L49
[spawn]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/KitsunePackSpell.java#L103-L135
[stats]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/KitsunePackSpell.java#L137-L147
[recast-local]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/KitsunePackSpell.java#L85-L100
[guide]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/resources/assets/iss_magicfromtheeast/lang/en_us.json#L47-L48
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
[mob]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/kitsune/SummonedKitsune.java#L31-L135
[mob-flags]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/kitsune/SummonedKitsune.java#L137-L163
[entity-type]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTEEntityRegistries.java#L115-L120
[soulburn]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/effects/SoulburnEffect.java#L20-L36
[config]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/configs/MFTEServerConfigs.java#L27-L33
