# Binding

Status: `SOURCE-PINNED 5.13.1 / FAMILIAR-BINDING RITUAL`

- Registry id: `ars_nouveau:ritual_binding`
- Class: `RitualBinding`
- Completion threshold: `3` progress steps, advanced once per 20 server ticks
- Search radius: `5` blocks
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

At completion, Binding scans every entity within radius 5. For each entity it iterates Ars Nouveau's registered `FamiliarRegistry` holders and applies the holder's provider predicate.

When a holder recognizes an entity:

1. the entity is removed with `RemovalReason.DISCARDED`;
2. Ars spawns its visual poof;
3. the holder's `getOutputItem()` is spawned at that entity's location;
4. a provider sound is played;
5. nearby players are rewarded through Ars' familiar advancement trigger.

The ritual then finishes.

The output item is the provider's bound-script/familiar-binding representation; Black Arcana does not own that identity.

## Black Arcana boundary

Binding is the canonical Ars conversion route from eligible familiar entity to provider binding item. Black Arcana must not independently delete the entity, duplicate the output, or interpret a bound script as a Black Arcana familiar contract.

Any bridge to Familiars & Divination must preserve the registered Ars holder identity and provider lifecycle.

## QA

Source behavior is pinned to 5.13.1. Cross-addon familiar holders registered into the same registry and full-pack entity matching remain runtime/registry QA.

## Dossiê de implementação para perks — ritual exato

- **Classe fonte:** [`RitualBinding.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualBinding.java), fonte `112920ff774831f204031da75b4c4e73d3765157` para Ars 5.13.1.
- **Tick/completion:** no servidor, `getGameTime()%20==0` chama `incrementProgress`; quando `getProgress()>=3` obtém todas entidades em `new AABB(getPos()).inflate(5)`, verifica cada `AbstractFamiliarHolder` do `FamiliarRegistry.getFamiliarHolderMap().values()` por `holder.isEntity.test(entity)`.
- **Conversão provider-owned:** cada entidade reconhecida é descartada (`RemovalReason.DISCARDED`), gera `holder.getOutputItem()` como `ItemEntity`, partículas/som e `ANCriteriaTriggers.FAMILIAR` para jogadores próximos (8 blocos); `setFinished` encerra o ritual. O loop não encerra no primeiro holder; não inferir automaticamente que o registry impede múltiplas correspondências.
- **Perks:** quantidade de familiares, filtros, drops e avanço são domínios do provider; não premiar entidade removida como kill normal nem duplicar Bound Script. Fonte não prova mutation hook do RPG.
- **Mutabilidade externa:** ⛔ nenhum adapter RPG provado que altere lifecycle, Source ou raio sem duplicar settlement; 🟡 fórmula/lógica source-pinned; ⚠️ runtime, receitas/config física, addons e Survival pendentes.

## Certificação técnica estática — familiar binding (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** A identidade classe→ID é comprovada no [manifesto binário do Ars 5.13.1](../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md); o comportamento abaixo foi inspecionado no [`RitualBinding.java` imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualBinding.java). Não há equivalência integral dos métodos do JAR ou validação in-game.

| Campo requerido para perks | Contrato de execução e limite |
|---|---|
| Identidade | `ars_nouveau:ritual_binding`, `RitualBinding`, Ars Nouveau `5.13.1`, fonte `112920ff774831f204031da75b4c4e73d3765157`, publisher JAR SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. |
| Tick e condição de conclusão | `AbstractRitual.tryTick` só despacha rituais iniciados e ainda não finalizados. `RitualBinding.tick` emite partículas no cliente separadamente; **apenas no servidor e `world.getGameTime()%20==0`** incrementa progresso, processando a conversão no mesmo tick se `getProgress()>=3`. A duração não é um cooldown de spell e depende da fase dos ticks do mundo. |
| Targeting e geometria | `getEntitiesOfClass(Entity.class, new AABB(getPos()).inflate(5))`: seleção por **AABB inflada em 5 blocos**, não raio esférico de 5 nem raycast do caster. Para cada entidade, itera **todos** os valores de `FamiliarRegistry.getFamiliarHolderMap()`; predicado de seleção é `familiarHolder.isEntity.test(entity)`. A coleção efetivamente instalada e a ordem de holders são variáveis. |
| Efeito e causalidade | Para cada predicado positivo remove a entidade com `RemovalReason.DISCARDED`, gera partículas e som, instancia `ItemEntity` contendo `holder.getOutputItem()` na posição anterior e recompensa jogadores num raio de 8 pelo gatilho `ANCriteriaTriggers.FAMILIAR`. **Não há `break`** no loop de holders; múltiplos matches podem executar mais de uma vez a sequência e produzir mais de um item no caminho-fonte. Não presumir unicidade ou revalidar `entity.isRemoved()` sem contrato. `setFinished()` ocorre depois da varredura, inclusive sem matches. |
| Dano, projéteis, duração e persistência | Não há chamada local de dano, projectile de spell, buff, lifetime temporizado ou aquisição de kill. `ItemEntity` é resultado da conversão; partículas/advancements não são casts. Persistência e conversão do Familiar pertencem aos sistemas do Ars e dependem de QA físico. |
| Source, ingredientes e cooldown | `RitualBinding` não sobrescreve `AbstractRitual.getSourceCost()`; getter herdado **0 Source** e `consumesSource()` depende desse getter. Isso **não equivale a ritual grátis**: itens de ativação/brazier/config e suas transações não foram demonstrados. Nenhum cooldown/mana de Glyph ou spell de Iron's se aplica a esta execução. |
| Integração e segurança | Ars é authority de `FamiliarRegistry`, entidade, binding output, crafting/ritual e advancement. Black Arcana não deve aplicar remoção ou drop secundário, nem conceder Mastery por cada holder/partícula. Modificações de alvo, quantidade, Source, output ou tempo exigem ponto de mutação demonstrado e deduplicação por execução real; RPG Skill Tree só fornece perks/atributos/Mastery/gates por contrato seguro. |

**Pendência fail-closed:** confirmar holders adicionados por addons, receitas e consumo via brazier, rollback de entidade/item, proteção de mundo, identidade de efeitos e persistência no modpack, multiplayer e teste servidor/cliente. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Nenhuma perk mutadora está autorizada por esta ficha.
