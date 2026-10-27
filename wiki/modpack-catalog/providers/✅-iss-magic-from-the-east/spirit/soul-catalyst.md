# Soul Catalyst

**Dossiê documental — 27/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT` **somente no registry**; lógica `RELEASE_BOUNDED_SOURCE`; integração `CONDITIONAL`; QA físico `PENDING`. **+0 identidades / +0 strict**: projéteis, proxies, efeitos e impactos são filhos da spell. Nenhuma equivalência integral de métodos nem integração jogável é certificada.

## Identidade, proveniência e descrição

ISS: Magic From The East, mod_id `iss_magicfromtheeast`, spell **`iss_magicfromtheeast:soul_catalyst`**, escola própria `iss_magicfromtheeast:spirit`; declarante `net.warphan.iss_magicfromtheeast.spells.spirit.SoulCatalystSpell`. [Registry][registry], [escola][school], [classe][spell].

JAR histórico **`iss_magicfromtheeast-1.1.5.jar`**, MC 1.21.1/NeoForge, publisher [CF7385201](https://www.curseforge.com/minecraft/mc-mods/magic-from-the-east/files/7385201), 1.680.780 bytes, SHA-1 `e3552ea6b7b32b843c48bf0d857237d4b7129ab0`; [identidade binária](../EXACT-BINARY-SPELLS-1.1.5.md). A lógica abaixo é **`RELEASE_BOUNDED_SOURCE`** do candidato oficial **`WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88`**. Esse commit de 27/12/2025, 16:35 UTC, antecede o upload de 17:17 UTC; data e versão 1.1.5 restringem a proveniência, **não provam equivalência integral de métodos com o JAR**. A inspeção `javap` abaixo confirma somente os literais/chamadas declarados, sem certificado de equivalência nem aceite físico.

Build do candidato: **NeoForge 21.1.187 / Iron’s 3.14.8**; pack: **NeoForge 21.1.250 / Iron’s 3.16.3**. O host consultado é `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`; seus contratos abaixo são condicionais à composição real do pack. Defaults não são configuração implantada. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.1.5.md). Metadata **All Rights Reserved**; MIT do template é limitada aos arquivos do template. Apenas fatos, paráfrases e permalinks, sem importar código ou assets.

[Guia oficial][guide], parafraseado: uma salva de crânios espirituais semeia Soulburn ao atingir. Não há override local de crafting/loot; segue elegibilidade host. Scroll/config implantados e rota Survival concreta **NÃO VERIFICADOS**. Mobs Onmyoji também referenciam esta spell em seu perfil; isso não prova o mesmo wrapper/pagamento jogador. [Host][acquisition], [perfil NPC][mob-profile].

## Localizadores e unidades

`L` é o nível recebido pelo executor; `P` usa os fatores host `SPELL_POWER × SpiritPower × POWER_MULTIPLIER`. Multiplicadores 1 definem o cenário neutro, sem afirmar configuração implantada. Dano é expresso em HP pedidos; 20 ticks correspondem a 1 s nominal, distâncias a blocks e velocidades a blocks/tick. Não confundir tentativa do helper, retorno de `hurt` e perda final de HP. [Escala, mana e tempo host][power].

| Campo | Classe e métodos concretos / autoridade |
| --- | --- |
| Defaults e escala | `SoulCatalystSpell#<init>/getDefaultConfig/getCastType/getUniqueInfo`; `AbstractSpell#getManaCost/getSpellPower/getEffectiveCastTime`. [Spell][spell], [host][power]. |
| Quantidade, origem e spawn | `SoulCatalystSpell#onCast`, inclusive `super.onCast` dentro do loop. [Emissão][emission], [host som][base-finish]. |
| Movimento e colisão | `SoulSkullProjectile#<init>/shoot/getSpeed/onHitEntity/onHitBlock`; `AbstractMagicProjectile#tick/handleHitDetection/checkDespawn`. [Projétil][skull], [impacto][skull-hit], [host][projectile-host], [colisão][hit-host]. |
| DOT, configuração e proteção | `SoulburnEffect#applyEffectTick/shouldApplyEffectTickThisTick`, `MFTEServerConfigs` e `SoulwardRing#curioTick`. [Efeito][soulburn], [config][config], [anel][ring]. |
| Saída e save | `AbstractMagicProjectile#onAntiMagic/readAdditionalSaveData/addAdditionalSaveData/shouldBeSaved`. [Estado][projectile-save]. |

## Pipeline e parâmetros resolvidos

Defina `L` nível entregue ao onCast, `P=(2+(L−1))×SPELL_POWER×SpiritPower×POWER_MULTIPLIER`. Dano por crânio `D=P/2`, count `N=2+L/2` com divisão inteira. Neutro significa multiplicadores 1, não config implantada. [Spell][spell], [escala host][power].

| L default | Mana neutra | P | D por crânio (HP tentados) | N solicitado |
| --- | --- | --- | --- | --- |
| 1 | 35 | 2 | 1 | 2 |
| 2 | 40 | 3 | 1.5 | 3 |
| 3 | 45 | 4 | 2 | 3 |
| 4 | 50 | 5 | 2.5 | 4 |
| 5 | 55 | 6 | 3 | 4 |
| 6 | 60 | 7 | 3.5 | 5 |
| 7 | 65 | 8 | 4 | 5 |
| 8 | 70 | 9 | 4.5 | 6 |

1. **Ingresso:** LONG 20 ticks base; host aplica redução de cast quando pertinente. Mana `int((35+5(L−1))×MANA_MULTIPLIER)`, cooldown default 60 s=1200 ticks antes de modifiers; sem recast próprio. Wrapper anuncia/debita antes de onCast. [Spell][spell], [host][cast-host].
2. **Emissão:** por N, cria SoulSkullProjectile(owner=caster), posição caster+Y(eyeHeight−metade da altura da bullet), shoot(look, .12), grava D e solicita spawn sem consumir boolean. Com AABB registrada 0.4×0.4 blocks, offset Y nominal eyeHeight−0.2. getSpeed = 1.75 blocks/tick; shoot local normaliza e perturba vetor com inaccuracy 0.12, preserva seu módulo antes de host shoot. NoGravity; homing/pierce/ricochet não configurados pela spell. [Emissão][emission], [projétil][skull], [tipo][entity], [host][projectile-host].
3. **Colisão:** herda swept query/AABB inflação 0.1/interseção 0.3, ordenação por distância e exclusão owner/aliados. Host publica ProjectileImpactEvent no hit de entidade antes de onHit; cada crânio é entidade independente. MFTE onHitEntity chama super, depois helper D com sourceSpell Soul Catalyst, direta=crânio/causador=owner. Para Living tenta Soulburn 80 ticks/amp 0 e escreve invulnerableTime = 0 **mesmo quando helper retorna false**; depois discard. Block impact chama super/discard sem AOE. O override `SoulSkullProjectile#onHitEntity` não tem guarda local de servidor: o wrapper normal não demonstra sozinho a autoridade de todos os callbacks herdados ou ingressos diretos. Ramo de magic shield no super pode descartar e ainda retornar ao restante do método MFTE, sem guarda isRemoved local. [Impacto][skull-hit], [host][hit-host], [shield][shield-host], [settlement][damage-host].
4. **Saída:** source chama super.onCast **dentro do loop**. No host consultado isso solicita som de término N vezes; o wrapper não é reinvocado, logo isso não demonstra N novos SpellOnCastEvent/débitos/Mastery. Getters/count e chamadas estreitas de emissão/impacto foram localizados no publisher (onCast setDamage81/spawn87/pop90/super99; hit applyDamage34/pop37), sem declarar todos os métodos iguais. [Base][base-finish].
5. **Lifecycle:** host expira tickCount > 300, tem despawn por ticking range, antiMagic discard e save de Damage/Age; unload-to-chunk é excluído de shouldBeSaved nesse host. Duração do buff 80 não é lifetime do projétil, nem quatro hits garantidos. [Lifecycle][projectile-host], [save][projectile-save].

### Soulburn: consumidor separado no candidato de release

`SoulburnEffect#applyEffectTick` calcula `x=Hmax×scaling/100` e faz uma tentativa de `hurt` com fonte plain **`iss_magicfromtheeast:soul_damage`**, sem caster original. Os ramos pedem 1 HP se `x<1`, `x` se `1≤x≤maxDamage`, ou `maxDamage` se `x>maxDamage`. Defaults `scaling=5` e `maxDamage=10` dão entre 1 e 10 HP por pulso; o amplificador não multiplica esse valor. As entradas são `define`, sem `defineInRange`: não assumir clamp/validação adicional para configuração anômala. `#shouldApplyEffectTickThisTick` usa `i=20 >> amplifier` e executa se `i≤0` ou `remainingDuration % i=0`; amp 0 corresponde a cada 20 ticks de duração restante. [Métodos][soulburn], [`MFTEServerConfigs`][config].

O candidato f2 e o trecho do publisher inspecionado **não têm o guard posterior de tag de imunidade em `applyEffectTick`**. Isso não prova ausência de imunidade em outros consumers. Soulburn não chama `DamageSources.applyDamage`/`SpellDamageEvent`; cada `hurt` ainda segue seu pipeline de dano e listeners. Config é global **SERVER**, e as duas entradas de Soulburn não usam `worldRestart` nesse bloco. `SoulwardRing#curioTick` pede remoção do buff; seu handler incoming para ServerPlayer equipado usa `originalAmount×0.8` em fontes `is_soul` — 80% restante antes dos demais listeners, sem garantir HP final. [Efeito][soulburn], [anel][ring].

**N/A comprovados:** `SoulCatalystSpell#onCast`/`SoulSkullProjectile#onHitEntity` não criam cura, teleporte, ritual, mutação de blocos, summon slots ou AI. Não há alcance ofensivo fixo nem cap global de vítimas configurado; cada crânio termina no impacto/bloco ou nos limites host. Tracking 64 é sincronização, não range; homing, ricochet e aceleração não são configurados pelo executor. [Emissão][emission], [hit][skull-hit], [host][projectile-host].

## Matriz de alteração por perks

**Leitura de mutabilidade:** `NATIVE_ATTRIBUTE` = atributo consumido no caminho indicado; `CONFIG_NATIVE` = configuração global; `HOOK_VERIFICADO` = campo realmente mutável no evento host citado; `CONDITIONAL` = adapter ainda não implementado/validado; `⛔ SEM_HOOK_SEGURO` = alteração sem seam específico demonstrado. Os hooks gerais de cast/dano não expõem alvo, geometria, tipo ou contagem automaticamente; ver [contrato comum](../SPELL-PERK-BOUNDARIES-1.1.5.md).

| Eixo | Valor / consumidor / fase | Superfície e limite | QA |
| --- | --- | --- | --- |
| Dano / power | D=P/2 snapshot por emissão; applyDamage no hit. [Emissão][emission], [impacto][skull-hit]. | SPELL_POWER/spirit_spell_power e config power são inputs nativos; SpellDamageEvent amount/cancel só no ramo Living+SpellDamageSource antes de resist/hurt. Adapter CONDITIONAL; não duplicar dano. | Q1/Q3 |
| Tipo / DOT | Direct hit Spirit; Soulburn plain soul_damage/config/maxHP/cadência independente. [Escola][school], [DOT][soulburn]. | Amount não converte DamageType. ⛔ SEM_HOOK_SEGURO para conversão ou unificar DOT ao scaling P. Sem guard de tag de imunidade neste consumer do candidato. | Q3/Q4 |
| Alvo / range / área | Look/projectile; sem target resolver remoto ou dano AOE local; host swept path e filtros. [Host][hit-host]. | Sem setter de range/retarget/área pré-settlement verificado. ⛔ SEM_HOOK_SEGURO single→AOE; range de tracking 64 não é alcance ofensivo. | Q2 |
| Projétil / count | N=2+L/2, AABB 0.4², speed 1.75, inaccuracy 0.12, expiry > 300. [Tipo][entity], [skull][skull]. | SetDamage/pierce/homing herdados são por instância; não há callback terceiro pré-spawn comprovado. Resize/speed/spread/count independentes CONDITIONAL/⛔ fail-closed. | Q2/Q4 |
| Tempo / cooldown | LONG 20 base,60 s cooldown, DOT 80 ticks/amp 0. [Spell][spell]. | Cast-time/cooldown nativos via host/comum; não modificam automaticamente DOT/cadência/lifetime. | Q1/Q4 |
| Mana / casts | Custo inicial 35+5(L−1) antes config; sem charges/recast próprio. [Host][cast-host]. | SpellOnCastEvent mutável nesse wrapper; nível novo não recalcula custo; super em loop não é nova cobrança. | Q1/Q5 |
| Estados / proteção | Soulburn/addEffect e iFrames 0 independem de dano aceito; registry/rootowner nativos. [Hit][skull-hit]. | Não premiar tentativa/status como HP final. PvP/claims/friendly/guards e sync físicos pendentes; não modificar efeito global por perk sem seam. | Q3/Q5 |
| Summons / mundo | Crânios são filhos sem AI/summon slots; sem block mutation/teleport/heal local. [Emissão][emission]. | SummonAI N/A; sem segunda entidade, DOT, ledger ou custo BA/RPG. | Q2/Q5 |
| Persistência / dedup | UUID crânio→cast pai→vítima/fase; Damage/Age herdados. [Save][projectile-save]. | Não contar cada crânio/pulso/partícula como novo cast. Mastery escola custom condicionado no [comum](../SPELL-PERK-BOUNDARIES-1.1.5.md). | Q4/Q5 |

Assinatura ocupada: salva discreta de crânios com dano inicial, DOT maxHP e reset de iFrames. Magia original exige budget/owner/token próprios; documentar esta fórmula não cria mutador.

- **Q1:** config/origem/scroll, L 1–8/atributos, custo antes/depois de evento, interrupção e cooldown.
- **Q2:** spawn negado/count vivo, hitbox/spread/blocos/escudos/aliados/owner/PvP/claims, trajetórias e ticking range.
- **Q3:** helper false/veto/resist, buff recusado/mesclado, iFrames 0, fonte/kill credit, Soulburn, ring e imunidades downstream.
- **Q4:** expiry/load/relog/restart, DOT cadence/amp/config e múltiplos crânios no mesmo alvo/tick.
- **Q5:** som N vezes, dedicado/cliente/sync/Survival, dedup/Mastery custom. **Todos PENDING**; sem runtime/adapter novo.

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
[spell]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/SoulCatalystSpell.java#L24-L52
[emission]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/SoulCatalystSpell.java#L75-L86
[guide]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/resources/assets/iss_magicfromtheeast/lang/en_us.json#L37-L38
[skull]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/soul_skull/SoulSkullProjectile.java#L33-L75
[skull-hit]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/soul_skull/SoulSkullProjectile.java#L77-L92
[entity]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTEEntityRegistries.java#L80-L84
[base-finish]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L359-L368
[mob-profile]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/mfte_wizards/onmyoji/OnmyojiEntity.java#L51-L62
