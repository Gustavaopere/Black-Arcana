# Ars Nouveau — Thread of Immolation

Status: `SOURCE-PINNED 5.13.1 / CONTRATO TÉCNICO ESTÁTICO / RUNTIME QA PENDING`

No evento de cast, troca fogo no caster por um status de100 ticks. O bônus de dano é consumido depois por `ArsEvents.preSpellDamage`; o tempo do status e a duração de uma magia de fogo são grandezas diferentes.

## Contrato individual para perks

| Campo | Contrato source-pinned e limites |
|---|---|
| Identidade e versão | `ars_nouveau:thread_immolation`, `com.hollingsworth.arsnouveau.common.perk.ImmolatePerk`, Ars5.13.1; registro de produção [registry]. MínimoONE herdado [slot]. Implementa `IEffectResolvePerk`, mas o override deste Thread é `onSpellCast`, não o callback Pre de Kindling/Chilling [perk]. |
| Comportamento e causalidade | Para cada instância despachada no `SpellCastEvent`, obtém caster de `context.getUnwrappedCaster` e `L=PerkUtil.countForPerk(INSTANCE,caster)` [perk] [cast-dispatch]. Se `isOnFire`, extingue e tenta aplicar `IMMOLATE_EFFECT`; separadamente, se o bloco exato em `caster.blockPosition()` pertence a `BlockTags.FIRE`, chama `removeBlock(pos,false)` e tenta aplicar o mesmo status. São dois if independentes; não há busca por fogo adjacente [perk]. |
| Parâmetros e consumidores | Duração fixa **100 ticks=5s**, amplifier **L−1**, onde L é o **maior valor de slot** equipado desta perk, não soma nem quantidade de itens [instances]. `ImmolateEffect` só define categoria BENEFICIAL/cor; o consumidor auditado em `ArsEvents.preSpellDamage` acrescenta **2*(amplifier+1)=2L** ao `SpellDamageEvent.Pre.damage` se a fonte está em `DamageTypeTags.IS_FIRE` e o caster possui o status [status] [fire-damage]. |
| Targeting, tipo de dano e tempo | Buff no caster; eventual remoção de um bloco na própria blockPosition, sem raio, projétil, seleção de terceiros ou dano direto no Thread. O consumidor usa tag IS_FIRE, não nome, escola ou glyph específico. O bônus entra no pipeline de SpellDamageEvent, não em todo `hurt` de fogo da engine [damage-pipeline]. O callback não testa claims localmente nem o booleano retornado por removeBlock; isso não prova comportamento no pack [perk]. |
| Custos, aquisição e gates | Apparatus: reagent Blank Thread, Fire Essence×3; resultado1, `sourceCost=0`, `keepNbtOfReagent=false` [recipe]. Instalação mínimoONE e `split(1)` em slot elegível [install]. Sem mana adicional/cooldown/XP de glyph próprios. `SpellResolver.onCast` publica SpellCastEvent após admissão e antes do resultado da Form/pagamento; o buff não comprova cast concluído ou pago [cast-order]. |
| API, autoridade e deduplicação | APIs nativas `SpellCastEvent` e `SpellDamageEvent.Pre` existem; o helper de dano relê damage/source modificados e pode recusar ou cancelar o golpe depois [damage-pipeline]. O dispatcher percorre instâncias, enquanto L é máximo global. Primeiro callback pode consumir o fogo, mudando a condição dos seguintes; não interpretar número de callbacks como duração/dano acumulados. Sem tag persistente própria, `getInitTag` default null; status e equipamento têm autoridades distintas [slot] [component]. |
| Evidência e pendências | Source e JSON gerado pinados; extensão de duração anunciada na descrição não possui consumidor confirmado no recorte que referencia IMMOLATE_EFFECT. Confirmar lado/ordem, composição com outros listeners, remoção de bloco e gameplay antes de bridge. Release SHA não prova registry/body deste Thread; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. |

## Divergência editorial e estado confirmado

O provider descreve dano adicional **e maior duração** para fire spells [perk]. Os usos de `IMMOLATE_EFFECT` encontrados neste source são a criação do status, seu registro e o bônus em `ArsEvents`; a classe do status não implementa tick ou scaling de duração [status] [fire-damage]. Portanto esta ficha comprova o bônus consumido de dano e os100 ticks do buff, sem transformar a frase sobre duração numa fórmula ou hook de duração verificados.

O `onSpellCast` e o listener de dano não possuem um guard local de lado; o caminho autoritativo precisa seguir o pipeline do Ars, não chamadas diretas do cliente. O simples fato de receber SpellCastEvent não é settlement da magia: cancelamento por outro listener, falha da Form e pagamento são etapas separadas [cast-order].

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
[perk]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/perk/ImmolatePerk.java#L15-L44
[cast-dispatch]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/PerkEvents.java#L88-L95
[fire-damage]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/ArsEvents.java#L51-L55
[status]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/potions/ImmolateEffect.java#L7-L10
[cast-order]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L115-L134
[damage-pipeline]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/IDamageEffect.java#L39-L73
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/thread_immolation.json#L1-L23
