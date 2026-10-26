# Bookwyrm Familiar

State: `SOURCE-PINNED 5.13.1 / RUNTIME QA PENDING`

Registry id: `ars_nouveau:familiar_bookwyrm`
Conversion entity: Ars Nouveau `EntityBookwyrm`
Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Aquisição

O holder reconhece `EntityBookwyrm`. Binding converte a entidade em Bound Script e o uso do script desbloqueia o familiar no capability Ars.

## Behavior confirmado

A cada 20 ticks no servidor, com owner resolvido como `Player`, o familiar procura entidades em uma AABB inflada em 5 blocos ao redor do owner.

### Item magnet

Para `ItemEntity`:

- ignora stack vazio;
- ignora pickup delay ativo;
- ignora `PreventRemoteMovement=true` no persistent data;
- ignora entidade não-viva;
- dispara `ItemEntityPickupEvent.Pre` e respeita veto explícito;
- ignora item cujo `ItemEntity.owner` seja igual ao UUID do owner do familiar;
- tenta inserir o stack no inventário principal do jogador via `InventoryManager`/`PlayerMainInvWrapper`;
- mantém na entidade qualquer restante que não couber.

O skip por owner UUID explica o comportamento documentado de não recolher itens arremessados pelo próprio jogador sem transformar essa regra em heurística Black Arcana.

### Experience magnet

Para `ExperienceOrb`:

- ignora orb já removida;
- dispara `PlayerXpEvent.PickupXp` e respeita cancelamento;
- concede `orb.value` ao jogador;
- remove a orb com `DISCARDED`.

## Authority e deduplicação

- A coleta é Ars-owned e respeita eventos NeoForge de pickup/XP; bridges não devem processar os mesmos itens/orbs uma segunda vez.
- Black Arcana não deve creditar kill/loot/mastery apenas porque o Bookwyrm entregou um item ou XP ao jogador.
- O raio de 5 é um magnet do familiar, não um generic ownership radius.

## QA pendente

1. Validar interação com inventários expandidos/Curios e mods que substituam pickup.
2. Confirmar comportamento com itens lançados por dispensers, outros jogadores e automações.
3. Validar event ordering com outros magnet mods do pack.

## Certificação técnica estática — Familiar Bookwyrm (2026-10-26)

**✅ somente `STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Ars Nouveau 5.13.1 JAR SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. A auditoria compilada dos **109 IDs glyph/ritual não cobre esta entidade**. [FamiliarBookwyrm.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/familiar/FamiliarBookwyrm.java) · [BookwyrmFamiliarHolder.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/familiars/BookwyrmFamiliarHolder.java) · [InventoryManager.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/InventoryManager.java) · [FamiliarEntity.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/familiar/FamiliarEntity.java) · [FamiliarEvents.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/FamiliarEvents.java) · [FamiliarData.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/capability/FamiliarData.java) · [PacketSummonFamiliar.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/network/PacketSummonFamiliar.java).

| Campo | Contrato na fonte |
|---|---|
| Aquisição e identidade | `BookwyrmFamiliarHolder` aceita `EntityBookwyrm` e cria `FamiliarBookwyrm(ModEntities.ENTITY_FAMILIAR_BOOKWYRM.get(),world)`; script/holder, `ownerID` e hotkey/toggle pertencem ao Ars. É um magnet nativo, **não é perk Item Pickup nem Source-based crafting**. |
| Frequência/área | `FamiliarBookwyrm.tick()` funciona em servidor quando `level.getGameTime()%20==0`, exige `getOwner() instanceof Player`. Consulta `level.getEntities(owner,new AABB(owner.getOnPos()).inflate(5.0))`; a geometria é **AABB do bloco onde owner pisa expandida em cinco**, não esfera de raio cinco centrada matematicamente nos olhos. |
| Admissão dos itens | Para `ItemEntity`, rejeita stack vazio, `hasPickUpDelay()`, `getPersistentData().getBoolean("PreventRemoteMovement")` e entidade não viva. Posta `ItemEntityPickupEvent.Pre(player,i)`; só tenta inserir se `!prePickup.canPickup().isFalse()` e `!getOwnerID().equals(i.getOwner())`. **O teste do UUID do item impede a coleta remota de drops explicitamente owned pelo próprio player**; isso não elimina todos os itens arremessados de provenance desconhecida. |
| Inventário e remainder | Constrói `new FilterableItemHandler(new PlayerMainInvWrapper(player.inventory),new ArrayList<>())`, embutido em `InventoryManager`. `stack=manager.insertStack(stack)` e `i.setItem(stack)` mantém o restante após tentar inserir no **inventário principal vanilla do jogador**; não presumir transferência direta para curios/baús/storage de outros mods. A fonte não confirma que um `ItemEntity` removido pelo mundo conte como sucesso para perk/XP. |
| XP distinto de itens | `ExperienceOrb` não usa ItemPickup; para orb não removida posta `PlayerXpEvent.PickupXp`, respeita `isCanceled()`, depois `player.giveExperiencePoints(orb.value)` e `orb.remove(Entity.RemovalReason.DISCARDED)`. Esse caminho não é experiência Ars Mastery ou dano do familiar. |
| Identidade persistente/segurança | `FamiliarEntity` elimina familiar sem owner resolvido em checagem de 20 ticks, conserva `ownerID/holderID/terminated` e dados name/color/cosmetic NBT. `FamiliarSummonEvent` é cancelável no packet; o sender não confere retorno de `addFreshEntity` antes de efeitos visuais/setLastSummonedFamiliar. Black Arcana e RPG Skill Tree **não** devem gerar segunda coleta, duplicar ganho de XP nem premiar Mastery pelo mesmo orb. |

**QA:** inventários ampliados, proteção `PreventRemoteMovement`, item-owner UUID, pickup cancels, orbs concorrentes, magnet de outros mods, chunks e owner offline, double-insert e sync. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.
