# Crystalline Carver

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades/+0 strict**: efeitos, entidades e fases derivados não são novas spells.

## Identidade e proveniência

Provider **Discerning The Eldritch**, `mod_id=discerning_the_eldritch`, JAR físico histórico **`discerning_the_eldritch-1.4.4-1.21.jar`**, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`; [publisher CF8816497](https://www.curseforge.com/minecraft/mc-mods/discerning-the-eldritch/files/8816497), [prova estática de identidade](../EXACT-BINARY-SPELLS-1.4.4-1.21.md). Source oficial `AceTheEldritchKing/Discerning_The_Eldritch@7bbd81f902c65a4452f47656ebd948cae8cd5833`. Build Iron’s 3.16.2/NeoForge 21.1.244/Azure 3.1.0 versus pack Iron’s 3.16.3/NeoForge 21.1.250/Azure 3.1.11; Ace 1.2.7.2 coincide na versão declarada, sem prova de ABI. Host lido Iron’s `e4056af90302d37eb1739f5ff05020b020e6e252`. Versão declarada não equipara métodos source↔JAR. Sinais MIT/PolyForm Shield conflitantes: fatos/paráfrases/permalinks, sem importar implementação/assets. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md).

Spell **`discerning_the_eldritch:crystalline_carver`**, escola default `irons_spellbooks:ice`, Rare, níveis default1–5; declarante `net.acetheeldritchking.discerning_the_eldritch.spells.ice.CrystallineCarverSpell`. [Defaults][spell]. [Guia oficial][guide], parafraseado: golpes próximos aplicam Chilled e preparam um golpe final reforçado. O bônus source lê **attachment FROSTBITE_LEVEL**, não o amplifier do MobEffect Chilled.

Sem override local de crafting/loot/learning/precondição: aquisição e origens seguem host/config, rota concreta Survival **NÃO VERIFICADA**. Admissão/custo/gates externos no [contrato comum](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md). [Wrapper][host-cast], [aquisição][acquisition].

## Fórmulas e valores neutros

`P=(5+2(L−1))×SPELL_POWER×ICE_SPELL_POWER×POWER_MULTIPLIER`; `W=Utils#getWeaponDamage(caster)`; dano base final **`B=.5P+W` HP**. No callback final, Living com Chilled usa B+A (A=attachment inteiro atual); sem Chilled usa B. Se Living e mainhand tag FROZEN_WEAPONS, multiplica a expressão inteira por1.5. NonLiving usa B, **sem multiplicador da tag**. P/W/tag são resolvidos **no callback**, não congelados em cada golpe de preparação. [Finisher][finish], [helper de dano][damage], [arma][weapon], [power][host-power].

| L default | Mana neutra | P neutro | B sem arma | Total casts solicitado / janela |
|---|---|---|---|---|
| 1 | 50 | 5 | 2.5 HP | 1 /160ticks |
| 2 | 55 | 7 | 3.5 HP | 2 /160ticks |
| 3 | 60 | 9 | 4.5 HP | 3 /160ticks |
| 4 | 65 | 11 | 5.5 HP | 4 /160ticks |
| 5 | 70 | 13 | 6.5 HP | 5 /160ticks |

Sem cap/clamp próprio de A no cálculo; efeito/item/datapack/attachments externos podem mudar inputs. Máximo default5 não é garantia de A≤5, pois diferentes casts/casters podem acumular o mesmo attachment da vítima. [Setup][setup], [attachment][attachment].

## Pipeline causal, recast e estado compartilhado

1. **Admissão/tempo:** field `isFinalCast` pertence ao objeto Spell registrado, sem chave de caster. Quando true, getCastType=LONG e canBeInterrupted=false; quando false, INSTANT e true. Override getEffectiveCastTime retorna getCastTime em ambos ramos: **host retorna0 para INSTANT e campo20ticks para LONG**, bypassando o atributo CAST_TIME_REDUCTION. Portanto não é20fixo em toda fase. CastType/animação/tempo da admissão dependem do valor compartilhado naquele instante, não de uma garantia de “último golpe” por jogador. [Flag/tempo][state], [host getter][host-power].
2. **Recast/cobrança:** onCast sem recast ativo adiciona RecastInstance(id,L,total=L,160ticks,origem,null). Host constructor grava remaining=L−1; wrapper jogador não decrementa a instância recém-criada, não cobra mana outra vez enquanto recast ativo e renova janela a cada decrement com remaining>0. Após setup, escreve `isFinalCast=(remaining consultado==2)` **antes do decrement externo do host**. Não interpretar essa flag como autoridade transacional do combo. [Setup/flag][setup], [constructor][recast-instance], [wrapper][host-cast], [manager][recasts].
3. **L1/timeout:** total1 gera remaining0, que não é ativo pelo predicate host. O decrement normal só produz USED_ALL_RECASTS quando uma instância ativa chega a0; timeout produz TIMEOUT. Não prometer finisher funcional L1 só pelo tooltip/registro: confirmar o caminho físico, comandos e callbacks. [Active/decrement/tick][recasts], [success][recast-result].
4. **Setup:** posição=`casterPos+(0,.3×altura,0)+forward.multiply(1.5,.35,1.5)`; query caixa **6.5×3.25×6.5 blocks**. Filtros: caster.isPickable, d²<3.25², LOS e alvo nãoItem. Para Living incrementa attachment A+1 e pede Chilled60ticks/amp0, sem dano. Não exige ally/PvP/living-alive ou retorno true de addEffect antes do incremento. A caixa não é um cone com teste de forward adicional. [Setup][setup].
5. **Finalização:** `#onRecastFinished` chama super primeiro (host adiciona cooldown) e só executa finisher se recastResult.isSuccess, que neste host é **USED_ALL_RECASTS**; timeout/death/counterspell/user cancel não entram. Nova query em posição forward.multiply(1.2,.35,1.2), caixa **4.3×2.15×4.3**, distância<2.15/LOS/caster-pickable/nãoItem. Não reutiliza lista de vítimas do setup. Tenta helper com B ou fórmula acima; partículas/enchantments locais só quando helper=true. [Callback][finish], [host callback][host-finish], [success][recast-result].
6. **Reset abrangente:** `target.setData(FROSTBITE_LEVEL,0)` fica **fora dos filtros internos** e ocorre para cada Entity retornado pela caixa final, inclusive Item/fora da distância/semLOS/não-pickable caster. Também reseta quando dano cancela/falha. Não há restore local do attachment em falha. Timeout não entra nesse loop, logo não demonstra limpar stacks de setups anteriores. [Reset][finish-end].
7. **Fonte:** SpellDamageSource Ice padrão, direta/causing=caster, sem freezeTicks80 ou iFrames custom da GlacialEdge. Helper Living publica SpellDamageEvent antes de resist/friendly/hurt; nonLiving cai no hurt direto desse helper. Chilled do setup é independente desse settlement posterior. [Host source][source-host], [escola][school], [helper][helper].
8. **VFX/estado/save:** setup e sucesso criam CrystalCarveEntity e setIsFinal(false/true), sem passar dano/owner do combo. applyEffect desse filho é vazio; renderer/entidade visual não executa o finisher. Registro5×1 não substitui dimensões herdadas de AoeEntity; deathTime=8ticks e shouldBeSaved=false, override tick sem super. Attachment FROSTBITE_LEVEL default0 usa Codec.INT serialize, distinto da classe FrostbitePotionEffect vazia. Recast ativo pode salvar via host; flag singleton não tem persistência por caster neste source. Sync/cleanup/multiplayer exigem QA. [Visual][visual], [visual registry][entity], [attachment][attachment], [effect marker][marker], [save recasts][recasts].

## Matriz de alteração por perks

| Eixo | Valor / consumer / fase | Boundary real e limite | QA |
|---|---|---|---|
| Dano / power / arma / cap | B=.5P+W; LivingChilled somaA, Livingtag×1.5; NonLiving sóB, no callback bem-sucedido. [Finish][finish], [damage][damage]. | SPELL_POWER/ICE_SPELL_POWER **NATIVE_ATTRIBUTE**, POWER_MULTIPLIER **CONFIG_NATIVE**; SpellDamageEvent amount/cancel **HOOK_VERIFICADO** no helper Living, adapter **CONDITIONAL**. Sem capA/crítico próprios; não snapshot por preparação. | Q1/Q2 |
| Tipo / Chilled / Frostbite | IceSource padrão; setup Chilled60/amp0+attachmentA+1, callback consome/resetA. [Setup][setup], [attachment][attachment]. | Amount setter não muda DamageType, attachment não é amplifier. Conversão/stack cap/reset/tempo de status por perk **⛔ SEM_HOOK_SEGURO** até seam completo pré-efeito; sem ledger paralelo RPG. | Q2/Q3 |
| Alcance / targeting | Setup d<3.25/box6.5×3.25×6.5, final d<2.15/box4.3×2.15×4.3; LOS e filtros diferentes do reset. [Setup][setup], [finish][finish]. | Sem resolver/raio mutável localizado; ampliar só uma fase muda quem acumula/recebe/reset. Range/retarget/single→AOE **⛔ SEM_HOOK_SEGURO** sem adapter de todas fases. | Q2/Q3 |
| Área / budgets / ownership | Nenhum cap/ordenação de alvos local; attachment é da vítima e compartilhável entre casters, não token de combo. [Setup][setup], [reset][finish-end]. | Radius/friendly/protection/sync por perk **⛔ SEM_HOOK_SEGURO**; callback não autoriza takeover de stacks alheios. | Q3/Q4 |
| Projétil / apresentação | CrystalCarveEntity VFX, applyEffect vazio; flags final/mirrored sincronizadas. [Visual][visual]. | Hitbox/speed/pierce de projétil de dano **N/A**. Setter visual final não é setter de dano/fase de combo. | Q2/Q4 |
| Cast / tempo / interrupção | INSTANT0 ou LONG20 conforme flag singleton; CTR bypass; flag atualizada com remaining==2 antes do decrement externo. [State][state], [setup][setup]. | **NÃO VERIFICADO** isolamento entre casters; atributo CTR não resolve esse override. Tempo/animação/interrupção independente **⛔ SEM_HOOK_SEGURO**, não escrever field compartilhado por perk. | Q1/Q4 |
| Mana / recast / cooldown | Mana `int((50+5(L−1))×config)`, totalL, janela160 renovável; cooldown35s=700ticks, base chama antes do finisher. [Defaults][spell], [recasts][recasts]. | Mana/level/cooldown events genéricos **HOOK_VERIFICADO**, integração **CONDITIONAL** no [contrato comum](../SPELL-PERK-BOUNDARIES-1.4.4-1.21.md). Nível altera total/P/custo previamente calculado; sem segunda cobrança ou ledger de combo. | Q1/Q4 |
| Mundo / summons / saída | Sem bloco/teleporte/summonAI próprios; estados, callback e visual têm lifecycle distinto. [Visual][visual], [finish][finish]. | Summon knobs **N/A**; save/restart/relog/morte/cancel/reset/flag e proteção **PENDING**. Não contar visual/frostbite/final como novos casts. | Q3/Q4 |

## Ownership, concepção e pendências

DTE/Iron’s possuem recast, cobrança, attachment, Chilled, finisher e VFX; RPG progressão/Mastery, BA seus casts/world safety e Enshrouded seus efeitos/classificação. Dedup caster/spell/recast→setup/vítima→success→finalhelper/reset; não creditar partículas, incrementos ou finisher como lançamentos independentes. Assinatura ocupada: preparação Ice com attachment e finisher weapon-scaled em outro alcance. Uma nova magia com estado isolado por caster/rollback requer contrato original, não editar singleton externo ou duplicar execução.

- **Q1:** config/Survival/origens, L1/2/3/5 e extrapolação, mana inicial/recasts, timeout e35s cooldown antes/depois de success, flag0/20 versus CTR.
- **Q2:** caixas/LOS/posição/pickableCaster/Item/NonLiving, Chilled recusado/refresh, power/W/tag no callback, amount0/cancel/resist/hurtfalse, tipo e ausência de freeze custom.
- **Q3:** dois casters/mesma vítima/Aalto ou externo, setup fora do alcance final, reset fora de filtros/Item/semLOS/failedhurt, timeout sem loop, ownership e persistência do attachment.
- **Q4:** singleton concorrente/anim/interrupção, dedicado/cliente/recast sync, logout/death/restart/unload, saveactive/token/visual8ticks/budgets, dedup. **Todos físicos PENDING**, sem novo adapter/perk/runtime.

[versions]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/gradle.properties#L11-L48
[host-power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L160-L257
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L333
[helper]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L119
[weapon]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L787-L802
[source-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/SpellDamageSource.java#L24-L71
[spell]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/ice/CrystallineCarverSpell.java#L47-L74
[guide]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/resources/assets/discerning_the_eldritch/lang/en_us.json#L197-L198
[acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L612
[state]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/ice/CrystallineCarverSpell.java#L86-L128
[setup]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/ice/CrystallineCarverSpell.java#L151-L196
[finish]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/ice/CrystallineCarverSpell.java#L199-L277
[finish-end]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/ice/CrystallineCarverSpell.java#L267-L290
[damage]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/spells/ice/CrystallineCarverSpell.java#L292-L304
[attachment]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEAttachmentRegistry.java#L12-L28
[marker]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/effects/FrostbitePotionEffect.java#L1-L10
[visual]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/entity/spells/crystal_carve/CrystalCarveEntity.java#L17-L84
[entity]: https://github.com/AceTheEldritchKing/Discerning_The_Eldritch/blob/7bbd81f902c65a4452f47656ebd948cae8cd5833/src/main/java/net/acetheeldritchking/discerning_the_eldritch/registries/DTEEntityRegistry.java#L160-L166
[school]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/registry/SchoolRegistry.java#L69-L77
[recast-instance]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/RecastInstance.java#L27-L35
[recasts]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/PlayerRecasts.java#L46-L212
[recast-result]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/capabilities/magic/RecastResult.java#L3-L16
[host-finish]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L335-L347
