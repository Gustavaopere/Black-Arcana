# Green Omen — Hexalia 1.3.7

**Estado:** ⚠️ `SOURCE_RELEASE_PINNED_1.3.7 / ACTIVE_WITH_ACCESSORIES_CONDITION / STATIC_TECHNICAL_CATALOG_PENDING_CERTIFICATION` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

- **Provider:** Hexalia · `hexalia` · `hexalia-neoforge-1.3.7.jar` · Minecraft 1.21.1 / NeoForge / Java 21.
- **JAR reportado na modlist física:** SHA-1 `ca90edf1664cf6d44fe7e5318c71069050499c7e`, **não inspecionado nesta contribuição**.
- **Source fixado da release 1.3.7:** [`AstralyaStudios/Hexalia@98c22aaf70e069c616fed5ad2dc56d2b37fcd283`](https://github.com/AstralyaStudios/Hexalia/commit/98c22aaf70e069c616fed5ad2dc56d2b37fcd283). SHA da fonte e SHA do JAR **não demonstram equivalência binária**.
- **Categoria:** acessório mágico passivo ou proc; **não** é uma magia lançada nem um novo ritual.
- **Condição de ativação:** [`Hexalia.initAccessoriesCompat`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/Hexalia.java#L65-L80) carrega `AccessoriesCompat` apenas com o mod `accessories` presente; [`AccessoriesIntegration`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/integration/accessories/AccessoriesIntegration.java#L12-L25) tem lookup default que retorna `false` na ausência da compat. **Presença física/funcionamento do Accessories no pack: não reconfirmado aqui**.

- **Item ID:** `hexalia:green_omen` — [`ModItems.java`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/item/ModItems.java#L180-L200), `stacksTo(1)`.
- **Slot de Accessories (tag de item):** `ring` — [`data/accessories/tags/item/ring.json`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/generated/resources/data/accessories/tags/item/ring.json).

## Descrição e tipo de efeito

Anel que pode copiar os drops existentes de colheitas reconhecidas por uma tag de blocos.

## Targeting, geometria e aplicação

O `BlockState` associado ao evento de drops; não há busca radial, feitiço de crescimento ou modificação de mundos adjacentes no consumer auditado.

## Valores, fórmulas, duração, cooldown e custos

`DOUBLE_DROPS_CHANCE=0.1F` no `GreenOmenEffects.createBonusDrops`. Requer lista de drops não vazia, jogador não criativo, `state.is(ModTags.Blocks.CROPS)` (tag **`c:crops`**, família BLOCK e não ITEM), acessório equipado e rolagem <0.1; cria cópias `ItemStack.copy()` apenas das entradas não vazias. O consumer NeoForge `NeoForgeGreenOmenEvents.onBlockDrops` registra listener de `BlockDropsEvent` com prioridade `LOWEST` e adiciona `ItemEntity` na posição dos drops originais com pickup delay.

**Casting/mana/cooldown:** N/A ao pipeline de feitiço; nenhum custo mágico, barra de Soul ou cooldown por spell está declarado no consumer observado. Isso **não prova** ausência de limitações de outros mods, configs ou eventos do servidor. Sem projétil ou spell level nativo neste item.

## Fluxo causal e evidência de código

`HexaliaNeoForge` registra `NeoForgeGreenOmenEvents` → `BlockDropsEvent` → `createBonusDrops(ServerPlayer,pos,state,stacks)` → novas entidades de item em `event.getDrops()`. Source apresenta procs por oportunidade de drops, **não** uma receita/ritual/cast.

- **Consumer(s) de referência:** [`GreenOmenEffects` L17–40](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/event/GreenOmenEffects.java#L17-L40) · [`NeoForgeGreenOmenEvents` L13–43](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/neoforge/src/main/java/net/astralya/hexalia/neoforge/event/NeoForgeGreenOmenEvents.java#L13-L43) · [`ModTags.Blocks.CROPS` L70–71](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/util/ModTags.java#L70-L71)
- **Registro/ativação:** [`Hexalia.init`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/Hexalia.java#L38-L62) e [`AccessoriesCompat`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/integration/accessories/AccessoriesCompat.java#L8-L28).
- **Tags de slot, não gates de perk:** o JSON de Accessories classifica o item para a família de slot, sem criar tipo de dano, escola ou integração automática com RPG Skill Tree.

## Obtenção

Os cinco itens estão incluídos como opções no [loot table `hexalia:.../accessories/accessory.json`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/resources/data/hexalia/loot_table/accessories/accessory.json), com distribuição dependente dos loot modifiers/contextos e do datapack efetivamente carregado. **Não afirmar chance absoluta de obtenção por baú** a partir do peso dessa tabela. Receita alternativa ou drops efetivos no modpack: `NÃO VERIFICADO`.

## Limites, deduplicação e integração

10% é chance por avaliação elegível de evento de drops, não por item, planta ou stack. O código copia drops já gerados, portanto o ganho pode incluir itens de outros mods se presentes na lista. **Risco source-level:** `createBonusDrops` omite `ItemStack.EMPTY` no array retornado, mas o caller usa `drops.get(index)` para posicionar as cópias; não foi comprovada correspondência posicional se a lista de drops contiver stacks vazios. Não afirmar duplicação de cada bloco quebrado. `LOWEST` não prova ser o último listener absoluto.

Não disparar quebra adicional, recompensas de Mastery por drop duplicado ou nova rolagem ao consumir evento nativo. Claims e duplicação cruzada com mod de loot precisam de QA.

**Autoridade:** Hexalia/Accessories controla slot e aplicação de efeito; RPG Skill Tree pode oferecer progressão/Mastery/gates somente após eventos e contratos verificáveis; Black Arcana não se apropria de casting, perigo arcano, custo ou efeitos desses acessórios. Sem adapter ou mutação do provider habilitados.

## QA pendente

Testar c:crops de vários mods, BlockDropsEvent cancelado, loot com ItemStack.EMPTY, listas de múltiplos stacks, chance/feedback, proteção do mundo e plugins de loot.

A evidência é **documental estática da fonte 1.3.7**, não homologação do JAR, hit/loot confirmado, evento/mixin funcional no servidor real ou `COMPLETE_PERK_READY`. [Inventário agregado prévio](RELICS-WARDS-BINDING-AND-WEARABLES.md).

