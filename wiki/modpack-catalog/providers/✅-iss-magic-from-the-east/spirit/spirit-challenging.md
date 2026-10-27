# Spirit Challenging

**Dossiê documental — 27/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT` **somente no registry**; lógica `RELEASE_BOUNDED_SOURCE`; integração `CONDITIONAL`; QA físico `PENDING`. **+0 identidades / +0 strict**: projéteis, proxies, efeitos e impactos são filhos da spell. Nenhuma equivalência integral de métodos nem integração jogável é certificada.

## Identidade, proveniência e descrição

ISS: Magic From The East, mod_id `iss_magicfromtheeast`, spell **`iss_magicfromtheeast:spirit_challenging`**, escola própria `iss_magicfromtheeast:spirit`; declarante `net.warphan.iss_magicfromtheeast.spells.spirit.SpiritChallengingSpell`. [Registry][registry], [escola][school], [classe][spell].

JAR histórico **`iss_magicfromtheeast-1.1.5.jar`**, MC 1.21.1/NeoForge, publisher [CF7385201](https://www.curseforge.com/minecraft/mc-mods/magic-from-the-east/files/7385201), 1.680.780 bytes, SHA-1 `e3552ea6b7b32b843c48bf0d857237d4b7129ab0`; [identidade binária](../EXACT-BINARY-SPELLS-1.1.5.md). A lógica abaixo é **`RELEASE_BOUNDED_SOURCE`** do candidato oficial **`WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88`**. Esse commit de 27/12/2025, 16:35 UTC, antecede o upload de 17:17 UTC; data e versão 1.1.5 restringem a proveniência, **não provam equivalência integral de métodos com o JAR**. A inspeção `javap` abaixo confirma somente os literais/chamadas declarados, sem certificado de equivalência nem aceite físico.

Build do candidato: **NeoForge 21.1.187 / Iron’s 3.14.8**; pack: **NeoForge 21.1.250 / Iron’s 3.16.3**. O host consultado é `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`; seus contratos abaixo são condicionais à composição real do pack. Defaults não são configuração implantada. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.1.5.md). Metadata **All Rights Reserved**; MIT do template é limitada aos arquivos do template. Apenas fatos, paráfrases e permalinks, sem importar código ou assets.

[Guia oficial][guide], parafraseado: extrai um proxy atacável ligado ao alvo; dano e quebra do vínculo têm consequências no dono. Sem override local de aquisição, segue elegibilidade host. Obtenção/config Survival efetivas **NÃO VERIFICADAS**; Onmyoji referencia esta spell, sem provar ingresso idêntico ao jogador. [Aquisição][acquisition], [perfil NPC][mob-profile].

## Localizadores e unidades

`L` é o nível recebido pelo executor; `P` usa os fatores host `SPELL_POWER × SpiritPower × POWER_MULTIPLIER`. Multiplicadores 1 definem o cenário neutro, sem afirmar configuração implantada. Dano é expresso em HP pedidos; 20 ticks correspondem a 1 s nominal, distâncias a blocks e velocidades a blocks/tick. Não confundir tentativa do helper, retorno de `hurt` e perda final de HP. [Escala, mana e tempo host][power].

| Campo | Classe e métodos concretos / autoridade |
| --- | --- |
| Defaults, custo e escala | `SpiritChallengingSpell#<init>/getDefaultConfig/getCastType`; `AbstractSpell#getManaCost/getSpellPower`. [Spell][spell], [host][power]. |
| Seleção, gate e spawn | `SpiritChallengingSpell#checkPreCastConditions/onCast`, `Utils#preCastTargetHelper`. [Seleção][spawn], [host][target-host]. |
| Duração, vínculo e coeficiente | `SpiritChallengingSpell#getConnectionRange/getDuration/getBonusPercent`, `ExtractedSoul#setDuration/setBonusPercent/enableRadius`. [Helpers][challenge-helpers], [setters][proxy-owner], [flag][proxy-spawn]. |
| Proxy e estado | `ExtractedSoul#<init>/getDefaultDimensions/getOwner/getExtractor/tick/onUnSummon/hurt/shouldIgnoreDamage/readAdditionalSaveData/addAdditionalSaveData/onAntiMagic`. [Ctor][proxy-ctor], [owner][proxy-owner], [defesa][proxy-defense], [save][proxy-save]. |
| Forwarding e punição | `SoulChallengingEvents#linkedSoulChallengingEvent/soulOwnerHurtEvent/onSoulCrushedEvent/counterSpellCastOnSoul/punishingOwner`. [Eventos][proxy-events]. |

## Ingresso, coeficiente e lifecycle

`P=(10+10(L−1))×SPELL_POWER×SpiritPower×POWER_MULTIPLIER`; `B=min((int)P,80)/100.0`, truncamento antes do cap superior de 80%, sem clamp inferior próprio. Duração `160+40L` ticks. Defaults L 1–5: mana 65/85/105/125/145, P 10/20/30/40/50, B 10/20/30/40/50%, duração 200/240/280/320/360 ticks (10–18 s). LONG 20 ticks base, cooldown 120 s=2400 ticks, sem recast local. Mana fórmula `int((65+20(L−1))×MANA_MULTIPLIER)`. [Defaults][spell], [helpers][challenge-helpers], [host][power].

1. **Seleção:** checkPreCastConditions usa preCastTargetHelper(range 8 blocks, aimAssist 0.35), ray com blocos, Living/multipart ou passageiro de PreventDismount no host. Guarda TargetEntityCastData antes do evento de nível. onCast requer esse tipo, resolve target no ServerLevel e só então rejeita tipo na tag SPIRIT_CHALLENGING_IMMUNE (source inclui #c:bosses). Sem refund local se alvo nulo/imune após custo. Sem filtro extra local de friendly/claims/dimensão ou revalidação explícita range/LOS nesse onCast. [Target/spawn][spawn], [host target][target-host], [tag][immune].
2. **Proxy:** cria 1 ExtractedSoul(owner=alvo, extractor=caster), copia visual; MAX_HEALTH inicial recebe **vida atual** do alvo e Health=getMaxHealth. P/B não alteram essa vida. Define duração/B, posiciona em caster.position+getViewVector(5). Argumento 5 é interpolação do vetor, não distância 5; não inventar offset de 5 blocks. enableRadius ativa vínculo; cria visual de área 12 com owner=proxy e duração igual, antes de solicitar addFreshEntity(proxy) sem testar retorno. Sem SpellSummonEvent/SummonManager nessa criação. [Spawn][spawn], [constructor][proxy-ctor].
3. **Autoria/geometry:** não-player copia EntityType e dimensões desse tipo via getDefaultDimensions; para Player não grava entityToCopy e usa tipo proxy 0.6×1.8 blocks, com demais atributos/escala copiados quando disponíveis. Owner é vítima ligada, não caster. Spawn packet manda IDs owner/extractor e tipo; hasRadius é sync boolean; bonusPercent/duration são fields próprios, não comprovadamente sync completos por esse pacote. [Tipo][entity], [constructor][proxy-ctor], [spawn/sync][proxy-spawn].
4. **Forwarding Pre:** ver seção abaixo. A transferência não substitui o dano do proxy nem confirma HP entregue ao dono. Sem dano inicial desta spell e sem ataque AI; ExtractedSoul é LivingEntity/proxy, não IMagicSummon com dano escalado por SUMMON_DAMAGE. [Eventos][proxy-events], [classe][proxy-spawn].
5. **Vínculo/saída:** EntityTickEvent.Pre servidor com owner não-null e hasRadius exige distância≤12; >12 pede onUnSummon e pune owner, depois cancela tick. Caso contrário owner morto pede unsummon/cancel sem punição. Tick próprio decrementa duration só se>0 e unsummon no zero; valores≤0 não viram timeout ativo nesse método. onUnSummon descarta somente no servidor. LivingDeathEvent de qualquer ExtractedSoul com owner pune, independentemente de radius. [Eventos][proxy-events], [tempo/setters][proxy-owner].
6. **Counterspell:** handler MFTE se caster==extractor ou config PASS_CHALLENGING=true pede unsummon; caso contrário pune owner, sem cancelar CounterSpellEvent. No host 3.16.3 consultado, evento não cancelado continua para onAntiMagic→onUnSummon; portanto não afirmar que soul permanece no ramo de outro caster. Owner perdido nesse ramo não tem null guard antes da punição. Config pass default false/worldRestart é global; outros listeners/host/JAR precisam QA. [Eventos/config][proxy-events], [config][config], [host][counterspell-host], [antiMagic][proxy-save].

### Dano encaminhado, punição e persistência

SoulChallengingEvents#soulOwnerHurtEvent observa LivingDamageEvent.Pre; lê **originalDamage A**, não dano novo/final. Sendo proxy com owner: se fonte tem SOUL_HURTING (`iss_magicfromtheeast:is_soul`), solicita **A integral sem cap de vida**; demais fontes solicitam `min(A,HproxyAtual)×B` nos ramos ordinários. Cria fonte plain **soul_damage** com attacker original source.getEntity(), chama owner.hurt e ignora retorno. Não cancela/altera o dano do proxy. O helper/SpellDamageEvent/resist de escola não é chamado por esse forwarding; a nova hurt ainda tem seu pipeline NeoForge. [Consumer][proxy-events], [fase Pre][damage-pre], [tags][soul-types].

Punição solicita Soulburn 200 ticks/amp 0 + Iron’s SLOWED 200 ticks/amp 3, sem testar addEffect. Soulburn tem cálculo maxHP/cadência/config próprios; o candidato f2 e o trecho do publisher não possuem o guard posterior de tag de imunidade no `SoulburnEffect#applyEffectTick`. Outros consumers de imunidade continuam pendentes. SoulwardRing remove o buff por tick e aplica originalAmount×0.8 em incoming is_soul para ServerPlayer equipado, não redução de 80% garantida. [Eventos][proxy-events], [effect][soulburn], [ring][ring].

ExtractedSoul#hurt rejeita lado cliente/invulnerabilidade/shouldIgnoreDamage; esse último usa friendlyFireBetween(owner, proxy) sob suas condições, **não incoming attacker**. É pickable, não pushable/collidable, fireImmune, não congela; ausência de colisão física não significa invulnerabilidade geral. NBT salva ownerUUID/extractorUUID/entityToCopy/durationTimer, mas **não bonusPercent nem DATA_HAS_RADIUS**; ctor default B = 0/radius false pode divergir ao reconstruir sem outra restauração. IDs vivos/cache e lookup no level não provam consistência após unload/dimensão/restart. [Defesa][proxy-defense], [save][proxy-save], [owner][proxy-owner].

**N/A comprovados:** `SpiritChallengingSpell#onCast` não faz dano inicial, cura, projétil, ritual, teleporte da vítima ou mutação de blocos; o proxy não implementa summon AI/slots e não chama `SpellSummonEvent`. Pierce, ricochet e aceleração de projétil são N/A. A velocidade de movimento default do proxy é 0, não um range de seleção ou imunidade a deslocamento externo. [Spawn][spawn], [classe][proxy-spawn], [atributos][proxy-attributes].

## Matriz de alteração por perks

**Leitura de mutabilidade:** `NATIVE_ATTRIBUTE` = atributo consumido no caminho indicado; `CONFIG_NATIVE` = configuração global; `HOOK_VERIFICADO` = campo realmente mutável no evento host citado; `CONDITIONAL` = adapter ainda não implementado/validado; `⛔ SEM_HOOK_SEGURO` = alteração sem seam específico demonstrado. Os hooks gerais de cast/dano não expõem alvo, geometria, tipo ou contagem automaticamente; ver [contrato comum](../SPELL-PERK-BOUNDARIES-1.1.5.md).

| Eixo | Valor / consumidor / fase | Superfície e limite | QA |
| --- | --- | --- | --- |
| Power / dano | P controla B=min((int)P,80)/100.0, não HP/timer. Transferência Pre usa A original. [Helpers][challenge-helpers], [event][proxy-events]. | Atributos/config power nativos são input real. Forwarding plain não passa SpellDamageEvent; evento de dano do proxy não é setter dedicado do coeficiente/resultado ligado. Adapter CONDITIONAL. | Q1/Q3 |
| Tipo / fonte | Forwarding soul_damage/plain, causing attacker original; sem sourceSpell preservado. [Consumer][proxy-events]. | ⛔ SEM_HOOK_SEGURO para conversão elemental via amount. Não recriar hurt para manter escola/credit. | Q3 |
| Target / range | Seleção 8/aim 0.35, imune por tag no onCast; vínculo 12, origem do proxy perto caster. [Spawn][spawn], [target][target-host]. | Pre-target snapshot e nível do evento são fases distintas. Sem setter de alvo/range/radius por jogador identificado; single→multi/retarget ⛔ SEM_HOOK_SEGURO. | Q2 |
| Área / geometry | 1 proxy; dimensão de tipo copiado ou registry 0.6×1.8 para ramo Player; visual radius 12 não aplica dano AOE. [Tipo][entity], [constructor][proxy-ctor]. | setEntityTypeToCopy/enableRadius/setPos existem por instância; nenhum callback terceiro pré-spawn verificado. Resize/transporte CONDITIONAL/⛔ fail-closed. | Q2/Q4 |
| Tempo / mana | LONG 20, cooldown 120 s, duração 160+40L; mana 65+20(L−1) antes config. [Spell][spell]. | Host cast/mana/cooldown nativos no [comum](../SPELL-PERK-BOUNDARIES-1.1.5.md); setDuration público não demonstra owner/adaptação/cleanup seguro em qualquer tick. | Q1/Q4 |
| Summon / owner / cap | Living proxy sem AI/SummonManager; owner=target/extractor=caster, sem cap global local. [Ctor][proxy-ctor]. | Não herdar SUMMON_DAMAGE/timer de summons por analogia; takeover/replacement/count não tem hook real pré-spawn. | Q2/Q4 |
| Estados / counter | Punição 200/amp 0+200/amp 3; passChallenging global com worldRestart, default false. [Events][proxy-events], [config][config]. | Observer de teleporte/dano não é mutador desses statuses; CounterSpellEvent cancelável no host é boundary próprio, não simples boolean seguro de dismiss. | Q3/Q4 |
| Persistência / sync | NBT sem B/radius; spawn IDs/tipo, duration local e cache de owner. [Save][proxy-save], [sync][proxy-spawn]. | Source/JAR estreito confirma omissão dos fields nesse save; não afirmar restore coerente. Não escrever ledger paralelo para compensar. | Q4/Q5 |
| Mundo / dedup | Sem block mutation/heal/teleport local; hit do proxy→forward→owner podem gerar eventos distintos. [Events][proxy-events]. | Não premiar cada forwarding/punição como cast/Mastery. Escola custom e integração RPG condicionadas no [comum](../SPELL-PERK-BOUNDARIES-1.1.5.md). | Q3/Q5 |

Defaults/getters, setBonusPercent divide 100, forwarding e omissões NBT foram localizados estreitamente no publisher; isso não equipara todos os métodos/hosts. Assinatura ocupada: proxy temporário atacável com vínculo e punição; uma magia original requer contrato próprio de autoria, tolerância a falha e persistência.

- **Q1:** scroll/origens/config, L 1–5/B cap 80/truncamento/negativo externo, custo anunciado e target perdido/imune.
- **Q2:** range 8/radius 12/bordas/LOS/multipart, caster distante/crossdim, spawn recusado/visual órfão, Player e tipos escalados.
- **Q3:** original versus new damage, SOUL_HURTING overkill sem cap, attacker null/kill credit, owner/proxy recusando hurt, Soulburn/SLOWED/ring, ciclos e outros listeners.
- **Q4:** radius false/timeout 0/negativo/expiry/death/Counterspell outro caster/owner ausente, unload/reload e B/radius não salvos.
- **Q5:** dedicado/cliente/multiplayer/Survival/sync/relog/restart, budgets e dedup/Mastery. **Todos PENDING**; sem adapter/runtime novo.

[registry]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTESpellRegistries.java#L39-L50
[school]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTESchoolRegistries.java#L32-L54
[versions]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/gradle.properties#L11-L36
[power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L257
[cast-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L332
[acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L612
[damage-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L31-L64
[source-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L560-L565
[soulburn]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/effects/SoulburnEffect.java#L20-L37
[config]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/configs/MFTEServerConfigs.java#L20-L33
[ring]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/item/curios/SoulwardRing.java#L22-L38
[proxy-ctor]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/spirit_challenging/ExtractedSoul.java#L102-L158
[proxy-owner]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/spirit_challenging/ExtractedSoul.java#L160-L224
[proxy-defense]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/spirit_challenging/ExtractedSoul.java#L226-L293
[proxy-save]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/spirit_challenging/ExtractedSoul.java#L311-L360
[proxy-spawn]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/spirit_challenging/ExtractedSoul.java#L40-L98
[proxy-events]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/events/SoulChallengingEvents.java#L23-L95
[damage-pre]: https://github.com/neoforged/NeoForge/blob/e0e7ab5d273fdc034f23fee7bf91c61ae39d3019/src/main/java/net/neoforged/neoforge/event/entity/living/LivingDamageEvent.java#L40-L83
[counterspell-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/CounterspellSpell.java#L67-L106
[soul-types]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/datagen/MFTEDamageTypeTagGenerator.java#L29-L58
[spell]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/SpiritChallengingSpell.java#L32-L61
[spawn]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/SpiritChallengingSpell.java#L84-L134
[guide]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/resources/assets/iss_magicfromtheeast/lang/en_us.json#L41-L42
[entity]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTEEntityRegistries.java#L85-L89
[target-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L665-L710
[immune]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/resources/data/iss_magicfromtheeast/tags/entity_type/spirit_challenging_immune.json#L1-L6
[mob-profile]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/mfte_wizards/onmyoji/OnmyojiEntity.java#L51-L62

[challenge-helpers]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/SpiritChallengingSpell.java#L123-L134

[proxy-attributes]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/spirit_challenging/ExtractedSoul.java#L349-L360
