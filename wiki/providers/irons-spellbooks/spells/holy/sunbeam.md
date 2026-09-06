# Sunbeam — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO`

## Identidade
- **ID:** `irons_spellbooks:sunbeam`
- **Escola:** Holy
- **Raridade:** Uncommon
- **Max level:** 10
- **Função:** ataque Holy vertical em posição/alvo

## Custo e casting
- **Mana base:** 40
- **Mana/level:** +10
- **Cooldown:** 20 s
- **Cast:** Instant
- **Spell power base:** 24
- **Spell power/level:** +3
- **Targeting:** até 48 blocos

## Efeito
Cria `SunbeamEntity` no alvo/ponto resolvido pelo raycast.

`damage = getSpellPower(level, caster) * 0.5`

O spell procura posição relativa ao chão quando não há target entity e toca `SUNBEAM_WINDUP` na posição criada.

## Deduplicação
Bloqueia qualquer novo “raio de luz do céu” cuja única função seja dano Holy. Magia Celestial precisa agregar condição celeste, Sanctum/Ressonância, julgamento ou outro contrato distinto.
