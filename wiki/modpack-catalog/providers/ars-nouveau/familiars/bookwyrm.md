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
