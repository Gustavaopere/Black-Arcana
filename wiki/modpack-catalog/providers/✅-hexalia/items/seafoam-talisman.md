# Seafoam Talisman — Hexalia 1.3.7

**Estado:** ⚠️ `SOURCE_RELEASE_PINNED_1.3.7 / ACTIVE_WITH_ACCESSORIES_CONDITION / STATIC_TECHNICAL_CATALOG_PENDING_CERTIFICATION` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

- **Provider:** Hexalia · `hexalia` · `hexalia-neoforge-1.3.7.jar` · Minecraft 1.21.1 / NeoForge / Java 21.
- **JAR reportado na modlist física:** SHA-1 `ca90edf1664cf6d44fe7e5318c71069050499c7e`, **não inspecionado nesta contribuição**.
- **Source fixado da release 1.3.7:** [`AstralyaStudios/Hexalia@98c22aaf70e069c616fed5ad2dc56d2b37fcd283`](https://github.com/AstralyaStudios/Hexalia/commit/98c22aaf70e069c616fed5ad2dc56d2b37fcd283). SHA da fonte e SHA do JAR **não demonstram equivalência binária**.
- **Categoria:** acessório mágico passivo ou proc; **não** é uma magia lançada nem um novo ritual.
- **Condição de ativação:** [`Hexalia.initAccessoriesCompat`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/Hexalia.java#L65-L80) carrega `AccessoriesCompat` apenas com o mod `accessories` presente; [`AccessoriesIntegration`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/integration/accessories/AccessoriesIntegration.java#L12-L25) tem lookup default que retorna `false` na ausência da compat. **Presença física/funcionamento do Accessories no pack: não reconfirmado aqui**.

- **Item ID:** `hexalia:seafoam_talisman` — [`ModItems.java`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/item/ModItems.java#L180-L200), `stacksTo(1)`.
- **Slot de Accessories (tag de item):** `necklace` — [`data/accessories/tags/item/necklace.json`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/generated/resources/data/accessories/tags/item/necklace.json).

## Descrição e tipo de efeito

Acessório aquático passivo que repõe ar do usuário enquanto ele está submerso.

## Targeting, geometria e aplicação

O próprio `Player`; sem alvo à distância, projétil, AOE ofensiva ou seleção de entidades.

## Valores, fórmulas, duração, cooldown e custos

`AccessoryEffects.updateSeafoam`: somente quando `player.isUnderWater()` e `AccessoriesIntegration.isEquipped` são verdadeiros. A cada tick elegível, se `air > 0` e `player.tickCount % 4 != 0`, soma `+1` à reserva de ar. Adicionalmente, a cada `player.tickCount % 200 == 0`, acrescenta `+20`; limita resultado a `player.getMaxAirSupply()`. O ciclo de 200 usa o contador global de ticks do jogador, **não** um temporizador iniciado ao equipar. Quando `air <= 0`, o acréscimo incremental de +1 é bloqueado, mas o caminho de +20 ainda existe na fonte.

**Casting/mana/cooldown:** N/A ao pipeline de feitiço; nenhum custo mágico, barra de Soul ou cooldown por spell está declarado no consumer observado. Isso **não prova** ausência de limitações de outros mods, configs ou eventos do servidor. Sem projétil ou spell level nativo neste item.

## Fluxo causal e evidência de código

`Hexalia.init()` registra `AccessoryEffects.register()` → `TickEvent.PLAYER_POST` → `onPlayerTick` (verifica `!level.isClientSide`) → `updateSeafoam` → `player.setAirSupply`. O método não cobra Soul, mana ou durabilidade e não invoca cast.

- **Consumer(s) de referência:** [`AccessoryEffects` L30–31, L35–48 e L74–86](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/event/AccessoryEffects.java#L74-L86)
- **Registro/ativação:** [`Hexalia.init`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/Hexalia.java#L38-L62) e [`AccessoriesCompat`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/integration/accessories/AccessoriesCompat.java#L8-L28).
- **Tags de slot, não gates de perk:** o JSON de Accessories classifica o item para a família de slot, sem criar tipo de dano, escola ou integração automática com RPG Skill Tree.

## Obtenção

Os cinco itens estão incluídos como opções no [loot table `hexalia:.../accessories/accessory.json`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/resources/data/hexalia/loot_table/accessories/accessory.json), com distribuição dependente dos loot modifiers/contextos e do datapack efetivamente carregado. **Não afirmar chance absoluta de obtenção por baú** a partir do peso dessa tabela. Receita alternativa ou drops efetivos no modpack: `NÃO VERIFICADO`.

## Limites, deduplicação e integração

Valores `+1`/`+20` são unidades de `airSupply`, não saúde, segundos ou pontos de Mana; melhoria de oxigênio não equivale a Water Breathing permanente. A implementação source não mostra priorização contra mods de respiração/exaustão.

Ajustar `airSupply` de outro mod ou duplicar o loop por perks pode causar saturação, proc per-tick e inconsistência de respiração. Não creditar Mastery por recuperação de ar em tick.

**Autoridade:** Hexalia/Accessories controla slot e aplicação de efeito; RPG Skill Tree pode oferecer progressão/Mastery/gates somente após eventos e contratos verificáveis; Black Arcana não se apropria de casting, perigo arcano, custo ou efeitos desses acessórios. Sem adapter ou mutação do provider habilitados.

## QA pendente

Testar água/bubble, ar zerado, equip/desquip, dimensões, cliente-servidor, ticks globais 200 e coexistência com efeitos respiratórios.

A evidência é **documental estática da fonte 1.3.7**, não homologação do JAR, hit/loot confirmado, evento/mixin funcional no servidor real ou `COMPLETE_PERK_READY`. [Inventário agregado prévio](RELICS-WARDS-BINDING-AND-WEARABLES.md).
