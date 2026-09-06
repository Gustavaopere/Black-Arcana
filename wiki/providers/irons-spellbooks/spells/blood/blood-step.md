# Blood Step — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO / ECONOMIA HEMÁTICA FUTURA AINDA NÃO APLICADA`

## Identidade
- **ID:** `irons_spellbooks:blood_step`
- **Escola:** Blood
- **Raridade:** Uncommon
- **Max level:** 5
- **Função:** teleport/evasion + true invisibility

## Custo atual
- **Mana base:** 30
- **Mana/level:** +10
- **Cooldown:** 12 s
- **Cast:** Instant
- **Spell power base:** 8
- **Spell power/level:** +1

## Efeito
Resolve destino por `TeleportSpell.TeleportData`, raycast/target ou `TeleportSpell.findTeleportLocation`, e executa `Utils.handleSpellTeleport`.

Após teleport:
- reset fall distance;
- seta invisibilidade imediata;
- aplica `TRUE_INVISIBILITY` por 100 ticks (5 s).

**Distância:** `softCap(entityPowerMultiplier) * spellPower`.

## Deduplicação
Já ocupa o nicho de Blood mobility/teleport furtivo. Não criar outro “blood blink” para a expansão hemática sem delta real.

## Migração Blood
A futura regra zero-mana troca somente a fonte de custo; destination safety/teleport do provider deve ser preservada.
