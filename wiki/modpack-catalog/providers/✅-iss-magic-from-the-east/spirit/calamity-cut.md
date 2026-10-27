# Calamity Cut

**Dossiê documental — 27/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT` **somente no registry**; lógica `RELEASE_BOUNDED_SOURCE`; integração `CONDITIONAL`; QA físico `PENDING`. **+0 identidades / +0 strict**: projéteis, proxies, efeitos e impactos são filhos da spell. Nenhuma equivalência integral de métodos nem integração jogável é certificada.

## Identidade, proveniência e ingresso

Provider ISS: Magic From The East, `mod_id=iss_magicfromtheeast`; spell **`iss_magicfromtheeast:calamity_cut`**, escola default **`iss_magicfromtheeast:spirit`**. Declarante `net.warphan.iss_magicfromtheeast.spells.spirit.CalamityCutSpell`. [Registro][registry], [escola][school].

JAR histórico **`iss_magicfromtheeast-1.1.5.jar`**, MC 1.21.1/NeoForge, publisher [CF7385201](https://www.curseforge.com/minecraft/mc-mods/magic-from-the-east/files/7385201), 1.680.780 bytes, SHA-1 `e3552ea6b7b32b843c48bf0d857237d4b7129ab0`; [identidade binária](../EXACT-BINARY-SPELLS-1.1.5.md). A lógica abaixo é **`RELEASE_BOUNDED_SOURCE`** do candidato oficial **`WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88`**. Esse commit de 27/12/2025, 16:35 UTC, antecede o upload de 17:17 UTC; data e versão 1.1.5 restringem a proveniência, **não provam equivalência integral de métodos com o JAR**. A inspeção `javap` abaixo confirma somente os literais/chamadas declarados, sem certificado de equivalência nem aceite físico.

Build do candidato: **NeoForge 21.1.187 / Iron’s 3.14.8**; pack: **NeoForge 21.1.250 / Iron’s 3.16.3**. O host consultado é `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`; seus contratos abaixo são condicionais à composição real do pack. Defaults não são configuração implantada. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.1.5.md). Metadata **All Rights Reserved**; MIT do template é limitada aos arquivos do template. Apenas fatos, paráfrases e permalinks, sem importar código ou assets.

Esta classe não sobrescreve aquisição, aprendizado ou resolver de pre-cast. A escola usa constructor host com requiresLearning=false/allowLooting=true; crafting ainda depende da config e origem/admissão do host. Isso é elegibilidade, sem garantir scroll/rota Survival. [Spell][spell], [constructor escolar][school-constructor], [aquisição host][acquisition-host].

Nome de exibição upstream **Devastating Cut**, ID preservado calamity_cut. [Guia][guide], parafraseado: corte à frente cuja força inclui a arma. Não criar segunda identidade pelo nome público.

## Localizadores e unidades

`L` é o nível recebido pelo executor; `P` usa os fatores host `SPELL_POWER × SpiritPower × POWER_MULTIPLIER`. Multiplicadores 1 definem o cenário neutro, sem afirmar configuração implantada. Dano é expresso em HP pedidos; 20 ticks correspondem a 1 s nominal, distâncias a blocks e velocidades a blocks/tick. Não confundir tentativa do helper, retorno de `hurt` e perda final de HP. [Escala, mana e tempo host][power].

| Campo | Classe e métodos concretos / autoridade |
| --- | --- |
| Defaults, tempo e gate | `CalamityCutSpell#<init>/getDefaultConfig/getCastType/getEffectiveCastTime/canBeInterrupted`; custo em `AbstractSpell#getManaCost`. [Spell][spell], [host][power]. |
| Range, dano e arma | `CalamityCutSpell#getRange/getDamage/getAdditionalDamage`; `Utils#getWeaponDamage`, `AbstractSpell#getSpellPower`. [Helpers][helpers], [arma][weapon], [host][power]. |
| Query, filtros e settlement | `CalamityCutSpell#onCast`, `DamageSources#applyDamage`, `EnchantmentHelper#doPostAttackEffects`. [Executor][execution], [helper][damage-host]. |
| Visual e saída | `CalamityCutSpell#onCast` usa clip visual/partículas e termina síncrono; sem projétil ou save local. [Executor][execution]. |

## Fórmulas, geometria e settlement

`P=(4+4(L−1))×SPELL_POWER×SpiritPower×POWER_MULTIPLIER`; `W=Utils.getWeaponDamage(caster)`; `D=P+W` health points. O helper W lê ATTACK_DAMAGE efetivo, retorna 0 quando não supera o atributo base e considera Sharpness conforme item; não é somente o número da tooltip da arma. P/W são consultados no loop para cada tentativa, não snapshot único demonstrado. Defaults L 1–5: P 4–20, mana 30–102, count/range `R=9+2L`=11–19. [Spell][spell], [helpers][helpers], [arma][weapon], [power][power].

1. **Cast/custos:** LONG, getEffectiveCastTime retorna getCastTime: **24 ticks=1.2 s sem redução pelo atributo** neste override. canBeInterrupted=false; não implica imunidade a toda remoção/validação externa. Mana `int((30+18(L−1))×MANA_MULTIPLIER)`, cooldown 25 s=500 ticks antes de modifiers; sem recast/charge. Wrapper host valida/cobra antes do onCast; cooldown não é o tempo da animação. [Tempo/defaults][spell], [host][cast-host].
2. **Origem/direção:** forward é caster.forward com Y zerado e normalizado. Start=caster.eye−Y0.5+forward×1.5. Loop inteiro i=0 enquanto i<R cria centros start+forward×i; para defaults, último centro fica a R+0.5 blocks horizontais do caster, antes de considerar corpo dos alvos. Vetor horizontal degenerado ao olhar vertical/obstruções/terreno exige QA. [Executor][execution].
3. **Query real:** cada centro usa **AABB 0.5×1.5×0.5 blocks**, espaçamento 1 block. São caixas discretas com intervalos, não cilindro/linha contínua de largura 1 ou um único raycast de dano. A query exclui o caster, depois exige alive+pickable+LOS do centro+Y1 ao centro da AABB da vítima. Não possui filtro local de facção/PvP/claims/cap global nem ledger entre segmentos; uma AABB de alvo pode tocar várias caixas e receber várias tentativas. O helper ainda decide friendly fire para Living com SpellDamageSource. [Query][execution], [helper][damage-host].
4. **Terminal:** por Entity elegível cria fonte via getDamageSource(caster), direta/causadora=caster; default **spirit_magic**. applyDamage usa D=P+W e, apenas quando retorna true, chama EnchantmentHelper.doPostAttackEffects com `(ServerLevel)level`. O método não tem guarda local de lado; o wrapper normal é servidor. O cast explícito e encantamentos posteriores precisam teste em ingressos diretos; não prometer status/enchantment específico nem tratar sucesso do helper como HP exato. [Executor][execution], [tipo][source-type], [escola][school].
5. **Visual/saída:** ray visual de cada centro até 2 blocks abaixo só posiciona partículas; não desloca a caixa de dano para o solo. CameraShake 10 ticks/radius 10 é apresentação. Sem entidade de dano, timer/DOT/summon/rollback de bloco próprio; super.onCast final cuida do som. Interrupção/falha externa não desfaz tentativas já processadas. [Executor][execution].

**Inspeção binária estreita:** no publisher SHA-1 citado, `CalamityCutSpell#getEffectiveCastTime` chama `getCastTime` (offset 2), `#getRange` usa os literais 9 e 2 (offsets 0/3), e `#onCast` chama `AABB.ofSize` (188), `DamageSources.applyDamage` (284) e `EnchantmentHelper.doPostAttackEffects` (298). Esses achados corroboram os campos e consumers descritos; não demonstram equivalência do método inteiro, comportamento do host 3.16.3 ou HP final. [Métodos do candidato][spell], [query][execution], [helpers][helpers].

**N/A comprovados:** `CalamityCutSpell#onCast` resolve as caixas no mesmo callback, sem criar entidade de dano, projétil, summon/AI, DoT, cura, ritual ou mutação de blocos. Speed, aceleração, pierce, lifetime e NBT de projétil são N/A; não há ledger persistente de vítimas entre as caixas. [Executor][execution].

## Matriz para perks

**Leitura de mutabilidade:** `NATIVE_ATTRIBUTE` = atributo consumido no caminho indicado; `CONFIG_NATIVE` = configuração global; `HOOK_VERIFICADO` = campo realmente mutável no evento host citado; `CONDITIONAL` = adapter ainda não implementado/validado; `⛔ SEM_HOOK_SEGURO` = alteração sem seam específico demonstrado. Os hooks gerais de cast/dano não expõem alvo, geometria, tipo ou contagem automaticamente; ver [contrato comum](../SPELL-PERK-BOUNDARIES-1.1.5.md).

| Eixo | Valor, consumidor e fase | Superfície real / limite | QA |
| --- | --- | --- | --- |
| Dano/power/arma | D=P+W por tentativa; nível máximo default 5. [Helpers][helpers], [arma][weapon]. | SPELL_POWER/spirit_spell_power/ATTACK_DAMAGE são inputs nativos nos seus consumers; POWER_MULTIPLIER **CONFIG_NATIVE global**. SpellDamageEvent amount/cancel **HOOK_VERIFICADO** para helper Living; adapter por spell/caster/alvo/segmento **CONDITIONAL**. | Q1/Q3 |
| Tipo/crítico/status | SpellDamageSource spirit_magic; enchant post-attack só helper=true; sem crit/status próprio definido. [Fonte][source], [executor][execution]. | Sem setter de DamageType no evento; conversão/crítico ou segundo post-hit **⛔ SEM_HOOK_SEGURO**. Encantamentos/tags/mitigação downstream próprios. | Q3 |
| Alcance | R=9+2L é número/limite do loop; centros 1.5..R+0.5 à frente. [Helpers][helpers], [executor][execution]. | Getter range é privado; mudarL afeta também P/custo consultado anteriormente. Bônus de range isolado **⛔ SEM_HOOK_SEGURO**. Não chamar R de cap de distância do centro da vítima. | Q2 |
| Área/targeting/budget | Caixas 0.5×1.5×0.5, intervaladas 1, LOS por alvo, sem ledger entre caixas. [Query][execution]. | Não há callback mutável de resolver/caixas/cap. Single→AOE, ampliar largura, remover LOS e dedup por perk **⛔ SEM_HOOK_SEGURO**; não executar outra linha paralela. | Q2/Q3 |
| Tempo/cooldown | LONG 24 fixo no override; cooldown 25 s default; canBeInterrupted=false local. [Tempo][spell]. | Redução de cast nativa não é consumida aqui. Cooldown config/atributo/evento host no [comum](../SPELL-PERK-BOUNDARIES-1.1.5.md) é seam real, adapter **CONDITIONAL**; não altera quantidade de caixas. | Q1/Q4 |
| Mana/nível/recast | `int((30+18(L−1))×config)`, sem charge/recast local. [Power][power]. | SpellOnCastEvent#setManaCost/setSpellLevel reais pré-onCast; mudar nível não recalcula custo/admissão automaticamente. Sem segunda cobrança/refund paralelo. | Q1 |
| Projétil/summon/mundo | **N/A** projétil de dano/AI/slots. Partículas seguem clip visual 2 e câmera 10 ticks/r 10. [Executor][execution]. | Não transformar VFX em entidade/hitbox nem adicionar block break/fire/heal por observar a animação. Efeitos de mundo extras **⛔ fail-closed**. | Q2/Q4 |
| Ownership/persistência | Caster é fonte; execução síncrona sem cast-token/ledger persistente local. [Executor][execution]. | Correlacionar tentativa/segmento/vítima e resultado real; sem Mastery por partícula/enchantment/cada caixa. Mastery custom condicionada no [comum](../SPELL-PERK-BOUNDARIES-1.1.5.md). | Q3/Q4 |

Assinatura ocupada: corte linear por amostras discretas, arma+Spirit power, wind-up não redutível pelo caminho consultado e post-attack condicionado ao helper. Magia original requer definição própria de continuidade, cap e confirmação de alvo, sem clonar source/assets.

- **Q1:** config/origem/Survival, mana/cooldown/atributos, L 1–5, arma/fist/Sharpness e valores que mudam durante o loop; tempo 24 versus atributo de redução.
- **Q2:** pitch vertical, caixas/gaps/alvos largos/multissegmento, LOS, blocos/altura do terreno/claims/PvP/aliados, count/range e performance.
- **Q3:** SpellDamageEvent veto/amount/resistência/HP/iFrames, tentativas repetidas, enchant somente após true, side/cast ServerLevel e atribuição.
- **Q4:** cancelamento externo/direto, efeitos já executados, cliente/dedicado/multiplayer/Survival e Mastery. **Todos PENDING**; sem runtime ou adapter novo.

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
[guide]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/resources/assets/iss_magicfromtheeast/lang/en_us.json#L45-L46
[spell]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/CalamityCutSpell.java#L37-L86
[execution]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/CalamityCutSpell.java#L99-L123
[helpers]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/CalamityCutSpell.java#L125-L152
[weapon]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L787-L801
