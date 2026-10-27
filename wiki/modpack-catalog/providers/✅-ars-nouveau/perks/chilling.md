# Ars Nouveau — Chilling

Status: `SOURCE-PINNED 5.13.1 / CONTRATO TÉCNICO ESTÁTICO / RUNTIME QA PENDING`

Aplica um estado antes da resolução de um Effect que implementa `IDamageEffect`. A intensidade e a duração usam o **slot da instância despachada**, não a soma nem o maior slot equipado. A aplicação do estado não confirma dano aceito.

## Contrato individual para perks

| Campo | Contrato source-pinned e limites |
|---|---|
| Identidade e versão | `ars_nouveau:thread_chilling`, `com.hollingsworth.arsnouveau.common.perk.ChillingPerk`, source5.13.1, registrado em produção [registry]. Mínimo `PerkSlot.ONE` (valor1), herdado; slots nativos1/2/3 [slot] [slot-values]. |
| Comportamento e causalidade | `PerkEvents.preEffectResolve` percorre cada instância equipada e chama `onEffectPreResolve` [dispatch] [instances]. Exige `IDamageEffect`, `EntityHitResult`, alvo `LivingEntity`, `damageEffect.canDamage(...)` verdadeiro e alvo diferente do shooter [perk]. Primeiro acrescenta1 a `ticksFrozen`, depois tenta aplicar `FREEZING_EFFECT`. |
| Parâmetros e consumidores | Para slot `s`: duração **200*s ticks** (10*s segundos), amplifier **2 se s>=3, senão1**; slots1/2/3 resultam200/400/600 ticks e amplifiers1/1/2 [perk]. `FreezingEffect` atualiza a cada tick: `frozen=min(ticksRequiredToFreeze+3, frozen+3+amplifier)` [freeze]. O +1 inicial é separado desse tick. |
| Targeting, dano e duração | Um alvo vivo já selecionado pelo Effect; sem aquisição, raio, projétil ou DamageType próprios. O default de `canDamage` rejeita vivo morto e aliado do shooter, mas implementações podem sobrescrevê-lo [damage-gate]. Não exige hit posterior nem sucesso de `hurt`; o listener roda antes de outros gates/callbacks do resolver [resolve]. |
| Custos, aquisição e gates | Enchanting Apparatus: Blank Thread como reagent; Blue Ice, Water Essence×2 e Powder Snow Bucket; resultado1 Thread, `sourceCost=0`, `keepNbtOfReagent=false` [recipe]. Instalação exige slot disponível, mínimo válido e divide1 item do stack no caminho observado [install]. Sem débito de mana, XP de glyph, cooldown ou cast próprio nesta classe; custo da magia subjacente permanece separado. |
| API, autoridade e deduplicação | Interface nativa `IEffectResolvePerk` e evento Pre são superfícies reais; não há contrato RPG/Black Arcana comprovado. Duplicatas continuam aparecendo em `getPerksFromLiving`; aviso de equipamento não remove os dados do holder [equipment] [instances]. Cada callback acrescenta frozen+1 e tenta um MobEffectInstance; não inferir soma de durações, máximo de slots ou refresh universal. O Thread não possui tag de estado própria (`getInitTag` default null); equipamento persiste pelo holder [slot] [component]. |
| Validação e pendências | Source e JSON gerado pinados, com referências de membros/linhas. A divergência entre descrição e amplifier executado está explícita; regras finais de substituição de MobEffect, freeze damage vanilla, imunidades e ordenação real exigem QA. Release SHA não prova bytecode desta perk; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. |

## Divergência da descrição e consumidores posteriores

A descrição diz que em slot3 passa a “Freezing2”, mas o código fornece amplifier1 nos slots1/2 e amplifier2 no slot3 [perk]. Amplifiers vanilla são índices; esta ficha preserva o número passado e não corrige o programa pela descrição. O consumidor `FreezingEffect` usa esse amplifier numericamente [freeze]; não confundir com bônus de dano direto.

`EffectColdSnap` consulta a presença de `FREEZING_EFFECT` e pode forçar `ticksRequiredToFreeze+3` após sua própria tentativa de dano [cold-snap]. Assim, Chilling pode preparar um consumidor posterior da cadeia; cancelar ou falhar o dano não cria rollback automático do estado já aplicado. O prefixo “Pre” é fase de resolução, não confirmação de hit ou crédito separado de progressão.

A [matriz de providers de slots](../systems/perk-slot-providers.md) localiza as peças e layouts suportados; a [visão dos Threads](README.md) mantém o inventário de aquisição.

## Evidência e fronteira de integração

**✅ `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`; `evidence_grade=PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Source oficial `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, Ars Nouveau **5.13.1**. Publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`: proveniência da release, sem prova específica de registry/classfile ou equivalência de métodos deste Thread. A auditoria binária dos109 IDs cobre glyphs e rituais, não Threads.

O Ars conserva equipamentos, slots, atributos, eventos e recursos nativos. RPG Skill Tree governa progressão/perks apenas por contrato comprovado; Black Arcana conserva casting, Corruption, Strain e WorldEffectPolicy próprios; Enshrouded conserva seus sistemas ambientais. APIs existentes não equivalem a um adapter seguro para alterar este comportamento ou premiar cada evento/tick como cast novo. Não duplicar efeitos, mana ou crédito de Mastery ao observar o mesmo caminho. Config instalada, addons, ordem de listeners, cliente/servidor, persistência física e integração executável continuam pendentes. Mudança de source, JAR, receita, equipamento ou consumidores exige reauditoria.

[registry]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/APIRegistry.java#L166-L185
[slot]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/IPerk.java#L52-L75
[slot-values]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/PerkSlot.java#L29-L36
[holder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/IPerkHolder.java#L19-L28
[armor-slots]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java#L54-L62
[instances]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/PerkUtil.java#L50-L81
[equipment]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/PerkEvents.java#L38-L85
[install]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/AlterationTile.java#L123-L150
[component]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java#L14-L26
[perk]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/perk/ChillingPerk.java#L15-L40
[dispatch]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/PerkEvents.java#L118-L125
[freeze]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/potions/FreezingEffect.java#L8-L22
[damage-gate]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/IDamageEffect.java#L24-L25
[resolve]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L203-L270
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/thread_chilling.json#L1-L26
[cold-snap]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectColdSnap.java#L43-L55
