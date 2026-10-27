# Soul Burst

**Dossiê documental — 27/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT` **somente no registry**; lógica `RELEASE_BOUNDED_SOURCE`; integração `CONDITIONAL`; QA físico `PENDING`. **+0 identidades / +0 strict**: projéteis, proxies, efeitos e impactos são filhos da spell. Nenhuma equivalência integral de métodos nem integração jogável é certificada.

## Identidade, proveniência e descrição

ISS: Magic From The East, mod_id `iss_magicfromtheeast`, spell **`iss_magicfromtheeast:soul_burst`**, escola própria `iss_magicfromtheeast:spirit`; declarante `net.warphan.iss_magicfromtheeast.spells.spirit.SoulBurstSpell`. [Registry][registry], [escola][school], [classe][spell].

JAR histórico **`iss_magicfromtheeast-1.1.5.jar`**, MC 1.21.1/NeoForge, publisher [CF7385201](https://www.curseforge.com/minecraft/mc-mods/magic-from-the-east/files/7385201), 1.680.780 bytes, SHA-1 `e3552ea6b7b32b843c48bf0d857237d4b7129ab0`; [identidade binária](../EXACT-BINARY-SPELLS-1.1.5.md). A lógica abaixo é **`RELEASE_BOUNDED_SOURCE`** do candidato oficial **`WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88`**. Esse commit de 27/12/2025, 16:35 UTC, antecede o upload de 17:17 UTC; data e versão 1.1.5 restringem a proveniência, **não provam equivalência integral de métodos com o JAR**. A inspeção `javap` abaixo confirma somente os literais/chamadas declarados, sem certificado de equivalência nem aceite físico.

Build do candidato: **NeoForge 21.1.187 / Iron’s 3.14.8**; pack: **NeoForge 21.1.250 / Iron’s 3.16.3**. O host consultado é `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`; seus contratos abaixo são condicionais à composição real do pack. Defaults não são configuração implantada. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.1.5.md). Metadata **All Rights Reserved**; MIT do template é limitada aos arquivos do template. Apenas fatos, paráfrases e permalinks, sem importar código ou assets.

[Guia oficial][guide], parafraseado: explosão espiritual centrada no caster que danifica e aplica Soulburn. Sem override local de aquisição; elegibilidade/loot/crafting seguem host/config e a rota Survival concreta **NÃO VERIFICADA**. Onmyoji referencia a spell em seu perfil, sem provar o mesmo ingresso/custo do jogador. [Aquisição][acquisition], [perfil NPC][mob-profile].

## Localizadores e unidades

`L` é o nível recebido pelo executor; `P` usa os fatores host `SPELL_POWER × SpiritPower × POWER_MULTIPLIER`. Multiplicadores 1 definem o cenário neutro, sem afirmar configuração implantada. Dano é expresso em HP pedidos; 20 ticks correspondem a 1 s nominal, distâncias a blocks e velocidades a blocks/tick. Não confundir tentativa do helper, retorno de `hurt` e perda final de HP. [Escala, mana e tempo host][power].

| Campo | Classe e métodos concretos / autoridade |
| --- | --- |
| Defaults e escala | `SoulBurstSpell#<init>/getDefaultConfig/getCastType/getUniqueInfo`; `AbstractSpell#getManaCost/getSpellPower/getEffectiveCastTime`. [Spell][spell], [host][power]. |
| Dano, área, filtro e VFX | `SoulBurstSpell#onCast/getRadius/getDamage/getDuration`; query e lambda de impacto dentro de `onCast`. [Executor][executor], [helpers][burst-helpers]. |
| Fonte e settlement | `AbstractSpell#getDamageSource`; `DamageSources#applyDamage`. [Fonte][source-host], [helper][damage-host]. |
| DOT e cleanup | `SoulburnEffect#applyEffectTick/shouldApplyEffectTickThisTick`, `SoulwardRing#curioTick`; sem entidade persistente própria no `onCast`. [Efeito][soulburn], [anel][ring], [executor][executor]. |

## Pipeline, geometria e parâmetros

`P=(2+(L−1))×SPELL_POWER×SpiritPower×POWER_MULTIPLIER`; dano inicial `D=P` HP. Mana `int((40+10(L−1))×MANA_MULTIPLIER)`; níveis default 1–10 dão mana 40–130/P 2–11. LONG 20 ticks base, cooldown default 30 s=600 ticks, sem recast/charges próprios. Duração pedida de Soulburn `T=40+20L`ticks=60–240 (3–12 s), amp 0; raio literal 8 blocks. P não altera raio ou T nesse consumer. [Defaults][spell], [helpers][burst-helpers], [host][power].

1. Wrapper servidor testa admissão/pre-cast e anuncia/debita antes de onCast. A spell calcula raio, D e T; consulta `caster.boundingBox.inflate(8,4,8)` excluindo caster. Predicate exige !isFriendlyFireBetween(target, caster) e hasLineOfSight(..., true). Dentro do loop exige Living e **distanceToSqr(caster)<64**. Há recorte vertical/query-AABB além da esfera estrita, sem limite/ordenação de vítimas local. Não descrever toda esfera de 8 como automaticamente consultada. [Executor][executor], [host][cast-host].
2. Em cada alvo elegível tenta helper D com fonte SpellDamageSource Spirit do caster (direta e causadora pelo overload de 1 argumento). Depois tenta Soulburn T/amp 0 **sem ler retorno do dano ou addEffect**. Sem knockback/heal crítico adicional local e sem dano a blocos; blastwave e partículas não são novos hits. [Executor][executor], [source][source-host], [settlement][damage-host].
3. **Apresentação e prova estreita:** o candidato contém `CameraShakeData(10,caster.position,2r)`, isto é, 10 ticks e raio visual 16 blocks. No publisher, a chamada ocorre em `onCast` nos offsets 141–158; a lambda tenta helper e buff sem condicionar o segundo ao retorno do primeiro. Essa inspeção confirma esses campos e chamadas, sem equiparar o método inteiro ou tornar câmera/VFX uma hitbox. [Executor][executor].
4. Não cria entidade de dano persistente; aftercast é MobEffect no alvo e seus consumers. Timeout/remover/refresh do effect pertencem ao provider/host, sem ledger próprio de alvos neste spell. [Executor][executor], [effect][soulburn].

### Soulburn: consumidor separado no candidato de release

`SoulburnEffect#applyEffectTick` calcula `x=Hmax×scaling/100` e faz uma tentativa de `hurt` com fonte plain **`iss_magicfromtheeast:soul_damage`**, sem caster original. Os ramos pedem 1 HP se `x<1`, `x` se `1≤x≤maxDamage`, ou `maxDamage` se `x>maxDamage`. Defaults `scaling=5` e `maxDamage=10` dão entre 1 e 10 HP por pulso; o amplificador não multiplica esse valor. As entradas são `define`, sem `defineInRange`: não assumir clamp/validação adicional para configuração anômala. `#shouldApplyEffectTickThisTick` usa `i=20 >> amplifier` e executa se `i≤0` ou `remainingDuration % i=0`; amp 0 corresponde a cada 20 ticks de duração restante. [Métodos][soulburn], [`MFTEServerConfigs`][config].

O candidato f2 e o trecho do publisher inspecionado **não têm o guard posterior de tag de imunidade em `applyEffectTick`**. Isso não prova ausência de imunidade em outros consumers. Soulburn não chama `DamageSources.applyDamage`/`SpellDamageEvent`; cada `hurt` ainda segue seu pipeline de dano e listeners. Config é global **SERVER**, e as duas entradas de Soulburn não usam `worldRestart` nesse bloco. `SoulwardRing#curioTick` pede remoção do buff; seu handler incoming para ServerPlayer equipado usa `originalAmount×0.8` em fontes `is_soul` — 80% restante antes dos demais listeners, sem garantir HP final. [Efeito][soulburn], [anel][ring].

**N/A comprovados:** `SoulBurstSpell#onCast` não cria projétil, summon/AI, movimento, cura, ritual, mutação de blocos ou entidade de área persistente. Speed, pierce, homing e NBT de uma entidade de dano são N/A; a persistência posterior é o `MobEffect` Soulburn do alvo. [Executor][executor], [efeito][soulburn].

## Matriz de alteração por perks

**Leitura de mutabilidade:** `NATIVE_ATTRIBUTE` = atributo consumido no caminho indicado; `CONFIG_NATIVE` = configuração global; `HOOK_VERIFICADO` = campo realmente mutável no evento host citado; `CONDITIONAL` = adapter ainda não implementado/validado; `⛔ SEM_HOOK_SEGURO` = alteração sem seam específico demonstrado. Os hooks gerais de cast/dano não expõem alvo, geometria, tipo ou contagem automaticamente; ver [contrato comum](../SPELL-PERK-BOUNDARIES-1.1.5.md).

| Eixo | Valor / consumidor / fase | Superfície e limite | QA |
| --- | --- | --- | --- |
| Dano / power | D=P snapshot no onCast, por vítima elegível. [Executor][executor]. | SPELL_POWER/spirit_spell_power/config power nativos; helper Living permite amount/cancel pré-resistência/hurt. Adapter CONDITIONAL, sem dano paralelo. | Q1/Q3 |
| Tipo / DOT | Inicial Spirit com caster; Soulburn plain soul_damage sem caster original, maxHP/config. [Escola][school], [effect][soulburn]. | Não há setter de DamageType nesse evento; ⛔ SEM_HOOK_SEGURO para conversão. Power inicial não é setter de DOT. Imunidades adicionais não demonstradas neste consumer. | Q3/Q4 |
| Range / targeting | Self-centered; queryAABB inflate 8/4/8, filtros host e Living+distância3D<8. [Executor][executor]. | Getter getRadius literal 8 sem setter; sem hook de resolver/raio/maxTargets verificado. ⛔ SEM_HOOK_SEGURO para retarget/single→AOE/mais vítimas. | Q2 |
| Área / budget | Sem cap/ordem local de alvos; recorte da AABB e teste radial coexistem. [Executor][executor]. | Alteração de raio exige tratar custo/performance/filtros; VFX/camera não provam geometria mutável. | Q2/Q5 |
| Projétil / summon | N/A: resolução imediata, sem projétil ou AI. [Executor][executor]. | Não criar segunda área/entidade para simular bônus. | Q2 |
| Tempo / cooldown | LONG 20 base;30 s cooldown; T=40+20L, amp 0, cadência 20 no default. [Spell][spell]. | Cast-time/cooldown config/atributos host nativos; duração/status/cadência exigem consumer próprio, não setter de cast. | Q1/Q4 |
| Mana / casts | 40+10(L−1) antes config; sem recast próprio. [Host][cast-host]. | SpellOnCastEvent mana/level mutáveis nesse wrapper; não recompõem custo já calculado/admissão. | Q1 |
| Estados / mundo | Soulburn pedido mesmo damage false; sem block mutation/teleport/heal local. [Executor][executor]. | Listener de dano não é setter do status. Claims/PvP/LOS e buff recusado/mesclado requerem QA; sem segunda transação. | Q2/Q3 |
| Persistência / dedup | Cast único→conjunto de vítimas→effect/pulsos; sem entidade persistente local. [Effect][soulburn]. | Não premiar cada alvo/pulso/partícula como outro cast/Mastery; escola custom condicionada no [comum](../SPELL-PERK-BOUNDARIES-1.1.5.md). | Q4/Q5 |

Assinatura ocupada: burst centrado no caster com LOS, recorte geométrico composto e DOT maxHP. Uma magia original com seleção/budget diferente precisa contrato próprio, não cast espelhado.

- **Q1:** origens/scroll/config, L 1–10, mana e cast-time/cooldown modificados, power e anúncio pré-efeito.
- **Q2:** borda estrita 8, AABB vertical/caster grande, LOS/blocos/aliados/owner/PvP/claims e budgets de alvos.
- **Q3:** amount/veto/resistência, Soulburn apesar de hurt false, buff recusado e fonte/kill credit/ring.
- **Q4:** duração/cadência/merge e imunidades downstream, morte/relog/restart/cliente e config efetiva.
- **Q5:** câmera e partículas, dedicado/cliente/Survival/sync e dedup/Mastery custom. **Todos PENDING**; sem runtime novo.

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
[spell]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/SoulBurstSpell.java#L30-L60
[executor]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/SoulBurstSpell.java#L83-L105
[guide]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/resources/assets/iss_magicfromtheeast/lang/en_us.json#L39-L40
[mob-profile]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/mobs/mfte_wizards/onmyoji/OnmyojiEntity.java#L51-L62

[burst-helpers]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/SoulBurstSpell.java#L107-L117
