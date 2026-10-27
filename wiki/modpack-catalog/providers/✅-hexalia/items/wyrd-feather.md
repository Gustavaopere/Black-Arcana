# Wyrd Feather — Hexalia 1.3.7

**Estado:** ⚠️ `SOURCE_RELEASE_PINNED_1.3.7 / ACTIVE_WITH_ACCESSORIES_CONDITION / STATIC_TECHNICAL_CATALOG_PENDING_CERTIFICATION` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

- **Provider:** Hexalia · `hexalia` · `hexalia-neoforge-1.3.7.jar` · Minecraft 1.21.1 / NeoForge / Java 21.
- **JAR reportado na modlist física:** SHA-1 `ca90edf1664cf6d44fe7e5318c71069050499c7e`, **não inspecionado nesta contribuição**.
- **Source fixado da release 1.3.7:** [`AstralyaStudios/Hexalia@98c22aaf70e069c616fed5ad2dc56d2b37fcd283`](https://github.com/AstralyaStudios/Hexalia/commit/98c22aaf70e069c616fed5ad2dc56d2b37fcd283). SHA da fonte e SHA do JAR **não demonstram equivalência binária**.
- **Categoria:** acessório mágico passivo ou proc; **não** é uma magia lançada nem um novo ritual.
- **Condição de ativação:** [`Hexalia.initAccessoriesCompat`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/Hexalia.java#L65-L80) carrega `AccessoriesCompat` apenas com o mod `accessories` presente; [`AccessoriesIntegration`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/integration/accessories/AccessoriesIntegration.java#L12-L25) tem lookup default que retorna `false` na ausência da compat. **Presença física/funcionamento do Accessories no pack: não reconfirmado aqui**.

- **Item ID:** `hexalia:wyrd_feather` — [`ModItems.java`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/item/ModItems.java#L180-L200), `stacksTo(1)`.
- **Slot de Accessories (tag de item):** `charm` — [`data/accessories/tags/item/charm.json`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/generated/resources/data/accessories/tags/item/charm.json).

## Descrição e tipo de efeito

Talismã de evasão probabilística do evento de dano de combate.

## Targeting, geometria e aplicação

Somente o jogador que recebe a tentativa de dano; target selection é o destinatário do `EntityEvent.LIVING_HURT` fornecido pelo provider, não um raycast.

## Valores, fórmulas, duração, cooldown e custos

`WYRD_DODGE_CHANCE=0.1F`, ou 10% por avaliação elegível de `onLivingHurt`. Requer `entity instanceof Player`, servidor, acessório equipado e `isDirectAttack(source)`; para `DamageTypeTags.IS_PROJECTILE`, exige `source.getDirectEntity() != null`; caso contrário admite apenas `DamageTypes.PLAYER_ATTACK`, `MOB_ATTACK` e `MOB_ATTACK_NO_AGGRO`. Na ativação, emite 6 partículas POOF, áudio Breeze e retorna `EventResult.interruptFalse()`; demais casos retornam `EventResult.pass()`.

**Casting/mana/cooldown:** N/A ao pipeline de feitiço; nenhum custo mágico, barra de Soul ou cooldown por spell está declarado no consumer observado. Isso **não prova** ausência de limitações de outros mods, configs ou eventos do servidor. Sem projétil ou spell level nativo neste item.

## Fluxo causal e evidência de código

`AccessoryEffects.register()` → `EntityEvent.LIVING_HURT.register(onLivingHurt)` → `isDirectAttack` → RNG do jogador → `interruptFalse` quando o proc é aceito. Não possui cast root nem consumo nativo por ataque observado.

- **Consumer(s) de referência:** [`AccessoryEffects` L29, L35–38 e L88–128](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/event/AccessoryEffects.java#L88-L128)
- **Registro/ativação:** [`Hexalia.init`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/Hexalia.java#L38-L62) e [`AccessoriesCompat`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/integration/accessories/AccessoriesCompat.java#L8-L28).
- **Tags de slot, não gates de perk:** o JSON de Accessories classifica o item para a família de slot, sem criar tipo de dano, escola ou integração automática com RPG Skill Tree.

## Obtenção

Os cinco itens estão incluídos como opções no [loot table `hexalia:.../accessories/accessory.json`](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/resources/data/hexalia/loot_table/accessories/accessory.json), com distribuição dependente dos loot modifiers/contextos e do datapack efetivamente carregado. **Não afirmar chance absoluta de obtenção por baú** a partir do peso dessa tabela. Receita alternativa ou drops efetivos no modpack: `NÃO VERIFICADO`.

## Limites, deduplicação e integração

10% é a probabilidade de entrar no ramo de veto sob filtros presentes; **não garante redução observada de 10% de DPS** ou cancelamento universal de dano. Tipos de dano customizados e ordem entre mods precisam ser provados. O código não oferece setter externo de chance nem cooldown.

Não criar segunda rolagem ao observar dano, não interpretar `LIVING_HURT` como ataque já confirmado, não premiar Mastery por cada evento defensivo cancelado, nem omitir dano mágico filtrado.

**Autoridade:** Hexalia/Accessories controla slot e aplicação de efeito; RPG Skill Tree pode oferecer progressão/Mastery/gates somente após eventos e contratos verificáveis; Black Arcana não se apropria de casting, perigo arcano, custo ou efeitos desses acessórios. Sem adapter ou mutação do provider habilitados.

## QA pendente

Testar melee/mob/projectile com e sem `directEntity`, tipos personalizados, ataques indiretos, PvP/teams e interação com Epic Fight/armaduras.

A evidência é **documental estática da fonte 1.3.7**, não homologação do JAR, hit/loot confirmado, evento/mixin funcional no servidor real ou `COMPLETE_PERK_READY`. [Inventário agregado prévio](RELICS-WARDS-BINDING-AND-WEARABLES.md).

