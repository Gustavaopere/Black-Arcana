# Starbuncle Familiar

State: `SOURCE-PINNED 5.13.1 / RUNTIME QA PENDING`

Registry id: `ars_nouveau:familiar_starbuncle`  
Conversion entity: Ars Nouveau `Starbuncle`  
Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Aquisição

O holder reconhece entidades `Starbuncle`. O Ritual of Binding converte uma entidade elegível em Bound Script; usar o script desbloqueia o familiar no capability Ars do jogador.

## Behavior confirmado

- A cada 60 ticks no servidor, se o owner existir, aplica `MOVEMENT_SPEED` por 600 ticks com amplifier `1` ao owner e ao próprio familiar — equivalente a Speed II enquanto o refresh continuar.
- Interação owner-only com item da tag NeoForge `NUGGETS_GOLD` consome 1 nugget fora de creative/infinite materials.
- Essa interação concede Scrying por `3 * 20 * 60 = 3600` ticks, usando `CompoundScryer` com as tags de gold ore do NeoForge e vanilla.
- Também aceita determinadas dyes/cores próprias do Starbuncle para alterar a variante visual.

## Authority e deduplicação

- O Speed refresh, consumo do nugget, persistent familiar ownership e Scrying são Ars-owned.
- O Scrying concedido reutiliza `RitualScrying.grantScrying`; Black Arcana não deve criar um segundo estado de descoberta/visão para o mesmo efeito.
- O familiar não é equivalente à entidade Starbuncle usada em logística/automação. A entidade base é apenas a entidade de conversão do Binding.

## QA pendente

1. Validar refresh de Speed II e remoção ao unsummon/morte/owner unload.
2. Confirmar coexistência de gold-ore Scrying com outros scryers ativos.
3. Validar o consumo do nugget e persistência após relog/chunk unload.
