# Anchoring Kunai

**Dossiê documental — 27/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT` **somente no registry**; lógica `RELEASE_BOUNDED_SOURCE`; integração `CONDITIONAL`; QA físico `PENDING`. **+0 identidades / +0 strict**: projéteis, proxies, efeitos e impactos são filhos da spell. Nenhuma equivalência integral de métodos nem integração jogável é certificada.

## Identidade, proveniência e descrição

ISS: Magic From The East, mod_id `iss_magicfromtheeast`, spell **`iss_magicfromtheeast:anchoring_kunai`**, escola própria `iss_magicfromtheeast:spirit`; declarante `net.warphan.iss_magicfromtheeast.spells.spirit.AnchoringKunaiSpell`. [Registry][registry], [escola][school], [classe][spell].

JAR histórico **`iss_magicfromtheeast-1.1.5.jar`**, MC 1.21.1/NeoForge, publisher [CF7385201](https://www.curseforge.com/minecraft/mc-mods/magic-from-the-east/files/7385201), 1.680.780 bytes, SHA-1 `e3552ea6b7b32b843c48bf0d857237d4b7129ab0`; [identidade binária](../EXACT-BINARY-SPELLS-1.1.5.md). A lógica abaixo é **`RELEASE_BOUNDED_SOURCE`** do candidato oficial **`WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88`**. Esse commit de 27/12/2025, 16:35 UTC, antecede o upload de 17:17 UTC; data e versão 1.1.5 restringem a proveniência, **não provam equivalência integral de métodos com o JAR**. A inspeção `javap` abaixo confirma somente os literais/chamadas declarados, sem certificado de equivalência nem aceite físico.

Build do candidato: **NeoForge 21.1.187 / Iron’s 3.14.8**; pack: **NeoForge 21.1.250 / Iron’s 3.16.3**. O host consultado é `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`; seus contratos abaixo são condicionais à composição real do pack. Defaults não são configuração implantada. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.1.5.md). Metadata **All Rights Reserved**; MIT do template é limitada aos arquivos do template. Apenas fatos, paráfrases e permalinks, sem importar código ou assets.

[Guia oficial][guide], parafraseado: sequência de três kunais que marcam a vítima para deixar uma parte de sua alma quando há teleporte. Sem override local de crafting/loot; obtenção Survival/config implantada **NÃO VERIFICADAS**. Elegibilidade host não prova rota de aquisição. [Aquisição][acquisition].

## Localizadores e unidades

`L` é o nível recebido pelo executor; `P` usa os fatores host `SPELL_POWER × SpiritPower × POWER_MULTIPLIER`. Multiplicadores 1 definem o cenário neutro, sem afirmar configuração implantada. Dano é expresso em HP pedidos; 20 ticks correspondem a 1 s nominal, distâncias a blocks e velocidades a blocks/tick. Não confundir tentativa do helper, retorno de `hurt` e perda final de HP. [Escala, mana e tempo host][power].

| Campo | Classe e métodos concretos / autoridade |
| --- | --- |
| Defaults, mana, power e tooltip | `AnchoringKunaiSpell#<init>`, `#getDefaultConfig`, `#getUniqueInfo`, `#getCastType`; fórmulas herdadas `AbstractSpell#getManaCost/getSpellPower`. [Spell][spell], [host][power]. |
| Quantidade e emissão | `AnchoringKunaiSpell#getRecastCount/onCast`; `RecastInstance#<init>` e `PlayerRecasts#addRecast/decrementRecastCount`. [Emissão][emission], [recast][recasts], [constructor][recast-instance]. |
| Movimento, dano e marca | `AnchoringKunaiProjectile#<init>/getSpeed/setEffectLevel/setEffectTick/onHitEntity/onHitBlock/shouldPierceShields`. [Projétil][projectile], [impacto][impact]. |
| Trigger e coeficiente | `AnchoredSoulEffect#onEntityTeleportEvent` → `ExtractedSoul#setBonusPercent/setDuration`. [Trigger][anchor], [setters][proxy-owner]. |
| Proxy, saída e persistência | `ExtractedSoul#<init>/getDefaultDimensions/tick/onUnSummon/readAdditionalSaveData/addAdditionalSaveData/onAntiMagic`; `SoulChallengingEvents#soulOwnerHurtEvent/onSoulCrushedEvent/counterSpellCastOnSoul/punishingOwner`. [Ctor][proxy-ctor], [tempo][proxy-owner], [save][proxy-save], [eventos][proxy-events]. |

## Cast, projétil e trigger de teleporte

`P=(3+(L−1))×SPELL_POWER×SpiritPower×POWER_MULTIPLIER`; dano direto `D=P`. Mana `int((20+10(L−1))×MANA_MULTIPLIER)`, L default 1–8:20–90 mana/P 3–10. INSTANT 0 ticks, cooldown 90 s=1800 ticks antes de modifiers. getRecastCount retorna **3 total casts**; janela 100 ticks (5 s), remaining inicial 2 no host, não três adicionais. Recasts ativos não cobram mana novamente no wrapper; decremento após onCast e renovação de janela são host-owned. [Spell][spell], [emissão][emission], [recast host][recasts], [constructor][recast-instance], [wrapper][cast-host].

1. onCast cria recast se não ativo, então 1 AnchoringKunaiProjectile(owner=caster), grava effectLevel=L, chama setEffectTick(5L+10), D=P, posição caster+Y(eyeHeight−halfbulletHeight), shoot(look), solicita spawn e ignora retorno. Campo effectTick começa 20; setter **multiplica o campo pelo argumento**, logo uma chamada normal produz 20(5L+10) ticks=300–1.000 (15–50 s). Repetir setter acumula multiplicações, não reatribui segundos absolutos. [Emissão][emission], [projétil][projectile].
2. Tipo 0.5×0.5 blocks/tracking 64, noGravity, speed 1.2 blocks/tick pelo host shoot; sem homing/pierce/ricochet configurados. Colisão herda swept/inflação/filtros owner/aliados; no hit, MFTE chama super, tenta helper D com sourceSpell AnchoringKunai/direta=kunai/causador=owner, depois Living recebe tentativa ANCHORED_SOUL(effectTick, amp = L, false, false, true) **independente do retorno do dano**, e descarte. Block hit descarta. Esses overrides de impacto não têm guarda local de servidor; o wrapper normal é servidor, mas a autoridade do callback herdado e seus ingressos diretos continuam condicionais ao host e à QA. shouldPierceShields=true só pula o ramo host de ShieldPart/AbstractShieldEntity; não prova ignorar escudo vanilla/item/claims. [Tipo][entity], [impacto][impact], [shield host][shield-host], [settlement][damage-host].
3. **Anúncio de teleporte:** AnchoredSoulEffect reage a EntityTeleportEvent para Living com buff; sem guarda local de logical side/cancelamento ou chegada confirmada. NeoForge trata a classe base e filhos como eventos de intenção; getPrev lê posição atual da entidade. Não significa que todo teleporte vanilla/modded poste esse evento. [Handler][anchor], [evento][teleport-event].
4. Handler cria ExtractedSoul(owner=vítima, extractor=null), HPmax=HP atual da vítima/Health=max, duração 200 ticks, posição oldPos. Não chama enableRadius: a regra distance>12 não é ativada nesse caminho. Solicita spawn sem ler boolean e remove o buff sem verificar retorno, mesmo sem chegada/spawn confirmado. Um veto posterior não desfaz automaticamente soul/remoção. [Handler][anchor], [proxy][proxy-ctor].

### Coeficiente real, forwarding e saída

Tooltip anuncia `(L+1)×5%`=10–45%. Handler usa `(amp+1)×0.5` como argumento e ExtractedSoul#setBonusPercent divide 100; com amp = L, **B=(L+1)×0.005 =1–4.5%**. Não depende de P/SpiritPower no caminho normal do anchor; não corrigir silenciosamente a diferença 10×. Publisher estreito confirma multiply 0.5@65–67 no handler e divide 100@2–6 no setter, além de Kunai.setEffectTick multiply@6. [Tooltip][spell], [trigger][anchor], [setter][proxy-owner].

LivingDamageEvent.Pre sobre proxy usa originalDamage A: fonte is_soul transfere **A integral sem cap de HP**, outras fontes pedem min(A, HP atual do proxy)×B ao owner via hurt plain soul_damage, preservando apenas original source.getEntity() como attacker. Não reduz/cancela dano do proxy, ignora resultado de owner.hurt e não usa helper/SpellDamageEvent. Não prometer percentual de HP final ou autoria do caster inicial do kunai. [Forward][proxy-events], [fase Pre][damage-pre], [tags][soul-types].

Ausência de radius evita só a punição por afastamento; **LivingDeathEvent ainda pune qualquer ExtractedSoul** com owner: Soulburn 200/amp 0 + SLOWED 200/amp 3. Counterspell de caster real com extractor=null e config false entra na punição, não cancela evento; host pode seguir para antiMagic e descartar. onUnSummon/expiry 200 não pune por si. Owner ausente, death/listener order e mundo/dimensão requerem QA. [Eventos][proxy-events], [config][config], [host][counterspell-host].

A classe do projétil não possui override de save para effectLevel/effectTick; load que só restaure o host conserva Damage/Age, mas não comprova recuperar L/T e pode reconstruir defaults 0/20 sem setter externo. Proxy salva owner/extractor/tipo/duração, **não B/radius**; spawn packet também não fecha esses fields como sync completo. Geometry copia tipo de não-Player, senão registry 0.6×1.8, com demais efeitos de escala/pose pendentes. [Save projétil][projectile-save], [proxy save][proxy-save], [sync][proxy-spawn], [ctor][proxy-ctor].

**N/A comprovados:** o `AnchoringKunaiSpell#onCast`/projétil não cria cura, ritual, mutação de blocos, ataque AI ou summon slots; o proxy é `LivingEntity`, sem AI de pet ou `SpellSummonEvent`. Não há alcance ofensivo fixo configurado neste executor: tracking 64 é sincronização, e colisão, expiração e ticking range encerram o trajeto. Sem homing, ricochet ou aceleração configurados aqui; `getSpeed` só alimenta o lançamento host. [Emissão][emission], [projétil][projectile], [host][projectile-host], [proxy][proxy-spawn].

## Matriz de alteração por perks

**Leitura de mutabilidade:** `NATIVE_ATTRIBUTE` = atributo consumido no caminho indicado; `CONFIG_NATIVE` = configuração global; `HOOK_VERIFICADO` = campo realmente mutável no evento host citado; `CONDITIONAL` = adapter ainda não implementado/validado; `⛔ SEM_HOOK_SEGURO` = alteração sem seam específico demonstrado. Os hooks gerais de cast/dano não expõem alvo, geometria, tipo ou contagem automaticamente; ver [contrato comum](../SPELL-PERK-BOUNDARIES-1.1.5.md).

| Eixo | Valor / consumidor / fase | Superfície e limite | QA |
| --- | --- | --- | --- |
| Dano / power | D=P no spawn, helper no impacto. B anchor=(L+1)×.005 independente de P. [Spell][spell], [handler][anchor]. | Atributos Spirit/power config alteram D nativamente; não alteram B automaticamente. SpellDamageEvent amount/cancel pré-resistência só no hit Living+SpellDamageSource; adapter CONDITIONAL. | Q1/Q3 |
| Tipo / linked damage | Direct Spirit; forwarding plain soul_damage com attacker do golpe no proxy. [Fonte][source-host], [eventos][proxy-events]. | Sem setter de DamageType nesse evento; ⛔ SEM_HOOK_SEGURO para conversão, double-hit ou linked-damage RPG paralelo. | Q3 |
| Target / range / área | Look/projétil, sem target resolver local; anchor usa oldPos no anúncio, proxy sem quebra de vínculo em 12 blocks. [Emission][emission], [anchor][anchor]. | Tracking 64 não é alcance ofensivo; sem hook seguro para retarget/single→AOE/forçar spawn/limite global de souls. | Q2/Q4 |
| Projétil / trajetória | 1 por cast, 0.5×0.5 blocks, speed 1.2, noGravity; lifetime host > 300. [Tipo][entity], [projétil][projectile], [host][projectile-host]. | SetDamage/SetEffectLevel/setEffectTick públicos são por instância, sem callback terceiro pré-spawn confirmado. Resize/speed/pierce custom CONDITIONAL/⛔ fail-closed. | Q2/Q4 |
| Tempo / cooldown | INSTANT 0 ticks, 90 s; buff 20(5L+10), soul 200, recast 100. [Spell][spell], [anchor][anchor]. | Clocks independentes. Atributo cooldown não é duração; setEffectTick multiplicativo não é setter absoluto idempotente. | Q1/Q4 |
| Mana / recast | 20+10(L−1) antes config;3 casts totais e 2 remaining inicial. [Wrapper][cast-host], [recast][recasts]. | Hook de mana/nível host existe no wrapper, custo anterior não recalculado. Janela/count sem mutador MFTE por jogador verificado; sem segunda reserva/cobrança. | Q1/Q4 |
| Estados / proteção | ANCHORED_SOUL aplicado mesmo hurt false; trigger remove efeito mesmo spawn false; punição de morte não depende radius. [Impacto][impact], [handler][anchor], [events][proxy-events]. | Anúncio/observer não é sucesso. Teleporte genérico mutável/cancelável não demonstra hook per-spell de proxy/cap/cleanup. PvP/claims/sideguards continuam pendentes. | Q2/Q3/Q5 |
| Summon / mundo | Proxy sem AI/SummonManager/SpellSummonEvent; owner=vítima, extractor=null; não altera blocos. [Ctor][proxy-ctor]. | Não tratar como pet nem duplicar owner/ledger. Cap de proxies por owner/cast não demonstrado. | Q2/Q4 |
| Persistência / dedup | Host projectile Damage/Age, estado anchor/proxy próprio com omissões; UUID→cast→vítima→teleportevent→proxy. [Save][projectile-save], [proxy][proxy-save]. | Não creditar cada evento/forward/punição de morte como novo cast/Mastery. Escola custom condicionada no [comum](../SPELL-PERK-BOUNDARIES-1.1.5.md). | Q4/Q5 |

Soulburn da punição é consumer plain/maxHP separado; o candidato f2 e o trecho do publisher não possuem o guard posterior de tag de imunidade em `SoulburnEffect#applyEffectTick`. SoulwardRing remove esse buff por tick e aplica originalAmount×0.8 no seu ramo ServerPlayer/is_soul; settlement final depende dos listeners/config. [Effect][soulburn], [ring][ring]. Assinatura ocupada: marca por projétil que transforma anúncio de teleporte em proxy de dano na origem; magia original precisa um contrato de commit/rollback/token próprio.

- **Q1:** origens/scroll/config/L 1–8, custo inicial/recast 3, cooldown inicial/final, snapshot de L/P versus effectLevel/tooltip.
- **Q2:** hitbox/blocks/magicshield/itemshield/aliados/PvP/claims, spawns negados, anúncio sem teleporte/post manual/subclasses e lado cliente/servidor.
- **Q3:** veto do helper/status mesmo sem HP, coeficiente 1–4.5% versus 10–45%, is_soul 100% / overkill/attacker null, proxy/owner invulnerável, punição de morte sem radius.
- **Q4:** buff/recast/childtimers distintos, multiplicação setter repetida, antiMagic/extractor null/owner perdido, save/load sem fields B/radius/L/T, múltiplos proxies e budgets.
- **Q5:** dedicado/cliente/multiplayer/Survival/sync/relog/dimensão/restart, chegada e dedup/Mastery. **Todos PENDING**; sem adapter/runtime novo.

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
[projectile-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L46-L114
[hit-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L153-L200
[shield-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L361-L367
[projectile-save]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L302-L359
[proxy-ctor]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/spirit_challenging/ExtractedSoul.java#L102-L158
[proxy-owner]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/spirit_challenging/ExtractedSoul.java#L160-L224
[proxy-defense]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/spirit_challenging/ExtractedSoul.java#L226-L293
[proxy-save]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/spirit_challenging/ExtractedSoul.java#L311-L360
[proxy-spawn]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/spirit_challenging/ExtractedSoul.java#L40-L98
[proxy-events]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/events/SoulChallengingEvents.java#L23-L95
[damage-pre]: https://github.com/neoforged/NeoForge/blob/e0e7ab5d273fdc034f23fee7bf91c61ae39d3019/src/main/java/net/neoforged/neoforge/event/entity/living/LivingDamageEvent.java#L40-L83
[counterspell-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/CounterspellSpell.java#L67-L106
[soul-types]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/datagen/MFTEDamageTypeTagGenerator.java#L29-L58
[spell]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/AnchoringKunaiSpell.java#L24-L64
[emission]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/AnchoringKunaiSpell.java#L76-L95
[guide]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/resources/assets/iss_magicfromtheeast/lang/en_us.json#L55-L56
[projectile]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/anchoring_kunai/AnchoringKunaiProjectile.java#L25-L64
[impact]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/anchoring_kunai/AnchoringKunaiProjectile.java#L72-L92
[entity]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTEEntityRegistries.java#L143-L147
[anchor]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/effects/AnchoredSoulEffect.java#L25-L47
[teleport-event]: https://github.com/neoforged/NeoForge/blob/e0e7ab5d273fdc034f23fee7bf91c61ae39d3019/src/main/java/net/neoforged/neoforge/event/entity/EntityTeleportEvent.java#L21-L84
[recasts]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/PlayerRecasts.java#L46-L131
[recast-instance]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/RecastInstance.java#L27-L35
