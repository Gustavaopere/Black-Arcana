# Ars Nouveau — Kindling

Status: `SOURCE-PINNED 5.13.1 / CONTRATO TÉCNICO ESTÁTICO / RUNTIME QA PENDING`

Define o tempo de fogo do alvo antes do callback de um Effect de dano. **Substitui** `remainingFireTicks` por um valor do slot; não acrescenta segundos ao tempo anterior nem garante que o dano seguinte será aplicado.

## Contrato individual para perks

| Campo | Contrato source-pinned e limites |
|---|---|
| Identidade e versão | `ars_nouveau:thread_kindling`, `com.hollingsworth.arsnouveau.common.perk.IgnitePerk`, source5.13.1 e registro em produção [registry]. Mínimo `PerkSlot.ONE` herdado; valores nativos1/2/3 são slots de Thread, não nível de glyph [slot] [slot-values]. |
| Comportamento e causalidade | `PerkEvents.preEffectResolve` chama cada `IEffectResolvePerk` equipado [dispatch] [instances]. `IgnitePerk.onEffectPreResolve` exige `IDamageEffect`, `EntityHitResult`, `canDamage(...)` e alvo diferente do shooter; não exige explicitamente LivingEntity [perk]. Chama `setRemainingFireTicks` antes da resolução efetiva. |
| Parâmetros e semântica de escrita | Para slot `s`, **T=20*5*s=100*s ticks**:100/200/300 ticks (5/10/15 segundos) nos slots1/2/3 [perk]. É setter absoluto: pode encurtar fogo existente. O callback não lê o valor anterior, soma slots ou calcula máximo. Múltiplas instâncias executam em sequência, sujeitas à ordem de `getArmorSlots`/holder e eventos; último setter executado pode determinar o valor, sem garantir monotonicidade [instances]. |
| Targeting, geometria e dano | Alvo-entidade do Effect já selecionado; sem área, alcance, partícula/projétil, bloco ou DamageType próprios. O default de `canDamage` rejeita mortos/aliados, porém um Effect pode sobrescrever o predicado [damage-gate]. O setter não é `hurt`, não usa `SpellDamageEvent` e não comprova dano periódico final, imunidade ao fogo ou sobrevivência do status. |
| Custos, aquisição e gates | Apparatus: reagent Blank Thread; Magma Cream, Fire Essence e Fire Charge; resultado1, `sourceCost=0`, `keepNbtOfReagent=false` [recipe]. MínimoONE, instalação com slot disponível e `stack.split(1)` [install]. Não há mana, XP de glyph, cooldown ou custo por ignite nesta classe; pagamento da magia continua do provider. |
| API, autoridade e deduplicação | Superfície nativa real em Pre; adapter seguro RPG/Black Arcana continua não verificado. `getPerksFromLiving` mantém instâncias equipadas, e o aviso de duplicatas não remove o conteúdo do holder [equipment] [instances]. Não premiar cada setter/tick de fogo como novo cast. `getInitTag` herdado null; não há contador/cooldown persistente próprio neste Thread [slot] [component]. |
| Validação e limites | Source pinado e receita gerada conferidos. O resolver publica Pre antes de capabilities e do callback; um veto posterior pode deixar o fogo já alterado [resolve]. Nenhuma garantia de rollback, stacking final, dano vanilla ou QA de modpack; release SHA não comprova classe compilada. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. |

## Aplicação útil para uma perk futura

Alterar `SpellStats.durationMultiplier` não muda a fórmula deste Thread: o receptor lê `perkInstance.getSlot().value()` [perk]. Uma perk que queira preservar a maior duração, mudar o alvo ou escalar dano de fogo precisaria de outro contrato e fase comprovados; copiar o resultado do setter para um segundo proc duplicaria a mecânica nativa. O alvo não-self e o predicado do Effect não são um filtro universal de PvP ou claims.

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
[perk]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/perk/IgnitePerk.java#L12-L35
[dispatch]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/PerkEvents.java#L118-L125
[damage-gate]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/IDamageEffect.java#L24-L25
[resolve]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L203-L270
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/thread_kindling.json#L1-L23
