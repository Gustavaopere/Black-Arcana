# Moonward Ring — Hexalia 1.3.7

**Estado:** ⚠️ `SOURCE_RELEASE_PINNED_1.3.7 / ACTIVE_WITH_ACCESSORIES_CONDITION / STATIC_TECHNICAL_CATALOG_PENDING_CERTIFICATION` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

- **Provider:** Hexalia · `hexalia` · `hexalia-neoforge-1.3.7.jar` · Minecraft 1.21.1 / NeoForge / Java 21.
- **JAR reportado na modlist física:** SHA-1 `ca90edf1664cf6d44fe7e5318c71069050499c7e`, **não inspecionado nesta contribuição**.
- **Source fixado da release 1.3.7:** [`AstralyaStudios/Hexalia@98c22aaf70e069c616fed5ad2dc56d2b37fcd283`](https://github.com/AstralyaStudios/Hexalia/commit/98c22aaf70e069c616fed5ad2dc56d2b37fcd283). SHA da fonte e SHA do JAR **não demonstram equivalência binária**.
- **Categoria:** acessório mágico passivo ou proc; **não** é uma magia lançada nem um novo ritual.
- **Condição de ativação:** [`Hexalia.initAccessoriesCompat`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/Hexalia.java#L65-L80) carrega `AccessoriesCompat` apenas com o mod `accessories` presente; [`AccessoriesIntegration`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/integration/accessories/AccessoriesIntegration.java#L12-L25) tem lookup default que retorna `false` na ausência da compat. **Presença física/funcionamento do Accessories no pack: não reconfirmado aqui**.

- **Item ID:** `hexalia:moonward_ring` — [`ModItems.java`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/item/ModItems.java#L180-L200), `stacksTo(1)`.
- **Slot de Accessories (tag de item):** `ring` — [`data/accessories/tags/item/ring.json`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/generated/resources/data/accessories/tags/item/ring.json).

## Descrição e tipo de efeito

Anel de limpeza passiva de dois efeitos visuais adversos vanilla.

## Targeting, geometria e aplicação

Somente o próprio `Player`; não atua sobre efeitos de entidades próximas ou sobre caster externo.

## Valores, fórmulas, duração, cooldown e custos

`updateMoonward` testa `AccessoriesIntegration.isEquipped(player, MOONWARD_RING)` e chama `player.removeEffect(MobEffects.DARKNESS)` e `player.removeEffect(MobEffects.BLINDNESS)` na rotina `PLAYER_POST`. Não lê amplificador, duração, DamageSource ou escola mágica; **não limpa automaticamente** Night Vision, Wither, Poison, Hexalia Bleeding, Corruption nem efeitos desconhecidos.

**Casting/mana/cooldown:** N/A ao pipeline de feitiço; nenhum custo mágico, barra de Soul ou cooldown por spell está declarado no consumer observado. Isso **não prova** ausência de limitações de outros mods, configs ou eventos do servidor. Sem projétil ou spell level nativo neste item.

## Fluxo causal e evidência de código

`Hexalia.init()` → `AccessoryEffects.register()` → `TickEvent.PLAYER_POST` server-side → `updateMoonward` → duas chamadas a `removeEffect`. Não há cast, evento de counterspell ou custo explícito neste trecho.

- **Consumer(s) de referência:** [`AccessoryEffects` L35–47 e L65–72](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/event/AccessoryEffects.java#L65-L72)
- **Registro/ativação:** [`Hexalia.init`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/Hexalia.java#L38-L62) e [`AccessoriesCompat`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/integration/accessories/AccessoriesCompat.java#L8-L28).
- **Tags de slot, não gates de perk:** o JSON de Accessories classifica o item para a família de slot, sem criar tipo de dano, escola ou integração automática com RPG Skill Tree.

## Obtenção

Os cinco itens estão incluídos como opções no [loot table `hexalia:.../accessories/accessory.json`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/resources/data/hexalia/loot_table/accessories/accessory.json), com distribuição dependente dos loot modifiers/contextos e do datapack efetivamente carregado. **Não afirmar chance absoluta de obtenção por baú** a partir do peso dessa tabela. Receita alternativa ou drops efetivos no modpack: `NÃO VERIFICADO`.

## Limites, deduplicação e integração

A fonte mostra tentativas de remoção por tick, não imunidade no instante de aplicação; efeitos reaplicados durante o tick podem existir temporariamente. Duração do efeito neutralizado e interações com outros listeners não foram medidas.

Uma perk não deve invocar limpeza em outros efeitos arbitrários, nem creditar dispel a cada `removeEffect` sem provar transição real e causalidade. Black Arcana curses continuam em runtime próprio.

**Autoridade:** Hexalia/Accessories controla slot e aplicação de efeito; RPG Skill Tree pode oferecer progressão/Mastery/gates somente após eventos e contratos verificáveis; Black Arcana não se apropria de casting, perigo arcano, custo ou efeitos desses acessórios. Sem adapter ou mutação do provider habilitados.

## QA pendente

Verificar sequências de aplicação/remoção de Darkness e Blindness, recasts no mesmo tick, conflito com magias externas, reload e multiplayer.

A evidência é **documental estática da fonte 1.3.7**, não homologação do JAR, hit/loot confirmado, evento/mixin funcional no servidor real ou `COMPLETE_PERK_READY`. [Inventário agregado prévio](RELICS-WARDS-BINDING-AND-WEARABLES.md).

