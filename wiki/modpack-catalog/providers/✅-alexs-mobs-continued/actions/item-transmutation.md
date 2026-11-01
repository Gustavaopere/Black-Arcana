# Transmutation Table — Item Transmutation

- Provider: **Alex's Mobs Continued** (`alexsmobs`)
- Version: `2.1.13`
- Exact physical/publisher SHA-1: `50ddafdf3d12b33331e4eecb4ab514ae451baadd`
- Owner surface: `alexsmobs:transmutation_table`
- Semantic type: deliberate supernatural item-transmutation action
- State: `COUNTED_EXACT`

## Identity and trigger

The exact installed artifact exposes a direct player-driven Transmutation Table path:

- player opens the provider table/menu;
- an eligible input item is inserted;
- the provider exposes three current transmutation possibilities;
- the player selects one possibility;
- the selection reaches the server-side transmutation settlement.

This is one parameterized **Item Transmutation** identity. Inputs, three displayed candidates, rarity pools, XP amounts, rerolls and result items are parameters of this root rather than separate spell identities.

## Server settlement

Exact artifact evidence closes that the provider:

- replaces the input with the selected transmuted result;
- removes the configured XP-level cost;
- records the provider transmutation state;
- rerolls provider result state after settlement.

Black Arcana must not replay the result replacement or charge a second cost.

## Exact acquisition

The exact artifact contains the provider's shaped Transmutation Table recipe. The audited acquisition surface is sufficient for catalog-level owner reachability and does not inherit the Void Worm summon gate.

## Disposition

- exact action identity: closed;
- exact owner acquisition: closed at catalog level;
- strict state: `COUNTED_EXACT`;
- strict contribution from this root: **+1**.

## Evidence boundary

The provider remains authority for candidate generation, rarity pools, effective XP cost, reroll behavior, table state and result settlement. This card does not invent current tuning values.

Source: `../EXACT-2.1.13-ARTIFACT-AUDIT.md`.

## Matriz de execução e progressão (2026-10-29)

Contrato JAR exato: seleção no menu, settlement server-owned de input/output, débito de XP e reroll são **um único evento causal**. O custo numérico e a autorização de `MessageTransmuteFromMenu` por slot/jogador/sessão **não** estão certificados por teste de modpack; validar `AMC-T01..T03` antes de reduzir XP, aumentar escolhas ou alterar candidatos. Não transformar as três opções em três spells. Mutadores **⛔ fail-closed** sem hook real. Veja [matriz de QA](../EXACT-ARTIFACT-PERK-QA-GATES-2.1.13.md) e [desvio de versão-fonte](../PUBLIC-SOURCE-VERSION-DRIFT-2026-10-29.md).

## Operandos de controle confirmados no JAR 2.1.13 (2026-10-31)

- `MenuTransmutationTable.clickMenuButton` envia `MessageTransmuteFromMenu(playerId, choice)` pelo cliente; a validação do **handler servidor** e do vínculo sessão/jogador não está certificada.
- `TileEntityTransmutationTable.getPossibility(int)` aplica **`Mth.clamp(choice, 0, 2)`**; `hasPossibilities` exige os três elementos presentes e não vazios. Não confundir clamp com rejeição de índice inválido.
- `MenuTransmutationTable.transmute` só entra no settlement se estiver server-side, houver tabela, input não vazio, possibilidades presentes, ratio de tamanhos >0 e XP suficiente **ou** `Abilities.instabuild`.
- Fórmula observada: `ratio = inputMaxStackSize / outputMaxStackSize`; `outputCount = max(1, floor(inputCount / ratio))`. Depois o provider chama `Slot.set(output)`, `giveExperienceLevels(-AMConfig.transmutingExperienceCost)` e `postTransmute`.
- `postTransmute` registra dados por UUID, soma a quantidade de entrada ao contador de transmutação, possui advancement em **1000** itens e define o UUID para reroll. XP efetivo, autorização C2S, concorrência e persistência não passaram por QA físico.

**Proveniência:** [mapa de bytecode SHA-exato](../EXACT-CONTROL-OPERANDS-2.1.13.md). Não certificar mutadores que alterem XP, pools, quantidades, ou reroll.
