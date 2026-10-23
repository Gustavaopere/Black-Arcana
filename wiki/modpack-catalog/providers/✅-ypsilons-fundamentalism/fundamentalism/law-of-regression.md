# Law Of Regression

**Dossiê técnico documental — 22/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; host `CONDITIONAL`; QA físico `PENDING`. **+0 magias**: cura, evento e limpeza são resultados desta identidade.

## Identidade e proveniência

| Campo | Evidência e limite |
|---|---|
| Provider / objeto | Ypsilon's Fundamentalism / Fundamental Principles; `mod_id=ypfundamentals`; spell Iron's `ypfundamentals:law_of_regression`; display **Law Of Regression**; escola default `ypfundamentals:fundamentalism`. |
| Artefato físico histórico | Minecraft 1.21.1 / NeoForge; `ypfundamentals-1.1.7.1.jar`; SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`; [publicação 8558503](https://www.curseforge.com/minecraft/mc-mods/fundamental-principles/files/8558503). [Auditoria Java21 de 13/10/2026](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38436717443) SUCCESS prova registry/classe; não métodos/execução. [Dossiê binário](../EXACT-BINARY-SPELLS-1.1.7.1.md). |
| Source da lógica | `ypsilonM/FundamentalPrinciples-1.21.1@a9b8f8222fb2a800edece8c1568984bd2a764fc2`; `com.ypsi.fundamentalism.spells.fundamentalism.LawOfRegressionSpell`. [Registry `ModSpells#LAW_OF_REGRESSION_SPELL`][registry], [ID/constructor/defaults][defaults]. |
| Host e compatibilidade | Source do addon declara Iron's **3.16.2**; pack usa **3.16.3**. Host consultado: `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`. Consulta não prova equivalência binária dos hosts; ver [boundaries comuns](../SPELL-PERK-BOUNDARIES-1.1.7.1.md). |
| Descrição oficial | [Guia upstream, chave `.guide`][guide], parafraseado: recupera o corpo do próprio conjurador. Consulta e referências apenas; sem copiar código/textos extensos/assets nem conceder licença de redistribuição. |

## Ingresso, gates e sequência causal

1. **Aquisição:** `requiresLearning=true`, loot/crafting desabilitados em [`LawOfRegressionSpell`][acquisition]. `PrinciplesLevelsAttachment#setLevel(Player,String,int)` limita Principles a `0..20`; ao alterar Remedium para `>=5`, chama `learnSpell`. O [switch do attachment][learn] e [`ModEvents#spellSelectionManager`][selection] oferecem `remedium_slot`: Remedium `5..9 → nível 1`, `10..13 → 2`, `14..16 e 18..19 → 3`, `20 → 4`. **17 foi omitido nos dois switches:** aprende pelo teste `>=5`, mas esses branches não oferecem nível/trigger para 17. Unlock/seleção nesses trechos não testam `PRINCIPLES_SYSTEM` diretamente; configuração/progressão efetivas pendentes.
2. **Admissão no servidor:** host `AbstractSpell#attemptInitiateCast` verifica casting, aprendizado, mana/cooldown segundo `CastSource`, precondições e `SpellPreCastEvent`. A precondição de alvo de Law está **comentada**; a herdada retorna `true`. Nenhum range/raycast ou alvo externo ativo. [Host][host-cast]. Burnout/Chained podem negar e interromper pelo [listener global][gates].
3. **Canalização:** `CONTINUOUS`, `castTime=200 ticks` base. Iron's 3.16.3 resolve `round(200×CAST_TIME_REDUCTION)`; `MagicManager#tick` chama `castSpell` quando o tempo restante é múltiplo de **10 ticks**. No ramo terminal há uma resolução ao chegar a `<=0` ou se `mana < 2×getManaCost(L)`. [Duração][host-time]; [scheduler][scheduler]. Isso não fixa total de cura observado: interrupção, origem, eventos e mana mudam o número de resoluções.
4. **Cada resolução:** host publica `SpellOnCastEvent`, debita seu `manaCost` quando a origem consome mana e passa seu `spellLevel` a `onCast`. Law define `healAmount=spellLevel`, publica `SpellHealEvent(caster,caster,healAmount,school)`, chama `caster.heal(healAmount)` e `removeEffectsCuredBy(HONEY)`. Não chama `super.onCast`. [Host][host-cast]; [efeito ativo separado do código comentado][effect]. Não cobrar mana única por canalização nem aplicar cura em outro loop.
5. **Saída:** cura tentada em health points, sujeita a `LivingEntity#heal` e listeners; recebimento pode ser menor. HONEY não significa todos os debuffs. Emite **2 partículas** por resolução, no servidor. Cooldown final/interrupção pertence ao host; [regras comuns](../SPELL-PERK-BOUNDARIES-1.1.7.1.md). Não invoca efeito autônomo; aprendizado/sync/persistência pertencem ao host/attachment.

**Evento de cura é observação:** no [Iron's 3.16.3, `SpellHealEvent`][heal-event], `healAmount` é `final`, há somente getters e o evento não implementa cancelamento. Law não usa retorno de `post` para decidir a cura. Esse evento **não** permite setter/cancelamento pré-cura. [`ModEvents#reverseCurseTechnique`][remedium] retorna imediatamente para escola Fundamentalism: não cobrar novamente comida da passiva Remedium no default desta magia. Outra escola configurada exige revalidar o ramo.

## Parâmetros e superfícies para perks

`L` é o nível recebido por `onCast`; números são defaults de source, não config implantada. `M=MANA_MULTIPLIER`. Status: **NATIVE / CONFIG_NATIVE**, **HOOK_VERIFICADO**, **CONDITIONAL / CONTRATO_CONDICIONAL** ou **⛔ SEM_HOOK_SEGURO**. Método público não significa hook de alteração.

| Eixo | Valor / fórmula e localizador | Fase, boundary e mutabilidade | Limite / QA |
|---|---|---|---|
| Cura / dano / tipo | Cura tentada `L health points` por `onCast`; níveis default `1..4`. Dano, DamageType, crit, DOT e knockback: **N/A**. Power declarado `1+(L−1)`, mas cura não usa `getSpellPower`. [`onCast`][effect]. | Servidor antes de `heal`: `SpellOnCastEvent#setSpellLevel(int)` altera L entregue: **HOOK_VERIFICADO** no host, **CONDITIONAL** para adapter. `SpellHealEvent` apenas observa: **⛔ SEM_HOOK_SEGURO** para editar cura nesse evento. | `SPELL_POWER`, power da escola e `POWER_MULTIPLIER` não aumentam diretamente essa cura. Não exceder níveis auditados. Testar cura parcial/vida cheia/listeners. |
| Alcance / targeting | **Self**; aquisição/impacto no caster; range externo/LOS: **N/A**. Targeting externo é código comentado. [`onCast`][effect]. | Servidor, `entity` literal; **⛔ SEM_HOOK_SEGURO** para redirecionar/selecionar aliado. | Level 4 continua self. Não criar cast paralelo. |
| Área / alvos | 1 caster por resolução; raio/cone/altura de área: **N/A**. [`onCast`][effect]. | Servidor, mesma chamada `heal`; **⛔ SEM_HOOK_SEGURO** para target único→área. | Partículas não constituem área; evento não prova cura recebida. |
| Projétil / hitbox / visual | Projétil, velocidade, pierce, lifetime e hitbox própria: **N/A**. 2 partículas, dispersão `(0.05,0,0.05) blocks`, velocidade de emissão `0.01`, centro `Y+bbHeight/2`. [`onCast`][effect]. | Servidor emite VFX a clientes; **⛔ SEM_HOOK_SEGURO** para converter VFX em colisão. | QA cliente de emissão/cancelamento. |
| Cast / pulsos / interrupção | Base `200 ticks=10 s`; efetivo `round(200×CAST_TIME_REDUCTION)`; oportunidades `%10==0`. [`getEffectiveCastTime`][host-time], [`MagicManager#tick`][scheduler]. | Atributo **NATIVE**; scheduler provider-owned. | Não prometer 20 pulsos nem `200×L` de cura. QA primeira/última resolução, interrupção e mana. |
| Mana / owner | `int((80−10×(L−1))×M)` por `castSpell`; `M=1`: `80/70/60/50 mana`. [`constructor`][defaults], [`getManaCost/castSpell`][host-cast]. | `MagicData` do caster. Config global **CONFIG_NATIVE**; `SpellOnCastEvent#setManaCost(int)` **HOOK_VERIFICADO**, antes do débito e depois da admissão. | Desconto tardio não altera admissão nem teste terminal `2×getManaCost`. Sem reserva/refund próprio. QA por origem, Creative e listeners. |
| Cooldown / recast | Default `5 s=100 ticks`; atributos/config resolvidos antes de `SpellCooldownAddedEvent.Pre`. `getRecastCount=0` herdado; nenhum recast próprio. [`defaults`][defaults], [host][cooldown]. | Config/`COOLDOWN_REDUCTION`: **NATIVE**; `Pre#setEffectiveCooldown(int)` **HOOK_VERIFICADO** antes da inserção. | Pre não desfaz efeito. Não rearmar proc por pulso nem duplicar Repetitio. QA fim/interrupção. |
| Estados / summons / mundo | Limpeza HONEY em self; summons/blocos/teleport/rollback: **N/A**. [`onCast`][effect]. | Depois de `heal`; **⛔ SEM_HOOK_SEGURO** para substituir cure set. | Testar efeitos com/sem cure HONEY, mantendo efeitos não curáveis. |

## Autoria, deduplicação e concepção

Iron's possui intenção/mana/cast/cooldown; Ypsilon possui aprendizado/Principles e efeito terminal. RPG Skill Tree possui sua progressão e Black Arcana não possui esta canalização. Observar evento não autoriza nova cura. Distinguir **cast/canalização** de cada `onCast` e seu `SpellHealEvent`: os últimos descrevem o mesmo pulso. O evento de cura não contém spell ID nem token do cast; escola/caster/tick não prova identidade inequívoca entre providers. Não contar VFX, cura e limpeza como procs independentes.

Assinatura ocupada: cura contínua pessoal com purga por mel e aprendizado por Remedium. Nova cura aliada/área ou outra purga exige identidade/targeting próprios; nenhuma implementação é proposta aqui.

## Verificação e pendências

| Dimensão | Estado |
|---|---|
| Registry/classe no JAR histórico | `COUNTED_EXACT`, prova de 13/10 separada de lógica. |
| Parâmetros / causalidade source | Auditados nos pins; cura literal por nível, evento observacional e Remedium 17 confirmados. |
| Config efetiva / host 3.16.2→3.16.3 | `CONDITIONAL`; revalidar JAR exato/ordenação de listeners. |
| Servidor / cliente / Survival | `PENDING`: unlock 4/5/9/10/13/14/16/17/18/19/20, sync/relogin, pulsos/mana, interrupção/cooldown, HONEY/coexistência. |
| Perk / adapter / runtime novo | Nenhum implementado. Target único→área, troca de tipo e hitbox: **⛔ fail-closed**. |

[registry]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/ModSpells.java#L69-L73
[defaults]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fundamentalism/LawOfRegressionSpell.java#L47-L80
[effect]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fundamentalism/LawOfRegressionSpell.java#L88-L137
[acquisition]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/spells/fundamentalism/LawOfRegressionSpell.java#L139-L150
[learn]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/attachments/customAtt/PrinciplesLevelsAttachment.java#L88-L151
[selection]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/event/ModEvents.java#L222-L250
[gates]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/event/ModEvents.java#L516-L562
[remedium]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/event/ModEvents.java#L1027-L1040
[guide]: https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/resources/assets/ypfundamentals/lang/en_us.json#L79
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L401
[host-time]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L230-L257
[scheduler]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/MagicManager.java#L26-L92
[heal-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellHealEvent.java#L18-L41
[cooldown]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/MagicManager.java#L94-L122
